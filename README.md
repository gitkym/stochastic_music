# Stochastic Music

generator.py generates a sequence of musical notes and corresponding MIDI messages using given inputs. The function takes in a list of possible pitches, as well as optional weightings for the pitches, octaves, and durations of the notes. The length of the sequence, time per beat, and variability in duration and velocity can also be specified. The output is a list of Note objects and MIDI messages that can be used to create a MIDI file or played through a MIDI device.

This function can be useful in generating randomized music sequences for creative applications or music analysis. By adjusting the weights and other parameters, users can create unique sequences that conform to specific musical styles or moods. Additionally, the function can be incorporated into larger software applications for music production or experimentation. The demo notebook shows how to use the function to generate randomized sequences of notes and MIDI messages, and how to play the MIDI messages through a MIDI device.

# Twelve-Tone Stochastic Music

twelve_tone_gen.py is an implementation of Twelve-Tone method, one of the compositional techniques that gained popularity in the 20th century as part of the Serial music movement. 

The script can be used to generate twelve-tone rows, matrices, and sequences of notes based on the rows, with options for controlling the octave, duration, and velocity of each note.

any_tone_gen.py is a modified version that works with any scale. The demo notebook shows how to use it with the pentatonic scale.

Although the sequences are generated using the twelve tone method, my implemetation imposes the same randomness on the octave, duration and velocity of each note. Additionally, successive sequences are constructed from rows randomly chosen from the matrix constructed from the prime row. 

## Installation:
```
pip install -r requirements.txt
```

Example usage:

```
import mido
import twelve_tone_gen as twelve_tone

prime_row = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

tt = twelve_tone.TwelveTone(prime_row)

notes, midi_notes = tt.generator(length=4)

midi_path = 'my_music.mid'
mid = mido.MidiFile()
track = mido.MidiTrack()
mid.tracks.append(track)
for note in midi_notes:
    track.append(note)
mid.save(midi_path)
```


