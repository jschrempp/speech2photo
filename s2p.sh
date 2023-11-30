# script to make running the speech2picture program easier
# will be called by the autostart desktop file
#
#!./bin/bash
cd ~
pwd
# OPENAI_API_KEY is in .bashrc
source ~/.bashrc
cd speech2picture
source /home/jbs/speech2picture/.venv/bin/activate
python pyspeech.py -o