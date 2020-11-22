import main
from main import convert_all, Logger
import os
import glob
import pathlib
import shutil

INPUT_ROOT_DIR = pathlib.Path("./test_input")
OUTPUT_ROOT_DIR = pathlib.Path("./test_output")


# デフォルト logger を上書き
# FIXME: これなんかもう少しうまくフックしたい
def create_default_config():
    import logging
    import logging.config

    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
    _logger = logging.getLogger("WebpConverterAppDebug")
    _logger.debug("default logger_init")
    del logging

    return _logger


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

    main.logger = create_default_config()
    convert_all(str(INPUT_ROOT_DIR), str(OUTPUT_ROOT_DIR))


def check_directory_path():
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


def cleanup_file():
    """
    問題なく作れたデータが削除できることの確認。（権限チェック）
    コンバート後のフォルダ構成を元に戻す処理を兼ねている。
    """
    cleanup_output_dir_files()
