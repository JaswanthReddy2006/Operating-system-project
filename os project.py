import matplotlib.pyplot as plt
from collections import deque

def fifo(pages, num_frames):
    memory, page_faults, history = deque(), 0, []
    for page in pages:
        if page not in memory:
            if len(memory) >= num_frames:
                memory.popleft()
            memory.append(page)
            page_faults += 1
        history.append(page_faults)
    return page_faults, history

def lru(pages, num_frames):
    memory, page_map, page_faults, history = [], {}, 0, []
    for i, page in enumerate(pages):
        if page not in memory:
            if len(memory) >= num_frames:
                memory.remove(min(page_map, key=page_map.get))
            memory.append(page)
            page_faults += 1
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
    pages = list(map(int, input().split(',')))
    num_frames = int(input())
    algorithm = input().strip().upper()

    if num_frames <= 0:
        return

    faults, history = (fifo if algorithm == "FIFO" else lru)(pages, num_frames) if algorithm in {"FIFO", "LRU"} else (None, None)
    
    if faults is None:
        return

    print(faults)
    plot_page_faults(history, algorithm)

if __name__ == "__main__":
    main()
