
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

## Analysis

- `paper-review.pdf`: this document provides a general review of the Traini Paper, focusing on its key findings, methodology, and implications for performance benchmarking in Java software:
[View paper](https://www.dropbox.com/scl/fi/gv0c2kfj8dj24vdz8ytdy/paper-review.pdf?rlkey=pkv84aro0lkhr7edg27dk6q5o&st=0r40ei24&dl=0)

- `independent-analysis.pdf`: this document presents my replicated results, specifically focusing on the analysis of the CV, highlighting how performance consistency fluctuates across the benchmarked fork instances:
[View paper](https://www.dropbox.com/scl/fi/wfahq13we1hs4gr5ky3lo/independent-analysis.pdf?rlkey=adxur4gtnxahixjibe9y6v1ft&st=ipb4w279&dl=0)

- `custom-analysis.pdf`: this document displays how varying the number of forks in JMH microbenchmarks affects the consistency of performance measurements when a steady-state is reached:
[View paper](https://www.dropbox.com/scl/fi/tn9z4umls8nzonc998n02/custom-analysis.pdf?rlkey=ietqjg47hg3dmcpg9rq5ywj8t&st=ercsv7o0&dl=0)

- `custom-analysis-teardown.pdf`: this document displays how the teardown phase influences subsequent executions or the stability of the performance measurements collected during the steady-state:
[View paper](https://www.dropbox.com/scl/fi/eulmh1ykub2vflw65r8rl/custom-analysis-teardown.pdf?rlkey=meqwpen576s8fyj0xw06estsm&st=pw3w18ur&dl=0)

## Changes Made:

- Import numpy: I added numpy (import numpy as np) to handle calculations for the mean and standard deviation

- Calculate the CV: For each fork, the mean and standard deviation are computed using np.mean(fork) and np.std(fork).  The CV is then calculated as:

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
