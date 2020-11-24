import os
import pathlib

import pytest

from src.converter.path_resolver import resolve_output_dir_path


def test_path():
    """
    指定パス直下のテスト
    """
    input_path = pathlib.PosixPath("input_test")
    input_root = pathlib.PosixPath("input_test")
    output_root = pathlib.PosixPath("output_test")
    res = resolve_output_dir_path(input_path, input_root, output_root)
    assert str(res) == "output_test"


def test_path_2():
    """
    指定パスから1階層深いテスト
    """
    input_path = pathlib.PosixPath("input_test/folder1")
    input_root = pathlib.PosixPath("input_test")
    output_root = pathlib.PosixPath("output_test")
    res = resolve_output_dir_path(input_path, input_root, output_root)
    assert str(res) == "output_test/folder1"


def test_path_3():
    """
    絶対パスのテスト
    """
    pwd = pathlib.PosixPath(os.getcwd())
    input_path = pwd / "input_test/folder1"
    input_root = pwd / "input_test"
    output_root = pwd / "output_test"
    res = resolve_output_dir_path(input_path, input_root, output_root)
    assert str(res) == str(pwd / "output_test/folder1")


def test_path_4():
    """
    指定できないパスの場合は ValueError になるテスト
    """

    with pytest.raises(ValueError):
        input_path = pathlib.PosixPath("input_test")
        input_root = pathlib.PosixPath("input_test/folder1")
        output_root = pathlib.PosixPath("output_test")
        resolve_output_dir_path(input_path, input_root, output_root)


def test_path_5():
    """
    絶対パス input と相対パス output
    """

    pwd = pathlib.PosixPath(os.getcwd())
    input_path = pwd / "input_test/folder1"
    input_root = pwd / "input_test"
    output_root = pathlib.PosixPath("output_test")
    res = resolve_output_dir_path(input_path, input_root, output_root)
    assert str(res) == "output_test/folder1"


def test_path_6():
    """
    相対パス input と絶対パス output
    """

    pwd = pathlib.PosixPath(os.getcwd())
    input_path = pathlib.PosixPath("input_test/folder1")
    input_root = pathlib.PosixPath("input_test")
    output_root = pwd / "output_test"
    res = resolve_output_dir_path(input_path, input_root, output_root)
    assert str(res) == str(pwd / "output_test/folder1")


def test_path_7():
    """
    相対パス
    """

    input_path = pathlib.PosixPath("../web_image_converter/input_test/folder1")
    input_root = pathlib.PosixPath("../web_image_converter/input_test")
    output_root = pathlib.PosixPath("../web_image_converter/output_test")
    res = resolve_output_dir_path(input_path, input_root, output_root)
    assert str(res) == "../web_image_converter/output_test/folder1"
