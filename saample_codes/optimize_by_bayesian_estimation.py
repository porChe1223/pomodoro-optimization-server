import pymc as pm
import numpy as np
import arviz as az
from scipy.optimize import minimize

def optimize_by_bayesian_estimation():
    """
    ベイズ推定 + 最適化を行う関数
    """
    # 仮の観測データ
    X_data = np.array([
        [25, 5, 4],
        [30, 10, 3],
        [20, 5, 5],
        [35, 7, 2],
        [40, 10, 6],
    ])

    # 集中度の実測値（0〜100）
    C_obs = np.array([78, 65, 82, 62, 85])

    # W, B, N に分解
    W_data, B_data, N_data = X_data[:, 0], X_data[:, 1], X_data[:, 2]

    # PyMC モデル構築
    with pm.Model() as model: # 係数に事前分布（正規分布）
        a = pm.Normal("a", mu=0, sigma=1)
        b = pm.Normal("b", mu=0, sigma=1)
        c = pm.Normal("c", mu=0, sigma=1)
        d = pm.Normal("d", mu=0, sigma=1)
        e = pm.Normal("e", mu=0, sigma=1)
        f = pm.Normal("f", mu=0, sigma=1)
        g = pm.Normal("g", mu=5, sigma=2)

        # 標準偏差
        sigma = pm.HalfNormal("sigma", sigma=1)

        # 線形予測
        mu = (
            a * W_data**2 +
            b * B_data**2 +
            c * N_data**2 +
            d * W_data * B_data +
            e * B_data * N_data +
            f * N_data * W_data +
            g
        )

        # 観測値の分布
        C = pm.Normal("C", mu=mu, sigma=sigma, observed=C_obs)

        # MCMCサンプリング
        trace = pm.sample(1000, tune=1000, return_inferencedata=True, random_seed=42)

    # 推定結果を可視化
    az.plot_trace(trace, var_names=["a", "b", "c", "d", "e", "f", "g"])

    # 事後分布から平均を取得
    posterior = trace.posterior
    a_mean = posterior["a"].mean().item()
    b_mean = posterior["b"].mean().item()
    c_mean = posterior["c"].mean().item()
    d_mean = posterior["d"].mean().item()
    e_mean = posterior["e"].mean().item()
    f_mean = posterior["f"].mean().item()
    g_mean = posterior["g"].mean().item()

    def expected_concentration(x):
        """集中度を最大化する目的関数"""
        W, B, N = x
        C_pred = (
        a_mean * W**2 +
        b_mean * B**2 +
        c_mean * N**2 +
        d_mean * W * B +
        e_mean * B * N +
        f_mean * N * W +
        g_mean
        )
        return -C_pred # 最大化のために符号を反転

    # 制約範囲
    bounds = [(1, None), # W: 1 分〜
            (1, None), # B: 1 分〜
            (1, None)] # N: 1 回〜

    # 最適化実行
    result = minimize(expected_concentration, x0=[25, 5, 4], bounds=bounds)

    # 結果表示
    optimal_W, optimal_B, optimal_N = result.x
    max_concentration = -result.fun

    return round(optimal_W, 0), round(optimal_B, 0), round(optimal_N, 0), round(max_concentration, 0)
