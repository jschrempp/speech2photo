"""
Python code to record audio from the default microphone and then transcribe it using OpenAI
    Then summarize the transcript and generate a picture based on the summary
    Then open the picture in a browser
    Then delay for 60 seconds
    Then repeat the process
    
To run:  python3 pyspeech.py
control-c to stop the program or it will end after loopsMax loops about (duration + delay)*loopsMax seconds

To run this you need to get an OpenAI API key and put it in a file called "creepy photo secret key"

Author: Jim Schrempp 2023 
"""

# import libraries
import sounddevice
import soundfile
import argparse
import webbrowser
import urllib.request
import time
import shutil
import os
import openai
from enum import IntEnum



# ----------------------
# record duration seconds of audio from the default microphone to a file and return the sound file name
#
def recordAudioFromMicrophone():
    # delete file recording.wav if it exists
    try:
        os.remove("recording.wav")
    except:
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

    print("\r\nRecording...")
    # Record audio from the default microphone
    recording = sounddevice.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)

    # Wait for the recording to finish
    sounddevice.wait()

    # Save the recording to a WAV file
    soundfile.write('recording.wav', recording, sample_rate)

    soundFileName = 'recording.wav'

    return soundFileName

# ----------------------
# get audio 
#
def getAudio(wavFileArg):
    
    if wavFileArg == 0:
        # record audio from the default microphone
        soundFileName = recordAudioFromMicrophone()
    else:
        # use the file specified by the wav argument
        soundFileName = wavFileArg
        print("\r\nUsing audio file: " + wavFileArg)

    return soundFileName

# ----------------------
# transcribe the audio file and return the transcript
#
def getTranscript(trascripitFileArg, wavFileName):
    
    if trascripitFileArg == 0:

        # transcribe the recording
        # Note: you need to be using OpenAI Python v0.27.0 for the code below to work
        print("\r\nTranscribing...")
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
        print("\r\nUsing transcript file: " + trascripitFileArg)

    return transcript

# ----------------------
# summarize the transcript and return the summary
#
def getSummary(summaryArg, transcript):
    
    if summaryArg == 0:
        # summarize the transcript 
        print("\r\nSummarizing...")
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

# ----------------------
# get keywords for the image generator and return the keywords
#
def getKeywordsForImageGen(extractArg, summary):

    nounsAndVerbs = ""

    if extractArg == 0:
        # extract the keywords from the summary

        print("\r\nExtracting...")
        prompt = f"in 10 words or less, What is the most interesting concept in the following text? \"\n{summary}\""
        if debugOn:
            print ("extract prompt: " + prompt)
        responseForImage = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]              
        )

        if debugOn:
            print("responseForImageGen: ")
            print(responseForImage)

        # extract the nouns and verbs
        nounsAndVerbs = responseForImage['choices'][0]['message']['content'].strip() 
        print("nounsAndVerbs: ")
        print(nounsAndVerbs)

    else:
        # use the extract file specified by the extract argument
        summaryFile = open(extractArg, "r")
        # read the summary file
        nounsAndVerbs = summaryFile.read()
        print("Using keywords file: " + extractArg)


    return nounsAndVerbs

# ----------------------
# get image url and return the url
#
def getImageURL(imageArg, keywords):

    if imageArg == 0:
        # use the keywords to generate an image


        prompt = f"Generate a picture based on the following \n{keywords}"
        print("Generating image...")
        print("image prompt: " + prompt)

        # use openai to generate a picture based on the summary
        responseSummary = openai.Image.create(
            prompt= prompt,
            n=1,
            size="512x512"
            )
        
        image_url = responseSummary['data'][0]['url']

        if args.savefiles and args.image == 0:
            # save the image from a url
            urllib.request.urlretrieve(image_url, "image.png")
            os.rename("image.png", timestr + "-image" + ".png")

        #print(image_url)

    else:
        image_url = imageArg
        print("Using image file: " + imageArg)

    return image_url



# ----------------------
# main program starts here
#
#
#

class processStep(IntEnum):
    Audio = 1
    Transcribe = 2
    Summarize = 3
    Keywords = 4
    Image = 5

# set the OpenAI API key
openai.api_key_path = 'creepy photo secret key'

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--savefiles", help="save the files", action="store_true") # optional argument
parser.add_argument("-d", "--debug", help="extra information printed to the console", action="store_true") # optional argument
parser.add_argument("-w", "--wav", help="use audio from file", type=str, default=0) # optional argument
parser.add_argument("-t", "--transcript", help="use transcript from file", type=str, default=0) # optional argument
parser.add_argument("-T", "--summary", help="use summary from file", type=str, default=0) # optional argument
parser.add_argument("-k", "--keywords", help="use keywords from file", type=str, default=0) # optional argument
parser.add_argument("-i", "--image", help="use image from file", type=str, default=0) # optional argument

args = parser.parse_args()

debugOn = args.debug

# if we're given a file then start at that step
# check in order so that processStartStep will be the maximum value

firstProcessStep = processStep.Audio

if args.image != 0: 
    firstProcessStep = processStep.Image
elif args.keywords != 0: 
    firstProcessStep = processStep.Keywords
elif args.summary != 0: 
    firstProcessStep = processStep.Summarize
elif args.transcript != 0: 
    firstProcessStep  = processStep.Transcribe

if firstProcessStep > processStep.Audio or args.wav != 0:
    loopsMax = 1
    loopDelay = 0   # no delay if we're not looping
else:
    loopsMax = 10  # only loop if we're recording new audio each time
    loopDelay = 120 # delay if we're looping

# Set the duration of each recording in seconds
duration = 60

# ----------------------
# Main Loop 
#

for i in range(loopsMax):

    # format a time string to use as a file name
    timestr = time.strftime("%Y%m%d-%H%M%S")

    soundFileName = ""
    transcript = ""
    summary = ""
    keywords = ""
    imageURL = ""

    # Audio
    if firstProcessStep == processStep.Audio:
       
        soundFileName = getAudio(args.wav)
         
        if args.savefiles:
            #copy the file to a new name with the time stamp
            shutil.copy(soundFileName, timestr + "-recording" + ".wav")
            soundFileName = timestr + "-recording" + ".wav"
   
    # Transcribe
    if firstProcessStep <= processStep.Transcribe:
    
        transcript = getTranscript(args.transcript, soundFileName)

        if args.savefiles and args.transcript == 0:
            f = open(timestr + "-rawtranscript" + ".txt", "w")
            f.write(transcript["text"])
            f.close()

    # Summary
    if firstProcessStep <= processStep.Summarize:

        summary = getSummary(args.summary, transcript)

        if args.savefiles and args.summary == 0:
            f = open(timestr + "-summary" + ".txt", "w")
            f.write(summary)
            f.close()

    # Keywords    
    if firstProcessStep <= processStep.Keywords:

        keywords = getKeywordsForImageGen(args.keywords, summary)

        if args.savefiles and args.keywords == 0:
            f = open(timestr + "-keywords" + ".txt", "w")
            f.write(keywords)
            f.close()

    # Image
    if firstProcessStep <= processStep.Image:

        imageURL = getImageURL(args.image, keywords)

        if args.savefiles and args.image == 0:
            # save the image
            #os.rename("image.png", timestr + "-image" + ".png")
            pass
        
    # Display
    webbrowser.open(imageURL)

    #delay
    print("delaying...")
    time.sleep(loopDelay)

# exit the program
exit()





