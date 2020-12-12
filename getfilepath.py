#======================
# imports
#======================
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import parselmouth
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


sns.set() # Use seaborn's default style to make attractive graphs

win = tk.Tk()
win.title("Pronunciation training")

audio_file_path = tk.StringVar()

# Disable resizing the GUI
#win.resizable(0,0)    

#
aLabel = ttk.Label(win, text = "Click to open file")
aLabel.grid(column = 0, row = 0)

#-----------------Functions ----------------------#
# draw_pitch: adopted from Parselmouth's examples
def draw_pitch(pitch):
    # Extract selected pitch contour, and
    # replace unvoiced samples by NaN to not plot
    pitch_values = pitch.selected_array['frequency']
    pitch_values[pitch_values==0] = np.nan
    plt.plot(pitch.xs(), pitch_values, 'x', markersize=5, color='w')
    plt.plot(pitch.xs(), pitch_values, 'o', markersize=2)
    plt.grid(False)
    plt.ylim(0, pitch.ceiling)
    plt.ylabel("fundamental frequency [Hz]")

#-------------- Button click events --------------#
# Button Click Event Function to open Audio file
def clickOpenAudio():
    audio_file_path.set(filedialog.askopenfilename())
    # path = filedialog.askopenfilename(filetypes=(("wav","*.wav"),("all files","*.*")))
    # audio_file_path = path
    aLabel.configure(text = audio_file_path.get())
    analyzeaudio.configure(state = 'enabled')
    drawpitch.configure(state='enabled')

def clickAnalyze():
    aLabel.configure(text = "this is file path" + audio_file_path.get())
    # Plot nice figures using Python's "standard" matplotlib library
    snd = parselmouth.Sound(audio_file_path.get())
    plt.figure()
    plt.plot(snd.xs(), snd.values.T)
    plt.xlim([snd.xmin, snd.xmax])
    plt.xlabel("time [s]")
    plt.ylabel("amplitude")
    plt.show() # or plt.savefig("sound.png"), or plt.savefig("sound.pdf")

def clickDrawPitch():
    snd = parselmouth.Sound(audio_file_path.get())
    pitch = snd.to_pitch()
    plt.figure()
    draw_pitch(pitch)
    plt.show()

#------------- Buttons ---------------#

openaudio = ttk.Button(win, text="Open Audio", command=clickOpenAudio)
openaudio.grid(column=1, row=0)

analyzeaudio = ttk.Button(win, text="Analyze Audio", command=clickAnalyze, state='disabled')
analyzeaudio.grid(column=1, row=4)

drawpitch = ttk.Button(win, text="Analyze Audio", command=clickDrawPitch, state='disabled')
drawpitch.grid(column=1, row=2)


#======================
# Start GUI
#======================
win.mainloop()