class BTNode:
    """
    Class representing a B-Tree node.

    Attributes:
        children: A list of B-Tree nodes.
        elements: A list of keys for the node
        is_leaf: True if this is a leaf node, False otherwise.
    """

    def __init__(self, is_leaf: bool = False) -> None:
        """
        Constructor for B-Tree node.
        """
        self.children: list[BTNode] = []
        self.elements: list[str] = []
        self.is_leaf = is_leaf

    def search(self, search_elem: str) -> tuple[int, bool]:
        """
        Binary search function for B-Tree node.
        :param search_elem: Element to search for.
        :return: Index of element/location to traverse to, True if found, False otherwise.
        """
        # Initialize pointers
        left = 0
        right = len(self.elements) - 1
        child_index = 0
        is_found = False

        while True:
            # If left surpasses right then end loop
            if left > right:
                break

            # Set mid to the middle of left and right
            mid = (left + right) // 2

            # If the element at mid-position is less than search
            if self.elements[mid] < search_elem:
                child_index = mid + 1
                # Set left to be mid + 1, searching at right-side of array
                left = mid + 1

            # If element at mid-position is greater than search
            elif self.elements[mid] > search_elem:
                child_index = mid
                # Set right to mid - 1, searching at left-side of array
                right = mid - 1

            # If element is equal then break
            else:
                # Set found index to current mid-pointer
                child_index = mid
                is_found = True
                break

        return child_index, is_found

    def split_node(self, insert_loc: int, parent_node: 'BTNode') -> None:
        """
        Split B-Tree node into two B-Tree nodes.
        :param insert_loc: Location to insert element into parent B-Tree node.
        :param parent_node: Parent B-Tree node.
        :return: None
        """
        # Create new neighbouring node and split elements from middle
        neigh_node = BTNode(self.is_leaf)

        # Get median index and element
        median_ind = len(self.elements) // 2
        median_element = self.elements[median_ind]

        # Split elements and children in the middle to left and right
        left_elements = self.elements[:median_ind]

        left_children = self.children[:median_ind + 1]

        right_elements = self.elements[median_ind + 1:]

        right_children = self.children[median_ind + 1:]

        # Assign original node to left node
        self.elements = left_elements
        self.children = left_children

        # Assign new node to right node
        neigh_node.elements = right_elements
        neigh_node.children = right_children

        # Push it median element to the index where it traverses from
        parent_node.elements.insert(insert_loc, median_element)

        # Insert the right child node pointer to the parent children list on insert_loc + 1
        parent_node.children.insert(insert_loc + 1, neigh_node)

    def get_predecessor(self, left_index: int) -> str:
        """
        Get predecessor of B-Tree node.
        :param left_index: Index of element to traverse.
        :return: Predecessor element of B-Tree node.
        """
        # Set current node to the children at left index
        current_node = self.children[left_index]

        # Loop until reaches leaf
        while not current_node.is_leaf:
            # Set current node to the rightmost children of the node
            current_node = current_node.children[len(current_node.children) - 1]

        # Return the rightmost element in the leaf node
        return current_node.elements[len(current_node.elements) - 1]

    def get_successor(self, right_index: int) -> str:
        """
        Get successor of B-Tree node.
        :param right_index: Index of element to traverse.
        :return: Successor element of B-Tree node.
        """
        # Set current node to children at right index
        current_node = self.children[right_index]
        # Loop until reaches leaf
        while not current_node.is_leaf:
            # Set to first child of the node
            current_node = current_node.children[0]
        # Return the first element in the node
        return current_node.elements[0]

    def merge_children(self, elem_index: int) -> 'BTNode':
        """
        Merge B-Tree nodes into a B-Tree node.
        :param elem_index: Index of element to push down to merged B-Tree node.
        :return: The merged B-Tree node.
        """
        # Set middle element to put in the middle of merge
        middle_element = self.elements[elem_index]

        # Merge left, right with middle element on left node
        left_node = self.children[elem_index]
        right_node = self.children[elem_index + 1]

        # Merge elements
        left_node.elements += [middle_element] + right_node.elements
        # Merge right node children with left node children
        left_node.children += right_node.children

        # Remove element from node
        self.elements.pop(elem_index)
        # Remove pointer to right node, since we only want to keep left node
        self.children.pop(elem_index + 1)

        # Return merged node
        return left_node

    def rotate_from_left(self, elem_index: int) -> None:
        """
        Rotate B-Tree node from left to right.
        :param elem_index: Element to rotate down to the right B-Tree node.
        :return: None
        """
        # Get left sibling and child itself
        left_sibling = self.children[elem_index - 1]
        child_node = self.children[elem_index]

        # Add element to the start of the child node
        child_node.elements.insert(0, self.elements[elem_index - 1])

        # Remove the immediate pred from left sibling
        removed_elem = left_sibling.elements.pop()

        # Rotate removed element to parent
        self.elements[elem_index - 1] = removed_elem

        # Check if there's subtree to rotate from sibling
        if not left_sibling.is_leaf:
            # Insert the popped subtree from left sibling into the child node
            child_node.children.insert(0, left_sibling.children.pop())

    def rotate_from_right(self, elem_index: int) -> None:
        """
        Rotate B-Tree node from right to left.
        :param elem_index: Element to rotate down to the left B-Tree node.
        :return: None
        """
        # Get right sibling and child itself
        right_sibling = self.children[elem_index + 1]
        child_node = self.children[elem_index]

        # Add element to the end of child node
        child_node.elements.append(self.elements[elem_index])

        # Remove the immediate successor from right sibling
        removed_elem = right_sibling.elements.pop(0)

        # Rotate removed element to parent
        self.elements[elem_index] = removed_elem

        # Check if there's a subtree to rotate
        if not right_sibling.is_leaf:
            # If right sibling is not a leaf, append the subtree to the child node children
            child_node.children.append(right_sibling.children.pop(0))


