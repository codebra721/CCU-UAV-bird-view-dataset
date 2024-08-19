
import cv2
import numpy as np
import os
from tqdm import tqdm
import concurrent.futures

# 定義棋盤格的大小和角點數量
CHECKERBOARD = (8,10)
subpix_criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC+cv2.fisheye.CALIB_CHECK_COND+cv2.fisheye.CALIB_FIX_SKEW

# 讀取資料夾中的所有影像
folder = 'camera_calibration/'
# images = [cv2.imread(os.path.join(folder, f)) for f in os.listdir(folder) if f.endswith('.png')]
print("---------detect point-----------------")
# 檢測棋盤格角點
corners_list = []
files = [f for f in os.listdir(folder) if f.endswith('.png')]
gray = None  # 初始化 gray 變數
for file in tqdm(files):
    img = cv2.imread(os.path.join(folder, file))
    gray_temp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray_temp, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH+cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)
    if ret == True:
        cv2.cornerSubPix(gray_temp,corners,(3,3),(-1,-1),subpix_criteria)
        corners_list.append(corners)
        if gray is None:  # 如果 gray 還沒有被定義，則將當前的灰度圖像存儲為 gray
            gray = gray_temp
    del img, gray_temp  # 釋放圖像記憶體
print("---------detect point done-----------------")
# 創建 objectPoints 列表
objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
objpoints = [objp]*len(corners_list)

# 校準魚眼鏡頭
N_OK = len(corners_list)
K = np.zeros((3, 3))
D = np.zeros((4, 1))
rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
retval, K, D, rvecs, tvecs = cv2.fisheye.calibrate(
    objpoints,
    corners_list,
    gray.shape[::-1],
    K,
    D,
    rvecs,
    tvecs,
    calibration_flags,
    (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
)
print("---------start calibration-----------------")
# 讀取另一個資料夾中的所有影像進行校正
correction_folder = 'drone/place_5/'  # 修改為您的要校正的圖片資料夾路徑

# 使用校準參數進行影像校正並顯示校正後的影像
map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, gray.shape[::-1], cv2.CV_16SC2)
output_folder = 'image/place_5/'  # 修改為您的輸出資料夾路徑
files = [f for f in sorted(os.listdir(correction_folder)) if f.endswith('.png')]
for i, file in enumerate(tqdm(files)):
    img = cv2.imread(os.path.join(correction_folder, file))
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imwrite(os.path.join(output_folder, f'image_{i:04d}.png'), undistorted_img)
    del img, undistorted_img  # 釋放圖像記憶體

cv2.destroyAllWindows()
