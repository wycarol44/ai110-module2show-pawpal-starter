import uuid


class Owner:
    def __init__(self, name="Carol", pets=None, **kwargs):
        self.name = name
        self.pets = list(pets) if pets is not None else []
        for pet in self.pets:
            if pet.owner is not None and pet.owner is not self:
                pet.owner.remove_pet(pet)
            pet.owner = self

    def add_pet(self, pet):
        if pet is None:
            raise ValueError("A pet is required.")
        if not isinstance(pet, Pet):
            raise TypeError("Only Pet objects can be added to an owner.")
        if pet.owner is not None and pet.owner is not self:
            pet.owner.remove_pet(pet)
        if pet not in self.pets:
            self.pets.append(pet)
        pet.owner = self
        return pet

    def remove_pet(self, pet):
        if pet in self.pets:
            self.pets.remove(pet)
        if pet.owner is self:
            pet.owner = None

    def get_pet(self, pet_ref):
        if pet_ref is None:
            return None
        if isinstance(pet_ref, Pet):
            return pet_ref if pet_ref in self.pets else None
        for pet in self.pets:
            if pet.pet_id == pet_ref or pet.name == pet_ref:
                return pet
        return None


class Pet:
    def __init__(self, name="CoCo", species="cat", owner=None, preferences=None, constraints=None, pet_id=None):
        self.name = name.strip() or "CoCo"
        self.species = species.strip() or "cat"
        self.pet_id = pet_id or str(uuid.uuid4())[:8]
        self.owner = None
        self.preferences = preferences or {}
        self.constraints = constraints or {}
        if owner is not None:
            owner.add_pet(self)

    def set_owner(self, owner):
        if owner is None:
            self.owner = None
            return
        owner.add_pet(self)

    def preferred_start_minutes(self):
        hour = int(self.preferences.get("preferred_start_hour", 8))
        minute = int(self.preferences.get("preferred_start_minute", 0))
        return hour * 60 + minute


