import pytest
from cloud_migrator import Task, map_tasks, render_summary_chart


def test_task_estimation_happy_path():
    raw = [
        {
            "name": "Lift‑and‑Shift",
            "base_cost": 5000,
            "base_effort": 10,
            "cost_multiplier": 1.2,
            "effort_multiplier": 1.1,
        },
        {
            "name": "Database Migration",
            "base_cost": 8000,
            "base_effort": 15,
        },
    ]
    tasks = map_tasks(raw)

    # Verify number of tasks
    assert len(tasks) == 2

    # First task calculations
    t0 = tasks[0]
    assert t0.name == "Lift‑and‑Shift"
    assert pytest.approx(t0.estimated_cost, rel=1e-6) == 5000 * 1.2
    assert pytest.approx(t0.estimated_effort, rel=1e-6) == 10 * 1.1

    # Second task uses default multipliers (1.0)
    t1 = tasks[1]
    assert t1.name == "Database Migration"
    assert t1.estimated_cost == 8000
    assert t1.estimated_effort == 15


def test_task_estimation_missing_fields():
    # Missing optional multipliers should default to 1.0
    raw = [
        {"name": "Network Setup", "base_cost": 2000, "base_effort": 5},
    ]
    tasks = map_tasks(raw)
    t = tasks[0]
    assert t.cost_multiplier == 1.0
    assert t.effort_multiplier == 1.0
    assert t.estimated_cost == 2000
    assert t.estimated_effort == 5


def test_task_estimation_negative_values():
    raw = [
        {"name": "Bad Task", "base_cost": -100, "base_effort": 5},
    ]
    with pytest.raises(ValueError):
        map_tasks(raw)


def test_render_summary_chart_happy_path():
    tasks = [
        Task(name="A", base_cost=1000, base_effort=2),
        Task(name="B", base_cost=3000, base_effort=4),
    ]
    chart = render_summary_chart(tasks)

    # Total cost = 4000, total effort = 6
    assert "Cost   :" in chart
    assert "Effort :" in chart
    # Verify that the bars have the same length because scaling is per total.
    # Since both totals are >0, each bar should be max length (40) because scaling
    # uses the total itself.
    cost_bar = chart.splitlines()[0].split('[')[1].split(']')[0]
    effort_bar = chart.splitlines()[1].split('[')[1].split(']')[0]
    assert len(cost_bar.strip()) == 40
    assert len(effort_bar.strip()) == 40
    # Verify numeric values appear correctly
    assert "$4,000.00" in chart
    assert "6.00 person‑days" in chart


def test_render_summary_chart_empty():
    chart = render_summary_chart([])
    lines = chart.splitlines()
    assert len(lines) == 2
    # Bars should be empty (only spaces)
    assert lines[0].endswith("] $0.00")
    assert lines[1].endswith("] 0.00 person‑days")
