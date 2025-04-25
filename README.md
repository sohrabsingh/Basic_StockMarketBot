```markdown
# 📈 Stock Market Analysis Bot (Tkinter GUI)

A Python desktop application for visual and statistical stock data analysis using **Tkinter GUI**, **yfinance**, and technical indicators like **SMA**, **Bollinger Bands**, **RSI**, and **MACD**. Includes simple NLP-style market insights and interactive chart visualizations.

---

## 🧰 Features

- 📊 Live stock data fetching via `yfinance`
- 🧮 Technical analysis indicators:
  - Simple Moving Average (SMA)
  - Bollinger Bands
  - Relative Strength Index (RSI)
  - MACD with Signal Line
- 📉 Volume and price chart visualization using `matplotlib`
- 🧠 Basic NLP-style insights based on market behavior
- 🪟 Modern tabbed GUI interface built with `Tkinter`

---

## 🛠️ Requirements

Install the necessary dependencies with:

```bash
pip install yfinance pandas matplotlib ta tabulate alphavantage
```

> **Note:** `Tkinter` usually comes pre-installed with Python. If not, install it using:
> ```bash
> sudo apt-get install python3-tk
> ```

---

## 🚀 How to Run

Execute the application using:

```bash
python Final_Yfinance.py
```

_or_

```bash
python Final_AlphaVantage.py
```

---

## 🔍 Usage

1. Enter a stock ticker (e.g., `AAPL`, `TSLA`, `INFY.NS`).
2. Choose a time period (e.g., `1d`, `5d`, `1mo`, `6mo`, `1y`).
3. Click **Analyze** to generate insights.
4. Explore generated charts, indicators, and NLP feedback.

---

## 📦 File Structure

```
.
├── Final_AlphaVantage.py     # Alpha Vantage version of the app
├── Final_Yfinance.py         # yFinance version of the app
├── README.md                 # Project documentation
```

---

## 💡 Notes

- Default USD to INR currency conversion is set manually to `82.5`.
- For advanced AI-driven insights, consider integrating with real-time NLP or financial APIs.

---

## 🧑‍💻 Authors

Developed by **Sohrab Pritpal Singh**, **Harshit Sharma**, and **Arnav Sinha**
```
