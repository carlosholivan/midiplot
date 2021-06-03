"""
``midipianorolls`` contains utility function/classes for handling MIDI data.
If you end up using ``midipianorolls`` in a published research project, please
cite the following report:
    
    
Example usage for extracting MIDI data and plotting:
    
.. code-block:: python
        
    import midipianorolls
    # Load MIDI file into MidiProcessing object
    midi = midipianorolls.MidiProcessing('midi.mid')
    # Print tracks of the MIDI file
    midi.print_tracks()
    # Get the notes_tuple a single track by its program number:
    tuple1 = midi.get_notestuple_of_singletrack_by_nprogram(program_number=9)
    # Get the notes_tuple a single track by its track name:
    tuple2 = midi.get_notestuple_of_singletrack_by_name(track_name='drums')
    # Plot the pianoroll of one tuple:
    midipianorolls.Pianoroll.plot_singletrack_pianoroll(tuple1)
    # Plot the pianoroll of both tuples overlapped:
    midipianorolls.Pianoroll.overlap_multitrack_pianorolls(tuple1, tuple2) 
    # Plot the pianoroll of both tuples in different subplots:
    midipianorolls.Pianoroll.subplot_pianoroll(tuple1, tuple2) 
    # Cut the MIDI track by setting the starting and ending bars values:
    cut_tuple = midipianorolls.cut_midi_bars(2, 6, tuple_notes=tuple1)
    # Write a MIDI track from the tuple:
    midipianorolls.writemidtrack(cut_tuple)
    # Save the MIDI track in disk:
    midipianorolls.savemiditrack(cut_tuple, 'your/output/path', 'track_midi_name')
        
    
Tutorials can be found in the source tree's `examples directory
<https://github.com/carlosholivan/midi-pianorolls/tree/master/tutorials>`_.


``midipianorolls.MidiProcessing``
==========================

.. autoclass:: MidiProcessing
   :members:
   :undoc-members:
       
       
Utility functions
=================
.. autofunction:: writemidtrack
.. autofunction:: savemiditrack

"""

from .midiprocessing import *

__version__ = '0.0'