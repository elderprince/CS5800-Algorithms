import sys
from nltk.tokenize import word_tokenize


class Node:
    def __init__(self, data):
        """
        Initialize a node in a RB tree
        """
        self.data = data    # Value in the node
        self.parent = None  # Pointer to the parent
        self.left = None    # Pointer to left child
        self.right = None   # Pointer to right child
        self.color = 'r'    # 'r': Red; 'b': Black


class RedBlackTree:
    def __init__(self, node_keys=None):
        """
        Initialize an RB tree
        """
        self.TNULL = Node(None)
        self.TNULL.color = 'b'
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL
        self.height = None
        if node_keys is not None:
            for i in node_keys:
                self.insert(i)
                self.pretty_print()
                print('--------------------------------')

    def __height_finder(self, k):
        """
        Get tree height
        """
        height = 0
        while k != self.root:
            k = k.parent
            height += 1
        if height > self.height:
            self.height = height

    def __fix_insert(self, k):
        """
        Keep fixing the tree until Parent's color turns black
        """
        while k.parent.color == 'r':
            # Parent is the right child of Grandparent
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                # Parent is red and Uncle is red
                if u.color == 'r':
                    # Case 1
                    # Change P, U and G's colors
                    u.color = 'b'
                    k.parent.color = 'b'
                    k.parent.parent.color = 'r'
                    # Regard Grandparent as a new insertion
                    # Check if its parent's color is aginst the rule
                    k = k.parent.parent
                # Parent is red and Uncle is black
                else:
                    # Insertion is the left child
                    if k == k.parent.left:
                        # Case 2.2
                        # Right rotate around Parent
                        # Regard Parent as a new insertion
                        # New Insertion is a right child
                        k = k.parent
                        self.right_rotate(k)
                    # Case 2.1
                    # Insertion is the right child
                    # Left rotate around Grandparent
                    # Change Parent and Grandparent's colors
                    k.parent.color = 'b'
                    k.parent.parent.color = 'r'
                    self.left_rotate(k.parent.parent)

            # Parent is the left child of Grandparent
            # Mirror cases of the above
            else:
                u = k.parent.parent.right

                # Parent is red and Uncle is red
                if u.color == 'r':
                    # Case 1
                    # Change P, U and G's colors
                    u.color = 'b'
                    k.parent.color = 'b'
                    k.parent.parent.color = 'r'
                    # Regard Grandparent as a new insertion
                    # Check if its parent's color is against the rule
                    k = k.parent.parent
                # Parent is red and Uncle is black
                else:
                    # Insertion is the right child
                    if k == k.parent.right:
                        # Left rotate around Parent
                        # Regard Parent as a new insertion
                        # New Insertion is a left child
                        k = k.parent
                        self.left_rotate(k)
                    # Insertion is the left child
                    # Right rotate around Grandparent
                    # Change Parent and Grandparent's colors
                    k.parent.color = 'b'
                    k.parent.parent.color = 'r'
                    self.right_rotate(k.parent.parent)
            # Insertion is the tree root
            if k == self.root:
                break
        # Make sure tree root's color is black
        self.root.color = 'b'

    def __search_tree_helper(self, node, key):
        """
        Find nodes with key and the comparison node
        """
        if node == self.TNULL:
            print('Key Not Found')
            return
        else:
            if key == node.data:
                return node
            elif key < node.data:
                return self.__search_tree_helper(node.left, key)
            else:
                return self.__search_tree_helper(node.right, key)

    def __print_helper(self, node, indent, next_branch):
        """
        Print the tree structure on the screen

        Helper function from website (Algorithm Tutor)
        """
        if node != self.TNULL:
            sys.stdout.write(indent)
            if next_branch:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            s_color = "RED" if node.color == 'r' else "BLACK"
            print(str(node.data) + "(" + s_color + ")")
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)

    def insert(self, key):
        """
        Insert a node into a tree like a BST
        AND fix the tree according RB tree rules
        """
        # Ordinary Binary Search Insertion
        node = Node(key)
        node.parent = None
        node.data = key
        node.left = self.TNULL
        node.right = self.TNULL
        # Inserted node must be red
        node.color = 'r'

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        # Assign insertion's parent
        node.parent = y
        # Insertion is the tree root
        # Tree root must be black
        if y is None:
            node.color = 'b'
            self.root = node
            self.height = 0
            print('Insert {}'.format(key))
            print('Tree height {}'.format(self.height))
            return
        # Insertion is a left child
        elif node.data < y.data:
            y.left = node
        # Insertion is a right child
        else:
            y.right = node

        # Fix the tree according to RB tree rules
        self.__fix_insert(node)
        self.__height_finder(node)
        print('Insert {}'.format(key))
        print('Tree height {}'.format(self.height))

    def search(self, key):
        """
        Search the tree for the key
        AND return the corresponding node
        """
        return self.__search_tree_helper(self.root, key)

    def minimum(self, node=None):
        """
        Find the node with the minimum key
        """
        if node is None:
            node = self.root
        while node.left != self.TNULL:
            node = node.left
        return node

    def maximum(self, node=None):
        """
        Find the node with the minimum key
        """
        if node is None:
            node = self.root
        while node.right != self.TNULL:
            node = node.right
        return node

    def successor(self, x):
        """
        Find the successor of a given node
        """
        # If the right subtree is not None,
        # the successor is the leftmost node in the
        # right subtree
        if x.right != self.TNULL:
            return self.minimum(x.right)

        # The lowest ancestor of x whose left
        # child is x or also an ancestor of x
        else:
            y = x.parent
            while y != self.TNULL and x == y.right:
                x = y
                y = y.parent
            return y

    def predecessor(self, x):
        """
        Find the predecessor of a given node
        """
        # If the left subtree is not None,
        # the predecessor is the rightmost node
        # in the left subtree
        if x.left != self.TNULL:
            return self.maximum(x.left)

        # The highest ancestor of x whose right
        # child is x or also an ancestor of x
        else:
            y = x.parent
            while y != self.TNULL and x == y.left:
                x = y
                y = y.parent
            return y

    def left_rotate(self, x):
        """
        Rotate left at node x
        """
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        """
        Rotate left at node x
        """
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def sort_asc(self):
        """
        Sort tree in ascending order
        """
        sort_asc = []
        min_node = self.minimum()
        sort_asc.append(min_node.data)
        max_node = self.maximum()
        while min_node != max_node:
            min_node = self.successor(min_node)
            sort_asc.append(min_node.data)
        return sort_asc

    def sort_desc(self):
        """
        Sort tree in ascending order
        """
        sort_desc = []
        max_node = self.maximum()
        sort_desc.append(max_node.data)
        min_node = self.minimum()
        while max_node != min_node:
            max_node = self.predecessor(max_node)
            sort_desc.append(max_node.data)
        return sort_desc

    def pretty_print(self):
        """
        Print tree structure
        """
        self.__print_helper(self.root, "", True)


