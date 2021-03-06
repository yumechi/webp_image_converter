"""
全体的なテスト
"""

import os
import pathlib
import shutil

from src.converter import file_conveter
from src.converter.logger import Logger

INPUT_ROOT_DIR = pathlib.Path("./test_input")
OUTPUT_ROOT_DIR = pathlib.Path("./test_output")

file_conveter.logger = Logger().get_logger()


def cleanup_output_dir_files():
    def _delete(file):
        if file.is_file():
            f.unlink(missing_ok=True)
        if file.is_dir():
            shutil.rmtree(file)

    for f in OUTPUT_ROOT_DIR.rglob("*"):
        if f.name != ".keep":
            _delete(f)


def test_convert_all():
    """
    コンバート処理が行われたことのテスト。
    ファイル・フォルダの作成が正常に行われることの確認。
    """
    file_conveter.convert_all(INPUT_ROOT_DIR, OUTPUT_ROOT_DIR)


def test_check_directory_path():
    """
    コンバート後ディレクトリの確認その1
    """

    input_files = [f for f in INPUT_ROOT_DIR.rglob("*")]
    output_files = [str(f) for f in OUTPUT_ROOT_DIR.rglob("*")]
    for inp in input_files:
        inp_s = str(inp)
        expect_output_content = inp_s.replace("input", "output")
        output_list = [
            str(f) for f in output_files if expect_output_content in str(f)
        ]
        if inp.is_dir():
            assert len(output_list) > 1
        else:
            assert len(output_list) == 1


def test_check_directory_full_path():
    """
    コンバート後ディレクトリの確認その2
    """
    pwd = pathlib.Path(os.getcwd())
    input_root_dir_ = pwd / pathlib.Path("test_input")
    output_root_dir_ = pwd / pathlib.Path("test_output")
    file_conveter.logger = Logger().get_logger()
    file_conveter.convert_all(input_root_dir_, output_root_dir_)

    input_files = [f for f in input_root_dir_.rglob("*")]
    output_files = [str(f) for f in output_root_dir_.rglob("*")]
    for inp in input_files:
        inp_s = str(inp)
        expect_output_content = inp_s.replace("input", "output")
        output_list = [
            str(f) for f in output_files if expect_output_content in str(f)
        ]
        if inp.is_dir():
            assert len(output_list) > 1
        else:
            assert len(output_list) == 1


def test_skip_convert_file_green_1():
    """
    ディレクトリの場合はスキップされる
    """
    assert not file_conveter.convert(
        INPUT_ROOT_DIR, OUTPUT_ROOT_DIR, INPUT_ROOT_DIR
    )


def test_skip_convert_file_green_2():
    """
    ディレクトリの場合はスキップされる
    """
    input_root_dir_ = INPUT_ROOT_DIR / "folder1/"
    output_root_dir_ = OUTPUT_ROOT_DIR / "test_output/"
    output_dir = OUTPUT_ROOT_DIR / "folder1/"
    assert not file_conveter.convert(
        input_root_dir_, output_root_dir_, output_dir
    )


def test_skip_convert_file_green_3():
    """
    ディレクトリの場合はスキップされる
    """

    pwd = pathlib.Path(os.getcwd())
    input_root_dir_ = pwd / pathlib.Path("test_input")
    output_root_dir_ = pwd / pathlib.Path("test_output")
    assert not file_conveter.convert(
        input_root_dir_, output_root_dir_, output_root_dir_
    )


def test_cleanup_file():
    """
    問題なく作れたデータが削除できることの確認。（権限チェック）
    コンバート後のフォルダ構成を元に戻す処理を兼ねている。

    FIXME: 多分 conftest.py を使ったほうが良い
    """
    cleanup_output_dir_files()
