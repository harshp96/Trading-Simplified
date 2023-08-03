import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class OptionTradingStrategy:
    def __init__(self, rsi_period=14, bb_window=20, bb_num_std=2, rsi_buy_threshold=30, rsi_sell_threshold=70):
        self.rsi_period = rsi_period
        self.bb_window = bb_window
        self.bb_num_std = bb_num_std
        self.rsi_buy_threshold = rsi_buy_threshold
        self.rsi_sell_threshold = rsi_sell_threshold

        self.prices = pd.Series()
        self.rsi = pd.Series()
        self.upper_band = pd.Series()
        self.lower_band = pd.Series()
        self.signals = pd.Series()

    def calculate_rsi(self):
        delta = self.prices.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=self.rsi_period).mean()
        avg_loss = loss.rolling(window=self.rsi_period).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def calculate_bollinger_bands(self):
        rolling_mean = self.prices.rolling(window=self.bb_window).mean()
        rolling_std = self.prices.rolling(window=self.bb_window).std()
        upper_band = rolling_mean + (rolling_std * self.bb_num_std)
        lower_band = rolling_mean - (rolling_std * self.bb_num_std)
        return upper_band, lower_band

    def add_new_data_point(self, price):
        self.prices = pd.concat([self.prices, pd.Series(price)])
        self.rsi = self.calculate_rsi()
        upper_band, lower_band = self.calculate_bollinger_bands()
        self.upper_band = pd.concat([self.upper_band, pd.Series(upper_band.iloc[-1])])
        self.lower_band = pd.concat([self.lower_band, pd.Series(lower_band.iloc[-1])])

        if len(self.rsi) < 2:
            signal = 0
        else:
            prev_rsi = self.rsi.iloc[-2]
            prev_price = self.prices.iloc[-2]
            prev_upper_band = self.upper_band.iloc[-2]
            prev_lower_band = self.lower_band.iloc[-2]

            signal = 0
            if prev_rsi < self.rsi_buy_threshold and prev_price < prev_lower_band:
                signal = 1
            elif prev_rsi > self.rsi_sell_threshold and prev_price > prev_upper_band:
                signal = -1

        self.signals = pd.concat([self.signals, pd.Series(signal)])
        return signal

def generate_live_data(start_date, end_date, interval, max_price_change=0.01):
    date_rng = pd.date_range(start=start_date, end=end_date, freq=interval)
    prices = [100.0]  # Initial price
    for i in range(1, len(date_rng)):
        prev_price = prices[-1]
        price_change = np.random.uniform(-max_price_change, max_price_change)
        new_price = prev_price * (1 + price_change)
        prices.append(new_price)
    data = pd.DataFrame({'Close': prices}, index=date_rng)
    return data

# Sample data for demonstration (you can replace this with real-time data)
start_date = '2023-01-01'
end_date = '2023-01-05'
interval = '15T' # 15T 1H
max_price_change = 0.01

prices = generate_live_data(start_date, end_date, interval, max_price_change)
date_rng = pd.date_range(start='2023-01-01', end='2023-01-05', freq=interval)

# Initialize the option trading strategy
strategy = OptionTradingStrategy()

# Apply the option trading strategy to the sample data
signals = []
for price in prices.values:
    signal = strategy.add_new_data_point(price)
    signals.append(signal)

# Convert the signals to a DataFrame with the same index as the price data
signals_df = pd.DataFrame({'Signal': signals}, index=prices.index)

# Plotting the signals and Bollinger Bands
plt.figure(figsize=(12, 6))
plt.plot(prices.index, prices, label='Price', color='blue')
plt.plot(signals_df.loc[signals_df['Signal'] == 1].index, prices[signals_df['Signal'] == 1], '^', markersize=8, color='g', label='Buy Signal')
plt.plot(signals_df.loc[signals_df['Signal'] == -1].index, prices[signals_df['Signal'] == -1], 'v', markersize=8, color='r', label='Sell Signal')
# plt.plot(prices.index, strategy.upper_band, label='Upper Band', color='grey', linestyle='dotted')
# plt.plot(prices.index, strategy.lower_band, label='Lower Band', color='grey', linestyle='dotted')
plt.fill_between(prices.index, strategy.upper_band, strategy.lower_band, color='gray', alpha=0.2, label='Bollinger Bands')
plt.legend()
plt.title('Option Trading Strategy with RSI and Bollinger Bands ({} Interval)'.format(interval))
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
