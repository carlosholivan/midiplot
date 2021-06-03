import os
import setuptools 

def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as fh:
            return fh.read()
    except IOError:
        return ''

requirements = read('requirements.txt').splitlines()

setuptools.setup(name='midiplot',
      version='0.0',
      description='Python mono Wav to MIDI transcription and analysis',
      url='https://github.com/carlosholivan/midiplot',
      author='Carlos Hernandez Olivan',
      author_email='carloshero@unizar.es',
      license='Apache License, Version 2.0',
      packages=setuptools.find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: Apache Software License v2.0",
          ],
      install_requires=requirements,
      )