import random
from random_word import RandomWords
import threading
import tools

def generate_test_case(test_index):
    test_case_string = ""
    test_case_string += ("\n\tdef test_" + str(test_index) + "(self):")

    r = RandomWords()
    word_list_len = random.randint(10, 100)
    word_list = []
    for _ in range(word_list_len):
        word = r.get_random_word()
        if word not in word_list:
            word_list.append(r.get_random_word())

    expected_output = word_list.copy()
    command_list_len = random.randint(1, len(word_list))
    command_list = []
    for _ in range(command_list_len):
        is_insert = random.choice([True, False])
        if is_insert:
            word = r.get_random_word()
            if word not in expected_output:
                command_list.append(f"insert {word}")
                expected_output.append(word)
        else:
            word_exist = random.choices([True, False], weights=[90, 10], k=1)[0]
            if word_exist:
                word = random.choice(expected_output)
                command_list.append(f"delete {word}")
            else:
                word = r.get_random_word()
                command_list.append(f"delete {word}")
            try:
                expected_output.remove(word)
            except ValueError:
                pass

    expected_output.sort()
    degree = random.randint(2, word_list_len)
    test_case_string += (f"\n\t\twords = {word_list}"
                         f"\n\t\tcommands = {command_list}"
                         f"\n\t\tdegree = {degree}"
                         f"\n\t\texpected_output = {expected_output}"
                         f"\n\t\tactual_output = self.initialize_and_get(degree, words, commands)"
                         f"\n\t\tassert actual_output == expected_output")
    print(f"thread {test_index} finished")
    return test_case_string

# Main test case string with import and class definition
main_test_case_string = ("import unittest"
                         "\nfrom q2.q2 import BTree"
                         "\nclass TestBTree(unittest.TestCase):"
                         "\n\tdef initialize_and_get(self, degree, words, commands):"
                         "\n\t\tbt = BTree(degree)"
                         "\n\t\tfor word in words:"
                         "\n\t\t\tbt.insert(word)"
                         "\n\t\tfor command in commands:"
                         "\n\t\t\taction, word = command.split()"
                         "\n\t\t\tif action == \"delete\":"
                         "\n\t\t\t\tbt.delete(word)"
                         "\n\t\t\telif action == \"insert\":"
                         "\n\t\t\t\tbt.insert(word)"
                         "\n\t\treturn bt.get_tree_ordered_elems()")

# Number of test cases to generate
num_test_cases = 100

# Create a list to hold all the threads
threads = []

# Create a list to collect the test case strings
test_case_strings = [""] * num_test_cases

# Function to run in each thread
def thread_function(index):
    test_case_strings[index] = generate_test_case(index)

# Start threads
for i in range(num_test_cases):
    thread = threading.Thread(target=thread_function, args=(i,))
    threads.append(thread)
    thread.start()
    print(f"thread {i} starting")

# Wait for all threads to complete
for thread in threads:
    thread.join()


# Combine all the generated test case strings
for test_case_string in test_case_strings:
    main_test_case_string += test_case_string

# Write the combined test cases to a file
tools.write_file("test_btree.py", main_test_case_string)
