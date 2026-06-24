from cloud_migrator import generate_roadmap, render_gantt_chart, export_to_pdf, export_to_csv, Milestone, Service
from datetime import datetime
import pytest

def test_generate_roadmap():
    milestones = [
        Milestone("Milestone 1", datetime(2024, 1, 1), datetime(2024, 1, 31), [Service("Service 1", 1000.0)]),
        Milestone("Milestone 2", datetime(2024, 2, 1), datetime(2024, 2, 28), [Service("Service 2", 2000.0)])
    ]
    roadmap = generate_roadmap(milestones)
    assert len(roadmap.milestones) == 2

def test_render_gantt_chart():
    milestones = [
        Milestone("Milestone 1", datetime(2024, 1, 1), datetime(2024, 1, 31), [Service("Service 1", 1000.0)]),
        Milestone("Milestone 2", datetime(2024, 2, 1), datetime(2024, 2, 28), [Service("Service 2", 2000.0)])
    ]
    roadmap = generate_roadmap(milestones)
    gantt_chart = render_gantt_chart(roadmap)
    assert "Milestone 1" in gantt_chart
    assert "Milestone 2" in gantt_chart

def test_export_to_pdf():
    milestones = [
        Milestone("Milestone 1", datetime(2024, 1, 1), datetime(2024, 1, 31), [Service("Service 1", 1000.0)]),
        Milestone("Milestone 2", datetime(2024, 2, 1), datetime(2024, 2, 28), [Service("Service 2", 2000.0)])
    ]
    roadmap = generate_roadmap(milestones)
    pdf_content = export_to_pdf(roadmap)
    assert "Milestone 1" in pdf_content
    assert "Milestone 2" in pdf_content

def test_export_to_csv():
    milestones = [
        Milestone("Milestone 1", datetime(2024, 1, 1), datetime(2024, 1, 31), [Service("Service 1", 1000.0)]),
        Milestone("Milestone 2", datetime(2024, 2, 1), datetime(2024, 2, 28), [Service("Service 2", 2000.0)])
    ]
    roadmap = generate_roadmap(milestones)
    csv_content = export_to_csv(roadmap)
    assert "Milestone 1" in csv_content
    assert "Milestone 2" in csv_content

def test_empty_roadmap():
    roadmap = generate_roadmap([])
    assert len(roadmap.milestones) == 0
    gantt_chart = render_gantt_chart(roadmap)
    assert gantt_chart == ""
    pdf_content = export_to_pdf(roadmap)
    assert pdf_content == ""
    csv_content = export_to_csv(roadmap)
    assert csv_content == "Milestone,Start Date,End Date,Service,Cost\n"