class BTree:
    """
    Class representing a B-Tree.

    Attributes:
        root: Root of B-Tree.
        t: Determines the min and max elements and branches of the B-Tree.
        verbosity: Verbosity level.
    """

    def __init__(self, degree: int, verbosity: int = 0) -> None:
        """
        Constructor for B-Tree tree.
        :param degree: Degree of the B-Tree.
        :param verbosity: Verbosity level.
        """
        self.root = None
        self.t = degree
        self.verbosity = verbosity

    def traverse_to_leaf(self, node: BTNode, search_elem: str) -> tuple[None, int] | tuple[BTNode, int]:
        """
        Recursive traversal to the leaf while searching for element
        :param node: Node to search
        :param search_elem: Element to search for in the node
        :return: Leaf node where the element is found and the index where it is found.
        """
        # If node is the root and node elements is full
        if node == self.root and len(node.elements) == 2 * self.t - 1:
            # Create new node as the new root
            new_node = BTNode()
            self.root = new_node

            new_node.children.append(node)
            # Split node with new node as the root parent node
            node.split_node(0, new_node)
            node = new_node

        # Get next traversing index
        traverse_index, is_found = node.search(search_elem)

        # If the element already exists in the tree then return None
        if is_found:
            return None, -1

        # If the node reaches a leaf then return the node and the index to insert element
        if node.is_leaf:
            return node, traverse_index

        # Next node will be following the traverse index
        next_node = node.children[traverse_index]

        # If elements in next node is full
        if len(next_node.elements) == 2 * self.t - 1:
            # Split node with next child node with the current node as the parent
            next_node.split_node(traverse_index, node)
            # Recursively traverse from the same current node
            return self.traverse_to_leaf(node, search_elem)
        else:
            # Recursively traverse from the child node
            return self.traverse_to_leaf(next_node, search_elem)

    def insert(self, element: str) -> None:
        """
        Insert element into B-Tree node.
        :param element: Element to insert.
        :return: None
        """

        # If root is None, meaning the tree is empty
        if not self.root:
            # Create root node and add element to the new root node
            self.root = BTNode(True)
            self.root.elements.append(element)
        else:
            # Traverse to the leaf from root node to insert
            leaf_node, index = self.traverse_to_leaf(self.root, element)
            # If leaf node is None it means that the element is found in the tree
            if not leaf_node:
                if self.verbosity:
                    print("Element is already in the tree")
                return
            # Insert element into leaf node at index
            leaf_node.elements.insert(index, element)

    def traverse_and_find(self, node: BTNode, search_elem: str) -> tuple[BTNode, int] | tuple[None, int]:
        """
        Traverse B-Tree and find the index of element in B-Tree node. Used by deletion operation
        :param node: Node to search
        :param search_elem: Element to search for in the node
        :return: A node where the element is found and the index where it is found.
        """
        # Perform binary search to find element in node
        traverse_index, is_found = node.search(search_elem)
        # If element is found then return the node that the element was found in and the index
        if is_found:
            return node, traverse_index

        # If node reaches a leaf it means that element isn't found then return None
        if node.is_leaf:
            return None, -1

        # "Traverse" to check child node
        child_node = node.children[traverse_index]

        # Child node has exactly t - 1 elements
        if len(child_node.elements) == self.t - 1:
            # Case 3a-1, check if traversal is not the left most and check left immediate sibling, if they have at
            # least t elements
            if traverse_index != 0 and len(node.children[traverse_index - 1].elements) >= self.t:
                node.rotate_from_left(traverse_index)

            # Case 3a-2,
            # If traversal is not the right most and check right immediate sibling, if they have at least t elements
            elif traverse_index != len(node.elements) and len(node.children[traverse_index + 1].elements) >= self.t:
                node.rotate_from_right(traverse_index)

            # Case 3b
            # If immediate sibling only have exactly t - 1 elements
            else:
                # Merge with right sibling if traverse index not right most
                if traverse_index != len(node.elements):
                    merged_node = node.merge_children(traverse_index)
                # Merge with left sibling if traverse index is right most
                else:
                    merged_node = node.merge_children(traverse_index - 1)

                # If there are no more elements in the root then set root to the merged node
                if not self.root.elements:
                    self.root = merged_node

                # Continue traversing into the merged node
                return self.traverse_and_find(merged_node, search_elem)

        # Traverse into next node
        return self.traverse_and_find(node.children[traverse_index], search_elem)

    def delete(self, element: str) -> str | None:
        """
        Delete element from B-Tree
        :param element: Element to delete.
        :return: Element that was deleted, None if element was not found.
        """
        # Call the internal recursive delete function
        return self._delete(self.root, element)

    def _delete(self, start_node: BTNode, element: str) -> str | None:
        """
        Internal recursive function that performs deletion on B-Tree.
        :param start_node: Node to start traversing and deleting from.
        :param element: Element to delete.
        :return: Element that was deleted, None if element was not found.
        """

        # Traverse and find the node with element and the index where element is found
        found_node, found_index = self.traverse_and_find(start_node, element)
        # If node is not found then return None
        if not found_node:
            if self.verbosity:
                print("Element not found")
            return None

        # Case 1, if node is a leaf and element is >= t or node is the root, delete straight
        if found_node.is_leaf and (len(found_node.elements) >= self.t or found_node == self.root):
            removed_elem = found_node.elements.pop(found_index)
            # If node is the root and elements is empty then set root to None
            if found_node == self.root and not found_node.elements:
                self.root = None
            return removed_elem

        # Case 2a, if node is an internal node, check root node of left subtree
        left_node = found_node.children[found_index]
        # If subtree has at least t elements
        if len(left_node.elements) >= self.t:
            # Get predecessor of found node
            pred_elem = found_node.get_predecessor(found_index)
            # Replace element at the found location with predecessor element
            found_node.elements[found_index] = pred_elem

            # Recursively delete predecessor element from subtree
            return self._delete(left_node, pred_elem)

        # Case 2b, mirror of 2a, check root node of right subtree    
        right_node = found_node.children[found_index + 1]
        # If subtree has at least t elements
        if len(right_node.elements) >= self.t:
            # Get successor of found node
            succ_elem = found_node.get_successor(found_index + 1)
            # Replace element
            found_node.elements[found_index] = succ_elem

            return self._delete(right_node, succ_elem)

        # Case 2c, where both left and right has exactly t - 1 elements, merge to become 2t - 1
        merged_node = found_node.merge_children(found_index)

        # If root element is empty then replace root with the newly merged node
        if not self.root.elements:
            self.root = merged_node

        # Recursive delete from merged node
        return self._delete(merged_node, element)

    def get_tree_ordered_elems(self) -> list[str]:
        """
        Gets the ordered elements from the tree
        :return: A list of ordered elements.
        """
        in_order_elements = []
        # Traverse into the tree to populate the array
        self.traverse_ordered_elems(self.root, in_order_elements)

        return in_order_elements

    def traverse_ordered_elems(self, node: BTNode, elements: list[str], depth: str = "") -> None:
        """
        Traverse down the B-Tree to populate the ordered elements
        :param node: Node to traverse into
        :param elements: List of ordered elements
        :param depth: Depth of the tree used for printing
        :return: None
        """
        if not node:
            return

        # If verbosity level is > 0 then print the tree
        if self.verbosity:
            print(depth + " ".join(node.elements))

        # If node is a leaf then add to elements
        if node.is_leaf:
            elements += node.elements
            return

        # For each of the child in children traverse into the children
        for index, child in enumerate(node.children):
            # Recursively traverse into the child
            self.traverse_ordered_elems(child, elements, depth + "|- ")
            # Append the parent element of the subtree
            if index < len(node.elements):
                elements.append(node.elements[index])


if __name__ == "__main__":
    words = [
            "ant", "bat", "cat", "dog", "eel", "fox", "goat", "horse", "iguana", "jaguar",
            "koala", "lemur", "monkey", "newt", "owl", "penguin", "quail", "rabbit", "snake",
            "tiger", "umbrella", "vulture", "wolf", "xerus", "yak", "zebra", "alligator",
            "buffalo", "crocodile", "deer", "eagle", "falcon", "gorilla", "hawk", "ibis",
            "kangaroo", "lion", "moose", "narwhal", "octopus", "panda", "quokka", "raccoon",
            "salamander", "turtle", "unicorn", "viper", "walrus", "xerus", "yak", "zebra"
        ]

    tree = BTree(2, verbosity=1)

    for word in words:
        tree.insert(word)

    cmd_list =[
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


    for command in cmd_list:
        action, word = command.split()
        if action == "delete":
            tree.delete(word)
            tree.get_tree_ordered_elems()

        elif action == "insert":
            tree.insert(word)

    print(tree.get_tree_ordered_elems())
