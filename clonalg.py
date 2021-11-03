import datetime
import operator

import numpy as np
import random
import logging

import clonalg_settings


# 1. Create Random Cells function
def create_random_population(problem_size, population_size, knapsack, knapsack_capacity):
    """
    function to create random population

    :param problem_size: the number of items to chose from (non-negative integer)
    :param knapsack_capacity: size of the knapsack (non-negative integer)
    :param population_size: number of cells per population

    :return: the created population (list)
    """

    return_population = []
    i = 0
    logging.info(f"population_size {population_size}")

    while i < population_size:

        rand_num = random.random()
        random_current_cell = np.random.choice([0, 1], size=problem_size, p=[1.0 - rand_num, rand_num])

        current_knapsack_cell = check_only_valid_affinity(random_current_cell, knapsack, knapsack_capacity)
        if current_knapsack_cell[2] != 0:
            return_population.append(current_knapsack_cell)
            i += 1

    logging.info(f"Was able to create populations: {len(return_population)}")

    return return_population


# 2 and 5 Select best population
def select_best_cells(best_cells, number_of_best_cells, best_cell):

    best_cells = sorted(best_cells, key=operator.itemgetter(2, 1), reverse=True)
    if best_cell[2] < best_cells[0][2]:
        best_cell = best_cells[0]
    logging.info(f"NUMBER OF MEMORY CELLS {len(best_cells[0:number_of_best_cells])}")

    return best_cells[0:number_of_best_cells], best_cell


