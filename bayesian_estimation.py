import pymc as pm
import numpy as np
import arviz as az

def bayesian_estimation():
    """
    ベイズ推定を行う関数
    """
    # 仮の観測データW, B, N, C
    X_data = np.array([
        [25, 5, 4],
        [30, 10, 3],
        [20, 5, 5],
        [35, 7, 2],
        [40, 10, 6],
    ])
    C_obs = np.array([7.8, 6.5, 8.2, 6.2, 8.5])

    # W, B, Nに分解
    W_data, B_data, N_data = X_data[:,0], X_data[:,1], X_data[:,2]

    # PyMCモデル構築
    with pm.Model() as model:
        # 係数に事前分布（正規分布）
        a = pm.Normal("a", mu=0, sigma=1)
        b = pm.Normal("b", mu=0, sigma=1)
        c = pm.Normal("c", mu=0, sigma=1)
        d = pm.Normal("d", mu=0, sigma=1)  # W * N の交差項
        intercept = pm.Normal("intercept", mu=5, sigma=2)

        # 精度（逆分散）または標準偏差
        sigma = pm.HalfNormal("sigma", sigma=1)

        # 線形予測
        mu = (
            a * W_data**2 +
            b * B_data**2 +
            c * N_data +
            d * W_data * N_data +
            intercept
        )

        # 観測値の分布（正規分布とする）
        C = pm.Normal("C", mu=mu, sigma=sigma, observed=C_obs)

        # 推論（MCMCサンプリング）
        trace = pm.sample(1000, tune=1000, return_inferencedata=True, random_seed=42)

    # 推定結果を表示
    az.plot_trace(trace, var_names=["a", "b", "c", "d", "intercept"])
