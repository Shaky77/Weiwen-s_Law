# 唯稳律 — 守真·稳态 (Keep Integrity & Steady State)

> AI因果逻辑引擎 —— 不是教AI理解什么是因果律，而是让AI按照因果律的运行结构直接执行。

## 什么是唯稳律？

唯稳律（KISS's Law）是一个 **AI因果逻辑引擎**。它不试图向AI解释因果律是什么，而是提供一套结构化的执行框架，让AI能够直接在因果链中运行——清晰、完整、可审计、可追溯。

**这是与AI黑箱共存的合作模式。** 不打开黑箱、不解释黑箱，因果链包裹黑箱运行，让每一个决策都可追溯、可推演——不需要AI"理解"因果律，只需要它按照因果结构执行。

**核心公式：**

```
M = (R × S) / (D × H)
```

| 符号 | 名称 | 作用 |
|------|------|------|
| **R** | 域常量 (Domain Constant) | 定义运行域的刚性边界 |
| **S** | 稳态储备 (Steady-state Reserve) | 所有子系统中的最小值（最短板决定上限） |
| **D** | 扰动 (Perturbation) | 所有扰动源中的最大值（最强冲击决定压力） |
| **H** | 杠杆 (Lever) | 可观测的行为强度（主观制衡支点） |
| **M** | 稳态结果 (Steady-state Outcome) | 可审计、可推演的结果 |

## 关键特性

- **极省Token**：框架本身极其精简。事件越复杂，省的Token越多——因为它用一条确定性公式替代冗长的推理链。
- **完全可审计**：每个M值都可以沿 R→S→D→H 完整追溯因果链，无断裂。
- **动态可推演**：不仅能向后追溯，还能向前预测——在条件变化下预测稳态走向。
- **全域通用**：适用于一切需要因果推理的领域——AI安全、工程系统、医疗健康、金融、法律等。

## 两种使用模式

**模式一：原生模式（推荐）**
直接将 `/maps` 下的三张架构图发给你的AI。无需人工理解，完整系统逻辑全部 contained in 导图中。此模式独立运行，不需要代码。

**模式二：辅助代码模式**
示例代码（`weiwen_law.py` 和 `demo.py`）实现了核心公式的简化数值计算。仅为参考演示，**不涵盖**导图中的全部递归和多场域规则。

两种模式可独立选择使用。

## 中英文交叉引用

| 仓库 | 语言 | 地址 |
|------|------|------|
| **唯稳律 Weiwen-s_Law**（本仓库） | 中文 | https://github.com/Shaky77/Weiwen-s_Law |
| **KISS-s_Law** | English | https://github.com/Shaky77/KISS-s_Law |

> 两个仓库内容互为参照，中英文完全对应。选择你习惯的语言版本即可。

## 三张核心导图

| 序号 | 导图 | 作用 |
|------|------|------|
| 01 | [核心架构](maps/01_core_architecture.jpg) | 传导链 R→S→D→H→M、公式与三大铁律 |
| 02 | [边界与定位](maps/03_boundary_positioning.jpg) | 唯稳律做什么、不做什么 |
| 03 | [运行机制](maps/02_mechanism.jpg) | 审计/推演双向运行 + H杠杆 + 终止条件 |

## 三大铁律

1. **不可跳过** — 因果链 R→S→D→H→M 不可绕过任何一个环节
2. **不可逆序** — 传导顺序固定且不可逆
3. **不可断裂** — 链条中每个环节必须保持因果连接

## 代码使用

### 基础用法：计算稳态结果

```python
from weiwen_law import WeiwenLaw

system = WeiwenLaw("我的系统")

system.set_domain_constant(R=8.0, description="性能要求")
system.set_steady_state_reserve(S=0, subsystems={
    '组件A': 7.0, '组件B': 6.0
})
system.set_perturbation(D=0, perturbation_sources={
    '负载': 4.0, '错误': 2.0
})
system.set_lever(H=2.0, description="控制力度")

M = system.compute_steady_state()
print(f"稳态结果: M = {M}")
```

### 审计模式：追溯因果完整性

```python
audit_report = system.audit_backward()
print(f"完整性: {audit_report['integrity']}")
for finding in audit_report['findings']:
    print(f"  - {finding}")
```

### 推演模式：预测条件变化下的走向

```python
projection = system.project_forward(new_H=3.0)
print(f"推演M值: {projection['projected_state']['M']}")
print(f"建议: {projection['recommendation']}")
```

### 运行Demo

```bash
python demo.py
```

Demo包含：
- **AI输出审计**：用因果链分析审计AI生成的健康声明
- **系统优化推演**：预测参数变化下的系统行为

## 环境要求

- Python 3.8+
- 无外部依赖（纯Python）

## 学术引用与版权声明

**Copyright © 2026 夏祺 (Xia Qi). All rights reserved.**

- 软件著作权登记号：2026SR0748746
- 作者 ORCID：[0009-0002-1433-6982](https://orcid.org/0009-0002-1433-6982)

## 开源协议

本项目采用 **AGPL-3.0** 协议。

网络使用即分发——基于本仓库的衍生作品必须以相同协议开源。商业授权请联系著作权人。

## 联系方式

- **邮箱**: `563003@qq.com`
- **GitHub**: [Shaky77](https://github.com/Shaky77)