# 3. Clone
def clone_best_cells(best_cells, clone_rate):

    result_list = [best_cells[i // clone_rate] for i in range(len(best_cells) * clone_rate)]
    logging.info(f"CLONE POPULATION: {len(result_list)}")

    return result_list


# 4. Hyper mutate
def hyper_mutate(clones, problem_size, knapsack, knapsack_capacity, clone_rate, max_mutation_rate):

    clone_size = len(clones) / clone_rate
    result = []
    no_mutation = 1.0
    mutation = 0.0
    mutation_step = max_mutation_rate / clone_size
    compensate_rounding_error = 0
    i = 0

    for clone in clones:

        mutation_matrix = np.random.choice([0, 1], size=problem_size, p=[no_mutation + compensate_rounding_error, mutation])

        new_clone = np.bitwise_xor(mutation_matrix, clone[0])
        new_clone = check_only_valid_affinity(new_clone, knapsack, knapsack_capacity)
        # check for new_clone[2] != 0 (clone has value) not really necessary
        # as long as check_only_valid_affinity returns only valid cells.
        if new_clone[2] != 0:
            result.append(new_clone)

        i += 1
        if i % clone_rate == 0:
            no_mutation -= mutation_step
            mutation += mutation_step
            compensate_rounding_error = 1.0 - (no_mutation + mutation)
            i = 0

    return result


# Helper function used in 1. create_random_population and 4. hyper_mutate
def check_only_valid_affinity(current_cell, knapsack, knapsack_capacity):
    current_cell_kp_capacity = 0
    current_cell_kp_value = 0

    problem_size = len(knapsack)
    current_cell_temp = [0] * problem_size

    index = random.randint(0, problem_size - 1)
    start_index = index

    # while index < problem_size:
    #     if current_cell[index] == 1:
    #         knapsack_current_capacity += knapsack[index][0]
    #         if knapsack_current_capacity <= knapsack_capacity:
    #             knapsack_current_value += knapsack[index][1]
    #             current_cell_new[index] = 1
    #         else:
    #             knapsack_current_capacity -= knapsack[index][0]
    #             current_cell_new[index] = 0
    #             break
    #
    #     if index == problem_size - 1:
    #         index = 0
    #     else:
    #         index += 1
    #     if index == start_index:
    #         break

    while True:
        if current_cell[index] == 1:
            if current_cell_kp_capacity + knapsack[index][0] <= knapsack_capacity:
                current_cell_kp_capacity += knapsack[index][0]
                current_cell_kp_value += knapsack[index][1]
                current_cell_temp[index] = 1
            else:
                break

        index += 1
        index %= problem_size
        if index == start_index:
            break

    return [current_cell_temp, current_cell_kp_capacity, current_cell_kp_value]


def clonalg(_, knapsack_capacity, knapsack, solution_file_path):
    # Init Settings
    population_size = clonalg_settings.POPULATION_SIZE
    # percentage_of_min_valid_cells = clonalg_settings.PERCENTAGE_OF_MIN_VALID_CELLS
    percentage_of_memory_cells = clonalg_settings.PERCENTAGE_OF_MEMORY_CELLS
    percentage_of_cells_to_be_cloned = clonalg_settings.PERCENTAGE_OF_CELLS_TO_BE_CLONED
    generations = clonalg_settings.GENERATIONS
    clone_rate = clonalg_settings.CLONE_RATE
    max_mutation_rate = clonalg_settings.MAX_MUTATION_RATE

    best_cell = [[], 0, 0, 0]
    generation_first = generations
    first_run = True

    best_value_list = []

    # 1. Create init memory cells population****************************************************************************
    logging.info("CLOANLG STARTED")
    best_populations = create_random_population(
        problem_size=len(knapsack),
        population_size=population_size,
        knapsack=knapsack,
        knapsack_capacity=knapsack_capacity)

    logging.info(f"HAVING A INIT POPULATION OF {len(best_populations)}")

    while generations > 0:

        # 1. Create new random cells************************************************************************************
        if not first_run:

            new_random_populations = create_random_population(
                problem_size=len(knapsack),
                population_size=population_size - len(best_populations),
                knapsack=knapsack,
                knapsack_capacity=knapsack_capacity)

            best_populations.extend(new_random_populations)

            logging.info("+++++++++++++++++")
            logging.info(f"ADDED NEW POPULATION: {len(new_random_populations)}")
            logging.info(f"best_population after append: {len(best_populations)}")
            logging.info("+++++++++++++++++")

        # 2. Create best population Pn**********************************************************************************
        best_populations, best_cell = select_best_cells(
            best_cells=best_populations,
            # number_of_best_populations=population_size,  # TODO think about cap
            number_of_best_cells=int(population_size * percentage_of_cells_to_be_cloned),
            best_cell=best_cell)

        # 3. Clone******************************************************************************************************
        best_populations = clone_best_cells(best_populations, clone_rate)
        # print(f"CLONALG afetr #3: best_population {best_populations} - affinity_list {affinity_list}")

        # 4. Hyper mutate***********************************************************************************************
        # TODO cap best_populations after hypermutation if best_population is greater than X
        best_populations = hyper_mutate(best_populations, len(knapsack), knapsack, knapsack_capacity, clone_rate,
                                        max_mutation_rate)

        # 5. Check mutated clones for affinity**************************************************************************
        best_populations, best_cell = select_best_cells(
            best_cells=best_populations,
            number_of_best_cells=int(population_size * percentage_of_memory_cells),  # TODO think about cap
            best_cell=best_cell)

        generations -= 1

        logging.info(f"****** New Generation: {generation_first - generations} ***************************************")
        logging.info(f"population size after hypermutation: {len(best_populations)}")
        logging.info(f" ADDING new populations {population_size - len(best_populations)}")
        # logging.info(f"best_cell:  {best_cell[1]}, {best_cell[2]}, {best_cell[3]}")
        best_value_list.append(best_cell)
        first_run = False

        if generations == 0:

            time = datetime.datetime.now().timestamp()
            file_path = solution_file_path + str(time) + ".csv"
            knapsack_progress = open(file_path, 'w')

            knapsack_progress.write(f"weight, value\n")
            for best_value in best_value_list:
                knapsack_progress.write(f"{best_value[1]}, {best_value[2]}\n")
            knapsack_progress.close()

    return best_cell[2], best_cell[1], best_cell[0]
