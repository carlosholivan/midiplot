# -*- coding: utf-8 -*-
"""
This file provides MIDI handling tools.

"""

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
import pretty_midi
             
             
class MidiProcessing:
    
    """This class presents some functions to process and extract data from a
    MIDI file with ``pretty_midi`` library.
    
    Parameters
    ----------
    midi_path : str or file
        Path or file pointer to a MIDI file.

    Attributes
    ----------
    midi_file : pretty_midi.pretty_midi.PrettyMIDI
        Pretty MIDI attribute
        
    Examples
    --------     
    >>> import wavaimidiz
    >>> midi = wavaimidiz.MidiProcessing('midi.mid')
    >>> midi.print_tracks()  
    >>> tuple = midi.get_notestuple_of_singletrack_by_nprogram(program_number=9)
    >>> tuple2 = midi.get_notestuple_of_singletrack_by_name(track_name='drums')
    """
                 
    def __init__(self, midi_path):
        
        """Initialize by taking MIDI data from a file."""
        
        if midi_path[-4:] == '.mid' or midi_path[-5:] == '.midi':
        
            self.midi_file = pretty_midi.PrettyMIDI(midi_path)
            
        else:
            raise NameError('the inserted path does not corrrespond to a .mid or .midi file.')
        
    
    def get_tracks(self):
        
        """This function stores the MIDI tracks in a tuple of 
        [track, program number, name, is_drum, notes_list].
            
        Returns
        ----------
        n_track_list : list of ints
            Numer of track in the MIDI file.
        nprogram_list : list of ints
            Numbers of the MIDI programs for each instrument.
        name_list : list of strs
            Names of the MIDI tracks.
        isdrum_list : list of bools
            Is the instrument a drum instrument (channel 9)?
        notes_list : tuple of [np.ndarray, np.ndarray, np.ndarray]
            Tuple of pitch, onsets and offsets times in seconds.
        """
        
        n_track_list = []
        nprogram_list = []
        name_list = []
        isdrum_list = []
        notes_list = []
        
        for i in range(len(self.midi_file.instruments)):
            nprogram = self.midi_file.instruments[i].program
            name = self.midi_file.instruments[i].name
            isdrum = self.midi_file.instruments[i].is_drum
            notes = self.get_notestuple_of_singletrack_by_name(name)
            
            n_track_list.append(i)
            nprogram_list.append(nprogram)
            name_list.append(name)
            isdrum_list.append(isdrum)
            notes_list.append(notes)
                
        return (n_track_list, nprogram_list, name_list, isdrum_list, notes_list)
    
    
    def print_tracks(self):
        
        """This function prints the track number, program number, track name
        and is_drum.
        """
        
        lists_tuple = self.get_tracks()
        
        for i, it in enumerate(lists_tuple[0]):
            print('Track no:', i, 
                  '| Program no:', lists_tuple[1][i], 
                  '| Track name:', lists_tuple[2][i], 
                  '| is drum:', lists_tuple[3][i])
            
        return
    
    
    def estimate_bpm(self, print_bpm=False):
    
        """This function returns the bpm estimation of a MIDI file using 
        ``pretty_midi`` library.
        
        Parameters
        ----------
        print_bpm : bool
            Prints the bpm value.
         
        Returns
        -------
        bpm : float 
            Estimated bpm of the input MIDI file.      
        """
                
        bpm = self.midi_file.estimate_tempo()
        
        if print_bpm == True:
            print('MIDI file bpm are:', bpm)
        
        return bpm   
    
    
    def get_duration(self, print_duration=False):
        
        """This function returns the duration of the MIDI file using 
        ``pretty_midi`` library.
        
        Parameters
        ----------
        print_duration : bool
            Prints the duration value in seconds.
         
        Returns
        -------
        duration : float 
            Duration in seconds of the input MIDI file.       
        """
        
        duration = self.midi_file.get_end_time()
        
        if print_duration == True:
            print('MIDI file duration in seconds is:', duration)
    
        return duration
    
    
    def cut_initial_silence(self, tuple_notes=None, select_track_by='track_name', 
                            track_n=1, program_name='drums'):
        
        """This function cuts the initial silence of a track. The initial
        silence is the silence between time 0 and the first note of the MIDI
        file taking into account all the MIDI tracks.
        
        Parameters
        ----------
        tuple_notes : tuple of [np.ndarray, np.ndarray, np.ndarray]
            Tuple of pitch, onsets and offsets times in seconds.
            If we have a tuple_notes we can cut it even if it does not belong 
            to the input MIDI file. Default ``None`` which means that a track 
            of the MIDI file will be selected to be cut.
        select_track_by : str
            ``track_name`` selects the track by its name.
            ``program_number`` selects the track by its program number.
        track_n : int
            Numer of the track to cut if select_track_by = ``program_number``.
        program_name : str
            Name of the track to cut if select_track_by = ``track_name``.    
        
        Returns
        -------
        tuples : tuple of [np.ndarray, np.ndarray, np.ndarray]
            Tuple of pitch, onsets and offsets times in seconds.      
        """
        
        
        if tuple_notes is not None:
            start_time_sec = tuple_notes[1][0]
            pitch = []
            onsets = []
            offsets = []
            for i, onset in enumerate(tuple_notes[1]):
                if (onset or tuple_notes[2][i] >= start_time_sec):
                    pitch.append(tuple_notes[0][i])
                    onsets.append(tuple_notes[1][i] - start_time_sec)
                    offsets.append(tuple_notes[2][i] - start_time_sec)
        
        else:
            if select_track_by == 'track_name':
                tuple_notes = self.get_notestuple_of_singletrack_by_name(program_name)
            
            elif select_track_by == 'program_number':
                tuple_notes = self.get_notestuple_of_singletrack_by_nprogram(track_n)
                
        
            start_time_sec = self.midi_file.estimate_beat_start()
            
            pitch = []
            onsets = []
            offsets = []
            for i, onset in enumerate(tuple_notes[1]):
                if (onset or tuple_notes[2][i] >= start_time_sec):
                    pitch.append(tuple_notes[0][i])
                    onsets.append(tuple_notes[1][i] - start_time_sec)
                    offsets.append(tuple_notes[2][i] - start_time_sec)


        tuples = lists_to_tuple(pitch, onsets, offsets)
        
        return tuples

    
    
    def get_bars(self, bpm=None, bar='4/4', print_n_bars=False):
        
        """This function calculates the total number of bars of the MIDI file
        with the total duration of the MIDI file, the bpm and the bar measure. 
        The MIDI file is not quantized so the number of bars will vary between 
        this bar values and a DAW.
        
        Parameters
        ----------
        bpm : int or float
            Beats per minute. Default ``120``.
        bar : str
            Bar measure ``2/4``, ``3/4`` or ``4/4``. Default ``4/4``.
        print_n_bars : bool
            print_time_per_bar = ``True`` prints the value of the number of 
            bars.
   
        Returns
        -------
        n_bars : float
            Total number of bars.      
        """
        
        if bpm is not None:
            
            bps = 60 / bpm
            sec_per_bar = bps * int(bar[0])
            n_bars = self.get_duration() / sec_per_bar
           
            return n_bars
        
        else:
        
            if bar == '4/4' or bar == '3/4' or bar == '2/4':
                changes_array, bpm_array = self.midi_file.get_tempo_changes()
                
                n_bars_per_change_bpm = []
                #changes are the seconds where a change of bpm occur
                # bpm are the bpm for each change
                
                changes_ant = 0
                for (changes, bpm) in zip(changes_array, bpm_array): 
                    
                    bps = 60 / bpm
                    sec_per_bar = bps * int(bar[0])
                    
                    n_bars_per_change = (changes - changes_ant) / sec_per_bar
                    n_bars_per_change_bpm.append(round(n_bars_per_change))
                    
                    changes_ant = changes
                    
                n_bars = np.ceil(sum(n_bars_per_change_bpm))
                
                change_ant = 0
                changes_bars = []
                for i, bar in enumerate(n_bars_per_change_bpm):
                    changes_bar = bar + change_ant
                    changes_bars.append(changes_bar)
                    change_ant = changes_bar
               
            else:
                ValueError: 'bar inserted is not correct.'
                
            if print_n_bars == True:
                print('MIDI file has:', n_bars, 'bars')
                
            return changes_array, bpm_array, n_bars_per_change_bpm, changes_bars, n_bars 
        
    

    def cut_midi_bars(self, start_bar, end_bar, bpm=None, tuple_notes=None, 
                      select_track_by='track_name', 
                      track_n=1, program_name='drums'):
        
        """This function cuts the duration of a track by selecting the 
        starting bar and the ending bar. The MIDI file is not quantized so
        the bars values will vary between this bar values and a DAW.
        
        Parameters
        ----------
        start_bar : int
            Desired starting bar.
        end_bar : int
            Desired ending bar.
        bpm : int or float
            Beats per minute. Default ``120``.
        tuple_notes : tuple of [np.ndarray, np.ndarray, np.ndarray]
            Tuple of pitch, onsets and offsets times in seconds.
            If we have a tuple_notes we can cut it even if it does not belong 
            to the input MIDI file. Default ``None`` which means that a track 
            of the MIDI file will be selected to be cut.
        select_track_by : str
            ``track_name`` selects the track by its name.
            ``program_number`` selects the track by its program number.
        track_n : int
            Numer of the track to cut if select_track_by = ``program_number``.
        program_name : str
            Name of the track to cut if select_track_by = ``track_name``.    
        
        Returns
        -------
        tuples : tuple of [np.ndarray, np.ndarray, np.ndarray]
            Tuple of pitch, onsets and offsets times in seconds.
        """
        
        if bpm == None:
            changes_array, bpm_array, n_bars_per_change_bpm, changes_bars, n_bars = self.get_bars()
            
        else:
            n_bars = self.get_bars(bpm)
        
        if end_bar > n_bars:
            raise ValueError('The number of bars in the MIDI file', n_bars, 'is lower than the number of bars given', end_bar)
    
        if tuple_notes is None:
            if select_track_by == 'track_name':
                tuple_notes = self.get_notestuple_of_singletrack_by_name(program_name)
            
            elif select_track_by == 'program_number':
                tuple_notes = self.get_notestuple_of_singletrack_by_nprogram(track_n)
        else:
            tuple_notes = tuple_notes
            
        # Array of all the bars one by one ordered [0, 1, 2, 3...]
        bars_array = np.arange(0, np.ceil(n_bars), 1)
        # Initialize the array of all the bpm in each bar of the bars_array
        bpm_bar_array = np.zeros(len(bars_array))
        # We loop to write the bpm_bar_array 
        change_ant = 0
        for i, change in enumerate(changes_bars):
            if i != 0:
                change = int(change)
                bpm_bar_array[change_ant:int(change)] = bpm_array[i-1]
                change_ant = change 
        
        # Array of time duration of each bar obtained with bpm value of each bar
        sec_per_bar = np.zeros(len(bars_array))
        for b, bpms in enumerate(bpm_bar_array):
                sec_per_bar[b] = (60 / bpms) * 4

        # We loop in the array of bar duration so we can cut the time according
        # to the desired starting and ending bars
        for i in enumerate(sec_per_bar):
            
            start_time_sec = np.sum(sec_per_bar[0:start_bar])
            end_time_sec = np.sum(sec_per_bar[0:end_bar])
            
            pitch = []
            onsets = []
            offsets = []
            for i, onset in enumerate(tuple_notes[1]):
                if (onset or tuple_notes[2][i] >= start_time_sec) and (onset or tuple_notes[2][i]) <= end_time_sec:
                    pitch.append(tuple_notes[0][i])
                    onsets.append(tuple_notes[1][i] - start_time_sec)
                    offsets.append(tuple_notes[2][i] - start_time_sec)
    
    
            tuples = lists_to_tuple(pitch, onsets, offsets)
        
        return tuples
  
 
    def get_notestuple_of_singletrack_by_name(self, track_name):
    
        """This function returns the tuple_notes of a single track by passing
        to it the name of the track.
        
        Parameters
        ----------         
        track_name : np.ndarray
            Name of the track.                    
                       
        Returns
        -------
        notes_tuple : tuple of [np.ndarray, np.ndarray, np.ndarray]
            Tuple of pitch, onsets and offsets times in seconds.       
        """
        
        names = []
        for i in range(len(self.midi_file.instruments)):
            names.append(self.midi_file.instruments[i].name)
            
        
        if any(name == track_name for name in names) == False:
            raise ValueError('Program name inserted is not in the MIDI file')
            
        else:
            for i in range(len(self.midi_file.instruments)):
                if self.midi_file.instruments[i].name  == track_name:
                    index = i
                    
            note_on_list = []
            note_off_list = []
            pitch_list = []
            for note in self.midi_file.instruments[index].notes:
                pitch_list.append(note.pitch)
                note_on_list.append(note.start)
                note_off_list.append(note.end)
                
            notes_tuple = lists_to_tuple(pitch_list, note_on_list, note_off_list)
            
            return notes_tuple
            
    
    
    def get_notestuple_of_singletrack_by_nprogram(self, program_number):
    
        """This function returns the tuple_notes of a single track by passing
        to it the program number.
        
        Parameters
        ----------         
        program_number : int
            Program number of the track.                    
                       
        Returns
        -------
        notes_tuple : tuple of [np.ndarray, np.ndarray, np.ndarray]
            Tuple of pitch, onsets and offsets times in seconds.       
        """
            
        for i in range(len(self.midi_file.instruments)):
            if self.midi_file.instruments[i].program  == program_number:
                index = i
                
        note_on_list = []
        note_off_list = []
        pitch_list = []
        for note in self.midi_file.instruments[index].notes:
            pitch_list.append(note.pitch)
            note_on_list.append(note.start)
            note_off_list.append(note.end)
        
        notes_tuple = lists_to_tuple(pitch_list, note_on_list, note_off_list)
            
        return notes_tuple
    
    """
    def combine_tracks(self, *args):
        
        for i, it in enumerate(args):
            tuple_combined_ant = it[0], it[1], it[2]
            
            
        
        return tuple_combined_notes
    """     
    
