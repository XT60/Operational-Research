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

## License
This project is open-sourced under the MIT license.

## Author
[Your Name]

---

Feel free to customize any part of this README.md to better fit the specifics of your project or to add additional sections such as "Contributing," "Future Improvements," or "Acknowledgments" as needed.