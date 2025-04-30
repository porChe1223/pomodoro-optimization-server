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
import matplotlib.pyplot as plt
import os

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
  
@app.get("/optimize/")
def optimize():
    space = [
      Real(15, 60, name="work_duration"),    # 作業時間（分）
      Real(3, 20, name="break_duration"),    # 休憩時間（分）
    ]
    
    # 📦 ログファイルの初期化
    log_file = "pomodoro_optimization_log.csv"
    if not os.path.exists(log_file):
      pd.DataFrame(columns=["datetime", "work_duration", "break_duration", "focus_score"]).to_csv(log_file, index=False)
    
    def simulate_focus_score(work_duration, break_duration):
    # 理想値との差を取ってスコアを下げる（理想：作業30分、休憩7分）
      work_penalty = abs(work_duration - 30) / 6     # ±6分ずれるごとに1点減点
      break_penalty = abs(break_duration - 7) / 2.5  # ±2.5分ずれるごとに1点減点

      base_score = 10 - (work_penalty + break_penalty)

      # ノイズを追加（±0.5程度のブレ）
      noise = np.random.normal(0, 0.5)
      score = base_score + noise

      # スコアは1〜10にクリップ
      return float(np.clip(score, 1, 10))


    # 🧠 最適化する目的関数
    @use_named_args(space)
    def objective(when=None, **params):
      print(f"\n🕒 ポモドーロ設定を提案します:")
      print(f"👉 作業時間: {params['work_duration']:.1f}分")
      print(f"👉 休憩時間: {params['break_duration']:.1f}分")

      # 🔀 擬似的に集中度をシミュレート
      score = simulate_focus_score(params["work_duration"], params["break_duration"])
      print(f"✨ 自動生成された集中度スコア: {score:.2f}")
      if when is None:
          when = datetime.now()
      print(f"✨ 完了した時間: {when}")

        # ログに保存
      new_entry = {
            "datetime": datetime.now(),
            "work_duration": params["work_duration"],
            "break_duration": params["break_duration"],
            "focus_score": score
        }
      df = pd.read_csv(log_file)
      df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
      df.to_csv(log_file, index=False)

      return -score

    TARGET_SCORE = 9.8

    # コールバック関数
    def call_back(res):
        current_best = -res.fun
        if current_best >= TARGET_SCORE:
          return True
        return False

    initial_point = [25, 5]
    initial_score = simulate_focus_score(25, 5)

    # 🔁 最適化の実行
    result = gp_minimize(
        func=objective,
        dimensions=space,
        n_calls=1000,
        n_initial_points=1,
        x0=[initial_point],
        y0=[initial_score],
        random_state=42,
        verbose=True,
        callback=[call_back]
    )

    # 📊 結果の可視化
    print("\n✅ 最適な設定（集中度最大）:")
    print(f"作業時間: {result.x[0]:.1f}分")
    print(f"休憩時間: {result.x[1]:.1f}分")
    print(f"最大集中度: {-result.fun:.1f}")
    
    return  {
      "作業時間": f"{result.x[0]:.1f}分",
      "休憩時間": f"{result.x[1]:.1f}分",
      "最大集中度": f"{-result.fun:.1f}"
    }