"""----------------------------------------------------------------"""
"""-----------------------------PLOTS------------------------------"""
"""----------------------------------------------------------------"""  

COLOR_EDGES = ['#C232FF',
               '#C232FF',
               '#89FFAE',
               '#FFFF8B',
               '#A9E3FF',
               '#FF9797',
               '#A5FFE8',
               '#FDB0F8',
               '#FFDC9C',
               '#F3A3C4',
               '#E7E7E7']


COLOR = ['#D676FF', 
         '#D676FF', 
         '#0AFE57', 
         '#FEFF00',
         '#56C8FF', 
         '#FF4C4C',
         '#4CFFD1', 
         '#FF4CF4', 
         '#FFB225', 
         '#C25581', 
         '#737D73'] 
               
               
class Pianoroll:      
    
    """This class presents a collection of functions to plot 
    MIDI tracks pianorolls.
    """
    
    def setup(self, ax, axis='time'):
        
        """This function is the setup of the axis of the pianoroll plots.
        
        Parameters
        ----------         
        ax : matplotlib.axes
            Axis.  
        axis : str
            Change axis between ``time`` to plot time in seconds in the x axis 
            or ``bar`` to plot the bars.                
        """
        
        if axis == 'time':
            plt.xlabel('time s')
        elif axis == 'bar':
            plt.xlabel('bar')
        else:
            raise ValueError('Axis must be time or bar.')
            
        plt.ylabel('Pitch')
        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.grid(linewidth=0.25)
        ax.set_facecolor('#282828')
                         
        return self
    

    def track_loop(self, notes_tuple, ax, COLOR, COLOR_EDGES, 
                   axis='time', time_1_bar=None):
    
        """This function is the loop which plots the the pianoroll of a track.
        
        Parameters
        ----------
        notes_tuple : tuple of [np.ndarray, np.ndarray, np.ndarray]
            Tuple of pitch, onsets and offsets times in seconds.  
        ax : matplotlib.axes
            Axis.
        COLOR : list
            Predefined list of colors to plot notes on the pianorolls. 
        COLOR_EDGES : list
            Predefined list of colors to plot notes borders on the pianorolls.
        axis : str
            Change axis between ``time`` to plot time in seconds in the x axis 
            or ``bar`` to plot the bars.   
        time_1_bar : float
            Time duration of 1 bar. Default ``None`` so it will be calculated
            in ``plot`` functions.
        """
        
        if axis == 'time':
            
            for p, pitch in enumerate(notes_tuple[0]):
                            
                plt.vlines(x = notes_tuple[1][p], 
                           ymin = pitch, 
                           ymax = pitch+1,
                           color=COLOR_EDGES, 
                           linewidth=0.01)
                               
                ax.add_patch(plt.Rectangle((notes_tuple[1][p], pitch), 
                                            width = notes_tuple[2][p] - notes_tuple[1][p],
                                            height = 1,
                                            alpha = 0.5,
                                            edgecolor = COLOR_EDGES,
                                            facecolor = COLOR))
                
        elif axis == 'bar':
            
            for p, pitch in enumerate(notes_tuple[0]):
                            
                plt.vlines(x = notes_tuple[1][p] / time_1_bar, 
                           ymin = pitch, 
                           ymax = pitch+1,
                           color=COLOR_EDGES, 
                           linewidth=0.01)
                               
                ax.add_patch(plt.Rectangle((notes_tuple[1][p] / time_1_bar, pitch), 
                                            width = (notes_tuple[2][p] - notes_tuple[1][p])  / time_1_bar,
                                            height = 1,
                                            alpha = 0.5,
                                            edgecolor = COLOR_EDGES,
                                            facecolor = COLOR))
                
        return 
    
    
    def plot_singletrack_pianoroll(self, notes_tuple, bpm=120, 
                                   axis='time', bar='4/4', plot_title=''):
                
        """This function plots a pianoroll of a single track.
        
        Parameters
        ----------
        notes_tuple : tuple of [np.ndarray, np.ndarray, np.ndarray]
            Tuple of pitch, onsets and offsets times in seconds.
        bpm : int or float
            Beats per minute. Default ``120``.
        axis : str
            Change axis between ``time`` to plot time in seconds in the x axis 
            or ``bar`` to plot the bars.       
        bar : str
            Bar measure ``2/4``, ``3/4`` or ``4/4``. Default ``4/4``.
        plot_title : str
            Writes a title in the pianoroll plot. Default ``''`` no title.
        """
        
        fig, ax = plt.subplots(figsize=(20, 5))
        
        if plot_title != '':
            plt.title(plot_title)
    
        if axis == 'time':
            self.setup(ax, axis)
        
            self.track_loop(notes_tuple, ax, COLOR[0], COLOR_EDGES[0])
            
        elif axis == 'bar':
            duration = notes_tuple[2][-1]
            n_bars = duration*bpm / (int(bar[0])*60)
            time_1_bar = duration / n_bars
             
            self.setup(ax, axis=axis)
            
            yint = np.arange(0, round(n_bars), 1)
            plt.yticks(yint)
        
            self.track_loop(notes_tuple, ax, COLOR[0], COLOR_EDGES[0], 
                            axis=axis, time_1_bar = time_1_bar)
            
        return 
    
    
    def overlap_multitrack_pianorolls(self, *argv, plot_title=''):
                
        """This function plots a multitrack pianoroll with each track in a 
        different color.
        
        Parameters
        ----------
        *argv: tuples of [np.ndarray, np.ndarray, np.ndarray]
            Tuples of pitch, onsets and offsets times in seconds. 
        plot_title : str
            Writes a title in the pianoroll plot. Default ``''`` no title.
        """
        
        fig, ax = plt.subplots(figsize=(20, 10))
        
        if plot_title != '':
            plt.title(plot_title)
        
        for i, arg in enumerate(argv):
            self.track_loop(arg, ax, COLOR[i+1], COLOR_EDGES[i+1])
            
        self.setup(ax)
    
        
        return
    
    
    def subplot_pianoroll(self, *args, plot_title=''):
    
        """This function plots the pinoroll of single tracks in different
        subplots.
        
        Parameters
        ----------
        *args: tuples of [np.ndarray, np.ndarray, np.ndarray]
            Tuples of pitch, onsets and offsets times in seconds. 
        plot_title : str
            Writes a title in the pianoroll plot. Default ``''`` no title.
        """ 
        
        fig, ax = plt.subplots(len(args), 1, figsize=(20, 2*len(args)))
                
        plt.subplots_adjust(hspace=0.010)

        for i, arg in enumerate(args):
            ax = fig.add_subplot(i+1, 1, i+1)
            self.track_loop(arg, ax, COLOR[i+1], COLOR_EDGES[i+1])
            
            self.setup(ax)

        return
    

