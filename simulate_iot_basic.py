import time
import psutil
import os
import random

# Use psutil to monitor the current process
proc = psutil.Process(os.getpid())

def simulate_iot_payload(payload_size=128, fake_work=False):
    print("\n🟢 Starting IoT payload simulation")

    # Step 1: Create dummy payload (like from an IoT sensor)
    payload = bytes([random.randint(0, 255) for _ in range(payload_size)])
    print(f"📦 Payload size: {len(payload)} bytes")

    # Step 2: Track memory before processing
    initial_mem = proc.memory_info().rss / 1024**2
    print(f"🧠 Initial memory: {initial_mem:.2f} MB")

    # Step 3: Simulate processing
    start_time = time.time()

    if fake_work:
        # Do real CPU work (simulate encoding/hashing)
        [x ** 2 for x in range(10000)]
    else:
        # Just simulate delay
        time.sleep(0.2)

    end_time = time.time()
    elapsed = end_time - start_time
    print(f"⏱️ Processing time: {elapsed:.4f} seconds")

    # Step 4: Track memory and CPU after
    cpu = proc.cpu_percent(interval=0.1)
    mem = proc.memory_info().rss / 1024**2
    print(f"⚙️ CPU usage: {cpu:.2f}%")
    print(f"🧠 Final memory: {mem:.2f} MB")

if __name__ == "__main__":
    simulate_iot_payload()
