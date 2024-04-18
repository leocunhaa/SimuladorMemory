import logging
from typing import List

from utils import print_table, Process, print_gantt_chart, GanttChart
from utils.examples import PRIORITY_EXAMPLES

logging.basicConfig(level=logging.DEBUG)


def priority(processes: List[Process]) -> None:

    gantt_chart = []
    executed_queue = []
    current_time = 0
    while processes:
        arrived_processes = list(filter(lambda p: p.arrival_time <= current_time, processes))
        arrived_processes.sort(key=lambda p: p.priority)

        process = arrived_processes[0]
        processes.remove(process)
        
        current_time = max(current_time, process.arrival_time)
        process.waiting_time = max(0, current_time - process.arrival_time)
        process.turnaround_time = process.burst_time + process.waiting_time
        current_time += process.burst_time
        executed_queue.append(process)
        gantt_chart.append(GanttChart(name=process.name, arrival_time=current_time))

    print_gantt_chart(gantt_chart)
    print_table(executed_queue, show_priority=True)


if __name__ == '__main__':

    print("-------------------------")
    logging.debug("Detalhes do teste")
    logging.info("Iniciando teste")
    print("-------------------------")
    
    priority(PRIORITY_EXAMPLES.example2)

    print("-------------------------")
    logging.info("Teste concluido com sucesso!")
    print("-------------------------")



