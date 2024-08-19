import os
import numpy as np
import rasterio
from PIL import Image
from tqdm import tqdm
import concurrent.futures
import pandas as pd
from pyproj import Transformer
import time
import matplotlib.pyplot as plt
import cv2
import math

def calculate_pixels_to_crop(height, fov_h, fov_v, pixel_resolution):
    width = 2 * height * math.tan(math.radians(fov_h / 2))
    height = 2 * height * math.tan(math.radians(fov_v / 2))
    pixels_w = int(width / pixel_resolution)
    pixels_h = int(height / pixel_resolution)
    return pixels_w, pixels_h

def process_image(i, angle):
    np.random.seed(int(time.time()) + i)  # 確保每次切割的位置都是隨機的
    
    # 獲取旋轉後影像的大小
    rows, cols = image.shape[1], image.shape[2]
    rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    cos = np.abs(rotation_matrix[0, 0])
    sin = np.abs(rotation_matrix[0, 1])
    new_cols = int(rows * sin + cols * cos)
    new_rows = int(rows * cos + cols * sin)
        # 設定無人機參數
    # drone_height = 100  # 無人機高度（米）
    # fov_h = 87.6  # 水平FOV
    # fov_v = 56.7  # 垂直FOV
    # pixel_resolution = 0.5  # 像素分辨率（米/像素）
    # size_x, size_y = calculate_pixels_to_crop(drone_height, fov_h, fov_v, pixel_resolution)
    
    while True:
        # 隨機選擇一個中心點
        center_x = np.random.randint(size_x / 2, cols - size_x / 2)
        center_y = np.random.randint(size_y / 2, rows - size_y / 2)

        # 計算經緯度
        lon, lat = rasterio.transform.xy(src.transform, center_y, center_x)

        # 轉換到 WGS84 坐標系統
        transformer = Transformer.from_crs(src.crs, "EPSG:4326", always_xy=True)
        lon_wgs84, lat_wgs84 = transformer.transform(lon, lat)

        # 對原始影像進行旋轉
        rotated_image = cv2.warpAffine(image.transpose(1, 2, 0), rotation_matrix, (new_cols, new_rows), borderValue=(0, 0, 0))
        rotated_image = rotated_image.transpose(2, 0, 1)

        # 計算旋轉後的起始點
        start_x_rot = int(center_x - size_x / 2)
        start_y_rot = int(center_y - size_y / 2)

        # 確保起始點和切割大小在旋轉後的圖像的範圍內
        if start_x_rot < 0 or start_y_rot < 0 or start_x_rot + size_x > new_cols or start_y_rot + size_y > new_rows:
            continue

        # 切割影像
        sub_image = rotated_image[:, start_y_rot:start_y_rot+size_y, start_x_rot:start_x_rot+size_x]
        
        # 檢查四個角點是否包含黑色區域
        if np.any(sub_image[:, 0, 0] == 0) or np.any(sub_image[:, 0, -1] == 0) or \
           np.any(sub_image[:, -1, 0] == 0) or np.any(sub_image[:, -1, -1] == 0):
            continue  # 如果任一角點包含黑色區域,則跳過該影像
        
        # 將影像從 (channels, height, width) 轉換為 (height, width, channels)
        image_to_save = np.transpose(sub_image, (1, 2, 0))
        
        # 保存影像
        output_path = os.path.join(output_folder, f'image_{i:04d}.png')
        Image.fromarray(image_to_save.astype(np.uint8)).save(output_path)
        angle = 360-angle
        # 返回圖片檔名和經緯度
        return {"IMG_FILE": output_path, "LON": lon_wgs84, "LAT": lat_wgs84,"HEA": angle}
    
# 讀取 TIF 衛星影像
with rasterio.open('satellite/big_cropped_ccu.tif') as src:
    image = src.read(out_dtype=rasterio.uint8)

# 獲取影像的寬度和高度
height, width = image.shape[1:]
print(f"Image size: {width} x {height}")
size_x = 800
size_y = 800
dataset_num = 1000

# 創建一個新的資料夾來保存切割的影像
output_folder = 'sat_img/test/'
os.makedirs(output_folder, exist_ok=True)

# # 生成10個不同的旋轉角度
# rotation_angles = np.random.uniform(0.0, 360.0, size=dataset_num)

# 生成均勻分佈的旋轉角度
rotation_angles = np.linspace(0.0, 360.0, num=dataset_num)

# 打亂角度
np.random.shuffle(rotation_angles)
# 使用 concurrent.futures 進行平行處理
with concurrent.futures.ProcessPoolExecutor() as executor:
    results = list(tqdm(executor.map(process_image, range(dataset_num), rotation_angles), total=dataset_num))

# 將結果寫入 CSV 檔案
df = pd.DataFrame(results)
df.to_csv('image_info_test.csv', index=False)
print("All done!")