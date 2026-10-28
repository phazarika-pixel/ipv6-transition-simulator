
import ipaddress
import time
from pathlib import Path

import pandas as pd
import streamlit as st


# =========================================================
# CNIS MINI PROJECT | MCAM/033
# IPv4-to-IPv6 Transition Simulator
# Educational DSTM-inspired simulation
# =========================================================

PROJECT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = PROJECT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

IPV4_POOL = [
    "192.0.2.10",
    "192.0.2.11",
    "192.0.2.12",
]

IPV4_SERVER = "192.0.2.100"
IPV6_SERVER = "2001:db8:2::100"


# -------------------- PAGE CONFIGURATION --------------------

st.set_page_config(
    page_title="CNIS | IPv4-IPv6 Transition",
    layout="wide",
)

st.title("IPv4-to-IPv6 Transition Simulator")
st.caption(
    "Computer Networks and Information Security | "
    "MCA Semester III | Roll No. MCAM/033"
)




# -------------------- SIMULATION FUNCTIONS --------------------

def simulate_dual_stack(client):
    start = time.perf_counter()

    client_address = ipaddress.IPv6Address(client)
    server_address = ipaddress.IPv4Address(IPV4_SERVER)

    # Assumption: a dual-stack client can also use IPv4,
    # and has a usable IPv4 configuration.
    success = (
        client_address.version == 6
        and server_address.version == 4
    )

    elapsed_ms = (time.perf_counter() - start) * 1000

    return {
        "Method": "Dual Stack",
        "Client IPv6": client,
        "Temporary IPv4": "Not required",
        "Success": success,
        "Processing time (ms)": round(elapsed_ms, 6),
        "Details": "IPv4 used to reach the IPv4 server",
    }


def simulate_tunneling(client):
    start = time.perf_counter()

    inner_packet = (
        f"IPv6 source={client}; destination={IPV6_SERVER}"
    )

    # Represent an outer IPv4 header and an inner IPv6 packet.
    outer_packet = {
        "outer_source": "192.0.2.1",
        "outer_destination": "192.0.2.2",
        "payload": inner_packet,
    }

    # Simulate decapsulation at the tunnel endpoint.
    recovered_packet = outer_packet["payload"]
    success = recovered_packet == inner_packet

    elapsed_ms = (time.perf_counter() - start) * 1000

    return {
        "Method": "Basic Tunneling",
        "Client IPv6": client,
        "Temporary IPv4": "Not required by this model",
        "Success": success,
        "Processing time (ms)": round(elapsed_ms, 6),
        "Details": (
            "IPv6 payload encapsulated in an outer IPv4 packet "
            "and recovered at the tunnel endpoint"
        ),
    }


def simulate_dstm(client, pool, mappings):
    start = time.perf_counter()

    if client in mappings:
        temporary_ipv4 = mappings[client]
        success = True
        details = "Existing address mapping reused"

    elif pool:
        temporary_ipv4 = pool.pop(0)
        mappings[client] = temporary_ipv4
        success = True
        details = "Temporary IPv4 address allocated"

    else:
        temporary_ipv4 = "Unavailable"
        success = False
        details = "Temporary IPv4 address pool exhausted"

    elapsed_ms = (time.perf_counter() - start) * 1000

    return {
        "Method": "DSTM-Inspired",
        "Client IPv6": client,
        "Temporary IPv4": temporary_ipv4,
        "Success": success,
        "Processing time (ms)": round(elapsed_ms, 6),
        "Details": details,
    }


def generate_clients(count):
    return [
        f"2001:db8:1::{i:x}"
        for i in range(1, count + 1)
    ]


def run_comparison(client_count):
    clients = generate_clients(client_count)
    rows = []

    # Each method is tested using the same number of clients.
    for client in clients:
        rows.append(simulate_dual_stack(client))

    for client in clients:
        rows.append(simulate_tunneling(client))

    # Give the DSTM-inspired method a fresh pool for this experiment.
    pool = IPV4_POOL.copy()
    mappings = {}

    for client in clients:
        rows.append(simulate_dstm(client, pool, mappings))

    return pd.DataFrame(rows), pool, mappings


# -------------------- SIDEBAR --------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a section",
    [
        "Dashboard",
        "Run Simulation",
        "Compare Methods",
        "Address Pool",
        "About Project",
    ],
)

