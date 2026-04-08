from collections import OrderedDict


class MemoryLevel:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.storage = OrderedDict()

    def read(self, address):
        if address in self.storage:
            value = self.storage.pop(address)
            self.storage[address] = value
            return value
        return None

    def write(self, address, data):
        if address in self.storage:
            self.storage.pop(address)
        elif len(self.storage) >= self.size:
            evicted = self.storage.popitem(last=False)
            print(f"{self.name}: Evicting {evicted[0]}")

        self.storage[address] = data

    def contents(self):
        return list(self.storage.keys())


class MemorySystem:

    def __init__(self):

        self.ssd = MemoryLevel("SSD", 100)
        self.dram = MemoryLevel("DRAM", 50)
        self.l3 = MemoryLevel("L3", 10)
        self.l2 = MemoryLevel("L2", 5)
        self.l1 = MemoryLevel("L1", 3)

        self.levels = [self.l1, self.l2, self.l3, self.dram, self.ssd]

        self.clock = 0
        self.hits = 0
        self.misses = 0

        self.print_configuration()

    def tick(self):
        self.clock += 1

    def print_configuration(self):
        print("\n===== MEMORY HIERARCHY CONFIGURATION =====")
        print("SSD (Capacity: 100)")
        print("DRAM (Capacity: 50)")
        print("L3  (Capacity: 10)")
        print("L2  (Capacity: 5)")
        print("L1  (Capacity: 3)")
        print("Order: SSD → DRAM → L3 → L2 → L1 → CPU")
        print("==========================================")

    def load(self, address, data):

        print(f"\n=== LOAD {address} = {data} ===")

        self.ssd.write(address, data)

        prev = "SSD"
        print("Data Movement:")

        for level in [self.dram, self.l3, self.l2, self.l1]:
            level.write(address, data)
            print(f"  {prev} → {level.name}")
            prev = level.name
            self.tick()

    def fetch(self, address):

        print(f"\n=== INSTRUCTION TRACE: READ {address} ===")

        trace = []

        for i, level in enumerate(self.levels):

            trace.append(level.name)

            data = level.read(address)

            if data is not None:

                print("Trace Path:", " → ".join(trace))
                print(f"Cache Result: HIT at {level.name}")

                self.hits += 1

                self.promote(address, data, i)

                return

            self.tick()

        print("Trace Path:", " → ".join(trace))
        print("Cache Result: MISS")

        self.misses += 1

    def promote(self, address, data, level_index):

        if level_index == 0:
            return

        print("Data Movement:")

        for i in range(level_index - 1, -1, -1):

            upper = self.levels[i]
            lower = self.levels[i + 1]

            upper.write(address, data)

            print(f"  {lower.name} → {upper.name}")

            self.tick()

    def write(self, address, data):

        print(f"\n=== INSTRUCTION TRACE: WRITE {address} = {data} ===")

        prev = "CPU"

        print("Data Movement:")

        for level in self.levels:

            level.write(address, data)

            print(f"  {prev} → {level.name}")

            prev = level.name

            self.tick()

    def show(self):

        print("\n========== FINAL MEMORY STATE ==========")

        for level in self.levels[::-1]:

            print(
                f"{level.name:5} | Size: {len(level.storage)}/{level.size} | Data: {level.contents()}"
            )

        print("\n========== PERFORMANCE ==========")

        print("Total Clock Cycles :", self.clock)
        print("Total Cache Hits   :", self.hits)
        print("Total Cache Misses :", self.misses)

        print("=================================")


def run():

    system = MemorySystem()

    print("\nCommands:")
    print("LOAD <address> <data>")
    print("R <address>")
    print("W <address> <data>")
    print("SHOW")
    print("Q")

    while True:

        cmd = input("\n>>> ").split()

        if not cmd:
            continue

        if cmd[0].upper() == "LOAD":
            system.load(cmd[1], cmd[2])

        elif cmd[0].upper() == "R":
            system.fetch(cmd[1])

        elif cmd[0].upper() == "W":
            system.write(cmd[1], cmd[2])

        elif cmd[0].upper() == "SHOW":
            system.show()

        elif cmd[0].upper() == "Q":
            print("Exiting simulator.")
            break

        else:
            print("Invalid command")


if __name__ == "__main__":
    run()