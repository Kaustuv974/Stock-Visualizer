import tkinter as tk
from tkcalendar import DateEntry
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
from alpha_vantage.timeseries import TimeSeries

def fetch_stock_data(ticker, from_date, to_date):
    api_key = '26H83PWPM72VUVJY'  # Replace with your actual API key
    ts = TimeSeries(key=api_key, output_format='pandas')
    try:
        data, _ = ts.get_daily(symbol=ticker, outputsize='full')
        data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        data.reset_index(inplace=True)
        data['Date'] = data['date'].map(mdates.date2num)
        return data
    except Exception as e:
        error_label.config(text="Error: Failed to fetch data.")
        return None

def visualize_stock_data():
    ticker = text_ticker.get()
    from_date = cal_from.get_date()
    to_date = cal_to.get_date()

    start = dt.datetime(from_date.year, from_date.month, from_date.day)
    end = dt.datetime(to_date.year, to_date.month, to_date.day)

    data = fetch_stock_data(ticker, start, end)
    if data is not None:
        plot_candlestick_chart(ticker, data)

def plot_candlestick_chart(ticker, data):
    fig, ax = plt.subplots()
    ax.grid(True)
    ax.set_axisbelow(True)
    ax.set_title(f'{ticker} Share Price', color='white')
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.xaxis_date()

    candlestick_ohlc(ax, data[['Date', 'Open', 'High', 'Low', 'Close']].values, width=0.5, colorup='g')

    plt.show()

# Define Main Window
root = tk.Tk()
root.title("Kaustuv's Stock Visualizer")

label_from = tk.Label(root, text="From:")
label_from.grid(row=0, column=0, padx=5, pady=5)
cal_from = DateEntry(root, width=12, year=2010, month=1, day=1)
cal_from.grid(row=0, column=1, padx=5, pady=5)

label_to = tk.Label(root, text="To:")
label_to.grid(row=0, column=2, padx=5, pady=5)
cal_to = DateEntry(root, width=12)
cal_to.grid(row=0, column=3, padx=5, pady=5)

label_ticker = tk.Label(root, text="Ticker Symbol:")
label_ticker.grid(row=1, column=0, padx=5, pady=5)
text_ticker = tk.Entry(root)
text_ticker.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

btn_visualize = tk.Button(root, text="Visualize Stock", command=visualize_stock_data)
btn_visualize.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

error_label = tk.Label(root, text="", fg="red")
error_label.grid(row=3, column=0, columnspan=4)

root.mainloop()
