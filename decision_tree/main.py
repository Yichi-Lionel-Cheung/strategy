# region imports
from AlgorithmImports import *
import xgboost as xgb
import joblib
import numpy as np
# endregion

class decision_tree(QCAlgorithm):

    def initialize(self):
        # Locally Lean installs free sample data, to download more data please visit https://www.quantconnect.com/docs/v2/lean-cli/datasets/downloading-data
        self.set_start_date(2020, 1, 1)  # Set Start Date
        self.set_end_date(2024, 12, 1)  # Set End Date
        self.set_cash(1000000)  # Set Strategy Cash
        self.ko = self.add_equity("KO", resolution=Resolution.DAILY).symbol
        training_length = 252 * 2
        self.training_data = [RollingWindow[float](training_length) for _ in range(5)]
        history = self.history[TradeBar](self.ko, training_length, Resolution.DAILY)
        for bar in history:
            self.training_data[0].add(bar.close)
            self.training_data[1].add(bar.high)
            self.training_data[2].add(bar.low)
            self.training_data[3].add(bar.open)
            self.training_data[4].add(bar.volume)
        
        if self.object_store.contains_key('xgboost'):
            model_key = 'xgboost'
            file_name = self.object_store.get_file_path(model_key)
            self.model = joblib.load(file_name)
        else:
            self.train(self.training_method)
        
        self.train(self.date_rules.every(DayOfWeek.SUNDAY), self.time_rules.at(8, 0), self.training_method)

    def get_features_and_labels(self, n_steps=5):
    # Reverse data for chronological order
        close_prices = np.array(list(self.training_data[0])[::-1])
        high_prices = np.array(list(self.training_data[1])[::-1])
        low_prices = np.array(list(self.training_data[2])[::-1])
        open_prices = np.array(list(self.training_data[3])[::-1])
        volume = np.array(list(self.training_data[4])[::-1])

        # Compute smoothed features
        def smooth(prices):
            return (np.roll(prices, -1) - prices) * 0.5 + prices * 0.5

        df_close = smooth(close_prices)[:-1]
        df_high = smooth(high_prices)[:-1]
        df_low = smooth(low_prices)[:-1]
        df_open = smooth(open_prices)[:-1]
        df_volume = smooth(volume)[:-1]

        features = []
        labels = []

        for i in range(len(df_close) - n_steps):
            feature = np.concatenate([
                df_close[i:i+n_steps],
                df_high[i:i+n_steps],
                df_low[i:i+n_steps],
                df_open[i:i+n_steps],
                df_volume[i:i+n_steps],
            ])
            features.append(feature)
            labels.append(df_close[i + n_steps])  # Predict next day's price

        features = np.array(features)
        labels = np.array(labels)

        features = (features - features.mean(axis=0)) / features.std(axis=0)
        labels = (labels - labels.mean()) / labels.std()

        d_matrix = xgb.DMatrix(features, label=labels)
        return d_matrix

    
    def training_method(self):
        d_matrix = self.get_features_and_labels()

        params = {
            'booster': 'gbtree',
            'colsample_bynode': 0.8,
            'learning_rate': 0.1,
            'lambda': 0.1,
            'max_depth': 25,
            'num_parallel_tree': 100,
            'objective': 'reg:squarederror',
            'subsample': 0.8,
        }

        self.model = xgb.train(params, d_matrix, num_boost_round=10)
        


    def on_data(self, data: Slice):
        """on_data event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        """
        if self.ko in data.bars:
            self.training_data[0].add(data.bars[self.ko].close)
            self.training_data[1].add(data.bars[self.ko].high)
            self.training_data[2].add(data.bars[self.ko].low)
            self.training_data[3].add(data.bars[self.ko].open)
            self.training_data[4].add(data.bars[self.ko].volume)
        
        new_d_matrix = self.get_features_and_labels()
        prediction = self.model.predict(new_d_matrix)
        prediction = prediction.flatten()

        if float(prediction[-1]) > float(prediction[-2]):
            self.set_holdings(self.ko, 1)
        else:
            self.set_holdings(self.ko, -1)
        

    def on_end_of_algorithm(self):
        model_key = 'xgboost'
        file_name = self.object_store.get_file_path(model_key)
        joblib.dump(self.model, file_name)
        self.object_store.save(model_key)