def read_doc(file_path):
    """
    Read a file
    """
    f = open(file_path, "r")
    content = f.read()
    f.close()
    return content


def transform_to_list(content):
    """
    Transform the content into the list we need
    """
    tokens = word_tokenize(content)
    nums = []
    for i in tokens:
        if i.isdigit():
            nums.append(int(i))
    return nums


def array_input():
    """
    Ask the user to input valid file
    """
    num_list = []
    while not num_list:
        print('Current RB Tree element list is empty.')
        file = input("Please input a valid file containing arrays for RB Tree: ")
        content = read_doc(file)
        num_list = transform_to_list(content)
    print('Elements input successfully.')
    return num_list


def main():
    elems = array_input()
    print(elems)

    rb = RedBlackTree(elems)
    print('RB Tree initialized successfully')
    print('Tree height is ' + str(rb.height))
    print('--------------------------------')

    operation = ""
    valid = ['desc', 'asc', 'search', 'min', 'max', 'suc', 'pre', 'insert', 'print', 'esc']
    instruction = """
        Descending sorting (desc)
        Ascending sorting (asc)
        Search an element (search)
        Find the min value (min)
        Find the max value (max)
        Find an element's successor (suc)
        Find an element's predecessor (pre)
        Insert an element (insert)
        Print the RB tree (print)
        Exit (esc)

        Please input a valid operation according to the above instruction: 
        """

    while operation != 'esc':
        if operation == "" or operation not in valid:
            operation = input(instruction)
        elif operation == 'desc':
            print(rb.sort_desc())
            print('Tree height is ' + str(rb.height))
            operation = input('Please input a valid operation: ')
        elif operation == 'asc':
            print(rb.sort_asc())
            print('Tree height is ' + str(rb.height))
            operation = input('Please input a valid operation: ')
        elif operation == 'search':
            key = input('Please input the key you want to search: ')
            node = rb.search(int(key))
            if node is not None:
                print(str(node.data) + ': ' + node.color)
            print('Tree height is ' + str(rb.height))
            operation = input('Please input a valid operation: ')
        elif operation == 'min':
            print('Min value is ' + str(rb.minimum().data))
            print('Tree height is ' + str(rb.height))
            operation = input('Please input a valid operation: ')
        elif operation == 'max':
            print('Max value is ' + str(rb.maximum().data))
            print('Tree height is ' + str(rb.height))
            operation = input('Please input a valid operation: ')
        elif operation == 'suc':
            key = input('Please input whose successor you want to search: ')
            node = rb.search(int(key))
            if node is not None:
                suc = rb.successor(node)
                if suc is None:
                    print('Successor of ' + str(key) + ' is ' + str(suc))
                else:
                    print('Successor of ' + str(key) + ' is ' + str(suc.data))
            print('Tree height is ' + str(rb.height))
            operation = input('Please input a valid operation: ')
        elif operation == 'pre':
            key = input('Please input whose predecessor you want to search: ')
            node = rb.search(int(key))
            if node is not None:
                pre = rb.predecessor(node)
                print('Predecessor of ' + str(key) + ' is ' + str(pre.data))
            print('Tree height is ' + str(rb.height))
            operation = input('Please input a valid operation: ')
        elif operation == 'insert':
            key = input('Please input the key you want to insert: ')
            rb.insert(int(key))
            operation = input('Please input a valid operation: ')
        elif operation == 'print':
            rb.pretty_print()
            operation = input('Please input a valid operation: ')
    return


if __name__ == '__main__':
    main()