def writemidtrack(notes_tuple):
        
    """This function returns a MIDI track given a notes_tuple containing the 
    pitch, the note on and note off events in seconds.
        
    Parameters
    ----------
    notes_tuple : tuple of [np.ndarray, np.ndarray, np.ndarray]
        Tuple of pitch, onsets and offsets times in seconds.
                
    Returns
    -------
    track : pretty_midi.pretty_midi.PrettyMIDI
        MIDI track of the tuple with pitch, note on and note off arrays.
    
    """
    
    track = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)
    for n, notes in enumerate(notes_tuple[0]):
        note = pretty_midi.Note(velocity = 100, 
                                pitch = notes, 
                                start = notes_tuple[1][n], 
                                end = notes_tuple[2][n])
        instrument.notes.append(note)
    track.instruments.append(instrument)
        
    return track


def savemiditrack(track, out_path, name):
    
    """This function writes a MIDI file in disk given a track, the output
    directory to save the MIDI file and the name of the MIDI file.
        
    Parameters
    ----------
    track : pretty_midi.pretty_midi.PrettyMIDI]
        MIDI track of the tuple with pitch, note on and note off arrays.      
    out_path : str
        Output directory where the MIDI file willl be stored
    name : str
        Name of the output MIDI file.
                     
    """
        
    track.write(out_path + name + '.mid')
    print(name, '.mid', 'has been saved in:', out_path)
        
    return 


