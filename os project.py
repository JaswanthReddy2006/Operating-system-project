import tkinter as tk
from tkinter import messagebox, ttk
import random
import time


def fifo_paging(reference_string, num_frames):
    frames = []
    hits = 0
    misses = 0
    swap_space = []
    frame_orders = []

    for i, page in enumerate(reference_string):
        if page in frames:
            hits += 1
            frame_orders.append((list(frames), " --> Hit", list(swap_space), i + 1))
        else:
            if len(frames) < num_frames:
                frames.append(page)
                frame_orders.append((list(frames), " --> Miss (No change)", list(swap_space), i + 1))
            else:
                evicted_page = frames.pop(0)
                frames.append(page)
                swap_space.append(evicted_page)

                frame_orders.append((list(frames), f" --> Miss (Removed -> {evicted_page})", list(swap_space), i + 1))
            misses += 1

    hit_ratio = hits / len(reference_string)
    miss_ratio = misses / len(reference_string)
    return hits, misses, hit_ratio, miss_ratio, frame_orders


def lru_paging(reference_string, num_frames):
    frames = []
    hits = 0
    misses = 0
    swap_space = []
    frame_orders = []

    for i, page in enumerate(reference_string):
        if page in frames:
            hits += 1
            frames.remove(page)
            frames.append(page)
            frame_orders.append((list(frames), " --> Hit", list(swap_space), i + 1))
        else:
            if len(frames) < num_frames:
                frames.append(page)
                frame_orders.append((list(frames), " --> Miss (No change)", list(swap_space), i + 1))
            else:
                evicted_page = frames.pop(0)
                frames.append(page)
                swap_space.append(evicted_page)
                frame_orders.append((list(frames), f" --> Miss (Removed -> {evicted_page})", list(swap_space), i + 1))
            misses += 1

    hit_ratio = hits / len(reference_string)
    miss_ratio = misses / len(reference_string)
    return hits, misses, hit_ratio, miss_ratio, frame_orders


def optimal_paging(reference_string, num_frames):
    frames = []
    hits = 0
    misses = 0
    swap_space = []
    frame_orders = []

    for i, page in enumerate(reference_string):
        if page in frames:
            hits += 1
            frame_orders.append((list(frames), " --> Hit", list(swap_space), i + 1))
        else:
            if len(frames) < num_frames:
                frames.append(page)
                frame_orders.append((list(frames), " --> Miss (No change)", list(swap_space), i + 1))
            else:
                # Find the page to evict
                future_uses = {frame: None for frame in frames}
                for j in range(i + 1, len(reference_string)):
                    if reference_string[j] in future_uses and future_uses[reference_string[j]] is None:
                        future_uses[reference_string[j]] = j

                # Evict the page that won't be used for the longest time
                evicted_page = max(future_uses,
                                   key=lambda x: future_uses[x] if future_uses[x] is not None else float('inf'))
                frames.remove(evicted_page)
                frames.append(page)
                swap_space.append(evicted_page)
                frame_orders.append((list(frames), f" --> Miss (Removed -> {evicted_page})", list(swap_space), i + 1))
            misses += 1

    hit_ratio = hits / len(reference_string)
    miss_ratio = misses / len(reference_string)
    return hits, misses, hit_ratio, miss_ratio, frame_orders


def random_paging(reference_string, num_frames):
    frames = []
    hits = 0
    misses = 0
    swap_space = []
    frame_orders = []

    for i, page in enumerate(reference_string):
        if page in frames:
            hits += 1
            frame_orders.append((list(frames), " --> Hit", list(swap_space), i + 1))
        else:
            if len(frames) < num_frames:
                frames.append(page)
                frame_orders.append((list(frames), " --> Miss (No change)", list(swap_space), i + 1))
            else:
                evicted_page = random.choice(frames)
                frames.remove(evicted_page)
                frames.append(page)
                swap_space.append(evicted_page)
                frame_orders.append((list(frames), f" --> Miss (Removed -> {evicted_page})", list(swap_space), i + 1))
            misses += 1

    hit_ratio = hits / len(reference_string)
    miss_ratio = misses / len(reference_string)
    return hits, misses, hit_ratio, miss_ratio, frame_orders


def calculate_total_pages():
    try:
        total_memory = int(memory_entry.get())
        page_size = int(page_size_entry.get())
        if total_memory <= 0 or page_size <= 0:
            raise ValueError("Memory and page size must be positive integers.")
        total_pages = total_memory // page_size
        total_pages_label.config(text=f"Total Pages: {total_pages}")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))


