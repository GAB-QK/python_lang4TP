import json
from fondation import Fleet, Spaceship, Operator, Mentalist

def save_data(fleet: Fleet, file_name: str) -> None:
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = {"name": fleet.name, "spaceships": []}

    data = {
        "name": fleet.name,
        "spaceships": existing_data["spaceships"]
    }

    existing_spaceship_names = {spaceship["name"] for spaceship in existing_data["spaceships"]}

    for spaceship in fleet.spaceships: 
        if spaceship.name not in existing_spaceship_names: # if the spaceship is not in the existing data add it
            spaceship_data = {
                "name": spaceship.name,
                "type": spaceship.type,
                "condition": spaceship.condition,
                "crew": []
            }
            data["spaceships"].append(spaceship_data)
        else:                                             # if the spaceship is in the existing data, update the crew members     
            for existing_spaceship in data["spaceships"]:
                if existing_spaceship["name"] == spaceship.name: #
                    existing_member_names = {member["last_name"] for member in existing_spaceship["crew"]}
                    for member in spaceship.crew:
                        if member.last_name not in existing_member_names:
                            if isinstance(member, Operator):
                                member_data = {
                                    "first_name": member.first_name,
                                    "last_name": member.last_name,
                                    "gender": member.gender,
                                    "age": member.age,
                                    "role": member.role,
                                    "experience": member.experience
                                }
                            existing_spaceship["crew"].append(member_data)

    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_data(file_name: str) -> Fleet:
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
        fleet = Fleet(data['name'])
        for spaceship_data in data['spaceships']:
            spaceship_type = spaceship_data['type'].lower()
            spaceship = Spaceship(spaceship_data['name'], spaceship_type)
            spaceship.condition = spaceship_data['condition']
            for member_data in spaceship_data['crew']:
                if 'role' in member_data and member_data['role'] in Operator.POSSIBLE_ROLES: # load Operator or Mentalist
                    member = Operator(
                        member_data['first_name'],
                        member_data['last_name'],
                        member_data['gender'],
                        member_data['age'],
                        member_data['role']
                    )
                    member.experience = member_data['experience'] 
                else: 
                    member = Mentalist(
                        member_data['first_name'],
                        member_data['last_name'],
                        member_data['gender'],
                        member_data['age']
                    )
                    member.mana = member_data.get('mana', 100) 
                spaceship.add_member(member) # read the member associate to the spaceship
            fleet.add_spaceship(spaceship)  # read the spaceship associate to the fleet
        return fleet

def read_data(file_name: str) -> Fleet:
    try:
        return load_data(file_name)
    except FileNotFoundError:
        print(f"Le fichier {file_name} n'existe pas.")
        return Fleet("Galactic Fleet")

fleet = Fleet("Galactic Fleet")

file_name = 'data.json'
save_data(fleet, file_name)

loaded_fleet = load_data(file_name)
print(loaded_fleet)