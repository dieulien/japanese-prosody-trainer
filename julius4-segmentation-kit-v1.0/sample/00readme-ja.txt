このディレクトリにはサンプル音声とそのtranscriptが収められています．

   sample.wav		「今日はいい天気だ」の音声ファイル(WAV,16bit,16kHz)
   sample.trans		上記のtranscription
   sample.trans_line	         〃         (複数行)

動作確認は以下のように行ってください．

○sample.trans に基づいてセグメンテーションを行う：

  % ../segment_julius4.pl sample.raw sample.trans

○sample.trans_line に基づいてセグメンテーションを行う：

  % ../segment_julius4.pl sample.raw sample.trans_line


IPAモデル（モノフォン，16混合，性別非依存）を用いて
上記を実行した結果が result/ 以下にありますので，ご覧ください．

以上
