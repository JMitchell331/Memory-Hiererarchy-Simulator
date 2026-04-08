import random
from collections import OrderedDict


class memLevel:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.storage = {}

    def readerFunc(self, address):
        return self.storage.get(address, None)

    def writerFunc(self, address, data):
        if len(self.storage) >= self.size:
            self.evictor()
        self.storage[address] = data

    def evictor(self):
        if self.storage:
            key = random.choice(list(self.storage.keys()))
            print(f"  [Evict] {self.name}: {key}")
            del self.storage[key]

    def contents(self):
        return list(self.storage.keys())


class Cache(memLevel):
    def __init__(self, name, size):
        super().__init__(name, size)
        self.storage = OrderedDict()

    def readerFunc(self, address):
        if address in self.storage:
            self.storage.move_to_end(address)
            return self.storage[address]
        return None

    def writerFunc(self, address, data):
        if address in self.storage:
            self.storage.move_to_end(address)
        else:
            if len(self.storage) >= self.size:
                self.evictor()
        self.storage[address] = data

    def evictor(self):
        evicted_address, _ = self.storage.popitem(last=False)
        print(f"  [Evict] {self.name}: {evicted_address}")


class memSystem:
    def __init__(self):
        self.clock = 0
        self.hits = 0
        self.misses = 0

        self.ssd = memLevel("SSD", 100)
        self.dram = memLevel("DRAM", 50)
        self.l3 = Cache("L3", 10)
        self.l2 = Cache("L2", 5)
        self.l1 = Cache("L1", 3)

        self.levels = [self.ssd, self.dram, self.l3, self.l2, self.l1]

    def tick(self):
        self.clock += 1


    def showConfiguration(self):
        print("\n===== MEMORY HIERARCHY CONFIGURATION =====")
        for level in self.levels:
            print(f"{level.name} (Capacity: {level.size})")
        print("Order: SSD → DRAM → L3 → L2 → L1 → CPU")
        print("==========================================")


    def fetch(self, address):
        print(f"\n=== INSTRUCTION TRACE: READ {address} ===")

        trace_path = []

        for i in range(len(self.levels)-1, -1, -1):
            level = self.levels[i]
            trace_path.append(level.name)

            data = level.read(address)

            if data is not None:
                print(f"Trace Path: {' → '.join(trace_path)}")
                print(f"Cache Result: HIT at {level.name}")
                self.hits += 1

                self.promote(address, data, i)
                return

        print(f"Trace Path: {' → '.join(trace_path)}")
        print("Cache Result: MISS")
        self.misses += 1


    def promote(self, address, data, level_index):
        print("Data Movement:")

        for i in range(level_index + 1, len(self.levels)):
            src = self.levels[i - 1].name
            dest = self.levels[i].name

            self.levels[i].write(address, data)
            print(f"  {src} → {dest}")
            self.tick()


    def loadFromSSD(self, address, data):
        print(f"\n=== LOAD {address} = {data} ===")

        self.ssd.writerFunc(address, data)

        print("Data Movement:")
        prev = "SSD"

        for level in self.levels[1:]:
            level.write(address, data)
            print(f"  {prev} → {level.name}")
            prev = level.name
            self.tick()


    def write(self, address, data):
        print(f"\n=== INSTRUCTION TRACE: WRITE {address} = {data} ===")

        print("Data Movement:")
        prev = "CPU"

        self.l1.writerFunc(address, data)
        print(f"  {prev} → L1")
        prev = "L1"

        for level in [self.l2, self.l3, self.dram, self.ssd]:
            level.write(address, data)
            print(f"  {prev} → {level.name}")
            prev = level.name
            self.tick()


    def display(self):
        print("\n========== FINAL MEMORY STATE ==========")

        for level in self.levels:
            print(f"{level.name:5} | Size: {len(level.storage)}/{level.size} | Data: {list(level.storage.keys())}")

        print("\n========== PERFORMANCE ==========")
        print(f"Total Clock Cycles : {self.clock}")
        print(f"Total Cache Hits   : {self.hits}")
        print(f"Total Cache Misses : {self.misses}")
        print("=======================================")



def interactiveMode():
    system = memSystem()
    system.showConfiguration()

    print("\nCommands:")
    print("  LOAD <addr> <data>")
    print("  R <addr>")
    print("  W <addr> <data>")
    print("  SHOW")
    print("  Q\n")

    while True:
        cmd = input(">>> ").strip()
        parts = cmd.split()

        if not parts:
            continue

        if parts[0].upper() == 'Q':
            print("Exiting program...")
            break

        elif parts[0].upper() == 'LOAD':
            system.loadFromSSD(parts[1], int(parts[2]))

        elif parts[0].upper() == 'R':
            system.fetch(parts[1])

        elif parts[0].upper() == 'W':
            system.write(parts[1], int(parts[2]))

        elif parts[0].upper() == 'SHOW':
            system.display()

        else:
            print("Invalid command")



if __name__ == "__main__":
    interactiveMode()