
import csv
import time
import ipaddress
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = PROJECT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

CLIENT_COUNT = 5

IPV4_POOL = [
    "192.0.2.10",
    "192.0.2.11",
    "192.0.2.12",
]

IPV4_SERVER = "192.0.2.100"


def generate_clients(count):
    return [f"2001:db8:1::{i:x}" for i in range(1, count + 1)]


def simulate_dual_stack(client):
    # Simplified model: the client can use IPv4 to reach
    # an IPv4 server because it supports both IP versions.
    start = time.perf_counter()

    success = ipaddress.ip_address(IPV4_SERVER).version == 4

    elapsed = (time.perf_counter() - start) * 1000
    return success, elapsed, "No temporary IPv4 allocation"


def simulate_tunneling(client):
    # Simplified model: an IPv6 packet is represented as
    # an inner payload inside an outer IPv4 packet.
    start = time.perf_counter()

    inner_packet = f"IPv6:{client}->2001:db8:2::100"
    outer_packet = f"IPv4 tunnel payload=({inner_packet})"
    recovered_packet = outer_packet.split("payload=(", 1)[1][:-1]

    success = recovered_packet == inner_packet

    elapsed = (time.perf_counter() - start) * 1000
    return success, elapsed, "Simulated encapsulation and decapsulation"


def simulate_dstm(client, pool, mappings):
    # Temporary IPv4 address allocation and mapping.
    start = time.perf_counter()

    if client in mappings:
        address = mappings[client]
        success = True
    elif pool:
        address = pool.pop(0)
        mappings[client] = address
        success = True
    else:
        address = None
        success = False

    elapsed = (time.perf_counter() - start) * 1000

    if success:
        details = f"Temporary IPv4 allocated: {address}"
    else:
        details = "Address pool exhausted"

    return success, elapsed, details


def main():
    clients = generate_clients(CLIENT_COUNT)
    pool = IPV4_POOL.copy()
    mappings = {}
    rows = []

    methods = [
        ("Dual Stack", simulate_dual_stack),
        ("Basic Tunneling", simulate_tunneling),
    ]

    for method, function in methods:
        for client in clients:
            success, elapsed, details = function(client)

            rows.append({
                "method": method,
                "client_ipv6": client,
                "success": success,
                "processing_time_ms": round(elapsed, 6),
                "details": details,
            })

    for client in clients:
        success, elapsed, details = simulate_dstm(
            client, pool, mappings
        )

        rows.append({
            "method": "DSTM-Inspired",
            "client_ipv6": client,
            "success": success,
            "processing_time_ms": round(elapsed, 6),
            "details": details,
        })

    output = RESULTS_DIR / "comparison_results.csv"

    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("\nCNIS Transition Comparison")
    print("=" * 65)
    print(f"Clients tested per method: {CLIENT_COUNT}\n")

    print(
        f"{'Method':<20} {'Success':>8} "
        f"{'Failed':>8} {'Success rate':>14}"
    )
    print("-" * 55)

    for method in ["Dual Stack", "Basic Tunneling", "DSTM-Inspired"]:
        method_rows = [r for r in rows if r["method"] == method]
        successes = sum(r["success"] for r in method_rows)
        failures = len(method_rows) - successes
        rate = successes / len(method_rows) * 100

        print(
            f"{method:<20} {successes:>8} "
            f"{failures:>8} {rate:>13.1f}%"
        )

    print(f"\nCSV saved to: {output}")


if __name__ == "__main__":
    main()
