import os
import pandas as pd
import random

# 定义图像文件夹路径和CSV文件路径
image_folder = 'image/place_5/'
csv_file = 'row_csv/gps_5.csv'
output_csv_file = 'gps_csv/place_5_coordinate.csv'

# 读取经纬度信息的CSV文件
coordinates_df = pd.read_csv(csv_file)
print(len(coordinates_df))
# 获取图像文件夹中所有图像文件的文件名
image_files = sorted(os.listdir(image_folder))  # 对图像文件进行排序
for i, image_file in enumerate(image_files):
    old_path = os.path.join(image_folder, image_file)
    new_path = os.path.join(image_folder, f"Image_{i:04d}.png")  # 修改文件名的逻辑可以根据需求自定义
    os.rename(old_path, new_path)
    
# 创建一个空列表来存储图像文件名和对应的经纬度信息
image_files = sorted(os.listdir(image_folder)) 
merged_data_list = []

# 将图像文件名和对应的经纬度信息依次添加到merged_data_list中
for i, image_file in enumerate(image_files):
    # 确保不超出 coordinates_df 的行数
    if i < len(coordinates_df):
        # 获取对应的经纬度信息
        latitude = coordinates_df.iloc[i]['LAT']
        longitude = coordinates_df.iloc[i]['LON']
        heading = coordinates_df.iloc[i]['HEA']
        # 将图像文件名和对应的经纬度信息添加到merged_data_list中
        merged_data_list.append({
            'IMG_FILE': os.path.join("place_5", image_file),
            'LAT': latitude,
            'LON': longitude,
            'HEA': heading})
    else:
        print(f"Warning: No coordinates found for image {image_file}. Skipping.")

# 将merged_data_list转换为DataFrame
merged_data = pd.DataFrame(merged_data_list)

# 将整合后的数据保存到新的CSV文件中
merged_data.to_csv(output_csv_file, index=False)