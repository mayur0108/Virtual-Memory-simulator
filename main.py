################MayurKumar Patel######################
################OS FINAL PROJECT######################

# Virtual Memory Simulator with FIFO, LRU, Clock, and Aging Page Replacement Algorithms

# Initialization
virtual_memory_size = 10  # Number of virtual pages
physical_memory_size = 5  # Number of physical frames
physical_memory = [None] * physical_memory_size
page_table = {}

# Performance Metrics
total_accesses = 0
total_page_faults = 0
total_hit_time = 0
total_fault_time = 0
hit_time = 1
fault_time = 10

# FIFO Page Replacement Algorithm
fifo_queue = []  # Queue to track the order of pages loaded into memory
def fifo_replacement(page_number):
    global total_page_faults, total_fault_time
    if page_number in page_table:
        return False  # No replacement needed, page already in memory
    if len(fifo_queue) < physical_memory_size:
        # Add new page to physical memory and FIFO queue
        fifo_queue.append(page_number)
    else:
        # Replace the oldest page (first in the queue)
        oldest_page = fifo_queue.pop(0)
        del page_table[oldest_page]
        fifo_queue.append(page_number)
    frame_number = fifo_queue.index(page_number)
    physical_memory[frame_number] = page_number
    page_table[page_number] = frame_number
    total_page_faults += 1
    total_fault_time += fault_time
    return True  # Page replaced

# LRU Page Replacement Algorithm
access_history = []
def lru_replacement(page_number):
    global total_page_faults, total_fault_time
    if page_number in page_table:
        access_history.remove(page_number)
        access_history.append(page_number)
        return False
    if None in physical_memory:
        frame_number = physical_memory.index(None)
    else:
        lru_page = access_history.pop(0)
        frame_number = page_table[lru_page]
        del page_table[lru_page]
    physical_memory[frame_number] = page_number
    page_table[page_number] = frame_number
    access_history.append(page_number)
    total_page_faults += 1
    total_fault_time += fault_time
    return True


# Clock Page Replacement Algorithm
clock_pointer = 0
use_bits = [False] * physical_memory_size
def clock_replacement(page_number):
    global total_page_faults, total_fault_time, clock_pointer
    if page_number in page_table:
        use_bits[page_table[page_number]] = True
        return False
    while True:
        if not use_bits[clock_pointer]:
            if physical_memory[clock_pointer] is not None:
                del page_table[physical_memory[clock_pointer]]
            physical_memory[clock_pointer] = page_number
            page_table[page_number] = clock_pointer
            total_page_faults += 1
            total_fault_time += fault_time
            clock_pointer = (clock_pointer + 1) % physical_memory_size
            return True
        use_bits[clock_pointer] = False
        clock_pointer = (clock_pointer + 1) % physical_memory_size


# Aging Page Replacement Algorithm
aging_counters = [0] * physical_memory_size  # Age counters for each frame
def aging_replacement(page_number):
    global total_page_faults, total_fault_time, aging_counters
    if page_number in page_table:
        aging_counters[page_table[page_number]] = 0xFF
        return False
    if None in physical_memory:
        frame_number = physical_memory.index(None)
    else:
        oldest_frame = aging_counters.index(min(aging_counters))
        del page_table[physical_memory[oldest_frame]]
        frame_number = oldest_frame
    physical_memory[frame_number] = page_number
    page_table[page_number] = frame_number
    aging_counters[frame_number] = 0xFF
    total_page_faults += 1
    total_fault_time += fault_time
    return True

# Memory Access Function
def access_memory(page_number, replacement_algorithm):
    global total_accesses, total_hit_time, aging_counters
    if replacement_algorithm == "Aging":
        aging_counters = [age >> 1 for age in aging_counters]
    page_fault = False
    if page_number >= virtual_memory_size:
        print("Page number out of range.")
        return
    if replacement_algorithm == "FIFO":
        page_fault = fifo_replacement(page_number)
    elif replacement_algorithm == "LRU":
        page_fault = lru_replacement(page_number)
    elif replacement_algorithm == "Clock":
        page_fault = clock_replacement(page_number)
    elif replacement_algorithm == "Aging":
        page_fault = aging_replacement(page_number)
    total_accesses += 1
    if page_fault:
        print(f"Page fault occurred, loaded page {page_number} into frame {page_table[page_number]}")
    else:
        total_hit_time += hit_time
        print(f"Accessed page {page_number} in frame {page_table[page_number]}")

# Performance Metrics Display
def display_performance_metrics():
    if total_accesses == 0:
        print("No memory accesses have been made yet.")
        return
    hit_ratio = ((total_accesses - total_page_faults) / total_accesses) * 100
    average_access_time = (total_hit_time + total_fault_time) / total_accesses
    throughput = total_accesses / (total_hit_time + total_fault_time)
    print(f"Total Memory Accesses: {total_accesses}")
    print(f"Total Page Faults: {total_page_faults}")
    print(f"Page Fault Rate: {100 - hit_ratio:.2f}%")
    print(f"Hit Ratio: {hit_ratio:.2f}%")
    print(f"Average Memory Access Time: {average_access_time:.2f} units")
    print(f"Throughput: {throughput:.2f} accesses/unit time")


# User Interface
def start_simulation():
    print("Select Page Replacement Algorithm:")
    print("1. FIFO")
    print("2. LRU")
    print("3. Clock")
    print("4. Aging")
    algorithm_choice = input("Enter your choice (1, 2, 3, or 4): ")
    replacement_algorithm = "LRU" if algorithm_choice == "2" else "Clock" if algorithm_choice == "3" else "Aging" if algorithm_choice == "4" else "FIFO"

    while True:
        print("\nVirtual Memory Simulator")
        print("1. Access Memory")
        print("2. Show Memory State")
        print("3. Show Performance Metrics")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            page = int(input("Enter page number to access: "))
            access_memory(page, replacement_algorithm)
        elif choice == "2":
            print("Physical Memory:", physical_memory)
            print("Page Table:", page_table)
        elif choice == "3":
            display_performance_metrics()
        elif choice == "4":
            break
        else:
            print("Invalid choice")

# Start the simulator
start_simulation()
