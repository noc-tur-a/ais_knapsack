# coding: utf-8


def dynamic_programming(problem_size, knapsack_capacity, knapsack, _):
    """
    Solve the knapsack problem by finding the most valuable
    subsequence of `knapsack` subject that weighs no more than
    `knapsack_capacity`.

    :param problem_size: the number of items to chose from (non-negative integer)
    :param knapsack_capacity: size of the knapsack (non-negative integer)
    :param knapsack: the weight-value pairs of the knapsack (list)

    :return:
        K[problem_size][knapsack_capacity]: amount of used capacity (non-negative integer)
        best_capacity: the achieved value (non-negative integer)
        selected_items[::-1]: list of selected (1) and not selected (0) items
        used capacity (non-negative integer), achieved value (non-negative integer),
    """

    K = [[0 for x in range(knapsack_capacity + 1)] for x in range(problem_size + 1)]

    # Build table K[][] in bottom up manner
    for i in range(problem_size + 1):
        for w in range(knapsack_capacity + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif knapsack[i - 1][0] <= w:
                K[i][w] = max(knapsack[i - 1][1] + K[i - 1][w - knapsack[i - 1][0]], K[i - 1][w])

            else:
                K[i][w] = K[i - 1][w]

    i = 0
    row = 1
    column = 0
    current_row = 0
    last_element = problem_size - 1
    best_capacity = 0
    selected_items = []

    while i < len(K) - 1:
        if K[problem_size - current_row][knapsack_capacity - column] > K[problem_size - row][knapsack_capacity - column]:
            current_row = row
            column += knapsack[last_element][0]
            best_capacity += knapsack[last_element][0]
            last_element -= 1
            row += 1
            selected_items.append(1)
        else:
            row += 1
            last_element -= 1
            selected_items.append(0)
        i += 1

    # used_capacity, best_value, best_combination
    print(f"best_capacity {best_capacity}")
    print(f"K[problem_size][knapsack_capacity] {K[problem_size][knapsack_capacity]}")
    return K[problem_size][knapsack_capacity], best_capacity, selected_items[::-1]


if __name__ == "__main__":
    print("Please call the main.py file.\nYou can't call dynamic_programming.py directly.")
