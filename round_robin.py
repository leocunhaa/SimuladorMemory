from typing import List

from utils.examples import ROUND_ROBIN_EXAMPLES
from utils import Process, print_table, GanttChart, print_gantt_chart

import logging

logging.basicConfig(level=logging.DEBUG)


def round_robin(processes: List[Process], time_slice: int) -> None:

    # Inicializa as variáveis

    current_time = 0
    gantt_chart = []
    executed_queue = []

    logging.info("Initial processes:")
    print_table(processes)

    while processes:
        processes.sort(key=lambda p: p.next_arrival_time)
        process = processes.pop(0)

        logging.info(f"Executing process {process.name} at time {current_time}")

        if process.remaining_time > time_slice:
            current_time += time_slice
            process.remaining_time -= time_slice
            process.next_arrival_time = current_time
            processes.append(process)
        else:
            current_time += process.remaining_time
            process.remaining_time = 0
            process.waiting_time = current_time - process.arrival_time - process.burst_time
            process.turnaround_time = current_time - process.arrival_time
            executed_queue.append(process)
            logging.info(f"Process {process.name} completed at time {current_time}")


        gantt_chart.append(GanttChart(name=process.name, arrival_time=current_time + process.remaining_time))

    logging.info("Final executed processes:")
    print_table(executed_queue)

    logging.info("Gantt Chart:")
    print_gantt_chart(gantt_chart)


if __name__ == '__main__':
    print("-------------------------")
    logging.debug("Detalhes do teste")
    logging.info("Iniciando teste")
    print("-------------------------")

    example = ROUND_ROBIN_EXAMPLES.example1
    round_robin(processes=example.processes, time_slice=example.time_slice)

    print("-------------------------")
    logging.info("Teste concluido com sucesso!")
    print("-------------------------")

