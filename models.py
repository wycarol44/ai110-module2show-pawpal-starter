class Owner:
    def __init__(self, name="Carol", pets=None, **kwargs):
        self.name = name
        self.pets = pets if pets is not None else []

    def add_pet(self, pet):
        self.pets.append(pet)


class Pet:
    def __init__(self, name="CoCo", species="cat"):
        self.name = name
        self.species = species


class Task:
    PRIORITY_RANK = {"high": 3, "medium": 2, "low": 1}

    def __init__(self, title="Morning walk", duration_minutes=20, priority="medium", pet=None):
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.pet = pet

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get("title", ""),
            duration_minutes=int(data.get("duration_minutes", 0)),
            priority=data.get("priority", "medium"),
            pet=data.get("pet"),
        )

    @property
    def priority_value(self):
        return self.PRIORITY_RANK.get(self.priority, 0)


class Scheduler:
    @staticmethod
    def format_time(total_minutes):
        hour = total_minutes // 60
        minute = total_minutes % 60
        return f"{hour:02d}:{minute:02d}"

    @classmethod
    def schedule_tasks(cls, task_dicts, pets, start_hour=8, start_minute=0):
        task_objects = [Task.from_dict(task) for task in task_dicts]
        scheduled = []
        pet_counts = {pet.name: 0 for pet in pets}
        if not task_objects:
            return []

        remaining = list(enumerate(task_objects))
        while remaining:
            max_priority = max(task.priority_value for _, task in remaining)
            candidates = [item for item in remaining if item[1].priority_value == max_priority]
            candidates.sort(key=lambda item: (pet_counts.get(item[1].pet, 0), item[0]))
            chosen_index, chosen_task = candidates[0]
            remaining = [(idx, task) for idx, task in remaining if idx != chosen_index]
            pet_counts[chosen_task.pet] = pet_counts.get(chosen_task.pet, 0) + 1
            scheduled.append(chosen_task)

        minutes = start_hour * 60 + start_minute
        timeline = []
        for task in scheduled:
            start = minutes
            end = start + task.duration_minutes
            timeline.append(
                {
                    "start": cls.format_time(start),
                    "end": cls.format_time(end),
                    "title": task.title,
                    "pet": task.pet,
                    "priority": task.priority,
                    "duration_minutes": task.duration_minutes,
                    "display": (
                        f"{cls.format_time(start)}–{cls.format_time(end)} {task.title} | "
                        f"Pet: {task.pet or 'Unassigned'} | Priority: {task.priority.capitalize()}"
                    ),
                }
            )
            minutes = end
        return timeline
