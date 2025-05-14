import os
import csv
import matplotlib.pyplot as plt
from collections import defaultdict

# --- Path to your benchmark CSV ---
benchmark_dir = "/Users/hamzaparekh/Library/CloudStorage/OneDrive-UTS/Documents/University Work/Honours/Honours Experimentation"
csv_filename = "iot_spec_benchmark_with_blobs.csv"
filepath = os.path.join(benchmark_dir, csv_filename)

# --- Check if file exists ---
if not os.path.exists(filepath):
    raise FileNotFoundError(f"CSV not found: {filepath}")

print(f"📊 Plotting results from: {filepath}")

# --- Read the CSV and group by payload size ---
results = defaultdict(list)

with open(filepath, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        size = int(row["PayloadSize"])
        results[size].append({
            "latency": float(row["Latency(s)"]),
            "cpu": float(row["CPU(%)"]),
            "mem": float(row["Memory(MB)"])
        })

# --- Compute averages ---
sizes = sorted(results.keys())
avg_latency = [sum(x["latency"] for x in results[s]) / len(results[s]) for s in sizes]
avg_cpu = [sum(x["cpu"] for x in results[s]) / len(results[s]) for s in sizes]
avg_mem = [sum(x["mem"] for x in results[s]) / len(results[s]) for s in sizes]

# --- Plotting ---
plt.figure(figsize=(14, 6))

plt.subplot(1, 3, 1)
plt.plot(sizes, avg_latency, marker="o", color="blue")
plt.title("Latency vs Payload Size")
plt.xlabel("Payload Size (bytes)")
plt.ylabel("Latency (s)")

plt.subplot(1, 3, 2)
plt.plot(sizes, avg_cpu, marker="s", color="orange")
plt.title("CPU Usage vs Payload Size")
plt.xlabel("Payload Size (bytes)")
plt.ylabel("CPU (%)")

plt.subplot(1, 3, 3)
plt.plot(sizes, avg_mem, marker="^", color="green")
plt.title("Memory Usage vs Payload Size")
plt.xlabel("Payload Size (bytes)")
plt.ylabel("Memory (MB)")

plt.suptitle("Spec Benchmark with Mock Blobs")
plt.tight_layout()
plt.show()
