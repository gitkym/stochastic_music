def default_scale(notes):
    '''Returns a scale with the given notes and default weights.'''
    return {
        'notes': notes,
        'pitch_weights': [1] * len(notes),
        'octave_weights': [1] * len(notes),
        'duration_weights': [1] * len(notes)
    }
# Scales
chromatic = default_scale([0,1,2,3,4,5,6,7,8,9,10,11])
major = default_scale([0,2,4,5,7,9,11])
minor_natural = default_scale([0,2,3,5,7,8,10])
minor_harmonic = default_scale([0,2,3,5,7,8,11])
whole_tone = default_scale([0,2,4,6,8,10])
full_dim = default_scale([0,2,3,5,6,8,10,11])
half_dim = default_scale([0,1,3,4,6,7,9,10])
major_pentatonic = default_scale([0,2,4,7,9])
minor_pentatonic = default_scale([0,3,5,7,10])
major_blues = default_scale([0,3,4,5,7,10])
minor_blues = default_scale([0,3,5,6,7,10])
japanese = default_scale([0,1,5,7,10])
# Arpeggios
major_arpeggio = default_scale([0,4,7])
major_7_arpeggio = default_scale([0,4,7,11])
major_9_arpeggio = default_scale([0,4,7,11,2])
major_11_arpeggio = default_scale([0,4,7,11,2,5])
major_13_arpeggio = default_scale([0,4,7,11,2,5,9])
minor_arpeggio = default_scale([0,3,7])
minor_7_arpeggio = default_scale([0,3,7,10])
minor_9_arpeggio = default_scale([0,3,7,10,2])
minor_11_arpeggio = default_scale([0,3,7,10,2,5])
minor_13_arpeggio = default_scale([0,3,7,10,2,5,9])
dim_arpeggio = default_scale([0,3,6])
dim_7_arpeggio = default_scale([0,3,6,9])
aug_arpeggio = default_scale([0,4,8])
aug_7_arpeggio = default_scale([0,4,8,10])
sus2_arpeggio = default_scale([0,2,7])
sus4_arpeggio = default_scale([0,5,7])
sus2_7_arpeggio = default_scale([0,2,7,10])
sus4_7_arpeggio = default_scale([0,5,7,10])
dom_7_arpeggio = default_scale([0,4,7,10])
dom_9_arpeggio = default_scale([0,4,7,10,2])
dom_11_arpeggio = default_scale([0,4,7,10,2,5])
dom_13_arpeggio = default_scale([0,4,7,10,2,5,9])
dom_7_sharp_9_arpeggio = default_scale([0,4,7,10,3])
dom_7_flat_9_arpeggio = default_scale([0,4,7,10,1])
dom_7_sharp_5_arpeggio = default_scale([0,4,8,10])
dom_7_flat_5_arpeggio = default_scale([0,4,6,10])
dom_7_sharp_5_sharp_9_arpeggio = default_scale([0,4,8,10,3])
dom_7_sharp_5_flat_9_arpeggio = default_scale([0,4,8,10,1])
dom_7_flat_5_sharp_9_arpeggio = default_scale([0,4,6,10,3])
dom_7_flat_5_flat_9_arpeggio = default_scale([0,4,6,10,1])
dom_7_sharp_11_arpeggio = default_scale([0,4,7,10,5])
dom_7_flat_11_arpeggio = default_scale([0,4,7,10,4])

