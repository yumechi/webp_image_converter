import main
from main import convert_all, Logger


# デフォルト logger を上書き
# FIXME: これなんかもう少しうまくフックしたい
def create_default_config():
    import logging
    import logging.config

    logging.basicConfig(
        format="%(levelname)s:%(message)s", level=logging.DEBUG
    )
    _logger = logging.getLogger("WebpConverterAppDebug")
    _logger.debug("default logger_init")
    del logging

    return _logger


def test_convert_all():
    input_root_dir = './test_input'
    output_root_dir = './test_output'
    main.logger = create_default_config()
    convert_all(input_root_dir, output_root_dir)
