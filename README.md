
## Getting Started

Welcome to the microbenchmarking-coefficient-variation.  This modified codebase uses only timeseries data related to JSON decoding and encoding.

## Folder Structure

The workspace contains three Python scripts by default, where:

- `example_ce.py`: this script calculates the coefficient of variation (CV)
- `example_vf.py`: this script demonstrates how dynamically adjusting the fork count influences the CV, providing insights into the impact of changing fork instances on performance consistency
- `example_viz.py`: this script is designed to visualize performance measurements from a set of Java microbenchmarks stored in JSON files

To add the CV calculation to the script, we will compute the CV for each fork in the plot function.  This involves calculating the mean and standard deviation of the execution times and then using these to compute the CV. The CV will then be displayed in the plot title for each fork.

## How to Run

- `python3 example_vf.py`: this command will display the performance consistency across a series of fork instance time series

## Changes Made:

- Import numpy: I added numpy (import numpy as np) to handle calculations for the mean and standard deviation.

- Calculate the CV: For each fork, the mean and standard deviation are computed using np.mean(fork) and np.std(fork).  The coefficient of variation is then calculated as:

```markdown
cv = (std_dev_exec_time / mean_exec_time) * 100  # Expressed as a percentage
```

If the mean execution time is zero (an edge case), we handle it by setting cv = 0 to avoid division by zero.

- Display CV: The CV is displayed in the title of each subplot for the corresponding fork:

```markdown
axs[i].set_title('Fork: {} (CV: {:.2f}%)'.format(i, cv))
```

# Dataset for the ICPE 2023 Data Challenge track

Information about the track:
[https://icpe2023.spec.org/tracks-and-submissions/data-challenge-track/](https://icpe2023.spec.org/tracks-and-submissions/data-challenge-track/)

The dataset contains performance measurements of JMH microbenchmarks from 30 Java open source projects. The list of projects, along with the revision at which the microbenchmarks were executed, can be found in [benchmarks_revision.csv](benchmarks_revision.csv).

The measurements are organized in time series available in the [timeseries](timeseries) folder. Morevover, the raw samples (JMH output) in JSON format can be found on [https://zenodo.org/record/5961018](https://zenodo.org/record/5961018) (~65GB when unpacked).

Questions about the dataset can be asked by opening issues on this repository, or by sendind an e-mail to icpe2023-data-challenge@easychair.org.

## Usage example

In the python script [example_ce.py](example_ce.py) you can find an example of how to read the data and generate a simple plot for a random benchmark in the dataset. The script requires `pandas` and `matplotlib`:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python example_ce.py
```

---

The dataset was originally created for the paper:

Luca Traini, Vittorio Cortellessa, Daniele Di Pompeo, Michele Tucci  
**Towards effective assessment of steady state performance in Java software: Are we there yet?**  
Empirical Software Engineering (EMSE) - 28, 13 (2023)  
[https://doi.org/10.1007%2Fs10664-022-10247-x](https://doi.org/10.1007%2Fs10664-022-10247-x)  
[https://github.com/SEALABQualityGroup/steady-state](https://github.com/SEALABQualityGroup/steady-state)
