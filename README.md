# speech2picture
Based on the WhisperFrame project idea on Hackaday. 

Python code to record audio from the default microphone and then transcribe it using OpenAI
Then summarize the transcript and generate a picture based on the summary
Then open the picture in a browser
Then delay for 60 seconds
Then repeat the process
Author: Jim Schrempp 2023 

To run:  python3 pyspeech.py
control-c to stop the program or it will end after loopsMax loops about (duration + delay)*loopsMax seconds

To run this you need to get an OpenAI API key and put it in a file called "creepy photo secret key"
