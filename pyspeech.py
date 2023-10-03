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
    Audio = 1
    Transcribe = 2
    Summarize = 3
    Keywords = 4
    Image = 5
    Display = 6
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




def getTranscript(trascripitFileArg, wavFileName):
    
    if trascripitFileArg == 0:

        # transcribe the recording
        # Note: you need to be using OpenAI Python v0.27.0 for the code below to work
        print("Transcribing...")
        audio_file= open(wavFileName, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

        # print the transcript
        print("transcript: ")
        print(transcript)

    else:
        # use the text file specified 
        transcriptFile = open(trascripitFileArg, "r")
        # read the transcript file
        transcript = transcriptFile.read()
        print("Using transcript file: " + trascripitFileArg)

    return transcript

def getSummary(summaryArg, transcript):
    
    if summaryArg == 0:
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
        # use the text file specified by the transcript argument
        summaryFile = open(summaryArg, "r")
        # read the summary file
        summary = summaryFile.read()
        print("Using summary file: " + summaryArg)

    return summary

def getKeywords(extractArg, summary):

    if extractArg == 0:
        # extract the keywords from the summary

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

    else:
        # use the extract file specified by the extract argument
        summaryFile = open(extractArg, "r")
        # read the summary file
        summary = summaryFile.read()
        print("Using extract file: " + extractArg)


    return nounsAndVerbs


def getImageURL(imageArg, keywords):

    if imageArg == 0:
        # use the keywords to generate an image
        print("Generating image...")
        responseImage = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content" : 
                f"Generate an image of a {keywords}." }
            ]              
            
        )

        if debugOn:
            print("responseImage: ")
            print(responseImage)

        # extract the image url
        imageURL = responseImage['choices'][0]['message']['content'].strip() 
        if debugOn:
            print("imageURL: ")
            print(imageURL)

        # use openai to generate a picture based on the summary
        responseSummary = openai.Image.create(
            prompt= summary,
            n=1,
            size="512x512"
            )
        
        image_url = responseSummary['data'][0]['url']
        #print(image_url)

    else:
        image_url = imageArg
        print("Using image file: " + imageArg)

    return image_url

def saveTheFiles():
    """
    # format a time string to use as a file name
    timestr = time.strftime("%Y%m%d-%H%M%S")

    if firstProcessStep == processStep.Display:
        return # don't save files if we're only displaying
    
    if firstProcessStep == processStep.Image:
        # save the image
        #os.rename("image.png", timestr + "-image" + ".png")
    
    if firstProcessStep == processStep.Keywords:
        # save the extract
        f = open(timestr + "-extract" + ".txt", "w")
        f.write(keywords)
        f.close()

    if firstProcessStep == processStep.Audio:
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
    """


# ----------------------
# main program starts here

openai.api_key_path = 'creepy photo secret key'


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--savefiles", help="save the files", action="store_true") # optional argument
parser.add_argument("-d", "--debug", help="extra information printed to the console", default=0) # optional argument
parser.add_argument("-w", "--wav", help="use audio from file", type=str, default=0) # optional argument
parser.add_argument("-t", "--transcript", help="use transcript from file", type=str, default=0) # optional argument
parser.add_argument("-T", "--summary", help="use summary from file", type=str, default=0) # optional argument
parser.add_argument("-e", "--extract", help="use extract from file", type=str, default=0) # optional argument
parser.add_argument("-i", "--image", help="use image from file", type=str, default=0) # optional argument

args = parser.parse_args()

debugOn = args.debug

# if we're given a file then start at that step
# check in order so that processStartStep will be the maximum value

if args.display != 0: 
    firstProcessStep = processStep.Display  
elif args.image != 0: 
    firstProcessStep = processStep.Image
elif args.extract != 0: 
    firstProcessStep = processStep.Keywords
elif args.summary != 0: 
    firstProcessStep = processStep.Summarize
elif args.transcript != 0: 
    firstProcessStep  = processStep.Transcribe
elif args.wav != 0: 
    firstProcessStep = processStep.Audio


if firstProcessStep > processStep.RecordAudio:
    loopsMax = 1
else:
    loopsMax = 10  # only loop if we're recording new audio each time

# Set the duration of each recording in seconds
duration = 240

# Once a recording and display is completed, wait this many seconds before starting the next recording
loopDelay = 120

# ----------------------
# Main Loop for recording, transcribing, and displaying
loopcount = 0
while loopcount < loopsMax:
    loopcount += 1

    # Audio
    if firstProcessStep == processStep.Audio:
       
        if args.wav == 0:
            soundFileName = recordAudioFromMicrophone() # might take a long time if we are recording new audio
        else:
            soundFileName = args.wav # use the file specified by the wav argument
           
    # Transcribe
    if firstProcessStep <= processStep.Transcribe:
    
        transcript = getTranscript(args.transcript, soundFileName)

    # Summary
    if firstProcessStep <= processStep.SummarizeTranscript:

        summary = getSummary(args.summary, transcript)

    # Keywords    
    if firstProcessStep <= processStep.Keywords:

        keywords = getKeywords(args.extract, summary)

    # Image
    if firstProcessStep <= processStep.Image:

        imageURL = getImageURL(args.image, keywords)
        
    # Display
    webbrowser.open(imageURL)


    # if savefiles is true then save the files
    if args.savefiles:

        saveTheFiles()

    #delay
    print("delaying...")
    time.sleep(loopDelay)




# exit the program
exit()





