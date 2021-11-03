import argparse
import clonalg
import dynamic_programming

# Available algorithms (default is dynamic programming
DYNAMIC_PROGRAMMING = "dynamic"
CLONALG = "clonalg"


def parse_commandline():
    """
    Parses the user input.
    -f: input file containing the knapsack problem. Required
    -o: output file of the solution. Default if none given: data/solution/solution.dat
    -r: number of repetitions for the timeit function. Default if none given: 1 (no repetition)
    -m: chosen algorithm to solve the problem. Default if none given: dynamic programming

    :return: args: parsed user inputs
    """

    parser = argparse.ArgumentParser(description='Script solving the 0/1 knapsack problem')
    parser.add_argument('-f', required=True, type=str, dest="problem_file_path",
                        help='Path to knapsack problem file (*.dat)')
    parser.add_argument('-o', type=str, dest="solution_file_path", default="data/solution/solution.dat",
                        help='Path to file where solutions will be saved. Default value: data/solution/solution.dat')
    parser.add_argument('-r', type=int, dest="repeat", default=1,
                        help='Number of repetitions. Default value: 1')
    parser.add_argument("-m", default=DYNAMIC_PROGRAMMING, type=str, dest="method",
                        choices=[DYNAMIC_PROGRAMMING, CLONALG],
                        help="Solving method. Default value: dynamic programming algorithm")

    args = parser.parse_args()

    if args.method == DYNAMIC_PROGRAMMING:
        args.method = dynamic_programming.dynamic_programming
    elif args.method == CLONALG:
        args.method = clonalg.clonalg
    else:
        raise Exception("Unknown solving algorithm")

    return args


if __name__ == "__main__":
    print("Please call the main.py file.\nYou can't call ParseCommandLine.py directly.")
