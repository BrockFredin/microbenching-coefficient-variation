import re
import sys
import random
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Import numpy for standard deviation and mean calculation
from glob import glob
from os.path import basename, join
import os

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

def plot(benchmark):
    """Simple plot just to check that everything is in place"""

    # Get the measurements
    data = benchmark.get_measurements()

    # Create as many axes as the number of forks in the data
    fig, axs = plt.subplots(len(data), figsize=(15, 3 * len(data)))

    # Put some info about the benchmark in the title
    title = 'Project {} at rev {}\nMethod: {}'.format(
            benchmark.get_repository(), benchmark.revision, benchmark.method)
    if benchmark.params != '':
        title += '\nParams: {}'.format(benchmark.params)
    fig.suptitle(title)

    # Make a scatter plot for each fork
    for i, fork in enumerate(data):
        x = [x for x in range(0, len(fork))]

        # Calculate Coefficient of Variation (CV)
        mean_exec_time = np.mean(fork)
        std_dev_exec_time = np.std(fork)
        if mean_exec_time != 0:
            cv = (std_dev_exec_time / mean_exec_time) * 100  # Express CV as a percentage
        else:
            cv = 0  # Handle edge case where mean is 0

        # Plot the data
        axs[i].scatter(x, fork)
        axs[i].set_title('Fork: {} (CV: {:.2f}%)'.format(i, cv))  # Display CV in the title
        axs[i].set_xlabel('Iteration')
        axs[i].set_ylabel('Average Exec Time (seconds)')

    # Ensure plot layout is neat
    plt.subplots_adjust(top=0.85)

    # Save the plot with the correct path
    plotfile = join('/tmp/', basename(benchmark.filename).replace('.json', '.png'))  # Change path as needed
    plt.savefig(plotfile, dpi=300)
    plt.show()  # Display the plot to ensure it's being created

    # Debugging: print the current working directory and file path
    print('Current working directory:', os.getcwd())
    print('Plot file path:', plotfile)
    print('Plot saved to: {}'.format(plotfile))

def random_viz(data_dir, revisions):
    """Randomly pick a benchmark to visualize"""

    # Find the measurements data
    benchmarks = get_benchmarks(data_dir)

    # Randomly select a benchmark to visualize
    bench = random.choice(benchmarks)

    # Associate a revision to the benchmark
    bench.set_revision(revisions)

    # Plot it
    plot(bench)

if __name__ == "__main__":
    # Define paths
    DATA_DIR = 'timeseries'
    REVISIONS = 'benchmarks_revision.csv'

    # Debugging: print the paths being used
    print(f"Data directory: {DATA_DIR}")
    print(f"Revisions file: {REVISIONS}")

    # Call the visualization function
    random_viz(DATA_DIR, REVISIONS)
