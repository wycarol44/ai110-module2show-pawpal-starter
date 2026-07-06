# PawPal+ — Pet Care Scheduling Assistant

PawPal+ is a Python-based pet care planning assistant that helps owners organize daily routines for their pets. The project combines a lightweight object model for owners, pets, and tasks with a scheduler that orders activities by priority, time, and pet-specific considerations.

## Overview

A busy pet owner often needs help staying consistent with daily care tasks such as walks, feeding, playtime, and grooming. PawPal+ provides a simple way to:

- store owner and pet information
- create and manage pet care tasks
- sort tasks by time
- filter tasks by completion status or pet name
- generate a sample daily schedule from the available tasks
- support recurring daily and weekly tasks

## Project Structure

- pawpal_system.py: core classes for Owner, Pet, Task, and Scheduler
- app.py: Streamlit-based user interface for interacting with the system
- main.py: command-line demonstration that prints a sample schedule
- tests/: regression tests for core scheduling behavior

## Getting Started

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the app

```bash
python -m streamlit run app.py
```

### Run the sample scheduler

```bash
python main.py
```

## 🖥️ Sample Output

Verified terminal output from running the sample scheduler script:

```text
Today's Schedule
====================
Sorted by time:
- 08:00 Morning walk (Max)
- 08:30 Feed breakfast (CoCo)
- 16:00 Playtime (Max)

Incomplete tasks for CoCo:
- 08:30 Feed breakfast

Scheduled plan:
08:00–08:20 Morning walk | Pet: Max | Priority: High
  Reason: priority high; pet fairness count 1
08:20–08:30 Feed breakfast | Pet: CoCo | Priority: Medium
  Reason: priority medium; pet fairness count 1
08:30–08:45 Playtime | Pet: Max | Priority: Low
  Reason: priority low; pet fairness count 2
```

## 🧪 Testing

Run the test suite with:

```bash
pytest -q tests/test_pawpal.py
```

## Features Implemented

- task creation with description, time, frequency, and completion state
- owner-to-pet relationships
- task sorting by time
- filtering by completion status and pet name
- recurring daily and weekly task handling
- explainable scheduling output for each planned task
