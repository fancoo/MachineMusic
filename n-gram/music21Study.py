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

# flats use '-' and sharps use '#'
bflat = note.Note("B-2")
print bflat.pitch.frequency

notes_file = open('oscar2ngrams.txt', 'r')

s = stream.Part()
for line in notes_file:
    toks = line.strip().split(',')
    print toks
    tone = toks[0]
    offset = float(toks[1])
    n = note.Note(nameWithOctave=tone, quarterLength=offset)
    s.append(n)
notes_file.close()
s.write('midi', 'study.mid')