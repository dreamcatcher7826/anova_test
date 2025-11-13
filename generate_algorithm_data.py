"""
生成机器人控制算法性能测试数据
模拟三种算法（PID、LQR、MPC）在控制误差上的表现
"""
import numpy as np
import pandas as pd

# 设置随机种子以保证结果可复现
np.random.seed(42)

# 定义样本数量（每个算法测试次数）
n_samples = 30

# 生成三种算法的控制误差数据（单位：毫米）
# PID: 平均误差较大，波动较大
pid_errors = np.random.normal(loc=15.0, scale=4.0, size=n_samples)

# LQR: 平均误差中等，波动较小
lqr_errors = np.random.normal(loc=10.0, scale=3.0, size=n_samples)

# MPC: 平均误差最小，波动最小
mpc_errors = np.random.normal(loc=7.0, scale=2.5, size=n_samples)

# 确保误差值为正数
pid_errors = np.abs(pid_errors)
lqr_errors = np.abs(lqr_errors)
mpc_errors = np.abs(mpc_errors)

# 创建数据框
data = {
    'error': np.concatenate([pid_errors, lqr_errors, mpc_errors]),
    'algorithm': ['PID'] * n_samples + ['LQR'] * n_samples + ['MPC'] * n_samples
}

df = pd.DataFrame(data)

# 保存为 CSV 文件
df.to_csv('algorithm_performance_data.csv', index=False)

print("数据生成完成！")
print("\n数据预览：")
print(df.head(10))
print("\n各算法统计信息：")
print(df.groupby('algorithm')['error'].describe())