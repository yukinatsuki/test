"""
    プログラム名: ログ定義プログラム
    プログラム概要:新物流で使用するログ出力プログラム。フォーマットや出力先を合わせるために利用。
    作成者:西谷
    作成日:2023.4.25
    更新者:西部
    更新日:2023.8.30
"""

from logging import Formatter, basicConfig, INFO
from logging.handlers import TimedRotatingFileHandler
import os

# ログレベルの設定。DEBUG, INFO, NOTSET, WARN, ERORR, CRITICALの中からひとつを指定
# INFOを設定した場合、DEBUG以下は出力されないようになる。
LOG_LEVEL = INFO

# ファイルエンコーディング
ENCODING = "utf-8"


def setup_log(folder_path: str, file_name: str, backup_day: int):
    """
    ログ出力の行う準備を行う関数

    :param file_fullpath: ログファイルのフルパス
    :param backup_day: 保持するファイル日数
    """

    # ログフォルダが無ければ作る
    os.makedirs(folder_path, exist_ok=True)

    file_fullpath = f"{folder_path}/{file_name}"

    # 日付ローテーション
    file_handler = TimedRotatingFileHandler(
        file_fullpath, when="D", backupCount=backup_day, encoding=ENCODING
    )

    # ログ出力フォーマットを設定
    file_handler.setFormatter(
        Formatter(
            "%(asctime)s.%(msecs)03d,%(levelname)-5s,%(module)s,%(lineno)04d,%(message)s",
            datefmt="%Y/%m/%d %H:%M:%S",
        )
    )

    # ルートロガーの設定
    basicConfig(level=LOG_LEVEL, handlers=[file_handler])

    # -----使用例-----
    # import setup_log
    # import logging
    # # setup_logは一度だけ呼び出す
    # setup_log.setup_log("/usr/local/tmcpython/nishibe/pytest/log/t_kpi.log", 30)
    # # ログ出力自体はloggingで行う
    # logging.info('メッセージ')
    # logging.error('エラーメッセージ')
