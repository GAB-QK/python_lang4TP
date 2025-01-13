import time
import random
import signal
import sys
import json
from fondation import Operator, Mentalist, Spaceship, Fleet
from save import read_data, save_data

colors = {
    "Menu": "\033[96m",
    "Reset": "\033[0m",
    "Error": "\033[91m",
    "Success": "\033[92m",
    "Warning": "\033[93m",
}

# load file data.json
fleet = read_data("data.json")


def add_member() -> None:
    print("Bonjour ! Ajout d'un membre d'équipage:  \n")
    first_name = input("Prénom du membre d'équipage : ")
    last_name = input("Nom du membre d'équipage : ")
    # check gender M / F
    while True:
        gender = input("Genre du membre d'équipage (M/F) : ").upper()
        if gender in ["M", "F"]:
            break
        else:
            print(
                f"{colors['Warning']}[X] Veuillez entrer 'M' pour masculin ou 'F' pour féminin {colors['Reset']}"
            )
    # check is in int
    while True:
        try:
            age = int(input("Âge du membre d'équipage : "))
            break
        except ValueError:
            print(
                f"{colors['Warning']}[X] Veuillez entrer un nombre valide pour l'âge {colors['Reset']}"
            )

    # Display available roles
    print("Rôles disponibles:")
    for i, role in enumerate(Operator.POSSIBLE_ROLES, 1):
        print(f"{i}. {role}")
    while True:
        try:
            role_choice = int(input("Choisissez un rôle (numéro) : "))
            if 1 <= role_choice <= len(Operator.POSSIBLE_ROLES):
                role = Operator.POSSIBLE_ROLES[role_choice - 1]
                break
            else:
                print(
                    f"{colors['Warning']}[X] Veuillez entrer un numéro valide {colors['Reset']}"
                )
        except ValueError:
            print(
                f"{colors['Warning']}[X] Veuillez entrer un numéro valide {colors['Reset']}"
            )

    # check experience is in int
    while True:
        try:
            experience = int(input("Années d'expérience : "))
            break
        except ValueError:
            print(
                f"{colors['Warning']}[X] Veuillez entrer un nombre valide pour l'experience {colors['Reset']}"
            )

    if multi_check_member(first_name, last_name, age, role) is False:
        new_member = Operator(first_name, last_name, gender, age, role)
        new_member.experience = experience

        # associate the member to a spaceship
        print("Associer le membre à un vaisseau: \n")
        print(
            f"{colors['Menu']}{'Numéro':<10} {'Nom':<20} {'Type':<15} {'Condition':<15} {'Nombre de membres':<20}{colors['Reset']}"
        )
        print("-" * 80)
        for i, spaceship in enumerate(fleet.spaceships):
            print(
                f"{i + 1:<10} {spaceship.name:<20} {spaceship.type:<15} {spaceship.condition:<15} {len(spaceship.crew):<20}"
            )
        while True:
            try:
                choice = int(input("Choisissez un vaisseau (numéro) : "))
                if (
                    1 <= choice <= len(fleet.spaceships)
                ):  # check if the choice is in the range
                    selected_spaceship = fleet.spaceships[choice - 1]
                    result = selected_spaceship.add_member(new_member)
                    print(f"{colors['Success']}[/] {result}{colors['Reset']}")
                    save_data(fleet, "data.json")  # save the updated fleet data
                    break
                else:
                    print(
                        f"{colors['Warning']}[X] Veuillez entrer un numéro valide {colors['Reset']}"
                    )
            except ValueError:
                print(
                    f"{colors['Warning']}[X] Veuillez entrer un numéro valide {colors['Reset']}"
                )
        return


def multi_check_member(first_name: str, last_name: str, age: int, role: str) -> bool:
    print(
        f"{colors['Menu']}Votre enregistrement de membre d'équipage est en étude merci d'attendre la verification du support ... \n{colors['Reset']}"
    )
    time.sleep(2)

    try:
        for spaceship in fleet.spaceships:
            for member in spaceship.crew:
                if member.last_name.lower() == last_name.lower():
                    raise ValueError(
                        "Un des membres d'équipage a déjà ce nom de famille"
                    )  # check if the last name is already in use

        if (
            age < 18 and role.lower() == "technicien"
        ):  # check if the age is valid for the technician role
            raise ValueError(
                "Ce membre d'équipage est trop jeune pour être technicien ! "
            )
        if (
            age < 25 and role.lower() == "pilote"
        ):  # check if the age is valid for the pilot role
            raise ValueError("Ce membre d'équipage est trop jeune pour être Pilote ! ")
        if age > 65:
            raise ValueError(  # check if the age is valid for the crew member
                "Ce membre d'équipage est trop vieux pour faire partie de l'équipage ! "
            )
        if not (
            3 <= len(first_name) <= 15
        ):  # check if the first name and last name are valid between 3 and 15 characters max
            raise ValueError("Le prénom doit contenir entre 3 et 15 caractères")
        if not (
            3 <= len(last_name) <= 15
        ):  # check if the first name and last name are valid between 3 and 15 characters max
            raise ValueError("Le nom doit contenir entre 3 et 15 caractères")
    except ValueError as e:
        print(f"{colors['Error']}[!] {e}{colors['Reset']}")
        return True

    return False


