from itertools import product


def get_results(A, N):
    alpha = [chr(ord('a') + i) for i in range(A)]

    all_combinations = [''.join(item) for item in product(alpha, repeat=N)]

    greater_than_2 = 0
    exactly_n = 0
    exactly_one = 0
    non_dist_dict = {}

    for combination in all_combinations:
        rotations = {combination[i:] + combination[:i]
                     for i in range(len(combination))}

        n_distinct = len(rotations)

        if n_distinct >= 2:
            greater_than_2 += 1

        if n_distinct == N:
            exactly_n += 1

        if n_distinct == 1:
            exactly_one += 1

    return greater_than_2, exactly_n, exactly_one, greater_than_2 % N == 0
