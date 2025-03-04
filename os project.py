import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque


class MemoryVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Management Visualizer")

        # Input fields
        ttk.Label(root, text="Page Reference String (comma-separated):").grid(row=0, column=0, padx=10, pady=5)
        self.page_entry = ttk.Entry(root, width=30)
        self.page_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(root, text="Number of Frames:").grid(row=1, column=0, padx=10, pady=5)
        self.frame_entry = ttk.Entry(root, width=10)
        self.frame_entry.grid(row=1, column=1, padx=10, pady=5)

        # Algorithm selection
        ttk.Label(root, text="Replacement Algorithm:").grid(row=2, column=0, padx=10, pady=5)
        self.algo_choice = ttk.Combobox(root, values=["FIFO", "LRU"], state="readonly")
        self.algo_choice.grid(row=2, column=1, padx=10, pady=5)
        self.algo_choice.current(0)

        # Buttons
        ttk.Button(root, text="Run Simulation", command=self.run_simulation).grid(row=3, column=0, columnspan=2,
                                                                                  pady=10)

        # Output Label
        self.result_label = ttk.Label(root, text="", font=("Arial", 12, "bold"))
        self.result_label.grid(row=4, column=0, columnspan=2, pady=5)

        # Graph Frame
        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=2, pady=10)

    def run_simulation(self):
        try:
            pages = list(map(int, self.page_entry.get().split(',')))
            num_frames = int(self.frame_entry.get())
            algorithm = self.algo_choice.get()

            if num_frames <= 0:
                messagebox.showerror("Error", "Number of frames must be positive!")
                return

            if algorithm == "FIFO":
                faults, history = self.fifo(pages, num_frames)
            else:
                faults, history = self.lru(pages, num_frames)

            self.result_label.config(text=f"Total Page Faults: {faults}")

            self.plot_graph(history)

        except ValueError:
            messagebox.showerror("Error", "Invalid input! Enter numbers separated by commas.")

    def fifo(self, pages, num_frames):
        memory = deque()
        page_faults = 0
        history = []

        for page in pages:
            if page not in memory:
                if len(memory) < num_frames:
                    memory.append(page)
                else:
                    memory.popleft()
                    memory.append(page)
                page_faults += 1
            history.append(page_faults)

        return page_faults, history

    def lru(self, pages, num_frames):
        memory = []
        page_faults = 0
        history = []
        page_map = {}

        for i, page in enumerate(pages):
            if page not in memory:
                if len(memory) < num_frames:
                    memory.append(page)
                else:
                    # Remove least recently used page
                    lru_page = min(page_map, key=page_map.get)
                    memory.remove(lru_page)
                    memory.append(page)
                page_faults += 1

            # Update last used index
            page_map[page] = i
            history.append(page_faults)

        return page_faults, history

    def plot_graph(self, history):
        self.ax.clear()
        self.ax.plot(history, marker='o', linestyle='-')
        self.ax.set_title("Page Faults Over Time")
        self.ax.set_xlabel("Number of Requests")
        self.ax.set_ylabel("Page Faults")
        self.ax.grid(True)
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryVisualizer(root)
    root.mainloop()
