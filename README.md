# CCU-UAV-bird-view-dataset
Taiwan CCU UAV bird-view dataset for [CLIP-UAV-localization](https://github.com/codebra721/CLIP-UAV-localization)
## Step
install anaconda environment
```bash
conda env create -f myensv.yml
```
that you can run all code pack python code
## Code_pack Describe 
- UAV_pick.py:
  
  It is for combine UAV bird-view photo and CCU satellite image to a training dataset
- calibration.py:
  
  It is for calibration Gopro camera(test use)
- clik_crop.py:
  
  It is to crop satellite image to property size
- combine.py:
  
  It is to fit UAV coordinate csv and image path to a combine csv(training dataset)
- crop_sat.py:
  
  It is to crop big satellite to 800x800 size image to training dataset
- extract.py:
  
  It is to extrcact big satellite .tif all Geo-information to model(test use)
- kmz2csv.py:
  
  It is change fly log .kmz to .csv
## dataset
I storage my dataset in synology please use [this_link](https://gofile.me/7uply/w8UKyP7yI), then enter the password enter file to download datset.

password: please notice me, that I will sent you password
