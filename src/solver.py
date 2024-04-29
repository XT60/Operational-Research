import random
import tqdm
from .rubikscube import RubiksCube


class BeesAlgorithm:
    def __init__(self, cube, initial_population_size, num_scouts, num_local_searches, max_iterations):

        self.best_cubes = [cube]
        self.cube = cube
        self.cube.make_alg("scramble")
        self.population = [cube.copy() for _ in range(initial_population_size)]
        self.num_scouts = num_scouts
        self.num_local_searches = num_local_searches
        self.max_iterations = max_iterations

    def local_search(self, cube):
        best = cube.copy()
        best_fitness = best.get_score()

        for _ in range(self.num_local_searches):
            candidate = cube.copy()
            candidate_fitness = candidate.get_score()
            if candidate_fitness < 10:
                candidate.make_alg("random_algs", move_count=1)
            else:
                candidate.make_alg("random_algs", move_count=random.randint(1, 10))
                candidate.make_alg("random_moves", move_count=random.randint(0, 2))
            candidate_fitness = candidate.get_score()
            if candidate_fitness < best_fitness:
                best = candidate.copy()
                best_fitness = candidate_fitness
        return best

    def global_search(self):
        new_population = []
        j = 0
        for i in tqdm.tqdm(range(self.num_scouts), desc="global_search"):

            if i % 3 == 0:
                if j >= len(self.best_cubes):
                    new_cube = self.cube.copy()
                else:
                    new_cube = self.best_cubes[int(j)].copy()
                    j += 0.5
            else:
                new_cube = self.cube.copy()
            if new_cube.get_score() < 10:
                new_cube.make_alg("random_algs", move_count=4)
            else:
                new_cube.make_alg("random_moves", move_count=random.randint(0, 30))
                new_cube.make_alg("random_algs", move_count=random.randint(20, 30))
            new_population.append(new_cube)
        return new_population

    def solve(self, iter_num=-1):
        if iter_num == -1:

            for iteration in range(self.max_iterations):
                self.population = [self.local_search(cube) for cube in self.population]
                self.population.extend(self.global_search())
                self.population.sort(key=lambda x: x.get_score())
                self.population = self.population[:(len(self.population)*3) // 4]

                for cube in self.population:
                    if cube.get_score() == 0:
                        print("Solved!")
                        print(cube.move_history)
                        return True, self.population[0]
        else:
            print(f"Iteration: {iter_num}")
            if iter_num > self.max_iterations:
                print("Above Limit")
                return False, self.population[0]
            self.population = [self.local_search(cube) for cube in tqdm.tqdm(self.population, desc="local_search")]
            self.population.extend(self.global_search())
            self.population.sort(key=lambda x: x.get_score())
            self.best_cubes = self.population[:len(self.population)//5]
            self.population = self.population[:len(self.population) // 2]  # Keep the best half
            for cube in self.population:
                if cube.get_score() == 0:
                    print("Solved!")
                    print(cube.move_history)
                    return True, cube
            return False, self.population[0]
