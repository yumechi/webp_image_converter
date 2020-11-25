import argparse
import pathlib

from src.converter.const import Setting
import src.converter.file_conveter as file_conveter
from src.converter.logger import Logger

logger = None


def parse_args() -> Setting:
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
    parser.add_argument(
        "--logger-config",
        default="logging.yaml",
        type=argparse.FileType("r"),
        help="logger config",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="debug mode",
    )
    return parser.parse_args()


def fix_patch() -> None:
    """
    ライブラリ周りでこちらがしてほしくない動きをするものを修正する。
    今は PIL で DEBUG レベルのログが出るので、それを抑え込む処理だけ入っている。

    Returns:
        None
    """

    import logging

    pil_logger = logging.getLogger("PIL")
    pil_logger.setLevel(logging.INFO)
    del logging


def run(setting: Setting) -> None:
    # NOTE: スタート、終了のログを出すためにこうしているが少し冗長かも？
    input_root_dir = pathlib.PosixPath(setting.input_directory)
    output_root_dir = pathlib.PosixPath(setting.output_directory)

    logger.debug(f"start convert: {input_root_dir} -> {output_root_dir}")
    file_conveter.logger = logger
    file_conveter.convert_all(
        input_root_dir=input_root_dir, output_root_dir=output_root_dir
    )
    logger.debug(f"end convert: {input_root_dir} -> {output_root_dir}")


if __name__ == "__main__":
    setting_ = parse_args()
    logger = Logger(setting_).get_logger()
    fix_patch()
    run(setting_)
