import time
import logging

import Common.DBAccessor as DBAccessor
import utils.def_sql as def_sql
import transport.get_rms_info as rms_info

def trigger():
    try:
        function_name = "tri.src.transport.test.trigger"

        connection = DBAccessor.connect_DB()
        cursor = connection.cursor(dictionary=True)

        logging.info(f"[{function_name}] DB接続成功")

        # 停止中の棚取得
        sql_result = def_sql.fetch_free_shelf_info(connection, cursor, function_name)

        # 停止中の棚情報無し
        if not sql_result:
            logging.info(f"[{function_name}] 停止中の棚はありません。{sql_result}")
            return None

        for item in sql_result:
            shelf_code = item["shelf_code"]
            current_position_id = item["position_id"]

            # 搬送先取得
            position = def_sql.fetch_shelf_position(connection, cursor, shelf_code, current_position_id, function_name)

            new_position_id = str(position[0]["position_id"])

            # 搬送指示挿入
            def_sql.insert_shelf_status(connection, cursor, shelf_code, new_position_id, function_name)

        # DB更新
        connection.commit()

        # 接続終了
        cursor.close()
        connection.close()

        return 1

    except Exception as e:
        logging.error(f"[{function_name}] エラー発生: {e}")
        return None
    
def update_shelf_status():
    try:
        function_name = "tri.src.transport.test.update_shelf_status"

        connection = DBAccessor.connect_DB()
        cursor = connection.cursor(dictionary=True)

        logging.info(f"[{function_name}] DB接続成功")

        sql_result = def_sql.fetch_moving_shelf_info(connection, cursor, function_name)

        # 移動中の棚情報無し
        if not sql_result:
            logging.info(f"[{function_name}] 移動中の棚はありません。{sql_result}")
            return None

        for item in sql_result:
            # 要素取出
            act_id = item["act_id"]
            shelf_code = item["shelf_code"]
            position_id = item["position_id"]
            shelf_status = item["shelf_status"]
            cell_code = str(item["cell_code"])

            # RMSから棚情報取得
            shelf_info = rms_info.return_rms_info("SHELF")

            if not shelf_info:
                logging.info(f"[{function_name}] RMSから取得した棚情報が空です。{shelf_info}")
                return None

            # 指定の要素取得
            new_item = shelf_info[shelf_code]

            # リフトアップ前
            if shelf_status == 0:
                # 搬送開始
                if "robotId" in new_item:
                    robot_id = new_item["robotId"]

                    logging.info(f"[{function_name}] 搬送開始 {shelf_code}: {new_item} robot_id {robot_id}")

                    # shelf_status更新
                    def_sql.update_shelf_status(function_name, connection, cursor, act_id, 1, robot_id)

                else:
                    logging.info(f"[{function_name}] 待機中 {shelf_code}: {new_item}")

            # リフトアップ後、搬送中
            elif shelf_status == 1:
                # リフトダウン
                if "robotId" not in new_item:
                    # 目的地に到着している
                    if str(new_item["locationCellCode"]) == cell_code:
                        logging.info(f"[{function_name}] 搬送完了 {shelf_code}: {new_item}")

                        # shelf_status更新
                        def_sql.update_shelf_status(function_name, connection, cursor, act_id, 2)
                        # position_id更新
                        def_sql.update_shelf_position(function_name, connection, cursor, shelf_code, position_id)

                    else:
                        logging.info(f"[{function_name}] 状態不明 {shelf_code}: {new_item}")

                else:
                    logging.info(f"[{function_name}] 搬送中 {shelf_code}: {new_item}")

            # DB更新
            connection.commit()

        # 接続終了
        cursor.close()
        connection.close()

        return 1

    except Exception as e:
        logging.error(f"[update_shelf_status] エラー発生: {e}")
        return None