import os
import pathlib
from pathlib import PosixPath

from PIL import Image

from src.converter.path_resolver import resolve_output_dir_path

logger = None

# TODO: 拡張子ベースチェックではなくデータの中身を見てチェックしたい
CONVERT_TARGET_FILE_TYPE = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]


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
            file_path = pathlib.PosixPath(filename)
            input_dir = pathlib.PosixPath(dir_path)
            output_dir = resolve_output_dir_path(
                input_dir, input_root_dir, output_root_dir
            )
            convert(
                input_dir=input_dir,
                output_dir=output_dir,
                file_path=file_path,
            )


def _make_output_filename(f_) -> PosixPath:
    if not _is_image(f_):
        return f_
    # FIXME: 強制的にファイル名が `file_name.png.webp` のようになってしまうので hook したい
    return pathlib.PosixPath(f"{f_}.webp")


def _row_copy(inp, out) -> None:
    import shutil

    logger.debug(f"Copy: {inp} -> {out}")
    try:
        shutil.copy2(inp, out)
    except Exception as e:
        logger.warning(f"Copy failed[{inp} -> {out}]: {e}")


def _is_image(file_path: PosixPath) -> bool:
    if file_path.is_dir():
        return False

    ext: str = file_path.suffix.lower()
    return ext in CONVERT_TARGET_FILE_TYPE


def convert(
    input_dir: PosixPath, output_dir: PosixPath, file_path: PosixPath
) -> bool:

    if file_path.is_dir():
        logger.warn(f"Skip: {file_path=} reason=Directory data")
        return False

    is_image = _is_image(file_path)
    os.makedirs(output_dir, exist_ok=True)
    output_filename = _make_output_filename(file_path)
    input_path = f"{input_dir}/{file_path}"
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
    return True
