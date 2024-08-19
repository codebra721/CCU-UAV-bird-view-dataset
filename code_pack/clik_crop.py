import cv2
import numpy as np
import rasterio
from rasterio.windows import Window

# 初始化點擊的點的列表
points = []

# 定義滑鼠回調函數
def click_and_crop(event, x, y, flags, param):
    # 如果左鍵被點擊，記錄下點的位置
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))

        # 如果已經點擊了四個點，則畫出矩形並顯示裁剪後的圖片
        if len(points) == 4:
            rect = cv2.boundingRect(np.array(points))
            cropped = image[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]
            cropped_rgb = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)  # 將 BGR 轉換為 RGB
            cv2.namedWindow("Cropped", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Cropped", 800, 600)
            cv2.imshow("Cropped", cropped_rgb)

            # 使用 rasterio 保存裁剪的影像並保留地理參考資訊
            with rasterio.open('satellite/ccu.tif') as src:
                transform = src.transform
                profile = src.profile

            new_transform = rasterio.Affine.translation(rect[0] * transform.a, rect[1] * transform.e) * transform
            profile.update({
                "height": rect[3],
                "width": rect[2],
                "transform": new_transform,
                "count": 3})

            with rasterio.open('satellite/big_cropped_ccu.tif', 'w', **profile) as dst:
                dst.write(cropped_rgb.transpose((2, 0, 1)).astype(rasterio.float32))

# 讀取影像
image = cv2.imread('satellite/ccu.tif')

# 創建一個名為 "image" 的視窗並設定滑鼠回調函數
cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("image", 800, 600)
cv2.setMouseCallback("image", click_and_crop)

# 保持視窗開啟直到 'q' 鍵被按下
while True:
    # 顯示影像
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

    # 如果 'q' 鍵被按下，跳出迴圈
    if key == ord("q"):
        break

# 關閉所有視窗
cv2.destroyAllWindows()