# PageControl - Memory Management Simulator with Virtual Memory

## Overview

**PageControl** is a memory management simulator that demonstrates two popular paging algorithms: **FIFO (First In, First Out)** and **LRU (Least Recently Used)**. The simulator models how an operating system handles memory paging and utilizes **virtual memory** to simulate page faults and memory management operations.

In this project, you'll be able to see how pages are loaded into memory, how page faults occur, and how virtual memory (swap space) is used to manage processes when physical memory is full.

## Features

- Simulate **FIFO** and **LRU** paging algorithms.
- Track memory hits, misses, and page faults.
- Display step-by-step memory frame states with hit/miss status.
- Show virtual memory (swap space) used for storing evicted pages.

## How It Works

This simulator simulates the process of managing memory pages in an operating system using two paging algorithms:

### 1. FIFO (First In, First Out)
- The **FIFO** algorithm replaces the oldest page when a new page needs to be loaded into memory.

### 2. LRU (Least Recently Used)
- The **LRU** algorithm replaces the least recently used page when a new page needs to be loaded into memory.

**Virtual Memory** is used to store pages that are evicted from physical memory. When a page is evicted from the main memory, it is placed into the **swap space** (virtual memory), and when needed again, it is swapped back into the physical memory.

## How to Run
Download the exe file and install it in your computer.
Google drive link: https://drive.google.com/file/d/1AxX5fWoE6gp3FZs6RUbd0Yi4qpPxfFew/view?usp=sharing
