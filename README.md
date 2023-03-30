# stochastic_music

generator.py generates a sequence of musical notes and corresponding MIDI messages using given inputs. The function takes in a list of possible pitches, as well as optional weightings for the pitches, octaves, and durations of the notes. The length of the sequence, time per beat, and variability in duration and velocity can also be specified. The output is a list of Note objects and MIDI messages that can be used to create a MIDI file or played through a MIDI device.

This function can be useful in generating randomized music sequences for creative applications or music analysis. By adjusting the weights and other parameters, users can create unique sequences that conform to specific musical styles or moods. Additionally, the function can be incorporated into larger software applications for music production or experimentation. The demo notebook shows how to use the function to generate randomized sequences of notes and MIDI messages, and how to play the MIDI messages through a MIDI device.

# TwelveTone

twelve_tone_gen.py is an implementation of twelve-tone composition, also known as serial composition, a method of music composition developed by Arnold Schoenberg in the early 20th century. The class can be used to generate twelve-tone rows, matrices, and sequences of notes based on the rows, with options for controlling the octave, duration, and velocity of each note.

any_tone_gen.py is a modified version that works with any scales. The demo notebook shows how to use it with the pentatonic scale.
# Applications

The TwelveTone class can be used for:

Generating random twelve-tone rows and sequences of notes for use in music composition and sound design
Exploring and analyzing the properties of twelve-tone matrices and sequences, including transpositions, inversions, retrogrades, and retrograde inversions
Studying and teaching the principles of serial composition in music theory and composition courses
Example usage:

'''
import any_tone

row = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

tt = any_tone.TwelveTone(row)

notes, midi_notes = tt.generator(length=4)

midi_path = 'my_music.mid'
mid = mido.MidiFile()
track = mido.MidiTrack()
mid.tracks.append(track)
for note in midi_notes:
    track.append(note)
mid.save(midi_path)
'''


