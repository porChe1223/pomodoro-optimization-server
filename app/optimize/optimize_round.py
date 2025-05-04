from skopt import Optimizer
from skopt.learning import GaussianProcessRegressor
from skopt.learning.gaussian_process.kernels import Matern
import sys
sys.path.append("../")
from csv_handler.csv_handler import CSVHandler


def optimize_round(explanatory_variable, objective_variable):
    """ラウンド最適化を行う関数
    
    Args:
        explanatory_variable: list // 説明変数のリスト [[25, 5], [30, 5], [20, 5]]
        objective_variable: list // 目的変数のリスト [25, 30, 20]
    Returns:
        work_time (float): 最適な作業時間
        break_time (float): 最適な休憩時間
    """
    # ベイズ最適化の初期化
    opt = Optimizer(
        dimensions=[(15.0, 60.0), (3.0, 20.0)],  # 作業時間15-60分、休憩時間3-20分
        base_estimator=GaussianProcessRegressor(kernel=Matern(length_scale=1.0)),
        n_initial_points=10,
        acq_func="EI"
    )
    # 最適化用データを追加
    opt.tell(explanatory_variable, objective_variable)
    # 最適化を実行
    work_time, break_time = opt.ask()

    return work_time, break_time


if __name__ == "__main__":
    # CSVファイル操作
    csv_handler = CSVHandler("../../data/round_data.csv")
    # 説明変数と目的変数を取得
    explanatory_variable = csv_handler.make_chosen_data_list(columns=["work_time", "break_time"])
    objective_variable = csv_handler.make_chosen_data_list(columns=["focus_score"])
    print("説明変数リスト", explanatory_variable)
    print("目的変数リスト", objective_variable)
    # ラウンド最適化
    work_time, break_time = optimize_round(explanatory_variable, objective_variable)
    print("提案された作業時間: ", work_time)
    print("提案された休憩時間: ", break_time)