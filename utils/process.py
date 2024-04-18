from dataclasses import dataclass, field
import math
from typing import List


@dataclass(order=True)
class Process:
    name: str
    arrival_time: int
    burst_time: int
    priority: int = field(init=True, default=0)
    waiting_time: int = field(init=False, default=0)
    turnaround_time: int = field(init=False, default=0)
    remaining_time: int = field(init=False, default=0, repr=True)
    next_arrival_time: int = field(init=False, default=0, repr=False)
    size: int = field(init=True, default=0)
    subprocesses: List[str] = field(init=False, default_factory=list)

    def __post_init__(self):
        self.remaining_time = self.burst_time
        self.next_arrival_time = self.arrival_time
        self.split_into_subprocesses()

    def split_into_subprocesses(self):
        num_subprocesses = math.ceil(self.size / 1)  # Dividir o tamanho do processo em subprocessos de 1 KB
        for i in range(num_subprocesses):
            subprocess_name = f"{self.name}_Sub_{i+1}"
            self.subprocesses.append(subprocess_name)

    def __str__(self):
        return f"Process Name: {self.name}, Arrival Time: {self.arrival_time}, Burst Time: {self.burst_time}, Size: {self.size}, Subprocesses: {self.subprocesses}"


# Exemplo de uso:
p1 = Process(name='P1', arrival_time=0, burst_time=10, size=100)
print(p1)