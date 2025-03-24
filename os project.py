import tkinter as tk
from tkinter import messagebox, ttk
import random


# FIFO Paging Algorithm
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


# LRU Paging Algorithm
def lru_paging(reference_string, num_frames):
    frames = []
    hits = 0
    misses = 0
    swap_space = []
    frame_orders = []

    for i, page in enumerate(reference_string):
        if page in frames:
            hits += 1
            frames.remove(page)  # Remove the page to update its position
            frames.append(page)  # Re-add the page to mark it as recently used
            frame_orders.append((list(frames), " --> Hit", list(swap_space), i + 1))
        else:
            misses += 1
            if len(frames) < num_frames:
                frames.append(page)
                frame_orders.append((list(frames), " --> Miss (No change)", list(swap_space), i + 1))
            else:
                evicted_page = frames.pop(0)  # Remove the least recently used page
                frames.append(page)
                swap_space.append(evicted_page)
                frame_orders.append((list(frames), f" --> Miss (Removed -> {evicted_page})", list(swap_space), i + 1))

    hit_ratio = hits / len(reference_string)
    miss_ratio = misses / len(reference_string)
    return hits, misses, hit_ratio, miss_ratio, frame_orders


# Optimal Paging Algorithm
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


# Random Paging Algorithm
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


# Function to calculate total pages
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


# Function to run the simulation
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
        elif algo_choice == "Optimal (OPT)":
            hits, misses, hit_ratio, miss_ratio, frame_orders = optimal_paging(reference_string, num_frames)
        elif algo_choice == "Random (RAND)":
            hits, misses, hit_ratio, miss_ratio, frame_orders = random_paging(reference_string, num_frames)
        else:
            messagebox.showerror("Error", "Please select a valid paging algorithm.")
            return

        results_text.config(state=tk.NORMAL)
        results_text.delete("1.0", tk.END)
        results_text.insert(tk.END, f"Page Faults: {misses}\n", "fault")
        results_text.insert(tk.END, f"Hits: {hits}\n", "hit")
        results_text.insert(tk.END, f"Hit Ratio: {hit_ratio:.2f}\n", "ratio")
        results_text.insert(tk.END, f"Miss Ratio: {miss_ratio:.2f}\n\n", "ratio")

        results_text.insert(tk.END, "Step-by-Step Frame State:\n", "header")
        results_text.config(state=tk.DISABLED)

        # Function to update the results text with a delay
        def update_results(index):
            if index < len(frame_orders):
                frames, status, swap, step = frame_orders[index]
                results_text.config(state=tk.NORMAL)

                # Different colors for hits and misses
                tag = "hit_text" if "Hit" in status else "miss_text"
                results_text.insert(tk.END, f"Step {step}: {frames} ", "step")
                results_text.insert(tk.END, f"{status}\n", tag)
                results_text.insert(tk.END, f"Swap Space: {swap}\n\n", "swap")

                results_text.config(state=tk.DISABLED)
                results_text.see(tk.END)  # Scroll to the end
                root.after(300, update_results, index + 1)  # Schedule the next update after 300ms

        # Start the delayed updates
        update_results(0)

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))


