import sys

sys.set_int_max_str_digits(10 ** 7)


class StringPermutation:
    """
    This class generates all possible strings of length N from the set of alphabets
    A, where A is the set of characters a-z, and it calculates the number of distinct
    cyclic rotations that are possible for the string.

    Attributes:
        alpha_num: Number of alphabets
        string_len: Length of string
        factors: A list of factors that affects the distinct cyclic rotations
    """

    def __init__(self, alpha_num: int, string_len: int) -> None:
        self.alpha_num = alpha_num
        self.string_len = string_len
        self.factors = self.setup_factor()

    def setup_factor(self) -> list[int]:
        """
        Sets up the factor list, since N can only be divisible by number <= N/2,
        thus the size of the factors list should only be N/2 + 1 size, and we
        populate the first factor by setting to the alphabet number itself, this means
        that when the string is divided into N slots, the maximum possibility will only
        be A^1

        :return: A list of the factors that are unpopulated except for the first element
        """
        # N can only be divisible by number <= N/2
        N_divisible = self.string_len // 2

        # Create an array for factors
        factors = [-1] * (N_divisible + 1)

        # Populate first factor A^1
        factors[0] = self.alpha_num

        return factors

    def get_non_n_rotations(self, n):
        """
        For a given number n, find the factors that causes the number of distinct cyclic
        rotations to be < N. The case where number of distinct cyclic rotations is < N is
        when the string of length N is divided into subsections, where each section has the
        same sequence of characters.
        E.g. Given A = 3, N = 6, _ _ _ _ _ _ there are 6 potential slots for string combination
        and to build a string that has < N distinct rotations is to divide into equal sections,
        lets say divide into 2 sections _ _ _ and _ _ _ both of these will have the same sequence
        of char (e.g. abc abc). This will yield (N / number of sections) distinct rotations, in this
        case 6 / 2 = 3 (abcabc, bcabca, cabcab). Thus, to find the number of distinct cyclic rotations
        we just have to find the factors of N

        For each of the factors, we find the max possible combination for one section e.g. Divided into
        2 sections _ _ _ , _ _ _ we omit the latter _ _ _. The first _ _ _ will give us the max combination
        of A A A = A^3, we can see that in every factor we will have A ^ (N / factor) maximum number of
        possible combinations

        However, when the factor is not a prime, where it also contains other factors we have to take
        into account of the combinations of the other factors (e.g. A = 2, N = 12, let's say we're looking
        at splitting into 2 sections _ _ _ _ _ _ and _ _ _ _ _ _, the maximum number of possible combination
        is A ^ (N / 2) = 2 ^ 6. 6 has 3 and 2 as a factor, thus we need to minus off the maximum number of
        possible combination that the string has when divided into N/2 (6) and N/3 (4) section yield since
        they will be overlapping (e.g. ababab ababab, ab ab ab ab ab ab, abab abab abab).

        Thus, in order to get the maximum possible combination of the factor, we just use A ^ factor -
        maximum possible combination of the factor of factor, by using recursion which obtains the previously
        calculated value
        :param n: The current number to look for factors

        :return: The number of distinct cyclic rotation that is < N
        """
        non_n_rotations = 0

        for i in range(0, n // 2):
            if n % (i + 1) == 0:
                if self.factors[i] == -1:
                    self.factors[i] = self.alpha_num ** (i + 1) - \
                                      (self.get_non_n_rotations(i + 1))

                non_n_rotations += self.factors[i]

        return non_n_rotations

    def get_cyclic_rotations(self) -> tuple[int, int, int, bool]:
        """
        The result will yield 4 items.

        1. Number of strings with >= 2 distinct cyclic rotations
        How to obtain:
        - Get the number of possible string that is length N with all combinations of set alphabets A
           by using A^N. For example, when A = 3, N = 4, There are _ _ _ _ 4 empty slots and each slot
           can have a max of A combinations, therefore, A * A * A * A thus giving A^N
        - The number of strings with >= 2 distinct cyclic rotations is just number of all possible string
           combination - number of strings with exactly 1 distinct cyclic rotation
        - The number of strings with exactly 1 distinct cyclic rotation is just A^1, since we only take into
           account of one slot in the string and the other slots will follow the character in that one slot

        2. Number of strings with exactly N distinct cyclic rotations
        How to obtain:
        - Get the number of strings with < N distinct cyclic rotations, since number of cyclic rotations cannot
          exceed > N cyclic rotations. (See get_non_n_rotations function docs)
        - Then use the number of all possible string - the number of strings with < N distinct cyclic rotations

        3. Number of strings with exactly 1 distinct cyclic rotations
        How to obtain:
        - Length of alphabet set A (See 1. 3rd point)

        4. Boolean that indicates if number of strings >= 2 distinct cyclic rotations is an integer multiple of N
        How to obtain:
        - Use the number of strings with >= 2 distinct % (mod) with N and check if its == 0

        :return: 4 items described above
        """

        # Get number of strings with exactly 1 distinct cyclic rotations
        exactly_one = self.alpha_num

        # Get all possible string combination
        possible_combination = self.alpha_num ** self.string_len

        # Get number of strings with >= 2 distinct cyclic rotations
        greater_than_2 = possible_combination - exactly_one
        # Get number of strings with < N distinct cyclic rotations
        non_n_rotations = self.get_non_n_rotations(
            self.string_len)
        # Get == N distinct cyclic rotations by all possible combination - non n rotations
        n_rotations = possible_combination - non_n_rotations

        is_multiple_of_n = greater_than_2 % self.string_len == 0

        return greater_than_2, n_rotations, exactly_one, is_multiple_of_n


if __name__ == "__main__":
    _, alpha_num_str, string_len_str = sys.argv

    str_per = StringPermutation(int(alpha_num_str), int(string_len_str))
    greater_2, exactly_n, exactly_1, multi_of_n = str_per.get_cyclic_rotations()

    print(greater_2, exactly_n, exactly_1, str(multi_of_n).lower())
