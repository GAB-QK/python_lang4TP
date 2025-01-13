from typing import List
import random

colors = {
    "Reset": "\033[0m",
    "Menu": "\033[36m",
    "Success": "\033[32m",
    "Error": "\033[31m",
    "Warning": "\033[33m",
}


class Person:
    def __init__(self, first_name: str, last_name: str, gender: str, age: int) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.age = age

    def introduce_yourself(self) -> str:
        return f"Bonjour, je m'appelle {self.first_name} {self.last_name}, je suis {self.gender} et j'ai {self.age} ans"


class Operator(Person):
    POSSIBLE_ROLES = [
        "Commandant",
        "Technicien",
        "Armurier",
        "Entretien",
        "Pilote",
        "Marchand"
    ]
    FUNNY_ACTIONS = [
        "danser frenesique",
        "se couper les cheveux",
        "faire la vaisselle du vaisseau",
        "imiter le capitaine",
        "faire des tours sur lui même",
        "adopter une souris qu'il appelle 'Maurice'",
    ]

    def __init__(
        self, first_name: str, last_name: str, gender: str, age: int, role: str, experience: int = 0
    ) -> None:
        if role.lower() not in [r.lower() for r in self.POSSIBLE_ROLES]:
            raise ValueError(f"Rôle invalide. Rôles possibles: {self.POSSIBLE_ROLES}")
        super().__init__(first_name, last_name, gender, age)
        self.role = role
        self.experience = experience

    def act(self) -> str:
        action = random.choice(self.FUNNY_ACTIONS)
        return f"{action}"

    def gain_experience(self) -> str:
        self.experience += 1
        return f"{self.first_name} {self.last_name} a maintenant {self.experience} niveau d'expérience"


class Mentalist(Person):
    def __init__(self, first_name: str, last_name: str, gender: str, age: int, mana: int = 100) -> None:
        super().__init__(first_name, last_name, gender, age)
        self.mana = mana

    def act(self, target: Operator) -> str:
        if self.mana >= 20:
            self.mana -= 20
            action = target.act()
            return f'{self.first_name} {self.last_name} utilise ses pouvoirs de mentaliste pour influencer {target.first_name} {target.last_name}. et le force a "{action}"'
        else:
            return f"{self.first_name} {self.last_name} n'a pas assez de mana pour agir"

    def recharge_mana(self) -> str:
        self.mana = min(self.mana + 50, 100)
        return f"{self.first_name} {self.last_name} a rechargé son mana !!! Mana actuel: {self.mana}"


class Spaceship:
    POSSIBLE_TYPES = ["transport", "guerre", "marchand"]
    POSSIBLE_CONDITIONS = ["opérationnel", "endommagé"]

    def __init__(self, name: str, type: str, condition: str = "opérationnel") -> None:
        if type not in self.POSSIBLE_TYPES:
            raise ValueError(
                f"Type de vaisseau invalide. Types possibles: {self.POSSIBLE_TYPES}"
            )
        self.name = name
        self.type = type
        self.crew = []
        self.condition = condition

    def add_member(self, person: Person) -> str:
        if len(self.crew) >= 10:
            return "Capacité maximale de l'équipage"
        self.crew.append(person)
        return f"{person.first_name} {person.last_name} a été ajouté à l'équipage"

    def check_preparation(self) -> bool:
        has_pilot = any(
            member.role == "Pilote"
            for member in self.crew
            if isinstance(member, Operator)
        )
        has_technician = any(
            member.role == "Technicien"
            for member in self.crew
            if isinstance(member, Operator)
        )
        return has_pilot and has_technician


class Fleet:
    def __init__(self, name: str) -> None:
        self.name = name
        self.spaceships = []

    def add_spaceship(self, spaceship: Spaceship) -> str:
        if len(self.spaceships) >= 15:
            return "Capacité maximale de la flotte"
        self.spaceships.append(spaceship)
        return f"Le vaisseau {spaceship.name} a été ajouté à la flotte {self.name}"

    def statistics(self) -> str:
        total_members = sum(len(spaceship.crew) for spaceship in self.spaceships)
        operational_ships = sum(
            1 for spaceship in self.spaceships if spaceship.condition == "opérationnel"
        )
        damaged_ships = sum(
            1 for spaceship in self.spaceships if spaceship.condition == "endommagé"
        )

        role_distribution = {}
        total_experience = 0
        operator_count = 0

        for spaceship in self.spaceships:
            for member in spaceship.crew:
                if isinstance(member, Operator):
                    total_experience += member.experience if member.experience is not None else 0
                    operator_count += 1
                    role_distribution[member.role] = (
                        role_distribution.get(member.role, 0) + 1
                    )
                else:
                    role_distribution[member.__class__.__name__] = (
                        role_distribution.get(member.__class__.__name__, 0) + 1
                    )

        average_experience = (
            total_experience / operator_count if operator_count > 0 else 0
        )

        stats = [
            ["Statistique", "Valeur"],
            ["Nombre total de vaisseaux", len(self.spaceships)],
            ["Nombre total de membres d'équipage", total_members],
            ["Vaisseaux opérationnels", operational_ships],
            ["Vaisseaux endommagés", damaged_ships],
            ["Niveau moyen d'expérience des opérateurs", f"{average_experience:.2f}"],
        ]

        for role, count in role_distribution.items():
            stats.append([f"Nombre de {role}", count])

        table = "\n".join([f"{row[0]:<40} {row[1]}" for row in stats])
        return f"\n{colors['Menu']}Flotte {self.name} - Statistiques:\n{'-' * 70}\n{table}{colors['Reset']}"
