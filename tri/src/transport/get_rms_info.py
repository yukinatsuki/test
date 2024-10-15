import logging

import utils.post_rms_command as def_rms


# ==================================================================================================#
class rms_imfo:
    """概要

    RMSから取得した情報を保持する

    """

    def __init__(self):
        self.robot_info = []
        self.cell_info = []
        self.shelf_info = []
        self.task_info = {}


# インスタンス化
RMS_info = rms_imfo()


# ==================================================================================================#
# rmsから各種情報取得
def execute_post(param):
    """概要

    RMSから各種情報取得

    Args:
        param: 取得したい情報

    Examples:
        >>> execute_post("ROBOT")

    """
    try:
        # RMSから各種状態取得
        res_data = def_rms.get_rms_info(param)

        if param == "ROBOT":
            if res_data:
                RMS_info.robot_info = res_data

            else:
                RMS_info.robot_info = []

        elif param == "CELL":
            if res_data:
                RMS_info.cell_info = res_data

            else:
                RMS_info.cell_info = []

        elif param == "SHELF":
            if res_data:

                shelf_list = {}
                for item in res_data["response"]["body"]["shelves"]:
                    key = item["shelfCode"]
                    shelf_list[key] = item
                
                RMS_info.shelf_info = shelf_list

            else:
                RMS_info.shelf_info = []

        else:
            if res_data:
                if res_data["response"]["header"]["code"] == 0:
                    tasks = res_data["response"]["body"]["tasks"]

                    task_info = {}

                    for task in tasks:
                        # キーはタスクID
                        key = task["taskId"]

                        if "taskPhase" in task:
                            task_phase = str(task["taskPhase"])
                            robot_id = task["robotId"]

                            robots = RMS_info.robot_info["response"]["body"]["robots"]

                            for robot in robots:
                                if robot_id == robot["robotId"]:
                                    if "locationCellCode" in robot:
                                        location_cell_code = robot["locationCellCode"]

                                    else:
                                        location_cell_code = "None"

                                    break

                        else:
                            task_phase = "not_exist"
                            robot_id = "not_exist"
                            location_cell_code = "not_exist"

                        task_info[key] = {
                            "task_phase": task_phase,
                            "robot_id": robot_id,
                            "location_cell_code": location_cell_code,
                        }

                    RMS_info.task_info = task_info

                elif res_data["response"]["header"]["code"] == 4500:
                    RMS_info.task_info = {
                        "not_exist": {
                            "task_pahse": "None",
                            "robot_id": "None",
                            "location_cell_code": "None",
                        }
                    }

                else:
                    RMS_info.task_info = {
                        "not_exist": {
                            "task_pahse": "None",
                            "robot_id": "None",
                            "location_cell_code": "None",
                        }
                    }
                    code = res_data["response"]["header"]["code"]
                    logging.error(f"異常応答:エラーコード[{code}]")

            else:
                RMS_info.task_info = {
                    "not_exist": {
                        "task_pahse": "None",
                        "robot_id": "None",
                        "location_cell_code": "None",
                    }
                }

    except Exception as e:
        logging.error(f"[post_rms_command] エラーが発生しました。{param}: {e}")
        logging.error(f"[post_rms_command] エラーが発生しました。{res_data}")

        if param == "ROBOT":
            RMS_info.robot_info = []

        elif param == "CELL":
            RMS_info.cell_info = []

        elif param == "SHELF":
            RMS_info.shelf_info = []

        else:
            RMS_info.task_info = {
                "not_exist": {
                    "task_pahse": "None",
                    "robot_id": "None",
                    "location_code": "None",
                }
            }


# ==================================================================================================#
# レスポンス
def return_rms_info(param):
    """概要

    RMSから各種情報取得

    Args:
        param: 取得したい情報

    Returns:
        dict: dictを返す

    Examples:
        >>> return_rms_info("ROBOT")
            dict
    """
    if param == "ROBOT":
        return RMS_info.robot_info

    elif param == "CELL":
        return RMS_info.cell_info

    elif param == "SHELF":
        return RMS_info.shelf_info

    else:
        return RMS_info.task_info
