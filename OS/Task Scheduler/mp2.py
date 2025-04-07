import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

# ---------------------------
# Process Dataset
# ---------------------------
processes = [
    {"pid": 1, "burst": 20, "priority": 0},
    {"pid": 2, "burst": 15, "priority": 0},
    {"pid": 3, "burst": 11, "priority": 1},
    {"pid": 4, "burst": 9,  "priority": 1},
    {"pid": 5, "burst": 11, "priority": 2},
    {"pid": 6, "burst": 9,  "priority": 3},
    {"pid": 7, "burst": 12, "priority": 2},
    {"pid": 8, "burst": 14, "priority": 4},
    {"pid": 9, "burst": 15, "priority": 3},
    {"pid":10, "burst": 19, "priority": 2},
    {"pid":11, "burst": 25, "priority": 0},
    {"pid":12, "burst": 21, "priority": 1},
    {"pid":13, "burst": 8,  "priority": 2},
    {"pid":14, "burst": 3,  "priority": 5},
    {"pid":15, "burst": 4,  "priority": 5},
    {"pid":16, "burst": 14, "priority": 4},
    {"pid":17, "burst": 12, "priority": 4},
    {"pid":18, "burst": 10, "priority": 2},
    {"pid":19, "burst": 10, "priority": 3},
    {"pid":20, "burst": 9,  "priority": 2}
]

TIME_QUANTUM = 3

# ---------------------------
# Gantt Chart Drawer
# ---------------------------
def draw_gantt_chart(gantt_data, title):
    fig, ax = plt.subplots(figsize=(14, 3))
    colors = plt.cm.tab20.colors
    color_map = {}
    current_color = 0

    for i, block in enumerate(gantt_data):
        pid = block['pid']
        start = block['start']
        burst = block['burst']
        if pid not in color_map:
            color_map[pid] = colors[current_color % len(colors)]
            current_color += 1
        ax.broken_barh([(start, burst)], (10, 9), facecolors=color_map[pid], edgecolor='black')
        ax.text(start + burst / 2, 14.5, f"P{pid}", ha='center', va='center', fontweight='bold')

    total_time = gantt_data[-1]['start'] + gantt_data[-1]['burst']
    ax.set_ylim(5, 25)
    ax.set_xlim(0, total_time)
    ax.set_xlabel("Time")
    ax.set_yticks([])
    ax.set_title(f"Gantt Chart for {title} Scheduling", fontweight='bold')
    ax.set_xticks(range(0, total_time + 1, 3))
    ax.grid(axis='x')
    plt.tight_layout()
    plt.show()

# ---------------------------
# Base Non-Preemptive Scheduler
# ---------------------------
class NonPreemptiveScheduler(ABC):
    def __init__(self, processes):
        for p in processes:
            p.setdefault('arrival', 0)
        self.processes = [p.copy() for p in processes]
        self.results = []
        self.gantt = []

    @abstractmethod
    def sort_processes(self):
        pass

    def schedule(self):
        self.sort_processes()
        time = 0
        for p in self.processes:
            if time < p['arrival']:
                time = p['arrival']
            self.gantt.append({'pid': p['pid'], 'start': time, 'burst': p['burst']})
            waiting_time = time - p['arrival']
            turnaround_time = waiting_time + p['burst']
            self.results.append({
                'pid': p['pid'],
                'waiting_time': waiting_time,
                'turnaround_time': turnaround_time,
                'burst': p['burst']
            })
            time += p['burst']

    def print_metrics(self, title):
        print(f"\n--- {title} Scheduling ---")
        print(f"{'PID':<5}{'Waiting Time':<15}{'Turnaround Time':<20}")
        total_wt = total_tat = 0
        for r in self.results:
            print(f"{r['pid']:<5}{r['waiting_time']:<15}{r['turnaround_time']:<20}")
            total_wt += r['waiting_time']
            total_tat += r['turnaround_time']
        print(f"\nAverage Waiting Time: {total_wt / len(self.results):.2f} ms")
        print(f"Average Turnaround Time: {total_tat / len(self.results):.2f} ms")
        draw_gantt_chart(self.gantt, title)

class FCFS_Scheduler(NonPreemptiveScheduler):
    def sort_processes(self):
        pass

class SJF_Scheduler(NonPreemptiveScheduler):
    def sort_processes(self):
        self.processes.sort(key=lambda p: (p['arrival'], p['burst']))

    def schedule(self):
        processes = sorted(self.processes, key=lambda p: p['arrival'])
        ready_queue = []
        time = 0
        scheduled = set()

        while len(scheduled) < len(processes):
            # Add newly arrived processes to the ready queue
            for p in processes:
                if p['pid'] not in scheduled and p['arrival'] <= time and p not in ready_queue:
                    ready_queue.append(p)

            if not ready_queue:
                # Fast forward to the next arrival time if CPU is idle
                time = min(p['arrival'] for p in processes if p['pid'] not in scheduled)
                continue

            # Choose the shortest job among ready processes
            ready_queue.sort(key=lambda p: p['burst'])
            current = ready_queue.pop(0)

            self.gantt.append({'pid': current['pid'], 'start': time, 'burst': current['burst']})
            waiting_time = time - current['arrival']
            turnaround_time = waiting_time + current['burst']
            self.results.append({
                'pid': current['pid'],
                'waiting_time': waiting_time,
                'turnaround_time': turnaround_time,
                'burst': current['burst']
            })

            time += current['burst']
            scheduled.add(current['pid'])


