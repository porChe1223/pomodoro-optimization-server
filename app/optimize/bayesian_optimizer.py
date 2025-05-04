from skopt import Optimizer
from skopt.learning import GaussianProcessRegressor
from skopt.learning.gaussian_process.kernels import Matern
import sys
sys.path.append("../")
from csv_handler.csv_handler import CSVHandler

class BayesianOptimizer:
    def __init__(self, target):
        try:
            if target == "round":
                self.opt = Optimizer(
                    dimensions=[(15.0, 60.0), (3.0, 20.0)],
                    base_estimator=GaussianProcessRegressor(kernel=Matern(length_scale=1.0)),
                    n_initial_points=10,
                    acq_func="EI"
                )
            elif target == "session":
                self.opt = Optimizer(
                    dimensions=[(60.0, 480.0), (25.0, 60.0), (4, 8)],
                    base_estimator=GaussianProcessRegressor(kernel=Matern(length_scale=1.0)),
                    n_initial_points=10,
                    acq_func="EI"
                )
            else:
                raise ValueError(f"未対応の最適化タイプが指定されました: '{target}'")
        except Exception as e:
            print(f"[初期化エラー] \n{e}")
            raise  
    
    
    def optimize(self, explanatory_variable, objective_variable):
        # 最適化用データを追加
        self.opt.tell(explanatory_variable, objective_variable)
        # 最適化を実行
        work_time, break_time = self.opt.ask()

        return work_time, break_time
    


if __name__ == "__main__":
    # CSVファイル操作
    csv_handler = CSVHandler("../../data/round_csv/001.csv")
    # 説明変数と目的変数を取得
    explanatory_variable = csv_handler.make_chosen_data_list(columns=["work_time", "break_time"])
    objective_variable = csv_handler.make_chosen_data_list(columns=["focus_score"])
    print("説明変数リスト", explanatory_variable)
    print("目的変数リスト", objective_variable)
    # ラウンド最適化
    opt = BayesianOptimizer("round")
    work_time, break_time = opt.optimize(explanatory_variable, objective_variable)
    print("提案された作業時間: ", work_time)
    print("提案された休憩時間: ", break_time)




