# region imports
from AlgorithmImports import *
# endregion

class Overnight(QCAlgorithm):

    def initialize(self):
        # Locally Lean installs free sample data, to download more data please visit https://www.quantconnect.com/docs/v2/lean-cli/datasets/downloading-data
        self.set_start_date(2020, 1, 1)  # Set Start Date
        self.set_end_date(2024, 12, 1)  # Set End Date
        self.set_cash(1000000)  # Set Strategy Cash
        self.tqqq = self.add_equity("TQQQ", resolution=Resolution.MINUTE).symbol
        self.holding_flag = False


    def on_data(self, data: Slice):
        """on_data event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        """
        # get now cash amount
        cash = self.portfolio.cash
        if not self.portfolio.invested and self.holding_flag == False:
            self.market_on_close_order(self.tqqq, cash // data[self.tqqq].close)
            self.holding_flag = True
            self.log(f"Buying {cash // data[self.tqqq].close} shares of TQQQ at {data[self.tqqq].close} in date {self.Time}")

    def on_order_event(self, order_event):
        if order_event.status == OrderStatus.FILLED and self.holding_flag == True:
            self.market_on_close_order(self.tqqq, -self.portfolio[self.tqqq].quantity)
            self.holding_flag = False
            self.log(f"Selling {self.portfolio[self.tqqq].quantity} shares of TQQQ at {self.portfolio[self.tqqq].price} in date {self.Time}")