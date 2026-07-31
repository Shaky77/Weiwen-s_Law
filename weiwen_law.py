"""
唯稳律 (KISS's Law) - 核心实现
================================

    *** 辅助参考代码 ***

完整系统规则、多场域递归和内生风控机制全部 contained in /maps 下的三张架构导图中。
本简化代码仅实现核心公式计算和基础审计/推演功能。
不涵盖导图中全部递归和多场域规则。

原生推荐用法：
    直接将导图发给你的AI。无需代码。

---

核心公式: M = (R × S) / (D × H)

其中:
- R: 域常量 (Domain Constant) — 运行域的刚性边界
- S: 稳态储备 (Steady-state Reserve) — 所有子系统中的最小值
- D: 扰动 (Perturbation) — 所有扰动源中的最大值
- H: 杠杆 (Lever) — 可观测的行为强度
- M: 稳态结果 (Steady-state Outcome) — 可审计、可推演

三大铁律:
1. 不可跳过: R→S→D→H→M 链条不可绕过
2. 不可逆序: 传导顺序固定
3. 不可断裂: 每个环节必须保持因果连接

协议: AGPL-3.0
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import json


@dataclass
class CausalNode:
    """因果链中的节点"""
    name: str
    value: float
    description: str = ""
    subsystems: Optional[List['CausalNode']] = None


class WeiwenLaw:
    """
    唯稳律框架实现。
    
    提供以下功能:
    - 计算稳态结果 (M)
    - 向后追溯因果链（审计模式）
    - 向前预测稳态走向（推演模式）
    - 验证因果链完整性
    """
    
    def __init__(self, domain_name: str = "系统"):
        self.domain_name = domain_name
        self.causal_chain = {}
        self.audit_log = []
    
    def set_domain_constant(self, R: float, description: str = "") -> None:
        """
        设置域常量 (R) — 运行域的刚性边界。
        这是定义系统的不可协商约束。
        """
        self.causal_chain['R'] = CausalNode('R', R, description)
        self._log(f"R 设定: {R} ({description})")
    
    def set_steady_state_reserve(self, S: float, description: str = "", 
                                  subsystems: Optional[Dict[str, float]] = None) -> None:
        """
        设置稳态储备 (S) — 所有子系统中的最小值。
        最薄弱的子系统决定整体稳定性上限。
        """
        subsystem_nodes = None
        if subsystems:
            subsystem_nodes = [CausalNode(name, val, f"子系统: {name}") 
                             for name, val in subsystems.items()]
            actual_S = min(subsystems.values())
            self._log(f"S 计算为子系统最小值: {actual_S}")
            self._log(f"  子系统: {subsystems}")
        else:
            actual_S = S
        
        self.causal_chain['S'] = CausalNode('S', actual_S, description, subsystem_nodes)
        self._log(f"S 设定: {actual_S} ({description})")
    
    def set_perturbation(self, D: float, description: str = "",
                        perturbation_sources: Optional[Dict[str, float]] = None) -> None:
        """
        设置扰动 (D) — 所有扰动源中的最大值。
        最强的扰动决定系统压力。
        """
        perturbation_nodes = None
        if perturbation_sources:
            perturbation_nodes = [CausalNode(name, val, f"扰动源: {name}") 
                                 for name, val in perturbation_sources.items()]
            actual_D = max(perturbation_sources.values())
            self._log(f"D 计算为扰动源最大值: {actual_D}")
            self._log(f"  扰动源: {perturbation_sources}")
        else:
            actual_D = D
        
        self.causal_chain['D'] = CausalNode('D', actual_D, description, perturbation_nodes)
        self._log(f"D 设定: {actual_D} ({description})")
    
    def set_lever(self, H: float, description: str = "") -> None:
        """
        设置杠杆 (H) — 可观测的行为强度。
        这是主观选择点，能动性在此施加力量。
        """
        self.causal_chain['H'] = CausalNode('H', H, description)
        self._log(f"H 设定: {H} ({description})")
    
    def compute_steady_state(self) -> float:
        """
        使用核心公式计算稳态结果 (M)。
        M = (R × S) / (D × H)
        """
        self._validate_chain_completeness()
        
        R = self.causal_chain['R'].value
        S = self.causal_chain['S'].value
        D = self.causal_chain['D'].value
        H = self.causal_chain['H'].value
        
        if D * H == 0:
            raise ValueError("D 和 H 不能为零（除数为零）")
        
        M = (R * S) / (D * H)
        self.causal_chain['M'] = CausalNode('M', M, "稳态结果")
        self._log(f"M 计算: ({R} × {S}) / ({D} × {H}) = {M:.4f}")
        
        return M
    
    def audit_backward(self) -> Dict[str, Any]:
        """
        审计模式: 从结果 (M) 向后追溯因果链。
        返回审计报告，显示因果连接完整性。
        """
        self._validate_chain_completeness()
        
        audit_report = {
            'mode': '审计 (向后追溯)',
            'domain': self.domain_name,
            'chain': [],
            'integrity': '通过',
            'findings': []
        }
        
        # 从 M 开始向后追溯
        M = self.causal_chain['M'].value
        H = self.causal_chain['H'].value
        D = self.causal_chain['D'].value
        S = self.causal_chain['S'].value
        R = self.causal_chain['R'].value
        
        # 验证因果连接
        expected_M = (R * S) / (D * H)
        
        audit_report['chain'] = [
            {'node': 'M', 'value': M, 'description': '稳态结果'},
            {'node': 'H', 'value': H, 'description': '杠杆 (行为强度)'},
            {'node': 'D', 'value': D, 'description': '扰动'},
            {'node': 'S', 'value': S, 'description': '稳态储备'},
            {'node': 'R', 'value': R, 'description': '域常量'},
        ]
        
        if abs(M - expected_M) > 1e-6:
            audit_report['integrity'] = '失败'
            audit_report['findings'].append(
                f"因果断裂: M={M:.4f} ≠ 预期={expected_M:.4f}"
            )
        
        # 检查违规
        if self.causal_chain['S'].subsystems:
            min_S = min(n.value for n in self.causal_chain['S'].subsystems)
            if S != min_S:
                audit_report['findings'].append(
                    f"S 应为子系统最小值: {S} ≠ {min_S}"
                )
        
        if self.causal_chain['D'].subsystems:
            max_D = max(n.value for n in self.causal_chain['D'].subsystems)
            if D != max_D:
                audit_report['findings'].append(
                    f"D 应为扰动源最大值: {D} ≠ {max_D}"
                )
        
        self._log(f"审计完成: {audit_report['integrity']}")
        return audit_report
    
    def project_forward(self, new_H: float, new_D: Optional[float] = None) -> Dict[str, Any]:
        """
        推演模式: 预测条件变化下的未来稳态。
        返回推演报告。
        """
        if 'R' not in self.causal_chain or 'S' not in self.causal_chain:
            raise ValueError("推演前必须先设定 R 和 S")
        
        R = self.causal_chain['R'].value
        S = self.causal_chain['S'].value
        old_H = self.causal_chain['H'].value if 'H' in self.causal_chain else 1.0
        old_D = self.causal_chain['D'].value if 'D' in self.causal_chain else 1.0
        
        proj_H = new_H
        proj_D = new_D if new_D is not None else old_D
        
        old_M = (R * S) / (old_D * old_H)
        new_M = (R * S) / (proj_D * proj_H)
        
        projection_report = {
            'mode': '推演 (向前预测)',
            'domain': self.domain_name,
            'current_state': {
                'M': old_M,
                'H': old_H,
                'D': old_D
            },
            'projected_state': {
                'M': new_M,
                'H': proj_H,
                'D': proj_D
            },
            'delta_M': new_M - old_M,
            'stability_change': '改善' if new_M > old_M else '恶化',
            'recommendation': self._generate_recommendation(old_M, new_M)
        }
        
        self._log(f"推演: M 从 {old_M:.4f} 变化到 {new_M:.4f}")
        return projection_report
    
    def _validate_chain_completeness(self) -> None:
        """验证所有节点 R, S, D, H 是否存在"""
        required = ['R', 'S', 'D', 'H']
        missing = [n for n in required if n not in self.causal_chain]
        
        if missing:
            raise ValueError(f"因果链缺少节点: {missing}")
    
    def _generate_recommendation(self, old_M: float, new_M: float) -> str:
        """根据推演结果生成建议"""
        if new_M > old_M * 1.2:
            return "显著改善 — 可信心推进"
        elif new_M > old_M:
            return "适度改善 — 密切监控"
        elif new_M > old_M * 0.8:
            return "轻微恶化 — 考虑调整"
        else:
            return "严重恶化 — 停止并重新评估"
    
    def _log(self, message: str) -> None:
        """记录审计日志"""
        self.audit_log.append(message)
    
    def get_summary(self) -> str:
        """获取当前状态的人类可读摘要"""
        if not self.causal_chain:
            return "未配置因果链"
        
        lines = [f"=== 唯稳律: {self.domain_name} ==="]
        
        for key in ['R', 'S', 'D', 'H', 'M']:
            if key in self.causal_chain:
                node = self.causal_chain[key]
                lines.append(f"{key}: {node.value:.4f} - {node.description}")
        
        if 'M' in self.causal_chain:
            M = self.causal_chain['M'].value
            if M > 1.0:
                status = "稳定"
            elif M > 0.5:
                status = "谨慎"
            else:
                status = "危急"
            lines.append(f"\n稳态: {status} (M={M:.4f})")
        
        return "\n".join(lines)
    
    def export_audit_log(self) -> str:
        """导出审计日志"""
        return "\n".join(self.audit_log)


def demo_ai_audit():
    """
    演示: 使用唯稳律审计AI输出质量。
    
    场景: AI系统正在生成内容。我们想审计输出是否保持因果完整性。
    """
    print("=" * 60)
    print("演示: 使用唯稳律审计AI输出")
    print("=" * 60)
    print()
    
    # 初始化框架
    system = WeiwenLaw("AI内容生成器")
    
    # 设置域常量 - 什么是不可协商的约束？
    # 在这个案例中: 内容必须事实准确
    system.set_domain_constant(
        R=10.0,
        description="事实准确性要求 (1-10分)"
    )
    
    # 设置稳态储备 - 有哪些子系统？
    # 分解为: 研究深度、来源质量、引用准确性
    subsystems = {
        '研究深度': 7.5,
        '来源质量': 8.0,
        '引用准确性': 6.5  # 最薄弱环节
    }
    system.set_steady_state_reserve(
        S=0,  # 会自动计算为最小值
        description="综合质量储备",
        subsystems=subsystems
    )
    
    # 设置扰动 - 存在哪些干扰？
    # 分解为: 时间压力、来源冲突、查询模糊
    perturbation_sources = {
        '时间压力': 3.0,
        '来源冲突': 4.5,  # 最强扰动
        '查询模糊': 2.0
    }
    system.set_perturbation(
        D=0,  # 会自动计算为最大值
        description="运行扰动",
        perturbation_sources=perturbation_sources
    )
    
    # 设置杠杆 - 我们施加多少行为强度？
    # 在这个案例中: 验证力度
    system.set_lever(
        H=2.0,
        description="验证力度倍数"
    )
    
    # 计算稳态结果
    M = system.compute_steady_state()
    
    print(system.get_summary())
    print()
    
    # 审计结果
    print("--- 审计报告 ---")
    audit = system.audit_backward()
    print(json.dumps(audit, indent=2, ensure_ascii=False))
    print()
    
    # 推演: 如果增加验证力度会怎样？
    print("--- 推演: 将验证力度增加到 H=3.0 ---")
    projection = system.project_forward(new_H=3.0)
    print(f"当前 M: {projection['current_state']['M']:.4f}")
    print(f"推演 M: {projection['projected_state']['M']:.4f}")
    print(f"变化: {projection['delta_M']:+.4f}")
    print(f"稳定性: {projection['stability_change']}")
    print(f"建议: {projection['recommendation']}")
    print()
    
    # 推演: 如果扰动增加会怎样？
    print("--- 推演: 扰动增加到 D=6.0 ---")
    projection2 = system.project_forward(new_H=3.0, new_D=6.0)
    print(f"推演 M: {projection2['projected_state']['M']:.4f}")
    print(f"稳定性: {projection2['stability_change']}")
    print(f"建议: {projection2['recommendation']}")
    print()
    
    print("--- 完整审计日志 ---")
    print(system.export_audit_log())


if __name__ == "__main__":
    demo_ai_audit()
