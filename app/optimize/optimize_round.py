from skopt import Optimizer
from skopt.learning import GaussianProcessRegressor
from skopt.learning.gaussian_process.kernels import Matern
import pandas as pd
import numpy as np

def load_data_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    X = df[['work_time', 'break_time']].values.tolist()
    y = df['focus_score'].tolist()
    return X, y

def optimize_round():
    opt = Optimizer(
        dimensions=[(15.0, 60.0), (3.0, 20.0)],  # 作業時間20-60分、休憩時間3-20分
        base_estimator=GaussianProcessRegressor(kernel=Matern(length_scale=1.0)),
        n_initial_points=10,
        acq_func="EI"
    )
    
    opt.tell(*load_data_from_csv("../../data/round_data.csv"))
    
    next_x = opt.ask()
    work_time, break_time = next_x

    return work_time, break_time



work_time, break_time = optimize_round()
print("提案された作業時間: ", work_time)
print("提案された休憩時間: ", break_time)