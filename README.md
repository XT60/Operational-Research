# Operational-Research

## Overview
This project features a Rubik's Cube solver implemented in Python, utilizing OpenGL and GLFW for visualization. It employs a combination of permutation algorithms and the Bees Algorithm to efficiently find solutions.

## Files Description
- **drawer.py**: Handles the graphical representation of the Rubik's Cube using OpenGL.
- **permutation_table.py**: Contains move definitions and permutations for cube transformations.
- **rubikscube.py**: Defines the Rubik's Cube model and its operations using numpy arrays.
- **solver.py**: Implements the Bees Algorithm to solve the cube.
- **main.py**: The entry point of the application, setting up and running the visualization.

## Installation
To run this project, you need Python and the following packages, by running:
```bash
pip install glfw PyOpenGL PyOpenGL_accelerate tqdm numpy
```
or 
```bash
pip install -r requirements.txt
```

## Usage
Execute the main script to start the application:
```bash
python main.py
```

## Configuration
Before running the application, you can configure various parameters in the `config.json` file located in the source directory.

### Default Configuration:
If the `config.json` file is not found or is improperly formatted, the application will use the following default settings:
```json
{
  "mode": "both",
  "scramble_moves_count": 50,
  "manual_scramble": "",
  "solver_settings": {
    "initial_population_size": 50,
    "num_scouts": 50,
    "num_local_searches": 50,
    "max_iterations": 50,
    "save_solution": true
  },
  "drawer_settings": {
    "initial_delay": 500,
    "delay_solving": 10
  }
}
```

### Modifying Configuration:
1. Open the `config.json` file in a text editor.
2. Adjust the parameters as needed. Below are the descriptions of each parameter:

#### Parameters:
- **mode**: Determines which components to run. Possible values:
  - `"both"`: Run both the solver and visualizer.
  - `"solver"`: Run only the solver.
  - `"visualizer"`: Run only the visualizer.
- **scramble_moves_count**: Number of random moves to scramble the Rubik's Cube. Ignored if `manual_scramble` is provided.
  - Example: `"scramble_moves_count": 30`
- **manual_scramble**: String of moves to manually scramble the Rubik's Cube. Overrides `scramble_moves_count`.
  - Example: `"manual_scramble": "U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2"`
- **solver_settings**: Settings for the Bees Algorithm solver:
  - **initial_population_size**: Initial population size for the solver.
    - Example: `"initial_population_size": 100`
  - **num_scouts**: Number of scout bees.
    - Example: `"num_scouts": 50`
  - **num_local_searches**: Number of local searches.
    - Example: `"num_local_searches": 50`
  - **max_iterations**: Maximum number of iterations for the solver.
    - Example: `"max_iterations": 200`
  - **save_solution**: Whether to save the solution (the solution will be saved in the `solutions` folder).
    - Example: `"save_solution": false`
- **drawer_settings**: Settings for the visualizer (drawer):
  - **initial_delay**: Initial delay before starting the visualization in frames.
    - Example: `"initial_delay": 1000`
  - **delay_solving**: Delay between each move during solving in frames.
    - Example: `"delay_solving": 20`

After adjusting the configuration file, you can run the program with:
```bash
python main.py
```

## Output
The solution to the Rubik's Cube will be displayed in the console and saved to the solutions folder if save_solution is set to true. The output will include the sequence of moves required to solve the cube and the time taken to find the solution. An example of the output is shown below:

```
Solution for: L2 E' L' F L' F x' y M R' z2 M S2 F2 x2 y' y' E2 L2 z E' y' z x' B' R R U' R S R F2 x2 S' B2 z2 z' L E' D' E2 E U2 D2 S' L2 B' F B U2

Found in 133 seconds with 28 iterations
with following parameters: initial_population_size=50 num_scouts=50 num_local_searches=50 max_iterations=50
```

## License
This project is open-sourced under the MIT license.
