import mido
import random
import numpy as np

class Note:
    def __init__(self, pitch, octave, duration, velocity):
        self.pitch = int(pitch)
        self.octave = int(octave)
        self.duration = int(duration)
        self.velocity = int(velocity)
#####################################
def transpose(row, interval, direction='up'):
    """Transpose row by interval"""
    if direction == 'up':
        return [(note+interval)%12 for note in row]
    else:
        return [(note-interval)%12 for note in row]
#####################################
def invert(row):
    """Invert row"""
    return [(12-note)%12 for note in row]
#####################################
def gen_matrix(row):
    """Generate a matrix from a row"""
    for p in row: 
        if p not in range(0, 12):
            raise ValueError("Please enter a 12 tone row")
    if len(row)!=len(set(row)):
        raise ValueError("Please enter a 12 tone row")
    # create 12-tone matrix
    if row[0]!=0:     # if first note is not 0, transpose the row so it is 0
        row = transpose(row, row[0], direction='down')

    matrix = np.zeros((12, 12))
    matrix[0,:] = row
    inverse = invert(row)

    for i, d in zip(range(1,12), inverse[1:]):
        matrix[i,:] = transpose(matrix[i-1,:], d, direction='up')
    return matrix
#####################################
def twelve_tone(prime_row, octave_weights=None, duration_weights=None, length=1, tpb=480, 
              duration='fixed', velocity = 'fixed', 
              sd=0.064, rest_probability=0.16):
    matrix = gen_matrix(prime_row)
    # create list of all possible choices
    rows = [matrix[i,:] for i in range(12)]
    inverses = [matrix[:,i] for i in range(12)]
    retrogrades = [matrix[i,::-1] for i in range(12)]
    retrograde_inverses = [matrix[::-1,i] for i in range(12)]

    choices = rows + inverses + retrogrades + retrograde_inverses

    if octave_weights is None:
        octave_weights = {octave: 1 for octave in range(0, 9)}  # set all weights to 1 if not specified
    durations = tpb*np.logspace(-5, 2, num=8, base=2) # duration of the note from 1/32 to 4
    if duration_weights is None:
        duration_weights = {duration: 1 for duration in durations}  # set all weights to 1 if not specified

    vel = 64
    sequences = []
    for _ in range(length):
        # Pick a random row from the list of choices
        row = list(random.choice(choices))
        sequence = []
        for no in row:
            # Choose a random octave between 0 and 8
            octave = int(random.choices(range(0, 9), weights=octave_weights)[0])
            # Choose a random note from the given notes with the given weights
            dur = int(random.choices(durations, weights=duration_weights)[0])
            # Check for variables
            if duration == 'variable':
                dur = int(random.normalvariate(dur, dur * sd))
            if velocity == 'variable':
                vel = int(random.normalvariate(64, 64 * sd))
            # Introduce rests with a certain probability
            if random.random() < rest_probability:
                sequence.append(Note(pitch=0, octave=0, duration=dur, velocity=0))

            sequence.append(Note(pitch=int(no), octave=octave, duration=dur, velocity=vel))
        sequences.append(sequence)

    notes = [note for seq in sequences for note in seq]      # flatten sequences
    midi_notes = []
    for n in notes:
        note_on = mido.Message('note_on', note=int(n.pitch) + (n.octave * 12), 
                               velocity=n.velocity, time=0)
        midi_notes.append(note_on)
        note_off = mido.Message('note_off', note=int(n.pitch) + (n.octave * 12), 
                                velocity=n.velocity, time=n.duration)
        midi_notes.append(note_off)

    return notes, midi_notes