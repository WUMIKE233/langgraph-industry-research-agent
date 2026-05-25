from __future__ import annotations

import os
from pathlib import Path

from src.deep_research_agent import run_agent


QUESTION = (
    "请详述 2026 年全球半导体先进制程（如 2nm 节点）的量产进展，"
    "并对比台积电与英特尔在相关晶体管架构（GAA/RibbonFET）上的最新技术演进与交付时间表。"
)


def main() -> None:
    max_loops = int(os.getenv("MAX_LOOPS", "2"))
    final_state = run_agent(QUESTION, max_loops=max_loops)

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "experiment_output.txt"
    output_path.write_text(final_state["final_answer"], encoding="utf-8")
    print(f"\n[Observation] 最终报告已保存到：{output_path}")


if __name__ == "__main__":
    main()
