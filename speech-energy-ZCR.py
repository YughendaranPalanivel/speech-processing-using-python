
""" 
Pip install everything for any doubt visit pypi
URL : https://pypi.org/project/
"""

from tkinter import *
from tkinter.filedialog import askopenfilename
from pydub import AudioSegment
from pydub.playback import play
import wavio
import sounddevice as sd
import sounddevice as sd
from matplotlib import pyplot as plt
from PIL import Image
from PIL import ImageTk
import cv2
from math import floor
import numpy as np
import os

#Reading an audio file
def start():
    global source
    global source1
    global pannelA
    global y1
    global y2
    global x1
    global panel
    source=askopenfilename(filetypes=(("wav file","*.wav"),("mp3 file","*.mp3")))
    if(source.endswith(".mp3")):
        sound=AudioSegment.from_mp3(source)
        source=source.replace(".mp3",".wav")         
        sound.export(source,format="wav")            
    y=wavio.read(source)
    y11=[i[0] for i in y.data]
    z=max(y11)
    y1=[i/z for i in y11]
    y2=y.rate
    x1=[i/y.rate for i in range(0,len(y1))]
    plt.cla()
    plt.title("Original Signal ("+str(y.rate)+"Hz, Maximum Amplitude:"+str(z)+")")
    plt.xlabel("Time in Seconds")
    plt.ylabel("Amplitude")
    plt.plot(x1,y1)
    source1=source.replace(".wav",".png")
    plt.savefig(source1)
    image=ImageTk.PhotoImage(Image.open(source1))
    if(pannelA==False):
        panel = Label(image=image)
        panel.image = image
        panel.pack(padx=20, pady=30)
        pannelA=True
    else:
        panel.configure(image=image)
        panel.image = image
        panel.pack(padx=20, pady=30)
     
# Recording audio
def record():
    global source
    global source1
    global pannelA
    global y1
    global y2
    global x1
    global panel
    store=sd.rec((8000*5),samplerate=8000,channels=1)
    sd.wait()
    source=os.getcwd()+"/record.wav"
    wavio.write(source,store,8000,sampwidth=2)
    y=wavio.read(source)
    y11=[i[0]for i in y.data]
    z=max(y11)
    y1=[i/z for i in y11]
    y2=y.rate
    x1=[i/y.rate for i in range(0,len(y1))]
    plt.cla()
    plt.title("Original Signal ("+str(y.rate)+"Hz, Maximum Amplitude:"+str(z)+")")
    plt.xlabel("Time in Seconds")
    plt.ylabel("Amplitude")
    plt.plot(x1,y1)
    source1=source.replace(".wav",".png")
    plt.savefig(source1)
    image=ImageTk.PhotoImage(Image.open(source1))
    if(pannelA==False):
        panel = Label(image=image)
        panel.image = image
        panel.pack(padx=20, pady=30)
        pannelA=True
    else:
        panel.configure(image=image)
        panel.image = image
        panel.pack(padx=20, pady=30)
        
# Playing .wav file

def Play():
    sound=AudioSegment.from_wav(source)
    play(sound)
    
# Computing energy for each 20 msec of audio/speech frame.

def energy():
    ns=floor(y2/1000*20)
    x3=[i for i in range(0,floor(len(y1)/ns))]
    y3=[]
    total=0
    for i in range(1,len(y1)+1):
        if(i%ns==0):
            y3.append(total/ns)
            total=0
        else:
            total+=(y1[i-1])**2
    plt.cla()
    plt.title("Energy (Frame Size= 20ms )")
    plt.xlabel("Frame number")
    plt.ylabel("Energy")
    plt.plot(x3,y3)
    source2=source1.replace(".png",".jpg")
    plt.savefig(source2)
    image=ImageTk.PhotoImage(Image.open(source2))
    panel.configure(image=image)
    panel.image = image
    panel.pack(padx=20, pady=30)
    
# Computing zero-crossing rate (ZCR) for each 20 msec of audio/speech frame.

def zcr():
    ns=floor(y2/1000*20)
    x3=[i for i in range(0,floor(len(y1)/ns))]
    y3=[]
    count=0
    for i in range(1,len(y1)+1):
        if(i%ns==0):
            y3.append(count/(2*ns)) 
            count=0
        else:
            if(i!=len(y1)):
                count+=abs((np.sign(y1[i-1])-np.sign(y1[i])))
    plt.cla()
    plt.title("ZCR (Frame Size= 20ms )")
    plt.xlabel("Frame number")
    plt.ylabel("ZCR")
    plt.plot(x3,y3)
    source3=source1.replace(".png",".jpeg")
    plt.savefig(source3)
    image=ImageTk.PhotoImage(Image.open(source3))
    panel.configure(image=image)
    panel.image = image
    panel.pack(padx=20, pady=30)
    plt.cla()
    
    
# Main Block
if __name__ == "__main__":
    root=Tk()
    pannelA=False
    root.geometry('600x500')
    root.title("AUDIO SIGNAL PROCESSING (ENERGY and ZERO CROSSING RATE)")
    fm = Frame(root, width=300, height=50)
    fm.pack(side=BOTTOM, expand=NO, fill=NONE)
    btn = Button(root, text="Select the file (.wav/.mp3)",font=("callibri",10,"bold"), command=start)
    btn.pack(side="top",pady=10)
    btn5 = Button(fm, text="Record (5sec)", command=record,font=("callibri",10,"bold"),height=2, width=10)
    btn5.pack(side=LEFT, padx=10, pady=20)
    btn2 = Button(fm, text="Play", command=Play,font=("callibri",10,"bold"),height=2, width=10)
    btn2.pack(side=LEFT, padx=10, pady=20)
    btn3 = Button(fm, text="Energy", command=energy,font=("callibri",10,"bold"),height=2, width=10)
    btn3.pack(side=LEFT, padx=10, pady=20)
    btn4 = Button(fm, text="ZCR", command=zcr,font=("callibri",10,"bold"),height=2, width=10)
    btn4.pack(side=LEFT, padx=10, pady=20)
    root.mainloop()
