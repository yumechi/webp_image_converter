# ライブラリ周りでこちらがしてほしくない動きをするものを修正する。
# 今は PIL で DEBUG レベルのログが出るので、それを抑え込む処理だけ入っている。
import logging

pil_logger = logging.getLogger("PIL")
pil_logger.setLevel(logging.INFO)
del logging
