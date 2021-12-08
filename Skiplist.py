import random
from Linked_List import Node
from Linked_List import LinkedList


class SkipNode:
    def __init__(self, height=1, data=None):
        self.data = data
        self.next = None
        self.prev = None
        self.down = None
        self.height = height


class SkipList:
    def __init__(self, nodes=None):
        self.head = SkipNode(data=float("-inf"))
        self.NIL = SkipNode(data=float("inf"))
        self.head.next = self.NIL
        self.NIL.prev = self.head
        self.level = []
        if nodes is not None:
            for elem in nodes:
                self.insert(elem)

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def __repr__(self):
        node = self.head
        nodes = []
        heights = []
        while node is not None:
            nodes.append(str(node.data))
            heights.append(str(node.height))
            node = node.next
        return " -> ".join(nodes)

    def __random_height__(self):
        height = 1
        k = random.randint(0, 1)
        while k == 1:
            height += 1
            k = random.randint(0, 1)
        return height

    def __level_insert__(self, elem, level_list):
        for i in level_list:
            if i.data < elem < i.next.data:
                node = Node(elem)
                n_next = i.next
                n_next.prev = node
                node.next = n_next
                node.prev = i
                i.next = node

    def search(self, elem):
        if self.head.height == 1:
            compare_node = self.head
        else:
            compare_node = self.level[self.head.height-2].find(self.head.data)
        while elem != compare_node.data:
            if elem > compare_node.data:
                if compare_node.next.data != float("inf"):
                    compare_node = compare_node.next
                else:
                    if compare_node.down is not None:
                        compare_node = compare_node.down
                    else:
                        print('Skipnode ' + str(elem) + ' not found')
                        return None
            else:
                compare_node = compare_node.prev
                if compare_node.down is None:
                    print('Skipnode ' + str(elem) + ' not found')
                    return None
                else:
                    compare_node = compare_node.down
        while compare_node.down:
            compare_node = compare_node.down
        print('Skipnode ' + str(elem) + ' found')
        return compare_node

    def insert(self, elem):
        if self.search(elem) is None:
            node = SkipNode(self.__random_height__(), elem)
            head_node = self.head
            while head_node.next.data < elem:
                head_node = head_node.next
            node.next = head_node.next
            head_node.next.prev = node
            head_node.next = node
            node.prev = head_node
            for i in range(1, node.height):
                if i <= len(self.level):
                    self.__level_insert__(elem, self.level[i-1])
                else:
                    self.level.append(LinkedList([self.head.data, elem, self.NIL.data]))
                    head = self.level[i - 1].find(self.head.data)
                    tail = self.level[i - 1].find(self.NIL.data)
                    if i == 1:
                        head.down = self.head
                        tail.down = self.NIL
                    else:
                        head_down = self.level[i - 2].find(self.head.data)
                        head.down = head_down
                        tail_down = self.level[i - 2].find(self.NIL.data)
                        tail.down = tail_down
                    self.head.height += 1
                    self.NIL.height += 1
                level_node = self.level[i - 1].find(elem)
                if i == 1:
                    level_node.down = node
                else:
                    down_node = self.level[i - 2].find(elem)
                    level_node.down = down_node
            print('Insert ' + str(elem) + ' successfully')
        else:
            print('No element inserted')

    def remove(self, elem):
        remove_node = self.search(elem)
        if remove_node is not None:
            r_node = remove_node
            for i in range(r_node.height):
                if i == 0:
                    r_node.prev.next = r_node.next
                    r_node.next.prev = r_node.prev
                else:
                    self.level[i-1].remove(elem)
            print('Remove ' + str(elem) + ' successfully')
        else:
            print('No element removed')


if __name__ == '__main__':
    sl = SkipList([1, 3, 5, 9, 20, 15, 18, 30, 40, 32, 35])
    print(sl)
    print('-----------')
    sl.insert(8)
    print(sl)
    print('-----------')
    sl.remove(3)
    print(sl)
    print('-----------')
    sl.insert(99)
    sl.insert(76)
    print(sl)
    print('-----------')
    sl.insert(32)
    print(sl)
    print('-----------')
    sl.remove(2)
    print(sl)
    print('-----------')
    sl.search(2)
    print(sl)