# Function to compare all algorithms
def compare_algorithms():
    try:
        total_memory = int(memory_entry.get())
        page_size = int(page_size_entry.get())
        num_frames = int(frames_entry.get())
        reference_string = list(map(int, reference_entry.get().split()))
        criteria = criteria_var.get()

        if total_memory <= 0 or page_size <= 0 or num_frames <= 0:
            raise ValueError("Memory, page size, and frames must be positive integers.")

        algorithms = ["FIFO", "LRU", "Optimal (OPT)", "Random (RAND)"]
        results = []

        for algo in algorithms:
            if algo == "FIFO":
                hits, misses, hit_ratio, miss_ratio, _ = fifo_paging(reference_string, num_frames)
            elif algo == "LRU":
                hits, misses, hit_ratio, miss_ratio, _ = lru_paging(reference_string, num_frames)
            elif algo == "Optimal (OPT)":
                hits, misses, hit_ratio, miss_ratio, _ = optimal_paging(reference_string, num_frames)
            elif algo == "Random (RAND)":
                hits, misses, hit_ratio, miss_ratio, _ = random_paging(reference_string, num_frames)
            results.append((algo, hits, misses, hit_ratio, miss_ratio))

        # Determine the best algorithm based on the selected criteria
        if criteria == "Hit Ratio":
            best_algorithm = max(results, key=lambda x: x[3])  # x[3] is the hit ratio
            best_metric = best_algorithm[3]
            metric_name = "Hit Ratio"
        else:
            best_algorithm = min(results, key=lambda x: x[4])  # x[4] is the miss ratio
            best_metric = best_algorithm[4]
            metric_name = "Miss Ratio"

        # Display results in a new window
        comparison_window = tk.Toplevel(root)
        comparison_window.title("Algorithm Comparison")
        comparison_window.geometry("600x450")
        comparison_window.configure(bg="#F5F5F5")  # Light background for comparison window

        # Title for comparison window
        title_frame = tk.Frame(comparison_window, bg="#3A7CA5")  # Changed to a nicer blue
        title_frame.pack(fill="x", pady=0)
        title_label = tk.Label(title_frame, text="Algorithm Performance Comparison",
                               font=("Arial", 14, "bold"), bg="#3A7CA5", fg="white", pady=10)
        title_label.pack()

        # Create a table to display the results (using a centered layout)
        main_comparison_frame = tk.Frame(comparison_window, bg="#F5F5F5")
        main_comparison_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Center the table horizontally
        center_frame = tk.Frame(main_comparison_frame, bg="#F5F5F5")
        center_frame.place(relx=0.5, rely=0.4, anchor="center")

        table_frame = tk.Frame(center_frame, bg="#F5F5F5")
        table_frame.pack()

        # Table headers with better colors
        headers = ["Algorithm", "Hits", "Misses", "Hit Ratio", "Miss Ratio"]
        header_colors = ["#2E86C1", "#3498DB", "#2874A6", "#21618C", "#1B4F72"]  # Nicer blue gradient

        for col, header in enumerate(headers):
            label = tk.Label(table_frame, text=header, bg=header_colors[col], fg="white",
                             font=("Arial", 12, "bold"), padx=10, pady=5, width=12)
            label.grid(row=0, column=col, sticky="ew")

        # Table rows with improved algorithm-specific colors
        algo_colors = {
            "FIFO": "#AED6F1",  # Lighter blue
            "LRU": "#A3E4D7",  # Lighter teal
            "Optimal (OPT)": "#F9E79F",  # Lighter yellow
            "Random (RAND)": "#D7BDE2"  # Lighter purple
        }

        for row, result in enumerate(results, start=1):
            algo_name = result[0]
            row_color = algo_colors[algo_name]

            for col, value in enumerate(result):
                text_color = "black"  # Better contrast on light backgrounds
                if col == 0:  # Algorithm name column
                    font_style = ("Arial", 11, "bold")
                    display_value = value  # Use the full algorithm name
                elif col == 3 or col == 4:  # Hit or Miss ratio - format to 2 decimal places
                    font_style = ("Arial", 11)
                    display_value = f"{value:.2f}"  # Format to 2 decimal places
                else:
                    font_style = ("Arial", 11)
                    display_value = value

                label = tk.Label(table_frame, text=display_value, bg=row_color, fg=text_color,
                                 font=font_style, padx=10, pady=5, width=12)
                label.grid(row=row, column=col, sticky="ew")

        # Display the best algorithm
        result_frame = tk.Frame(comparison_window, bg="#F5F5F5")
        result_frame.place(relx=0.5, rely=0.8, anchor="center")

        best_label = tk.Label(result_frame,
                              text=f"Best Algorithm: {best_algorithm[0]}",
                              font=("Arial", 12, "bold"), fg="#2471A3", bg="#F5F5F5")
        best_label.pack()

        metric_label = tk.Label(result_frame,
                                text=f"{metric_name}: {best_metric:.2f}",
                                font=("Arial", 11), fg="#2471A3", bg="#F5F5F5")
        metric_label.pack()

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))


# GUI Setup
root = tk.Tk()
root.title("PageControl - Memory Management Simulator")
root.configure(bg="#F0F0F0")  # Light gray background for main window

# Set window to maximized instead of fullscreen
root.state('zoomed')  # This maximizes the window without fullscreen mode

