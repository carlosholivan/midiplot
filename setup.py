import os
import setuptools 

def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as fh:
            return fh.read()
    except IOError:
        return ''

requirements = read('requirements.txt').splitlines()

classifiers = ['Development Status :: 0 - Beta',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3.5',
               'Programming Language :: Python :: 3.6',
               'Programming Language :: Python :: 3.7',
               'License :: Free for non-commercial use',
               'Topic :: Multimedia :: Sound/Audio :: Analysis']
			   
setuptools.setup(name='midiplot',
      version='0.0-beta',
      description='Python MIDI plotting and analysis',
      url='https://github.com/carlosholivan/midiplot',
      author='Carlos Hernandez Olivan',
      author_email='carloshero@unizar.es',
      license='https://github.com/carlosholivan/midiplot',
      packages=setuptools.find_packages(),
	  exclude_package_data={'': ['tests', 'docs']},
      install_requires=requirements,
	  classifiers=classifiers
      )