def delete_member() -> None:
    print("Suppression d'un membre d'équipage: \n")
    last_name = input("Nom du membre d'équipage à supprimer : ")
    member_found = False

    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    for spaceship in data["spaceships"]:  # check if the member is in the crew
        for member in spaceship["crew"]:
            if member["last_name"].lower() == last_name.lower():
                spaceship["crew"].remove(member)
                member_found = True
                print(
                    f"{colors['Success']}[/] Membre d'équipage supprimé du vaisseau {spaceship['name']} !{colors['Reset']}"
                )
                break
        if member_found:
            break

    if member_found:
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        # Update the fleet data
        global fleet
        fleet = read_data("data.json")
    else:
        print(
            f"{colors['Error']}[!] Aucun membre d'équipage avec ce nom de famille trouvé{colors['Reset']}"
        )


def display_crew() -> None:
    print("\nMembres d'équipage: \n")
    print(
        f"{colors['Menu']}{'Prénom':<15} {'Nom':<15} {'Genre':<5} {'Âge':<5} {'Rôle':<20} {'Expérience':<10} {'Mana':<10}{colors['Reset']}"
    )  # header
    print("-" * 85)

    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    for spaceship in data["spaceships"]:
        for member in spaceship["crew"]:
            role = member["role"] if "role" in member else member["class"]
            experience = (
                member["experience"] if member.get("experience") is not None else "N/A"
            )
            mana = member.get("mana", "")
            print(
                f"{member['first_name']:<15} {member['last_name']:<15} {member['gender']:<5} {member['age']:<5} {role:<20} {experience:<10} {mana:<10}"
            )


def check_crew() -> None:  # check if the crew is ready for the mission
    for spaceship in fleet.spaceships:
        if spaceship.check_preparation():
            print(
                f"{colors['Success']}[/] L'équipage du vaisseau {spaceship.name} est prêt pour la mission !{colors['Reset']}"
            )
        else:
            print(
                f"{colors['Error']}[!] L'équipage du vaisseau {spaceship.name} n'est pas prêt à partir. Il doit y avoir au moins 2 membres, un pilote et un technicien.{colors['Reset']}"
            )


def rand_intrusion_in_board() -> bool:  # simulate an intrusion in the spaceship
    for _ in range(1000):
        print(f"{colors['Error']}[!] Intrusion détectée !{colors['Reset']} " * 3)
        time.sleep(0.3)
    print(f"{colors['Menu']}Résolution de l'intrusion ...{colors['Reset']}")
    time.sleep(3)
    print(f"{colors['Success']}[/] Intrusion résolue !{colors['Reset']}")


def rand_resignation() -> None:  # simulate a crew member resignation
    for spaceship in fleet.spaceships:
        if len(spaceship.crew) > 0:
            member = random.choice(spaceship.crew)
            spaceship.crew.remove(member)
            print(
                f"{colors['Warning']}[!] {member.first_name} {member.last_name} a démissionné de l'équipage du vaisseau {spaceship.name} !{colors['Reset']}"
            )


def rand_mentalist_action() -> None:  # simulate a mentalist action
    for spaceship in fleet.spaceships:
        if len(spaceship.crew) > 1:
            mentalist = next(
                (member for member in spaceship.crew if isinstance(member, Mentalist)),
                None,
            )
            if mentalist:
                target = random.choice(
                    [member for member in spaceship.crew if member != mentalist]
                )
                print(mentalist.act(target))


def rand_event(
    game_start: bool,
) -> None | bool:  # simulate a random event and call the corresponding function
    if game_start is True:
        return False
    else:
        events = [rand_mentalist_action, rand_resignation, promote_technician]
        event = random.choice(events)
        event()


