# Memory Hierarchy Simulator

## Overview

This project implements a **Memory Hierarchy Simulator** that showcases how data moves through levels of memory in a computer system. The simulator demonstrates the interaction between **SSD, DRAM, and multi-level cache (L3, L2, L1)** and enforces hierarchical data movement.


---

## Features

* Simulates full memory hierarchy:

  * SSD → DRAM → L3 Cache → L2 Cache → L1 Cache → CPU
* Interactive command-line interface
* Instruction access tracing
* Data movement visualization across memory levels
* Cache hit and miss tracking
* LRU (Least Recently Used) cache replacement policy
* Clock cycle simulation
* Final memory state reporting

---

## Memory Hierarchy Configuration

| Level | Capacity |
| ----- | -------- |
| SSD   | 100      |
| DRAM  | 50       |
| L3    | 10       |
| L2    | 5        |
| L1    | 3        |

---

## How to Run the Program

### Requirements

* Python 3.x

### Run the program:

```bash
python your_file_name.py
```

---

## Commands

The simulator supports the following commands:

| Command                 | Description                                  |
| ----------------------- | -------------------------------------------- |
| `LOAD <address> <data>` | Loads data into the system starting from SSD |
| `R <address>`           | Reads data (fetch operation)                 |
| `W <address> <data>`    | Writes data to memory                        |
| `SHOW`                  | Displays final memory state and performance  |
| `Q`                     | Exits the program                            |

---

## Example Usage

### Input:

```
LOAD A 100
LOAD B 200
R A
W C 300
SHOW
Q
```

---

## Sample Output

### Memory Hierarchy Configuration

```
===== MEMORY HIERARCHY CONFIGURATION =====
SSD (Capacity: 100)
DRAM (Capacity: 50)
L3 (Capacity: 10)
L2 (Capacity: 5)
L1 (Capacity: 3)
Order: SSD → DRAM → L3 → L2 → L1 → CPU
==========================================
```

### Instruction Trace Example

```
=== INSTRUCTION TRACE: READ A ===
Trace Path: L1
Cache Result: HIT at L1
```

### Data Movement Example

```
Data Movement:
  SSD → DRAM
  DRAM → L3
  L3 → L2
  L2 → L1
```

### Final State

```
========== FINAL MEMORY STATE ==========
L1    | Size: 3/3 | Data: ['A', 'B', 'C']
...
```

---

## System Behavior

### Read Operation
* If data is found → **Cache Hit**
* If not found → **Cache Miss**
* Data is promoted upward to L1 cache

### Write Operation

* Data is written to L1 cache first
* Then propagated downward through all levels (write-back behavior)

### Load Operation

* Simulates loading data from SSD into all higher memory levels

---

## Design Details

* **MemoryLevel Class**: Represents SSD and DRAM
* **Cache Class**: Implements LRU cache using `OrderedDict`
* **MemorySystem Class**: Controls hierarchy operations and simulation logic

---
