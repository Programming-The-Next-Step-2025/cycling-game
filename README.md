# Tourist Bowling - A Pygame Side-Scroller

A fast-paced arcade-style cycling game set in the Netherlands. Dodge potholes, and avoid other bikers. A simulation about biking in a Dutch metropolitan city.
This package is completely built using Python 3.10 and Pygame 2.6.

## Gameplay
Once the game has started, you can dodge obstacles by moving up (UP-Arrow) or down using the DOWN-Arrow on your keyboard. Obstacles will spawn randomly and with decreasing distance, the longer you survive. Good luck and watch out for other bikers!


## Features
- Procedurally generated obstacles
- Progressively more difficult with increasing score
- Obstacle spawning
- Upgrade system (planned)
- Endless runs with high score tracking

## Play the Game
To play the game, please navigate to the game (package) folder and the  
"Executables" folder and select the folder for your operating system.
Next, start the game by executing the .exe / .app file.
Given, the development stage of this game, your operating system might  
flag this as malware. To start the game regardless, you have to bypass the  
firewall (see the vignette inside docs for more information on how to bypass the firewall).
Note: Due to a mistake when creating the Windows .exe the highscore system is not working properly.
Mistake will be fixed in future iterations!


## Manual Installation

1. Clone the repository: 

```bash
git clone https://github.com/Programming-The-Next-Step-2025/cycling-game.git your_folder_name
cd cycling-game #Change directories to where you cloned the repository
``` 

2. Install the game-package
```bash
pip install -e .
``` 

3. Install dependencies (optional if installed via the package):  
```bash
pip install -r requirements.txt
``` 
---

5. **Running the Game**
Please run this code in the VS-Code terminal, as there have been some unfixed bugs when trying to run the game function in the general shell terminal (Please see report.ipynb for more details).

```bash
cycle_game_run
```
Should this function not work,  
you can start the game with:  

```bash
python run.py
```

### Troubleshooting
Should the installation not work, please navigate to the vignette contained in   
the docs folder (see below) for more detailed instructions


# Folder Structure
Here an overview of the general project structure:  

cycling-game/
├── dist/                --> App/.exe files after PyInstaller build
├── docs/                --> Vignette in Jupyter NB form
├── Executables/         --> Pre-built macOS/Windows executables
│   └── MacOS/   
│   └── Windows/   
├── src/                 --> Source code package (cycling_game/)
│   └── cycling_game/   
│       ├── game_test.py    --> The game classes and main code
│       ├── utils.py        --> Functions for loading assets
│       ├── animation.py    --> Functions for creating animation lists
│       ├── entities.py     --> The player and obstacle classes
│       ├── cache.py        --> Contains animation and sprite caches
│       ├── run.py          --> Contains the run_game function
│       └── highscore.txt   --> Contains the highscore
│           └── Resources/          --> Contains all the assets
│               ├── Images/         --> Contains all sprites and animations
│               ├── Font/           --> Contains the font 
│               └── Sounds/         --> Contains game sound
├── LICENSE              --> MIT License
├── README.md            
├── requirements.txt     --> PIP dependencies
├── pyproject.toml       --> Project metadata


## License
MIT License (see License file)

## Contact
For any bugreports, issues or suggestions please reach me at: felix_hofer@gmx.de
