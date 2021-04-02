
import sys
sys.path.insert(0, 'H:\\INVESTIGACION\\Proyectos\\AIBeatz\\wavAImidiZ\\wavaimidiz\\')
import transcription_metrics, crepe_processing, midiprocessing

path = 'H:\\INVESTIGACION\\Proyectos\\AIBeatz\\datasets\\Training dataset 01\\Rap\\All the stars (kendrick lamar)\\all the stars with sza.mid'
m = midiprocessing.MidiProcessing(path)

#Obtaining the number of bars by substracting automatically bpm changes in the MIDI file
changes_array, bpm_array, n_bars_per_change_bpm, changes_bars, n_bars = m.get_bars()

#Obtaining the number of bars by setting a constant bpm
n_bars2 = m.get_bars(97)


bars_array = array = np.arange(0, np.ceil(n_bars), 1)
bpm_bar_array = np.zeros(len(bars_array))
change_ant = 0
for i, change in enumerate(changes_bars):
    if i != 0:
        change = int(change)
        bpm_bar_array[change_ant:int(change)] = bpm_array[i-1]
        change_ant = change 

sec_per_bar = np.zeros(len(bars_array))
for b, bpms in enumerate(bpm_bar_array):
    sec_per_bar[b] = (60 / bpms) * 4