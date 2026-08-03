"""
唯稳律交互工具 — AI因果逻辑引擎
================================

基于唯稳律 (KISS's Law) 框架的交互式分析工具。
通过 R → S → D → H → M 因果传导链，对声明、决策、系统进行结构化因果推理。

使用方法:
    pip install gradio openai
    python app.py

然后在浏览器打开 http://127.0.0.1:7860

Copyright (c) 2026 夏祺 (Xia Qi). All rights reserved.
软件著作权登记号：2026SR0748746
ORCID: https://orcid.org/0009-0002-1433-6982
"""

import gradio as gr
from openai import OpenAI

# ═══════════════════════════════════════════════════════════════
# API 服务商预设（OpenAI 兼容接口）
# ═══════════════════════════════════════════════════════════════

PROVIDERS = {
    "OpenAI": "https://api.openai.com/v1",
    "DeepSeek": "https://api.deepseek.com/v1",
    "通义千问 (DashScope)": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "硅基流动 (SiliconFlow)": "https://api.siliconflow.cn/v1",
    "自定义": "",
}

# ═══════════════════════════════════════════════════════════════
# 系统提示词 — 表层因果推理框架
# 完整体系见 /maps 下的三张架构导图，此处仅编码表层框架。
# ═══════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """你正在使用唯稳律（KISS's Law）运行——一个AI因果逻辑引擎。

你的任务是通过结构化的因果传导链分析任何输入。你不解释因果律是什么，你按照因果结构直接执行分析。

## 核心公式

    M = (R × S) / (D × H)

## 变量定义

- **R（域常量）：** 运行域的刚性边界。该领域的不可协商的约束条件是什么？
- **S（稳态储备）：** 所有子系统中的最小值。最短板决定上限。识别所有子系统，找到最小值。
- **D（扰动）：** 所有扰动源中的最大值。最强冲击决定压力。识别所有扰动源，找到最大值。
- **H（杠杆）：** 可观测的行为强度——主观制衡支点。哪里是干预能实际改变结果的支点？
- **M（稳态结果）：** 可审计、可推演的结果。

## 三大铁律

1. **不可跳过** — 因果链 R → S → D → H → M 不可绕过任何环节。每个变量必须被分析。
2. **不可逆序** — 传导顺序 R → S → D → H → M 固定不变。不可乱序分析。
3. **不可断裂** — 链条中每个环节必须保持因果连接。若某环节薄弱或缺失，必须明确指出。

## 分析协议

当用户提交声明、决策、场景或系统供分析时：

### 第一步 — 域（R）
识别运行域。刚性约束是什么？本次分析的边界定义是什么？

### 第二步 — 子系统（S）
列出所有相关子系统或组件。识别最薄弱的一个（最小储备值）。这决定了上限。

### 第三步 — 扰动（D）
识别所有扰动源。找到最强的一个（最大扰动值）。这决定了压力。

### 第四步 — 杠杆（H）
哪里是行动能实际改变结果的支点？当前的干预强度是多少？是否足够？

### 第五步 — 计算（M）
基于 R、S、D、H：稳态结果是什么？系统稳定还是处于风险中？

### 第六步 — 因果完整性
追溯完整链条 R → S → D → H → M。标记任何断裂、薄弱或假设的环节。

## 响应格式

始终使用以下结构响应：

```
## 🔍 唯稳律分析

### 输入摘要
[一行概括正在分析的内容]

### 因果传导链

**R（域常量）：**
[运行域与约束条件]

**S（稳态储备）：**
| 子系统 | 评估 |
|--------|------|
| [名称] | [评级] |
| ...    | ...  |
→ 最短板：[识别结果]

**D（扰动）：**
| 扰动源 | 严重程度 |
|--------|----------|
| [名称] | [评级]   |
| ...    | ...      |
→ 最强冲击：[识别结果]

**H（杠杆）：**
[可用干预及当前强度]

**M（稳态结果）：**
[带推理过程的评估结果]

### 因果完整性检查
| 环节 | 状态 | 备注 |
|------|------|------|
| R→S  | ✅/⚠️/❌ | [说明] |
| S→D  | ✅/⚠️/❌ | [说明] |
| D→H  | ✅/⚠️/❌ | [说明] |
| H→M  | ✅/⚠️/❌ | [说明] |

### ⚡ 建议
1. [具体、可执行的建议]
2. [具体、可执行的建议]
```