def promote_technician() -> None:  # promote a technician to a pilot
    print("Promotion d'un technicien: \n")
    last_name = input("Nom du technicien à promouvoir : ")
    for spaceship in fleet.spaceships:
        for member in spaceship.crew:
            if (
                member.last_name.lower() == last_name.lower()
                and member.role.lower() == "technicien"
            ):
                if member.experience >= 10 and member.age >= 25:
                    member.role = "pilote"
                    print(
                        f"{colors['Success']}[/] Technicien promu au poste de pilote !{colors['Reset']}"
                    )
                    return
                else:
                    print(
                        f"{colors['Error']}[!] Le technicien n'a pas assez d'expérience ou est trop jeune pour être promu pilote.{colors['Reset']}"
                    )
                    return
    print(
        f"{colors['Error']}[!] Aucun technicien avec ce nom de famille trouvé{colors['Reset']}"
    )


def crew_report() -> None:  # display a report of the crew
    print("\nRapport de l'équipage: \n")
    total_members = sum(len(spaceship.crew) for spaceship in fleet.spaceships)
    print(f"Nombre total de membres d'équipage: {total_members}")

    role_distribution = {}
    for spaceship in fleet.spaceships:
        for member in spaceship.crew:
            if isinstance(member, Operator):
                role = member.role
            else:
                role = member.__class__.__name__
            if role in role_distribution:
                role_distribution[role] += 1
            else:
                role_distribution[role] = 1

    print("\nRépartition par rôle:")
    print(f"{colors['Menu']}{'Rôle':<20} {'Nombre':<10}{colors['Reset']}")
    print("-" * 30)
    for role, count in role_distribution.items():
        print(f"{role:<20} {count:<10}")

    print("\nMembres proches de l'âge maximum (65 ans):\n")
    print(
        f"{colors['Menu']}{'Prénom':<15} {'Nom':<15} {'Âge':<5} {'Rôle':<20}{colors['Reset']}"
    )
    print("-" * 55)
    near_max_age = False
    for spaceship in fleet.spaceships:
        for member in spaceship.crew:
            if member.age >= 60:
                if isinstance(member, Operator):
                    role = member.role
                else:
                    role = member.__class__.__name__
                print(
                    f"{member.first_name:<15} {member.last_name:<15} {member.age:<5} {role:<20}"
                )
                near_max_age = True
    if not near_max_age:
        print(
            f"{colors['Success']}Aucun membre proche de l'age limite.{colors['Reset']}"
        )


def fleet_statistics() -> (
    None
):  # display statistics about the fleet ( stupid function but it's just for the example)
    print(fleet.statistics())


def spaceship_statistics() -> (
    None
):  # display statistics about the spaceships, the function is called by the stupid function above
    stats = [
        ["Nom du vaisseau", "Type", "Condition", "Nombre de membres", "Préparation"]
    ]
    for spaceship in fleet.spaceships:
        stats.append(
            [
                spaceship.name,
                spaceship.type,
                spaceship.condition,
                len(spaceship.crew),
                "Prêt" if spaceship.check_preparation() else "Pas prêt",
            ]
        )

    table = "\n".join(
        [
            f"{row[0]:<20} {row[1]:<15} {row[2]:<15} {row[3]:<20} {row[4]}"
            for row in stats
        ]
    )
    print(
        f"\n{colors['Menu']}Statistiques des vaisseaux:\n{'-' * 70}\n{table}{colors['Reset']}"
    )


def add_spaceship() -> None:  # add a spaceship to the fleet
    print("Ajout d'un vaisseau: \n")
    name = input("Nom du vaisseau : ")
    type = input("Type du vaisseau (transport/guerre/marchand) : ").lower()
    try:
        new_spaceship = Spaceship(name, type)
        result = fleet.add_spaceship(new_spaceship)
        print(f"{colors['Success']}[/] {result}{colors['Reset']}")
        save_data(fleet, "data.json")  # Save the updated fleet data
    except ValueError as e:
        print(f"{colors['Error']}[!] Erreur: {e}{colors['Reset']}")


def recharge_mana() -> None:  # reload the mana of a mentalist
    print("Recharger le mana d'un mentaliste: \n")
    last_name = input("Nom du mentaliste : ")
    for spaceship in fleet.spaceships:
        mentalist = next(
            (
                member
                for member in spaceship.crew
                if isinstance(member, Mentalist)
                and member.last_name.lower() == last_name.lower()
            ),
            None,
        )
        if mentalist:
            print(mentalist.recharge_mana())
            return
    print(
        f"{colors['Error']}[!] Aucun mentaliste avec ce nom de famille trouvé{colors['Reset']}"
    )
