import json
import random
import threading
from src.rubikscube import RubiksCube
from src.solver import BeesAlgorithm
from src.drawer import Drawer
from src.permutation_table import viable_moves

# Default configuration
DEFAULT_CONFIG = {
    "mode": "both",
    "scramble_moves_count": 50,
    "manual_scramble": "",
    "solver_settings": {
        "initial_population_size": 50,
        "num_scouts": 50,
        "num_local_searches": 50,
        "max_iterations": 50,
        "save_solution": True,
    },
    "drawer_settings": {
        "initial_delay": 500,
        "delay_solving": 10
    }
}

def load_config(file_path='config.json'):
    """Load configuration from a JSON file and merge with default settings."""
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
        # Merge default config with loaded config
        return {**DEFAULT_CONFIG, **config}
    except FileNotFoundError:
        print("Configuration file not found. Using default settings.")
        return DEFAULT_CONFIG
    except json.JSONDecodeError:
        print("Error decoding JSON. Using default settings.")
        return DEFAULT_CONFIG

def main():
    # Load configuration
    config = load_config()

    # Set up threading
    lock = threading.Lock()
    stop_event = threading.Event()

    # Determine the scramble: manually configured or random
    manual_scramble = config['manual_scramble']
    if manual_scramble:
        scramble = manual_scramble
    else:
        scramble_moves_count = config['scramble_moves_count']
        scramble = " ".join(random.choices(viable_moves, k=scramble_moves_count))

    # Initialize the Rubik's Cube
    cube = RubiksCube(scramble)

    # Check the mode to decide what components to run
    mode = config['mode']

    save = config['solver_settings']['save_solution']


    if mode not in ['solver']:
        drawer_settings = config['drawer_settings']
        drawer = Drawer(cube)
        drawer.set_delays(drawer_settings['initial_delay'], drawer_settings['delay_solving'])
        drawer_thread = threading.Thread(target=drawer.run, args=(stop_event,))
        drawer_thread.start()

    if mode not in ['visualizer']:
        solver_settings = config['solver_settings']
        solver = BeesAlgorithm(
            cube,
            solver_settings['initial_population_size'],
            solver_settings['num_scouts'],
            solver_settings['num_local_searches'],
            solver_settings['max_iterations']
        )
        solver.set_save(save)
        solver_thread = threading.Thread(target=solver.solver_thread, args=(lock, stop_event, drawer.update_cube if mode == 'solver+visualizer' else None))
        solver_thread.start()

    if mode in ['solver+visualizer', 'visualizer', 'solver']:
        # Join threads relevant to the selected mode
        if 'drawer_thread' in locals():
            drawer_thread.join()
        if 'solver_thread' in locals():
            solver_thread.join()

if __name__ == "__main__":
    main()
