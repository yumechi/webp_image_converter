import os
import pathlib
from pathlib import PosixPath

from PIL import Image

from src.converter.path_resolver import resolve_output_dir_path

logger = None


def convert_all(
    input_root_dir: PosixPath,
    output_root_dir: PosixPath,
) -> None:
    # NOTE: os.walk使うより、再帰処理にしたほうがきれいかも？（雑にメモリに展開されすぎている気がする）
    for dir_path, dir_list, file_list in os.walk(input_root_dir):
        file_count = len(file_list)
        if file_count == 0:
            # skip
            continue
        logger.debug(f"{dir_path} count: {file_count}")
        for filename in file_list:
            input_dir = pathlib.PosixPath(dir_path)
            output_dir = resolve_output_dir_path(
                input_dir, input_root_dir, output_root_dir
            )
            convert(
                input_dir=str(input_dir),
                output_dir=str(output_dir),
                filename=filename,
            )


def _make_output_filename(f_, _is_image):
    if not _is_image:
        return f_
    # FIXME: 強制的にファイル名が `file_name.png.webp` のようになってしまうので hook したい
    return f"{f_}.webp"


def _row_copy(inp, out):
    import shutil

    logger.debug(f"Copy: {inp} -> {out}")
    try:
        shutil.copy2(inp, out)
    except Exception as e:
        logger.warning(f"Copy failed[{inp} -> {out}]: {e}")


def _is_image_file(f_):
    fragments = f_.split(".")
    if len(fragments) < 2:
        return False
    ext = fragments[-1].lower()
    # FIXME: 変換可能なファイル形式が網羅できてない気がする
    return ext in ["jpg", "jpeg", "png", "gif", "bmp"]


def convert(input_dir: str, output_dir: str, filename: str) -> None:

    is_image = _is_image_file(filename)
    os.makedirs(output_dir, exist_ok=True)
    output_filename = _make_output_filename(filename, is_image)
    input_path = f"{input_dir}/{filename}"
    output_path = f"{output_dir}/{output_filename}"

    try:
        if is_image:
            logger.info(f"Try convert: {input_path} -> {output_path}")
            im = Image.open(input_path)
            im.save(output_path, "webp")
        else:
            _row_copy(input_path, output_path)
    except Exception as e:
        import traceback

        # print error, but continue
        logger.warning("Convert Error: %s\n%s", e, traceback.format_exc())
        # そのままコピーする
        _row_copy(input_path, output_path)
