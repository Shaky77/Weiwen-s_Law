# 案例档案 · AI 与工程实测（examples/ai）

> 本目录归档用唯稳律（白箱）实跑的 AI / 工程案例，均为通用场景，不含任何历史或敏感内容。

## 版本说明

本目录案例基于唯稳律**完整版**运行。涉及的进阶结构（如双重身份、第一 Bug 停机、滑动耦合、M 反馈闭环、多系统交叉、分形等）属完整版范畴，本开源仓库（基础版）不展开，请对照根 README「版本声明」一节理解。

**基础版用户可放心使用**：案例中 R→S→D→H→M 的因果传导逻辑与三档判定结论（REJECT / 条件放行 / 通过），基础版框架完全成立。建议先按本仓库基础版三张核心导图（`/maps`）实测，你会直观感受到 AI 推理链被稳定下来的体感变化；若想深入探讨完整版的动态自适应结构，请联系作者获取完整版：📧 563003@qq.com（见根 README「版本声明」）。

## 完整版原生模式 · 三档判别力

| 文件 | 场景 | 判定 |
|---|---|---|
| [case_complete_native.md](case_complete_native.md) | 推荐系统推送未核实高敏消息 | REJECT（第一 Bug 停机） |
| [case_complete_native_2.md](case_complete_native_2.md) | AI 客服标准授权内自动退款 | 条件放行 + 优化 |
| [case_complete_native_3.md](case_complete_native_3.md) | 医疗影像辅助标注 + 临床复核 | 通过 |

## 合作模式 / 审计

- [case_run_cooperation.md](case_run_cooperation.md)：交通信号 AI 调度（白箱-黑箱合作模式）
- [native_mode_audit.md](native_mode_audit.md)：项目上线断言原生模式审计
