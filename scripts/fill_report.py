from __future__ import annotations

import shutil
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt


ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = Path.home() / "Downloads"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DOCX = OUTPUT_DIR / "实验4_基于LangGraph的行业研报智能体_实验报告.docx"


def find_template() -> Path:
    candidates = [
        p
        for p in DOWNLOADS.glob("* (5).docx")
        if "_" not in p.name and p.name.endswith("(5).docx")
    ]
    if not candidates:
        raise FileNotFoundError("未找到学生实验报告模板 (5).docx")
    return max(candidates, key=lambda p: p.stat().st_mtime)


def set_cell_shading(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_run_font(run, bold: bool = False, size: int = 10) -> None:
    run.bold = bold
    run.font.size = Pt(size)
    run.font.name = "宋体"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")


def add_para(cell, text: str = "", bold: bool = False, size: int = 10, align=None):
    paragraph = cell.add_paragraph()
    if align is not None:
        paragraph.alignment = align
    paragraph.paragraph_format.space_after = Pt(3)
    paragraph.paragraph_format.line_spacing = 1.15
    run = paragraph.add_run(text)
    set_run_font(run, bold=bold, size=size)
    return paragraph


def clear_cell(cell) -> None:
    cell.text = ""
    for paragraph in cell.paragraphs:
        paragraph.text = ""


def fill_section(cell, title: str, paragraphs: list[str]) -> None:
    clear_cell(cell)
    set_cell_shading(cell, "F7FBFF")
    add_para(cell, title, bold=True, size=12)
    for text in paragraphs:
        add_para(cell, text, size=10)


def replace_paragraph(paragraph, text: str, size: int = 12, bold: bool = False) -> None:
    paragraph.text = ""
    run = paragraph.add_run(text)
    set_run_font(run, bold=bold, size=size)


def fill_basic_table(doc: Document) -> None:
    table = doc.tables[0]
    values = {
        (0, 1): "待填写",
        (0, 3): "待填写",
        (1, 1): "待填写",
        (1, 3): "待填写",
        (2, 1): "独立完成",
        (2, 2): "",
        (2, 3): "",
        (3, 1): "机房/自习环境",
        (3, 2): "",
        (3, 3): "",
    }
    for (row, col), value in values.items():
        table.cell(row, col).text = value
        for paragraph in table.cell(row, col).paragraphs:
            for run in paragraph.runs:
                set_run_font(run, size=10)


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    template = find_template()
    shutil.copyfile(template, OUTPUT_DOCX)
    doc = Document(str(OUTPUT_DOCX))

    replace_paragraph(doc.paragraphs[4], "实验课程名称：大模型与智能体应用开发", size=12)
    replace_paragraph(doc.paragraphs[5], "实验项目名称：实验4 基于LangGraph的行业研报智能体", size=12)
    replace_paragraph(doc.paragraphs[6], "实验类型：设计性实验", size=12)
    replace_paragraph(doc.paragraphs[9], "实验日期：2026 年 5 月 25 日", size=12)

    fill_basic_table(doc)

    sections = doc.tables[1].rows
    fill_section(
        sections[0].cells[0],
        "实验目的",
        [
            "1. 掌握智能体认知架构从单次 Prompt 调用向多步迭代、反思和状态流转演进的基本思想。",
            "2. 掌握 LangGraph StateGraph 的节点、边、条件边与状态规约器机制，理解 Fan-out/Fan-in 场景下的状态追加更新。",
            "3. 实现 Deep Search 闭环控制逻辑，使智能体具备查询生成、检索读取、动态反思、循环决策与最终总结能力。",
        ],
    )
    fill_section(
        sections[1].cells[0],
        "实验内容",
        [
            "1. 设计行业研报智能体的图架构：START -> generate_queries -> execute_search -> reflect_judge -> finalize_answer -> END。",
            "2. 使用 TypedDict 定义 OverallState，并对 search_queries、raw_results、reflections 使用 Annotated[list, operator.add] 规约器，避免多轮检索覆盖历史状态。",
            "3. 编写 generate_queries、execute_search、reflect_judge、finalize_answer 四个节点函数；反思节点输出 is_sufficient 与 next_queries，用于条件边路由。",
            "4. 设置 current_loops/max_loops 终止屏障，防止模型在信息不足时陷入幻觉式死循环。",
            "5. 运行复杂测试任务：分析 2026 年全球半导体 2nm/18A 先进制程量产进展，并对比台积电 GAA 与英特尔 RibbonFET 技术路线。",
        ],
    )
    fill_section(
        sections[2].cells[0],
        "实验环境",
        [
            "操作系统：Windows，本地工作目录 W:\\基于LangGraph的⾏业研报智能体。",
            "开发语言：Python 3.12；依赖包：langgraph 1.2.1、tavily-python 0.7.24、typing-extensions。",
            "大模型与检索后端：Gemini Flash Latest 用于查询生成、结构化反思与最终报告生成；Tavily API 用于联网检索网页材料。",
            "密钥使用方式：API Key 仅通过当前终端环境变量注入，未写入代码仓库或报告正文；未配置密钥时系统可回退到 demo 检索与本地规则。",
            "运行命令：python run_experiment.py；输出文件：outputs/experiment_trace.txt 与 outputs/experiment_output.txt。",
        ],
    )
    fill_section(
        sections[3].cells[0],
        "实验过程与结果",
        [
            "1. 全局状态设计：OverallState 保存 question、current_loops、max_loops、pending_queries、next_queries、is_sufficient、final_answer，并将 search_queries/raw_results/reflections 定义为追加规约列表。",
            "2. 图节点实现：generate_queries 优先调用 Gemini 生成 2-3 个检索词；execute_search 调用 Tavily 检索网页材料；reflect_judge 调用 Gemini 输出结构化 JSON 反思；finalize_answer 调用 Gemini 生成最终研报。",
            "3. 条件路由：reflect_judge 后调用 route_after_reflection。若 is_sufficient=true，则进入 finalize_answer；若 current_loops >= max_loops，则触发安全熔断；否则返回 generate_queries 补充检索。",
            "4. 运行结果：第一轮由 Gemini 派生“台积电 2nm N2 GAA 纳米片量产时间表”“英特尔 18A RibbonFET PowerVia 量产交付时间表”“台积电与英特尔 2nm 架构对比”等查询，Tavily 返回台积电 N2 量产、Intel 18A 良率爬坡、GAA/RibbonFET 对比等材料。",
            "5. 反思节点判断第一轮虽已出现 Intel 18A 线索，但仍需要针对架构细节与交付时间表做二次交叉验证，因此自动生成 TSMC GAA Nanosheet vs Intel RibbonFET、Intel 18A TSMC N2 A16 delivery schedule 2026、Samsung 2nm GAA mass production progress 2026 等补充查询。",
            "6. 第二轮检索补齐 TSMC N2/GAA nanosheet、Intel 18A/RibbonFET/PowerVia 与 2025-2026 量产节奏证据后，反思节点输出 is_sufficient=true，系统进入最终总结节点。",
            "7. 终端可观测日志包含 [Thought]、[Action]、[Observation] 三类记录，完整呈现“发现知识缺口 -> 派生子查询 -> 检索观察 -> 反思判断 -> 最终报告”的闭环。",
            "8. 最终结论：2026 年先进制程竞争围绕台积电 N2/2nm 与英特尔 18A 展开。台积电 N2 首次引入 GAA nanosheet，并在 2026 年进入多厂扩产；英特尔 18A 采用 RibbonFET 与 PowerVia 组合，进入量产和良率爬坡阶段。",
        ],
    )
    fill_section(
        sections[4].cells[0],
        "操作异常问题与解决方案",
        [
            "1. 问题：真实 API Key 不应硬编码到项目中。解决：Tavily 与 Gemini Key 均通过终端环境变量临时注入，代码中只保留空占位说明。",
            "2. 问题：智能体可能因信息不足反复返回 loop 分支。解决：在 OverallState 中加入 current_loops/max_loops，并在 route_after_reflection 中硬编码最大轮次熔断条件。",
            "3. 问题：多轮检索容易覆盖历史结果。解决：使用 Annotated[list, operator.add] 作为 search_queries、raw_results、reflections 的规约器，使每轮增量追加到状态中。",
            "4. 问题：Gemini 的反思可能过于保守或输出格式不稳定。解决：提示词要求固定 JSON 字段，同时在代码中保留规则校验与回退逻辑，确保条件边可稳定路由。",
            "5. 问题：中文路径与控制台编码可能影响脚本输出。解决：运行时设置 PYTHONIOENCODING=utf-8，并在报告生成脚本中使用 pathlib 自动定位模板文件。",
        ],
    )
    fill_section(
        sections[5].cells[0],
        "实验总结",
        [
            "本次实验完成了一个具备多轮检索、反思判断和终止屏障的 LangGraph 行业研报智能体。通过 StateGraph 将复杂任务拆解为明确节点，并利用条件边完成动态路由，系统能够在第一轮信息不足时主动识别缺口并补充检索。",
            "从工程实现看，状态规约器是本实验的关键：列表型数据必须通过 reducer 追加，否则多轮或并发更新会产生覆盖风险。current_loops/max_loops 则保证系统在无法继续获得有效信息时仍能安全收束。",
            "后续可优化方向包括：接入真实 Tavily 与大模型结构化输出、增加网页正文清洗与来源去重、为研报增加引用编号和可信度评分，并使用异步节点提升多查询并发检索效率。",
        ],
    )

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            if run.text:
                set_run_font(run, size=run.font.size.pt if run.font.size else 12)
    doc.save(str(OUTPUT_DOCX))
    print(OUTPUT_DOCX)


if __name__ == "__main__":
    main()
