from osgeo import gdal
import numpy as np
import cv2

# 讀取 TIF 文件
dataset = gdal.Open('satellite/big_cropped_ccu.tif')
if dataset is None:
    raise Exception("無法打開 TIF 文件")

# 讀取所有波段
bands = [dataset.GetRasterBand(i + 1).ReadAsArray() for i in range(dataset.RasterCount)]

# 組合波段（假設是 RGB 順序）
if len(bands) >= 3:
    image = np.dstack((bands[0], bands[1], bands[2]))
else:
    raise Exception("TIF 文件波段數量不足")

# 正規化數據到 0-255 範圍
image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
image = image.astype(np.uint8)

# 保存為 PNG
cv2.imwrite('output_image.png', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))