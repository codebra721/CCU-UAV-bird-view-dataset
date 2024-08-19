import os
import pandas as pd

# 設定資料夾路徑
folder_path = 'gps_csv'

# 獲取資料夾中的所有 csv 文件
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 讀取 image_info.csv 文件的列名稱
with open('image_info_bigeat.csv', 'r') as f:
    column_names = f.readline().strip().split(',')

# 初始化一個空的 DataFrame 來保存選取的資料
selected_data = pd.DataFrame(columns=column_names)

# 遍歷每一個 csv 文件
for csv_file in csv_files:
    # 讀取 csv 文件
    df = pd.read_csv(os.path.join(folder_path, csv_file))

    # 確保 df 有相同的列名稱
    df = df[column_names]

    # 在 'IMG_FILE' 列的值前面添加 'image/'
    df['IMG_FILE'] = df['IMG_FILE'].apply(lambda x: 'image/' + x)
    df['HEA'] = df['HEA'].apply(lambda x: 180 - x - 90)
    # 隨機選取 50 筆資料
    selected = df.sample(n=50)

    # 將選取的資料添加到 selected_data 中
    selected_data = pd.concat([selected_data, selected], ignore_index=True)

# 將選取的資料寫入 image_info.csv 文件
selected_data.to_csv('image_info_bigeat.csv', mode='a', header=False, index=False)