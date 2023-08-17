import pandas as pd #导入pandas工具包
import numpy as np #导入numpy工具包
data = pd.read_excel("F:\Desktop\Python运行文件.xlsx")
# 设置 地区 为索引
data.set_index(['地区'], inplace=True)

data[:5]
# 获取列名称
n = list(data.columns)

# 这里采用均值化法
for i in n:
    data[i] = data[i]/np.average(data[i])
data[:5]
# 这里以最优值为参考数列
A1 = []
# 获取最优列值
for i in n:
    Max = np.max(data[i])
    A1.append(Max)

# 转换形式
A1 = np.array(A1)
A1
m = len(data)
for i in range(m):
    data[i:i+1] = abs(data[i:i+1] - A1)
# 最大值
MAX = []
# 每个指标的最大值
for i in n:
    l = max(data[i])
    MAX.append(l)

MAX = max(MAX)

# 最小值
MIN = []
# 每个指标的最小值
for i in n:
    l = min(data[i])
    MIN.append(l)

MIN = min(MIN)
# 这里 rho 为0.5，可自行调整
for i in n:
    data[i] = (MIN + 0.5 * MAX) / (data[i] + 0.5 * MAX)

data[:5]
