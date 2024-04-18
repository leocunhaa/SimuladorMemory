import time
from typing import List

from utils.examples import ROUND_ROBIN_EXAMPLES
from utils import Process, print_table, GanttChart, print_gantt_chart

import logging

logging.basicConfig(level=logging.DEBUG)


# ROUND ROBIN FINALIZADO COM SUCESSO

class CPU:
    def __init__(self, num_cores=4, instr_per_core=7, clock=1000):
        self.num_cores = num_cores
        self.instr_per_core = instr_per_core
        self.clock = clock

    def execute(self, process):
        print(f"Executing process {process.name} on CPU")
        remaining_instructions = process.remaining_instructions
        while remaining_instructions > 0:
            # Executa instruções até atingir a capacidade do núcleo ou acabarem as instruções do processo
            for core in range(self.num_cores):
                if remaining_instructions > 0:
                    instructions_to_execute = min(remaining_instructions, self.instr_per_core)
                    print(f"Core {core + 1}: Executing {instructions_to_execute} instructions")
                    remaining_instructions -= instructions_to_execute
            time.sleep(self.clock / 1000)  # Aguarda o tempo do clock
        print(f"Process {process.name} completed execution")

class MemoryManager:
    def __init__(self, physical_memory_size=256, page_size=4):
        self.physical_memory_size = physical_memory_size  # Tamanho da memória física em KB
        self.page_size = page_size  # Tamanho da página de paginação em KB
        self.page_table = {}  # Tabela de páginas

    def add_process_to_memory(self, process):
        # Verifica se há espaço suficiente na memória para o processo
        required_memory = process.size
        if required_memory > self.physical_memory_size:
            print(f"Error: Not enough physical memory for process {process.name}")
            return False

        # Calcula o número de páginas necessárias para o processo
        num_pages = required_memory // self.page_size
        if required_memory % self.page_size != 0:
            num_pages += 1

        # Verifica se há espaço suficiente na memória para todas as páginas do processo
        if len(self.page_table) + num_pages > self.physical_memory_size // self.page_size:
            print(f"Error: Not enough physical memory for process {process.name}")
            return False

        # Aloca as páginas do processo na memória
        for i in range(num_pages):
            page_number = len(self.page_table) + i
            self.page_table[page_number] = process.name

        print(f"Added process {process.name} to memory")
        return True

    def is_memory_full(self):
        return len(self.page_table) == self.physical_memory_size // self.page_size

    def __str__(self):
        return f"Physical Memory Size: {self.physical_memory_size} KB, Page Size: {self.page_size} KB"


# Definindo o quantum para o Round Robin como 3000ms
ROUND_ROBIN_QUANTUM = 3000

def round_robin(processes: List[Process], time_slice: int, quantum: int, clock: int) -> None:
    current_time = 0
    gantt_chart = []
    executed_queue = []
    memory = []  # Lista para armazenar os processos na memória
    memory_capacity = 0  # Capacidade total da memória
    memory_full_log = []  # Log para memória cheia
    page_fault_log = []  # Log para page faults

    logging.info("Initial processes:")
    print_table(processes)

    while processes or memory:
        # Adicionando processos na memória enquanto houver espaço e processos a executar
        while processes and processes[0].size + memory_capacity <= 254:
            process = processes.pop(0)
            memory.append(process)
            memory_capacity += process.size
            logging.info(f"Added process {process.name} to memory at time {current_time}")

        # Verificando se há processos na memória
        if memory:
            process = memory.pop(0)
            logging.info(f"Executing process {process.name} at time {current_time}")

            if process.remaining_time > time_slice:
                current_time += time_slice
                process.remaining_time -= time_slice
                process.next_arrival_time = current_time
                memory.append(process)
            else:
                current_time += process.remaining_time
                process.remaining_time = 0
                process.waiting_time = current_time - process.arrival_time - process.burst_time
                process.turnaround_time = current_time - process.arrival_time
                executed_queue.append(process)
                logging.info(f"Process {process.name} completed at time {current_time}")

            gantt_chart.append(GanttChart(name=process.name, arrival_time=current_time + process.remaining_time))

        # Verificando se é hora de fazer o quantum
        if current_time % quantum == 0:
            logging.info(f"Quantum time reached at time {current_time}")

        # Verificando se é hora de fazer o clock
        if current_time % clock == 0:
            logging.info(f"Clock time reached at time {current_time}")

        # Verificando se há page fault (processos não carregados na memória)
        if processes and processes[0].size + memory_capacity > 254:
            process = processes[0]
            page_fault_log.append(f"Page Fault occurred for process {process.name} at time {current_time}")
            logging.info(f"Page Fault occurred for process {process.name} at time {current_time}")
            processes.pop(0)

        # Verificando se a memória está cheia
        if memory_capacity == 254:
            memory_full_log.append(f"Memory is full at time {current_time}")
            logging.info(f"Memory is full at time {current_time}")

    logging.info("Final executed processes:")
    print_table(executed_queue)

    logging.info("Gantt Chart:")
    print_gantt_chart(gantt_chart)

    logging.info("Page Fault Log:")
    for entry in page_fault_log:
        logging.info(entry)

    logging.info("Memory Full Log:")
    for entry in memory_full_log:
        logging.info(entry)


if __name__ == '__main__':
    print("-------------------------")
    logging.debug("Detalhes do teste")
    logging.info("Iniciando teste")
    print("-------------------------")

    example = ROUND_ROBIN_EXAMPLES.example1
    round_robin(processes=example.processes, time_slice=example.time_slice, quantum=3000, clock=500)

    print("-------------------------")
    logging.info("Teste concluído com sucesso!")
    print("-------------------------")