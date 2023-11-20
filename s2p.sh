# script to make running the speech2picture program easier
# will be called by the autostart desktop file
#
cd ~
pwd
source ~/.bashrc
source /home/jbs/.venv/bin/activate
cd speech2picture
python pyspeech.py -o