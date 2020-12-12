# -*- coding: utf-8 -*-

from praatio import tgio
from praatio import praat_scripts as pscript
from praatio import pitch_and_intensity as PI
import os
from os.path import join


praatpath = r"C:\Users\dieul\Desktop\praat6040_win64\Praat.exe"
wavFile = r"C:\Users\dieul\research18\py2\audio\yakisobamono.wav"
outputPath = r"C:\Users\dieul\research18\py2\textgrid"

#Get filename to save as Textgrid
def _get_file_name(filepath):
    tup = os.path.splitext(os.path.basename(filepath))
    return tup[0]
print(_get_file_name(wavFile))

#Create a text grid with silence and sound
def create_silence_textgrid(audioFile, outputfolder):
    pscript.annotateSilences(praatEXE=praatpath, inputWavPath=audioFile,
                             outputTGPath=join(outputfolder,_get_file_name(audioFile)+".TextGrid"),
                             minSoundDur=0.5)

#Get a list of tuples of labels, start, stop and duration
def duration_list(textGridpath,tierindex=2):
    tg = tgio.openTextgrid(textGridpath)
    soundtier = tg.tierDict[tg.tierNameList[tierindex]]
    lb_list = []
    for start, stop, label in soundtier.entryList:
        lb_list.append((label, start, stop, stop - start))
    return lb_list

#Replace sound labels with an utterance string and name the tier 'utterances'
def create_utterance_tier(textGridpath, utterance):
    tg = tgio.openTextgrid(textGridpath)
    soundtier = tg.tierDict[tg.tierNameList[0]]
    soundtier.name = "utterances"
    newEntryList = []
    for start, stop, label in soundtier.entryList:
        if label == "sound":
            newEntryList.append((start, stop, utterance))
        else:
            newEntryList.append((start, stop, ""))
    soundtier.entryList = newEntryList
    tg.save(fn = textGridpath)

# create_silence_textgrid(wavFile, outputPath)
# create_utterance_tier(r"C:\Users\dieul\research18\py2\audio\yakisobamono.TextGrid", u"やきそば")

# Get time points in between consonant and vowel or in the middle of "standalone"
def get_time_pitch(entrylist):
    timelist = []
    for label, start, stop, duration in entrylist:
        if label in cons_list:
            timelist.append(stop)
        elif label in standalone:
            timelist.append(start + duration/2)
        elif label in vowel_list:
            continue
    return timelist

# def get_pitch_at(wavFile, time):
#     outputfile = r"C:\Users\dieul\research18\py2\audio\text.txt"
#     list = PI.extractPitch(wavFile,outputfile, praatpath, 25, 600, sampleStep=time)
#     for i in list: print i

#Return a list of (time, pitch) tuples
# def get_pitch_values(wavFile, timelist):
#     outputfile = r"C:\Users\dieul\research18\py2\audio\text.txt"
#     timepitchlist = []
#     for time in timelist:
#         try:
#             listo = PI.extractPitch(wavFile, outputfile, praatpath, 25, 600, sampleStep=time)
#             timepitchlist.append(listo[0])
#         except IndexError:
#             listo = PI.extractPitch(wavFile, outputfile, praatpath, 25, 600, sampleStep=time/8)
#             timepitchlist.append(listo[7])
#     for i in timepitchlist: print i

def get_pitch_values(wavFile, timelist):
    outputfile = r"C:\Users\dieul\research18\py2\audio\text.txt"
    timepitchlist = []
    listo = PI.extractPitch(wavFile, outputfile, praatpath, 25, 600, sampleStep=0.01)
    pitchdict = dict(listo)
    for time in timelist:
        newtime = round(time,2)
        pitch = pitchdict[newtime]
        timepitchlist.append((newtime,pitch))
    for i in timepitchlist: print i


    #Didn't work
    #
    # for time in timelist:
    #     newtime = round(time,2)
    #     print newtime
    #     index = int(newtime*100) - 1
    #     timepitchlist.append(listo[index])
    #     print(listo[index])
    # for i in timepitchlist: print i

# get_pitch_values(wavFile)
    # for time in timelist:
    #     try:
    #
    #         timepitchlist.append(listo[0])
    #     except IndexError:
    #         listo = PI.extractPitch(wavFile, outputfile, praatpath, 25, 600, sampleStep=time/8)
    #         timepitchlist.append(listo[7])
    # for i in timepitchlist: print i

vowel_list = ['a','i','u','e','o','a:','o:']
cons_list = ['k','s','t','n','h','m','y','r','w','g','z','j','d','b','p','sh','ch','tsu','ky']
standalone = ['N']


#Create a tier that has duration equal to the .wav file
# utterancesTier = tgio.IntervalTier('utterances',[],0,pairedWav=wavFile)
# tg = tgio.Textgrid()
# tg.addTier(utterancesTier)
# tg.save(join(outputPath, name + ".TextGrid"))

# inputFN = join('..', 'examples', 'files', 'mary.TextGrid')
#

#phone tier is always the 3rd tier
# phoneTier = tg.tierDict[tg.tierNameList[2]]


