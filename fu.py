import tkinter as tk
from tkinter import ttk, messagebox
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tabulate import tabulate
import ta  # For technical analysis indicators

class StockMarketBot:
    def __init__(self, api_key):
        self.ts = TimeSeries(key=api_key, output_format='pandas')  # Initialize Alpha Vantage API client

    def get_stock_data(self, symbol, period='1mo'):
        try:
            if period == '1mo':
                period = 'daily'
            elif period == '3mo':
                period = 'weekly'
            elif period == '1y':
                period = 'weekly'
            data, meta_data = self.ts.get_daily(symbol=symbol, outputsize='full')
            return data
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
            return None

class StockMarketGUI:
    def __init__(self, root, api_key):
        self.root = root
        self.root.title("Stock Market Analysis")
        self.root.geometry("1200x800")

        self.bot = StockMarketBot(api_key)
        self.current_symbol = ""
        self.update_interval = 60000

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
        try:
            data = self.bot.get_stock_data(symbol, period)
            if data is not None:
                data = data.sort_index()
                period_map = {
                    '1d': 1,
                    '5d': 5,
                    '1mo': 30,
                    '3mo': 90,
                    '6mo': 180,
                    '1y': 365
                }
                days = period_map.get(period, 90)
                data = data.last(f'{days}D')
                return data
            return None
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
            return None

    def plot_chart(self, data):
        self.figure.clear()
        gs = self.figure.add_gridspec(2, 1, height_ratios=[1, 1], hspace=0.3) # Adjust height ratios

        ax1 = self.figure.add_subplot(gs[0, 0])
        ax1.plot(data.index, data['4. close'], label='Close Price', color='blue')

        # Calculate SMA
        sma_window = 20
        sma = data['4. close'].rolling(window=sma_window).mean()
        ax1.plot(data.index, sma, label=f'SMA ({sma_window})', color='orange', linestyle='--')

        # Calculate Bollinger Bands
        window = 20
        rolling_mean = data['4. close'].rolling(window=window).mean()
        rolling_std = data['4. close'].rolling(window=window).std()
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
        ax2.bar(data.index, data['5. volume'], label='Volume', color='skyblue')
        ax2.set_ylabel('Volume')
        ax2.grid(True)
        ax2.legend(loc='upper left')

        # RSI subplot
        # ax3 = self.figure.add_subplot(gs[2, 0], sharex=ax1)
        # rsi_indicator = ta.momentum.RSIIndicator(close=data['4. close'], window=14)
        # data['rsi'] = rsi_indicator.rsi()
        # ax3.plot(data.index, data['rsi'], label='RSI (14)', color='purple')
        # ax3.axhline(70, color='red', linestyle='--', alpha=0.5)
        # ax3.axhline(30, color='green', linestyle='--', alpha=0.5)
        # ax3.set_ylabel('RSI')
        # ax3.set_ylim(0, 100)
        # ax3.grid(True)
        # ax3.legend(loc='upper left')

        self.figure.tight_layout()
        self.canvas.draw()

    def update_indicators(self, data):
        sma_window = 20
        sma = data['4. close'].rolling(window=sma_window).mean().iloc[-1]

        rsi_indicator = ta.momentum.RSIIndicator(close=data['4. close'], window=14)
        rsi = rsi_indicator.rsi().iloc[-1]

        exp1 = data['4. close'].ewm(span=12, adjust=False).mean()
        exp2 = data['4. close'].ewm(span=26, adjust=False).mean()
        macd_line = exp1 - exp2  # Keep the entire MACD Series
        signal = macd_line.ewm(span=9, adjust=False).mean().iloc[-1] # Calculate signal on the MACD Series
        macd = macd_line.iloc[-1] # Get the last MACD value

        current_price = data['4. close'].iloc[-1]
        prev_close = data['4. close'].iloc[-2]
        price_change = ((current_price - prev_close) / prev_close) * 100

        text = f"""Current Price: ${current_price:.2f} ({price_change:+.2f}%)\n\n"""
        text += f"SMA ({sma_window}): ${sma:.2f}"
        text += " (Bullish)" if current_price > sma else " (Bearish)"

        text += f"\n\nRSI (14): {rsi:.2f}"
        if rsi > 70:
            text += " (Overbought - Consider Selling)"
        elif rsi < 30:
            text += " (Oversold - Consider Buying)"
        else:
            text += " (Neutral)"

        text += f"\n\nMACD: {macd:.2f}"
        text += " (Bullish Signal)" if macd > signal else " (Bearish Signal)"

        self.indicators_text.delete(1.0, tk.END)
        self.indicators_text.insert(tk.END, text)

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

    def nlp_func(self, symbol, data):
        try:
            current_price = data['4. close'].iloc[-1]
            rsi_indicator = ta.momentum.RSIIndicator(close=data['4. close'], window=14)
            rsi = rsi_indicator.rsi().iloc[-1]
            sentiment = "positive" if current_price > data['4. close'].iloc[-2] else "negative"

            response = f"""
                🤖 ChatBot Analysis for {symbol}:

                - The current stock price is ${current_price:.2f}.
                - The recent trend seems to be {sentiment}.
                - The RSI is at {rsi:.2f}, indicating it is {"overbought" if rsi > 70 else "oversold" if rsi < 30 else "neutral"}.
                - Based on this, you may want to {"wait for a dip" if rsi > 70 else "consider buying" if rsi < 30 else "hold your position"}.

                📊 I hope this helps! Type another query or click Analyze again.
            """
            self.nlp_text.delete(1.0, tk.END)
            self.nlp_text.insert(tk.END, response.strip())

        except Exception as e:
            self.nlp_text.delete(1.0, tk.END)
            self.nlp_text.insert(tk.END, f"Error processing NLP response: {str(e)}")

def main():
    root = tk.Tk()
    api_key = "HHB2E7F9CS4GTSR1"  # Replace with your Alpha Vantage API key
    app = StockMarketGUI(root, api_key)
    root.mainloop()

if __name__ == "__main__":
    main()
