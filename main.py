import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import AuthorHistory


def plot_chart(author_id):
    # Fetch data from AuthorHistory
    x, y, z = AuthorHistory.getAuthorHistory(author_id)

    # Create a new window for the plot
    plot_window = tk.Toplevel()
    plot_window.title(f"Timeline Chart for Author ID: {author_id}")

    # Create a Matplotlib figure and axis
    fig, ax = plt.subplots()

    # Plotting a timeline chart with labels from z
    for i in range(len(x)):
        ax.plot_date(x[i], y[i], linestyle='solid', marker='o', label=z[i])

    ax.set_title(f"Timeline Chart for Author ID: {author_id}")
    ax.set_xlabel("Creation Date")
    ax.set_ylabel("Score")

    # Improve date formatting on x-axis
    fig.autofmt_xdate()
    date_format = DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(date_format)

    # Add legend to the chart
    ax.legend()

    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack()


def on_button_click(author_id_entry):
    author_id = author_id_entry.get()
    plot_chart(author_id)

def create_main_window():
    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Author ID Input")

    # Create and place the input label and entry
    author_id_label = ttk.Label(root, text="Enter Author ID:")
    author_id_label.pack(pady=5)
    author_id_entry = ttk.Entry(root)
    author_id_entry.pack(pady=5)

    # Create and place the button
    plot_button = ttk.Button(root, text="Show Chart", command=lambda: on_button_click(author_id_entry))
    plot_button.pack(pady=20)

    return root

def main():
    root = create_main_window()
    root.mainloop()

if __name__ == "__main__":
    main()
