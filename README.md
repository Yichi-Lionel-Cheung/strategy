# Strategy

This repository contains my personal trading strategies. The strategies are implemented by [LEAN](https://github.com/QuantConnect/Lean) and backtested by [QuantConnect](https://www.quantconnect.com/).

# Usage

1. Install [LEAN](https://github.com/QuantConnect/Lean) according to the official guide

2. Initialize a new project by `lean init`

```console
lean init
```

3. Backtest some strategies

```console
 lean cloud backtest --push <strategy-name>
```

## Strategy Zoo

+ [Overnight](overnight/)
+ [Pairs Trading](pairs_trading/)

### TBD

+ Momentum
+ Mean Reversion
+ FinBERT
+ ...
