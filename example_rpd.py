import re
import sys
import random
import json
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
from os.path import basename


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

    def compute_rpd(self, fork1, fork2):
        """Compute Relative Performance Deviation (RPD) between two forks"""
        mean_fork1 = sum(fork1) / len(fork1)
        mean_fork2 = sum(fork2) / len(fork2)
        rpd = abs(mean_fork1 - mean_fork2) / mean_fork1
        return rpd


def get_benchmarks(data_dir):
    """Get all the jsons we can find and try to parse their names"""
    return [Benchmark(f) for f in glob('{}/*.json'.format(data_dir))]

def plot_rpd(benchmark, rpd_before_after):
    """Plot the RPD between forks before and after the teardown phase"""
    
    # Create plot
    plt.figure(figsize=(10, 6))
    x = list(range(len(rpd_before_after)))
    y = rpd_before_after
    plt.bar(x, y, color='skyblue')

    plt.title(f'RPD between forks before and after teardown for {benchmark.method}')
    plt.xlabel('Fork Pair')
    plt.ylabel('Relative Performance Deviation (RPD)')
    plt.xticks(x, [f'Fork {i} vs Fork {i+1}' for i in x])
    plt.tight_layout()

    # Save and display
    plotfile = basename(benchmark.filename).replace('.json', '_rpd.png')
    plt.savefig(plotfile, dpi=300)
    print(f'RPD plot saved to: {plotfile}')
    plt.show()


def analyze_rpd(benchmark):
    """Analyze the RPD between forks before and after the teardown phase"""

    # Get the measurements
    data = benchmark.get_measurements()

    # Calculate RPD between consecutive forks (simulating before/after teardown)
    rpd_before_after = []
    for i in range(len(data) - 1):
        rpd = benchmark.compute_rpd(data[i], data[i+1])
        rpd_before_after.append(rpd)

    # Plot the RPD analysis
    plot_rpd(benchmark, rpd_before_after)


def random_viz(data_dir, revisions):
    """Randomly pick a benchmark to analyze"""

    # Find the measurements data
    benchmarks = get_benchmarks(DATA_DIR)

    # Randomly select a benchmark to visualize
    bench = random.choice(benchmarks)

    # Associate a revision to the benchmark
    bench.set_revision(REVISIONS)

    # Analyze RPD between forks before and after teardown
    analyze_rpd(bench)


if __name__ == "__main__":

    DATA_DIR = 'timeseries'
    REVISIONS = 'benchmarks_revision.csv'

    random_viz(DATA_DIR, REVISIONS)
