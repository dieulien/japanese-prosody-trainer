# -*- coding: utf-8 -*-
'''
Created on Aug 31, 2014

@author: tmahrt

This is an example that will force align a directory of wav files and
corresponding TextGrid files.
'''

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import textgrid as analysis
from os.path import join

from pyjulius import alignFromTextgrid

path = r"C:\Users\dieul\research18\py2\audio"
cabochaOutput = join(path, "cabocha_output")
alignedOutput = join(path, "aligned_output")
juliusScriptPath = r"C:\Users\dieul\research18\julius4-segmentation-kit-v1.0\segment_julius4.pl"
soxPath = r'C:\"Program Files (x86)"\sox-14-4-2\sox'
cabochaPath = r"C:\Program Files (x86)\CaboCha\bin\cabocha"

analysis.create_silence_textgrid(join(path, "yakisobamono.wav"),path)
print("done with creating silence textgrid")

analysis.create_utterance_tier(r"C:\Users\dieul\research18\py2\audio\yakisobamono.TextGrid", u"やきそば")
print("done with creating utterances")

alignFromTextgrid.textgridToCSV(inputPath=path,
                                outputPath=path)

alignFromTextgrid.convertCorpusToKanaAndRomaji(inputPath=path,
                                               outputPath=cabochaOutput,
                                               cabochaEncoding="utf-8",
                                               cabochaPath=cabochaPath,
                                               encoding="utf-8")

alignFromTextgrid.forceAlignCorpus(wavPath=path, txtPath=cabochaOutput,
                                   outputPath=alignedOutput,
                                   juliusScriptPath=juliusScriptPath,
                                   soxPath=soxPath)

phonelist = analysis.duration_list(join(path, "aligned_output","yakisobamono.TextGrid"), 2)
timelist = analysis.get_time_pitch(phonelist)
for i in timelist: print i
analysis.get_pitch_values(join(path, "yakisobamono.wav"),timelist)
