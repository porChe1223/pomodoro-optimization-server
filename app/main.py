from fastapi import FastAPI

from skopt import gp_minimize
from skopt.space import Real
from skopt.utils import use_named_args
from skopt.learning import GaussianProcessRegressor
from skopt.callbacks import EarlyStopper
import datetime
from sklearn.gaussian_process.kernels import RBF, Matern, WhiteKernel, ConstantKernel as C
import numpy as np
import pandas as pd
from datetime import datetime
import os

app = FastAPI()


@app.get("/")
def read_root():
    return "SelfPomodoroAPI: 自動ポモドーロ最適化サーバー"


@app.get("/optimize_once/")
def optimize(focus_level: int):
    """
    最適化。
    
    Args:
    - focus_level: 集中度スコア

    Returns:
    -   -最適化された作業時間と休憩時間
    """
    # 最適化の範囲
    space = [
        Real(15, 60, name="work_duration"), # 作業時間（分）
        Real(3, 20, name="break_duration"), # 休憩時間（分）
    ]

    # CSVログファイルの初期化
    log_file = "pomodoro_optimization_log.csv"
    if os.path.exists(log_file):
        os.remove(log_file)
    pd.DataFrame(columns=[
        "work_time",
        "break_time",
        "focus_score"]).to_csv(log_file, index=False)
    print("ログファイルを初期化しました。")
    
    # 最適化
