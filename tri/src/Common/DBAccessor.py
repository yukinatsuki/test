"""
views.pyで用いられる関数を定義
"""

import mysql.connector
from pathlib import Path
import yaml

def get_ip(request):
    """
    リクエストを送ってきたIPの取得

    :param request: リクエスト
    """
    ip = ""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]  # プロキシの背後にある場合、リストの最初のIPを取得
    else:
        ip = request.META.get("REMOTE_ADDR")  # プロキシを使用していない場合、この方法を使用
    return ip


def connect_DB():
    """
    DB接続処理

    :return: 接続情報
    """
    seting = read_config()
    connection: mysql.connector.MySQLConnection = mysql.connector.connect(
        host=seting["IP"],
        user=seting["DATABASE"]["USER"],
        password=seting["DATABASE"]["PASSWORD"],
        database=seting["DATABASE"]["DATABASE"],
    )

    return connection


def read_config():
    base_dir = Path(__file__).resolve().parent.parent
    config_path = base_dir / "Config" / "config.yaml"

    with open(config_path, "r") as yml:
        settings = yaml.safe_load(yml)

    return settings
    

