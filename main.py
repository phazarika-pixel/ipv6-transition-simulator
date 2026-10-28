
import ipaddress
import time
from dataclasses import dataclass


# ==========================================
# CNIS ASSIGNMENT
# Roll No.: MCAM/033
# IPv4-to-IPv6 Transition Simulator
# ==========================================

IPV4_POOL = [
    "192.0.2.10",
    "192.0.2.11",
    "192.0.2.12",
]

IPV6_CLIENT = "2001:db8:1::10"
IPV4_SERVER = "192.0.2.100"


@dataclass
class SimulationResult:
    method: str
    success: bool
    elapsed_ms: float
    details: str


class DSTMInspiredSimulator:
    def __init__(self):
        self.address_pool = IPV4_POOL.copy()
        self.address_mapping = {}

    def validate_addresses(self):
        client = ipaddress.ip_address(IPV6_CLIENT)
        server = ipaddress.ip_address(IPV4_SERVER)

        print("\nAddress validation")
        print("------------------")
        print(f"IPv6 client: {client} (version {client.version})")
        print(f"IPv4 server: {server} (version {server.version})")
        print("The addresses belong to different IP versions.")

    def allocate_ipv4(self, ipv6_client):
        """Allocate and record a temporary IPv4 address."""

        if ipv6_client in self.address_mapping:
            return self.address_mapping[ipv6_client]

        if not self.address_pool:
            return None

        temporary_ipv4 = self.address_pool.pop(0)
        self.address_mapping[ipv6_client] = temporary_ipv4

        return temporary_ipv4

    def simulate_dual_stack(self):
        """Model a client and network that support both IP versions."""

        start = time.perf_counter()

        # The dual-stack client uses IPv4 to contact
        # the IPv4 server in this simplified model.
        success = (
            ipaddress.ip_address(IPV4_SERVER).version == 4
        )

        elapsed = (time.perf_counter() - start) * 1000

        return SimulationResult(
            method="Dual Stack",
            success=success,
            elapsed_ms=elapsed,
            details=(
                "The client has IPv4 and IPv6 capability "
                "and selects IPv4 for this IPv4 server."
            ),
        )

    def simulate_tunnel(self):
        """Model IPv6 packet encapsulation inside IPv4."""

        start = time.perf_counter()

        inner_packet = (
            f"IPv6 source={IPV6_CLIENT}; "
            f"destination=2001:db8:2::100"
        )

        outer_packet = (
            f"IPv4 tunnel header; payload=({inner_packet})"
        )

        # Simulate the tunnel endpoint removing the outer header.
        decapsulated_packet = inner_packet

        success = decapsulated_packet == inner_packet

        elapsed = (time.perf_counter() - start) * 1000

        return SimulationResult(
            method="Basic Tunneling",
            success=success,
            elapsed_ms=elapsed,
            details=(
                f"Encapsulated packet: {outer_packet}\n"
                "Tunnel endpoint removes the outer IPv4 header."
            ),
        )

    def simulate_dstm(self):
        """Model temporary IPv4 allocation and tunnel delivery."""

        start = time.perf_counter()

        temporary_ipv4 = self.allocate_ipv4(IPV6_CLIENT)

        if temporary_ipv4 is None:
            elapsed = (time.perf_counter() - start) * 1000

            return SimulationResult(
                method="DSTM-Inspired",
                success=False,
                elapsed_ms=elapsed,
                details="No temporary IPv4 addresses remain.",
            )

        inner_packet = (
            f"IPv6 source={IPV6_CLIENT}; "
            f"destination=IPv4 service {IPV4_SERVER}"
        )

        outer_packet = (
            f"IPv4 source={temporary_ipv4}; "
            f"destination=tunnel endpoint; "
            f"payload=({inner_packet})"
        )

        # Simulate receiving the packet and removing
        # the outer tunnel header.
        decapsulated_packet = inner_packet

        success = (
            decapsulated_packet == inner_packet
            and IPV6_CLIENT in self.address_mapping
        )

        elapsed = (time.perf_counter() - start) * 1000

        return SimulationResult(
            method="DSTM-Inspired",
            success=success,
            elapsed_ms=elapsed,
            details=(
                f"Allocated temporary IPv4: {temporary_ipv4}\n"
                f"Mapping: {IPV6_CLIENT} -> {temporary_ipv4}\n"
                f"Simulated tunnel packet: {outer_packet}\n"
                "Tunnel endpoint removes the outer header."
            ),
        )

    def show_results(self, result):
        print("\n" + "=" * 55)
        print(f"Method: {result.method}")
        print("=" * 55)
        print(f"Delivery successful: {'Yes' if result.success else 'No'}")
        print(f"Simulated processing time: {result.elapsed_ms:.6f} ms")
        print(f"Details: {result.details}")

    def show_mappings(self):
        print("\nIPv6-to-temporary-IPv4 mapping table")
        print("-" * 45)

        if not self.address_mapping:
            print("No addresses have been allocated yet.")
            return

        for ipv6, ipv4 in self.address_mapping.items():
            print(f"{ipv6}  -->  {ipv4}")

    def show_pool(self):
        print("\nTemporary IPv4 address pool")
        print("-" * 35)
        print(f"Available addresses: {len(self.address_pool)}")

        if self.address_pool:
            for address in self.address_pool:
                print(f"  {address}")
        else:
            print("  Pool exhausted.")

    def run(self):
        while True:
            print("\n" + "=" * 55)
            print("CNIS: IPv4-to-IPv6 Transition Simulator")
            print("Roll No.: MCAM/033")
            print("=" * 55)
            print("1. Validate IPv4 and IPv6 addresses")
            print("2. Simulate Dual Stack")
            print("3. Simulate Basic Tunneling")
            print("4. Simulate DSTM-Inspired Transition")
            print("5. View Address Mapping Table")
            print("6. View Available IPv4 Pool")
            print("7. Exit")

            choice = input("\nEnter your choice (1-7): ").strip()

            if choice == "1":
                self.validate_addresses()

            elif choice == "2":
                self.show_results(self.simulate_dual_stack())

            elif choice == "3":
                self.show_results(self.simulate_tunnel())

            elif choice == "4":
                self.show_results(self.simulate_dstm())

            elif choice == "5":
                self.show_mappings()

            elif choice == "6":
                self.show_pool()

            elif choice == "7":
                print("\nSimulation ended. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    simulator = DSTMInspiredSimulator()
    simulator.run()
