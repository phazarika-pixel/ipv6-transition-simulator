
import csv
import ipaddress
import time
from pathlib import Path


# CNIS assignment: MCAM/033
# Repeatable experiment for a DSTM-inspired model.
# This is a software simulation, not a real network tunnel.

PROJECT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = PROJECT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

ADDRESS_POOL = [
    "192.0.2.10",
    "192.0.2.11",
    "192.0.2.12",
]

IPV4_SERVER = "192.0.2.100"


def make_ipv6_client(number):
    return f"2001:db8:1::{number:x}"


def run_experiment():
    pool = ADDRESS_POOL.copy()
    mappings = {}
    results = []

    clients = [make_ipv6_client(i) for i in range(1, 6)]

    for client in clients:
        start = time.perf_counter()

        # Validate addresses before simulating allocation.
        ipaddress.IPv6Address(client)
        ipaddress.IPv4Address(IPV4_SERVER)

        if pool:
            temporary_ipv4 = pool.pop(0)
            mappings[client] = temporary_ipv4
            success = True
            details = "Temporary IPv4 allocated"
        else:
            temporary_ipv4 = ""
            success = False
            details = "Address pool exhausted"

        elapsed_ms = (time.perf_counter() - start) * 1000

        results.append({
            "roll_no": "MCAM/033",
            "client_ipv6": client,
            "server_ipv4": IPV4_SERVER,
            "temporary_ipv4": temporary_ipv4,
            "success": success,
            "processing_time_ms": round(elapsed_ms, 6),
            "details": details,
        })

    output_file = RESULTS_DIR / "experiment_results.csv"

    with output_file.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )
        writer.writeheader()
        writer.writerows(results)

    print("\nDSTM-inspired allocation experiment")
    print("-" * 65)
    print(f"Clients tested: {len(clients)}")
    print(f"Successful allocations: {sum(r['success'] for r in results)}")
    print(f"Failed allocations: {sum(not r['success'] for r in results)}")
    print(f"Addresses remaining: {len(pool)}")
    print("\nClient allocation results:")

    for result in results:
        status = "SUCCESS" if result["success"] else "FAILED"
        address = result["temporary_ipv4"] or "None"
        print(
            f"{result['client_ipv6']} -> {address} | "
            f"{status} | {result['details']}"
        )

    print(f"\nCSV saved to: {output_file}")

    print("\nMapping table")
    print("-" * 45)

    for ipv6, ipv4 in mappings.items():
        print(f"{ipv6} -> {ipv4}")


if __name__ == "__main__":
    run_experiment()
