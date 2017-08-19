from collections import Counter, defaultdict
from itertools import izip_longest
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
from itertools import groupby
import pandas as pd
import copy
import numpy as np
import sys


oscar = pd.read_csv('../midi/oscar2notes.txt', skiprows=2)[:].sort_values(by="Offset")
oscar.index = xrange(1, len(oscar) + 1)
oscar = oscar[oscar.Octave >= 4]
"""
with open('../midi/oscar2notes.txt', 'rb') as f:
    metmark = float(f.readline())
    tsig_num, tsig_den = [i for i in f.readline().replace(' /', '').split()]

print "Metrics:"
print metmark, tsig_num + "/" + tsig_den, len(oscar)
"""

""" 1. Get generated notes based on the trigram model.


# Iterate over a list in chunks of size n, return tuples.
def chunks(iterable, n):
    for ix, item in enumerate(iterable):
        if ix == len(iterable) - (n-1): return
        yield tuple(iterable[ix:ix+n])

# Build the conditional probability tables.
def condProbTables(ngramfreqs, )

s = ['a', 'b', 'c', 'd']
t = chunks(s, 3)
for item in t:
    print item
"""

possiblenotes = ["%s%s" % (row[1]["Note/Rest"], row[1]["Octave"]) for row in oscar.iterrows()]
possiblenotes.insert(0, "start")
possiblenotes.insert(0, "start")
possiblenotes.insert(0, "start")


def ngram(iter, grams):
    """
    generate the n-gram vocabulary.
    """
    for index, note in enumerate(iter):
        if index == len(iter) - (grams-1):return
        yield tuple(iter[index:index+grams])

t = ngram(possiblenotes, 2)
for item in t:
    print item