from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Service:
    name: str
    cost: float

@dataclass
class Milestone:
    name: str
    start_date: datetime
    end_date: datetime
    services: List[Service]

@dataclass
class Roadmap:
    milestones: List[Milestone]

def generate_roadmap(milestones: List[Milestone]) -> Roadmap:
    return Roadmap(milestones)

def render_gantt_chart(roadmap: Roadmap) -> str:
    gantt_chart = ""
    for milestone in roadmap.milestones:
        gantt_chart += f"{milestone.name}: {milestone.start_date} - {milestone.end_date}\n"
        for service in milestone.services:
            gantt_chart += f" - {service.name}: ${service.cost}\n"
    return gantt_chart

def export_to_pdf(roadmap: Roadmap) -> str:
    pdf_content = ""
    for milestone in roadmap.milestones:
        pdf_content += f"{milestone.name}\n"
        pdf_content += f"Start Date: {milestone.start_date}\n"
        pdf_content += f"End Date: {milestone.end_date}\n"
        for service in milestone.services:
            pdf_content += f" - {service.name}: ${service.cost}\n"
        pdf_content += "\n"
    return pdf_content

def export_to_csv(roadmap: Roadmap) -> str:
    csv_content = "Milestone,Start Date,End Date,Service,Cost\n"
    for milestone in roadmap.milestones:
        for service in milestone.services:
            csv_content += f"{milestone.name},{milestone.start_date},{milestone.end_date},{service.name},{service.cost}\n"
    return csv_content
