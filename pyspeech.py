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
import sounddevice as sd
import soundfile as sf
import webbrowser
import time
import openai
openai.api_key_path = 'creepy photo secret key'

# number of loops before ending
loopsMax = 10

# Set the duration of each recording in seconds
duration = 240

# Once a recording and display is completed, wait this many seconds before starting the next recording
loopDelay = 120

loopcount = 0
while loopcount < loopsMax:
    loopcount += 1

    # print the devices
    # print(sd.query_devices())

    # Set the sample rate and number of channels for the recording
    sample_rate = int(sd.query_devices(1)['default_samplerate'])
    channels = 1

    # echo the sample rate and channels
    #print(sample_rate)
    #print(channels)

    # Record audio from the default microphone
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)

    # Wait for the recording to finish
    sd.wait()

    # Save the recording to a WAV file
    sf.write('recording.wav', recording, sample_rate)

    # transcribe the recording
    # Note: you need to be using OpenAI Python v0.27.0 for the code below to work
    audio_file= open("recording.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    # print the transcript
    #print("transcript: ")
    #print(transcript)

    #summary= transcript["text"] // comment out the summarize step and use the transcript as the summary for testing
    # summarize the transcript 
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please summarize the following text:\n{transcript}",
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5
    )
    summary = response.choices[0].text.strip()

    # print the summary
    print("summary: ")
    print(summary)

    # use openai to generate a picture based on the summary
    response = openai.Image.create(
    prompt= summary,
    n=1,
    size="512x512"
    )
    image_url = response['data'][0]['url']

    # open a url in the browser
    webbrowser.open(image_url)
    #print(image_url)

    #delay
    time.sleep(loopDelay)

# exit the program
exit()




