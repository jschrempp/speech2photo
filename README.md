# speech2picture
Use your voice and OpenAI to make new art. Or, monitor an ongoing conversation
and have the picture frame change to reflect the conversation - an
eveasdropping picture frame!

A video of this project in action: https://www.youtube.com/watch?v=Wzuj7Vhyl8w

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

Runs on Mac OSX and Raspberry Pi. RPi has the option to trigger the process with a button. Includes
"kiosk" mode so the RPi will boot into a running session, ready for a button press.

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

-h Hardware ... Goes into a loop waiting for a button to be pressed (a pin to be pulled low)

-g Goes into Kiosk mode, useful for autostart installations

Command line options exist to let you pass in an existing file to one of the steps. For instance, if you want to experiment with how the final image files are displayed, -i <filename> will jump right to that step so you don't have to do all the previous steps.

Typical execution:
   python3 pyspeech.py -o

To run this you need to get an OpenAI API key and put it into an environment variable OPENAI_API_KEY. See more
details in the comments at the top of the source file.

Kiosk hardware set up
https://github.com/jschrempp/speech2picture/wiki

NOTE: With the Jan 8, 2024 commit there has been a significant change. We have found that OpenAI can 
occasionally create offensive images. For that reason we have changed how the idle display of images
works. Random images are now displayed from the ./idleDisplayFiles folder. New images are automatically
saved in the ./history folder. As a result, new images will not be in the idle display rotation. We 
suggest that you periodically review the files in the ./history folder and move acceptable images into
the ./idleDisplayFiles folder.

We suggest that you periodically look at the new files, remove any offensive ones, and add them to the 
list of files for idle display. To do this remotely:

1.   mkdir temp
2.   cd temp
3.   scp -r <user>@<ip address>:~/speech2picture/history .
4.   examine the files you just downloaded and remove any you have concerns about
5.   scp -r . <user>@<ip address>:~/speech2picture/idleDisplayFiles
