# -*- coding: utf-8 -*-

import analysis
import callback as player
import os.path
import recordpyaudio as recorder
import Tkinter as tk
from Tkinter import *
import ttk

#--------- Change the paths to run the program -----------

praatpath = r"C:\Users\dieul\Desktop\praat6040_win64\Praat.exe"
juliusScriptPath = r"C:\Users\dieul\research18\julius4-segmentation-kit-v1.0\segment_julius4.pl"
soxPath = r'C:\"Program Files (x86)"\sox-14-4-2\sox'
cabochaPath = r"C:\Program Files (x86)\CaboCha\bin\cabocha"
recordpydaudio_dir = r"C:\Users\dieul\research18\py2"
#-------------------- End of paths ------------------------

class App:
    #master = root or main window
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.printButton = ttk.Button(frame, text="Record audio", command=self.record_audio)
        self.printButton.pack(side=LEFT)

        self.printButton = ttk.Button(frame, text="Play recorded", command=self.play_speaker)
        self.printButton.pack(side=LEFT)

        self.quitButton = ttk.Button(frame, text="Quit", command=master.destroy)
        self.quitButton.pack(side=LEFT)

        self.speakers_wavpath = ""
        self.utterance = ""

        self.native_instance = lambda: None
        self.speaker_instance = lambda: None

    def record_audio(self):
        speakerfilepath = os.path.join(recordpydaudio_dir, "speakers.wav")
        recorder.record_via_pyaudio(speakerfilepath, self.start_do, self.done_do)
        self.speakers_wavpath = speakerfilepath

    def play_speaker(self):
        player.AudioFile(self.speakers_wavpath)

    def start_do(self):
        print("*recording")

    def done_do(self):
        print("*done recording")


root = tk.Tk()
b=App(root)
root.mainloop()

