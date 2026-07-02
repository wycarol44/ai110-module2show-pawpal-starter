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
    def __init__(self, title="Morning walk", duration_minutes=20, priority="medium", pet=None):
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.pet = pet
