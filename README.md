# Galactic Fleet Management

## Overview
This project is a simulation of managing a galactic fleet. It includes functionalities to add, delete, and display crew members, manage spaceships, and save/load fleet data from a JSON file

## Project Structure
- `main.py`: The main entry point of the application. It provides a menu for interacting with the fleet
- `save.py`: Contains functions to save and load fleet data to/from a JSON file
- `fondation.py`: Defines the core classes such as `Fleet`, `Spaceship`, `Operator`, and `Mentalist`
- `crew.py`: Contains functions to manage crew members and handle various events
- `data.json`: The JSON file used to store the fleet data

## How to Run
1. Ensure you have Python installed on your system
2. Clone the repository or download the project files
3. Navigate to the project directory
4. Run the main script:
    ```sh
    python main.py
    ```

## Features
- **Add Crew Member**: Add a new crew member to a spaceship
- **Delete Crew Member**: Remove a crew member from a spaceship
- **Display Crew**: Display all crew members in the fleet
- **Check Crew**: Check if the crew of each spaceship is ready for a mission
- **Promote Technician**: Promote a technician to a pilot if they meet the criteria
- **Crew Report**: Generate a report of the crew members
- **Fleet Statistics**: Display statistics of the fleet
- **Spaceship Statistics**: Display statistics of each spaceship
- **Add Spaceship**: Add a new spaceship to the fleet
- **Recharge Mana**: Recharge the mana of a mentalist
- **Save Data**: Save the current state of the fleet to a JSON file
- **Load Data**: Load the fleet data from a JSON file

## Data Persistence
The fleet data is saved in `data.json`. The data includes the fleet name, spaceships, and crew members with their details. Feel free to add your own data.json to custom your fleet

## Error Handling
The application includes basic error handling to manage invalid inputs and file-related errors

## futur improvement
- Add more functionalities to manage spaceships and crew members
- Implement a GUI with PYGAME or with html interface for a better user experience
- improve save fonction to save the data in a database
- Add more tests to ensure the application is robust

