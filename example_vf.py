import re
import sys
import random
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # For mean and standard deviation calculations
from glob import glob
from os.path import basename, join


class Benchmark:
    """Measurements from a single benchmark"""

    def __init__(self, filename):
        self.filename = filename

        m = re.match(r'(?P<org>[^_]+)__(?P<proj>[^#]+)#'
                     r'(?P<method>[^#]+)#(?P<params>.*)\.json',
                     basename(filename))
        if m is None:
            print('Unable to parse: {}'.format(filename), file=sys.stderr)
            return

        for k, v in m.groupdict().items():
            setattr(self, k, v)

    def get_repository(self):
        return '{}/{}'.format(self.org, self.proj)

    def get_repository_url(self):
        return 'https://github.com/{}'.format(self.get_repository())

    def set_revision(self, revisions_csv):
        df = pd.read_csv(revisions_csv)
        df = df[df['repository'] == self.get_repository()]
        self.revision = df['tag'].iloc[0]

    def get_measurements(self):
        with open(self.filename) as f:
            self.measurements = json.load(f)
        return self.measurements

def get_benchmarks(data_dir):
    """Get all the jsons we can find and try to parse their names"""
    return [Benchmark(f) for f in glob('{}/*.json'.format(data_dir))]

def calculate_cv(fork_data):
    """Calculate the Coefficient of Variation (CV) for a fork's execution times"""
    mean_exec_time = np.mean(fork_data)
    std_dev_exec_time = np.std(fork_data)
    if mean_exec_time != 0:
        cv = (std_dev_exec_time / mean_exec_time) * 100  # CV as a percentage
    else:
        cv = 0  # Handle edge case
    return cv

def plot_cv_vs_forks(benchmark):
    """Plot how the Coefficient of Variation (CV) changes as the number of forks increases"""

    # Get the measurements
    data = benchmark.get_measurements()

    # Store CVs for each fork
    cvs = []
    
    # Calculate CV for each fork
    for i, fork in enumerate(data):
        cv = calculate_cv(fork)
        cvs.append(cv)

    # Plot CV vs number of forks
    forks = list(range(1, len(data) + 1))
    plt.figure(figsize=(10, 6))
    plt.plot(forks, cvs, marker='o')
    plt.title('Coefficient of Variation (CV) vs Number of Forks\nProject: {}, Method: {}'.format(
        benchmark.get_repository(), benchmark.method))
    plt.xlabel('Number of Forks')
    plt.ylabel('Coefficient of Variation (%)')
    plt.grid(True)

    # Save the plot
    plotfile = join('/tmp/', basename(benchmark.filename).replace('.json', '_cv_vs_forks.png'))
    plt.savefig(plotfile, dpi=300)
    plt.show()  # Show the plot
    print('CV vs Forks plot saved to: {}'.format(plotfile))

def random_viz(data_dir, revisions):
    """Randomly pick a benchmark to visualize and plot CV vs forks"""

    # Find the measurements data
    benchmarks = get_benchmarks(DATA_DIR)

    # Randomly select a benchmark to visualize
    bench = random.choice(benchmarks)

    # Associate a revision to the benchmark
    bench.set_revision(REVISIONS)

    # Plot CV vs number of forks
    plot_cv_vs_forks(bench)

if __name__ == "__main__":
    # Define paths
    DATA_DIR = 'timeseries'
    REVISIONS = 'benchmarks_revision.csv'

    # Call the visualization function
    random_viz(DATA_DIR, REVISIONS)
