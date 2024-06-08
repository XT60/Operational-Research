import random
import time
import csv
import os
import tqdm
from .rubikscube import RubiksCube
from .permutation_table import translate_moves


class BeesAlgorithm:
    def __init__(self, cube, initial_population_size, num_scouts, num_local_searches, max_iterations):
        """
        Initializes a new instance of the Bees Algorithm solver for cube problems.

        The constructor sets up the initial state and parameters for solving the cube using the Bees Algorithm, mimicking
        the natural foraging behavior of bees. The cube is scrambled initially to diversify the starting conditions. A
        population of cubes is created from copies of the scrambled cube to simulate a swarm of bees exploring the search space.

        Args:
            cube (Cube): The cube instance that serves as the basis for all operations.
            initial_population_size (int): The size of the cube population at the start, representing the swarm size.
            num_scouts (int): The number of scout bees used to identify promising regions in the search space.
            num_local_searches (int): The number of searches each selected site undergoes, similar to bees exploring a neighborhood.
            max_iterations (int): The maximum number of iterations or foraging rounds the algorithm performs.

        Attributes:
            best_cubes (list): Initially contains just the base cube, intended to store the best solutions found (best sites).
            cube (Cube): The original cube instance, used as a reference and to reset and scramble (source hive).
            solved_cube (Cube): A copy of the original cube intended to represent the solved state.
            initial_population_size (int): The number of cubes in the initial population, representing the swarm size.
            population (list): The initial population of cube instances derived from the base cube, representing the swarm.
            num_scouts (int): Number of scout bees.
            num_local_searches (int): Number of local search iterations per promising site.
            max_iterations (int): The maximum number of foraging rounds.
            score_threshold (int): A threshold used to determine the intensity and type of mutations during search, similar to choosing richer sites for more intense exploration.
            solution (str): The final solution found by the algorithm, represented as a sequence of moves.
            save (bool): A flag indicating whether to save the solution to a file.

        The initialization scrambles the base cube to provide varied starting conditions for the evolutionary process,
        akin to sending out scout bees from the hive.
        """
        self.best_cubes = [cube]
        self.cube = cube
        self.cube.reset_state()
        self.cube.make_alg("scramble")
        self.solved_cube = cube.copy()
        self.initial_population_size = initial_population_size
        self.population = [cube.copy() for _ in range(initial_population_size)]
        self.num_scouts = num_scouts
        self.num_local_searches = num_local_searches
        self.max_iterations = max_iterations
        self.score_threshold = 5
        self.solution = ""
        self.save = False

        self.execution_id = int(time.time())  # Unique ID for each execution based on current time
        self.init_csv_files()


    def set_save(self, save):
        """
        Sets the flag to save the solution to a file.

        Args:
            save (bool): A flag indicating whether to save the solution to a file.
        """
        self.save = save

    def local_search(self, cube):
        """
        Performs local search to improve a given cube using a set number of search iterations defined by `self.num_local_searches`.
        This method aims to fine-tune a cube by exploring nearby configurations and identifying potentially better solutions.

        Executes local searches on a given cube to simulate the intense exploration of a promising site by bees.

        This method refines a cube by simulating bees performing a thorough search around a promising site. It attempts
        to locally optimize a cube by exploring minor variations in its configuration, aiming to find a better solution
        near the current state.

        Each iteration involves:
        - Creating a candidate cube by copying the original.
        - Depending on the cube's fitness scores, different algorithms are applied:
            * If the corner fitness score is zero, edge-oriented algorithms are applied.
            * Otherwise, corner-oriented algorithms are applied.
        - The intensity and type of algorithms depend on the cube's current score relative to a predefined threshold.
        - After applying an algorithm, the candidate's fitness is reassessed.
        - If the candidate's fitness is better than the best known fitness, it becomes the new best solution.

        Args:
            cube (Cube): The cube instance to be locally searched.

        Returns:
            Cube: The best cube found during the local search, which may be the original cube or a better version of it.

        This method aims to incrementally improve the cube's configuration by minimizing its fitness score through targeted applying of algorithms.
        """
        best = cube.copy()
        best_fitness, best_fitness_edges, best_fitness_corners = best.get_score()

        for _ in range(self.num_local_searches):
            candidate = cube.copy()
            candidate_fitness, candidate_fitness_edges, candidate_fitness_corners = candidate.get_score()
            if candidate_fitness_corners == 0:
                if candidate_fitness <= self.score_threshold:
                    candidate.make_alg("random_moves_algs_moves_prim_edges", move_count=random.randint(1, 2))
                else:
                    candidate.make_alg("random_moves_algs_moves_prim_edges", move_count=random.randint(1, 4))
            else:
                candidate.make_alg("random_moves_algs_moves_prim_corners", move_count=random.randint(1, 2))
            candidate_fitness = candidate.get_score()[0]
            if candidate_fitness < best_fitness:
                best = candidate.copy()
                best_fitness = candidate_fitness
        return best

    def global_search(self):
        """
        Performs a global search to generate a new population of cubes by exploring promising regions identified by scout bees.

        This method mimics the behavior of bees scouting for new sites. It assesses the fitness of cubes from the best
        performers and generates new solutions based on those with promising results. Scout bees (iterations) diversify
        the search, focusing on regions around the best solutions found in the population.

        Executes a global search to generate a new population of cubes by enhancing selected cubes from the best performers and the base cube.
        The method utilizes a strategy that includes both diversification and intensification to explore different configurations of the cubes.

        The method iterates over a predefined number of scouts (`self.num_scouts`), applying different strategies based on the cubes' scores:
        - A portion of the iterations specifically targets the best performing cubes (`best_cubes`).
        - Other iterations use a copy of a generic cube (`cube`).

        During each iteration:
        - If the cube's corner score is zero and meets specific conditions, or if the score does not meet the conditions but still qualifies based on thresholds, a cube from `best_cubes` is copied and potentially modified.
        - Otherwise, the base cube is copied.
        - Depending on the cube's fitness scores, different algorithms are applied to mutate the cube:
            * If the corner score is zero, edge-focused algorithms are applied.
            * Otherwise, corner-focused algorithms are applied.
            * The number and type of moves depend on whether the cube's score is below a set threshold.

        The method employs random numbers to determine the amount of exploring applied, making each exploring step stochastic in nature.

        Returns:
            list: A list of new cube instances that make up the new population for subsequent rounds of exploring.
        """

        new_population = []
        j = 0
        for i in tqdm.tqdm(range(self.num_scouts), desc="global_search"):

            # Choose a cube from the best cubes if the score (corner_score or edge_score) is below the threshold
            # Fifth of the cubes will be from the best cubes, the rest from the base cube
            corner_score = self.best_cubes[0].get_score()[2]
            edge_score = self.best_cubes[0].get_score()[1]
            if (corner_score == 0 and (i % 5 == 0 or edge_score <= self.score_threshold)) or (
                    corner_score != 0 and (i % 5 == 0 or corner_score <= self.score_threshold)):
                if j >= len(self.best_cubes) or (corner_score == 0 and edge_score > self.score_threshold + 3) or (
                        corner_score != 0 and corner_score > self.score_threshold + 3):
                    new_cube = self.best_cubes[0].copy()
                else:
                    new_cube = self.best_cubes[int(j)].copy()
                    j += 0.2
            else:
                new_cube = self.cube.copy()

            new_cube_fitness, new_cube_fitness_edges, new_cube_fitness_corners = new_cube.get_score()

            # If the corner_score is 0, random edge algorithms are applied, else random corner algorithms are applied
            # If the score is below the threshold, the number of moves for edges is limited to 4,
            # else it is limited to 60
            if new_cube_fitness_corners == 0:
                if new_cube_fitness <= self.score_threshold:
                    new_cube.make_alg("random_moves_algs_moves_prim_edges", move_count=random.randint(1, 4))
                else:
                    new_cube.make_alg("random_algs_edges", move_count=random.randint(0, 60))
                    new_cube.make_alg("random_moves_algs_moves_prim_edges", move_count=random.randint(1, 40))
            else:
                new_cube.make_alg("random_moves_algs_moves_prim_corners", move_count=random.randint(1, 30))
            new_population.append(new_cube)
        return new_population

    def solve(self):
        """
        Performs one iteration of the solving process for a population of cubes.
        This method integrates both local and global search strategies,
        improves the population based on their scores, and determines the best solutions.

        The process involves:
        1. Applying a local search to each cube in the current population.
        2. Extending the population with results from a global search.
        3. Sorting the population based on the cubes' scores, prioritizing cubes with a specific score pattern.
        4. Selecting the top 25% of cubes based on their scores to keep in `best_cubes`.
        5. Reducing the population to the top 50% based on their scores for further processing.

        During the sort operation, each cube is sorted by the third element of its score tuple (corner_score) primarily,
        and conditionally by the second element (edge_score) if the third element is zero.

        After sorting and trimming the population:
        - The method checks each cube in the population to see if it has been solved (i.e., first element of the score is 0).
        - If a solved cube is found, the method returns `True`, along with the solved cube and its move history translated into
          more readable moves.

        Returns:
            tuple: A tuple containing a boolean indicating if a solution was found, the best cube (solved or not), and its
                   move history. If no solution was found, returns the first cube from the sorted list and an empty list of moves.
        """

        self.population = [self.local_search(cube) for cube in tqdm.tqdm(self.population, desc="local_search")]

        self.population.extend(self.global_search())

        self.population.sort(key=lambda x: (x.get_score()[2], x.get_score()[1] if x.get_score()[2] == 0 else 0))
        self.best_cubes = self.population[:len(self.population) // 4]
        self.population = self.population[:len(self.population) // 2]

        for cube in self.population:
            if cube.get_score()[0] == 0:
                cube.solved = True
                return True, cube, translate_moves(cube.move_history)
        return False, self.population[0], []

    def init_csv_files(self):
        # Execution log file
        if not os.path.exists('execution_log.csv'):
            with open('execution_log.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'initial_population_size', 'num_scouts', 'num_local_searches',
                    'max_iterations', 'execution_id', 'num_iterations', 'execution_time'
                ])

        # Iteration log file
        if not os.path.exists('iteration_log.csv'):
            with open('iteration_log.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'initial_population_size', 'num_scouts', 'num_local_searches',
                    'max_iterations', 'execution_id', 'iteration', 'score', 'corner_score', 'edge_score'
                ])

    def log_execution(self, num_iterations, execution_time):
        with open('execution_log.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                self.initial_population_size, self.num_scouts, self.num_local_searches,
                self.max_iterations, self.execution_id, num_iterations, execution_time
            ])

    def log_iteration(self, iteration, score, corner_score, edge_score):
        with open('iteration_log.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                self.initial_population_size, self.num_scouts, self.num_local_searches,
                self.max_iterations, self.execution_id, iteration, score, corner_score, edge_score
            ])
    def run_solver(self, lock, stop_event, callback=None):
        """
        Executes the solving process for the Rubik's Cube in a potentially multithreaded environment. It uses a stop event
        to allow external control over the duration of the solving process and a lock to handle resource synchronization.

        This method iteratively applies the solving algorithm to the cube, updating the cube's state and checking if the
        solution is reached or if the stop event is triggered. Each iteration involves evaluating the cube's current
        score and optionally updating external observers via a callback function.

        Args:
            lock (threading.Lock): A lock used to synchronize access to shared resources, particularly for the callback and updating the cube state.
            stop_event (threading.Event): An event that can be set externally to signal the solver to stop running.
            callback (function, optional): A function to call after each iteration, which receives the latest solution and the cube state.

        Workflow:
            1. Initialize the solving process and display the initial state.
            2. Enter a loop that continues until the cube is solved, the stop event is set, or the maximum number of iterations is reached.
            3. In each iteration, apply the solve method, update the cube's state, and invoke the callback with the current solution.
            4. After exiting the loop, check the reason for termination: solution found, aborted by stop event, or iteration limit reached.
            5. Display the final state and statistics, including the total time taken for the attempt.

        Note:
            - The method prints detailed information about each iteration's progress and the final outcome directly to the console.
            - The callback function, if provided, should accept two parameters: the list of moves and the cube object, allowing external
              components to respond to updates in real time.
        """
        print(f"________________________\nIteration: {0}")

        print(f"\nScore: {self.solved_cube.get_score()[0]}\nScore_corners: {self.solved_cube.get_score()[2]}\n"
              f"Score_edges: {self.solved_cube.get_score()[1]}\n________________________\n\n")

        is_solved = False
        i = 0
        start_time = time.time()
        while not stop_event.is_set() and not is_solved and not i > self.max_iterations:
            if i != 0:
                print(f"________________________\nIteration: {i}")

            is_solved, new_cube, solution = self.solve()
            new_cube = new_cube.copy()

            with lock:
                if callback:
                    callback(solution, new_cube)
                self.solved_cube = new_cube.copy()

            score = self.solved_cube.get_score()[0]
            corner_score = self.solved_cube.get_score()[2]
            edge_score = self.solved_cube.get_score()[1]
            self.log_iteration(i, score, corner_score, edge_score)

            print(
                f"\nScore: {self.solved_cube.get_score()[0]}\nScore_corners: {self.solved_cube.get_score()[2]}\n"
                f"Score_edges: {self.solved_cube.get_score()[1]}\n________________________\n\n")

            i += 1
        end_time = time.time()

        found_solution = " ".join(translate_moves(self.solved_cube.move_history))
        execution_time = int(end_time - start_time)

        if is_solved:
            print(
                f"\n\n\n________________________________________________\n\nSolved the Rubik's Cube!\n\n"
                f"Found Solution: \n\n{found_solution}\n\n________________________________________________\n\n")
            self.solution = found_solution
            print(f"Time taken: {int(end_time - start_time)} seconds")
            if self.save:
                solution_filename = f"solution_{int(time.time())}.txt"
                with open("solutions/" + solution_filename, 'w') as file:
                    file.write(f"Solution for: {self.solved_cube.get_scramble()}\n"
                               f"Found in {int(end_time - start_time)} seconds "
                               f"with {i} iterations\n"
                               f"with following parameters: initial_population_size={self.initial_population_size},"
                               f" num_scouts={self.num_scouts}, num_local_searches={self.num_local_searches},"
                               f" max_iterations={self.max_iterations}\n\n"
                               f"\n\n{found_solution}")
                print(f"Solution saved to {solution_filename}")

        elif i > self.max_iterations:
            if callback:
                callback(self.population[0].move_history, self.population[0])
            print("Above Limit, Aborting")

        else:
            if callback:
                callback([], self.solved_cube)
            print("Aborted")
        self.log_execution(i, execution_time)
        return execution_time if is_solved else execution_time * 2

    def solver_thread(self, lock, stop_event, callback=None):
        if callback is not None:
            time.sleep(2)
        self.run_solver(lock, stop_event, callback=callback)
