class BTNode:
    def __init__(self)->None:
        self.children = [] 
        self.elements = []
        self.is_leaf = False
    

class BTree:
    def __init__(self, degree: int)->None:
        self.root = BTNode()
        self.root.is_leaf = True
        self.t = degree
    
    def search(self, node: BTNode, search_elem) -> None:
        elem_arr = node.elements
        left = 0
        right = len(elem_arr) - 1
        search_index = -1
       
        while True:
            if left > right:
                break

            mid = (left + right) // 2

            if elem_arr[mid] < search_elem:
                left = mid + 1
            
            elif elem_arr[mid] > search_elem:
                right = mid - 1

            else:
                search_index = mid
                break

        
        if search_index != -1 or node.is_leaf:
            return node, search_index
        
        if elem_arr[mid] < search_elem:
            return self.search(node.children[mid+1], search_elem)
        
        else:
            return self.search(node.children[mid], search_elem)
                
        



    def insert(self, string):
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

    print(tree.search(tree.root, search_elem))
    