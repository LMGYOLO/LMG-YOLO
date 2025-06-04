import pandas as pd

# 读取CSV文件
df = pd.read_csv('runs/train/exp15/results.csv')

# 对指定的列进行除以100的操作
columns_to_divide = ['metrics/mAP50-95(B)', 'metrics/mAP50(B)', 'metrics/precision(B)', 'metrics/recall(B)']
df[columns_to_divide] = df[columns_to_divide] / 100

# 保存处理后的CSV文件
df.to_csv('runs/train/exp15/results1.csv', index=False)