st.sidebar.divider()
st.sidebar.write("**Student:** MCAM/033")
st.sidebar.write("**Topic:** IPv6 and IPv4-to-IPv6 transition")


# -------------------- DASHBOARD --------------------

if page == "Dashboard":
    st.header("Project Dashboard")

    st.write(
        "Explore how dual stack, IPv4 tunneling, and a simplified "
        "DSTM-inspired transition model behave under different "
        "simulation conditions."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Transition Methods", "3")
    col2.metric("Temporary IPv4 Pool", len(IPV4_POOL))
    col3.metric("Default Test Clients", "5")

    st.subheader("Network Address Examples")

    address_col1, address_col2 = st.columns(2)

    with address_col1:
        st.markdown("**IPv6 client**")
        st.code("2001:db8:1::10")

    with address_col2:
        st.markdown("**IPv4 service**")
        st.code(IPV4_SERVER)

    st.subheader("How the simulated system works")

    st.markdown(
        """
        1. An IPv6 client requests access to a service.
        2. The selected transition model handles the request.
        3. The DSTM-inspired model attempts to allocate a temporary
           IPv4 address and records the mapping.
        4. The simulator records success, failure, and processing time.
        5. Results can be compared and exported for the assignment report.
        """
    )


# -------------------- RUN ONE SIMULATION --------------------

elif page == "Run Simulation":
    st.header("Run a Transition Simulation")

    method = st.selectbox(
        "Select transition method",
        [
            "Dual Stack",
            "Basic Tunneling",
            "DSTM-Inspired",
        ],
    )

    client = st.text_input(
        "IPv6 client address",
        value="2001:db8:1::10",
    )

    if st.button("Run Simulation", type="primary"):
        try:
            ipaddress.IPv6Address(client)

            if method == "Dual Stack":
                result = simulate_dual_stack(client)

            elif method == "Basic Tunneling":
                result = simulate_tunneling(client)

            else:
                # A fresh pool is used for this individual test.
                result = simulate_dstm(
                    client,
                    IPV4_POOL.copy(),
                    {},
                )

            st.session_state["last_result"] = result

        except ipaddress.AddressValueError:
            st.error("Enter a valid IPv6 address, such as 2001:db8:1::10.")

    result = st.session_state.get("last_result")

    if result:
        st.subheader("Simulation Result")

        if result["Success"]:
            st.success("The simulated operation succeeded.")
        else:
            st.error("The simulated operation failed.")

        col1, col2 = st.columns(2)

        col1.metric("Selected Method", result["Method"])
        col2.metric(
            "Processing Time",
            f"{result['Processing time (ms)']:.6f} ms",
        )

        st.write("**Client IPv6:**", result["Client IPv6"])
        st.write("**Temporary IPv4:**", result["Temporary IPv4"])
        st.write("**Details:**", result["Details"])

        st.caption(
            "Processing time measures Python simulation code execution, "
            "not network latency."
        )


# -------------------- COMPARE METHODS --------------------

elif page == "Compare Methods":
    st.header("Compare Transition Methods")

    client_count = st.slider(
        "Number of simulated IPv6 clients",
        min_value=1,
        max_value=20,
        value=5,
    )

    st.write(
        "Each method receives the same number of simulated clients. "
        "The DSTM-inspired method has a pool of three temporary IPv4 "
        "addresses for this experiment."
    )

    if st.button("Run Comparison Experiment", type="primary"):
        df, remaining_pool, mappings = run_comparison(client_count)

        st.session_state["comparison_df"] = df
        st.session_state["remaining_pool"] = remaining_pool
        st.session_state["comparison_mappings"] = mappings

    df = st.session_state.get("comparison_df")

    if df is not None:
        summary = (
            df.groupby("Method")
            .agg(
                Clients=("Success", "count"),
                Successful=("Success", "sum"),
            )
            .reset_index()
        )

        summary["Failed"] = summary["Clients"] - summary["Successful"]

        summary["Success rate (%)"] = (
            summary["Successful"] / summary["Clients"] * 100
        ).round(1)

        st.subheader("Comparison Summary")
        st.dataframe(summary, use_container_width=True, hide_index=True)

        st.subheader("Simulated Delivery Success Rate")

        chart_data = summary.set_index("Method")[
            ["Success rate (%)"]
        ]
        st.bar_chart(chart_data, y="Success rate (%)")

        st.subheader("Detailed Experiment Results")

        display_df = df.copy()
        display_df["Success"] = display_df["Success"].map(
            {True: "Yes", False: "No"}
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )

        csv_data = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Comparison CSV",
            data=csv_data,
            file_name="comparison_results.csv",
            mime="text/csv",
        )

        st.caption(
            "The success rates reflect the assumptions and resource "
            "limits built into this simplified model. They do not establish "
            "real-world superiority of any transition method."
        )


