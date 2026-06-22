"""cloud_migrator module.

Provides simple task estimation and a textual summary chart for migration
planning. No external dependencies are required.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Task:
    """A migration task with cost and effort estimations."""

    name: str
    base_cost: float
    base_effort: float
    cost_multiplier: float = 1.0
    effort_multiplier: float = 1.0
    estimated_cost: float = field(init=False)
    estimated_effort: float = field(init=False)

    def __post_init__(self) -> None:
        if self.base_cost < 0 or self.base_effort < 0:
            raise ValueError("base_cost and base_effort must be non‑negative")
        if self.cost_multiplier < 0 or self.effort_multiplier < 0:
            raise ValueError("multipliers must be non‑negative")
        self.estimated_cost = self.base_cost * self.cost_multiplier
        self.estimated_effort = self.base_effort * self.effort_multiplier


def map_tasks(raw_tasks: List[Dict]) -> List[Task]:
    """Convert raw task dictionaries into fully‑estimated :class:`Task` objects.

    Each raw dict may contain:
        - ``name`` (str) – required
        - ``base_cost`` (float) – required
        - ``base_effort`` (float) – required
        - ``cost_multiplier`` (float) – optional, defaults to 1.0
        - ``effort_multiplier`` (float) – optional, defaults to 1.0

    Args:
        raw_tasks: List of dictionaries describing tasks.

    Returns:
        List of :class:`Task` objects with ``estimated_cost`` and
        ``estimated_effort`` populated.

    Raises:
        KeyError: If a required key is missing.
        ValueError: If numeric values are negative.
    """
    tasks: List[Task] = []
    for raw in raw_tasks:
        task = Task(
            name=raw["name"],
            base_cost=float(raw["base_cost"]),
            base_effort=float(raw["base_effort"]),
            cost_multiplier=float(raw.get("cost_multiplier", 1.0)),
            effort_multiplier=float(raw.get("effort_multiplier", 1.0)),
        )
        tasks.append(task)
    return tasks


def render_summary_chart(tasks: List[Task]) -> str:
    """Render a simple ASCII bar chart summarising total cost and effort.

    The chart contains two rows:
        - Cost bar (character ``#``) proportional to total cost.
        - Effort bar (character ``*``) proportional to total effort.

    The maximum bar length is 40 characters. If the total is zero, the bar
    is empty.

    Args:
        tasks: List of estimated :class:`Task` objects.

    Returns:
        A multi‑line string containing the chart.
    """
    max_bar_len = 40
    total_cost = sum(t.estimated_cost for t in tasks)
    total_effort = sum(t.estimated_effort for t in tasks)

    # Determine scaling factors; avoid division by zero.
    cost_scale = max_bar_len / total_cost if total_cost > 0 else 0
    effort_scale = max_bar_len / total_effort if total_effort > 0 else 0

    cost_bar_len = int(total_cost * cost_scale) if total_cost > 0 else 0
    effort_bar_len = int(total_effort * effort_scale) if total_effort > 0 else 0

    cost_bar = "#" * cost_bar_len
    effort_bar = "*" * effort_bar_len

    lines = [
        f"Cost   : [{cost_bar:<{max_bar_len}}] ${total_cost:,.2f}",
        f"Effort : [{effort_bar:<{max_bar_len}}] {total_effort:,.2f} person‑days",
    ]
    return "\n".join(lines)
