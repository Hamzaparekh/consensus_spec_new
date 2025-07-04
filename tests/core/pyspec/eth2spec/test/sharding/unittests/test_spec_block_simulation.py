import time
import psutil
import os
import random
import csv

from eth2spec.test.context import with_phases, spec_state_test
from eth2spec.test.helpers.constants import DENEB
from eth2spec.test.helpers.block import build_empty_block
from eth2spec.utils import bls


bls.Verify = lambda *args, **kwargs: True


output_dir = "/Users/hamzaparekh/Projects/Results"
os.makedirs(output_dir, exist_ok=True)

proc = psutil.Process(os.getpid())

@with_phases([DENEB])
@spec_state_test
def test_spec_block_simulation(spec, state):
    print("\n🧪 Running realistic spec.process_block simulation with mock blob data")

    iterations_per_size = 50
    payload_sizes = [64, 128, 256, 512, 1024, 2048, 4096, 8192]  #blob data sizes
    payloads_per_iteration = 5  # Number of transactions per block

    log_path = os.path.join(output_dir, f"ethereum_results_{payloads_per_iteration}tx.csv")
    with open(log_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Iteration", "PayloadSize", "NumPayloads", "Latency(s)", "CPU(%)", "Memory(MB)"])

        for payload_size in payload_sizes:
            print(f"\n🔵 Payload size: {payload_size} bytes, {payloads_per_iteration} payloads per block")

            for i in range(1, iterations_per_size + 1):
               
                payloads = []
                for _ in range(payloads_per_iteration):
                    payload = bytes([random.randint(0, 255) for _ in range(payload_size)])
                    
                    payloads.append(payload)

               
                block = build_empty_block(spec, state, slot=state.slot + 1)
                spec.process_slots(state, block.slot)

                
                block.body.randao_reveal = spec.BLSSignature(b'\x11' * 96)

                
                dummy_commitment = spec.KZGCommitment(b'\x00' * 48)
                block.body.blob_kzg_commitments = [dummy_commitment] * payloads_per_iteration

               
                mem_before = proc.memory_info().rss / 1024**2
                start_time = time.time()

                
                spec.process_block(state, block)

                elapsed = time.time() - start_time
                mem_after = proc.memory_info().rss / 1024**2
                cpu = proc.cpu_percent(interval=0.05)

                print(f"#{i:02} | {payload_size}B × {payloads_per_iteration} | "
                      f"Time: {elapsed:.6f}s | CPU: {cpu:.2f}% | Mem: {mem_after:.2f}MB")
                writer.writerow([i, payload_size, payloads_per_iteration, elapsed, cpu, mem_after])

    print(f"\n✅ Complete! Logged results to: {log_path}")
