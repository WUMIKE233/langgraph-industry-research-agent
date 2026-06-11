from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from src.deep_research_agent import export_research_trace, run_agent


QUESTION = (
    "请详述 2026 年全球半导体先进制程（如 2nm 节点）的量产进展，"
    "并对比台积电与英特尔在相关晶体管架构（GAA/RibbonFET）上的最新技术演进与交付时间表。"
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the LangGraph industry research demo.")
    parser.add_argument("--question", default=os.getenv("RESEARCH_QUESTION", QUESTION), help="Research question to analyze.")
    parser.add_argument("--max-loops", type=int, default=int(os.getenv("MAX_LOOPS", "2")), help="Maximum search/reflection loops.")
    parser.add_argument("--output-dir", default=os.getenv("OUTPUT_DIR", "outputs"), help="Directory for report and trace files.")
    args = parser.parse_args()

    final_state = run_agent(args.question, max_loops=args.max_loops)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "experiment_output.txt"
    output_path.write_text(final_state["final_answer"], encoding="utf-8")
    trace_path = output_dir / "experiment_trace.json"
    trace_path.write_text(
        json.dumps(export_research_trace(final_state), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n[Observation] 最终报告已保存到：{output_path}")
    print(f"[Observation] 运行轨迹已保存到：{trace_path}")


if __name__ == "__main__":
    main()
