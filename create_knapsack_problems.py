import random


def create_knapsack_problems(number_of_knapsack_problems, knapsack_problem_size, knapsack_capacity,
                             item_min_weight, item_max_weight, item_min_value, item_max_value,
                             problem_file_path):
    """
    Creates random knapsack problems with a fixed problem size and knapsack capacity. Items and its weights and values
    are randomly selected within a given range.

    :param number_of_knapsack_problems: number of knapsack problems to be created (non-negative integer)
    :param knapsack_problem_size: number of items (non-negative integer)
    :param knapsack_capacity: the maximum weight the knapsack can hold (non-negative integer)
    :param item_min_weight: minimum weight of an item (non-negative integer)
    :param item_max_weight: maximum weight of an item (non-negative integer)
    :param item_min_value: minimum value of an item (non-negative integer)
    :param item_max_value: maximum value of an item (non-negative integer)
    :param problem_file_path: path to the folder, where the knapsack file is stored


    :return: void. Creates the necessary knapsack files
    """

    if number_of_knapsack_problems <= 0:
        raise Exception(f"You must at least create one knapsack problem.")

    if knapsack_problem_size <= 0:
        raise Exception(f"You must have at least one item to choose from.")

    if item_min_weight <= 0 or item_max_weight <= 0:
        raise Exception(f"item min or max weight is less than zero.")

    if item_min_value <= 0 or item_max_value <= 0:
        raise Exception(f"item min or max value is less than zero.")

    if knapsack_capacity < item_min_weight:
        raise Exception(f"minimum item weight is bigger than the knapsack capacity.")

    is_valid = False
    problem_file_name = f"knapsack_{knapsack_problem_size}_capacity_{knapsack_capacity}"
    for index in range(1, number_of_knapsack_problems + 1):
        random_avg_weight = 0
        random_knapsack_weight_value_pair = []
        for _ in range(knapsack_problem_size):
            random_weight = random.randint(item_min_weight, item_max_weight)

            if not is_valid and random_weight <= knapsack_capacity:
                is_valid = True
            random_avg_weight += random_weight
            random_value = random.randint(item_min_value, item_max_value)
            random_knapsack_weight_value_pair.append(random_weight)
            random_knapsack_weight_value_pair.append(random_value)
        new_knapsack_weight_value_pair = " ".join("%s" % i for i in random_knapsack_weight_value_pair)

        if is_valid:
            problem_file = open(f"{problem_file_path}{problem_file_name}_{index}.dat", 'w')
            problem_file.write(f"{index} {knapsack_problem_size} {knapsack_capacity} {new_knapsack_weight_value_pair}\n")
            problem_file.close()
            print(f"Knapsack file successfully written to: {problem_file_path}")
        else:
            print(f"No item fits into knapsack. Knapsack is not solvable. No knapsack file was created")


if __name__ == "__main__":

    file_path = f"data/1_000/"

    create_knapsack_problems(number_of_knapsack_problems=3, knapsack_problem_size=10, knapsack_capacity=400,
                             item_min_weight=1, item_max_weight=10, item_min_value=1, item_max_value=800,
                             problem_file_path=file_path)




