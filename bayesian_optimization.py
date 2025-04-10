from bayes_opt import BayesianOptimization
import numpy as np

def bayesian_optimization():
    """
    ベイズ最適化を行う関数
    """
    # ベイズ推定で得られた係数（仮）
    a_mean = -0.02
    b_mean = -0.05
    c_mean = 0.1
    d_mean = -0.1
    intercept_mean = 5.0

    def concentration_function(W, B, N):
        """集中度を最大化する目的関数"""
        C_pred = (
            a_mean * W**2 +
            b_mean * B**2 +
            c_mean * N +
            d_mean * W * N +
            intercept_mean
        )
        return C_pred  # 最大化するのでそのまま返す

    # ベイズ最適化の範囲設定
    pbounds = {
        'W': (10, 60),   # 作業時間
        'B': (3, 30),    # 休憩時間
        'N': (1, 10)     # サイクル数
    }

    # 最適化オブジェクトを作成
    optimizer = BayesianOptimization(
        f=concentration_function,
        pbounds=pbounds,
        random_state=42,
        verbose=2  # 詳細ログを表示
    )

    # 最適化の実行
    optimizer.maximize(
        init_points=5,  # ランダム初期点
        n_iter=25        # 試行回数（多いほど精度↑）
    )

    # 結果の出力
    return optimizer.max['target'], optimizer.max['params']