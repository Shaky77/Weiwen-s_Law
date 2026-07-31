"""
演示: 使用唯稳律审计AI输出
============================

    *** 辅助参考代码 ***

完整系统规则全部 contained in /maps 下的三张架构导图中。
本演示仅展示基础公式计算和审计/推演功能 — 不涵盖导图中全部递归和多场域规则。

原生推荐用法：
    直接将导图发给你的AI。无需代码。

---

本演示展示如何使用唯稳律框架审计AI生成的内容
并识别因果完整性问题。

运行: python demo.py
"""

from weiwen_law import WeiwenLaw


def audit_ai_claims():
    """
    实际案例: 审计AI系统的健康声明。
    
    AI声称: "每天喝8杯水可以预防所有肾脏疾病。"
    
    我们将使用唯稳律审计这个声明的因果完整性。
    """
    print("=" * 70)
    print("审计: AI健康声明")
    print("=" * 70)
    print()
    print("声明: '每天喝8杯水可以预防所有肾脏疾病。'")
    print()
    
    # 初始化审计
    audit = WeiwenLaw("健康声明验证")
    
    # R: 域常量
    # 什么是不可协商的边界？在健康声明中，是科学证据。
    audit.set_domain_constant(
        R=9.0,
        description="科学证据阈值 (0-10分)"
    )
    
    # S: 稳态储备
    # 哪些子系统支持这个声明？
    # - 临床研究: 有中等程度证据
    # - 机制理解: 理解良好
    # - 共识一致: 并非普遍认同（有些肾病是遗传的）
    subsystems = {
        '临床研究': 7.0,      # 有一些证据但不具决定性
        '机制理解': 8.5,      # 水合作用机制清晰
        '共识一致': 3.0       # 关键: 并非所有肾病都可预防
    }
    
    audit.set_steady_state_reserve(
        S=0,  # 会自动计算为最小值
        description="支持证据质量",
        subsystems=subsystems
    )
    
    print("子系统分析:")
    for name, val in subsystems.items():
        print(f"  - {name}: {val}")
    print(f"  → S (最薄弱环节) = {min(subsystems.values())}")
    print()
    
    # D: 扰动
    # 哪些干扰影响这个声明的有效性？
    perturbation_sources = {
        '遗传因素': 8.0,      # 高: 很多肾病是遗传的
        '研究冲突': 4.0,       # 有些研究质疑这个声明
        '过度简化': 7.5       # "预防所有"太绝对了
    }
    
    audit.set_perturbation(
        D=0,  # 会自动计算为最大值
        description="有效性扰动",
        perturbation_sources=perturbation_sources
    )
    
    print("扰动分析:")
    for name, val in perturbation_sources.items():
        print(f"  - {name}: {val}")
    print(f"  → D (最强扰动) = {max(perturbation_sources.values())}")
    print()
    
    # H: 杠杆
    # 我们施加多少验证力度？
    audit.set_lever(
        H=1.5,
        description="事实核查力度"
    )
    
    # 计算稳态结果
    M = audit.compute_steady_state()
    
    print(audit.get_summary())
    print()
    
    # 审计声明
    print("=" * 70)
    print("审计发现")
    print("=" * 70)
    audit_report = audit.audit_backward()
    
    print(f"\n因果链完整性: {audit_report['integrity']}")
    
    if audit_report['findings']:
        print("\n发现的问题:")
        for i, finding in enumerate(audit_report['findings'], 1):
            print(f"  {i}. {finding}")
    
    print()
    print("解读:")
    if M < 1.0:
        print("  ⚠️  危急: 声明缺乏因果完整性")
        print("  → 该声明夸大了证据")
        print("  → 共识一致 (S=3.0) 是最薄弱环节")
        print("  → 遗传因素 (D=8.0) 是最强扰动")
        print()
        print("  纠正措施:")
        print("  → 修改声明为: '充足的水分摄入可能降低某些肾脏疾病的风险，")
        print("    但遗传和其他因素也起着重要作用。'")
    elif M < 2.0:
        print("  ⚠️  谨慎: 声明的因果支持有限")
    else:
        print("  ✓ 声明展现因果完整性")
    
    print()
    print("=" * 70)
    print("推演: 如果增加事实核查力度？")
    print("=" * 70)
    
    projection = audit.project_forward(new_H=3.0)
    print(f"当前 M:      {projection['current_state']['M']:.4f}")
    print(f"推演 M:      {projection['projected_state']['M']:.4f}")
    print(f"变化:        {projection['delta_M']:+.4f}")
    print(f"稳定性:      {projection['stability_change']}")
    print(f"建议:        {projection['recommendation']}")
    print()
    print("分析:")
    print("  增加验证力度 (H) 确实改善了 M，")
    print("  但根本问题在于薄弱的子系统 (共识一致)")
    print("  和强扰动 (遗传因素)。")
    print()
    print("  声明需要修改，而不仅仅是更多的事实核查。")
    print()


