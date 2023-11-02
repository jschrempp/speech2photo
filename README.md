# speech2picture
Use your voice and OpenAI to make new art. Or, monitor an ongoing conversation
and have the picture frame change to reflect the conversation - an
eveasdropping picture frame!

A full write up: https://www.jimschrempp.com/features/computer/speech_to_picture.htm

Based on the WhisperFrame project idea on Hackaday.  
https://hackaday.com/2023/09/22/whisperframe-depicts-the-art-of-conversation/

- Python code to record audio from the default microphone and 
- transcribe it using OpenAI
- summarize the transcript 
- generate 4 pictures based on the summary and combine them into one
- open the picture
- delay for 60 seconds
- repeat the process 10 times

Runs on Mac OSX and Raspberry Pi. RPi has the option to trigger the process with a button.
See the header comments for how to set up your Python environment.

Author: Jim Schrempp 2023 

To run:  python3 pyspeech.py

- control-c to stop the program or it will end after loopsMax loops about (duration + delay)*loopsMax seconds
- control-h to see all command line options

Useful options:

-d [0,1,2] Level 0 has progress messages. Level 1 lists returns from OpenAI. Level 2 is a trace.

-s Save all the intermediate files in the history/ folder (images are saved in all cases)

-o Only Keywords ... The audio transcript is passed directly to the image generation service
   without any interpretation. Useful mostly for 10 second audio recording to let people speak
   a few words and get a picture from it. 

Command line options exist to let you pass in an existing file to one of the steps. For instance, if you want to experiment with how the final image files are displayed, -i <filename> will jump right to that step so you don't have to do all the previous steps.

To run this you need to get an OpenAI API key and put it in a file called "creepy photo secret key"
