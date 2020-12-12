This directory contains sample wave data and transcription in Japanese.

   sample.wav		speech data of "Kyou ha ii tenki da"(WAV,16bit,16kHz)
   sample.trans		Transcription of above (IPA phoneset)
   sample.trans_line	Transcription of above (IPA phoneset) - multi-line

 - do forced alignment according to "sample.trans"

  % ../segment_julius4.pl sample.raw sample.trans

 - do forced alignment according to "sample.trans_line"

  % ../segment_julius4.pl sample.raw sample.trans_line


The directory "result/" contains alignment result in IPA Japanese
acoustic model (monophone, 16 mixtures, gender-independent).
