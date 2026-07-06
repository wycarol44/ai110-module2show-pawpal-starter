from pawpal_system import Owner, Pet, Scheduler


def build_sample_schedule():
    owner = Owner(name="Carol")
    coco = Pet(name="CoCo", species="cat", owner=owner)
    max = Pet(name="Max", species="dog", owner=owner)

    tasks = [
        {
            "title": "Morning walk",
            "description": "Take Max for a walk",
            "time": "08:00",
            "frequency": "daily",
            "completed": False,
            "duration_minutes": 20,
            "priority": "high",
            "pet": max,
        },
        {
            "title": "Feed breakfast",
            "description": "Feed CoCo breakfast",
            "time": "08:30",
            "frequency": "daily",
            "completed": False,
            "duration_minutes": 10,
            "priority": "medium",
            "pet": coco,
        },
        {
            "title": "Playtime",
            "description": "Play with Max in the afternoon",
            "time": "16:00",
            "frequency": "daily",
            "completed": False,
            "duration_minutes": 15,
            "priority": "low",
            "pet": max,
        },
    ]

    return owner, tasks


def main():
    owner, tasks = build_sample_schedule()
    print("Today's Schedule")
    print("=" * 20)
    schedule = Scheduler.schedule_tasks(tasks, owner.pets, start_hour=8, start_minute=0)
    for entry in schedule:
        print(entry["display"])
        if entry.get("explanation"):
            print(f"  Reason: {entry['explanation']}")


if __name__ == "__main__":
    main()
