![](images/logo.png)

A python library for monophonic wav to MIDI conversion and analysis with MIDI and wav handling tools.

beta.0 (June 2020) version

## Documentation

See documentation [here](https://carlosholivan.github.io/softwares/wavaimidiz/html/wavaimidiz.html)

## Features

* MIDI processing with pretty_midi library.

```
Track no: 0 | Program no: 65 | Track name: MELODY SZA | is drum: False  
Track no: 1 | Program no: 65 | Track name: MELODY KL | is drum: False 
Track no: 2 | Program no: 66 | Track name: MELODY 1 | is drum: False
Track no: 3 | Program no: 88 | Track name: NEW AGE | is drum: False
Track no: 4 | Program no: 48 | Track name: STRINGS | is drum: False
Track no: 5 | Program no: 89 | Track name: WARM PAD | is drum: False
Track no: 6 | Program no: 50 | Track name: SYN STRINGS 1 | is drum: False
Track no: 7 | Program no: 90 | Track name: POLYSYNTH | is drum: False
Track no: 8 | Program no: 35 | Track name: FRETLESS | is drum: False
Track no: 9 | Program no: 0 | Track name: DRUMS | is drum: True
Track no: 10 | Program no: 102 | Track name: ECHOES | is drum: False
Track no: 11 | Program no: 4 | Track name: E. PIANO 1 | is drum: False
Track no: 12 | Program no: 27 | Track name: CLEAN GTR | is drum: False
Track no: 13 | Program no: 95 | Track name: SWEEP PAD | is drum: False
Track no: 14 | Program no: 92 | Track name: BOWED | is drum: False
```

* Pianoroll representations of single tracks or multitracks in one or different subplots.

![](images/pianoroll.png)

* Wav to MIDI transcription with a tracking algorithm based on the pitch estimated by Crepe neural network.


## Dependencies

* [Numpy](https://numpy.org/)
* [Matplotlib](https://matplotlib.org/)
* [pretty_midi](https://github.com/craffel/pretty-midi)
* [plotly](https://plotly.com/)

## Installation

```
cd .path/to/wavAImidiZ
python setup.py install
```

## Authors

[**Carlos Hernández**](https://carlosholivan.github.io/index.html) - carloshero@unizar.es

Department of Electronic Engineering and Communications, Universidad de Zaragoza, Calle María de Luna 3, 50018 Zaragoza
