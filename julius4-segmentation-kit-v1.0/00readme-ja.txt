
		    Julius4 音素セグメンテーションキット

'04/03/05 作成		    李 晃伸 (ri@is.aist-nara.ac.jp)
'08/08/08 Julius4対応	    西村 竜一 (nisimura@sys.wakayama-u.ac.jp)							

□１．はじめに ///////////////////////////////////////////////////////

  このキットは Julius4 を使って音素単位のセグメンテーションを行うための
  キットです．Transcription からその音素の系列のみを許す文法を生成し，そ
  れを用いてJuliusで認識を行うことで，音声ファイルの音素単位の forced
  alignment が行えます．

□２．構成 ///////////////////////////////////////////////////////////

・ファイル構成

  00readme-ja.txt	本ファイル
  segment_julius4.pl	セグメンテーション実行スクリプト
  sample/		動作実験用サンプル


□３．動作要件 ///////////////////////////////////////////////////////

 動作させるには本キット以外に以下のものが必要です．

  1) Julius rev. 4.0 以降

     	Julius 4.0.2で動作確認を行なっています．
	Juliusの最新版は以下から入手できます：
	http://julius.sourceforge.jp/

  2) 音響モデル

	monophone あるいは triphone モデルをご使用下さい．
	日本語の場合，標準的な音響モデルが Julius の Web ページの
	応用キットから入手できます．下記の Web ページから
	「文法認識キット」をダウンロードして，その中の
	"model/phone_m/" 以下にある音響モデルを以下で使用してください．

	http://julius.sourceforge.jp/


□４．データの準備 ///////////////////////////////////////////////////

ある音声データに対してセグメンテーションを行うには，その音声データの
発声内容を音素モデル列で記述した書き下し（Transcription）ファイルが必要です．

  a) 音声ファイルの形式

	通常の Julius4 で認識できる形式でご用意ください．
	16kHz, 16bit, RAW (big endian) または WAV（無圧縮）を扱えます．
	また，HTK特徴量ファイル形式での入力も可能です．

  b) Transcriptionファイル

	Transcription は，各音声データの内容を表す音素系列です．
	音声ファイル１つごとに一ファイルを用意します．
	以下は「今日はいい天気だ」という音声ファイルの transcription の例です．

	例１：「今日はいい天気だ」の transcription
	------------------------------------------
	silB ky o: w a i i t e N k i d a silE
	------------------------------------------

	途中で改行をいれることで，そこで区切ってアラインメントを行う
	こともできます．例えば，以下のように transcription を複数行に分けて
	記述することで，音素単位のアラインメントの結果に追加して，それぞれ
	「今日は」，「いい」，「天気だ」というまとまりごとのアラインメント
	結果を出力できます．

	例２：「今日はいい天気だ」の transcription（改行入り）
	------------------------------------------
	silB
	ky o: w a
	i i
	t e N k i d a
	silE
	------------------------------------------

	なお，音素の表記についてですが，使用する音響モデルの音素体系に
	合わせて記述してください．その際，「今日」→「ky o:」，
	「は」→「w a」，「へ」→「e」などのように，ひらがな表記ではなく
	実際の発音に合わせて記述する必要があることに注意してください．

	また，先頭・末尾の無音区間も考慮する必要があります．上記の
	"silB" および "silE"は，それぞれ音声ファイルの先頭・末尾の部分の
	無音区間に対応するものです．録音や切り出しを行った音声データでは
	通常，ファイルの先頭・末尾に無音区間が存在する場合が多いです．
	その場合は上記のように Transcription でも指定する必要がありま
	す．

	Julius の Web ページで公開しているトライフォンモデルを使用する
	際，例１の方法ではエラーが出ることがあります．これは，silB,
	silE のトライフォンが定義されていないために起こります．
	この場合，transcription を以下のように与えることで回避できます．
	
	例３：「今日はいい天気だ」の transcription（トライフォンエラー回避）
	------------------------------------------
	silB
	ky o: w a i i t e N k i d a
	silE
	------------------------------------------


□５．セグメンテーションの実行方法 ///////////////////////////////////

 5-1) 実行スクリプトの準備
 ==========================

  "segment_julius4.pl" の先頭にある設定部分を見て，Juliusの実行バイナ
リや音響モデルの置場所などを，お使いの環境に合わせて変更してください．
triphone モデルを使う場合は，$hlist の定義のコメントを外して，音素のマッ
ピングを指定する hlist ファイル（応用キットには "logicalTri" というファ
イル名で音響モデルと同じディレクトリに含まれている）を指定してください．


 5-2) セグメンテーションの実行
 ==============================

  以下の要領でセグメンテーションを起動します．

	% ./segment_julius4.pl speechfile transcript 

起動後，認識処理に続いて音素単位のセグメンテーションが行われ，
結果がTranscriptionファイルと同じディレクトリに拡張子 ".align" をつけた
"transcript.align" という名前のファイルに記録されます．

 5-3) 結果の見方
 ==============================

"transcript.align" の見方ですが，
ファイル内の，"====== ALIGNMENT RESULT ======" 以下が
セグメンテーションの結果です．各欄の意味は以下の通りです：

       +------------------------------------------------------------+
       |from:	 開始フレーム                                       |
       |to:	 終了フレーム                                       |
       |n_score: 音響スコア（フレーム平均）                         |
       |unit:	 音素HMM名	                                    |
       |   (triphone の場合，logical=論理HMM名，physical=定義HMM名) |
       +------------------------------------------------------------+

複数行の形式で Transcription を与えた場合は，その行ごとのセグメンテー
ションの結果も合わせて出力されます．

なお，セグメンテーションを実行すると，Transcriptionファイルと同じ場所に
".align" と同時に ".log" ファイルも出力されます．これは Juliusの実行時
のログです．出力がおかしい，結果が出ないなどの場合は，このログファイルを
検証して，Julius が動作しているかどうかを確かめてください．


以上