def run_simulation():
    try:
        total_memory = int(memory_entry.get())
        page_size = int(page_size_entry.get())
        num_frames = int(frames_entry.get())
        reference_string = list(map(int, reference_entry.get().split()))
        algo_choice = algorithm_var.get()

        if total_memory <= 0 or page_size <= 0 or num_frames <= 0:
            raise ValueError("Memory, page size, and frames must be positive integers.")

        if algo_choice == "FIFO":
            hits, misses, hit_ratio, miss_ratio, frame_orders = fifo_paging(reference_string, num_frames)
        elif algo_choice == "LRU":
            hits, misses, hit_ratio, miss_ratio, frame_orders = lru_paging(reference_string, num_frames)
        elif algo_choice == "Optimal":
            hits, misses, hit_ratio, miss_ratio, frame_orders = optimal_paging(reference_string, num_frames)
        elif algo_choice == "Random":
            hits, misses, hit_ratio, miss_ratio, frame_orders = random_paging(reference_string, num_frames)
        else:
            messagebox.showerror("Error", "Please select a valid paging algorithm.")
            return

        results_text.config(state=tk.NORMAL)
        results_text.delete("1.0", tk.END)
        results_text.insert(tk.END, f"Page Faults: {misses}\n")
        results_text.insert(tk.END, f"Hits: {hits}\n")
        results_text.insert(tk.END, f"Hit Ratio: {hit_ratio:.4f}\n")
        results_text.insert(tk.END, f"Miss Ratio: {miss_ratio:.4f}\n\n")

        results_text.insert(tk.END, "Step-by-Step Frame State:\n")
        results_text.config(state=tk.DISABLED)

        # Function to update the results text with a delay
        def update_results(index):
            if index < len(frame_orders):
                frames, status, swap, step = frame_orders[index]
                results_text.config(state=tk.NORMAL)
                results_text.insert(tk.END, f"Step {step}: {frames} {status}\n")
                results_text.insert(tk.END, f"Swap Space: {swap}\n\n")
                results_text.config(state=tk.DISABLED)
                results_text.see(tk.END)  # Scroll to the end
                root.after(300, update_results, index + 1)  # Schedule the next update after 300ms

        # Start the delayed updates
        update_results(0)

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))


def create_gradient(canvas, width, height, color1, color2):
    for i in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * (i / height))
        g = int(color1[1] + (color2[1] - color1[1]) * (i / height))
        b = int(color1[2] + (color2[2] - color1[2]) * (i / height))
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(0, i, width, i, fill=color)




# GUI Setup
root = tk.Tk()
root.title("PageControl - Memory Management Simulator")
root.geometry("900x600")
root.configure(bg="#FFDAB9")  # Light peach background for an inviting look

# Main Frame with 2 Sections
main_frame = tk.Frame(root, bg="#FF6347", highlightbackground="#FFA07A", highlightthickness=3, relief="raised")  # Coral red with light highlights
main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.8)

# Left Section (Inputs)
input_frame = tk.Frame(main_frame, bg="#7FFFD4", highlightbackground="#40E0D0", highlightthickness=2)  # Aquamarine with turquoise borders
input_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

# Right Section (Results)
output_frame = tk.Frame(main_frame, bg="#20B2AA", highlightbackground="#48D1CC", highlightthickness=2)  # Light sea green
output_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

# Title Label
title_label = tk.Label(root, text="PageControl - Memory Management", font=("Comic Sans MS", 18, "bold"),
                       bg="#FF4500", fg="white", pady=10)  # Vibrant orange-red title
title_label.pack(fill="x", pady=10)

# Style Configuration
style = ttk.Style()
style.theme_use("clam")

# Modern Entry Field Style
style.configure("TEntry", padding=6, font=("Arial", 11), borderwidth=0, relief="flat", foreground="black")
style.map("TEntry", background=[("readonly", "#FFFFE0")])  # Light yellow for disabled entries

# Button Style with Rounded Corners
style.configure("Rounded.TButton", font=("Arial", 12, "bold"), padding=6, background="#9370DB", foreground="white", borderwidth=0)
style.map("Rounded.TButton", background=[("active", "#8A2BE2")])  # Purple hover effect

# Input Fields
labels = ["Total Memory (bytes):", "Page Size (bytes):", "Number of Frames:", "CPU Reference String:"]
entries = []

for text in labels:
    label = tk.Label(input_frame, text=text, bg="#7FFFD4", fg="#191970", font=("Arial", 10, "bold"))  # Midnight blue text
    label.pack(anchor="w", pady=3)

    entry = ttk.Entry(input_frame, style="TEntry", width=30)
    entry.pack(fill="x", pady=5)
    entries.append(entry)

memory_entry, page_size_entry, frames_entry, reference_entry = entries

# Total Pages Label
total_pages_label = tk.Label(input_frame, text="Total Pages: 0", bg="#7FFFD4", fg="#FF1493", font=("Arial", 10, "bold"))  # Hot pink
total_pages_label.pack(anchor="w", pady=5)

# Algorithm Selection
algorithm_var = tk.StringVar()
algorithm_dropdown = ttk.Combobox(input_frame, textvariable=algorithm_var, values=["FIFO", "LRU", "Optimal", "Random"],
                                  state="readonly", font=("Arial", 11))
algorithm_dropdown.set("FIFO")
algorithm_dropdown.pack(fill="x", pady=10)

# Run Simulation Button
run_button = ttk.Button(input_frame, text="Run Simulation", style="Rounded.TButton", command=run_simulation)
run_button.pack(fill="x", pady=10)

# Results Area
results_text = tk.Text(output_frame, wrap=tk.WORD, state=tk.DISABLED, font=("Courier New", 11), bg="#00008B", fg="white")  # Deep blue CMD-style
results_text.pack(fill="both", expand=True, padx=10, pady=10)

# Add Scrollbar
scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=results_text.yview)
scrollbar.pack(side="right", fill="y")
results_text.config(yscrollcommand=scrollbar.set)

# Update Total Pages
def update_total_pages(*args):
    try:
        total_memory = int(memory_entry.get())
        page_size = int(page_size_entry.get())
        if total_memory <= 0 or page_size <= 0:
            raise ValueError("Memory and page size must be positive integers.")
        total_pages = total_memory // page_size
        total_pages_label.config(text=f"Total Pages Possible : {total_pages}")
    except ValueError:
        total_pages_label.config(text="Total Pages: 0")

memory_entry.bind("<KeyRelease>", update_total_pages)
page_size_entry.bind("<KeyRelease>", update_total_pages)

# Run Application
root.mainloop()
