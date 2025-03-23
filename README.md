# PageControl - Memory Management Simulator

## Overview

PageControl is an educational and interactive memory management simulator designed to simplify the concepts of page replacement algorithms in operating systems. It enables users to simulate different algorithms, input memory parameters, and analyze performance metrics such as hit ratio, miss ratio, and page faults. With its interactive GUI and step-by-step visualization, PageControl is an invaluable tool for students, educators, and anyone looking to deepen their understanding of memory management.

---

## Features

- **Multiple Page Replacement Algorithms**: Supports the most widely used algorithms:
  - **FIFO (First-In-First-Out)**: Replaces the page that has been in memory the longest.
  - **LRU (Least Recently Used)**: Replaces the page that has not been accessed for the longest duration.
  - **Optimal**: Replaces the page that will not be used for the longest time in the future.
  - **Random**: Replaces a randomly selected page from memory.

- **Interactive and User-Friendly Interface**: 
  - Intuitive GUI designed with dropdown menus, text fields, and real-time results display.
  - Clear navigation ensures ease of use for users of all experience levels.

- **Step-by-Step Execution**: 
  - Visualizes each step of the simulation process.
  - Shows the real-time state of memory frames and swap space as the simulation progresses.

- **Performance Metrics**: 
  - Provides insights such as:
    - **Page Faults**: Total number of times a required page was not in memory.
    - **Hits**: Total number of times a required page was found in memory.
    - **Hit Ratio**: Ratio of hits to total memory accesses.
    - **Miss Ratio**: Ratio of misses to total memory accesses.

- **Customizable Input Parameters**: Allows users to configure:
  - **Total Memory Size**: Specify the total memory in bytes.
  - **Page Size**: Define the size of individual pages in bytes.
  - **Number of Frames**: Set the number of memory frames available for the simulation.
  - **CPU Reference String**: Enter the sequence of page references to simulate.

---

## Installation

1. **Download the Executable**:
   - Download the latest version of `PageControl.exe` from the source repository.

2. **Run the Application**:
   - Double-click the `PageControl.exe` file to launch the simulator.

3. **System Requirements**:
   - Windows operating system (64-bit recommended).
   - Minimum 2GB RAM for smooth operation.

---

## Usage Instructions

### Step 1: Input Parameters
- **Total Memory (bytes)**: Enter the total memory capacity available for the simulation, e.g., `1000`.
- **Page Size (bytes)**: Specify the size of each page, e.g., `100`.
- **Number of Frames**: Enter the number of frames available in memory, e.g., `3`.
- **CPU Reference String**: Input a reference string of page requests, separated by spaces, e.g., `1 2 3 4 1 2 5 1 2 3 4 5`.

### Step 2: Select a Page Replacement Algorithm
- From the dropdown menu, choose one of the algorithms:
  - **FIFO**
  - **LRU**
  - **Optimal**
  - **Random**

### Step 3: Run the Simulation
- Click on the "Run Simulation" button to execute the algorithm using the provided inputs.

### Step 4: View Results
- The results will display:
  - Total **page faults**.
  - Total **hits**.
  - **Hit ratio** and **miss ratio**.
- The memory states and swap space will be displayed for each step of the simulation.

---

## Example Simulation

### Input Parameters:
- **Total Memory (bytes)**: `1000`
- **Page Size (bytes)**: `100`
- **Number of Frames**: `3`
- **CPU Reference String**: `1 2 3 4 1 2 5 1 2 3 4 5`
- **Algorithm**: FIFO

### Output:
- **Page Faults**: 9
- **Hits**: 3
- **Hit Ratio**: 0.2500
- **Miss Ratio**: 0.7500

### Step-by-Step Execution:
Step 1: [1] --> Miss Frames: [1] Swap Space: []

Step 2: [1, 2] --> Miss Frames: [1, 2] Swap Space: []

Step 3: [1, 2, 3] --> Miss Frames: [1, 2, 3] Swap Space: []

Step 4: [2, 3, 4] --> Miss (Removed 1) Frames: [2, 3, 4] Swap Space: [1]

...

---

## Algorithms Explained

1. **FIFO (First-In-First-Out)**:
   - Replaces the oldest page in memory.
   - Simple but may not always result in optimal performance.

2. **LRU (Least Recently Used)**:
   - Tracks the usage history of pages.
   - Replaces the page that has not been accessed for the longest time.

3. **Optimal**:
   - Selects the page that will not be needed for the longest duration in the future.
   - Yields the best performance but requires prior knowledge of the reference string.

4. **Random**:
   - Picks any page at random for replacement.
   - Quick and easy but lacks predictability.

---

## Troubleshooting

- **Invalid Input**:
  - Ensure all input fields contain valid positive integers.
  - Verify that the reference string is formatted correctly.

- **Application Freezes**:
  - Avoid excessively long reference strings or extreme parameter values.

- **Algorithm Errors**:
  - Verify that the selected algorithm is applicable to the given inputs.


---

## Contact

For any questions, suggestions, or bug reports, please feel free to contact the developer:

- **Email**: [jaswanthr57@gmail.com]
- **GitHub Issues**: Submit your issues via the repository's issues tracker.

---

