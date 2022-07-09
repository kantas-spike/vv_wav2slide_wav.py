import glob
import os
import sys
import re
import toml
from pydub import AudioSegment

DEFAULT_DELIMITER_REGEX = r".*_@@+([^@]+).wav\Z"
DEFAULT_SLIDE_START_NO = 1
DEFAULT_BLANK_LINE_TIME_MS = 1600
DEFAULT_INTERLINE_TIME_MS = 800


def get_settings(toml_file=None):
    if toml_file is None:
        toml_file = os.path.join(os.path.dirname(__file__), "pyproject.toml")

    return toml.load(toml_file).get(
        "vv_wav2slide_wav",
        {
            "delimiter_regex": DEFAULT_DELIMITER_REGEX,
            "slide_start_no": DEFAULT_SLIDE_START_NO,
            "blank_line_time_ms": DEFAULT_BLANK_LINE_TIME_MS,
            "interline_time_ms": DEFAULT_INTERLINE_TIME_MS,
        },
    )


def show_usage():
    command_name = os.path.basename(__file__)
    print(f"USAGE: {command_name} INPUT_VV_WAVS_DIR OUTPUT_WAVS_FOR_SLIDES_DIR")


def get_slide_groups(input_dir, delimiter_regex):
    slide_groups = []
    slide_wavs = {"desc": "", "wavs": []}

    file_pattern = os.path.join(input_dir, "*.wav")

    for wav_path in sorted(glob.glob(file_pattern)):
        if result := re.match(delimiter_regex, wav_path):
            desc = str(result.group(1))
            slide_wavs["desc"] = desc
            slide_groups.append(slide_wavs)
            slide_wavs = {"desc": "", "wavs": []}
        else:
            slide_wavs["wavs"].append(wav_path)

    if len(slide_wavs["wavs"]) > 0:
        slide_groups.append(slide_wavs)

    return slide_groups


def combine_audio_file(wavs, desc, no, output_dir, blank_line_time, interline_time):
    if len(wavs) == 0:
        return

    output_path = os.path.join(output_dir, "{:03}_{}.wav".format(no, desc))
    print(f"combine to {output_path}...")
    empty_audio = AudioSegment.empty()
    for wp in wavs:
        file_name = os.path.basename(wp)
        if re.match(r".*_\.wav\Z", wp):
            print(f"   empty: {file_name}")
            empty_audio += AudioSegment.silent(duration=blank_line_time)
        else:
            print(f"   {file_name}")
            empty_audio += AudioSegment.from_wav(wp)
            empty_audio += AudioSegment.silent(duration=interline_time)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    empty_audio.export(output_path, format="wav")


def main():
    if len(sys.argv) < 3:
        print("VOICEVOXの音声ファイルを格納したディレクトリと音声ファイル出力するディレクトリを指定してください。")
        print("")
        show_usage()
        sys.exit(1)

    input_dir = os.path.abspath(os.path.expanduser(sys.argv[1]))
    output_dir = os.path.abspath(os.path.expanduser(sys.argv[2]))

    if not os.path.exists(input_dir):
        print(f"VOICEVOXの音声ファイルを格納したディレクトリが存在しません: {input_dir}")
        print("ディレクトリのパスに誤りがないか確認してください。")
        print("")
        show_usage()
        sys.exit(1)

    settings = get_settings()
    groups = get_slide_groups(input_dir, settings["delimiter_regex"])

    no = settings["slide_start_no"]
    blank_line_time = settings["blank_line_time_ms"]
    interline_time = settings["interline_time_ms"]

    for g in groups:
        combine_audio_file(g["wavs"], g["desc"], no, output_dir, blank_line_time, interline_time)
        no += 1


if __name__ == "__main__":
    main()
