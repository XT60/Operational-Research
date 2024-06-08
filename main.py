import json
import random
import threading
from hyperopt import hp, fmin, tpe, Trials, STATUS_OK
from src.rubikscube import RubiksCube
from src.solver import BeesAlgorithm
from src.drawer import Drawer
from src.permutation_table import viable_moves


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

# Default configuration
DEFAULT_CONFIG = {
    "mode": "both",  # other modes: "solver", "visualizer", "solver+visualizer", "optim"
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

def objective(params):
    cube = RubiksCube(" ".join(random.choices(viable_moves, k=50)))  # use random scramble for each trial
    solver = BeesAlgorithm(cube, **params)
    lock = threading.Lock()
    stop_event = threading.Event()
    metrics = solver.run_solver(lock, stop_event)  # Ensure this method returns metrics like solve time
    return {'loss': metrics['solve_time'], 'status': STATUS_OK}

def main():
    config = load_config()
    lock = threading.Lock()
    stop_event = threading.Event()

    scramble = config['manual_scramble'] or " ".join(random.choices(viable_moves, k=config['scramble_moves_count']))
    cube = RubiksCube(scramble)

    mode = config['mode']

    if mode == "optim":
        space = {
            'initial_population_size': hp.choice('initial_population_size', range(2, 150)),
            'num_scouts': hp.choice('num_scouts', range(2, 150)),
            'num_local_searches': hp.choice('num_local_searches', range(2, 150))
        }
        trials = Trials()
        best = fmin(objective, space, algo=tpe.suggest, max_evals=200, trials=trials)
        print("Best hyperparameters:", best)
        return

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
        solver.set_save(config['solver_settings']['save_solution'])
        solver_thread = threading.Thread(target=solver.solver_thread, args=(lock, stop_event, drawer.update_cube if mode == 'solver+visualizer' else None))
        solver_thread.start()

    if mode in ['solver+visualizer', 'visualizer', 'solver']:
        if 'drawer_thread' in locals():
            drawer_thread.join()
        if 'solver_thread' in locals():
            solver_thread.join()

if __name__ == "__main__":
    main()
