import parse_commandline
from timeit import timeit
import logging

import clonalg_settings


def parse_line(line):
    """Line parser method
    :param line: line from input file
    :return: tuple like: (instance id, number of items, knapsack capacity,
                            list of tuples like: [(weight, cost), (weight, cost), ...])
    """
    parts = [int(value) for value in line.split()]
    inst_id, problem_size, knapsack_max_size = parts[0:3]
    weight_cost = [(parts[i], parts[i + 1]) for i in range(3, len(parts), 2)]
    return inst_id, problem_size, knapsack_max_size, weight_cost


def solver(method, problem_size, knapsack_max_size, knapsack, solution_file_path):
    """Main method that solves knapsack problem using one of the existing methods

    :param method: knapsack problem solving method
    :param inst_file: path to file with input instances
    """
    result = []
    best_value, used_capacity, best_combination = method(problem_size, knapsack_max_size, knapsack, solution_file_path)
    best_combination_str = " ".join("%s" % i for i in best_combination)
    result.append([inst_id, problem_size, knapsack_max_size, best_value, used_capacity, best_combination_str])
    print("*******SOLVER**********************")
    print(f"used_capacity: {used_capacity}")
    print(f"best_value: {best_value}")
    print("*******END SOLVER**********************")
    return result


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    args = parse_commandline.parse_commandline()

    print("******** timeit for solver...")

    problem_file = open(args.problem_file_path, 'r')
    output = list()

    inst_id = 0
    problem_size = 0
    knapsack_max_size = 0
    knapsack = []
    first_run = True

    for line in problem_file:
        inst_id, problem_size, knapsack_max_size, knapsack = parse_line(line)

    time = timeit(stmt='output.append(solver(args.method, problem_size, knapsack_max_size, knapsack, args.solution_file_path))',
                  setup='from __main__ import solver, args, output, problem_size, knapsack_max_size, knapsack',
                  number=args.repeat)

    average_time = time / args.repeat

    problem_file.close()

    # write best result to file
    solution_file = open(args.solution_file_path, 'w')
    solution_file_data_only = open(args.solution_file_path + "_data_only.csv", 'w')

    for i in range(args.repeat):
        solution_file.write(f"{time} {average_time} {output[i][0]}\n")
        my_list = []
        for a in range(5):
            my_list.append(output[i][0][a])

        if first_run:
            solution_file_data_only.write(f"{args.method.__name__}, {my_list[0]}, {my_list[1]}, {my_list[2]}, {time}, {average_time}\n")
            solution_file_data_only.write(
                f"id, weight, value\n")
        first_run = False
        solution_file_data_only.write(f"{i}, {my_list[4]}, {my_list[3]} \n")

    solution_file.close()
    solution_file_data_only.close()

    solution_file_settings = open(args.solution_file_path + "_settings.csv", 'w')
    solution_file_settings.write(f"POPULATION_SIZE, {clonalg_settings.POPULATION_SIZE}\n"
                                 f"GENERATIONS, {clonalg_settings.GENERATIONS}\n"
                                 f"CLONE_RATE, {clonalg_settings.CLONE_RATE}\n"
                                 f"MAX_MUTATION_RATE, {clonalg_settings.MAX_MUTATION_RATE}\n"
                                 f"PERCENTAGE_OF_MEMORY_CELLS, {clonalg_settings.PERCENTAGE_OF_MEMORY_CELLS}\n"
                                 f"PERCENTAGE_OF_CELLS_TO_BE_CLONED, {clonalg_settings. PERCENTAGE_OF_CELLS_TO_BE_CLONED}\n"
                                 )
    solution_file_settings.close()

    print(f'Time for solver: {time}')
    print(f'Average Time for solver: {average_time}')
    print("******** END timeit for solver...")







