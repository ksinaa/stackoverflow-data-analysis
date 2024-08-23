from tkinter import ttk
import AuthorHistory
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from collections import defaultdict
import numpy as np
from scipy.interpolate import PchipInterpolator
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import ScalarFormatter
from scipy.signal import savgol_filter

def plot_chart(author_id, selected_skills):
    # Fetch data from AuthorHistory
    dates, scores, skill_areas = AuthorHistory.getAuthorHistory(author_id, selected_skills)

    # Create a new window for the plot
    plot_window = tk.Toplevel()
    plot_window.title(f"Stream Graph for Author ID: {author_id}")

    # Create a Matplotlib figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # Process the data for stream graph
    data = defaultdict(lambda: [0] * len(set(dates)))
    unique_dates = sorted(set(dates))
    date_indices = {date: i for i, date in enumerate(unique_dates)}

    for date, score, skill in zip(dates, scores, skill_areas):
        data[skill][date_indices[date]] += score

    # Convert defaultdict to regular dict for easier handling
    data = dict(data)

    # Ensure all skill areas have the same number of data points
    max_length = len(unique_dates)
    for skill in data:
        data[skill] = data[skill] + [0] * (max_length - len(data[skill]))

    # Convert dates to numerical values for interpolation
    x = mdates.date2num(unique_dates)

    # Create more points for smoother curves
    x_new = np.linspace(x.min(), x.max(), num=1000)  # Increased from 500 to 1000

    # Interpolate and smooth the data for each skill
    interpolated_data = {}
    for skill, values in data.items():
        interpolator = PchipInterpolator(x, values)
        interpolated_values = interpolator(x_new)
        # Apply Savitzky-Golay filter for smoothing
        smoothed_values = savgol_filter(interpolated_values, window_length=51, polyorder=3)
        interpolated_data[skill] = np.clip(smoothed_values, 0, None)  # Clip negative values to 0

    # Create the stream graph with interpolated and smoothed data
    ax.stackplot(x_new, interpolated_data.values(),
                 labels=interpolated_data.keys(), alpha=0.8)

    ax.set_title(f"Stream Graph for Author ID: {author_id}")
    ax.set_xlabel("Creation Date")
    ax.set_ylabel("Score (log scale)")

    # Set y-axis to logarithmic scale
    ax.set_yscale('symlog', linthresh=1)
    ax.yaxis.set_major_formatter(ScalarFormatter())

    # Improve date formatting on x-axis
    fig.autofmt_xdate()
    date_format = mdates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(date_format)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())

    # Convert x-axis back to dates
    ax.set_xlim(mdates.num2date(x_new.min()), mdates.num2date(x_new.max()))

    # Add legend to the chart
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Adjust layout to prevent cutoff
    plt.tight_layout()

    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Add a scrollbar
    scrollbar = tk.Scrollbar(plot_window, orient=tk.VERTICAL, command=canvas.get_tk_widget().yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.get_tk_widget().configure(yscrollcommand=scrollbar.set)
    canvas.get_tk_widget().bind('<Configure>', lambda e: canvas.get_tk_widget().configure(
        scrollregion=canvas.get_tk_widget().bbox('all')))


def on_button_click(author_id_entry, skill_listbox):
    author_id = author_id_entry.get()
    selected_skills = [skill_listbox.get(i) for i in skill_listbox.curselection()]
    plot_chart(author_id, selected_skills)

def create_main_window():
    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Author ID Input")

    # Create and place the input label and entry
    author_id_label = ttk.Label(root, text="Enter Author ID:")
    author_id_label.pack(pady=5)
    author_id_entry = ttk.Entry(root)
    author_id_entry.pack(pady=5)

    # Create and place the skill selection listbox
    skill_label = ttk.Label(root, text="Select Skills:")
    skill_label.pack(pady=5)
    skill_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=10)
    skill_listbox.pack(pady=5)

    # Populate the listbox with skill names
    skill_names = AuthorHistory.getUniqueSkillNames()
    for name in skill_names:
        skill_listbox.insert(tk.END, name)

    # Create and place the button
    plot_button = ttk.Button(root, text="Show Chart", command=lambda: on_button_click(author_id_entry, skill_listbox))
    plot_button.pack(pady=20)

    return root

def main():
    root = create_main_window()
    root.mainloop()

if __name__ == "__main__":
    main()