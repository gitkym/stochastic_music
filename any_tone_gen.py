import mido
import random
import numpy as np

class Note:
    def __init__(self, pitch, octave, duration, velocity):
        self.pitch = int(pitch)
        self.octave = int(octave)
        self.duration = int(duration)
        self.velocity = int(velocity)
####################################
def transpose(row, interval, direction='up'):
    '''modify transpose function to work with any row'''
    if direction == 'up':
        # Shift each element up in the row by the number of movements specified by the interval
        transposed_row = np.roll(row, interval)
    else:
        # Shift each element down in the row by the number of movements specified by the interval
        transposed_row = np.roll(row, -interval)
    return transposed_row
def invert(row):
    '''modify invert function to work with any row'''
    # first and middle note are the same, rest are mapped
    forward = [r for r in set(row)]
    forward = forward + [forward[0]]
    backward = reversed(forward)
    mapping = dict(zip(forward, backward))
    return [mapping[note] for note in row]
####################################
class TwelveTone:
    def __init__(self, prime_row):
        self.prime_row = prime_row
        self.matrix = self.gen_matrix(prime_row)
        self.choices = self.create_choices()

    def gen_matrix(self, row):
        r = len(row)
        """Generate a matrix from a row"""
        if r!=len(set(row)):
            raise ValueError("Please enter a tone row")
        # create tone matrix
        # if row[0]!=0:     # if first note is not 0, transpose the row so it is 0
        #     row = transpose(row, row[0], direction='down')

        matrix = np.zeros((r, r))
        matrix[0,:] = row
        matrix[:,0] = invert(row)

        for i in range(1, r):
            position = row.index(matrix[i,0])
            matrix[i,:] = transpose(row, position, direction='down')

        return matrix

    def create_choices(self):
        r = len(self.prime_row)
        rows = [self.matrix[i,:] for i in range(r)]
        inverses = [self.matrix[:,i] for i in range(r)]
        retrogrades = [self.matrix[i,::-1] for i in range(r)]
        retrograde_inverses = [self.matrix[::-1,i] for i in range(r)]

        choices = rows + inverses + retrogrades + retrograde_inverses
        # check if any note in not in original row
        for row in choices:
           for note in row:
              if note not in self.prime_row:
                 raise ValueError("Please enter a tone row")               
        return choices
        
    def generator(self, octave_weights=None, duration_weights=None, length=1, tpb=480, 
                           duration='fixed', velocity='fixed', sd=0.064, rest_probability=0.16):
        if octave_weights is None:
            octave_weights = {octave: 1 for octave in range(0, 9)}
        durations = tpb*np.logspace(-5, 2, num=8, base=2) # duration of the note from 1/32 to 4
        if duration_weights is None:
            duration_weights = {duration: 1 for duration in durations}
        
        vel = 64
        sequences = []
        for _ in range(length):
            # Pick a random row from the list of choices
            row = list(random.choice(self.choices))
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
                    if vel>127:     # velocity cannot be greater than 127
                        vel = 127
                    if vel<0:
                        vel = 0
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
