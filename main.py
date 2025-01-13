import subprocess
import os
import signal
import sys
from crew import (
    add_member,
    delete_member,
    display_crew,
    check_crew,
    promote_technician,
    crew_report,
    fleet_statistics,
    spaceship_statistics,
    rand_event,
    colors,
    fleet,
    add_spaceship,
    recharge_mana,
)
from save import save_data, read_data


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")



def Menu():
    global fleet
    fleet = read_data('data.json')  # recharge le fichier json
    choice = input(f"\nChoisissez une option: ")
    clear_terminal()

    try:
        match choice:
            case "1":
                add_member()
            case "2":
                delete_member()
            case "3":
                display_crew()
            case "4":
                check_crew()
            case "5":
                promote_technician()
            case "6":
                crew_report()
            case "7":
                fleet_statistics()
            case "8":
                spaceship_statistics()
            case "9":
                add_spaceship()
            case "10":
                recharge_mana()
            case "11":
                save_data(fleet, 'data.json')
                print(f"{colors['Success']}[/] Données sauvegardées avec succès !{colors['Reset']}")
            case "12":
                quit()
            case _:
                print(
                    f"{colors['Error']}[!] Veuillez entrer un choix valide{colors['Reset']}"
                )
    except Exception as e:
        print(f"{colors['Error']}[!] Erreur: {e}{colors['Reset']}")

    input(
        f"\n{colors['Menu']}Appuyez sur une touche pour revenir au menu...{colors['Reset']}"
    )
    clear_terminal()


def signal_handler(sig, frame):
    print(f"{colors['Warning']}\n[!] Vous avez quitté le programme.{colors['Reset']}")
    save_data(fleet, 'data.json')
    print(f"{colors['Success']}[/] Données sauvegardées avec succès !{colors['Reset']}")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def main():
    global fleet
    fleet = read_data('data.json')
    game_start = True
    event_counter = 0
    while True:
        clear_terminal()
        print("\nMenu: ")
        print("_" * 30)
        print(f"\n{colors['Menu']}1. Ajouter un membre d'équipage")
        print("2. Supprimer un membre d'équipage")
        print("3. Afficher les membres d'équipage")
        print("4. Vérifier l'équipage")
        print("5. Promouvoir un technicien")
        print("6. Rapport de l'équipage")
        print("7. Statistiques de la flotte")
        print("8. Statistiques des vaisseaux")
        print("9. Ajouter un vaisseau")
        print("10. Recharger le mana d'un mentaliste")
        print("11. Sauvegarder les données")
        print(f"12. Quitter {colors['Reset']}")
        print("_" * 30)

        if event_counter == 4:
            game_start = rand_event(game_start)
            event_counter = 0
        else:
            event_counter += 1

        Menu()


if __name__ == "__main__":
    main()
