from typing import List

from utils import print_table, Process, print_gantt_chart, GanttChart
from utils.examples import SJF_EXAMPLES
import logging

logging.basicConfig(level=logging.DEBUG)


def sjf(processes: List[Process]) -> None:
    gantt_chart = []
    executed_queue = []
    current_time = 0
    
    logging.info("Iniciando algoritmo SJF")
    
    while processes:
        arrived_processes = list(filter(lambda p: p.arrival_time <= current_time, processes))
        arrived_processes.sort(key=lambda p: p.burst_time)

        if arrived_processes:
            process = arrived_processes[0]
            processes.remove(process)

            current_time = max(current_time, process.arrival_time)
            process.waiting_time = max(0, current_time - process.arrival_time)
            process.turnaround_time = process.burst_time + process.waiting_time
            current_time += process.burst_time
            executed_queue.append(process)
            gantt_chart.append(GanttChart(name=process.name, arrival_time=current_time))

            logging.debug(f"Processo {process.name} executado. Tempo de espera: {process.waiting_time}, Turnaround time: {process.turnaround_time}")
            logging.debug(f"Próximo processo escolhido: {process.name}")
            logging.debug(f"Estado da fila no momento da escolha: {[p.name for p in processes]}")
            logging.debug(f"Logs de Processos concluida")



        else:
            current_time += 1

    print_gantt_chart(gantt_chart)
    print_table(executed_queue)

    logging.info("Algoritmo SJF concluído com sucesso.")

if __name__ == '__main__':
    print("-------------------------")
    logging.debug("Detalhes do teste")
    logging.info("Iniciando teste")
    print("-------------------------")

    sjf(SJF_EXAMPLES.example1)

    print("-------------------------")
    logging.info("Teste concluído com sucesso!")
    print("-------------------------")
