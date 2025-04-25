import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tabulate import tabulate
import ta  # For technical analysis indicators

class StockMarketBot:
    def get_stock_data(self, symbol, period='1mo'):
        try:
            ticker = yf.Ticker(symbol)
            if period == '1d':
                data = ticker.history(period='1d', interval='60m')
            elif period == '5d':
                data = ticker.history(period='5d', interval='60m')
            elif period == '1mo':
                data = ticker.history(period='1mo', interval='1d')
            elif period == '3mo':
                data = ticker.history(period='3mo', interval='1wk')
            elif period == '6mo':
                data = ticker.history(period='6mo', interval='1wk')
            elif period == '1y':
                data = ticker.history(period='1y', interval='1wk')
            else:
                messagebox.showerror("Error", f"Invalid period: {period}")
                return None

            if not data.empty:
                return data
            else:
                messagebox.showerror("Error", f"No data found for symbol: {symbol} and period: {period}")
                return None
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
            messagebox.showerror("Error", f"Error fetching data for {symbol}: {str(e)}")
            return None

class StockMarketGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Market Analysis")
        self.root.geometry("1200x800")

        self.bot = StockMarketBot()
        self.current_symbol = ""
        self.update_interval = 60000
        self.usd_to_inr = 82.5  # Example conversion rate, ideally fetch this dynamically

        self.input_frame = ttk.Frame(root, padding="10")
        self.input_frame.pack(fill=tk.X)

        self.title_frame = ttk.Frame(root, padding="5")
        self.title_frame.pack(fill=tk.X)
        self.company_name_label = ttk.Label(self.title_frame, text="", font=("Helvetica", 16, "bold"))
        self.company_name_label.pack()

        self.content_frame = ttk.Frame(root, padding="10")
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.input_frame, text="Stock Symbol:").pack(side=tk.LEFT)
        self.symbol_entry = ttk.Entry(self.input_frame, width=10)
        self.symbol_entry.pack(side=tk.LEFT, padx=5)

        self.period_var = tk.StringVar(value="1mo")
        ttk.Label(self.input_frame, text="Period:").pack(side=tk.LEFT, padx=(10, 0))
        period_combo = ttk.Combobox(self.input_frame, textvariable=self.period_var,
                                     values=["1d", "5d", "1mo", "3mo", "6mo", "1y"],
                                     width=5)
        period_combo.pack(side=tk.LEFT, padx=5)

        ttk.Button(self.input_frame, text="Analyze", command=self.analyze_stock).pack(side=tk.LEFT, padx=10)

        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.chart_tab = ttk.Frame(self.notebook)
        self.indicators_tab = ttk.Frame(self.notebook)
        self.nlp_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.chart_tab, text="Price Chart")
        self.notebook.add(self.indicators_tab, text="Technical Indicators")
        self.notebook.add(self.nlp_tab, text="Insights")

        self.figure = Figure(figsize=(12, 8))  # Increased figure height to accommodate more plots
        self.canvas = FigureCanvasTkAgg(self.figure, self.chart_tab)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.indicators_text = tk.Text(self.indicators_tab, wrap=tk.WORD, height=20)
        self.indicators_text.pack(fill=tk.BOTH, expand=True)

        self.nlp_text = tk.Text(self.nlp_tab, wrap=tk.WORD, height=20)
        self.nlp_text.pack(fill=tk.BOTH, expand=True)

    def get_stock_data(self, symbol, period='1mo'):
        data = self.bot.get_stock_data(symbol, period)
        if data is not None and not data.empty:
            data = data.sort_index(ascending=True)
            return data
        return None

    def plot_chart(self, data):
        self.figure.clear()
        gs = self.figure.add_gridspec(2, 1, height_ratios=[1, 1], hspace=0.3) # Adjust height ratios

        ax1 = self.figure.add_subplot(gs[0, 0])
        ax1.plot(data.index, data['Close'], label='Close Price', color='blue')

        # Calculate SMA
        sma_window = 20
        sma = data['Close'].rolling(window=sma_window).mean()
        ax1.plot(data.index, sma, label=f'SMA ({sma_window})', color='orange', linestyle='--')

        # Calculate Bollinger Bands
        window = 20
        rolling_mean = data['Close'].rolling(window=window).mean()
        rolling_std = data['Close'].rolling(window=window).std()
        upper_band = rolling_mean + (rolling_std * 2)
        lower_band = rolling_mean - (rolling_std * 2)

        ax1.plot(data.index, upper_band, label='Bollinger Upper', color='red', linestyle='--')
        ax1.plot(data.index, lower_band, label='Bollinger Lower', color='green', linestyle='--')
        ax1.fill_between(data.index, lower_band, upper_band, color='grey', alpha=0.2)

        ax1.set_title(f'{self.current_symbol} Stock Price with SMA and Bollinger Bands')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Price')
        ax1.grid(True)
        ax1.legend(loc='upper left')

        # Volume subplot
        ax2 = self.figure.add_subplot(gs[1, 0], sharex=ax1)
        ax2.bar(data.index, data['Volume'], label='Volume', color='skyblue')
        ax2.set_ylabel('Volume')
        ax2.grid(True)
        ax2.legend(loc='upper left')

        self.figure.tight_layout()
        self.canvas.draw()

    def calculate_indicators(self, data):
        # Calculate SMA and Bollinger Bands
        sma_20 = data['Close'].rolling(window=20).mean()
        std_dev = data['Close'].rolling(window=20).std()
        bollinger_upper = sma_20 + (std_dev * 2)
        bollinger_lower = sma_20 - (std_dev * 2)

        # Calculate RSI
        rsi_indicator = ta.momentum.RSIIndicator(close=data['Close'], window=14)
        rsi = rsi_indicator.rsi()

        # Calculate MACD
        macd_indicator = ta.trend.MACD(close=data['Close'])
        macd = macd_indicator.macd()
        signal = macd_indicator.macd_signal()

        return sma_20, rsi, macd, signal, bollinger_upper, bollinger_lower

    def update_indicators(self, data):
        if len(data) < 20:
            self.indicators_text.delete(1.0, tk.END)
            self.indicators_text.insert(tk.END, "Insufficient data to calculate indicators")
            return

        sma_20, rsi, macd, signal, bollinger_upper, bollinger_lower = self.calculate_indicators(data)

        current_price = data['Close'].iloc[-1]
        prev_close = data['Close'].iloc[-2]
        price_change = ((current_price - prev_close) / prev_close) * 100

        indicators_text = f"Current Price: ₹{current_price:.2f} ({price_change:+.2f}%)\n\n"
        indicators_text += f"SMA (20): ₹{sma_20.iloc[-1]:.2f}"
        indicators_text += " (Bullish)" if current_price > sma_20.iloc[-1] else " (Bearish)"

        indicators_text += f"\n\nBollinger Bands:"
        indicators_text += f"\n  Upper: ₹{bollinger_upper.iloc[-1]:.2f}"
        indicators_text += f"\n  Lower: ₹{bollinger_lower.iloc[-1]:.2f}"
        if current_price > bollinger_upper.iloc[-1]:
            indicators_text += " (Potentially Overbought)"
        elif current_price < bollinger_lower.iloc[-1]:
            indicators_text += " (Potentially Oversold)"

        indicators_text += f"\n\nRSI (14): {rsi.iloc[-1]:.2f}"
        if rsi.iloc[-1] > 70:
            indicators_text += " (Overbought - Consider Selling)"
        elif rsi.iloc[-1] < 30:
            indicators_text += " (Oversold - Consider Buying)"
        else:
            indicators_text += " (Neutral)"

        indicators_text += f"\n\nMACD: {macd.iloc[-1]:.2f}"
        indicators_text += " (Bullish Signal)" if macd.iloc[-1] > signal.iloc[-1] else " (Bearish Signal)"

        # Add trading volume analysis
        avg_volume = data['Volume'].mean()
        current_volume = data['Volume'].iloc[-1]
        volume_ratio = (current_volume / avg_volume) * 100

        indicators_text += f"\n\nVolume Analysis:"
        indicators_text += f"\nCurrent Volume: {current_volume:,.0f}"
        indicators_text += f"\nAverage Volume: {avg_volume:,.0f}"
        indicators_text += f"\nVolume Ratio: {volume_ratio:.1f}% of Average"

        self.indicators_text.delete(1.0, tk.END)
        self.indicators_text.insert(tk.END, indicators_text)

    def analyze_stock(self):
        symbol = self.symbol_entry.get().upper()
        if not symbol:
            messagebox.showwarning("Warning", "Please enter a stock symbol")
            return

        self.current_symbol = symbol
        data = self.get_stock_data(symbol, self.period_var.get())
        if data is not None and not data.empty:
            self.plot_chart(data)
            self.update_indicators(data)
            self.nlp_func(symbol, data)
        else:
            messagebox.showerror("Error", f"Could not retrieve data for {symbol}")

    def nlp_func(self, symbol, data):
        try:
            current_price = data['Close'].iloc[-1]
            rsi_value = ta.momentum.RSIIndicator(close=data['Close'], window=14).rsi().iloc[-1]
            sentiment = "positive" if current_price > data['Close'].iloc[-2] else "negative"

            response = f"""
                🤖 ChatBot Analysis for {symbol}:

                - The current stock price is ₹{current_price:.2f}.
                - The recent trend seems to be {sentiment}.
                - The RSI is at {rsi_value:.2f}, indicating it is {"overbought" if rsi_value > 70 else "oversold" if rsi_value < 30 else "neutral"}.
                - Based on this, you may want to {"wait for a dip" if rsi_value > 70 else "consider buying" if rsi_value < 30 else "hold your position"}.

                📊 I hope this helps! Type another query or click Analyze again.
            """
            self.nlp_text.delete(1.0, tk.END)
            self.nlp_text.insert(tk.END, response.strip())

        except Exception as e:
            self.nlp_text.delete(1.0, tk.END)
            self.nlp_text.insert(tk.END, f"Error processing NLP response: {str(e)}")

def main():
    root = tk.Tk()
    app = StockMarketGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
