#!/bin/bash
# EDIT THIS FILE TO REPLACE {your user} 
#
# script to make running the speech2picture program easier
#
# On RPi if using hardware button always, then modify the last line
# to have the -g command line option instead of -o
cd ~
pwd
# the OPENAI_API_KEY is initialized in .bashrc
# see comments at the top of pyspeech.py
source ~/.bashrc
cd speech2picture
source /home/{your user}/speech2picture/.venv/bin/activate
python pyspeech.py -o