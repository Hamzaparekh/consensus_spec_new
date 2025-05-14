import pandas as pd
import matplotlib.pyplot as plt
import os

# ---- Define output directory ----
output_dir = "/Users/hamzaparekh/Library/CloudStorage/OneDrive-UTS/Documents/University Work/Honours/Honours Experimentation"

# File to load
csv_file = os.path.join(output_dir, "iot_benchmark_combined.csv")

# Check file exists
if not os.path.exists(csv_file):
    print(f"⚠️ File {csv_file} not found. Exiting.")
    exit()

# Load data
df = pd.read_csv(csv_file)

# Get unique payload sizes
payload_sizes = sorted(df["PayloadSize"].unique())

# ---- Calculate Averages and Standard Deviation ----
avg_latency = df.groupby("PayloadSize")["Latency(s)"].mean()
std_latency = df.groupby("PayloadSize")["Latency(s)"].std()

avg_cpu = df.groupby("PayloadSize")["CPU(%)"].mean()
std_cpu = df.groupby("PayloadSize")["CPU(%)"].std()

avg_memory = df.groupby("PayloadSize")["Memory(MB)"].mean()
std_memory = df.groupby("PayloadSize")["Memory(MB)"].std()

# ---- Plot Average Latency (with error bars) ----
plt.figure(figsize=(8,6))
plt.errorbar(payload_sizes, avg_latency, yerr=std_latency, fmt='o-', capsize=5)
plt.title("Average Latency vs Payload Size (with Std Dev)")
plt.xlabel("Payload Size (bytes)")
plt.ylabel("Latency (seconds)")
plt.grid(True)
plt.savefig(os.path.join(output_dir, "latency_vs_payload_size.png"))
plt.show()

# ---- Plot Average CPU (with error bars) ----
plt.figure(figsize=(8,6))
plt.errorbar(payload_sizes, avg_cpu, yerr=std_cpu, fmt='o-', capsize=5, color='orange')
plt.title("Average CPU Usage vs Payload Size (with Std Dev)")
plt.xlabel("Payload Size (bytes)")
plt.ylabel("CPU Usage (%)")
plt.grid(True)
plt.savefig(os.path.join(output_dir, "cpu_vs_payload_size.png"))
plt.show()

# ---- Plot Average Memory (with error bars) ----
plt.figure(figsize=(8,6))
plt.errorbar(payload_sizes, avg_memory, yerr=std_memory, fmt='o-', capsize=5, color='green')
plt.title("Average Memory Usage vs Payload Size (with Std Dev)")
plt.xlabel("Payload Size (bytes)")
plt.ylabel("Memory Usage (MB)")
plt.grid(True)
plt.savefig(os.path.join(output_dir, "memory_vs_payload_size.png"))
plt.show()

# ---- Scatter Plot Latency ----
plt.figure(figsize=(10,6))
for size in payload_sizes:
    subset = df[df["PayloadSize"] == size]
    plt.scatter([size]*len(subset), subset["Latency(s)"], alpha=0.6)
plt.title("Latency Scatter Plot by Payload Size")
plt.xlabel("Payload Size (bytes)")
plt.ylabel("Latency (seconds)")
plt.grid(True)
plt.savefig(os.path.join(output_dir, "scatter_latency_vs_payload_size.png"))
plt.show()

# ---- Scatter Plot CPU ----
plt.figure(figsize=(10,6))
for size in payload_sizes:
    subset = df[df["PayloadSize"] == size]
    plt.scatter([size]*len(subset), subset["CPU(%)"], alpha=0.6)
plt.title("CPU Usage Scatter Plot by Payload Size")
plt.xlabel("Payload Size (bytes)")
plt.ylabel("CPU Usage (%)")
plt.grid(True)
plt.savefig(os.path.join(output_dir, "scatter_cpu_vs_payload_size.png"))
plt.show()

# ---- Scatter Plot Memory ----
plt.figure(figsize=(10,6))
for size in payload_sizes:
    subset = df[df["PayloadSize"] == size]
    plt.scatter([size]*len(subset), subset["Memory(MB)"], alpha=0.6)
plt.title("Memory Usage Scatter Plot by Payload Size")
plt.xlabel("Payload Size (bytes)")
plt.ylabel("Memory Usage (MB)")
plt.grid(True)
plt.savefig(os.path.join(output_dir, "scatter_memory_vs_payload_size.png"))
plt.show()

print("\n✅ All plots generated and saved inside:", output_dir)
