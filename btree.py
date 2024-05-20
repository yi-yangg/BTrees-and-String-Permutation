class BTNode:
    def __init__(self) -> None:
        self.children = []
        self.elements = []
        self.is_leaf = False


class BTree:
    def __init__(self, degree: int) -> None:
        self.root = BTNode()
        self.root.is_leaf = True
        self.t = degree

    def search(self, elements: list, search_elem) -> None:
        left = 0
        right = len(elements) - 1

        while True:
            if left > right:
                break

            mid = (left + right) // 2

            if elements[mid] < search_elem:
                left = mid + 1

            elif elements[mid] > search_elem:
                right = mid - 1

            else:
                break

        return mid

    def insert(self, element):
        pass


if __name__ == "__main__":
    tree = BTree(2)
    tree.root.elements = ["cascades"]
    left_node = BTNode()
    left_node.elements = ["Ascension", "abscissas"]
    left_node.is_leaf = True
    right_node = BTNode()
    right_node.elements = ["replica", "schmaltzy"]
    right_node.is_leaf = True
    tree.root.children = [left_node, right_node]

    tree.root.is_leaf = False

    search_elem = "replica"

    print(tree.search(tree.root.children[1].elements, search_elem))
