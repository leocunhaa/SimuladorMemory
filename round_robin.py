from typing import List

from utils.examples import ROUND_ROBIN_EXAMPLES
from utils import Process, print_table, GanttChart, print_gantt_chart

import logging

logging.basicConfig(level=logging.DEBUG)


# ROUND ROBIN FINALIZADO COM SUCESSO

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