class Task:
    PRIORITY_RANK = {"high": 3, "medium": 2, "low": 1}
    VALID_PRIORITIES = set(PRIORITY_RANK)

    def __init__(
        self,
        title=None,
        description=None,
        time=None,
        frequency="once",
        completed=False,
        duration_minutes=20,
        priority="medium",
        pet=None,
        pet_id=None,
        preferred_start_minutes=None,
        latest_end_minutes=None,
        constraints=None,
    ):
        self.title = title.strip() if isinstance(title, str) and title.strip() else (description or "").strip() or ""
        self.description = description.strip() if isinstance(description, str) and description.strip() else self.title
        self.time = time
        self.frequency = frequency or "once"
        self.completed = bool(completed)
        self.duration_minutes = int(duration_minutes)
        self.priority = str(priority).lower()
        self.pet = None
        self.pet_id = None
        self.preferred_start_minutes = preferred_start_minutes
        self.latest_end_minutes = latest_end_minutes
        self.constraints = constraints or {}
        self._set_pet(pet, pet_id)
        self.validate()

    def _set_pet(self, pet, pet_id):
        if pet is None and pet_id is None:
            return
        if isinstance(pet, Pet):
            self.pet = pet
            self.pet_id = pet.pet_id
            return
        if isinstance(pet, str):
            self.pet_id = pet
            return
        if isinstance(pet_id, str):
            self.pet_id = pet_id
            return
        raise TypeError("Task pet must be a Pet object or a pet id string.")

    def validate(self, owner=None):
        if not self.title:
            raise ValueError("Task title is required.")
        if self.duration_minutes <= 0:
            raise ValueError("Duration must be greater than zero.")
        if self.priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Invalid priority: {self.priority}")
        if self.pet is None and not self.pet_id and self.title:
            self.pet_id = None
        if owner is not None and self.pet is not None and self.pet.owner is not None and self.pet.owner is not owner:
            raise ValueError("Task pet does not belong to this owner.")
        if owner is not None and self.pet is None and self.pet_id is not None:
            matching_pet = owner.get_pet(self.pet_id)
            if matching_pet is None:
                raise ValueError("Task pet assignment is invalid.")
            self.pet = matching_pet
            self.pet_id = matching_pet.pet_id
        return self

    @classmethod
    def from_dict(cls, data, owner=None, pets=None):
        pet_ref = data.get("pet")
        pet_id = data.get("pet_id")
        if pets is not None and pet_ref is None and pet_id is None:
            raise ValueError("Task data is missing a pet assignment.")
        if owner is None and pets is not None:
            owner = pets[0].owner if pets and pets[0].owner is not None else None
        resolved_pet = None
        if isinstance(pet_ref, Pet):
            resolved_pet = pet_ref
        elif isinstance(pet_ref, str) and pets is not None:
            for pet in pets:
                if pet.pet_id == pet_ref or pet.name == pet_ref:
                    resolved_pet = pet
                    break
        elif pet_id is not None and pets is not None:
            for pet in pets:
                if pet.pet_id == pet_id:
                    resolved_pet = pet
                    break
        task = cls(
            title=data.get("title") or data.get("description", ""),
            description=data.get("description") or data.get("title", ""),
            time=data.get("time"),
            frequency=data.get("frequency", "once"),
            completed=data.get("completed", False),
            duration_minutes=data.get("duration_minutes", 20),
            priority=data.get("priority", "medium"),
            pet=resolved_pet,
            pet_id=pet_id or (resolved_pet.pet_id if resolved_pet else None),
            preferred_start_minutes=data.get("preferred_start_minutes"),
            latest_end_minutes=data.get("latest_end_minutes"),
            constraints=data.get("constraints", {}),
        )
        task.validate(owner=owner)
        return task

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
    def _resolve_start_time(cls, task, current_minutes):
        start = current_minutes
        if task.preferred_start_minutes is not None:
            start = max(start, task.preferred_start_minutes)
        if task.pet is not None:
            start = max(start, task.pet.preferred_start_minutes())
        if task.latest_end_minutes is not None and start + task.duration_minutes > task.latest_end_minutes:
            raise ValueError(f"Task '{task.title}' does not fit in its latest end window.")
        return start

    @classmethod
    def schedule_tasks(cls, task_dicts, pets, start_hour=8, start_minute=0):
        if not pets:
            return []

        owner = pets[0].owner if pets and pets[0].owner is not None else None
        valid_tasks = []
        invalid_tasks = []
        for raw_task in task_dicts:
            try:
                task = Task.from_dict(raw_task, owner=owner, pets=pets)
                valid_tasks.append(task)
            except (TypeError, ValueError) as exc:
                invalid_tasks.append({"task": raw_task, "error": str(exc)})

        if not valid_tasks:
            return []

        scheduled = []
        pet_counts = {pet.pet_id: 0 for pet in pets}
        remaining = list(enumerate(valid_tasks))
        current_minutes = start_hour * 60 + start_minute

        while remaining:
            max_priority = max(task.priority_value for _, task in remaining)
            candidates = [item for item in remaining if item[1].priority_value == max_priority]
            candidates.sort(key=lambda item: (pet_counts.get(item[1].pet.pet_id if item[1].pet else item[1].pet_id, 0), item[0]))
            chosen_index, chosen_task = candidates[0]
            remaining = [(idx, task) for idx, task in remaining if idx != chosen_index]

            try:
                start = cls._resolve_start_time(chosen_task, current_minutes)
            except ValueError as exc:
                invalid_tasks.append({"task": chosen_task.title, "error": str(exc)})
                continue

            end = start + chosen_task.duration_minutes
            pet_id = chosen_task.pet.pet_id if chosen_task.pet is not None else chosen_task.pet_id
            pet_counts[pet_id] = pet_counts.get(pet_id, 0) + 1
            reasons = [
                f"priority {chosen_task.priority}",
                f"pet fairness count {pet_counts[pet_id]}",
            ]
            if chosen_task.preferred_start_minutes is not None:
                reasons.append("preferred start window")
            if chosen_task.pet is not None and chosen_task.pet.preferences:
                reasons.append("pet-specific preference applied")
            scheduled.append(
                {
                    "start": cls.format_time(start),
                    "end": cls.format_time(end),
                    "title": chosen_task.title,
                    "pet": chosen_task.pet.name if chosen_task.pet is not None else chosen_task.pet_id,
                    "pet_id": pet_id,
                    "priority": chosen_task.priority,
                    "duration_minutes": chosen_task.duration_minutes,
                    "reasons": reasons,
                    "explanation": "; ".join(reasons),
                    "display": (
                        f"{cls.format_time(start)}–{cls.format_time(end)} {chosen_task.title} | "
                        f"Pet: {chosen_task.pet.name if chosen_task.pet is not None else chosen_task.pet_id} | "
                        f"Priority: {chosen_task.priority.capitalize()}"
                    ),
                }
            )
            current_minutes = end

        return scheduled
