# Pairs Trading

This strategy is based on the observation that 2 stocks tend to move together. The strategy buys the underperforming stock and sells the outperforming stock when the spread between the two stocks is greater than a certain threshold.

We set `KO` and `PEP` as the pair of stocks to trade. We buy `KO` and sell `PEP` when the spread between the two stocks is greater than 2 standard deviations, vice versa.

## Backtest Result

From `2020-01-01` to `2024-12-01`

| Statistic               | Value          | Statistic                 | Value             |
|--------------------------|----------------|---------------------------|-------------------|
| Equity                  | $1,350,694.62 | Fees                      | -$3,826.56       |
| Holdings                | $1,326,929.26 | Net Profit                | $317,142.86      |
| Probabilistic           | 22.187%       | Return                    | 35.07%           |
| Unrealized              | $33,486.39    | Volume                    | $58,048,933.00   |
| Total Orders            | 240           | Average Win               | 0.99%            |
| Average Loss            | -0.49%        | Compounding Annual Return | 6.601%           |
| Drawdown                | 11.300%       | Expectancy                | 0.350            |
| Start Equity            | $1,000,000    | End Equity                | $1,350,694.62    |
| Net Profit Percentage   | 35.069%       | Sharpe Ratio              | 0.343            |
| Sortino Ratio           | 0.432         | Probabilistic Sharpe Ratio| 22.187%          |
| Loss Rate               | 55%           | Win Rate                  | 45%              |
| Profit-Loss Ratio       | 2.00          | Alpha                     | 0.018            |
| Beta                    | 0.052         | Annual Standard Deviation | 0.065            |
| Annual Variance         | 0.004         | Information Ratio         | -0.364           |
| Tracking Error          | 0.181         | Treynor Ratio             | 0.431            |
| Total Fees              | $3,826.56     | Estimated Strategy Capacity| $120,000,000.00  |
| Lowest Capacity Asset   | PEP R735QTJ8XC9X | Portfolio Turnover      | 2.84%            |

