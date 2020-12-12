# -*- coding: utf-8 -*-
from Tkinter import *
import Tkinter as tk
import ttk

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import callback as player
import recordpyaudio as recorder
import training as training
import analysis
import tkMessageBox
import os



#--------- Change the paths to run the program -----------

praatpath = r"C:\Users\dieul\Desktop\praat6040_win64\Praat.exe"
# wavFile = r"C:\Users\dieul\research18\py2\audio\nonezumi2.wav"
# wavFile = r"C:\Users\dieul\research18\py2\speakers.wav"
juliusScriptPath = r"C:\Users\dieul\research18\julius4-segmentation-kit-v1.0\segment_julius4.pl"
soxPath = r'C:\"Program Files (x86)"\sox-14-4-2\sox'
cabochaPath = r"C:\Program Files (x86)\CaboCha\bin\cabocha"
path_for_record = r"C:\Users\dieul\research18\py2\speakers.wav"

#-------------------- End of paths ------------------------

class Window(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)

        self.user_audio_path = path_for_record
        self.master = master
        self.training_data = training.wordlist
        self.praatpath = praatpath
        self.juliusScriptPath = juliusScriptPath
        self.soxPath = soxPath
        self.cabochaPath = cabochaPath

        self.init_window()

    def play_model_audio(self):
        items = self.listbox.curselection()
        items = [self.training_data[int(item)] for item in items]
        audio = player.AudioFile(items[0][1])
        audio.play()

    def key_error_handler(self):
        tkMessageBox.showinfo("Error","Audio not recognized by the system. Please check the record again.")

    def show_pitch(self):
        items = self.listbox.curselection()
        items = [self.training_data[int(item)] for item in items]
        ana = analysis.PitchAnalysis(self.praatpath,items[0][1],items[0][2],
                                     self.juliusScriptPath, self.soxPath, self.cabochaPath)
        pitch_values = ana.ultra_pitch_value(self.key_error_handler)
        raw_pitch_val = ana.pitch_list

        intensity_values = ana.ultra_intensity_value(self.key_error_handler)
        raw_intensity_val = ana.intensity_list


        self.ultra_refresh_plot(self.model_plot, self.model_plot_raw, self.model_plot_com,
                                pitch_values, raw_pitch_val, intensity_values, raw_intensity_val)

    def show_pitch_vowel_end(self):
        items = self.listbox.curselection()
        items = [self.training_data[int(item)] for item in items]
        ana = analysis.PitchAnalysis(self.praatpath,items[0][1],items[0][2],
                                     self.juliusScriptPath, self.soxPath, self.cabochaPath)
        pitch_values = ana.ultra_pitch_value_vowel_end(self.key_error_handler)
        raw_pitch_val = ana.pitch_list
        intensity_values = ana.ultra_intensity_value(self.key_error_handler)
        raw_intensity_val = ana.intensity_list

        self.ultra_refresh_plot(self.model_plot, self.model_plot_raw, self.model_plot_com,
                                pitch_values, raw_pitch_val, intensity_values, raw_intensity_val)
        # self.fig.savefig(ana.filename + "_VE")

    def show_pitch_vowel_middle(self):
        items = self.listbox.curselection()
        items = [self.training_data[int(item)] for item in items]
        ana = analysis.PitchAnalysis(self.praatpath,items[0][1],items[0][2],
                                     self.juliusScriptPath, self.soxPath, self.cabochaPath)
        pitch_values = ana.ultra_pitch_value_vowel_mid(self.key_error_handler)
        raw_pitch_val = ana.pitch_list
        intensity_values = ana.ultra_intensity_value(self.key_error_handler)
        raw_intensity_val = ana.intensity_list

        self.ultra_refresh_plot(self.user_plot, self.user_plot_raw, self.user_plot_com,
                                pitch_values, raw_pitch_val, intensity_values, raw_intensity_val)
        # self.fig.savefig(ana.filename + "_VM")

    def show_user_pitch_VE(self):
        analysis.refresh(self.user_audio_path)
        items = self.listbox.curselection()
        items = [self.training_data[int(item)] for item in items]
        # record_dir = os.path.dirname(self.user_audio_path)
        # record_fn = os.path.splitext(os.path.basename(self.user_audio_path))[0]
        ana = analysis.PitchAnalysis(self.praatpath, self.user_audio_path, items[0][2],
                                     self.juliusScriptPath, self.soxPath, self.cabochaPath)
        pitch_values = ana.ultra_pitch_value_vowel_end(self.key_error_handler)
        raw_pitch_val = ana.pitch_list
        intensity_values = ana.ultra_intensity_value(self.key_error_handler)
        raw_intensity_val = ana.intensity_list

        self.ultra_refresh_plot(self.user_plot, self.user_plot_raw, self.user_plot_com,
                                pitch_values, raw_pitch_val, intensity_values, raw_intensity_val)

    def show_user_pitch_VM(self):
        analysis.refresh(self.user_audio_path)
        items = self.listbox.curselection()
        items = [self.training_data[int(item)] for item in items]
        ana = analysis.PitchAnalysis(self.praatpath, self.user_audio_path, items[0][2],
                                     self.juliusScriptPath, self.soxPath, self.cabochaPath)
        pitch_values = ana.ultra_pitch_value_vowel_mid(self.key_error_handler)
        raw_pitch_val = ana.pitch_list
        intensity_values = ana.ultra_intensity_value(self.key_error_handler)
        raw_intensity_val = ana.intensity_list

        self.ultra_refresh_plot(self.user_plot, self.user_plot_raw, self.user_plot_com,
                                pitch_values, raw_pitch_val, intensity_values, raw_intensity_val)

    def show_user_pitch(self):
        analysis.refresh(self.user_audio_path)
        items = self.listbox.curselection()
        items = [self.training_data[int(item)] for item in items]
        # record_dir = os.path.dirname(self.user_audio_path)
        # record_fn = os.path.splitext(os.path.basename(self.user_audio_path))[0]
        ana = analysis.PitchAnalysis(self.praatpath, self.user_audio_path, items[0][2],
                                     self.juliusScriptPath, self.soxPath, self.cabochaPath)
        pitch_values = ana.ultra_pitch_value_vowel_mid(self.key_error_handler)
        raw_pitch_val = ana.pitch_list
        intensity_values = ana.ultra_intensity_value(self.key_error_handler)
        raw_intensity_val = ana.intensity_list

        self.ultra_refresh_plot(self.user_plot, self.user_plot_raw, self.user_plot_com,
                                pitch_values, raw_pitch_val, intensity_values, raw_intensity_val)

    def play_recorded_audio(self):
        audio = player.AudioFile(self.user_audio_path)
        audio.play()
        self.record_status.configure(text = "Ready")

    def record_audio(self):
        recorder.record_via_pyaudio(self.user_audio_path, self.start_do, self.done_do)
        self.play_recorded_audio()

    def start_do(self):
        self.record_status['text']="recording"

    def done_do(self):
        self.record_status.configure(text="Done")
        self.userPlayButton.configure(state='active')

    def ultra_refresh_plot(self, simple_plot, raw_plot, com_plot, simple_pitch_values,
                           raw_pitch_values, simple_intensity_values, raw_intensity_values):
        simple_plot.clear()
        try:
            self.draw_simple_plot(simple_plot, simple_pitch_values)
            self.draw_simple_plot(simple_plot, simple_intensity_values)

            raw_plot.clear()
            self.draw_raw_plot(raw_plot, raw_pitch_values)
            self.draw_raw_plot(raw_plot, raw_intensity_values)

            com_plot.clear()
            self.draw_com_plot(com_plot, simple_pitch_values, raw_pitch_values)
            self.draw_com_plot(com_plot, simple_intensity_values, raw_intensity_values)
        except Exception:
            tkMessageBox.showinfo("ValueError", "The system could not parse your pronunciation. Please try again.")

        self.canvas.draw()

    def refresh_plot(self, plot, val_list):
        x, y = map(list, zip(*val_list))
        plot.clear()
        plot.set_ylim([50,450])
        plot.plot(x, y)
        plot.scatter(x, y, marker="o", s=200)
        self.canvas.draw()

    def draw_simple_plot(self, plot, simple_values):
        x = []
        for i in range(0, len(simple_values)):
            x.append(i)
        y = []
        for time, pitch in simple_values:
            y.append(pitch)
        # plot.clear()
        plot.set_ylim([50,450])
        plot.grid(color='grey', linestyle='-', linewidth=0.5)
        plot.plot(x, y)
        plot.scatter(x, y, marker="o", s=200)
        # self.canvas.draw()

    def draw_com_plot(self, plot, simple_values, pitch_list):
        # plot.clear()
        sim_time, sim_pitch = map(list, zip(*simple_values))
        plot.plot(sim_time, sim_pitch)
        plot.scatter(sim_time, sim_pitch, marker="o", s=200)

        time, pitch = map(list, zip(*pitch_list))

        plot.set_ylim([50,450])
        plot.scatter(time, pitch, marker="o", s=2, color='gray')
        # self.canvas.draw()

    def draw_raw_plot(self, plot, raw_values):
        time,pitch = map(list, zip(*raw_values))
        # plot.clear()
        plot.set_ylim([50,450])
        plot.scatter(time, pitch, marker="o", s=5)
        # self.canvas.draw()

    def draw_to_plot(self, plot, val_list):
        x, y = map(list, zip(*val_list))
        plot.scatter(x, y, marker="x", s=300)
        self.canvas.draw()


    def init_window(self):
        self.master.title("GUI")
        self.pack(fill=BOTH, expand=1)

        self.fig = Figure(figsize=(15, 5), dpi=100)
        # self.model_plot = self.fig.add_subplot(121)
        self.model_plot = self.fig.add_subplot(231)
        self.model_plot_raw = self.fig.add_subplot(232)
        self.model_plot_com = self.fig.add_subplot(233)
        self.user_plot = self.fig.add_subplot(234)
        self.user_plot_raw = self.fig.add_subplot(235)
        self.user_plot_com = self.fig.add_subplot(236)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        #========= Model ========
        self.model = ttk.LabelFrame(self, text = ' Native Speaker Model ')
        self.model.grid(column=0, row=0)

        self.list_frame = Frame(self.model)
        self.list_frame.grid(column=0, row=0)
        scrollbar = Scrollbar(self.list_frame, orient=VERTICAL)

        self.listbox = Listbox(self.list_frame, selectmode = SINGLE,
                               yscrollcommand=scrollbar.set)
        self.listbox.grid(column=0, row=0)
        self.listbox.delete(0, END)
        for name, filepath, string in self.training_data:
            self.listbox.insert(END, string + '('+ name + ')')
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=1)

        self.modelPlayButton = ttk.Button(self.model, text="Play",
                                         command=self.play_model_audio)
        self.modelPlayButton.grid(column=1, row=0, padx=8, pady=4)

        self.modelAnaButton = ttk.Button(self.model, text="Show Pitch",
                                         command=self.show_pitch)
        self.modelAnaButton.grid(column=1, row=1, padx=8, pady=4)

        self.modelAnaButton = ttk.Button(self.model, text="Show Pitch 2 (VE)",
                                         command=self.show_pitch_vowel_end)
        self.modelAnaButton.grid(column=2, row=1, padx=8, pady=4)

        self.modelAnaButton = ttk.Button(self.model, text="Show Pitch 3 (VM)",
                                         command=self.show_pitch_vowel_middle)
        self.modelAnaButton.grid(column=3, row=1, padx=8, pady=4)

        #========= User record ==========

        self.user_record = ttk.LabelFrame(self, text=' Your Pronunciation ')
        self.user_record.grid(column=2, row=0, padx=8, pady=4)

        self.userPlayButton = ttk.Button(self.user_record, text="Play",
                                         command=self.play_recorded_audio)
        self.userPlayButton.configure(state='disabled')
        self.userPlayButton.grid(column=1, row=0, padx=8, pady=4)

        self.record_status = ttk.Label(self.user_record, text="Ready")
        self.record_status.grid(column=0, row=1, padx=8, pady=4)

        self.userRecordButton = ttk.Button(self.user_record, text="Record", command=self.record_audio)
        self.userRecordButton.grid(column=0, row=0, padx=8, pady=4)

        self.userAnaButton = ttk.Button(self.user_record, text="Show Pitch",
                                         command=self.show_user_pitch)
        self.userAnaButton.grid(column=2, row=0, padx=8, pady=4)

        self.userAnaButton = ttk.Button(self.user_record, text="Show Pitch VE",
                                         command=self.show_user_pitch_VE)
        self.userAnaButton.grid(column=3, row=0, padx=8, pady=4)

        self.userAnaButton = ttk.Button(self.user_record, text="Show Pitch VM",
                                         command=self.show_user_pitch_VM)
        self.userAnaButton.grid(column=4, row=0, padx=8, pady=4)

root = Tk()
# root.geometry("400x300")

app = Window(root)

root.mainloop()

# menu = Menu(self.master)
# self.master.config(menu=menu)
#
# file = Menu(menu)
# file.add_command(label='Exit', command=self.client_exit)
# menu.add_cascade(label="File", menu=file)


# a = fig.add_subplot(121)
# a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])
#
# a = fig.add_subplot(122)
# a.plot([1, 2, 3, 4, 5, 6, 7, 8], [8,8,8,8,8,8,8,8])