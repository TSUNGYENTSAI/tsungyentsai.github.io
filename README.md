# Minimal Theme

TRY TO EDIT

# License

This work is licensed under a [Creative Commons Attribution-ShareAlike 3.0 Unported License](http://creativecommons.org/licenses/by-sa/3.0/).


Tina,

layout/main.py
# main.py

import logging
import os
import sys

import core_logic

# 匯入我們的自訂模組
import logging_setup
import status_updater
import yaml  # 需要 PyYAML 套件

# --- 1. 全域路徑合約 (Contract) ---
# 這些路徑是與 BE 團隊的合約，必須固定
INPUT_DIR = "/home/tsungyen/metai/layout/input"
OUTPUT_DIR = "/home/tsungyen/metai/layout/output"

CONFIG_FILE = os.path.join(INPUT_DIR, "config.yaml")
LOG_FILE = os.path.join(OUTPUT_DIR, "training.log")
RESULTS_DIR = os.path.join(OUTPUT_DIR, "results")


def main():
    """
    主執行函式，包含全局錯誤處理。
    """
    try:
        # --- 2. 初始化 ---

        # 2.1 建立儲存結果的資料夾 (OUTPUT_DIR 由 BE 掛載，應已存在)
        os.makedirs(RESULTS_DIR, exist_ok=True)

        # 2.2 設定日誌 (必須在所有 logging.* 呼叫之前)
        logging_setup.setup_logging(LOG_FILE)
        logging.info("Logger initialized. Starting AI Engine main execution.")

        # 2.3 寫入初始狀態 (告知 BE 我們已啟動)
        status_updater.initialize_status(OUTPUT_DIR)
        logging.info(f"Status set to 'initializing'. Output dir: {OUTPUT_DIR}")

        # --- 3. 讀取配置 ---
        logging.info(f"Loading config from {CONFIG_FILE}...")
        if not os.path.exists(CONFIG_FILE):
            raise FileNotFoundError(f"Config file not found at {CONFIG_FILE}")

        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        if config is None:
            raise ValueError("Config file is empty or invalid YAML.")

        logging.info("Config loaded successfully.")

        # --- 4. 邏輯路由 (Router) ---
        case_type = config.get("case_type")
        logging.info(f"Routing to case_type: {case_type}")

        if case_type == "A":
            core_logic.run_case_a(config, INPUT_DIR, RESULTS_DIR, OUTPUT_DIR)

        elif case_type == "B":
            core_logic.run_case_b(config, INPUT_DIR, RESULTS_DIR, OUTPUT_DIR)

        elif case_type == "C":
            core_logic.run_case_c(config, INPUT_DIR, RESULTS_DIR, OUTPUT_DIR)

        elif case_type == "D":
            core_logic.run_case_d(config, INPUT_DIR, RESULTS_DIR, OUTPUT_DIR)

        else:
            # 處理未知的 case_type
            raise ValueError(f"Unknown case_type '{case_type}' in config.yaml.")

        # --- 5. 成功處理 ---
        success_message = "Task finished successfully."
        logging.info(success_message)
        status_updater.update_status_completed(OUTPUT_DIR, success_message)

    except Exception as e:
        # --- 6. 全局失敗處理 ---
        error_message = f"An unhandled exception occurred: {str(e)}"

        # 嘗試寫入日誌 (如果日誌系統已初始化)
        # exc_info=True 會包含完整的 traceback
        logging.error(error_message, exc_info=True)

        # (關鍵) 更新 status.json 為 'failed'
        # 即使日誌系統失敗，也要盡力更新狀態
        try:
            status_updater.update_status_failed(OUTPUT_DIR, str(e))
        except Exception as status_e:
            # 如果連寫入狀態都失敗，只能印出到 stderr
            print(f"FATAL: Failed to write FAILED status: {status_e}", file=sys.stderr)
            print(f"Original error was: {e}", file=sys.stderr)

        # (關鍵) 以非 0 狀態碼退出，通知 BE 容器執行失敗
        sys.exit(1)

    finally:
        # --- 7. 清理 ---
        # 確保所有日誌緩衝區都被寫入檔案
        logging.info("Main script execution finished. Shutting down logger.")
        logging.shutdown()


if __name__ == "__main__":
    main()

layout/logging_setup.py
# logging_setup.py

import logging
import os
import sys


def setup_logging(log_file_path: str):
    """
    設定日誌系統，同時輸出到控制台 (stdout) 和指定的日誌檔案。
    """
    try:
        # 確保日誌檔案所在的目錄存在
        log_dir = os.path.dirname(log_file_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        # 定義日誌格式
        log_format = "%(asctime)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(log_format)

        # 取得根 logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)  # 設定根 logger 的級別

        # 清除可能已存在的 handlers，避免重複記錄
        if root_logger.hasHandlers():
            root_logger.handlers.clear()

        # 1. 設定 StreamHandler (輸出到 sys.stdout)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        root_logger.addHandler(stream_handler)

        # 2. 設定 FileHandler (寫入到日誌檔案)
        file_handler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    except Exception as e:
        # 如果日誌設定失敗，至少要能印出錯誤
        print(f"FATAL: Failed to configure logging: {e}", file=sys.stderr)
        # 這裡不建議 sys.exit(1)，讓 main.py 來決定是否終止

layout/core_logic.py

# core_logic.py

import logging
import os
import time  # 僅用於模擬長時間任務

# import pandas as pd # 暫時不需要 pandas
import status_updater

# --- Case A: 簡化的介面測試 (模擬進度) ---


def run_case_a(
    config: dict, input_dir: str, results_dir: str, output_dir_for_status: str
):
    """
    執行 Case A 的邏輯。
    (此版本為簡化版，僅用於測試介面流程)
    """
    logging.info("Starting Case A logic (Interface Test)...")

    # 1. 讀取設定
    try:
        total_steps = int(config.get("epochs", 50))
        report_interval = int(config.get("report_interval", 5))
        simulation_time_per_step = 0.2  # 模擬每一步驟花費 0.2 秒

        logging.info(
            f"Config: total_steps={total_steps}, report_interval={report_interval}"
        )

        if total_steps <= 0:
            raise ValueError("'epochs' (total_steps) must be greater than 0.")

    except Exception as e:
        logging.error(f"Failed to parse config for Case A: {e}")
        raise  # 拋出錯誤，讓 main.py 捕捉

    # 2. 讀取資料 (跳過)
    # 在這個測試中，我們跳過讀取 input_dir 中的任何檔案

    # 3. 執行模擬演算法
    logging.info("Starting simulation loop...")

    for step in range(total_steps):
        # 模擬任務執行
        time.sleep(simulation_time_per_step)

        current_metric = (step + 1) / total_steps  # 模擬一個 0 到 1 的指標

        # (關鍵) 回報進度
        # 在每個 'report_interval' 或最後一步時回報
        if (step + 1) % report_interval == 0 or (step + 1) == total_steps:
            progress = int(((step + 1) / total_steps) * 100)
            metrics = {"current_step": step + 1, "sim_metric": f"{current_metric:.3f}"}

            status_updater.update_status_running(
                output_dir_for_status,
                progress,
                f"Step {step + 1}/{total_steps} running...",
                metrics,
            )
            logging.info(
                f"Progress: Step {step + 1}/{total_steps}, Metric: {current_metric:.3f}"
            )

    # 4. 儲存結果 (模擬)
    logging.info("Simulation finished. Saving dummy results...")
    try:
        # 建立一個假的結果檔案，確認 results_dir 可寫入
        dummy_result_path = os.path.join(results_dir, "dummy_result.txt")
        with open(dummy_result_path, "w") as f:
            f.write(f"Simulation completed with {total_steps} steps.")
        logging.info(f"Dummy result saved to {dummy_result_path}")

    except Exception as e:
        logging.error(f"Failed to save results: {e}")
        raise

    logging.info("Case A logic (Interface Test) finished successfully.")

layout/status_updater.py
# status_updater.py

import json
import logging
import os
import sys
import tempfile
from typing import Any, Dict

# 狀態檔案的固定名稱
STATUS_FILE = "status.json"


def _write_status(output_dir: str, status_data: Dict[str, Any]):
    """
    (私有函式) 以原子方式寫入狀態字典到 status.json。

    使用「先寫入暫存檔，再執行 os.rename」的策略，
    確保讀取方 (BE) 永遠不會讀到一個正在寫入中、不完整的 JSON 檔案。
    """
    final_path = os.path.join(output_dir, STATUS_FILE)

    try:
        # 在與 output_dir 相同的目錄下建立一個暫存檔
        # delete=False 確保在 with 區塊結束後檔案不會被自動刪除
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=output_dir,
            delete=False,
            prefix="status_tmp_",
        ) as tf:
            json.dump(status_data, tf, ensure_ascii=False, indent=4)
            temp_path = tf.name  # 記住暫存檔的路徑

        # (核心) 原子操作：將暫存檔重命名為目標檔案
        # 在類 Unix 系統上，這是一個原子操作
        os.rename(temp_path, final_path)

    except Exception as e:
        # 如果狀態更新失敗，這是一個嚴重問題，必須記錄下來
        # logging 可能尚未初始化，故使用 print 到 stderr
        print(
            f"CRITICAL: Failed to write status file '{final_path}': {e}",
            file=sys.stderr,
        )
        # 同時嘗試使用 logging，以防萬一它已經啟動
        logging.error(f"CRITICAL: Failed to write status file '{final_path}': {e}")

        # 清理可能殘留的暫存檔
        if "temp_path" in locals() and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass  # 忽略清理錯誤


def initialize_status(output_dir: str):
    """
    寫入 'initializing' 初始狀態。
    """
    status = {
        "status": "initializing",
        "progress": 0,
        "message": "Container started, setting up...",
        "metrics": {},
    }
    _write_status(output_dir, status)


def update_status_running(
    output_dir: str, progress: int, message: str, metrics_dict: Dict[str, Any]
):
    """
    寫入 'running' 狀態，包含進度和自訂指標。
    """
    status = {
        "status": "running",
        "progress": int(progress),  # 確保進度是整數
        "message": message,
        "metrics": metrics_dict,
    }
    _write_status(output_dir, status)


def update_status_completed(output_dir: str, message: str):
    """
    寫入 'completed' 成功狀態。
    """
    status = {"status": "completed", "progress": 100, "message": message, "metrics": {}}
    _write_status(output_dir, status)


def update_status_failed(output_dir: str, error_message: str):
    """
    寫入 'failed' 失敗狀態。
    """
    status = {
        "status": "failed",
        "progress": -1,  # 使用 -1 表示失敗
        "message": error_message,
        "metrics": {},
    }
    _write_status(output_dir, status)

layout/input/config.yaml
# config.yaml
# (由 BE 團隊放置於 /app/input/config.yaml)

# -----------------
# 必要欄位: 任務路由
# -----------------
# 必須為 'A', 'B', 'C', 'D' 之一
case_type: 'A'

# -----------------
# Case 'A' 相關參數
# -----------------
# 這些參數會被 core_logic.run_case_a 讀取
learning_rate: 0.001
epochs: 50         # 總共要執行的 "週期"
report_interval: 5 # 每 5 個週期回報一次進度

# -----------------
# (其他 Case 的參數範例)
# -----------------
# case_b_params:
#   model_type: 'XGBoost'
#   n_estimators: 100
