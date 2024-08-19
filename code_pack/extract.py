import os
import rasterio
import pandas as pd
from tqdm import tqdm
from multiprocessing import Pool
from pyproj import Transformer

def process_pixel(args):
    i, j, transform, transformer = args
    # 使用地理轉換參數來計算像素的地理座標
    x, y = transform * (i, j)
    # 轉換座標到 WGS84
    lon, lat = transformer.transform(x, y)
    return (lon, lat)

def extract_coordinates(tif_file):
    # 檢查 tif 文件是否存在
    if not os.path.isfile(tif_file):
        print(f"File {tif_file} does not exist.")
        return None

    # 打開 tif 文件
    with rasterio.open(tif_file) as src:
        # 獲取地理轉換參數
        transform = src.transform

        # 獲取 tif 文件的寬度和高度
        width = src.width
        height = src.height

        # 創建一個空的 DataFrame 來保存座標
        df = pd.DataFrame(columns=['lon', 'lat'])

        # 創建一個座標轉換器
        transformer = Transformer.from_crs(src.crs, 'EPSG:4326', always_xy=True)
        pixel = 50
        # 創建一個進程池
        with Pool(os.cpu_count()) as p:
            # 遍歷 tif 文件的每一個像素，每10個像素讀取一次
            for result in tqdm(p.imap(process_pixel, [(i, j, transform, transformer) for i in range(0, width, pixel) for j in range(0, height, pixel)]), total=(width//pixel)*(height//pixel), desc='Processing'):
                df.loc[len(df)] = result

        return df

# 提取座標並保存到 csv 文件
df = extract_coordinates('satellite/cropped_ccu.tif')
if df is not None:
    df.to_csv('/home/rvl122/geo-clip/geoclip/model/gps_gallery/small50_all_coordinates.csv', index=False)