class Priority_Scheduler(NonPreemptiveScheduler):
    def sort_processes(self):
        self.processes.sort(key=lambda p: (p['priority']))

# ---------------------------
# SRPT Scheduler (Preemptive SJF)
# ---------------------------
def srpt_scheduler(processes):
    time = 0
    complete = 0
    n = len(processes)
    remaining = [p['burst'] for p in processes]
    wt = [0] * n
    tat = [0] * n
    gantt = []
    last_pid = -1

    while complete < n:
        idx = -1
        min_burst = float('inf')
        for i in range(n):
            if processes[i]['arrival'] <= time and remaining[i] > 0 and remaining[i] < min_burst:
                min_burst = remaining[i]
                idx = i

        if idx == -1:
            time += 1
            continue

        if last_pid != processes[idx]['pid']:
            gantt.append({'pid': processes[idx]['pid'], 'start': time})
            last_pid = processes[idx]['pid']

        remaining[idx] -= 1
        time += 1

        if remaining[idx] == 0:
            complete += 1
            finish_time = time
            tat[idx] = finish_time - processes[idx]['arrival']
            wt[idx] = tat[idx] - processes[idx]['burst']

    # Finalize burst times for Gantt
    gantt_blocks = []
    for i in range(len(gantt)):
        start = gantt[i]['start']
        end = gantt[i+1]['start'] if i + 1 < len(gantt) else time
        gantt_blocks.append({'pid': gantt[i]['pid'], 'start': start, 'burst': end - start})

    print("\n--- SRPT Scheduling ---")
    print(f"{'PID':<5}{'Waiting Time':<15}{'Turnaround Time':<20}")
    total_wt = total_tat = 0
    for i in range(n):
        print(f"{processes[i]['pid']:<5}{wt[i]:<15}{tat[i]:<20}")
        total_wt += wt[i]
        total_tat += tat[i]
    print(f"\nAverage Waiting Time: {total_wt / n:.2f} ms")
    print(f"Average Turnaround Time: {total_tat / n:.2f} ms")
    draw_gantt_chart(gantt_blocks, "SRPT")

# ---------------------------
# Round Robin Scheduler
# ---------------------------
def round_robin_scheduler(processes, quantum=TIME_QUANTUM):
    time = 0
    queue = []
    remaining = {p['pid']: p['burst'] for p in processes}
    arrival_dict = {p['pid']: p['arrival'] for p in processes}
    process_dict = {p['pid']: p for p in processes}
    completed = {}
    gantt = []
    n = len(processes)

    processes.sort(key=lambda x: x['arrival'])
    i = 0

    while len(completed) < n:
        while i < len(processes) and processes[i]['arrival'] <= time:
            queue.append(processes[i]['pid'])
            i += 1

        if not queue:
            time += 1
            continue

        current = queue.pop(0)
        start = time
        exec_time = min(quantum, remaining[current])
        remaining[current] -= exec_time
        time += exec_time
        gantt.append({'pid': current, 'start': start, 'burst': exec_time})

        while i < len(processes) and processes[i]['arrival'] <= time:
            queue.append(processes[i]['pid'])
            i += 1

        if remaining[current] > 0:
            queue.append(current)
        else:
            completed[current] = time

    print("\n--- Round Robin Scheduling ---")
    print(f"{'PID':<5}{'Waiting Time':<15}{'Turnaround Time':<20}")
    total_wt = total_tat = 0
    for p in processes:
        tat = completed[p['pid']] - p['arrival']
        wt = tat - p['burst']
        print(f"{p['pid']:<5}{wt:<15}{tat:<20}")
        total_wt += wt
        total_tat += tat
    print(f"\nAverage Waiting Time: {total_wt / n:.2f} ms")
    print(f"Average Turnaround Time: {total_tat / n:.2f} ms")
    draw_gantt_chart(gantt, "Round Robin")

# ---------------------------
# Runner Function
# ---------------------------
def run_all_schedulers():
    fcfs = FCFS_Scheduler(processes)
    fcfs.schedule()
    fcfs.print_metrics("FCFS")

    sjf = SJF_Scheduler(processes)
    sjf.schedule()
    sjf.print_metrics("SJF")

    priority = Priority_Scheduler(processes)
    priority.schedule()
    priority.print_metrics("Priority")

    srpt_scheduler([p.copy() for p in processes])
    round_robin_scheduler([p.copy() for p in processes], quantum=TIME_QUANTUM)


# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    run_all_schedulers()
