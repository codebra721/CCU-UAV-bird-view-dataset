import pandas as pd
import random

# 读取CSV文件
df = pd.read_csv('row_csv/gps_4_cut_new.csv')
fin_num = 400
# 获取原始数据笔数
original_length = len(df)
print(f"原始数据笔数: {original_length}")

# 先随机删除一部分数据,使剩余数据笔数可以被 440 整除
remainder = original_length % fin_num
if remainder > 0:
    remove_indices = random.sample(range(original_length), remainder)
    df = df.drop(df.index[remove_indices])

# 获取删减后的数据笔数
new_length = len(df)
print(f"删减后的数据笔数: {new_length}")

# 计算采样间隔
sample_interval = new_length // fin_num

# 通过间隔采样获取新的数据框
new_df = df.iloc[::sample_interval, :]

# 获取降采样后的数据笔数
final_length = len(new_df)
print(f"降采样后的数据笔数: {final_length}")

# 将结果存储到新的CSV文件
new_df.to_csv('new_file.csv', index=False)