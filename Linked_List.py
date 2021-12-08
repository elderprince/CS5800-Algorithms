class Node:
    """
    Build up a node and assign its pointer to the next element
    """

    def __init__(self, data, key=None):
        self.data = data
        self.next = None
        self.prev = None
        self.down = None
        self.key = key


class LinkedList:
    """
    Create a linked list and assign its nodes
    """

    def __init__(self, nodes=None):
        self.head = None
        self.size = 0
        if nodes is not None:
            node = Node(data=nodes.pop(0))
            self.head = node
            self.size = 1
            for elem in nodes:
                node.next = Node(data=elem)
                prev = node
                node = node.next
                node.prev = prev
                self.size += 1

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(str(node.data))
            node = node.next
        nodes.append("None")
        return " -> ".join(nodes)

    def insert(self, data, key=None):
        node = Node(data, key)
        if self.head is None:
            self.head = node
        else:
            n_next = self.head
            node.next = n_next
            n_next.prev = node
            self.head = node
        self.size += 1

    def append(self, data, key=None):
        # 1. Create a new node
        # 2. Put in the data
        # 3. Set next as None
        node = Node(data, key)
        # 4. If the Linked List is empty, then make the
        #    new node as head
        if self.head is None:
            self.head = node
        else:
            # 5. Else traverse till the last node
            last = self.head
            while last.next:
                last = last.next
            # 6. Change the next of last node
            last.next = node
            node.prev = last
        self.size += 1

    def find(self, data):
        node = self.head
        while node.data != data and node.next is not None:
            node = node.next
        if node.data == data:
            return node
        else:
            return None

    def remove(self, data):
        if self.find(data) is not None:
            r_node = self.find(data)
            if r_node.prev is None and r_node.next is None:
                self.head = None
            if r_node.prev:
                r_node.prev.next = r_node.next
            if r_node.next:
                r_node.next.prev = r_node.prev
            self.size -= 1
        else:
            return


if __name__ == '__main__':
    ll = LinkedList([1, 3, 5, 9, 4, 10, 8, 20, 14, 34, 23])
    print(ll.find(9).data)