def lists_to_tuple(pitch_list, note_on_list, note_off_list):
    
    """This function returns a tuple of 3 numpy arrays in a variable taking
    as inputs the pitch, note on and note off lists.
        
    Parameters
    ----------
    pitch_list : list
        List of Pitches.               
    note_on_list : list
        Note on event (or onset) in seconds for the pitches in pitch_list.
         
    note_off_list: list
        Note off event (or offset) in seconds for the pitches in pitch_list.
                       
    Returns
    -------
    notes_tuple : tuple of [np.ndarray, np.ndarray, np.ndarray]
        Tuple of pitch, onsets and offsets times in seconds.
    """
        
    pitch = np.asarray(pitch_list)
    noteon = np.asarray(note_on_list)
    noteoff = np.asarray(note_off_list)
        
    notes_tuple = (pitch, noteon, noteoff)
        
    return notes_tuple  
    
    
def note_sequence_to_tuple(note_sequence):
    
    """This function converts a note sequence in a tuple of [pitch, note on, 
    note off].
        
    Parameters
    ----------
    note_sequence : list
        Note sequence containing the pitch, note on, note off, velocity and the
        instrument of a track.
                           
    Returns
    -------
    notes_tuple : tuple of [np.ndarray, np.ndarray, np.ndarray]
        Tuple of pitch, onsets and offsets times in seconds.
    """
    
    pitch_list = []
    note_on_list = []
    note_off_list = []
    
    for i in range(len(note_sequence.notes)):
        pitch = note_sequence.notes[i].pitch
        note_on = note_sequence.notes[i].start_time
        note_off = note_sequence.notes[i].end_time
        
        pitch_list.append(pitch)
        note_on_list.append(note_on)
        note_off_list.append(note_off)
        
    return lists_to_tuple(pitch_list, note_on_list, note_off_list)

    