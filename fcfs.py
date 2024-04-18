import logging
from typing import List

from utils import print_table, Process, GanttChart, print_gantt_chart
from utils.examples import FCFS_EXAMPLES

logging.basicConfig(level=logging.DEBUG)

def fcfs(processes: List[Process]) -> None:
    
    processes.sort(key=lambda p: p.arrival_time)
    current_time = 0
    gantt_chart = []

    for process in processes:
        process.waiting_time = max(0, current_time - process.arrival_time)
        process.turnaround_time = process.burst_time + process.waiting_time
        current_time = process.turnaround_time  # Ajuste aqui
        gantt_chart.append(GanttChart(name=process.name, arrival_time=current_time))

    print_gantt_chart(gantt_chart)
    print_table(processes)


if __name__ == '__main__':
    print("-------------------------")
    logging.debug("Detalhes do teste")
    logging.info("Iniciando teste")
    print("-------------------------")

    fcfs(FCFS_EXAMPLES.example1)

    print("-------------------------")
    logging.info("Teste concluído com sucesso!")
    print("-------------------------")

