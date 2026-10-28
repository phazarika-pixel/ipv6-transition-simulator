# IPv4-to-IPv6 Transition Simulator

A Python-based simulation project developed for the Computer Networks and Information Security (CNIS) course. The project explores IPv4-to-IPv6 transition techniques through address validation, simulated packet tunneling, temporary IPv4 address allocation, and comparative experiments.


## Overview

IPv4 and IPv6 use different address formats and packet structures. During the transition from IPv4 to IPv6, networks may use techniques that allow both protocols to coexist or communicate across different network environments.

This project implements a simplified software simulation of three approaches:

1. **Dual Stack:** Models a client with IPv4 and IPv6 capabilities communicating with an IPv4 server.
2. **Basic Tunneling:** Models encapsulating an IPv6 packet inside an outer IPv4 packet and recovering the original packet at a simulated tunnel endpoint.
3. **DSTM-Inspired Transition:** Models allocating temporary IPv4 addresses to IPv6 clients and maintaining an address mapping table.

The project includes a command-line simulator, an allocation experiment, a comparison script, and an interactive graphical interface.

## Objectives

- Understand IPv4 and IPv6 addressing.
- Demonstrate address validation using Python.
- Model packet encapsulation and decapsulation.
- Simulate temporary IPv4 address allocation.
- Maintain IPv6-to-temporary-IPv4 address mappings.
- Investigate address-pool exhaustion.
- Compare the behavior of different transition models under controlled simulation conditions.
- Export experimental results as CSV files.
- Present simulation results through an interactive dashboard.

## Technologies Used

- **Python:** Core programming language.
- **Streamlit:** Interactive web-based graphical interface.
- **Pandas:** Tabular data processing and experiment summaries.
- **Python `ipaddress` module:** IPv4 and IPv6 address validation.
- **Python `csv` module:** Exporting experimental results.
- **Git and GitHub:** Version control and source-code hosting.

## Project Structure

```text
cn_is_dstm/
├── .gitignore
├── main.py
├── compare.py
├── gui.py
├── results/
│   ├── experiment.py
│   ├── experiment_results.csv
│   └── comparison_results.csv
└── .venv/
```

The `.venv` directory is a local Python virtual environment and should not be uploaded to GitHub.

### File Descriptions

| File | Description |
|---|---|
| `main.py` | Command-line simulator for address validation, dual stack, tunneling, and DSTM-inspired allocation. |
| `compare.py` | Runs the three simplified models against a common set of simulated clients and exports comparison results. |
| `gui.py` | Streamlit application with a dashboard, simulation controls, comparison charts, CSV download, and address-pool management. |
| `results/experiment.py` | Tests temporary IPv4 address allocation and pool exhaustion. |
| `results/experiment_results.csv` | Stores individual address-allocation experiment results. |
| `results/comparison_results.csv` | Stores individual results from the three-method comparison. |

## Requirements

- Windows, Linux, or macOS.
- Python 3.10 or later recommended.
- pip, the Python package installer.
- Visual Studio Code or another Python-compatible editor.
- Git for version control.
- An internet connection for installing dependencies.

The command-line simulator and allocation experiment primarily use Python's standard library. The graphical interface requires Streamlit and Pandas.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/cn-is-ipv6-transition-simulator.git
cd cn-is-ipv6-transition-simulator
```

Replace `YOUR-USERNAME` with the GitHub username associated with the repository.

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

On Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install streamlit pandas
```

## Running the Project

### Command-Line Simulator

Run:

```bash
python main.py
```

The menu allows users to:

1. Validate IPv4 and IPv6 addresses.
2. Simulate dual-stack communication.
3. Simulate basic tunneling.
4. Simulate DSTM-inspired address allocation.
5. View the address mapping table.
6. View the remaining temporary IPv4 address pool.
7. Exit the application.

### Address-Allocation Experiment

Run the experiment from the project root:

```bash
python results/experiment.py
```

The experiment generates five IPv6 clients and attempts to allocate addresses from a pool containing three temporary IPv4 addresses.

The resulting CSV file is saved under the `results` directory when the script is run from the project root.

### Transition Comparison

Run:

```bash
python compare.py
```

The comparison script evaluates the three simplified transition models using the same number of simulated clients and saves the detailed results to:

```text
results/comparison_results.csv
```

### Graphical Interface

Run:

```bash
python -m streamlit run gui.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

The graphical interface provides the following sections:

- Dashboard
- Run Simulation
- Compare Methods
- Address Pool
- About Project

The comparison section supports selecting the number of simulated clients, viewing summary statistics, examining individual results, and downloading the comparison CSV.

## Simulation Workflow

The project follows this general workflow:

1. Generate or enter an IPv6 client address.
2. Validate the address using Python's `ipaddress` module.
3. Select a transition model.
4. Simulate the model's behavior.
5. Record success or failure and relevant processing details.
6. Aggregate results for comparison.
7. Display the results in the terminal or graphical interface.
8. Export experimental data for further analysis.

## Experimental Results

In the default comparison experiment, five simulated IPv6 clients are tested against each transition model. The DSTM-inspired model has a pool of three temporary IPv4 addresses.

The expected results under the current implementation are:

| Method | Successful Operations | Failed Operations | Success Rate |
|---|---:|---:|---:|
| Dual Stack | 5 | 0 | 100% |
| Basic Tunneling | 5 | 0 | 100% |
| DSTM-Inspired | 3 | 2 | 60% |

These figures demonstrate the behavior of the current simulation under its configured assumptions.

The DSTM-inspired model fails to allocate an address to two clients because the available address pool is exhausted. The dual-stack and tunneling models are configured to succeed for all five clients in this experiment.

Consequently, these results should not be interpreted as proof that one transition technique is more efficient or reliable than another in real networks.

## Limitations

This project is an educational software simulation and has the following limitations:

- It does not transmit real IPv4 or IPv6 packets.
- Packet encapsulation and decapsulation are represented using Python data structures rather than actual network tunnel interfaces.
- It does not configure routers, routing tables, or real tunnel endpoints.
- The DSTM-inspired implementation models temporary IPv4 allocation and address mapping but does not implement the complete DSTM protocol.
- The comparison uses simplified assumptions that favor successful outcomes for dual stack and tunneling while imposing a limited address pool on the DSTM-inspired model.
- Processing time measures local Python execution time, not end-to-end network latency or throughput.
- The implementation must be checked against the selected patent before claiming that it reproduces patent-specific functionality.

## Future Improvements

Potential improvements include:

- Implementing shared simulation logic in a separate Python module.
- Adding more realistic packet and tunnel representations.
- Testing different address-pool sizes and client workloads.
- Introducing repeated trials and statistical summaries.
- Comparing allocation success, resource consumption, and simulated overhead under clearly defined conditions.
- Adding more detailed packet-flow visualizations to the graphical interface.
- Validating the implementation against an approved patent and documenting the patent-specific features.
- Extending the prototype to a real networking laboratory where feasible.

## Academic Context

This project was developed as part of the Computer Networks and Information Security assignment for MCA Semester III, academic session 2026–2027.

## License

No license has been selected for this project yet. Add an appropriate license file if you intend to distribute the source code publicly.