import pathlib
from pathlib import PosixPath

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
