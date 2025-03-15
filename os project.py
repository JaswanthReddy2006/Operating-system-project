import time

def fifo_paging(reference_string, num_frames):
    frames = []
    hits = 0
    misses = 0
    swap_space = []  # To track the virtual memory (swap space)
    frame_orders = []  # To track the state of frames after each page reference

    # Simulate FIFO Paging Algorithm
    for i, page in enumerate(reference_string):
        # If page is already in the frames, it's a hit
        if page in frames:
            hits += 1
            frame_orders.append((list(frames), " --> Hit", list(swap_space), i + 1))  # Include step number and swap space
        else:
            # If there is space in the frames, add the page
            if len(frames) < num_frames:
                frames.append(page)
                frame_orders.append((list(frames), " --> Miss (No change)", list(swap_space), i + 1))
            else:
                # If there is no space, replace the first page in the frame (FIFO)
                evicted_page = frames.pop(0)
                frames.append(page)
                # Move evicted page to swap space (virtual memory)
                swap_space.append(evicted_page)
                frame_orders.append((list(frames), f" --> Miss (Removed -> {evicted_page})", list(swap_space), i + 1))
            misses += 1

    # Calculate hit ratio and miss ratio
    total_requests = len(reference_string)
    hit_ratio = hits / total_requests
    miss_ratio = misses / total_requests

    return hits, misses, hit_ratio, miss_ratio, frame_orders, swap_space


def lru_paging(reference_string, num_frames):
    frames = []
    hits = 0
    misses = 0
    swap_space = []  # To track the virtual memory (swap space)
    frame_orders = []  # To track the state of frames after each page reference

    # Simulate LRU Paging Algorithm
    for i, page in enumerate(reference_string):
        # If page is already in the frames, it's a hit
        if page in frames:
            hits += 1
            # Move the page to the end (most recently used)
            frames.remove(page)
            frames.append(page)
            frame_orders.append((list(frames), " --> Hit", list(swap_space), i + 1))  # Include step number and swap space
        else:
            # If there is space in the frames, add the page
            if len(frames) < num_frames:
                frames.append(page)
                frame_orders.append((list(frames), " --> Miss (No change)", list(swap_space), i + 1))
            else:
                # If there is no space, replace the least recently used page
                evicted_page = frames.pop(0)
                frames.append(page)
                # Move evicted page to swap space (virtual memory)
                swap_space.append(evicted_page)
                frame_orders.append((list(frames), f" --> Miss (Removed -> {evicted_page})", list(swap_space), i + 1))
            misses += 1

    # Calculate hit ratio and miss ratio
    total_requests = len(reference_string)
    hit_ratio = hits / total_requests
    miss_ratio = misses / total_requests

    return hits, misses, hit_ratio, miss_ratio, frame_orders, swap_space


def main():
    while True:
        print("\nWelcome to PageControl - Memory Management Simulator with Virtual Memory!")
        print("Choose an option:")
        print("1. Start Memory Management Simulation")
        print("2. Exit")

        choice = input("Enter your choice (1 or 2): ")

        if choice == "1":
            # Get inputs for the memory simulation
            total_memory = int(input("\nEnter total memory size (in bytes): "))
            page_size = int(input("Enter page size (in bytes): "))
            num_frames = int(input("Enter number of frames: "))

            # Calculate number of pages
            num_pages = total_memory // page_size
            print(f"Total number of pages (based on total memory size and page size): {num_pages}")

            reference_string = list(map(int, input("\nEnter CPU reference string (space-separated): ").split()))

            # Choose Paging Algorithm
            print("\nChoose Paging Algorithm:")
            print("1. FIFO")
            print("2. LRU")
            algo_choice = input("Enter 1 for FIFO or 2 for LRU: ")

            if algo_choice == "1":
                print("\n--- FIFO Algorithm with Virtual Memory ---")
                hits, misses, hit_ratio, miss_ratio, frame_orders, swap_space = fifo_paging(reference_string, num_frames)
            elif algo_choice == "2":
                print("\n--- LRU Algorithm with Virtual Memory ---")
                hits, misses, hit_ratio, miss_ratio, frame_orders, swap_space = lru_paging(reference_string, num_frames)
            else:
                print("Invalid choice. Please try again.")
                continue

            # Output the results
            print(f"\nPage Faults: {misses}")
            print(f"Hits: {hits}")
            print(f"Hit Ratio: {hit_ratio:.4f}")
            print(f"Miss Ratio: {miss_ratio:.4f}")

            # Display step-by-step frame state and hit/miss status
            print("\nStep-by-Step Frame State and Hit/Miss Status:")
            for frames, status, swap, step in frame_orders:
                print(f"Step {step}: {frames} {status}")
                print(f"Swap Space: {swap}\n")  # Show swap space for each step

        elif choice == "2":
            print("Exiting the program. Goodbye!")
            time.sleep(1.5)
            break  # Exit the loop and close the program

        else:
            print("Invalid choice, please enter 1 or 2.")


# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()
