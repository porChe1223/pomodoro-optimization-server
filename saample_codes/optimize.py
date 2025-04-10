from scipy.optimize import minimize

def optimize(x):
    """最適化関数
    Args:
        x (list): W, B, N のリスト
    """
    def concentration(x):
        """集中度を最大化する目的関数"""
        W, B, N = x
        return -(-0.02 * W^2 - 0.05 * B^2 + 0.1 * N - 0.1 * W * N + 5)

    # 制約（範囲）
    bounds = [(1, None), # W: 1 分〜
    (1, None), # B: 1 分〜
    (1, None)] # N: 1 回〜

    # scipy による最適化(x0 は初期推定値)
    result = minimize(concentration, x0=[25, 5, 4], bounds=bounds)

    return result