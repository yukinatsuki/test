import json
import requests
from datetime import datetime
import Common.DBAccessor as DBAccessor
import logging
import traceback


def get_rms_info(param: str) -> dict:
    """概要

    ROBOT情報の取得

    Args:
        param: オプション

    Returns:
        list: 成功時はRMSからの返信情報を返す
        None: エラー発生時は None を返す

    Examples:
        >>> get_rms_info("ROBOT")
            list
    """
    try:
        # 現在時刻→requestIDに変換
        dt_now = datetime.now()
        requestId = (
            str(dt_now.year)
            + str(dt_now.month).zfill(2)
            + str(dt_now.day).zfill(2)
            + str(dt_now.hour).zfill(2)
            + str(dt_now.minute).zfill(2)
            + str(dt_now.second).zfill(2)
            + str(dt_now.microsecond).zfill(4)
        )

        # RMSの接続先
        config = DBAccessor.read_config()
        url = "http://" + config["IP"] + ":" + config["RMS_PORT"]

        # JSON形式のデータ
        json_data = {
            "id": "clientid",
            "msgType": "com.geekplus.athena.api.msg.req.QueryInstructionRequestMsg",
            "request": {
                "header": {
                    "clientCode": "geekplus",
                    "warehouseCode": "*",
                    "userId": "geekplus",
                    "userKey": "111111",
                    "version": "3.3.0",
                },
                "body": {"queryType": "detail"},
            },
        }

        # パラメータセット
        json_data["request"]["header"]["requestId"] = requestId
        json_data["request"]["body"]["instruction"] = param

        # json形式にjson.dumps関数で変換しないと、正しく処理を受け付けない。
        json2 = json.dumps(json_data, indent=4)
        response = requests.post(url, data=json2)
        res_data: dict = response.json()

        # RMSとのHTTP通信が成立した場合
        if response.status_code == 200:
            return res_data

        # RMSとのHTTP通信が不成立の場合
        else:
            logging.error(f"通信失敗:HTTPステータスコード[{response.status_code}]")
            return None

    except Exception as e:
        error_message = traceback.format_exc()
        logging.error(f"例外発生:{e}")
        logging.error(f"トレースバック:{error_message}")
        return None