# -------------------- ADDRESS POOL --------------------

elif page == "Address Pool":
    st.header("Temporary IPv4 Address Pool")

    st.write(
        "The addresses below use the documentation-only IPv4 range "
        "192.0.2.0/24. They are examples for simulation, not public "
        "service addresses."
    )

    if "pool_state" not in st.session_state:
        st.session_state["pool_state"] = IPV4_POOL.copy()

    if "mapping_state" not in st.session_state:
        st.session_state["mapping_state"] = {}

    client = st.text_input(
        "IPv6 client requesting an address",
        value="2001:db8:1::10",
        key="pool_client",
    )

    if st.button("Allocate Temporary IPv4"):
        try:
            ipaddress.IPv6Address(client)

            pool = st.session_state["pool_state"]
            mappings = st.session_state["mapping_state"]

            if client in mappings:
                st.info(
                    f"Existing mapping: {client} -> {mappings[client]}"
                )
            elif pool:
                address = pool.pop(0)
                mappings[client] = address
                st.success(f"Allocated {address} to {client}")
            else:
                st.error("Pool exhausted. No addresses remain.")

        except ipaddress.AddressValueError:
            st.error("Enter a valid IPv6 client address.")

    pool = st.session_state["pool_state"]
    mappings = st.session_state["mapping_state"]

    col1, col2 = st.columns(2)
    col1.metric("Available Addresses", len(pool))
    col2.metric("Allocated Addresses", len(mappings))

    st.subheader("Available Pool")

    if pool:
        st.dataframe(
            pd.DataFrame({"Available IPv4 addresses": pool}),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.warning("All temporary IPv4 addresses have been allocated.")

    st.subheader("Address Mapping Table")

    if mappings:
        mapping_df = pd.DataFrame(
            [
                {"IPv6 Client": ipv6, "Temporary IPv4": ipv4}
                for ipv6, ipv4 in mappings.items()
            ]
        )

        st.dataframe(
            mapping_df,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.write("No addresses have been allocated in this session.")

    if st.button("Reset Address Pool"):
        st.session_state["pool_state"] = IPV4_POOL.copy()
        st.session_state["mapping_state"] = {}
        st.rerun()


# -------------------- PROJECT INFORMATION --------------------

elif page == "About Project":
    st.header("About This Mini Project")

    st.markdown(
        """
        **Student:** Pratistha Hazarika

        **Roll number:** MCAM/033

        **Course:** Computer Networks and Information Security

        **Assigned topic:** III-6 — IPv6 and IPv4-to-IPv6 transition.

        **Project objective:** Build a software simulation of transition
        approaches and compare their behavior under a controlled workload.

        **Methods modelled:**
        - Dual Stack
        - Basic IPv4 tunneling
        - DSTM-inspired temporary IPv4 allocation and mapping
        """
    )

    st.warning(
        "The DSTM-inspired implementation is a simplified educational "
        "model. It does not implement the complete DSTM protocol or prove "
        "that this code reproduces the cited patent. Patent-specific "
        "features must be verified against the approved patent document."
    )

    st.subheader("Technologies")
    st.write("Python, Streamlit, Pandas, and the Python ipaddress module.")

    st.subheader("Suggested future improvements")
    st.markdown(
        """
        - Implement realistic packet and tunnel data structures.
        - Add repeated trials and statistical summaries.
        - Compare address consumption and allocation failures.
        - Validate the design against the selected patent.
        - Document limitations and experimental assumptions.
        """
    )


st.divider()
st.caption(
    "CNIS Patent-Based Mini Project | MCAM/033 | "
    "Educational simulation — not a production networking tool"
)

#to run the application: python -m streamlit run gui.py