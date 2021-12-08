import urllib
from Linked_List import LinkedList
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class HashTable(object):
    """
    Create a hash table with an assigned length
    """

    def __init__(self, length=4):
        # Initiate our array with empty values.
        self.array = [None] * length

    def hash(self, key):
        """
        Get the index of our array for a specific string key
        """
        length = len(self.array)
        return hash(key) % length

    def increase(self, key):
        """
        Add 1 to the current value by its key
        """
        node = self.find(key)
        node.data += 1

    def insert(self, key, value):
        """
        Add a value to our array by its key
        """
        index = self.hash(key)
        node = self.find(key)
        if node is not None:
            # If key is found, then update
            # its current value to the new value.
            node.data += value
        elif self.array[index]:
            # If no existing key was found,
            # so we can simply just add it to the end
            # if there's a linked list by the index.
            self.array[index].insert(value, key)
        else:
            # This index is empty. We should initiate
            # a linked list and append our key-value-pair to it.
            self.array[index] = LinkedList()
            self.array[index].insert(value, key)

    def find(self, key):
        """
        Get a value by key
        """
        index = self.hash(key)
        if self.array[index] is None:
            return None
        else:
            # Loop through all key-value-pairs
            # and find if our key exist. If it does
            # then return its value.
            for i in self.array[index]:
                if i.key == key:
                    return i
            # If no return was done during loop,
            # it means key didn't exist.
            return None

    def delete(self, key):
        """
        Delete a value by key
        """
        index = self.hash(key)
        if self.array[index] is None:
            raise KeyError()
        else:
            if self.array[index].head.key == key:
                node = self.array[index].head.next
                self.array[index].head = node
            else:
                for i in self.array[index]:
                    if i.next is None:
                        raise KeyError()
                    else:
                        if i.next.key == key:
                            i.next = i.next.next

    def key_list(self):
        """
        List all keys in the hashtable
        """
        keys = []
        for i in self.array:
            if i is None:
                continue
            else:
                for j in i:
                    keys.append(j.key)
        return keys


def read_doc(URL):
    """
    Read a document with URL
    """
    url = URL
    file = urllib.request.urlopen(url)

    content = ""

    for line in file:
        line = str(line)
        content += line

    return content


def pre_processing(content):
    """
    Pre-process a document
    """
    tokens = word_tokenize(content)
    print('Tokenization finished successfully')
    normalized1 = []
    for i in tokens:
        if i.isalpha() or i.isdigit():
            i = i.lower()
            normalized1.append(i)
    print('Punctuation removed successfully')
    normalized2 = [word for word in normalized1 if word not in stopwords.words()]
    print('Stopwords removed successfully')
    return normalized2


def output(output_list, file_name):
    """
    Output the result into a file
    """
    output_file = open(file_name, 'w')
    for element in output_list:
        output_file.write(str(element) + '\n')
    output_file.close()


def main():
    alice = read_doc('https://www.ccs.neu.edu/home/vip/teach/Algorithms/7_hash_RBtree_simpleDS/hw_hash_RBtree'
                     '/alice_in_wonderland.txt')
    print('Document read successfully')
    alice_normalized = pre_processing(alice)
    print('Pre-processing finished successfully')

    alice_ht = HashTable(length=500)
    print('Hashtable initialized successfully')

    for key in alice_normalized:
        alice_ht.insert(key, 1)
        print('Insert ' + key + ' successfully')
        node = alice_ht.find(key)
        print('Current data for ' + key + ' is ' + str(node.data))
    print('Hashtable built successfully')

    output_list = []
    for a in alice_ht.array:
        nodes = []
        if a:
            for b in a:
                nodes.append((b.key, b.data))
        output_list.append(nodes)
    print('Output list built successfully')

    output(output_list, 'alice_word_count.txt')
    print('Word count file built successfully')


if __name__ == '__main__':
    main()
