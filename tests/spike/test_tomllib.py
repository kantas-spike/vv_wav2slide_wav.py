import os
import tomllib


def test_load_file():
    toml_path = os.path.join(os.path.dirname(__file__), "sample.toml")
    with open(toml_path, "rb") as f:
        data = tomllib.load(f)
        print(data.get("vv_wav2slide_wav"))
