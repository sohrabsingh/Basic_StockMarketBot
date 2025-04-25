```markdown
# 📈 Stock Market Analysis Bot (Tkinter GUI)

A Python desktop application that allows you to analyze stock data visually and statistically using **Tkinter GUI**, **yfinance**, and **technical indicators** (SMA, Bollinger Bands, RSI, MACD). Includes basic sentiment-style NLP feedback and interactive charts.

---

## 🧰 Features

- 📊 Live stock data fetching from Yahoo Finance via `yfinance`
- 🧮 Technical analysis indicators:
  - Simple Moving Average (SMA)
  - Bollinger Bands
  - Relative Strength Index (RSI)
  - MACD and Signal Line
- 📉 Volume and price chart visualization using `matplotlib`
- 🧠 Simple NLP-style insights based on market conditions
- 🪟 Modern Tkinter GUI with tabbed interface

---

## 🛠️ Requirements

Install the dependencies using pip:

```bash
pip install yfinance pandas matplotlib ta tabulate alphavantage
```

> Tkinter comes preinstalled with Python in most distributions. If not:
> ```bash
> sudo apt-get install python3-tk
> ```

---

## 🚀 How to Run

Run the app using:

```bash
python Final_Yfinance.py
```
or
```bash
python Final_AlphaVantage.py
```
---


## 🔍 Usage

1. Enter a stock symbol (e.g., `AAPL`, `TSLA`, `INFY.NS`).
2. Select a time period (1d, 5d, 1mo, 3mo, 6mo, 1y).
3. Click **Analyze**.
4. View charts, indicators, and AI-generated insights.

---

## 📦 File Structure

```
.
├── Final_AlphaVantage.py     # Main application file
├── Final_Yfinance.py     # Main application file
├── README.md             # This file
```

---

## 💡 Notes

- The default currency conversion (USD to INR) is set at 82.5 manually.
- For more advanced AI insights, consider integrating real-time NLP models or financial APIs.

---

## 🧑‍💻 Author

Developed by [Sohrab Pritpal Singh, Harshit Sharma, Arnav Sinha]
```
