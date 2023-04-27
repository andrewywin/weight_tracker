import tkinter as tk
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt

# storing weight, if there is no where to track weight, will create new dataframe
try:
    weight_all  = pd.read_csv('weight_data.csv')
except FileNotFoundError:
    weight_all  = pd.DataFrame(columns=['Date', 'Weight'])


# recording both today's date, and the inputted weight
def record():
    today = date.today().strftime("%m/%d/%Y")
   
    weight = weight_entry.get()
    
    weight_all.loc[len(weight_all)] = [today, weight]
    weight_all.to_csv('weight_data.csv', index=False)
    weight_entry.delete(0, tk.END)

# to view all the weight data entries inputted so far
def view_data():
    top = tk.Toplevel()
    top.title("Weight Data")
    table = tk.Text(top)
    table.pack()

    table.insert(tk.END, weight_all)

def plot_data():
    top = tk.Toplevel()
    top.title("Plot Weight Data")

    start_date_label = tk.Label(top, text="Start Date (MM/DD/YYYY):")
    start_date_label.pack()
    start_date_entry = tk.Entry(top)
    start_date_entry.pack()

    end_date_label = tk.Label(top, text="End Date (MM/DD/YYYY):")
    end_date_label.pack()
    end_date_entry = tk.Entry(top)
    end_date_entry.pack()

    def plot_graph():
        start_date_str = start_date_entry.get()
        end_date_str = end_date_entry.get()
        try:
            start_date = pd.to_datetime(start_date_str, format="%m/%d/%Y")
            end_date = pd.to_datetime(end_date_str, format="%m/%d/%Y")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use MM/DD/YYYY")
            return

        data_range = weight_all[(pd.to_datetime(weight_all['Date'], format="%m/%d/%Y") >= start_date) & (pd.to_datetime(weight_all['Date'], format="%m/%d/%Y") <= end_date)]

        if data_range.empty:
            messagebox.showerror("Error", "No data within selected date range.")
            return

        plt.plot(data_range['Date'], data_range['Weight'])
        plt.xlabel('Date')
        plt.ylabel('Weight')
        plt.title('Weight Change over Time')
        plt.show()

    plot_button = tk.Button(top, text="Plot", command=plot_graph)
    plot_button.pack()

root = tk.Tk()
root.title("Weight Tracker")

# Weight input widgets
weight_label = tk.Label(root, text="Enter your weight for today:")
weight_label.pack()
weight_entry = tk.Entry(root)
weight_entry.pack()

# Record weight button
record_button = tk.Button(root, text="Record", command=record)
record_button.pack()

# View weight data button
view_button = tk.Button(root, text="View Data", command=view_data)
view_button.pack()

# Plot weight data button
plot_button = tk.Button(root, text="Plot Data", command=plot_data)
plot_button.pack()

root.mainloop()