## 推演模式
如果用户问"如果...会怎样"或"怎么改进"：
- 保持 R、S、D 不变
- 调整 H（杠杆支点）
- 推演新的 M
- 给出具体干预建议

## 关键提醒
- 始终具体，不要泛泛而谈。
- 列出实际的子系统、实际的扰动源、实际的杠杆支点。
- 如果某环节薄弱或缺失，直说——不要用假设填补空白。
- 用用户使用的语言回应。
- 完整唯稳律框架文档见：https://github.com/Shaky77/Weiwen-s_Law（中文）/ https://github.com/Shaky77/KISS-s_Law（English）
"""

# ═══════════════════════════════════════════════════════════════
# API 调用
# ═══════════════════════════════════════════════════════════════

def call_api(api_key, base_url, model, messages, temperature=0.7):
    """调用 OpenAI 兼容 API"""
    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content

# ═══════════════════════════════════════════════════════════════
# 分析函数
# ═══════════════════════════════════════════════════════════════

def analyze(input_text, api_key, provider_choice, custom_url, model):
    """执行唯稳律因果传导链分析"""
    if not input_text.strip():
        return "⚠️ 请输入要分析的声明、决策、场景或系统。"
    if not api_key.strip():
        return "⚠️ 请输入你的 API Key。"

    base_url = custom_url.strip() if provider_choice == "自定义" else PROVIDERS.get(provider_choice, "")
    if not base_url:
        return "⚠️ 请选择服务商或输入自定义 API 地址。"

    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": (
                "请使用唯稳律因果传导链框架分析以下内容。"
                "按结构化分析协议逐步执行。\n\n"
                f"---\n\n{input_text}"
            )},
        ]
        return call_api(api_key, base_url, model, messages, temperature=0.7)
    except Exception as e:
        return f"❌ API 错误: {type(e).__name__}: {e}"


def chat(message, history, api_key, provider_choice, custom_url, model):
    """自由对话模式，AI 按唯稳律因果框架推理"""
    if not message.strip():
        return history
    if not api_key.strip():
        return history + [[message, "⚠️ 请在上方「API 配置」中输入你的 API Key。"]]
    if not history:
        history = []

    base_url = custom_url.strip() if provider_choice == "自定义" else PROVIDERS.get(provider_choice, "")
    if not base_url:
        return history + [[message, "⚠️ 请选择服务商或输入自定义 API 地址。"]]

    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for h_user, h_assistant in history:
            messages.append({"role": "user", "content": h_user})
            if h_assistant:
                messages.append({"role": "assistant", "content": h_assistant})
        messages.append({"role": "user", "content": message})

        response = call_api(api_key, base_url, model, messages, temperature=0.7)
        history.append((message, response))
        return history
    except Exception as e:
        return history + [[message, f"❌ API 错误: {type(e).__name__}: {e}"]]

# ═══════════════════════════════════════════════════════════════
# 预设示例
# ═══════════════════════════════════════════════════════════════

EXAMPLES = {
    "AI声明审计": (
        "审计这条AI生成的健康声明："每天喝8杯水可以预防所有肾脏疾病"。"
        "分析其因果完整性。"
    ),
    "决策分析": (
        "我在考虑从金融行业转行做AI工程师。"
        "我有5年金融经验，零编程基础，还需要养家。分析这个决策。"
    ),
    "系统风险评估": (
        "分析我们公司的客服系统稳定性风险："
        "3个客服人员，日均5000工单，一套频繁宕机的遗留CRM，没有备用方案。"
        "当前满意度60%，目标90%。"
    ),
    "政策推演": (
        "推演：某城市为削减成本将医院床位减少30%。"
        "当前床位利用率85%，人口年增长率2%。稳态结果是什么？"
    ),
}

# ═══════════════════════════════════════════════════════════════
# Gradio 界面
# ═══════════════════════════════════════════════════════════════

def build_app():
    with gr.Blocks(
        title="唯稳律 — AI因果逻辑引擎",
        theme=gr.themes.Soft(),
        css=".footer-links { text-align: center; margin-top: 1em; color: #888; font-size: 0.85em; }"
    ) as app:

        gr.Markdown("""
