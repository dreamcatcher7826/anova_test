# 🤖 机器人控制算法 ANOVA 性能分析

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data Analysis](https://img.shields.io/badge/Analysis-ANOVA-green.svg)](https://github.com/dreamcatcher7826/anova_test)

## 📋 项目简介

本项目使用**单因素方差分析（One-way ANOVA）**比较不同机器人控制算法的性能差异，为项目管理中的算法选型提供数据支持。

### 🎯 分析目标

比较三种主流控制算法在控制精度上的表现：
- **PID** (比例-积分-微分控制)
- **LQR** (线性二次调节器)
- **MPC** (模型预测控制)

### 🔬 统计方法

- **方法**: 单因素方差分析 (One-way ANOVA)
- **显著性水平**: α = 0.05
- **评估指标**: 控制误差（单位：毫米）

---

## 🚀 快速开始

### 环境要求

```bash
Python >= 3.8
```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行分析

```bash
# 1. 生成测试数据
python generate_algorithm_data.py

# 2. 执行ANOVA分析（会显示可视化图表）
python algorithm_anova_analysis.py

# 3. 生成详细报告
python generate_anova_report.py
```

---

## 📊 分析流程

```
数据生成 → 数据探索 → ANOVA检验 → 统计显著性判断 → 可视化分析 → 生成报告 → 管理建议
```

---

## 📈 预期输出

### 1. 数据文件
- `algorithm_performance_data.csv` - 算法性能测试数据

### 2. 可视化结果
- `algorithm_anova_visualization.png` - 小提琴图和箱线图

### 3. 分析报告
- `ANOVA_Analysis_Report.md` - 详细的统计分析报告

---

## 📖 ANOVA 分析原理

### 核心思想
通过比较**组间变差**和**组内变差**来判断不同组之间是否存在显著差异。

### 计算步骤

1. **总变差** = Σ(x - x̄)²
2. **组内变差** = Σ(x - x̄ᵢ)² （组内数据与组内均值的偏差）
3. **组间变差** = 总变差 - 组内变差
4. **F统计量** = (组间方差) / (组内方差)
5. **显著性检验**: F值 > 临界值 → 拒绝零假设

### 假设检验

- **H₀ (零假设)**: 三种算法的平均控制误差无显著差异
- **H₁ (备择假设)**: 至少有一种算法的平均控制误差存在显著差异

---

## 📚 应用场景

### 项目管理中的应用

1. **算法选型决策**
   - 量化不同算法的性能差异
   - 为技术选型提供数据支持

2. **资源优化配置**
   - 识别最优算法方案
   - 减少研发试错成本

3. **团队协作工具比较**
   - 代码审查工具效率分析
   - 开发框架性能对比

4. **A/B/C 测试**
   - 多方案效果评估
   - 统计学显著性验证

---

## 📊 示例结果

```
ANOVA 检验结果：
  F 统计量:        32.45
  临界值 (α=0.05): 3.10
  p 值:            0.0001
  是否显著:        是 ✓

✓ 结论：拒绝零假设 (H0)
  三种算法的控制误差存在统计学上的显著差异

✓ 推荐算法: MPC
  平均控制误差最小: 7.12 mm
```

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出改进建议！

---

## 📝 许可证

本项目采用 MIT 许可证

---

## 👨‍💻 作者

**dreamcatcher7826**

- GitHub: [@dreamcatcher7826](https://github.com/dreamcatcher7826)

---

## 🙏 致谢

- 统计方法基于经典的单因素方差分析理论
- 可视化使用 seaborn 和 matplotlib 库
- 感谢开源社区的支持

---

**⭐ 如果这个项目对你有帮助，请给个 Star！