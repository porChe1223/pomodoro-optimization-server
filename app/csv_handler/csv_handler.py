import os
import pandas as pd

class CSVHandler:
    """CSVファイルを操作するクラス

    Attributes:
        file_path: str // CSVファイルの位置
        df: DataFrame // CSVファイルのデータ
    Methods:
        __init__(file_path: str) // CSVファイルの読み込み
        get_specific_columns_and_rows_data(columns: list[str], rows: list[int] | slice) // 特定のカラムと行を取得
    """
    def __init__(self, file_path):
        """ファイルの読み込み

        Args:
            file_path: str // CSVファイルの位置
        """
        try:
            # CSVファイルのパスを定義
            self.file_path = file_path
            # CSVファイルの存在確認
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            # CSVファイルの読み込み
            self.df = pd.read_csv(self.file_path)

        except Exception as e:
            print(f"CSVファイルの読み込みに失敗しました->\n {e}")
            raise {f"CSVファイルの読み込みに失敗しました->\n {e}"}


    def get_specific_data(self, columns: list[str] = None, rows: list[int] | slice = None):
        """CSVファイルの特定のカラムと行を取得
        Args:
            columns: list[str] // 取得したいカラム
            rows: list[int] | slice // 取得したい行
        Useage:
            columns=["work_time", "break_time"], rows=slice(0,2)
            columns=["work_time", "break_time"], rows=slice(0,None)
            columns=["work_time"], rows=None
            columns=None, rows=slice(0,2)
        Returns:
            specific_columns_and_rows_data: DataFrame // 特定のカラムと行のデータ
        """
        try:
            # カラムと行の取得
            if columns and rows is not None:
                specific_columns_and_rows_data = self.df.iloc[rows][columns]
            # カラムのみの取得            
            elif columns is not None and rows is None:
                specific_columns_and_rows_data = self.df[columns]
            # 行のみの取得
            elif rows is not None and columns is None:
                specific_columns_and_rows_data = self.df.iloc[rows]
            
            else:
                raise ValueError("カラムか列のいずれかを指定してください")
            
            return specific_columns_and_rows_data
        
        except Exception as e:
            print(f"CSVファイルの特定のカラムと行の取得に失敗しました->\n{e}")
            raise {f"CSVファイルの特定のカラムと行の取得に失敗しました->\n {e}"}



if __name__ == "__main__":
    csv_handler = CSVHandler("../../data/round_data.csv")
    print(csv_handler.get_specific_data( columns=["work_time", "break_time"], rows=slice(None,None)))