import random
import unittest
from btree import BTree


def setUp(bt, words, commands):
    for word in words:
        bt.insert(word)

    for command in commands:
        action, word = command.split()
        if action == "delete":
            bt.delete(word)

        elif action == "insert":
            bt.insert(word)
class TestBTree(unittest.TestCase):
    def test_1(self):
        bt = BTree(2)
        words = [
            "apple",
            "banana",
            "cherry",
            "date",
            "fig",
            "grape",
            "kiwi",
            "lemon",
            "mango",
            "nectarine"
        ]
        cmd_list = [
            "delete banana",
            "insert orange",
            "delete fig",
            "insert peach",
            "delete kiwi"
        ]
        expected_output = ["apple", "cherry", "date", "grape", "lemon", "mango", "nectarine", "orange", "peach"]
        expected_output.sort()
        setUp(bt, words, cmd_list)

        assert bt.get_tree_ordered_elems() == expected_output

    def test_2(self):
        bt = BTree(3)
        words = [
            "alpha",
            "bravo",
            "charlie",
            "delta",
            "echo",
            "foxtrot",
            "golf",
            "hotel",
            "india",
            "juliet"
        ]
        cmd_list = [
            "delete charlie",
            "insert kilo",
            "delete echo",
            "insert lima",
            "delete hotel"
        ]
        expected_output = ["alpha", "bravo", "delta", "foxtrot", "golf", "india", "juliet", "kilo", "lima"]
        expected_output.sort()
        setUp(bt, words, cmd_list)

        assert bt.get_tree_ordered_elems() == expected_output

    def test_3(self):
        bt = BTree(4)

        words = [
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "ten"
        ]
        cmd_list = [
            "delete two",
            "insert eleven",
            "delete five",
            "insert twelve",
            "delete seven"
        ]
        expected_output = ["eight", "eleven", "four", "nine", "one", "six", "ten", "three", "twelve"]
        expected_output.sort()
        setUp(bt, words, cmd_list)
        assert bt.get_tree_ordered_elems() == expected_output

    def test_4(self):
        bt = BTree(5)
        words = [
            "x-ray",
            "yankee",
            "zulu",
            "alpha",
            "bravo",
            "charlie",
            "delta",
            "echo",
            "foxtrot",
            "golf"
        ]
        cmd_list = [
            "delete zulu",
            "insert hotel",
            "delete yankee",
            "insert india",
            "delete x-ray"
        ]
        expected_output = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel", "india"]
        expected_output.sort()
        setUp(bt, words, cmd_list)
        assert bt.get_tree_ordered_elems() == expected_output

    def test_5(self):
        bt = BTree(6)
        words = [
            "dog",
            "cat",
            "bird",
            "fish",
            "elephant",
            "ant",
            "bee",
            "cow",
            "deer",
            "frog"
        ]
        cmd_list = [
            "delete fish",
            "insert goat",
            "delete bee",
            "insert horse",
            "delete frog"
        ]
        expected_output = ["ant", "bird", "cat", "cow", "deer", "dog", "elephant", "goat", "horse"]
        expected_output.sort()
        setUp(bt, words, cmd_list)
        assert bt.get_tree_ordered_elems() == expected_output

    def test_6(self):
        bt = BTree(7)
        words = [
            "ant", "bat", "cat", "dog", "eel", "fox", "goat", "horse", "iguana", "jaguar",
            "koala", "lemur", "monkey", "newt", "owl", "penguin", "quail", "rabbit", "snake",
            "tiger", "umbrella", "vulture", "wolf", "xerus", "yak", "zebra"
        ]
        commands = [
            "delete cat",
            "insert alligator",
            "delete dog",
            "insert buffalo",
            "delete eel",
            "insert crocodile",
            "delete fox",
            "insert deer",
            "delete goat",
            "insert eagle",
            "delete horse",
            "insert falcon",
            "delete jaguar",
            "insert gorilla",
            "delete koala",
            "insert hawk",
            "delete lemur",
            "insert ibis",
            "delete monkey",
            "insert jaguar",
            "delete newt",
            "insert kangaroo",
            "delete owl",
            "insert lion",
            "delete penguin",
            "insert moose",
            "delete quail",
            "insert narwhal",
            "delete rabbit",
            "insert octopus",
            "delete snake",
            "insert panda",
            "delete tiger",
            "insert quokka",
            "delete umbrella",
            "insert raccoon",
            "delete vulture",
            "insert salamander",
            "delete wolf",
            "insert turtle",
            "delete xerus",
            "insert unicorn",
            "delete yak",
            "insert viper",
            "delete zebra",
            "insert walrus"
        ]
        expected_output = [
            "alligator", "ant", "bat", "buffalo", "crocodile", "deer", "eagle", "falcon", "gorilla",
            "hawk", "ibis", "iguana", "jaguar", "kangaroo", "lion", "moose", "narwhal", "octopus",
            "panda", "quokka", "raccoon", "salamander", "turtle", "unicorn", "viper", "walrus"
        ]
        expected_output.sort()
        setUp(bt, words, commands)
        assert bt.get_tree_ordered_elems() == expected_output

    def test_7(self):
        bt = BTree(2)
        initial_words = [
            "ant", "bat", "cat", "dog", "eel", "fox", "goat", "horse", "iguana", "jaguar",
            "koala", "lemur", "monkey", "newt", "owl", "penguin", "quail", "rabbit", "snake",
            "tiger", "umbrella", "vulture", "wolf", "xerus", "yak", "zebra", "alligator",
            "buffalo", "crocodile", "deer", "eagle", "falcon", "gorilla", "hawk", "ibis",
            "kangaroo", "lion", "moose", "narwhal", "octopus", "panda", "quokka", "raccoon",
            "salamander", "turtle", "unicorn", "viper", "walrus", "xerus", "yak", "zebra"
        ]
        commands = [
            "delete cat",
            "insert alpaca",
            "delete dog",
            "insert bison",
            "delete eel",
            "insert camel",
            "delete fox",
            "insert dingo",
            "delete goat",
            "insert emu",
            "delete horse",
            "insert ferret",
            "delete jaguar",
            "insert gazelle",
            "delete koala",
            "insert hamster",
            "delete lemur",
            "insert iguana",
            "delete monkey",
            "insert jaguarundi",
            "delete newt",
            "insert koala",
            "delete owl",
            "insert llama",
            "delete penguin",
            "insert meerkat",
            "delete quail",
            "insert nyala",
            "delete rabbit",
            "insert oryx",
            "delete snake",
            "insert platypus",
            "delete tiger",
            "insert quetzal",
            "delete umbrella",
            "insert rhino",
            "delete vulture",
            "insert sloth",
            "delete wolf",
            "insert tapir",
            "delete xerus",
            "insert uakari",
            "delete yak",
            "insert vicuna",
            "delete zebra",
            "insert warthog",
            "delete alligator",
            "insert xenomorph",
            "delete buffalo",
            "insert yak",
            "delete crocodile",
            "insert zebra"
        ]
        expected_output = [
            "alpaca", "ant", "bat", "bison", "camel", "deer", "dingo", "emu", "eagle", "falcon",
            "ferret", "gazelle", "gorilla", "hawk", "hamster", "ibis", "iguana", "jaguarundi", "kangaroo",
            "koala", "llama", "lion", "meerkat", "moose", "narwhal", "nyala", "octopus", "oryx", "panda",
            "platypus", "quokka", "quetzal", "raccoon", "rhino", "salamander", "sloth", "tapir", "turtle",
            "uakari", "unicorn", "vicuna", "viper", "warthog", "walrus", "xenomorph", "yak", "zebra"
        ]

        expected_output.sort()

        setUp(bt, initial_words, commands)

        assert bt.get_tree_ordered_elems() == expected_output

    def test_8(self):
        bt = BTree(3)
        initial_words = [
            "ant", "bat", "cat", "dog", "eel", "fox", "goat", "horse", "iguana", "jaguar",
            "koala", "lemur", "monkey", "newt", "owl", "penguin", "quail", "rabbit", "snake",
            "tiger", "umbrella", "vulture", "wolf", "xerus", "yak", "zebra"
        ]

        commands = [
            "delete ant",
            "delete bat",
            "delete cat",
            "delete dog",
            "delete eel",
            "delete fox",
            "delete goat",
            "delete horse",
            "delete iguana",
            "delete jaguar",
            "delete koala",
            "delete lemur",
            "delete monkey",
            "delete newt",
            "delete owl",
            "delete penguin",
            "delete quail",
            "delete rabbit",
            "delete snake",
            "delete tiger",
            "delete umbrella",
            "delete vulture",
            "delete wolf",
            "delete xerus",
            "delete yak",
            "delete zebra"
        ]

        random.shuffle(commands)

        expected_output = []

        setUp(bt, initial_words, commands)

        assert bt.get_tree_ordered_elems() == expected_output

