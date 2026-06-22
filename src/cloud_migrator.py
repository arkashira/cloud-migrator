import json
from dataclasses import dataclass
from typing import List

@dataclass
class BusinessGoal:
    name: str
    priority: int

@dataclass
class TechnicalRoadmap:
    goals: List[BusinessGoal]

def generate_technical_roadmap(goals: List[BusinessGoal]) -> TechnicalRoadmap:
    """Generate a technical roadmap based on the input business goals"""
    return TechnicalRoadmap(goals)

def prioritize_technical_roadmap(roadmap: TechnicalRoadmap) -> TechnicalRoadmap:
    """Prioritize the technical roadmap based on business objectives"""
    roadmap.goals.sort(key=lambda x: x.priority)
    return roadmap

def align_with_cloud_migration_strategy(roadmap: TechnicalRoadmap) -> TechnicalRoadmap:
    """Align the technical roadmap with the company's cloud migration strategy"""
    # For simplicity, assume the cloud migration strategy is to prioritize goals with higher priority
    return roadmap

def main():
    goals = [
        BusinessGoal("Goal 1", 3),
        BusinessGoal("Goal 2", 1),
        BusinessGoal("Goal 3", 2)
    ]
    roadmap = generate_technical_roadmap(goals)
    roadmap = prioritize_technical_roadmap(roadmap)
    roadmap = align_with_cloud_migration_strategy(roadmap)
    print(json.dumps([goal.__dict__ for goal in roadmap.goals], indent=4))

if __name__ == "__main__":
    main()
