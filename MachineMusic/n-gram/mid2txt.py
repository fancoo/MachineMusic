from music21 import *

oscar = converter.parse('../midi/Oscar-Peterson-2.mid')
oscar2notes = open('../midi/oscar2notes.txt', 'w')
# oscar2.show('text')
'''
{0.0} <music21.stream.Part 46672864>
    {0.0} <music21.tempo.MetronomeMark Quarter=176.0>
    {0.0} <music21.meter.TimeSignature 4/4>
    {0.0} <music21.stream.Voice 0x25e5f60>
        {0.0} <music21.note.Rest rest>
        {8.0} <music21.chord.Chord D5 C4 E6 A6 A5 D6>
        {9.6667} <music21.chord.Chord G3 A3>
        {12.6667} <music21.note.Note B>
'''
# Get the first part
singlepart = oscar[0]
timesig = singlepart.getElementsByClass(meter.TimeSignature)[0]
mmark = singlepart.getElementsByClass(tempo.MetronomeMark)[0]
allnotes = []
allchords = []
# get different instruments' voices
for ix, voice in enumerate(singlepart.getElementsByClass(stream.Voice)):
    notes = voice.getElementsByClass(note.Note).notes
    chords = voice.getElementsByClass(chord.Chord)
    for i in notes:
        allnotes.append(i)
    for i in chords:
        allchords.append(i)

# Metronome
oscar2notes.write(str(mmark.number) + '\n')
print mmark.number
# 4/4
oscar2notes.write("%s / %s" % (timesig.numerator, timesig.denominator) + '\n')
print "%s / %s" % (timesig.numerator, timesig.denominator)

# Get chords and convert them to txt.
"""
print "FullName, CommonName, Len, Offset"
for i in allchords:
    '''
    pitchedCommonName: the common name of that chord
    quarterLength    : how many quarter note does this chord last.
    offset           : the time Offset of this position.
    '''
    print "%s,%s,%s,%s" % (i.fullName,
      i.pitchedCommonName, i.quarterLength, float(i.offset))"""

oscar2notes.write("Note/Rest,Octave,Len,Offset" + '\n')
for i in allnotes:
    oscar2notes.write("%s, %s, %s, %s" % (i.name, i.octave, i.quarterLength, float(i.offset)) + "\n")

oscar2notes.close()
