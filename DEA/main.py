import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# 输入数据：每个DMU的输入和输出指标
# 输入指标：x1, x2
# 输出指标：y1, y2
data = np.array([
    [2, 3, 4, 5],
    [1, 2, 6, 7],
    [3, 4, 8, 9],
    [4, 5, 10, 11]
])

# 定义DMU的个数和指标个数
num_dmu, num_indicators = data.shape

# 设置目标函数的系数
c = np.zeros(num_dmu)
c[0] = 1

# 设置约束条件：每个DMU的输入指标和输出指标的系数
A_eq = np.zeros((num_indicators, num_dmu))
A_eq[:, 1:] = -data[:, 1:]
b_eq = data[:, 0]

# 设置上界约束
bounds = [(0, None)] * num_dmu

# 使用线性规划求解DEA模型
result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds)

# 提取最优权重和效率
weights = result.x
efficiency = 1 / result.fun

# 绘制效率图
dmu_labels = ['DMU1', 'DMU2', 'DMU3', 'DMU4']
x = np.arange(len(dmu_labels))
plt.bar(x, efficiency, align='center', alpha=0.5)
plt.xticks(x, dmu_labels)
plt.xlabel('DMU')
plt.ylabel('Efficiency')
plt.title('DEA Efficiency')
plt.ylim(0, 1.1)
plt.show()

# 输出结果
print("最优权重：", weights)
print("最大效率：", efficiency)