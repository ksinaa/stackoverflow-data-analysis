import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AuthorSkillVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Author Skill Visualizer")
        self.root.geometry("800x600")

        # Load data
        self.df = pd.read_csv('../normalized_score.csv')

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create and set up the notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create the input tab
        self.input_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.input_tab, text="Input")

        # Create input fields
        ttk.Label(self.input_tab, text="Enter Author ID:").pack(pady=10)
        self.author_id_entry = ttk.Entry(self.input_tab)
        self.author_id_entry.pack(pady=10)

        # Create submit button
        ttk.Button(self.input_tab, text="Submit", command=self.create_chart).pack(pady=20)

    def create_chart(self):
        author_id = self.author_id_entry.get()
        if not author_id:
            return

        # Filter data for the specific author
        author_data = self.df[self.df['OwnerUserId'] == int(author_id)]

        if author_data.empty:
            tk.messagebox.showinfo("No Data", f"No data found for Author ID: {author_id}")
            return

        # Create a new tab for the chart
        chart_tab = ttk.Frame(self.notebook)
        self.notebook.add(chart_tab, text=f"Author {author_id}")
        self.notebook.select(chart_tab)

        # Create the chart
        fig, ax = plt.subplots(figsize=(10, 6))

        # Group data by Year and SkillArea
        grouped_data = author_data.groupby(['Year', 'SkillArea'])['normalized_score'].sum().unstack()

        # Plot stacked bar chart
        grouped_data.plot(kind='bar', stacked=True, ax=ax)

        ax.set_xlabel('Year')
        ax.set_ylabel('Normalized Score')
        ax.set_title(f'Skill Areas Over Time for Author {author_id}')
        ax.legend(title='Skill Area', bbox_to_anchor=(1.05, 1), loc='upper left')

        # Embed the chart in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=chart_tab)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Adjust layout
        plt.tight_layout()
        canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = AuthorSkillVisualizerApp(root)
    root.mainloop()