import pathlib
import shutil

from src.converter import convert_file
from src.converter.logger import Logger

INPUT_ROOT_DIR = pathlib.Path("./test_input")
OUTPUT_ROOT_DIR = pathlib.Path("./test_output")


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

    convert_file.logger = Logger().get_logger()
    convert_file.convert_all(str(INPUT_ROOT_DIR), str(OUTPUT_ROOT_DIR))


def test_check_directory_path():
    """
    コンバート後ディレクトリの確認その1
    FIXME: なんとなくそう思ってたけど、バグっている
    """

    input_files = [str(f) for f in INPUT_ROOT_DIR.rglob("*")]
    output_files = [str(f) for f in OUTPUT_ROOT_DIR.rglob("*")]
    for inp in input_files:
        expect_output_content = inp.replace("input", "output")
        assert any(
            f
            for f in output_files
            # FIXME: ディレクトリのテストも兼ねるため、正確に画像ファイルかどうか見てwebpで終わるかを見ていない
            if f in expect_output_content
        )


def test_cleanup_file():
    """
    問題なく作れたデータが削除できることの確認。（権限チェック）
    コンバート後のフォルダ構成を元に戻す処理を兼ねている。
    """
    cleanup_output_dir_files()
