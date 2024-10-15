import threading
import time
import logging

import Common.DBAccessor as DBAccessor
import Common.setup_log as setup_log
import transport.test as test
import transport.get_rms_info as rms_info


# ログ出力設定
setting = DBAccessor.read_config()
setup_log.setup_log(setting["LOG_FOLDER_PATH"], setting["LOG_FILE_NAME"], 5)


# 棚情報取得
def get_rms_info(param):
    while True:
        try:
            rms_info.execute_post(param)

        except Exception as e:
            logging.error(f"[get_rms_info] エラーが発生しました。{param}: {e}")

        finally:
            time.sleep(0.1)


# 搬送トリガ
def trigger():
    while True:
        try:
            test.trigger()

        except Exception as e:
            logging.error(f"[trigger] エラーが発生しました。: {e}")

        finally:
            time.sleep(0.1)


# 搬送状況監視
def update_shelf_status():
    while True:
        try:
            test.update_shelf_status()

        except Exception as e:
            logging.error(f"[update_shelf_status] エラーが発生しました。: {e}")

        finally:
            time.sleep(0.1)


t1 = threading.Thread(target=get_rms_info, args=("SHELF",))
t2 = threading.Thread(target=trigger)
t3 = threading.Thread(target=update_shelf_status)


t1.start()
t2.start()
t3.start()