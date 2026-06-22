import pytest
from cloud_migrator import BusinessGoal, generate_technical_roadmap, prioritize_technical_roadmap, align_with_cloud_migration_strategy

def test_generate_technical_roadmap():
    goals = [
        BusinessGoal("Goal 1", 3),
        BusinessGoal("Goal 2", 1),
        BusinessGoal("Goal 3", 2)
    ]
    roadmap = generate_technical_roadmap(goals)
    assert len(roadmap.goals) == 3

def test_prioritize_technical_roadmap():
    goals = [
        BusinessGoal("Goal 1", 3),
        BusinessGoal("Goal 2", 1),
        BusinessGoal("Goal 3", 2)
    ]
    roadmap = generate_technical_roadmap(goals)
    prioritized_roadmap = prioritize_technical_roadmap(roadmap)
    assert prioritized_roadmap.goals[0].name == "Goal 2"
    assert prioritized_roadmap.goals[1].name == "Goal 3"
    assert prioritized_roadmap.goals[2].name == "Goal 1"

def test_align_with_cloud_migration_strategy():
    goals = [
        BusinessGoal("Goal 1", 3),
        BusinessGoal("Goal 2", 1),
        BusinessGoal("Goal 3", 2)
    ]
    roadmap = generate_technical_roadmap(goals)
    aligned_roadmap = align_with_cloud_migration_strategy(roadmap)
    assert len(aligned_roadmap.goals) == 3

def test_edge_case_empty_goals():
    goals = []
    roadmap = generate_technical_roadmap(goals)
    assert len(roadmap.goals) == 0

def test_edge_case_single_goal():
    goals = [BusinessGoal("Goal 1", 3)]
    roadmap = generate_technical_roadmap(goals)
    assert len(roadmap.goals) == 1
