import argparse

# argparse.parse_args() は必ず Namespace を返すので Optional にしない。
# 受け取り側で None を許容したい場合は呼び出しごとに `Setting | None` で
# 表現すること。
Setting = argparse.Namespace
