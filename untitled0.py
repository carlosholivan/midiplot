# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 10:40:00 2021

@author: Carlos
"""

import sys
sys.path.append('.')
from midiplot import midiprocessing

midi_infile = 'H:\\GitHub\\midi-pianorolls\\example\\midi_file.mid'

m_gt = midiprocessing.MidiProcessing(midi_infile)

all_tracks = m_gt.get_tracks()
m_gt.print_tracks()

track = m_gt.get_notestuple_of_singletrack_by_name("11_33_PAD")
data = m_gt.get_all_tracks()

plots = midiprocessing.Pianoroll()
plots.plot_all_tracks(data)

#plots.plot_singletrack_pianoroll(track)

#gt_matrix = m_gt.get_notestuple_of_singletrack_by_name('Voice')
#gt_track = midiprocessing.writemidtrack(gt_matrix)