def project_system_changes():
    """
    示例: 使用推演模式预测条件变化下的系统行为。
    """
    print("=" * 70)
    print("推演: 系统优化")
    print("=" * 70)
    print()
    
    system = WeiwenLaw("系统优化")
    
    # 基线配置
    system.set_domain_constant(R=8.0, description="性能要求")
    system.set_steady_state_reserve(
        S=0,
        description="系统弹性",
        subsystems={
            '组件A': 7.0,
            '组件B': 6.0,
            '组件C': 8.5
        }
    )
    system.set_perturbation(
        D=0,
        description="环境压力",
        perturbation_sources={
            '负载峰值': 5.0,
            '网络延迟': 3.0
        }
    )
    system.set_lever(H=2.0, description="控制力度")
    
    baseline_M = system.compute_steady_state()
    print(f"基线 M: {baseline_M:.4f}")
    print()
    
    # 场景1: 加强最薄弱组件
    print("场景1: 将组件B从 6.0 提升到 8.0")
    system.set_steady_state_reserve(
        S=0,
        subsystems={
            '组件A': 7.0,
            '组件B': 8.0,  # 改进
            '组件C': 8.5
        }
    )
    new_M = system.compute_steady_state()
    print(f"新 M: {new_M:.4f} (变化: {new_M - baseline_M:+.4f})")
    print()
    
    # 场景2: 降低扰动
    print("场景2: 将负载峰值从 5.0 降低到 3.0")
    system.set_perturbation(
        D=0,
        perturbation_sources={
            '负载峰值': 3.0,  # 降低
            '网络延迟': 3.0
        }
    )
    new_M2 = system.compute_steady_state()
    print(f"新 M: {new_M2:.4f} (变化: {new_M2 - baseline_M:+.4f})")
    print()
    
    # 场景3: 增加控制力度
    print("场景3: 将控制力度从 2.0 增加到 3.0")
    system.set_lever(H=3.0, description="增加控制力度")
    new_M3 = system.compute_steady_state()
    print(f"新 M: {new_M3:.4f} (变化: {new_M3 - baseline_M:+.4f})")
    print()
    
    print("洞察:")
    print("  - 加强最薄弱组件 (S) 影响最大")
    print("  - 降低扰动 (D) 也有显著帮助")
    print("  - 增加控制力度 (H) 实际上降低了 M")
    print("    （因为H在分母——更多力度=更少稳定性）")
    print("    但这不意味着控制力度无用。")
    print("    低效冗余的制衡消耗系统资源，")
    print("    在固定条件下会压制整体稳态结果。")
    print("    H是主观制衡支点——效率比强度重要。")
    print()
    print("  这展示了公式的预测能力:")
    print("  M = (R × S) / (D × H)")
    print()


if __name__ == "__main__":
    audit_ai_claims()
    print("\n\n")
    project_system_changes()
    
    print("=" * 70)
    print("演示结束")
    print("=" * 70)
    print()
    print("关键要点:")
    print("  1. 唯稳律提供了因果分析的结构化框架")
    print("  2. 公式 M = (R × S) / (D × H) 是确定性的、可审计的")
    print("  3. 审计模式向后追溯，发现因果完整性问题")
    print("  4. 推演模式预测条件变化下的结果")
    print("  5. 框架是全域通用的，可应用于任何领域")
    print()
    print("下一步:")
    print("  - 探索 weiwen_law.py 模块了解完整API")
    print("  - 尝试将框架应用到你的领域")
    print("  - 阅读 maps/ 下的导图获取视觉参考")
