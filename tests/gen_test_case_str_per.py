import tools
from q1.q1 import StringPermutation
from naive_string_permutation import get_results
import random

test_case_string = ("import unittest"
                    "\nimport subprocess"
                    "\nclass TestStrPermutation(unittest.TestCase):"
                    "\n\tdef run_script(self, alphabet_size, string_length):"
                    "\n\t\tresult = subprocess.run("
                    "\n\t\t\t['python', '../q1/q1.py', str(alphabet_size), str(string_length)],"
                    "\n\t\t\tcapture_output=True,"
                    "\n\t\t\ttext=True"
                    "\n\t\t)"
                    "\n\t\treturn result.stdout.strip()")

for i in range(5):
    for j in range(10):
        test_case_string += "\n\tdef test_" + str(i * 10 + j) + "(self):"
        greater_2, exactly_n, exactly_one, multi_of_n = get_results(i + 1, j + 1)

        test_case_string += (f"\n\t\toutput = self.run_script({i + 1}, {j + 1})"
                             f"\n\t\texpected_output = '{greater_2} {exactly_n} {exactly_one} {str(multi_of_n).lower()}'"
                             f"\n\t\tassert output == expected_output")

for i in range(500):
    test_case_string += "\n\tdef test_" + str(i + 50) + "(self):"

    A = random.randint(1, 26)
    N = random.randint(1, 10000)

    str_per = StringPermutation(A, N)
    greater_2, exactly_n, exactly_one, multi_of_n = str_per.get_cyclic_rotations()

    test_case_string += (f"\n\t\toutput = self.run_script({A}, {N})"
                         f"\n\t\texpected_output = '{greater_2} {exactly_n} {exactly_one} {str(multi_of_n).lower()}'"
                         f"\n\t\tassert output == expected_output")

tools.write_file("test_string_permutation.py", test_case_string)
