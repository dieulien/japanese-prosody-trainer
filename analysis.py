# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from pyjulius import alignFromTextgrid
from praatio import tgio
from praatio import praat_scripts as pscript
from praatio import pitch_and_intensity as PI
import os
from os.path import join
import shutil
import matplotlib.pyplot as plt

praatpath = r"C:\Users\dieul\Desktop\praat6040_win64\Praat.exe"
# wavFile = r"C:\Users\dieul\research18\py2\audio\nonezumi2.wav"
wavFile = r"C:\Users\dieul\research18\py2\speakers.wav"
juliusScriptPath = r"C:\Users\dieul\research18\julius4-segmentation-kit-v1.0\segment_julius4.pl"
soxPath = r'C:\"Program Files (x86)"\sox-14-4-2\sox'
cabochaPath = r"C:\Program Files (x86)\CaboCha\bin\cabocha"


class PitchAnalysis:
    vowel_list = ['a', 'i', 'u', 'e', 'o', 'a:', 'o:']
    cons_list = ['k', 's', 't', 'n', 'h', 'm', 'y', 'r', 'w', 'g', 'z', 'j', 'd', 'b', 'p', 'sh', 'ch', 'ts', 'ky',]
    standalone = ['N']

    #To initiate a Pitch Analysis: needs praat.exe, .wav, string in Japanese, alignment requirements
    def __init__(self, praatpath, wavFile, utterances, juliusScriptPath, soxPath, cabochaPath):
        self.praatpath = praatpath
        self.wavFile = wavFile
        self.workingFolder = os.path.dirname(wavFile)
        self.utterances = utterances
        self.filename = self._get_file_name(wavFile)
        #For alignment
        self.juliusScriptPath = juliusScriptPath
        self.cabochaOutput = join(self.workingFolder, "cabocha_output")
        self.alignedOutput = join(self.workingFolder, "aligned_output")
        self.soxPath = soxPath
        self.cabochaPath = cabochaPath
        #Start working with alignment
        self.TGname = self.filename + ".TextGrid"
        self.rawTGpath = join(self.workingFolder, self.TGname)
        self._create_silence_textgrid()
        self.create_utterance_tier()
        self.alignedTGpath = ""
        self.pitch_list = []
        self.intensity_list = []

    # Get filename to save as Textgrid
    def _get_file_name(self,filepath):
        tup = os.path.splitext(os.path.basename(filepath))
        return tup[0]

    # Create a text grid with silence and sound
    def _create_silence_textgrid(self):
        pscript.annotateSilences(praatEXE=praatpath, inputWavPath=self.wavFile,
                                 outputTGPath=self.rawTGpath, silenceThreshold=-40,
                                 minSoundDur=0.5)

    # Replace sound labels with an utterance string and name the tier 'utterances'
    def create_utterance_tier(self):
        tg = tgio.openTextgrid(self.rawTGpath)
        soundtier = tg.tierDict[tg.tierNameList[0]]
        soundtier.name = "utterances"
        newEntryList = []
        for start, stop, label in soundtier.entryList:
            if label == "sound":
                newEntryList.append((start, stop, self.utterances))
            else:
                newEntryList.append((start, stop, ""))
        soundtier.entryList = newEntryList
        tg.save(fn=self.rawTGpath)

    #Reference: an example of pyJulius, author: tmahrt
    def run_alignment(self):
        alignFromTextgrid.textgridToCSV(inputPath= self.workingFolder,
                                        outputPath=self.workingFolder)
        alignFromTextgrid.convertCorpusToKanaAndRomaji(inputPath=self.workingFolder,
                                                   outputPath=self.cabochaOutput,
                                                   cabochaEncoding="utf-8",
                                                   cabochaPath=self.cabochaPath,
                                                   encoding="utf-8")
        alignFromTextgrid.forceAlignCorpus(wavPath=self.workingFolder, txtPath=self.cabochaOutput,
                                       outputPath=self.alignedOutput,
                                       juliusScriptPath=juliusScriptPath,
                                       soxPath=self.soxPath)
        self.alignedTGpath = os.path.join(self.alignedOutput, self.TGname)

    #==== Funtions that need aligned text grid ====

    # Get a list of tuples of labels, start, stop and duration
    def label_list(self, tierindex=2):
        tg = tgio.openTextgrid(self.alignedTGpath)
        soundtier = tg.tierDict[tg.tierNameList[tierindex]]
        lb_list = []
        for start, stop, label in soundtier.entryList:
            lb_list.append((label, start, stop, stop - start))
        return lb_list

    # Get time points in between consonant and vowel or in the middle of "standalone"
    def get_time_points(self, lb_list):
        timelist = []
        # val = label, start, stop, duration
        for idx, val in enumerate(lb_list):
            label = val[0]
            start = val[1]
            stop = val[2]
            duration = val[3]
            if label in self.cons_list:
                timelist.append(stop)
            elif label in self.standalone:
                timelist.append(start + duration / 2)
            elif label in self.vowel_list:
                if idx == 0:
                    timelist.append(start + duration / 2)
                else:
                    if lb_list[idx - 1][0] in self.cons_list:
                        continue
                    else:
                        if lb_list[idx - 1][0] == 'e' and label == 'i':
                            timelist.append(lb_list[idx - 1][1] + lb_list[idx - 1][3] / 2)
                        else:
                            timelist.append(start + duration / 2)
        for i in timelist:
            print i
        return timelist

    # Get time points at the end of vowels or in the middle of "standalone"
    def get_time_points_vowel_end(self, lb_list):
        timelist = []
        # val = label, start, stop, duration
        for idx, val in enumerate(lb_list):
            label = val[0]
            start = val[1]
            stop = val[2]
            duration = val[3]
            if label in self.vowel_list:
                timelist.append(stop)
            elif label in self.standalone:
                timelist.append(stop)
            elif label in self.cons_list:
                continue
        for i in timelist:
            print i
        return timelist

    def get_time_points_vowel_middle(self, lb_list):
        timelist = []
        # val = label, start, stop, duration
        for idx, val in enumerate(lb_list):
            label = val[0]
            start = val[1]
            stop = val[2]
            duration = val[3]
            if label in self.vowel_list:
                timelist.append(stop + start/2)
            elif label in self.standalone:
                timelist.append(stop + start/2)
            elif label in self.cons_list:
                continue
        for i in timelist:
            print i
        return timelist

    def get_pitch_values(self, timelist):
        outputfile = os.path.join(self.workingFolder, "text.txt")
        timepitchlist = []
        listo = PI.extractPitch(self.wavFile, outputfile, self.praatpath, 25, 600, sampleStep=0.001)
        self.pitch_list = listo[:]
        rounded_listo = [] #To prevent unexpected floating point
        for time, pitch in listo:
            rounded_listo.append((round(time,3),pitch))
        #Indexing is off - unknown reason. That's why using pitch instead of array
        pitchdict = dict(rounded_listo)
        for time in timelist:
            newtime = round(time, 3)
            pitch = pitchdict[newtime] if newtime in pitchdict else pitchdict[min(pitchdict.keys(), key=lambda k: abs(k - newtime))]
            timepitchlist.append((newtime, pitch))
        for i in timepitchlist: print i
        return timepitchlist

    def get_intensity_values(self, timelist):
        outputfile = os.path.join(self.workingFolder, "intensity.txt")
        time_intensity_list = []
        listo = PI.extractIntensity(self.wavFile, outputfile, self.praatpath, 25, sampleStep=0.01)
        self.intensity_list = listo[:]
        rounded_listo = [] #To prevent unexpected floating point
        for time, intensity in listo:
            rounded_listo.append((round(time,2),intensity))
        #Indexing is off - unknown reason. That's why using pitch instead of array
        intensitydict = dict(rounded_listo)
        for time in timelist:
            newtime = round(time, 2)
            intensity = intensitydict[newtime] if newtime in intensitydict else intensitydict[min(intensitydict.keys(), key=lambda k: abs(k - newtime))]
            time_intensity_list.append((newtime, intensity))
        # for i in time_intensity_list: print i
        return time_intensity_list


    def ultra_pitch_value(self, key_error_handler):
        try:
            self.run_alignment()
            lb_list = self.label_list()
            timelist = self.get_time_points(lb_list)
            values = self.get_pitch_values(timelist)
            return values
        except KeyError:
            key_error_handler()

    def ultra_intensity_value(self, key_error_handler):
        try:
            self.run_alignment()
            lb_list = self.label_list()
            timelist = self.get_time_points(lb_list)
            values = self.get_intensity_values(timelist)
            return values
        except KeyError:
            key_error_handler()

    def ultra_pitch_value_vowel_end(self, key_error_handler):
        try:
            self.run_alignment()
            lb_list = self.label_list()
            timelist = self.get_time_points_vowel_end(lb_list)
            values = self.get_pitch_values(timelist)
            return values
        except KeyError:
            key_error_handler()

    def ultra_intensity_value_vowel_end(self, key_error_handler):
        try:
            self.run_alignment()
            lb_list = self.label_list()
            timelist = self.get_time_points_vowel_end(lb_list)
            values = self.get_intensity_values(timelist)
            return values
        except KeyError:
            key_error_handler()

    def ultra_pitch_value_vowel_mid(self, key_error_handler):
        try:
            self.run_alignment()
            lb_list = self.label_list()
            timelist = self.get_time_points_vowel_middle(lb_list)
            values = self.get_pitch_values(timelist)
            return values
        except KeyError:
            key_error_handler()

    def ultra_intensity_value_vowel_mid(self, key_error_handler):
        try:
            self.run_alignment()
            lb_list = self.label_list()
            timelist = self.get_time_points_vowel_middle(lb_list)
            values = self.get_intensity_values(timelist)
            return values
        except KeyError:
            key_error_handler()

    def clear_traits(self):
        try:
            shutil.rmtree(self.cabochaOutput)
            shutil.rmtree(self.alignedOutput)
            shutil.rmtree(join(self.workingFolder,"align_tmp"))
            shutil.rmtree(join(self.workingFolder, "resampledAudio"))
            # os.remove(join(self.workingFolder, "text.txt"))
            os.remove(join(self.workingFolder,self.filename +".csv"))
            os.remove(self.rawTGpath)
        except Exception:
            pass
        print("temp files cleared")


