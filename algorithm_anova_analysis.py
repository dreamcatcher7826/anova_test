"""
机器人控制算法ANOVA分析
比较 PID、LQR、MPC 三种算法的控制误差是否存在显著差异
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as st

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def perform_anova_test(numeric_col, category_col, dataframe, alpha=0.05):
    """
    执行单因素方差分析
    
    Args:
        numeric_col: 数值列名（如控制误差）
        category_col: 分类列名（如算法类型）
        dataframe: 数据框
        alpha: 显著性水平，默认0.05
    
    Returns:
        f_value: F统计量
        threshold: 临界值
        is_significant: 是否显著
        p_value: p值
    """
    values = dataframe[numeric_col]
    categories = dataframe[category_col]
    groups = categories.unique()
    
    # 步骤 1: 计算总变差
    total_variance = ((values - values.mean()) ** 2).sum()
    
    # 步骤 2: 计算组内变差
    within_group_variance = 0
    for group in groups:
        group_values = values[categories == group]
        group_mean = group_values.mean()
        within_group_variance += ((group_values - group_mean) ** 2).sum()
    
    # 步骤 3: 计算组间变差
    between_group_variance = total_variance - within_group_variance
    
    # 计算效应量
    effect_size = between_group_variance / total_variance
    
    # 步骤 4: 计算 F 统计量
    dfn = len(groups) - 1
    dfd = len(values) - len(groups)
    between_variance = between_group_variance / dfn
    within_variance = within_group_variance / dfd
    f_value = between_variance / within_variance
    
    # 步骤 5: 计算临界值和 p 值
    threshold = st.f.ppf(1 - alpha, dfn=dfn, dfd=dfd)
    p_value = 1 - st.f.cdf(f_value, dfn=dfn, dfd=dfd)
    is_significant = (f_value >= threshold)
    
    print(f"\n[ANOVA 计算详情]")
    print(f"  组数: {len(groups)}")
    print(f"  总样本数: {len(values)}")
    print(f"  总变差: {total_variance:.4f}")
    print(f"  组内变差: {within_group_variance:.4f}")
    print(f"  组间变差: {between_group_variance:.4f}")
    print(f"  效应量: {effect_size:.4f}")
    
    return round(f_value, 4), round(threshold, 4), is_significant, round(p_value, 4)

def main():
    """主分析流程"""
    
    print("=" * 60)
    print("机器人控制算法性能 ANOVA 分析")
    print("=" * 60)
    
    # 1. 加载数据
    print("\n[步骤 1] 加载数据...")
    try:
        df = pd.read_csv('algorithm_performance_data.csv')
        print(f"  ✓ 数据加载成功！共 {len(df)} 条记录")
    except FileNotFoundError:
        print("  ✗ 错误：未找到数据文件")
        print("  请先运行: python generate_algorithm_data.py")
        return
    
    # 2. 数据探索
    print("\n[步骤 2] 数据探索性分析...")
    print("\n  各算法样本数量：")
    print(df['algorithm'].value_counts().to_string(header=False).replace('\n', '\n  '))
    
    print("\n  各算法控制误差描述性统计：")
    stats = df.groupby('algorithm')['error'].describe()
    print(stats.to_string().replace('\n', '\n  '))
    
    # 3. 执行 ANOVA 分析
    print("\n[步骤 3] 执行单因素方差分析...")
    print("-" * 60)
    
    f_value, threshold, significant, p_value = perform_anova_test(
        numeric_col='error',
        category_col='algorithm',
        dataframe=df,
        alpha=0.05
    )
    
    print("\n[ANOVA 检验结果]")
    print(f"  F 统计量:        {f_value}")
    print(f"  临界值 (α=0.05): {threshold}")
    print(f"  p 值:            {p_value}")
    print(f"  是否显著:        {'是 ✓' if significant else '否 ✗'}")
    
    # 4. 结果解释
    print("\n[步骤 4] 结果解释...")
    print("-" * 60)
    
    if significant:
        print("  ✓ 结论：拒绝原假设 (H₀)")
        print("    至少有一种算法的控制误差与其他算法存在显著差异")
        print(f"    在 α=0.05 的显著性水平下，F值 ({f_value}) > 临界值 ({threshold})")
    else:
        print("  ✗ 结论：不能拒绝原假设 (H₀)")
        print("    三种算法的控制误差没有显著差异")
    
    # 5. 可视化分析
    print("\n[步骤 5] 生成可视化图表...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 图1：小提琴图
    sns.violinplot(x='algorithm', y='error', data=df, ax=axes[0], palette='Set1')
    axes[0].set_title('Control Error Distribution by Algorithm\n(Violin Plot)', 
                      fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Algorithm', fontsize=11)
    axes[0].set_ylabel('Control Error (mm)', fontsize=11)
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # 图2：箱线图
    sns.boxplot(x='algorithm', y='error', data=df, ax=axes[1], palette='Set2')
    axes[1].set_title('Control Error Distribution by Algorithm\n(Box Plot)', 
                      fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Algorithm', fontsize=11)
    axes[1].set_ylabel('Control Error (mm)', fontsize=11)
    axes[1].grid(True, alpha=0.3, axis='y')
    
    # 在箱线图上标注均值
    means = df.groupby('algorithm')['error'].mean()
    positions = range(len(means))
    for pos, mean_val in zip(positions, means):
        axes[1].plot(pos, mean_val, marker='D', color='red', 
                    markersize=8, label='Mean' if pos == 0 else '')
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig('algorithm_anova_visualization.png', dpi=300, bbox_inches='tight')
    print("  ✓ 图表已保存: algorithm_anova_visualization.png")
    
    # 6. 管理建议
    print("\n[步骤 6] 项目管理建议...")
    print("-" * 60)
    
    if significant:
        best_algorithm = means.idxmin()
        worst_algorithm = means.idxmax()
        
        print(f"  ✓ 推荐算法: {best_algorithm}")
        print(f"    平均控制误差最小: {means[best_algorithm]:.2f} mm")
        print(f"\n  ✗ 不推荐算法: {worst_algorithm}")
        print(f"    平均控制误差最大: {means[worst_algorithm]:.2f} mm")
        print("\n  建议：")
        print("    1. 优先采用控制误差最小的算法")
        print("    2. 对性能较差的算法进行参数调优")
        print("    3. 考虑算法的计算复杂度和实时性要求")
    else:
        print("  三种算法性能相当，可以根据以下因素选择：")
        print("    1. 计算复杂度和实时性")
        print("    2. 实现难度和维护成本")
        print("    3. 对系统参数变化的鲁棒性")
    
    print("\n" + "=" * 60)
    print("分析完成！")
    print("=" * 60)
    
    plt.show()

if __name__ == '__main__':
    main()
