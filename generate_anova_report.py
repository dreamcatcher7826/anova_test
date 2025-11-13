"""
生成 ANOVA 分析详细报告（Markdown 格式）
注：此版本已将ANOVA逻辑直接整合，无需外部依赖
"""
import pandas as pd
import scipy.stats as st
from datetime import datetime

def perform_anova_test(numeric_col, category_col, dataframe, alpha=0.05):
    """执行单因素方差分析"""
    values = dataframe[numeric_col]
    categories = dataframe[category_col]
    groups = categories.unique()
    
    total_variance = ((values - values.mean()) ** 2).sum()
    
    within_group_variance = 0
    for group in groups:
        group_values = values[categories == group]
        group_mean = group_values.mean()
        within_group_variance += ((group_values - group_mean) ** 2).sum()
    
    between_group_variance = total_variance - within_group_variance
    
    dfn = len(groups) - 1
    dfd = len(values) - len(groups)
    between_variance = between_group_variance / dfn
    within_variance = within_group_variance / dfd
    f_value = between_variance / within_variance
    
    threshold = st.f.ppf(1 - alpha, dfn=dfn, dfd=dfd)
    p_value = 1 - st.f.cdf(f_value, dfn=dfn, dfd=dfd)
    is_significant = (f_value >= threshold)
    
    return round(f_value, 4), round(threshold, 4), is_significant, round(p_value, 4)

def generate_markdown_report():
    """生成 Markdown 格式的分析报告"""
    
    print("正在生成 ANOVA 分析报告...")
    
    try:
        df = pd.read_csv('algorithm_performance_data.csv')
        print(f"✓ 数据加载成功 ({len(df)} 条记录)")
    except FileNotFoundError:
        print("✗ 错误：未找到 'algorithm_performance_data.csv' 文件")
        print("请先运行: python generate_algorithm_data.py")
        return
    
    print("正在执行 ANOVA 分析...")
    f_value, threshold, significant, p_value = perform_anova_test(
        'error', 'algorithm', df, alpha=0.05
    )
    
    stats = df.groupby('algorithm')['error'].agg(['mean', 'std', 'min', 'max', 'count'])
    
    report = f"""# 机器人控制算法 ANOVA 分析报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**分析方法**: 单因素方差分析 (One-way ANOVA)  
**显著性水平**: α = 0.05

---

## 1. 研究目的

比较三种主流机器人控制算法（PID、LQR、MPC）在控制精度上的差异，为项目算法选型提供数据支持。

## 2. 假设检验

- **零假设 (H₀)**: 三种算法的平均控制误差无显著差异
- **备择假设 (H₁)**: 至少有一种算法的平均控制误差存在显著差异

## 3. 数据概览

| 算法 | 样本数 | 平均误差 (mm) | 标准差 (mm) | 最小值 (mm) | 最大值 (mm) |
|------|--------|---------------|-------------|-------------|-------------|
| PID  | {int(stats.loc['PID', 'count'])} | {stats.loc['PID', 'mean']:.2f} | {stats.loc['PID', 'std']:.2f} | {stats.loc['PID', 'min']:.2f} | {stats.loc['PID', 'max']:.2f} |
| LQR  | {int(stats.loc['LQR', 'count'])} | {stats.loc['LQR', 'mean']:.2f} | {stats.loc['LQR', 'std']:.2f} | {stats.loc['LQR', 'min']:.2f} | {stats.loc['LQR', 'max']:.2f} |
| MPC  | {int(stats.loc['MPC', 'count'])} | {stats.loc['MPC', 'mean']:.2f} | {stats.loc['MPC', 'std']:.2f} | {stats.loc['MPC', 'min']:.2f} | {stats.loc['MPC', 'max']:.2f} |

## 4. ANOVA 检验结果

| 统计量 | 数值 |
|--------|------|
| F 统计量 | {f_value} |
| 临界值 (F₀.₀₅) | {threshold} |
| p 值 | {p_value} |
| **检验结果** | **{'显著 ✓' if significant else '不显著 ✗'}** |

## 5. 结果解释

{'### ✓ 拒绝零假设' if significant else '### ✗ 不能拒绝零假设'}

{f'在 α=0.05 的显著性水平下，F 统计量 ({f_value}) 大于临界值 ({threshold})，p 值 ({p_value}) 小于 0.05。' if significant else f'在 α=0.05 的显著性水平下，F 统计量 ({f_value}) 小于临界值 ({threshold})，p 值 ({p_value}) 大于 0.05。'}

{'**结论**: 三种控制算法的控制误差存在统计学上的显著差异。' if significant else '**结论**: 三种控制算法的控制误差没有统计学上的显著差异。'}

## 6. 管理建议

{'### 算法优选建议' if significant else '### 综合考虑因素'}

{f'''1. **推荐算法**: {stats['mean'].idxmin()}
   - 平均控制误差最小: {stats['mean'].min():.2f} mm
   - 性能最优，适合高精度控制场景

2. **备选算法**: {stats['mean'].sort_values().index[1]}
   - 平均控制误差: {stats['mean'].sort_values().values[1]:.2f} mm
   - 性能适中，可用于一般精度要求场景

3. **不推荐**: {stats['mean'].idxmax()}
   - 平均控制误差最大: {stats['mean'].max():.2f} mm
   - 需要进行参数优化或重新设计
''' if significant else '''1. 三种算法性能相当，建议根据以下因素选择：
   - 计算复杂度和实时性要求
   - 实现难度和开发成本
   - 系统鲁棒性和适应性
   - 团队技术储备和经验
'''}

## 7. 可视化结果

![ANOVA 可视化分析](algorithm_anova_visualization.png)

---

**报告生成工具**: Python + scipy.stats  
**数据文件**: algorithm_performance_data.csv  
**项目仓库**: https://github.com/dreamcatcher7826/anova_test
""";
    
    with open('ANOVA_Analysis_Report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✓ 报告已生成: ANOVA_Analysis_Report.md")
    print(f"\n报告概要：")
    print(f"  - F 统计量: {f_value}")
    print(f"  - p 值: {p_value}")
    print(f"  - 结论: {'显著差异' if significant else '无显著差异'}")

if __name__ == '__main__':
    generate_markdown_report()