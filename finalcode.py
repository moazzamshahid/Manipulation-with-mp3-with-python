# importing libraries 
from pydub import silence
from pydub import *
import os
import subprocess
import shutil
import sys

def filespliting(path,duration):
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 1000 miliseconds or more and get chunks
    chunks = silence.split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = duration,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")

def file_concatenation(interval):
    a = AudioSegment.silent(duration=int(interval))
    c= AudioSegment.silent(duration=1)
    directory = os.fsencode("audio-chunks")
    for file in os.listdir(directory):
        filename = os.fsdecode(file) 
        if filename.endswith(".wav"):
            b = AudioSegment.from_file("audio-chunks" +"\\" + filename )   
            time_dif=int(b.duration_seconds)  
            #the time difference is calculated so that the start of the sentences (in the same original order) are placed at regular intervals T seconds apart
            time_dif=int(interval)-(time_dif*1000)-1000 
            a = AudioSegment.silent(duration=time_dif)    
            b=b+a
            c =c+b
            continue
        else:
            continue
    c.export("output.wav",format='wav')  
          
def mp3_to_wav(file):
    subprocess.call(['ffmpeg', '-i', file,
                 'Input.wav'])
def wav_to_mp3(x):
    
    subprocess.call(['ffmpeg', '-i', "output.wav",
                 x])
def remove_raw_files():
    os.remove("input.wav")
    os.remove("output.wav")
    shutil.rmtree("audio-chunks")

def main():
    i=0

    while i<=5:
        if sys.argv[i]=="-f":
            mp3file=sys.argv[i+1] # input file name
        elif sys.argv[i]=="-p":
            dur =sys.argv[i+1] # Parameter P
            dur=int(dur)
        elif sys.argv[i]=="-t":
            interval=sys.argv[i+1] # Parameter T
            interval=int(interval)
            print("interval: ",interval)
        i+=1

    return mp3file,dur,interval

mp3file,dur,interval= main()

mp3_to_wav(mp3file)
filespliting("input.wav", dur)
file_concatenation(interval)
x=mp3file.split(".")
output_file=x[0] +"_out.mp3"
print(output_file)
wav_to_mp3(output_file)
remove_raw_files()
