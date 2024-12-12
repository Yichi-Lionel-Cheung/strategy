# Strategy

This repository contains my personal trading strategies. The strategies are implemented by [LEAN](https://github.com/QuantConnect/Lean) and backtested by [QuantConnect](https://www.quantconnect.com/). Note that the strategies are for educational purposes only and should not be considered as financial advice.

## Setup and Backtest

1. Install [LEAN CLI](https://github.com/QuantConnect/Lean) according to the official guide

2. Initialize the project

    ```console
    cd strategy
    lean init
    ```

3. Backtest some strategies (cloud backtest recommended)

    ```console
    cd strategy
    lean cloud backtest --push --open <strategy-name>
    ```

## Strategy Zoo

+ [Overnight](overnight/)
+ [Pairs Trading](pairs_trading/)

### Under Development

+ Momentum
+ Mean Reversion
+ FinBERT
+ ...