# Style configuration for a cleaner look
style = ttk.Style()
style.theme_use('clam')  # Use 'clam' theme for a more modern look
style.configure("TEntry", font=("Arial", 11), fieldbackground="#FFFFFF", foreground="#000000")
style.configure("TButton", font=("Arial", 11, "bold"), background="#4682B4", foreground="white")
style.configure("TCombobox", font=("Arial", 11), fieldbackground="#FFFFFF", foreground="#000000")
style.map('TCombobox', fieldbackground=[('readonly', '#FFFFFF')])
style.map('TCombobox', selectbackground=[('readonly', '#4682B4')])
style.map('TCombobox', selectforeground=[('readonly', 'white')])

# Main Frame with light colors
main_frame = tk.Frame(root, bg="#F0F0F0", relief="ridge", bd=2)
main_frame.place(relx=0.5, rely=0.52, anchor="center", relwidth=0.92, relheight=0.85)

# Title Label with blue gradient appearance
title_label = tk.Label(root, text="PageControl - Memory Management", font=("Helvetica", 22, "bold"),
                       bg="#4682B4", fg="white", pady=12)
title_label.pack(fill="x", pady=(10, 15))

# Create frames with a fixed layout that doesn't resize content
frame_container = tk.Frame(main_frame, bg="#F0F0F0")
frame_container.pack(fill="both", expand=True)

# Left Section (Inputs) - Fixed width
input_frame = tk.Frame(frame_container, bg="#E8F4F8", width=350, relief="ridge", bd=1)
input_frame.pack(side="left", fill="y", padx=15, pady=15)
input_frame.pack_propagate(False)  # Prevent frame from shrinking

# Right Section (Results) - Expands with window
output_frame = tk.Frame(frame_container, bg="#E8F4F8", relief="ridge", bd=1)
output_frame.pack(side="right", fill="both", expand=True, padx=15, pady=15)

# Input Fields - with colored headers for each section
input_sections = [
    {"label": "Memory Configuration", "color": "#5DADE2", "fields": [
        "Total Memory (bytes):", "Page Size (bytes):", "Number of Frames:", "CPU Reference String:"
    ]},
    {"label": "Algorithm Settings", "color": "#1ABC9C", "fields": [  # Changed color to a more vibrant teal
        "Select Algorithm:", "Comparison Criteria:"
    ]}
]

entries = []
row_index = 0

for section in input_sections:
    # Section header - Make it look less like a button
    header_frame = tk.Frame(input_frame, bg=section["color"])
    header_frame.pack(fill="x", pady=(15 if row_index > 0 else 0, 8))

    header_label = tk.Label(header_frame, text=section["label"], bg=section["color"],
                            fg="white", font=("Arial", 12, "bold"), pady=7)
    header_label.pack(fill="x")

    # Section fields
    for field in section["fields"]:
        field_frame = tk.Frame(input_frame, bg="#E8F4F8")
        field_frame.pack(fill="x", pady=3)

        label = tk.Label(field_frame, text=field, bg="#E8F4F8", fg="#2C3E50",
                         font=("Arial", 10, "bold"), anchor="w")
        label.pack(fill="x", padx=5)

        if field == "Select Algorithm:":
            algorithm_var = tk.StringVar()
            dropdown = ttk.Combobox(field_frame, textvariable=algorithm_var,
                                    values=["FIFO", "LRU", "Optimal (OPT)", "Random (RAND)"],
                                    state="readonly")
            dropdown.current(0)
            dropdown.pack(fill="x", padx=5, pady=3)
        elif field == "Comparison Criteria:":
            criteria_var = tk.StringVar(value="Hit Ratio")
            dropdown = ttk.Combobox(field_frame, textvariable=criteria_var,
                                    values=["Hit Ratio", "Miss Ratio"],
                                    state="readonly")
            dropdown.pack(fill="x", padx=5, pady=3)
        else:
            # Custom styled Entry fields for numbers
            if "Memory" in field or "Size" in field or "Frames" in field:
                entry = ttk.Entry(field_frame)
                entry.pack(fill="x", padx=5, pady=3)
                entries.append(entry)
            else:
                entry = ttk.Entry(field_frame)
                entry.pack(fill="x", padx=5, pady=3)
                entries.append(entry)

    row_index += 1

