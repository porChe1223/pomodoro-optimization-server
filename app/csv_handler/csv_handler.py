import os
import pandas as pd

class CSVHandler:
    """CSVファイルを操作するクラス

    __init__:
        ファイルのパス定義
    read_csv:
        CSVファイルを読み込む関数

    """
    def __init__(self, file_path):
        """ファイルのパス定義

        Args:
            file_path: str // CSVファイルの位置
        """
        # CSVファイルのパスを定義
        self.file_path = file_path
        # CSVファイルの存在確認
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

    def read_csv(self):
        """CSVファイルを読み込む
        
        Returns:
            df: DataFrame // CSVファイルのデータ
        """
        df = pd.read_csv(self.file_path)

        return df

    def write_csv(self, df):
        """CSVファイルに書き込む"""
        df.to_csv(self.file_path, index=False)


if __name__ == "__main__":
    # 使用例
    csv_handler = CSVHandler("../pomodoro_optimization_log.csv")
    data = csv_handler.read_csv()
    print(data)