# region imports
from AlgorithmImports import *
import numpy as np
from datetime import datetime, timedelta

# endregion

class Pairstrading(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2020, 1, 1)  # Set Start Date
        self.set_end_date(2024, 12, 1)  # Set End Date
        self.set_cash(1000000)  # Set Strategy Cash

        # TODO: pick pairs of stocks according to the correlation
        # Add pairs
        self.pep = self.AddEquity("PEP", Resolution.DAILY).symbol
        self.ko = self.AddEquity("KO", Resolution.DAILY).symbol
        
        self.window = 30
        self.spread = RollingWindow[float](self.window)
        self.entry_threshold = 2.0
        
        # Warm up the algorithm
        self.set_warmup(timedelta(days=self.window))
        self.today_traded = False
        
    def on_data(self, data: Slice):
        if not (data.bars.contains_key(self.pep) and data.bars.contains_key(self.ko)):
            return
        
        # Calculate spread
        price_pep = data.bars[self.pep].close
        price_ko = data.bars[self.ko].close
        self.spread.add(price_pep - price_ko)
        
        if not self.spread.is_ready:
            return
        
        # Calculate Z-score
        mean = np.mean([x for x in self.spread])
        std = np.std([x for x in self.spread])
        z_score = (self.spread[0] - mean) / std
        
        if not self.today_traded:
            self.today_traded = True
            if z_score > self.entry_threshold:
                # Short PEP, Long KO
                self.set_holdings(self.pep, -0.5)
                self.set_holdings(self.ko, 0.5)
                self.log(f"Short PEP, Long KO: {z_score}, date: {self.Time}")
            elif z_score < -self.entry_threshold:
                # Long PEP, Short KO
                self.set_holdings(self.pep, 0.5)
                self.set_holdings(self.ko, -0.5)
                self.log(f"Long PEP, Short KO: {z_score}, date: {self.Time}")

        self.today_traded = False