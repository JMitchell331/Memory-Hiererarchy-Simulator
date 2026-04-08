from collections import OrderedDict


class MemoryLevel:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.storage = OrderedDict()

    def read(self, address):
        return self.storage.get(address)

    def write(self, address, data):
        if address in self.storage:
            del self.storage[address]

        elif len(self.storage) >= self.size:
            evicted_address, evicted_data = self.storage.popitem(last=False)
            print(f"[{self.name}] Evicted {evicted_address} = {evicted_data}")

        self.storage[address] = data

    def display(self):
        keys = list(self.storage.keys())
        print(
            f"{self.name:5} | Size: {len(self.storage)}/{self.size} | Data: {keys}"
        )


class Cache(MemoryLevel):
    def read(self, address):
        if address in self.storage:
            data = self.storage.pop(address)
            self.storage[address] = data  # Move to end for LRU
            return data
        return None


class MemorySystem:
    def __init__(self):
        self.ssd = MemoryLevel("SSD", 100)
        self.dram = MemoryLevel("DRAM", 50)
        self.l3 = Cache("L3", 10)
        self.l2 = Cache("L2", 5)
        self.l1 = Cache("L1", 3)

        # Ordered from lowest level to highest level
        self.levels = [self.ssd, self.dram, self.l3, self.l2, self.l1]

        self.clock_cycles = 0
        self.cache_hits = 0
        self.cache_misses = 0

    def tick(self, cycles=1):
        self.clock_cycles += cycles

    def show_configuration(self):
        print("\n===== MEMORY HIERARCHY CONFIGURATION =====")
        print(f"SSD  (Capacity: {self.ssd.size})")
        print(f"DRAM (Capacity: {self.dram.size})")
        print(f"L3   (Capacity: {self.l3.size})")
        print(f"L2   (Capacity: {self.l2.size})")
        print(f"L1   (Capacity: {self.l1.size})")
        print("Order: SSD → DRAM → L3 → L2 → L1 → CPU")
        print("==========================================")

    def load(self, address, data):
        print(f"\n=== LOAD {address} = {data} ===")

        print("Data Movement:")

        previous = None
        for level in self.levels:
            level.write(address, data)

            if previous is not None:
                print(f"  {previous} → {level.name}")

            previous = level.name
            self.tick()

    def read(self, address):
        print(f"\n=== INSTRUCTION TRACE: READ {address} ===")

        trace = []

        # Search from highest cache level to lowest memory level
        for index in range(len(self.levels) - 1, -1, -1):
            level = self.levels[index]
            trace.append(level.name)

            data = level.read(address)
            self.tick()

            if data is not None:
                print(f"Trace Path: {' → '.join(trace)}")
                print(f"Cache Result: HIT at {level.name}")
                print(f"Data Found: {address} = {data}")

                self.cache_hits += 1

                # Promote data upward toward L1 if it was found lower down
                if level != self.l1:
                    print("Data Movement:")

                    for promote_index in range(index + 1, len(self.levels)):
                        destination = self.levels[promote_index]
                        source = self.levels[promote_index - 1]

                        destination.write(address, data)
                        print(f"  {source.name} → {destination.name}")
                        self.tick()

                return

        print(f"Trace Path: {' → '.join(trace)}")
        print("Cache Result: MISS")
        print(f"Address {address} was not found in any memory level.")

        self.cache_misses += 1

    def write(self, address, data):
        print(f"\n=== INSTRUCTION TRACE: WRITE {address} = {data} ===")
        print("Data Movement:")

        # Write starts at L1 and propagates downward
        write_path = [self.l1, self.l2, self.l3, self.dram, self.ssd]

        previous = "CPU"

        for level in write_path:
            level.write(address, data)
            print(f"  {previous} → {level.name}")
            previous = level.name
            self.tick()

    def show_final_state(self):
        print("\n========== FINAL MEMORY STATE ==========")
        self.l1.display()
        self.l2.display()
        self.l3.display()
        self.dram.display()
        self.ssd.display()

        print("\n========== PERFORMANCE ==========")
        print(f"Total Clock Cycles : {self.clock_cycles}")
        print(f"Total Cache Hits   : {self.cache_hits}")
        print(f"Total Cache Misses : {self.cache_misses}")
        print("=================================")


# ------------------------
# Main Program
# ------------------------

def main():
    memory = MemorySystem()
    memory.show_configuration()

    print("\nCommands:")
    print("  LOAD <address> <data>")
    print("  R <address>")
    print("  W <address> <data>")
    print("  SHOW")
    print("  Q")

    while True:
        command = input("\nEnter command: ").strip()

        if not command:
            continue

        parts = command.split()
        action = parts[0].upper()

        try:
            if action == "LOAD":
                if len(parts) != 3:
                    print("Usage: LOAD <address> <data>")
                    continue

                address = parts[1]
                data = parts[2]
                memory.load(address, data)

            elif action == "R":
                if len(parts) != 2:
                    print("Usage: R <address>")
                    continue

                address = parts[1]
                memory.read(address)

            elif action == "W":
                if len(parts) != 3:
                    print("Usage: W <address> <data>")
                    continue

                address = parts[1]
                data = parts[2]
                memory.write(address, data)

            elif action == "SHOW":
                memory.show_final_state()

            elif action == "Q":
                print("\nExiting simulator.")
                break

            else:
                print("Invalid command.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
