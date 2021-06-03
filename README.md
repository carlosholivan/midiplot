![](logo.png)

A python library for monophonic wav to MIDI conversion and analysis with MIDI and wav handling tools.

beta.0 (June 2021) version

## Documentation

See documentation [here](https://carlosholivan.github.io/softwares/midiplot.html)

## Features

* MIDI processing with pretty_midi library.

```
Track no: 0 | Program no: 0 | Track name: 02_03_KICK | is drum: False
Track no: 1 | Program no: 0 | Track name: 03_03_SNARE | is drum: False
Track no: 2 | Program no: 0 | Track name: 04_03_HIHAT | is drum: False
Track no: 3 | Program no: 0 | Track name: 09_XX_BASS | is drum: False
Track no: 4 | Program no: 0 | Track name: 10_20_CHORDS - GRAND PIANO | is drum: False
Track no: 5 | Program no: 0 | Track name: 11_33_PAD | is drum: False
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
cd .path/to/midiplot
python setup.py install
```

## Authors

[**Carlos Hernández**](https://carlosholivan.github.io/index.html) - carloshero@unizar.es

Department of Electronic Engineering and Communications, Universidad de Zaragoza, Calle María de Luna 3, 50018 Zaragoza
