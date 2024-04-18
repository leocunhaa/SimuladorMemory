import time
from typing import List

from utils import Process, print_table, GanttChart, print_gantt_chart

import logging

logging.basicConfig(level=logging.DEBUG)

class CPU:
    def __init__(self, num_cores=4, instr_per_core=7, clock=1000):
        self.num_cores = num_cores
        self.instr_per_core = instr_per_core
        self.clock = clock

    def execute(self, process):
        logging.info(f"Executing process {process.name} on CPU")
        remaining_instructions = process.remaining_instructions
        while remaining_instructions > 0:
            for core in range(self.num_cores):
                if remaining_instructions > 0:
                    instructions_to_execute = min(remaining_instructions, self.instr_per_core)
                    logging.info(f"Core {core + 1}: Executing {instructions_to_execute} instructions")
                    remaining_instructions -= instructions_to_execute
            time.sleep(self.clock / 1000)
        logging.info(f"Process {process.name} completed execution")

class MemoryManager:
    def __init__(self, physical_memory_size=256, page_size=4):
        self.physical_memory_size = physical_memory_size
        self.page_size = page_size
        self.page_table = {}

    def add_process_to_memory(self, process):
        required_memory = process.size
        if required_memory > self.physical_memory_size:
            logging.error(f"Error: Not enough physical memory for process {process.name}")
            return False

        num_pages = required_memory // self.page_size
        if required_memory % self.page_size != 0:
            num_pages += 1

        if len(self.page_table) + num_pages > self.physical_memory_size // self.page_size:
            logging.error(f"Error: Not enough physical memory for process {process.name}")
            return False

        for i in range(num_pages):
            page_number = len(self.page_table) + i
            self.page_table[page_number] = process.name

        logging.info(f"Added process {process.name} to memory")
        return True

    def is_memory_full(self):
        return len(self.page_table) == self.physical_memory_size // self.page_size

    def __str__(self):
        return f"Physical Memory Size: {self.physical_memory_size} KB, Page Size: {self.page_size} KB"

def fcfs(processes: List[Process], memory_size: int) -> None:
    current_time = 0
    gantt_chart = []
    memory_manager = MemoryManager(physical_memory_size=memory_size)

    logging.info("Initial processes:")
    print_table(processes)

    for process in processes:
        if not memory_manager.add_process_to_memory(process):
            break

        logging.info(f"Executing process {process.name} at time {current_time}")

        cpu = CPU()
        cpu.execute(process)

        current_time += process.burst_time

        gantt_chart.append(GanttChart(name=process.name, arrival_time=current_time))

    logging.info("Final executed processes:")
    print_table(processes)

    logging.info("Gantt Chart:")
    print_gantt_chart(gantt_chart)


if __name__ == '__main__':
    print("-------------------------")
    logging.debug("Detalhes do teste")
    logging.info("Iniciando teste")
    print("-------------------------")

    # Define os processos e o tamanho da memória conforme o exemplo
    processes = [
        Process(name="P1", burst_time=15, size=130),
        Process(name="P2", burst_time=6, size=90),
        Process(name="P3", burst_time=7, size=34),
        Process(name="P4", burst_time=5, size=30),
    ]
    memory_size = 256  # Tamanho da memória em KB

    fcfs(processes, memory_size)

    print("-------------------------")
    logging.info("Teste concluído com sucesso!")
    print("-------------------------")
