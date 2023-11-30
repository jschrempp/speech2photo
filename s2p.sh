#!./bin/bash
# script to make running the speech2picture program easier
#
# Also could be called by s2p.desktop shortcut
#
# On RPi if using hardware button always, then modify the last line
# to have the -g command line option instead of -o
cd ~
pwd
# the OPENAI_API_KEY is initialized in .bashrc
# see comments at the top of pyspeech.py
source ~/.bashrc
cd speech2picture
source /home/jbs/speech2picture/.venv/bin/activate
python pyspeech.py -o