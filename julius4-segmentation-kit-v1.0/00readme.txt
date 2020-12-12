
		    Julius forced alignment kit

2004/03/05 
LEE Akinobu (ri@is.aist-nara.ac.jp)
2008/08/09 
NISIMURA Ryuichi (nisimura@sys.wakayama-u.ac.jp)

1. Introduction

  This toolkit helps performing "forced alignment" with speech
  recognition engine Julius with grammar-based recognition.
  This kit uses Julius to do forced alignment to a speech file
  by generating grammar for each samples from transcription.


2. Contents

  00readme.txt		This file
  segment_julius4.pl	script to run forced alignment
  sample/		sample data


3. Requirement

  1) Julius rev. 4.0.2 or later

     The latest version is available for free from:
	 http://julius.sourceforge.jp/en/

  2) Acoustic model

     Any type of acoustic model that can be used in Julius is
     applicable.  Julius supports HMM in HTK ascii format,
     trained with MFCC parameters.  For more detail, please
     consult Julius web page at:
     http://julius.sourceforge.jp/

4. Preparation

  To perform alignment, you need to prepare a speech file, and
  corresponding transciption text that consists of a sequence of
  phoneme (i.e. acousic model) that describes the content of the
  speech. 

  a) Format of speech data

        Speech format should be 16kHz, 16bit, RAW(bigendian) or WAV
	(no compression), or any kind that is acceptable in
	Julius.  Input with HTK parameter file is alsoavailable (in
	that case you have to set '-input mfcfile' at the htead of
	segment_julius4.pl)

  b) Transcription

	A transcription file should be prepared for each speech data.
	Below is an example of transcription for speech data in Japanese.

	Ex.1: transcription file of "Kyou ha ii tenki da"
	------------------------------------------
	silB ky o: w a i i t e N k i d a silE
	------------------------------------------

        By inserting newline, the forced alignment will be also
        performed per line.  With the next transcription will, Julius
        will perform segmentation for both phoneme unit and in line
        unit.  This feature can be useful if you get informations per
	unit larger than phoneme (i.e. word).

	Ex.2: transcription file of "Kyou ha ii tenki da" with newlines
	------------------------------------------
	silB
	ky o: w a
	i i
	t e N k i d a
	silE
	------------------------------------------

	Please note about the head silence and tail silence.  The
	"silB" and "silE" at the example above corresponds to silence
	at the beginnning and end of speech data, which often exists
	in most of speech database, or when you record a speech data
	with automatic speech detection.


5. How to run

 5-1) configure the script

   Please see the header part of "segment_julius4.pl", and set the
   paths to julius executables and acoustic model.  When you are specifying
   a triphone model in $hmmdefs, you also have to set $hlist to
   the HMM list file that specifies logical-to-physical phone mapping.
   

 5-2) run

   Alignment will be run as below:

	% ./segment_julius4.pl speech_file transcription_file

   Result will be stored in the same directory as the transcription
   file, with a filename attached with ".align" suffix, as
   "transcription_file.align".  The recognition log of Julius will be
   also stored in the same way at "transcription_file.log".

 5-3) how to view the result

In the .align file, the section below "====== ALIGNMENT RESULT ======"
is the result of forced alignment.

       +------------------------------------------------------------+
       |from:	 beginning frame of matched segment                 |
       |to:	 end frame of matched segment                       |
       |n_score: acoustic likelihood normalized by frame            |
       |unit:	 applied HMM name                                   |
       |   (with triphone, 'logical' means logical triphone name,   |
       |    and 'physical' means actual triphone name in hmmdefs    |
       +------------------------------------------------------------+

If your transcription consists of several lines, the alignment result
for each line will be also shown.

The .log file contains log output of Julius.  When you have some
trouble in forced alignment, first look into the log file to see if
Julius runs correctly.

