import logging
from typing import List

from utils import print_table, Process, GanttChart, print_gantt_chart
from utils.examples import FCFS_EXAMPLES

logging.basicConfig(level=logging.DEBUG)

def fcfs(processes: List[Process]) -> None:
    logging.debug("Iniciando algoritmo FCFS")
    
    processes.sort(key=lambda p: p.arrival_time)
    current_time = 0
    gantt_chart = []

    for process in processes:
        logging.debug(f"Processo {process.name} chegou em {process.arrival_time} e tem tempo de burst {process.burst_time}")
        process.waiting_time = max(0, current_time - process.arrival_time)
        logging.debug(f"Tempo de espera do Processo {process.name}: {process.waiting_time}")
        process.turnaround_time = process.burst_time + process.waiting_time
        logging.debug(f"Tempo de retorno do Processo {process.name}: {process.turnaround_time}")
        current_time = process.turnaround_time
        gantt_chart.append(GanttChart(name=process.name, arrival_time=current_time))

    logging.debug("Gantt Chart:")
    for process in gantt_chart:
        logging.debug(f"Processo {process.name} chegou em {process.arrival_time}")

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
