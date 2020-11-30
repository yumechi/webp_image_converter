"""
ファイル名などの細かい変換をする関数たちのテスト
"""


import pathlib
from pathlib import PosixPath
import os

from src.converter import file_conveter


def test_is_file_green_1():
    green_path: PosixPath = pathlib.PosixPath("green.jpg")
    assert file_conveter._is_image(green_path)


def test_is_file_green_2():
    green_path: PosixPath = pathlib.PosixPath("green/green.JPG")
    assert file_conveter._is_image(green_path)


def test_is_file_green_3():
    green_path: PosixPath = pathlib.PosixPath("green/green/green.png")
    assert file_conveter._is_image(green_path)


def test_is_file_green_4():
    green_path: PosixPath = pathlib.PosixPath("green/green/green.png.PNG")
    assert file_conveter._is_image(green_path)


def test_is_file_green_5():
    green_path: PosixPath = pathlib.PosixPath("green/green/green.jpg.png")
    assert file_conveter._is_image(green_path)


def test_is_file_red_1():
    red_path: PosixPath = pathlib.PosixPath("directory/")
    assert not file_conveter._is_image(red_path)


def test_is_file_red_2():
    red_path: PosixPath = pathlib.PosixPath("red/data.pdf")
    assert not file_conveter._is_image(red_path)


def test_is_file_red_3():
    red_path: PosixPath = pathlib.PosixPath("red/data.png.pdf")
    assert not file_conveter._is_image(red_path)


def test_is_file_red_4():
    red_path: PosixPath = pathlib.PosixPath("red/png/")
    assert not file_conveter._is_image(red_path)


def test_copy_file_name_green_1():
    green_path: PosixPath = pathlib.PosixPath("test_input")
    assert file_conveter._make_output_filename(green_path) == green_path


def test_copy_file_name_green_2():
    green_path: PosixPath = pathlib.PosixPath("test_input/.keep")
    assert file_conveter._make_output_filename(green_path) == green_path


def test_copy_file_name_green_3():
    green_path: PosixPath = pathlib.PosixPath("test_input/てすと.png")
    assert file_conveter._make_output_filename(
        green_path
    ) == pathlib.PosixPath("test_input/てすと.png.webp")


def test_copy_file_name_green_4():
    green_path: PosixPath = pathlib.PosixPath("../test_input/")
    assert file_conveter._make_output_filename(green_path) == green_path


def test_copy_file_name_green_5():
    green_path: PosixPath = pathlib.PosixPath("../test_input/.keep")
    assert file_conveter._make_output_filename(green_path) == green_path


def test_copy_file_name_green_6():
    green_path: PosixPath = pathlib.PosixPath("../test_input/てすと.png")
    assert file_conveter._make_output_filename(
        green_path
    ) == pathlib.PosixPath("../test_input/てすと.png.webp")


def test_copy_file_name_green_7():
    green_path = pathlib.PosixPath(os.getcwd()) / "test_input/"
    assert file_conveter._make_output_filename(green_path) == green_path


def test_copy_file_name_green_8():
    green_path = pathlib.PosixPath(os.getcwd()) / "test_input/.keep"
    assert file_conveter._make_output_filename(green_path) == green_path


def test_copy_file_name_green_9():
    pwd = pathlib.PosixPath(os.getcwd())
    green_path = pwd / "test_input/てすと.png"
    assert (
        file_conveter._make_output_filename(green_path)
        == pwd / "test_input/てすと.png.webp"
    )
