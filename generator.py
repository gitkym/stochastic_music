import random
import mido
import numpy as np

class Note:
    def __init__(self, pitch, octave, duration, velocity):
        self.pitch = pitch
        self.octave = octave
        self.duration = duration
        self.velocity = velocity

def generator(notes, pitch_weights=None, octave_weights=None, duration_weights=None, length=1, tpb=480, 
              duration='fixed', velocity = 'fixed', 
              sd=0.064, rest_probability=0.16):
    
    if pitch_weights is None:
        pitch_weights = {note: 1 for note in notes}  # set all weights to 1 if not specified
    if octave_weights is None:
        octave_weights = {octave: 1 for octave in range(0, 9)}  # set all weights to 1 if not specified

    durations = tpb*np.logspace(-5, 2, num=8, base=2) # duration of the note from 1/32 to 4
    if duration_weights is None:
        duration_weights = {duration: 1 for duration in durations}  # set all weights to 1 if not specified

    vel = 64
    sequence = []
    for _ in range(length):
        # Choose a random octave between 0 and 8
        octave = random.choices(range(0, 9), weights=octave_weights)[0]
        # Choose a random note from the given notes with the given weights
        pitch = random.choices(notes, weights=pitch_weights)[0]
        dur = int(random.choices(durations, weights=duration_weights)[0])
        # Check for variables
        if duration == 'variable':
            dur = int(random.normalvariate(dur, dur * sd))
        if velocity == 'variable':
            vel = int(random.normalvariate(64, 64 * sd))
        # Introduce rests with a certain probability
        if random.random() < rest_probability:
            sequence.append(Note(pitch=0, octave=0, duration=dur, velocity=0))
        # Append the note to the sequence
        sequence.append(Note(pitch=pitch, octave=octave, duration=dur, velocity=vel))

    midi_notes = []

    for n in sequence:
        note_on = mido.Message('note_on', note=n.pitch + (n.octave * 12), 
                               velocity=n.velocity, time=0)
        midi_notes.append(note_on)
        note_off = mido.Message('note_off', note=n.pitch + (n.octave * 12), 
                                velocity=n.velocity, time=n.duration)
        midi_notes.append(note_off)

    return sequence, midi_notes
