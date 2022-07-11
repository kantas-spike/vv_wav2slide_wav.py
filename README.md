# vv_wav2slide_wav

本ツールは、[VOICEVOX](https://github.com/VOICEVOX/voicevox) で生成した音声ファイルを、スライド資料用にスライド単位にグループ化した音声ファイルに変換します。

## 使い方

プロジェクトをチェックアウトしたディレクトリに移動後に、以下を実行します。

~~~shell
poetry run python3 vv_wav2slide_wav.py INPUT_VV_WAVS_DIR  OUTPUT_WAVS_FOR_SLIDES_DIR
~~~

もしくは、`vv_wav2slide_wav.sh` をインストール後に、以下を実行します。

~~~shell
~/bin/vv_wav2slide_wav.sh INPUT_VV_WAVS_DIR  OUTPUT_WAVS_FOR_SLIDES_DIR
~~~

## 説明

VOICEVOXは、音声原稿の各行を `[何行目]_[キャラ名]_[テキスト冒頭].wav` という名前で音声ファイルに書き出します。
音声原稿の行数分、ファイルが書き出されます。

スライド資料に音声を付けたい場合、沢山の音声ファイルからスライドに該当する音声を選択するのは大変です。

本ツールは、スライドの区切り位置を表す特別なファイル名を定義します。
デフォルトでは、`[テキスト冒頭]`部分の先頭が 識別子`@@`ではじまるものが区切りファイルになります。

~~~text
[何行目]_[キャラ名]_@@xxx.wav
~~~

本ツールは、音声ファイルの中から、区切りファイルを探し、
区切りファイルより上にある音声ファイルを同じスライドの音声だと判断します。
そして、そのスライドグループの音声ファイルを1つに結合します。

結合したファイル名は`[スライド番号]_[説明].wav`となります。

`[説明]`部分は、区切りファイル名の`[テキスト冒頭]`部分から、識別子を除いたものになります。

例えば、`[何行目]_[キャラ名]_@@xxx.wav`の場合、スライド用音声ファイル名は、以下になります。

~~~text
[スライド番号]_xxx.wav
~~~

そのため、VOICEVOXで音声原稿を作成する時に、区切りファイル作成用に、`@@xxx` のように識別子＋説明文 の行を記載してください。

### 例

以下のようなVOICEVOXの出力音声ファイルがある場合、

~~~shell
$ ls input_wavs/
001_冥鳴ひまり（ノーマル）_「ハッカーになろう….wav
002_冥鳴ひまり（ノーマル）_.wav
003_冥鳴ひまり（ノーマル）_「ハッカーになろう….wav
004_冥鳴ひまり（ノーマル）_翻訳は山形ヒロオさ….wav
005_冥鳴ひまり（ノーマル）_@@タイトル.wav
006_冥鳴ひまり（ノーマル）_私は、Python….wav
007_冥鳴ひまり（ノーマル）_目的がないことが原….wav
008_冥鳴ひまり（ノーマル）_.wav
009_冥鳴ひまり（ノーマル）_そこで、Pytho….wav
010_冥鳴ひまり（ノーマル）_おもしろそうなので….wav
011_冥鳴ひまり（ノーマル）_自分なりにまとめた….wav
012_冥鳴ひまり（ノーマル）_@@動機.wav
013_冥鳴ひまり（ノーマル）_エリックレイモンド….wav
014_冥鳴ひまり（ノーマル）_この写真の人です。….wav
015_冥鳴ひまり（ノーマル）_レイモンドさんは、….wav
016_冥鳴ひまり（ノーマル）_@@著者の紹介.wav
# 以下略
~~~

スライド用音声ファイルに変換した結果は、以下になります。

~~~shell
$ ls output_slide_wavs/
001_タイトル.wav
002_動機.wav
003_著者の紹介.wav
# 以下略
~~~

## 環境構築

以下を実行し、関連するモジュールをインストールしてください。
注意: `poetry` でパッケージを管理しています。事前に`poetry`をインストールしてください。

~~~shell
poetry install
~~~~

## カスタマイズ

`pyproject.toml`の`[vv_wav2slide_wav]`テーブルに設定情報があります。

~~~toml
[vv_wav2slide_wav]
delimiter_regex = '.*_@@+([^@]+).wav\Z'
slide_start_no = 1
blank_line_time_ms = 1600
interline_time_ms = 800
~~~

|項目|デフォルト値|説明|
|:---:|:---:|:---|
|delimiter_regex|'.*_@@+([^@]+).wav\Z'|区切りファイルを識別するための正規表現。最初のキャプチャグループが結合したファイル名の`[説明]`部分になる。|
|slide_start_no| 1 | 結合したファイル名の先頭に設定する`[スライド番号]`の開始番号|
|blank_line_time_ms| 1600 |空行の音声ファイルを結合するときに無音にする時間 [単位:ms]|
|interline_time_ms| 800 |音声ファイル間に挿入する無音の時間 [単位:ms]|

## 呼び出し用シェルスクリプトのインストール

`vv_wav2slide_wav.py`を呼び出す場合、ディレクトリの移動が必要など、実行するまでの作業が煩雑なため、
呼び出し用のシェルスクリプト `vv_wav2slide_wav.sh` を用意しています。

以下を実行してインストールしてください。デフォルトでは`~/bin`にインストールされます。

~~~shell
make install
~~~

インストール後は、以下で実行できるようになります。

~~~shell
~/bin/vv_wav2slide_wav.sh INPUT_VV_WAVS_DIR  OUTPUT_WAVS_FOR_SLIDES_DIR
~~~