def my_key_error_handler():
    print("Audio not recognized by the system. Please record your voice again.")


def plot_values(val_list, error_handler):
    x = []
    y = []
    try:
        for time, pitch in val_list:
            x.append(time)
            y.append(pitch)
        plt.plot(x,y)
        plt.scatter(x,y,marker="o",s=200)
        plt.show()
    except TypeError:
        error_handler()

def refresh(path):
    record_dir = os.path.dirname(path)
    record_fn = os.path.splitext(os.path.basename(path))[0]
    mycabochaOutput = os.path.join(record_dir, "cabocha_output")
    myalignedOutput = os.path.join(record_dir, "aligned_output")
    alignedTemp = os.path.join(record_dir, "align_tmp")
    resamp = os.path.join(record_dir, "resampledAudio")
    csvfile = join(record_dir, record_fn + ".csv")
    rawTGpath = join(record_dir, record_fn + ".TextGrid")
    if os.path.exists(mycabochaOutput):
        shutil.rmtree(mycabochaOutput)
    if os.path.exists(myalignedOutput):
        shutil.rmtree(myalignedOutput)
    if os.path.exists(alignedTemp):
        shutil.rmtree(alignedTemp)
    if os.path.exists(resamp):
        shutil.rmtree(resamp)
    # os.remove(join(self.workingFolder, "text.txt"))
    if os.path.exists(csvfile):
        os.remove(csvfile)
    # if os.path.exists(rawTGpath):
    #     os.remove(rawTGpath)
    print("temp files cleared")


# pitch_analysis_instance = PitchAnalysis(praatpath,wavFile,u"のねずみ", juliusScriptPath, soxPath, cabochaPath)
# values = pitch_analysis_instance.ultra_pitch_value(my_key_error_handler)
# plot_values(values, my_key_error_handler)
# pitch_analysis_instance.clear_traits()
