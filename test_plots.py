# conversational data monster
# plot tests

import csv
from matplotlib.figure import Figure
import numpy as np


dataset_file = 'datasets/population_by_country_2020.csv'
with open(dataset_file, 'r') as infile:
  reader = csv.reader(infile)
  dataset = list(reader)


def plot(a, b, limit=10, figsize=(8, 6), dpi=120):
    # plot a versus b - finding ab,b in dataset
    # find match in a:
    ai = [i for i, s in enumerate(dataset[0]) if a.lower() in s.lower()]
    # find match in b:
    bi = [i for i, s in enumerate(dataset[0]) if b.lower() in s.lower()]
    data = np.array(dataset)
    # Generate the figure **without using pyplot**.
    fig = Figure(figsize=figsize, dpi=dpi)
    ax = fig.subplots()
    # ax.plot(dataset[0], dataset[1])
    ax.plot(data[1:limit, ai[0]], data[1:limit, bi[0]])
    # save plot
    fig.savefig("test_figs.png", format="png")
    return data


print(dataset[0:3])
plot('country', 'population')
