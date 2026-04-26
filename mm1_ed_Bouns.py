import random

LAMBDA = 6 / 60.0
MU = 8 / 60.0
N_CUSTOMERS = 500
N_RUNS = 500
SEED = 585

random.seed(SEED)

avg_wait_runs = []
avg_sys_runs = []
util_runs = []

for r in range(N_RUNS):
    inter_arrivals = []
    service_times = []
    arrival_times = []
    service_start_times = []
    departure_times = []
    waiting_times = []
    system_times = []

    time_arr = 0.0
    for i in range(N_CUSTOMERS):
        ia = random.expovariate(LAMBDA)
        st = random.expovariate(MU)
        inter_arrivals.append(ia)
        service_times.append(st)
        time_arr += ia
        arrival_times.append(time_arr)

    service_start_times.append(arrival_times[0])
    departure_times.append(service_start_times[0] + service_times[0])
    waiting_times.append(service_start_times[0] - arrival_times[0])
    system_times.append(departure_times[0] - arrival_times[0])

    for i in range(1, N_CUSTOMERS):
        ss = max(arrival_times[i], departure_times[i-1])
        service_start_times.append(ss)
        dep = ss + service_times[i]
        departure_times.append(dep)
        w = ss - arrival_times[i]
        s = dep - arrival_times[i]
        waiting_times.append(w)
        system_times.append(s)

    n = N_CUSTOMERS
    avg_w = sum(waiting_times) / n
    avg_s = sum(system_times) / n
    busy_time = sum(service_times)
    total_time = departure_times[-1]
    util = busy_time / total_time

    avg_wait_runs.append(avg_w)
    avg_sys_runs.append(avg_s)
    util_runs.append(util)

overall_avg_wait = sum(avg_wait_runs) / N_RUNS
overall_avg_sys = sum(avg_sys_runs) / N_RUNS
overall_avg_util = sum(util_runs) / N_RUNS

rho = LAMBDA / MU

if rho < 1.0:
    W_theory = 1.0 / (MU - LAMBDA)
    Wq_theory = rho / (MU - LAMBDA)
else:
    W_theory = float('inf')
    Wq_theory = float('inf')

print("M/M/1 Hospital ED Queue Simulation")
print("----------------------------------")
print(f"Arrival rate (lambda): {LAMBDA:.4f} patients/min")
print(f"Service rate (mu):     {MU:.4f} patients/min")
print(f"Traffic intensity rho: {rho:.4f}")
print(f"Patients per run:      {N_CUSTOMERS}")
print(f"Number of runs:        {N_RUNS}")
print()

print("Sample of generated data for run 1 (first 10 patients):")
print("ID  ArrTime  ServStart  Depart   Wait     SysTime")
for i in range(10):
    print(f"{i:3d}  {arrival_times[i]:7.3f}  {service_start_times[i]:9.3f}  "
          f"{departure_times[i]:7.3f}  {waiting_times[i]:7.3f}  {system_times[i]:7.3f}")

print()
print("First 5 runs: average Wq, W, utilization")
print("Run  Avg_Wq  Avg_W   Util")
for r in range(5):
    print(f"{r+1:3d}  {avg_wait_runs[r]:7.3f}  {avg_sys_runs[r]:7.3f}  {util_runs[r]:6.3f}")

print()
print("Overall averages across all runs:")
print(f"Average of run Wq (overall): {overall_avg_wait:.3f} minutes")
print(f"Average of run W  (overall): {overall_avg_sys:.3f} minutes")
print(f"Average of run utilization:  {overall_avg_util:.3f}")

print()
print("Theoretical M/M/1 performance:")
print(f"Wq_theory (avg waiting in queue): {Wq_theory:.3f} minutes")
print(f"W_theory  (avg time in system):   {W_theory:.3f} minutes")
