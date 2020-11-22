import argparse
import os
from typing import Optional
from PIL import Image

Setting = Optional[argparse.Namespace]


def args() -> Setting:
    parser = argparse.ArgumentParser(description="Convert image to webp")
    parser.add_argument(
        "-i",
        "--input-directory",
        default="input",
        type=str,
        help="input file dir",
    )
    parser.add_argument(
        "-o",
        "--output-directory",
        default="output",
        type=str,
        help="output file dir",
    )
    parser.add_argument(
        "-m", "--mode", default=None, type=str, help="mode(feature)"
    )
    return parser.parse_args()


def run(setting: Setting) -> None:
    input_root_dir = setting.input_directory
    output_root_dir = setting.output_directory
    print(f"start convert: {input_root_dir} -> {output_root_dir}")
    convert_all(input_root_dir=input_root_dir, output_root_dir=output_root_dir)
    print(f"end convert: {input_root_dir} -> {output_root_dir}")


def convert_all(input_root_dir: str, output_root_dir: str):
    for dir_path, dir_list, file_list in os.walk(input_root_dir):
        file_count = len(file_list)
        if file_count == 0:
            # skip
            continue
        print(f"{dir_path} count: {file_count}")
        for filename in file_list:
            input_dir = dir_path
            t = dir_path.split("/")
            if len(t) == 1:
                output_dir = output_root_dir
            else:
                output_dir = "/".join([output_root_dir] + t[1:])
            convert(
                input_dir=input_dir,
                output_dir=output_dir,
                filename=filename,
            )


def convert(input_dir: str, output_dir: str, filename: str) -> None:
    def _make_output_filename(f_, _is_image):
        if not _is_image:
            return f_
        return f"{f_}.webp"

    def _row_copy(inp, out):
        import shutil

        print(f"Copy: {inp} -> {out}")
        try:
            shutil.copy2(inp, out)
        except Exception as e:
            print(f"Copy failed[{inp} -> {out}]: {e}")

    def _is_image_file(f_):
        fragments = f_.split(".")
        if len(fragments) < 2:
            return False
        ext = fragments[-1].lower()
        return ext in ["jpg", "jpeg", "png", "gif", "bmp"]

    is_image = _is_image_file(filename)
    os.makedirs(output_dir, exist_ok=True)
    output_filename = _make_output_filename(filename, is_image)
    input_path = f"{input_dir}/{filename}"
    output_path = f"{output_dir}/{output_filename}"

    try:
        if is_image:
            print(f"Try convert: {input_path} -> {output_path}")
            im = Image.open(input_path)
            im.save(output_path, "webp")
        else:
            _row_copy(input_path, output_path)
    except Exception as e:
        import traceback

        # print error, but continue
        print("Error: %s", e)
        # そのままコピーする
        _row_copy(input_path, output_path)


if __name__ == "__main__":
    run(args())
