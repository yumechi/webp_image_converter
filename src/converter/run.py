import argparse
import logging
import pathlib

import src.converter.file_converter as file_converter
from src.converter.const import Setting
from src.converter.logger import Logger

logger: logging.Logger = logging.getLogger(__name__)


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
    # NOTE: argparse.FileType は Python 3.14 で deprecated。
    # ファイル名だけ受け取り、open は Logger 側で行う。
    parser.add_argument(
        "--logger-config",
        default="logging.yaml",
        type=str,
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

    今は PIL で DEBUG レベルのログが出るので、それを抑え込む処理だけ
    入っている。

    Returns:
        None
    """

    pil_logger = logging.getLogger("PIL")
    pil_logger.setLevel(logging.INFO)


def run(setting: Setting) -> None:
    # NOTE: スタート、終了のログを出すためにこうしているが少し冗長かも？
    input_root_dir = pathlib.Path(setting.input_directory)
    output_root_dir = pathlib.Path(setting.output_directory)

    logger.debug(f"start convert: {input_root_dir} -> {output_root_dir}")
    file_converter.logger = logger
    file_converter.convert_all(
        input_root_dir=input_root_dir, output_root_dir=output_root_dir
    )
    logger.debug(f"end convert: {input_root_dir} -> {output_root_dir}")


if __name__ == "__main__":
    setting_ = parse_args()
    logger = Logger(setting_).get_logger()
    fix_patch()
    run(setting_)
