# Python code to record audio from the default microphone and then transcribe it using OpenAI
# Then summarize the transcript and generate a picture based on the summary
# Then open the picture in a browser
# Then delay for 60 seconds
# Then repeat the process
# Author: Jim Schrempp 2023 

# To run:  python3 pyspeech.py
# control-c to stop the program or it will end after loopsMax loops about (duration + delay)*loopsMax seconds

# To run this you need to get an OpenAI API key and put it in a file called "creepy photo secret key"

# import the libraries
import sounddevice
import soundfile
import sys
import getopt
# import parser
import argparse
import webbrowser
import time
import os
import openai
from enum import Enum

class processStep(Enum):
    RecordAudio = 1
    TranscribeAudio = 2
    SummarizeTranscript = 3
    ExtractKeywords = 4
    GenerateImage = 5
    DisplayImage = 6
    CleanUp = 7

# ----------------------
# record duration seconds of audio from the default microphone to a file and return the sound file name
def recordAudioFromMicrophone():
    # delete file recording.wav if it exists
    try:
        os.remove("recording.wav")
    except:
        # do nothing
        pass # do nothing   

    # print the devices
    # print(sd.query_devices())

    # Set the sample rate and number of channels for the recording
    sample_rate = int(sounddevice.query_devices(1)['default_samplerate'])
    channels = 1

    if debugOn:
        # echo the sample rate and channels
        print(sample_rate)
        print(channels)

    print("Recording...")
    # Record audio from the default microphone
    recording = sounddevice.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)

    # Wait for the recording to finish
    sounddevice.wait()

    # Save the recording to a WAV file
    soundfile.write('recording.wav', recording, sample_rate)

    soundFileName = 'recording.wav'

    return soundFileName


# ----------------------
# main program starts here

openai.api_key_path = 'creepy photo secret key'


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--savefiles", help="save the files", action="store_true") # optional argument
parser.add_argument("-d", "--debug", help="extra information printed to the console", default=0) # optional argument
parser.add_argument("-w", "--wav", help="do only one pass using the named wav file", type=str, default=0) # optional argument
parser.add_argument("-t", "--text", help="do only one pass using the named text file as the transcript", type=str, default=0) # optional argument
parser.add_argument("-T", "--Summary", help="do only one pass using the named text file as the Summary", type=str, default=0) # optional argument
args = parser.parse_args()

debugOn = args.debug

# if we're given a file then start at that step
# check in order so that processStartStep will be the maximum value
processStartStep = processStep.RecordAudio

argWAVFile = args.wav
if argWAVFile != 0: processStartStep = processStep.TranscribeAudio

argTranscriptFile = args.text
if argTranscriptFile != 0: processStartStep = processStep.SummarizeTranscript

argSummaryFile = args.Summary
if argSummaryFile != 0: processStartStep = processStep.ExtractKeywords

if processStartStep > processStep.RecordAudio:
    loopsMax = 1
else:
    loopsMax = 10  # number of times to loop  

# Set the duration of each recording in seconds
duration = 240

# Once a recording and display is completed, wait this many seconds before starting the next recording
loopDelay = 120

# ----------------------
# Main Loop for recording, transcribing, and displaying
loopcount = 0
while loopcount < loopsMax:
    loopcount += 1

    # do we need to record audio?
    if processStartStep == processStep.RecordAudio:
       
       soundFileName = recordAudioFromMicrophone()

    else:
        if processStartStep == processStep.TranscribeAudio:
            # use the wav file specified by the wav argument
            soundFileName = str(argWAVFile)
            print("Using wav file: " + soundFileName)

    # do we need to transcribe the audio?
    if processStartStep == processStep.TranscribeAudio:
        # transcribe the recording
        # Note: you need to be using OpenAI Python v0.27.0 for the code below to work
        print("Transcribing...")
        audio_file= open(argWAVFile, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

        # print the transcript
        #print("transcript: ")
        print(transcript)

    else:
        if processStartStep == processStep.SummarizeTranscript:
            # use the text file specified by the text argument
            transcriptFile = open(argTranscriptFile, "r")
            # read the transcript file
            transcript = transcriptFile.read()
            print("Using transcript file: " + argTranscriptFile)

    # do we need to summarize the transcript?
    if processStartStep == processStep.SummarizeTranscript:
        #summary= transcript["text"] // comment out the summarize step and use the transcript as the summary for testing
        # summarize the transcript 
        print("Summarizing...")
        responseSummary = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content" : 
                f"Please summarize the following text:\n{transcript}" }
            ]              
            
        )

        if debugOn: 
            # print the response
            print("responseSummary: ")
            print(responseSummary)

        summary = responseSummary['choices'][0]['message']['content'].strip()

        # print the summary
        print("summary: ")
        print(summary)
    
    else:
        summaryFile = open(argSummaryFile, "r")
        # read the summary file
        summary = summaryFile.read()

   # extracting key nouns and verbs
    print("extracting...")
    responseForImage = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content" : 
            f"What are 5 most significant nouns and verbs in the following text:\n{summary}" }
        ]              
        
    )

    if debugOn:
        print("responseForImage: ")
        print(responseForImage)

    # extract the nouns and verbs
    nounsAndVerbs = responseForImage['choices'][0]['message']['content'].strip() 
    if debugOn:
        print("nounsAndVerbs: ")
        print(nounsAndVerbs)

    # use openai to generate a picture based on the summary
    responseSummary = openai.Image.create(
    prompt= summary,
    n=1,
    size="512x512"
    )
    image_url = responseSummary['data'][0]['url']

    # open a url in the browser
    webbrowser.open(image_url)
    #print(image_url)

    # if savefiles is true then save the files
    if args.savefiles:

        # format a time string to use as a file name
        timestr = time.strftime("%Y%m%d-%H%M%S")

        if argWAVFile == 0:
            # save the audio file
            os.rename("recording.wav", timestr + "-recording" + ".wav")
    
        if argTranscriptFile == 0:
            # save the transcript
            f = open(timestr + "-rawtranscript" + ".txt", "w")
            f.write(transcript["text"])
            f.close()

        # save the summary
        f = open(timestr + "-summary" + ".txt", "w")
        f.write(summary)
        f.close()

        # save the transcript
        f = open(timestr + "-rawtranscript" + ".txt", "w")
        f.write(transcript["text"])
        f.close()

    #delay
    print("delaying...")
    time.sleep(loopDelay)




# exit the program
exit()





