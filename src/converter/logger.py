import yaml

from src.converter.const import Setting


class Logger:
    """
    このアプリ用の Logger 定義。

    yaml形式のコンフィグから読み出して、セットする。
    設定のロードに失敗するなど、上手くいかない場合はなるべくデフォルトのロガーをセットする。
    """

    _logger = None

    def __init__(self, setting: Setting | None = None):
        if setting:
            config_file = setting.logger_config or None
            self._debug = setting.debug
            _logger = self.create_config(config_file)
        else:
            self._debug = True
            _logger = self.create_default_config()
        self._logger = _logger

    def logger_name(self):
        if self._debug:
            return "WebpConverterAppDebug"
        return "WebpConverterApp"

    def create_config(self, config_file):
        if config_file:
            return self.create_custom_logger(config_file)
        return self.create_default_config()

    def create_custom_logger(self, config_file):
        import logging.config

        _logger = None
        try:
            with open(config_file, "r") as f:
                logging.config.dictConfig(yaml.safe_load(f))
            _logger = logging.getLogger(self.logger_name())
            _logger.debug("custom logger_init")
        except yaml.YAMLError, OSError:
            import traceback

            # logger の設定前に失敗しているのでここは print
            print(f"yaml load error: {traceback.format_exc()}")
        finally:
            if not _logger:
                _logger = self.create_default_config()
            del logging
        return _logger

    def create_default_config(self):
        import logging.config

        logging.basicConfig(
            format="%(levelname)s:%(message)s", level=logging.DEBUG
        )
        _logger = logging.getLogger(self.logger_name())
        _logger.debug("default logger_init")
        del logging

        return _logger

    def get_logger(self):
        return self._logger
