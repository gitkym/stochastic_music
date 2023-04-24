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
    if direction == 'up':
        return [(note+interval)%12 for note in row]
    else:
        return [(note-interval)%12 for note in row]
def invert(row):
    return [(12-note)%12 for note in row]
####################################
def create_chord(row, max_chord_size=5):
    """Create a chord from a row"""         # add condition to ignore rests ??
    chord_size = random.randint(2, max_chord_size)      # use (1, max) ??
    first = random.choice(row)
    start = row.index(first)
    if start+chord_size > len(row):
         chord = row[start:] + row[:chord_size-(len(row)-start)]
         new = row[chord_size-(len(row)-start):start] + [chord]
    else:
        chord = row[start:start+chord_size]
        new = row.copy()
        new[start:start+chord_size] = [chord]
    return new
def create_chord_2(row, max_chord_size=5, chord_prob=0.2):
    chord = []
    chord_size = 0
    new = []
    for note in row:        # add condition to ignore rests ??
        if random.random() < chord_prob:
            chord.append(note)
            chord_size += 1
            if chord_size == max_chord_size:
                row[row.index(note)] = chord
                chord = []
                chord_size = 0
        else:
            if chord_size > 1:
                row[row.index(note)] = chord
                chord = []
                chord_size = 0
    return row
####################################
def create_midi(events):
    midi_events = []
    for event in events:
        if isinstance(event, Note):     # includes notes and rests
            note_on = mido.Message('note_on', note=event.pitch+12*event.octave, velocity=event.velocity, time=0)
            midi_events.append(note_on)
            note_off = mido.Message('note_off', note=event.pitch+12*event.octave, velocity=event.velocity, time=event.duration)
            midi_events.append(note_off)
        else:
            for note in event:      # event is a chord
                note_on = mido.Message('note_on', note=note.pitch+12*note.octave, velocity=note.velocity, time=0)
                midi_events.append(note_on)
            for note in event:
                note_off = mido.Message('note_off', note=note.pitch+12*note.octave, velocity=note.velocity, time=note.duration)
                midi_events.append(note_off)
    return midi_events
####################################
class TwelveTone:
    def __init__(self, prime_row):
        self.prime_row = prime_row
        self.matrix = self.gen_matrix(prime_row)
        self.choices = self.create_choices()

    def gen_matrix(self, row):
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
        matrix[:,0] = inverse

        for i, d in zip(range(1,12), inverse[1:]):
            matrix[i,1:] = transpose(matrix[0,1:], d, direction='up')
        return matrix

    def create_choices(self):
        rows = [self.matrix[i,:] for i in range(12)]
        inverses = [self.matrix[:,i] for i in range(12)]
        retrogrades = [self.matrix[i,::-1] for i in range(12)]
        retrograde_inverses = [self.matrix[::-1,i] for i in range(12)]

        choices = rows + inverses + retrogrades + retrograde_inverses
        # ensure choices are unique otherwise raise error
        for row in choices:
            if len(row)!=len(set(row)):
                raise ValueError("Please enter a 12 tone row")
        return choices
    
    def generator(self, octave_weights=None, duration_weights=None, length=1, tpb=480,
                           duration='fixed', velocity='fixed', dur_sd=0.064, vel_sd=0.064, 
                           rest_probability=0.16, chord_probability=0.6, max_chord_size=5):
        """Generate a sequence of notes from the 12 tone matrix"""
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
                    dur = int(random.normalvariate(dur, dur * dur_sd))
                if velocity == 'variable':
                    vel = int(random.normalvariate(64, 64 * vel_sd))
                    if vel>127:     # velocity cannot be greater than 127
                        vel = 127
                    if vel<0:
                        vel = 0
                
                # sequence.append(Note(pitch=int(no), octave=octave, duration=dur, velocity=vel))
                # Introduce rests with a certain probability
                if rest_probability > 0 and  random.random() < rest_probability:
                    sequence.append(Note(pitch=0, octave=0, duration=dur, velocity=0))

                sequence.append(Note(pitch=int(no), octave=octave, duration=dur, velocity=vel))
            
            if chord_probability > 0 and random.random() < chord_probability:
                sequence = create_chord(sequence, max_chord_size=max_chord_size)
            sequences.append(sequence)

        events = [event for seq in sequences for event in seq]      # flatten sequences
        return events    