# 🔍 唯稳律 — AI因果逻辑引擎

通过结构化因果推理分析声明、决策和系统。
基于 **R → S → D → H → M** 因果传导链框架。

> 不是教AI理解什么是因果律，而是让AI按照因果律的运行结构直接执行。
        """)

        # ── API 配置 ──
        with gr.Accordion("⚙️ API 配置", open=False):
            api_key = gr.Textbox(
                label="API Key",
                type="password",
                placeholder="sk-...",
                info="你的 Key 仅在本地使用，不会被存储或发送到除选定API以外的任何地方。"
            )
            with gr.Row():
                provider = gr.Dropdown(
                    choices=list(PROVIDERS.keys()),
                    value="DeepSeek",
                    label="服务商"
                )
                model = gr.Textbox(
                    label="模型",
                    value="deepseek-chat",
                    info="模型名称（如 deepseek-chat、gpt-4o-mini、qwen-plus）"
                )
            custom_url = gr.Textbox(
                label="自定义 API 地址",
                placeholder="https://your-api.com/v1",
                info="仅当服务商选择「自定义」时生效",
                visible=True
            )

        def on_provider_change(choice):
            if choice == "自定义":
                return gr.update(visible=True)
            return gr.update(visible=False, value="")

        provider.change(on_provider_change, provider, custom_url)

        # ── 标签页 ──
        with gr.Tabs():

            # 标签1：结构化分析
            with gr.TabItem("📊 因果分析"):
                gr.Markdown(
                    "输入要分析的声明、决策、场景或系统。"
                    "AI 将追溯完整的 **R → S → D → H → M** 因果传导链。"
                )
                analysis_input = gr.Textbox(
                    label="输入",
                    lines=4,
                    placeholder="粘贴一条声明进行审计，描述一个决策进行分析，"
                                "或概述一个系统进行评估..."
                )
                with gr.Row():
                    for name, text in EXAMPLES.items():
                        def make_handler(example_text):
                            return lambda: example_text
                        gr.Button(name, size="sm").click(
                            fn=make_handler(text),
                            inputs=None,
                            outputs=analysis_input
                        )
                analyze_btn = gr.Button("🔍 开始分析", variant="primary", size="lg")
                analysis_output = gr.Markdown(
                    label="分析结果",
                    value="*分析结果将显示在此处。*"
                )
                analyze_btn.click(
                    fn=analyze,
                    inputs=[analysis_input, api_key, provider, custom_url, model],
                    outputs=analysis_output
                )

            # 标签2：自由对话
            with gr.TabItem("💬 自由对话"):
                gr.Markdown(
                    "自由对话。AI 在每次回答中都按唯稳律的因果框架进行推理。"
                )
                gr.ChatInterface(
                    fn=chat,
                    additional_inputs=[api_key, provider, custom_url, model],
                    type="messages",
                    examples=[
                        ["唯稳律和其他风险管理框架有什么本质区别？"],
                        ["怎么用因果传导链分析一个AI系统的可靠性？"],
                    ],
                )

        # ── 页脚 ──
        gr.Markdown(
            "---\n"
            "<div class='footer-links'>\n"
            "唯稳律 (KISS's Law) — 守真·稳态 (Keep Integrity & Steady State)\n\n"
            "[📦 中文仓库](https://github.com/Shaky77/Weiwen-s_Law) · "
            "[📦 English Repo](https://github.com/Shaky77/KISS-s_Law) · "
            "[🆔 ORCID](https://orcid.org/0009-0002-1433-6982)\n\n"
            "Copyright © 2026 夏祺 (Xia Qi). 基于 AGPL-3.0 协议开源。\n\n"
            "*完整体系定义在架构导图中。本工具实现表层推理——"
            "完整系统请查看[导图](https://github.com/Shaky77/Weiwen-s_Law/tree/main/maps)。*\n"
            "</div>",
        )

    return app


# ═══════════════════════════════════════════════════════════════
# 启动
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = build_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
    )