memory_entry, page_size_entry, frames_entry, reference_entry = entries

# Total Pages Label - Modified to not look like a button
total_pages_frame = tk.Frame(input_frame, bg="#E8F4F8", pady=8)
total_pages_frame.pack(fill="x")

# Changed to a bordered label instead of a button-like appearance
total_pages_label = tk.Label(total_pages_frame, text="Total Pages: 0", bg="#E8F4F8", fg="#2C3E50",
                             font=("Arial", 11, "bold"), pady=6, relief="groove", bd=1)
total_pages_label.pack(fill="x", padx=5)

# Buttons Section
button_frame = tk.Frame(input_frame, bg="#E8F4F8")
button_frame.pack(fill="x", pady=15, side="bottom")

# Run Simulation Button - Made more obvious as a button
run_button = tk.Button(button_frame, text="Run Simulation", font=("Arial", 12, "bold"),
                       bg="#4682B4", fg="white", padx=12, pady=10,
                       activebackground="#5DADE2", activeforeground="white",
                       relief="raised", bd=2,  # More pronounced button appearance
                       command=run_simulation)
run_button.pack(fill="x", padx=8, pady=8)

# Compare Algorithms Button - Made more obvious as a button
compare_button = tk.Button(button_frame, text="Compare Algorithms", font=("Arial", 12, "bold"),
                           bg="#1ABC9C", fg="white", padx=12, pady=10,  # Changed to match header color
                           activebackground="#1ABC9C", activeforeground="white",
                           relief="raised", bd=2,  # More pronounced button appearance
                           command=compare_algorithms)
compare_button.pack(fill="x", padx=8, pady=8)

# Results Header
results_header = tk.Label(output_frame, text="Simulation Results", bg="#5DADE2",
                          fg="white", font=("Arial", 14, "bold"), pady=10)  # Increased font size
results_header.pack(fill="x")

# Results Area with bolder and larger text - Modified as requested
results_text = tk.Text(output_frame, wrap=tk.WORD, state=tk.DISABLED,
                       font=("Courier New", 12, "bold"), bg="#FFFFFF", fg="#333333")  # Increased font size and bold
results_text.pack(fill="both", expand=True, padx=8, pady=8)

# Add Scrollbar with styling
scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=results_text.yview)
scrollbar.pack(side="right", fill="y")
results_text.config(yscrollcommand=scrollbar.set)

# Configure text tags for colored output - Made bolder and larger
results_text.tag_configure("header", foreground="#2980B9", font=("Courier New", 14, "bold"))
results_text.tag_configure("fault", foreground="#E74C3C", font=("Courier New", 13, "bold"))
results_text.tag_configure("hit", foreground="#27AE60", font=("Courier New", 13, "bold"))
results_text.tag_configure("ratio", foreground="#8E44AD", font=("Courier New", 13, "bold"))
results_text.tag_configure("step", foreground="#D35400", font=("Courier New", 13, "bold"))
results_text.tag_configure("hit_text", foreground="#27AE60", font=("Courier New", 13, "bold"))
results_text.tag_configure("miss_text", foreground="#E74C3C", font=("Courier New", 13, "bold"))
results_text.tag_configure("swap", foreground="#2C3E50",
                           font=("Courier New", 12))  # Changed color for better visibility


# Update Total Pages
def update_total_pages(*args):
    try:
        total_memory = int(memory_entry.get())
        page_size = int(page_size_entry.get())
        if total_memory <= 0 or page_size <= 0:
            raise ValueError("Memory and page size must be positive integers.")
        total_pages = total_memory // page_size
        total_pages_label.config(text=f"Total Pages: {total_pages}")
    except ValueError:
        total_pages_label.config(text="Total Pages: 0")


memory_entry.bind("<KeyRelease>", update_total_pages)
page_size_entry.bind("<KeyRelease>", update_total_pages)

# Set default values for easier testing
memory_entry.insert(0, "1024")
page_size_entry.insert(0, "256")
frames_entry.insert(0, "3")
reference_entry.insert(0, "1 2 3 4 1 2 5 1 2 3 4 5")

# Calculate total pages on startup
update_total_pages()

# Run Application
root.mainloop()
