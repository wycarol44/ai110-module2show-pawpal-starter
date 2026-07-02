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
