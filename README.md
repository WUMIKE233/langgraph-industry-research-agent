# 基于 LangGraph 的行业研报智能体

## 中文说明

本项目实现了实验 4 要求的 Deep Search 行业研报智能体。智能体使用 LangGraph 的 `StateGraph` 组织为有向状态机，包含查询生成、检索读取、反思判断、最终总结四类节点，并通过条件边实现“继续检索 / 生成报告”的动态路由。

项目重点实现：

- 使用 `TypedDict` 定义全局状态 `OverallState`。
- 对 `search_queries`、`raw_results`、`reflections` 使用 `Annotated[list, operator.add]` 规约器，避免并发或多轮更新时覆盖历史数据。
- 设置 `current_loops` 与 `max_loops`，当反思仍不充分但达到最大轮次时强制进入总结节点。
- 在终端输出 `[Thought] -> [Action] -> [Observation]` 格式的可观测运行链路。
- 支持 Gemini 生成查询、结构化反思和研报总结；未配置 Gemini Key 时自动回退到本地规则。
- 支持 Tavily API 检索；未配置 `TAVILY_API_KEY` 时自动使用内置演示数据，便于课堂验收和离线复现。

### 安装与运行

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python run_experiment.py
```

如需使用真实 Gemini 与 Tavily，请先配置环境变量：

```powershell
$env:GEMINI_API_KEY="your_gemini_api_key"
$env:TAVILY_API_KEY="your_api_key"
$env:SEARCH_BACKEND="tavily"
```

## English

This project implements the Deep Search industry research agent required by Experiment 4. It uses LangGraph `StateGraph` as a directed state machine with four major nodes: query generation, search and reading, reflection and judgement, and final report generation. Conditional edges decide whether the agent should keep searching or finalize the answer.

Key features:

- Defines the global `OverallState` with `TypedDict`.
- Uses `Annotated[list, operator.add]` reducers for `search_queries`, `raw_results`, and `reflections` to prevent state overwrites across branches or iterations.
- Applies `current_loops` and `max_loops` as a safety barrier to avoid hallucination-driven infinite search loops.
- Prints an observable `[Thought] -> [Action] -> [Observation]` execution trace in the terminal.
- Supports Gemini for query generation, structured reflection, and final report writing; when no Gemini key is configured, it falls back to local deterministic rules.
- Supports Tavily search; when `TAVILY_API_KEY` is not configured, it falls back to built-in demo data for classroom verification and offline reproduction.

### Setup and Run

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python run_experiment.py
```

To use live Gemini and Tavily, configure the environment variables first:

```powershell
$env:GEMINI_API_KEY="your_gemini_api_key"
$env:TAVILY_API_KEY="your_api_key"
$env:SEARCH_BACKEND="tavily"
```
