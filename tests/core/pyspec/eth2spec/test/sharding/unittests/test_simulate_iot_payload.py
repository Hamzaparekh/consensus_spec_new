import time
import psutil
import os
import random
import csv
import hashlib

from eth2spec.test.context import with_phases, spec_state_test
from eth2spec.test.helpers.constants import DENEB
from eth2spec.test.helpers.block import build_empty_block
from eth2spec.utils import bls

# --- Disable BLS signature verification ---
bls.Verify = lambda *args, **kwargs: True

# --- Output directory ---
output_dir = "/Users/hamzaparekh/Library/CloudStorage/OneDrive-UTS/Documents/University Work/Honours/Honours Experimentation"
os.makedirs(output_dir, exist_ok=True)

proc = psutil.Process(os.getpid())

# --- User Parameters ---
payloads_per_iteration = 5              # Change to 1, 10, etc.
processing_type = "sha256"              # Options: "xor" or "sha256"
iterations_per_size = 5
payload_sizes = [128, 512, 1024]        # You can expand this

@with_phases([DENEB])
@spec_state_test
def test_spec_block_simulation(spec, state):
    print("\n🧪 Running configurable Ethereum sharding simulation with real spec processing")

    # --- CSV file name reflects parameters ---
    csv_filename = f"spec_benchmark_{payloads_per_iteration}payloads_{processing_type}.csv"
    log_path = os.path.join(output_dir, csv_filename)

    with open(log_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Iteration", "PayloadSize", "NumPayloads", "Latency(s)", "CPU(%)", "Memory(MB)"])

        for payload_size in payload_sizes:
            print(f"\n🔵 Payload Size: {payload_size} bytes")

            for i in range(1, iterations_per_size + 1):
                payloads = []
                for _ in range(payloads_per_iteration):
                    payload = bytes([random.randint(0, 255) for _ in range(payload_size)])
                    if processing_type == "sha256":
                        _ = hashlib.sha256(payload).digest()
                    elif processing_type == "xor":
                        _ = [b ^ 0x55 for b in payload]
                    else:
                        raise ValueError("Invalid processing_type")

                    payloads.append(payload)

                # --- Prepare block and advance slot ---
                block = build_empty_block(spec, state, slot=state.slot + 1)
                spec.process_slots(state, block.slot)

                # --- Insert mock BLS and blobs ---
                block.body.randao_reveal = spec.BLSSignature(b'\x11' * 96)
                dummy_commitment = spec.KZGCommitment(b'\x00' * 48)
                block.body.blob_kzg_commitments = [dummy_commitment] * payloads_per_iteration

                # --- Measure performance ---
                mem_before = proc.memory_info().rss / 1024**2
                start_time = time.time()
                spec.process_block(state, block)
                elapsed = time.time() - start_time
                mem_after = proc.memory_info().rss / 1024**2
                cpu = proc.cpu_percent(interval=0.05)

                print(f"#{i:02} | {payload_size}B | {payloads_per_iteration} payloads | {processing_type} | Time: {elapsed:.6f}s | CPU: {cpu:.2f}% | Mem: {mem_after:.2f}MB")
                writer.writerow([i, payload_size, payloads_per_iteration, elapsed, cpu, mem_after])

    print(f"\n✅ Done! Results logged to: {log_path}")
