import logging


def fetch_free_shelf_info(connection, cursor, function_name):
    try:
        # sql作成
        sql = """
            SELECT
                shelf_code,
                position_id
            FROM
                t_shelf_position
            WHERE
                shelf_code NOT IN (
                    SELECT
                    shelf_code
                FROM
                    t_shelf_status
                WHERE
                    shelf_status IN (0,1)
                );
            """

        # sql実行
        cursor.execute(sql)
        # 変数にデータ格納
        sql_result: list[tuple] = cursor.fetchall()

        logging.info(f"[{function_name}] 停止中の棚情報: {sql_result}")

        return sql_result

    # sql実行時にエラー発生
    except Exception as e:
        # ロールバック
        connection.rollback()

        # 接続終了
        cursor.close()
        connection.close()

        logging.error(f"[{function_name}] SQL実行時にエラーが発生しました。SQL_1: {e}")
        return None


def fetch_shelf_position(connection, cursor, shelf_code, position_id, function_name):
    try:
        # sql作成
        sql = f"""
            SELECT
                shelf_code,
                position_id,
                cell_code
            FROM
                m_shelf_position
            WHERE
                shelf_code = '{shelf_code}'
            AND
                position_id != {position_id};
            """

        # sql実行
        cursor.execute(sql)
        # 変数にデータ格納
        sql_result: list[tuple] = cursor.fetchall()

        logging.info(f"[{function_name}] {shelf_code}の搬送先候補: {sql_result}")

        return sql_result

    # sql実行時にエラー発生
    except Exception as e:
        # ロールバック
        connection.rollback()

        # 接続終了
        cursor.close()
        connection.close()

        logging.error(f"[{function_name}] SQL実行時にエラーが発生しました。SQL_2: {e}")
        return None


def insert_shelf_status(connection, cursor, shelf_code, position_id, function_name):
    try:
        # sql作成
        sql = f"""
            INSERT INTO
                t_shelf_status(
                    shelf_code,
                    position_id
                )
            VALUES
                (
                    '{shelf_code}',
                    {position_id}
                );
            """

        # sql実行
        cursor.execute(sql)

        logging.info(
            f"[{function_name}] shelf_statusにデータを挿入しました。\
shelf_code :{shelf_code} position_id :{position_id} shelf_status :0"
        )

        return 1

    # sql実行時にエラー発生
    except Exception as e:
        # ロールバック
        connection.rollback()

        # 接続終了
        cursor.close()
        connection.close()

        logging.error(f"[{function_name}] SQL実行時にエラーが発生しました。SQL_3: {e}")
        return None
    

def fetch_moving_shelf_info(connection, cursor, function_name):
    try:
        # sql作成
        sql = """
            SELECT
                t_shelf_status.act_id,
                t_shelf_status.shelf_code,
                t_shelf_status.position_id,
                t_shelf_status.shelf_status,
                m_shelf_position.cell_code
            FROM
                t_shelf_status
            INNER JOIN
                m_shelf_position
            ON
                t_shelf_status.shelf_code = m_shelf_position.shelf_code
            AND
                t_shelf_status.position_id = m_shelf_position.position_id
            WHERE
                t_shelf_status.shelf_status IN (0,1);
            """

        # sql実行
        cursor.execute(sql)
        # 変数にデータ格納
        sql_result: list[tuple] = cursor.fetchall()

        logging.info(f"[{function_name}] 移動中の棚情報: {sql_result}")

        return sql_result

    # sql実行時にエラー発生
    except Exception as e:
        # ロールバック
        connection.rollback()

        # 接続終了
        cursor.close()
        connection.close()

        logging.error(f"[{function_name}] SQL実行時にエラーが発生しました。SQL_4: {e}")
        return None


def update_shelf_status(function_name, connection, cursor, act_id, shelf_status, robot_id = None):
    try:
        # 搬送指示生成・完了
        if not robot_id:
            # sql作成
            sql = f"""
                UPDATE
                    t_shelf_status
                SET
                    shelf_status = {shelf_status},
                    update_datetime = NOW()
                WHERE
                    act_id = {act_id};
                """
        
        # 搬送開始
        else:
            # sql作成
            sql = f"""
                UPDATE
                    t_shelf_status
                SET
                    shelf_status = {shelf_status},
                    robot_id = {robot_id},
                    update_datetime = NOW()
                WHERE
                    act_id = {act_id};
                """

        # sql実行
        cursor.execute(sql)

        logging.info(f"[{function_name}] t_shelf_statusを更新しました。act_id {act_id}")

        return 1

    # sql実行時にエラー発生
    except Exception as e:
        # ロールバック
        connection.rollback()

        # 接続終了
        cursor.close()
        connection.close()

        logging.error(f"[{function_name}] SQL実行時にエラーが発生しました。SQL_5: {e}")
        return None
    

def update_shelf_position(function_name, connection, cursor, shelf_code, position_id):
    try:
        # sql作成
        sql = f"""
            UPDATE
                t_shelf_position
            SET
                position_id = {position_id},
                update_datetime = NOW()
            WHERE
                shelf_code = '{shelf_code}';
            """

        # sql実行
        cursor.execute(sql)

        logging.info(f"[{function_name}] t_shelf_positionを更新しました。\
shelf_code {shelf_code} position_id {position_id}")

        return 1

    # sql実行時にエラー発生
    except Exception as e:
        # ロールバック
        connection.rollback()

        # 接続終了
        cursor.close()
        connection.close()

        logging.error(f"[{function_name}] SQL実行時にエラーが発生しました。SQL_6: {e}")
        return None