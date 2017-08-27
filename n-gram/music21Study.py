from music21 import *

# s = stream.Score()
# p1 = stream.Part()
# p1.id = 'part1'
# p1.insert(4, note.Note("C#4"))
# p1.insert(5.3, note.Rest())
# p2 = stream.Part()
# p2.id = 'part2'
# p2.insert(2.12, note.Note('D-4', type='half'))
# p2.insert(5.5, note.Rest())
# s.insert(0, p1)
# s.insert(0, p2)
# s.show('text', addEndTimes=True)
# cc = s.chordify()
# cc.show('text', addEndTimes=True)


f = note.Note("F5")
f4 = note.Note("F4")
print f.name
# the 5th octave of "F"
print f.octave
# the frequency of "F5"
print f.pitch.frequency
print f4.pitch.frequency

# # flats use '-' and sharps use '#'
# bflat = note.Note("B-2")
# print bflat.pitch.frequency

# print origin notes
import pandas as pd
oscar = pd.read_csv('../midi/oscar2notes.txt', skiprows=2)[:].sort_values(by="Offset")
oscar.index = xrange(1, len(oscar) + 1)


def deal(string):
    if '/' not in string:
        return float(string)
    elements = string.split('/')
    return float(elements[0]) / float(elements[1])

s = stream.Part()

for row in oscar.iterrows():
    tone = row[1]['Note/Rest'] +  str(row[1]['Octave'])
    length = row[1]['Len']
    length = deal(length)
    n = note.Note(nameWithOctave=tone, quarterLength=length)
    s.append(n)


s.write('midi', 'study.mid')