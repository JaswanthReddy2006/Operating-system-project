import matplotlib.pyplot as plt
from collections import deque

def fifo(pages, num_frames):
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

def lru(pages, num_frames):
    memory = []
    page_map = {}
    page_faults = 0
    history = []

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

def plot_page_faults(history, algorithm):
    plt.plot(history, marker='o', linestyle='-')
    plt.title(f"Page Faults Over Time ({algorithm})")
    plt.xlabel("Number of Requests")
    plt.ylabel("Page Faults")
    plt.grid(True)
    plt.show()

def main():
    pages = list(map(int, input("Enter Page Reference String (comma-separated): ").split(',')))
    num_frames = int(input("Enter Number of Frames: "))
    algorithm = input("Choose Replacement Algorithm (FIFO/LRU): ").strip().upper()

    if num_frames <= 0:
        print("Error: Number of frames must be positive!")
        return

    if algorithm == "FIFO":
        faults, history = fifo(pages, num_frames)
    elif algorithm == "LRU":
        faults, history = lru(pages, num_frames)
    else:
        print("Error: Invalid algorithm choice!")
        return

    print(f"Total Page Faults: {faults}")
    plot_page_faults(history, algorithm)

if __name__ == "__main__":
    main()
