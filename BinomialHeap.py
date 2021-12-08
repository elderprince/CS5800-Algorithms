import random
from Linked_List import LinkedList


def NodeLink(node_1, node_2):
    """
    Helper function to link two binomial nodes
    """
    if node_1.key <= node_2.key:
        node_1.sibling = node_2.sibling
        node_2.parent = node_1
        node_2.sibling = node_1.child
        node_1.child = node_2
        node_1.degree += 1
    else:
        node_1.parent = node_2
        node_1.sibling = node_2.child
        node_2.child = node_1
        node_2.degree += 1


class BinomialNode:
    def __init__(self, elem):
        """
        Initialize a binomial node
        """
        self.parent = None
        self.child = None
        self.sibling = None
        self.degree = 0
        self.key = elem


class BinomialHeap:
    def __init__(self):
        """
        Initialize an empty binomial heap
        """
        self.root = LinkedList()
        self.size = 0

    def minimum(self):
        """
        Find the node with minimum key
        """
        y = None
        x = self.root.head.data
        min_key = float("inf")
        while x:
            if x.key < min_key:
                min_key = x.key
                y = x
            x = x.sibling
        return y

    def __merge__(self, heap):
        """
        Merge another heap's root list
        """
        # Merged heap is empty
        if heap.size == 0:
            return self.root
        # Original heap is empty
        elif self.size == 0:
            return heap.root
        else:
            # Merge two root lists
            # Similar with the merge operation in merge sort
            merge_root = LinkedList()
            root_node_1 = self.root.head
            root_node_2 = heap.root.head
            while root_node_1 is not None or root_node_2 is not None:
                if root_node_1 is not None and root_node_2 is None:
                    merge_root.append(root_node_1.data)
                    # Update the sibling of the tail node in the root list
                    merge_root.find(root_tail).data.sibling = root_node_1.data
                    root_tail = root_node_1.data
                    root_node_1 = root_node_1.next
                elif root_node_1 is None and root_node_2 is not None:
                    merge_root.append(root_node_2.data)
                    # Update the sibling of the tail node in the root list
                    merge_root.find(root_tail).data.sibling = root_node_2.data
                    root_tail = root_node_2.data
                    root_node_2 = root_node_2.next
                else:
                    if root_node_1.data.degree <= root_node_2.data.degree:
                        merge_root.append(root_node_1.data)
                        # Add the 1st node into merged root list
                        if merge_root.size == 1:
                            root_tail = merge_root.head.data
                        else:
                            merge_root.find(root_tail).data.sibling = root_node_1.data
                            root_tail = root_node_1.data
                        root_node_1 = root_node_1.next
                    else:
                        merge_root.append(root_node_2.data)
                        # Add the 1st node into merged root list
                        if merge_root.size == 1:
                            root_tail = merge_root.head.data
                        else:
                            merge_root.find(root_tail).data.sibling = root_node_2.data
                            root_tail = root_node_2.data
                        root_node_2 = root_node_2.next
            return merge_root

    def __find_node___(self, key):
        """
        Find a binomial node according a given key
        Search priority: child > sibling > parent's sibling
        """
        compare_node = self.root.head.data
        while compare_node.key != key and compare_node is not None:
            if compare_node.child is not None:
                compare_node = compare_node.child
            elif compare_node.sibling is not None:
                compare_node = compare_node.sibling
            elif compare_node.parent.sibling is not None:
                compare_node = compare_node.parent.sibling
        if compare_node.key == key:
            return compare_node
        else:
            print('Key for decreasing is not valid')
            return None

    def union(self, heap):
        """
        Unite another heap into the current heap
        """
        # Initialize a new binomial heap
        union_heap = BinomialHeap()
        union_heap.root = self.__merge__(heap)
        union_heap.size = self.size + heap.size
        # Union result is an empty heap
        if union_heap.size == 0:
            return union_heap
        # At least one node is in the union result
        x_prev = None
        x = union_heap.root.head.data
        x_next = x.sibling
        # At least two nodes are in the union result
        while x_next is not None:
            # Two nodes with different degrees are in the union result
            if x.degree != x_next.degree and x_next.sibling is None:
                break
            # First two nodes with different degrees are in the union result
            elif x.degree != x_next.degree and x_next.sibling is not None:
                x_prev = x
                x = x_next
                x_next = x.sibling
            # Two nodes with same degree are in the union result
            elif x.degree == x_next.degree and x_next.sibling is None:
                if x.key <= x_next.key:
                    NodeLink(x, x_next)
                    union_heap.root.remove(x_next)
                else:
                    if x_prev is None:
                        union_heap.root.head = union_heap.root.head.next
                    else:
                        x_prev.sibling = x_next
                    NodeLink(x, x_next)
                    union_heap.root.remove(x)
                break
            # First two nodes with same degree are in the union result
            else:
                # The third node has the same degree
                if x_next.degree == x_next.sibling.degree:
                    x_prev = x
                    x = x_next
                # The third node has a different degree
                else:
                    # Keep the original heap's head or the previous node's sibling
                    if x.key <= x_next.key:
                        NodeLink(x, x_next)
                        union_heap.root.remove(x_next)
                    else:
                        # Change the original heap's head
                        if x_prev is None:
                            union_heap.root.head = union_heap.root.head.next
                            union_heap.root.head.prev = None
                            union_heap.root.size -= 1
                        # Change the previous node's sibling
                        else:
                            x_prev.sibling = x_next
                        NodeLink(x, x_next)
                        union_heap.root.remove(x)
                        x = x_next
                x_next = x.sibling
        # Update the original heap with the union result
        self.root = union_heap.root
        self.size = union_heap.size

    def insert(self, elem):
        """
        Insert a node with its key into the current heap
        """
        # Create a binomial heap only with the inserted node
        new_heap = BinomialHeap()
        node = BinomialNode(elem)
        new_heap.root.insert(node)
        new_heap.size += 1
        # Unify the heap with the inserted node
        self.union(new_heap)
        print('Insert ' + str(elem) + ' successfully')

    def extract_min(self):
        """
        Find and delete the node with minimum key from the current heap
        """
        min_node = self.minimum()
        child_node = min_node.child
        # Update minimum node's previous node's sibling
        if self.root.find(min_node) != self.root.head:
            self.root.find(min_node).prev.data.sibling = min_node.sibling
        # Remove the minimum node from root list
        self.root.remove(min_node)
        self.size -= 2 ** min_node.degree
        # Insert minimum node's children into a new heap
        children_heap = BinomialHeap()
        while child_node is not None:
            child_node.parent = None
            sibling = child_node.sibling
            if children_heap.root.head is None:
                children_heap_head_node = None
            else:
                children_heap_head_node = children_heap.root.head.data
            children_heap.root.insert(child_node)
            children_heap.root.head.data.sibling = children_heap_head_node
            children_heap.size += 2 ** child_node.degree
            child_node = sibling
        # Unify two heaps
        self.union(children_heap)
        return min_node

    def decrease_key(self, key, decreased_key):
        """
        Decrease a node's key to another given key
        """
        if decreased_key > key:
            print('New key is greater than current key')
        # Find the node with its key
        decrease_node = self.__find_node___(key)
        # Adjust the decreased node's location
        if decrease_node is not None:
            decrease_node.key = decreased_key
            y = decrease_node
            z = y.parent
            while z is not None and y.key < z.key:
                y_key = y.key
                y.key = z.key
                z.key = y_key
                y = z
                z = y.parent
        else:
            return

    def delete(self, key):
        """
        Delete a node with its key
        """
        delete_node = self.__find_node___(key)
        if delete_node is not None:
            self.decrease_key(key, float('-inf'))
            self.extract_min()
        else:
            return


if __name__ == '__main__':
    l = random.sample(range(100), 15)
    print(l)
    h = BinomialHeap()
    for i in l:
        print('----------')
        h.insert(i)
        print(h.size)
    print('----------')
    extracted_min = h.extract_min()
    print(extracted_min.key)
    print(h.size)
    print('----------')
    num = l[4]
    h.delete(num)
    print(h.size)
