import random
import tqdm
from .rubikscube import RubiksCube
from .permutation_table import translate_moves


class BeesAlgorithm:
    def __init__(self, cube, initial_population_size, num_scouts, num_local_searches, max_iterations):

        self.best_cubes = [cube]
        self.cube = cube
        self.cube.reset_state()
        self.cube.make_alg("scramble")
        self.population = [cube.copy() for _ in range(initial_population_size)]
        self.num_scouts = num_scouts
        self.num_local_searches = num_local_searches
        self.max_iterations = max_iterations
        self.score_threshold = 5

    def local_search(self, cube):
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
        new_population = []
        j = 0
        for i in tqdm.tqdm(range(self.num_scouts), desc="global_search"):
            if self.best_cubes[0].get_score()[2] == 0:
                if i % 5 == 0 or self.best_cubes[0].get_score()[1] <= self.score_threshold:
                    if j >= len(self.best_cubes) or self.best_cubes[0].get_score()[1] > self.score_threshold + 3:
                        new_cube = self.best_cubes[0].copy()
                    else:
                        new_cube = self.best_cubes[int(j)].copy()
                        j += 0.2
                else:
                    new_cube = self.cube.copy()
            else:
                if i % 5 == 0 or self.best_cubes[0].get_score()[2] <= self.score_threshold:
                    if j >= len(self.best_cubes) or self.best_cubes[0].get_score()[2] > self.score_threshold + 3:
                        new_cube = self.best_cubes[0].copy()
                    else:
                        new_cube = self.best_cubes[int(j)].copy()
                        j += 0.2
                else:
                    new_cube = self.cube.copy()

            new_cube_fitness, new_cube_fitness_edges, new_cube_fitness_corners = new_cube.get_score()
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

    def solve(self, iter_num=-1):
        if iter_num == -1:

            for iteration in range(self.max_iterations):
                self.population = [self.local_search(cube) for cube in self.population]
                self.population.extend(self.global_search())
                self.population.sort(key=lambda x: x.get_score()[2] * 10000 + x.get_score()[1])
                self.population = self.population[:(len(self.population) * 3) // 4]

                for cube in self.population:
                    if cube.get_score()[0] == 0:
                        return True, self.population[0], translate_moves(cube.move_history)
                return False, self.population[0], []
        else:
            if iter_num > self.max_iterations:
                return False, self.population[0], ["Above Limit"]
            self.population = [self.local_search(cube) for cube in tqdm.tqdm(self.population, desc="local_search")]
            self.population.extend(self.global_search())
            self.population.sort(key=lambda x: (x.get_score()[2], x.get_score()[1] if x.get_score()[2] == 0 else 0))
            self.best_cubes = self.population[:len(self.population) // 4]
            # self.population = self.population[:len(self.population * 3) // 4]  # Keep the best half
            self.population = self.population[:len(self.population) // 2]  # Keep the best half
            # self.population = self.population[:len(self.population) // 5]  # Keep the best fifth
            for cube in self.population:
                if cube.get_score()[0] == 0:
                    return True, cube, translate_moves(cube.move_history)
            return False, self.population[0], []
