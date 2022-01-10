from pandas import read_csv
from matplotlib import pyplot
import sys

series=read_csv(sys.argv[1], sep="\t", index_col=0,parse_dates=True, squeeze=True)

series.plot()
pyplot.show()