class SinglyLinkedNode(object):

    def __init__(self, item=None, next_link=None):
        super(SinglyLinkedNode, self).__init__()
        self._item = item
        self._next = next_link

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, item):
        self._item = item

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next):
        self._next = next

    def __repr__(self):
        return repr(self.item)


class SinglyLinkedList(object):

    def __init__(self):
        super(SinglyLinkedList, self).__init__()
        self.head = None

    # Gives the number of elements in the list
    def __len__(self):
        """
        >>> sll = SinglyLinkedList()
        >>> sll.prepend(10)
        >>> sll.prepend(20)
        >>> sll.prepend(30)
        >>> sll.__len__()
        3
        """
        cur_node = self.head
        i = 0
        while cur_node is not None:
            i += 1
            cur_node = cur_node.next
        return i

    def __iter__(self):
        cur_node = self.head
        while cur_node is not None:
            yield str(cur_node.item)
            cur_node = cur_node.next

    # Checks if a given item is present in the list
    def __contains__(self, item):
        """
        >>> sll = SinglyLinkedList()
        >>> sll.prepend(10)
        >>> sll.__contains__(10)
        'Item 10 is present in the list'
        >>> sll.__contains__(30)
        'Item 30 is not present in the list'
        """
        cur_node = self.head
        return_string = "Item " + str(item) + " is not present in the list"
        while cur_node is not None:
            if (cur_node.item is item):
                return_string = "Item " + str(item) + " is present in the list"
                break
            else:
                cur_node = cur_node.next
        return return_string

    # This method can be used when the data in the node is a dictionary
    def __get__dictionary__node__(self, key):
        """
        >>> sll = SinglyLinkedList()
        >>> item = {10: 'Supraj'}
        >>> sll.prepend(item)
        >>> sll.__get__dictionary__node__(10)
        {10: 'Supraj'}
        """
        cur_node = self.head
        while cur_node is not None:
            if (cur_node.item.keys()[0] is key):
                break
            else:
                cur_node = cur_node.next
        return cur_node

    # This method is used to remove the value from the data attribute in the node
    def remove(self, item):
        """
        >>> sll = SinglyLinkedList()
        >>> sll.prepend(10)
        >>> sll.remove(10)
        'Item 10 has been deleted from the head'
        >>> sll.remove(10)
        "Item 10 is not present in the list, can't be deleted"
        """
        cur_node = self.head
        pre_node = None
        return_string = "Item " + str(item) + " is not present in the list, can't be deleted"
        while cur_node is not None:
            if (cur_node.item is item and pre_node is None):
                self.head = cur_node.next
                return_string = "Item " + str(item) + " has been deleted from the head"
                break
            elif (cur_node.item is item):
                pre_node.next = cur_node.next
                return_string = "Item " + str(item) + " has been deleted"
                break
            else:
                pre_node = cur_node
                cur_node = cur_node.next
        return return_string

    # This method is used to delete a dictionary from the data in the node
    def remove_dictionary(self, key):
        """
        >>> sll = SinglyLinkedList()
        >>> item = {10: 'Supraj'}
        >>> sll.prepend(item)
        >>> sll.remove_dictionary(10)
        'Item 10 has been deleted from the head'
        >>> sll.remove_dictionary(10)
        "Item 10 is not present in the list, can't be deleted"
        """
        cur_node = self.head
        pre_node = None
        return_string = "Item " + str(key) + " is not present in the list, can't be deleted"
        while cur_node is not None:
            if (cur_node.item.keys()[0] is key and pre_node is None):
                self.head = cur_node.next
                return_string = "Item " + str(key) + " has been deleted from the head"
                break
            elif (cur_node.item.keys()[0] is key):
                pre_node.next = cur_node.next
                return_string = "Item " + str(key) + " has been deleted"
                break
            else:
                pre_node = cur_node
                cur_node = cur_node.next
        return return_string

    # This method is used for adding an element at the beginning of the list
    def prepend(self, item):
        """
        >>> sll = SinglyLinkedList()
        >>> sll.prepend(10)

        """
        cur_node = SinglyLinkedNode(item, self.head)
        self.head = cur_node

    def __repr__(self):
        """
        >>> sll = SinglyLinkedList()
        >>> sll.prepend(10)
        >>> sll.prepend(20)
        >>> sll.prepend(30)
        >>> sll.__repr__()
        'List:30->20->10'
        """
        s = "List:" + "->".join([item for item in self])
        return s


class ChainedHashDict(object):

    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        super(ChainedHashDict, self).__init__()
        self.hash_function = hashfunc
        self._bin_count = bin_count
        self.max_load = max_load
        self.hash_table = [None] * bin_count

    @property
    def load_factor(self):
        """
        >>> chc = ChainedHashDict(hashfunc=hash_function(10))
        >>> chc.__setitem__(57, 'Supraj')
        >>> chc.load_factor
        0.1
        """
        return float(self.__len__()) / float(self.bin_count)

    # Will return the number of bins
    @property
    def bin_count(self):
        """
        >>> chc = ChainedHashDict(hashfunc=hash_function(10))
        >>> chc.bin_count
        10
        """
        return self._bin_count

    # Will rebuild the hash table by doubling the number of bins
    def rebuild(self, bincount):
        self._bin_count *= 2
        if(self.hash_function.func_name is 'hashfunc'):
            self.hash_function = terrible_hash(self._bin_count)
        else:
            self.hash_function = hash_function(self._bin_count)
        cur_table = self.hash_table
        self.hash_table = [None] * self.bin_count
        for cur_list in cur_table:
            if cur_list is not None:
                cur_node = cur_list.head
                while cur_node is not None:
                    self.__setitem__(cur_node.item.keys()[0], cur_node.item.values()[0])
                    cur_node = cur_node.next

    # Will get the value for the corresponding key
    def __getitem__(self, key):
        """
        >>> chc = ChainedHashDict(hashfunc=hash_function(10))
        >>> chc.__setitem__(57, 'Supraj')
        >>> chc.__getitem__(57)
        'Supraj'
        >>> chc.__getitem__(58)
        'Key 58 is not present in the table'
        """
        return_string = "Key " + str(key) + " is not present in the table"
        index = self.hash_function(key)
        list = self.hash_table[index]
        if (list is not None):
            result = list.__get__dictionary__node__(key)
            if result is not None:
                return_string = str(result.item.values()[0])
        return return_string

    # Will insert the items in the Hash Table
    def __setitem__(self, key, value):
        """
        >>> chc = ChainedHashDict(hashfunc=hash_function(10))
        >>> chc.__setitem__(57, 'Supraj')

        """
        index = self.hash_function(key)
        item = {key: value}
        list = self.hash_table[index]
        if (list is None):
            list = SinglyLinkedList()
        list.prepend(item)
        self.hash_table[index] = list
        if(self.load_factor > self.max_load):
            self.rebuild(self.bin_count)

    # Will delete the item with 'key'
    def __delitem__(self, key):
        """
        >>> chc = ChainedHashDict(hashfunc=hash_function(10))
        >>> chc.__setitem__(57, 'Supraj')
        >>> chc.__delitem__(57)
        'Key 57 is deleted successfully'
        >>> chc.__delitem__(58)
        'Key 58 is not present in the table'
        """
        return_string = "Key " + str(key) + " is not present in the table"
        index = self.hash_function(key)
        list = self.hash_table[index]
        if (list is not None):
            remove_result = list.remove_dictionary(key)
            if(list.head is None):
                self.hash_table[index] = None
            if("not present" not in remove_result):
                return_string = "Key " + str(key) + " is deleted successfully"
        return return_string

    # Will check if the key is present in the Hash Table
    def __contains__(self, key):
        """
        >>> chc = ChainedHashDict(hashfunc=hash_function(10))
        >>> chc.__setitem__(57, 'Supraj')
        >>> chc.__contains__(57)
        'Key 57 is present in the table'
        >>> chc.__contains__(58)
        'Key 58 is not present in the table'
        """
        return_string = "Key " + str(key) + " is not present in the table"
        index = self.hash_function(key)
        list = self.hash_table[index]
        if (list is not None):
            result = list.__get__dictionary__node__(key)
            if result is not None:
                return_string = "Key " + str(key) + " is present in the table"
        return return_string

    # Will give the number of elements in the table
    def __len__(self):
        """
        >>> chc = ChainedHashDict(hashfunc=hash_function(10))
        >>> chc.__setitem__(57, 'Supraj')
        >>> chc.__setitem__(58, 'Sriram')
        >>> chc.__len__()
        2
        """
        i = 0
        for cur_list in self.hash_table:
            if(cur_list is not None):
                i += cur_list.__len__()
        return i

    # Will print all the values in the hash table
    def display(self):
        """
        >>> chc = ChainedHashDict(hashfunc=hash_function(10))
        >>> chc.__setitem__(57, 'Supraj')
        >>> chc.__setitem__(58, 'Sriram')
        >>> chc.display()
        0- None
        1- None
        2- None
        3- None
        4- None
        5- None
        6- None
        7- List:{57: 'Supraj'}
        8- List:{58: 'Sriram'}
        9- None
        """
        i = 0
        for cur_list in self.hash_table:
            print_string = str(i) + "- None"
            if cur_list is not None:
                print_string = str(i) + "- " + cur_list.__repr__()
            i += 1
            print print_string


def hash_function(bin):
    def h(item):
        return item % bin
    return h


class OpenAddressHashDict(object):

    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        super(OpenAddressHashDict, self).__init__()
        self.hash_table = [None] * bin_count
        self.hash_function = hashfunc
        self._bin_count = bin_count
        self.max_load = max_load

    @property
    def load_factor(self):
        """
        >>> ohd= OpenAddressHashDict()
        >>> ohd.__setitem__(57, 'Supraj')
        >>> ohd.load_factor
        0.1
        """
        return float(self.__len__()) / float(self.bin_count)

    # Will return the number of bins
    @property
    def bin_count(self):
        """
        >>> ohd= OpenAddressHashDict()
        >>> ohd.bin_count
        10
        """
        return self._bin_count

    # Will rebuild the hash table by doubling the number of bins
    def rebuild(self, bincount):
        self._bin_count *= 2
        if(self.hash_function == hash):
            self.hash_function = hash
        else:
            self.hash_function = terrible_hash(self._bin_count)
        cur_table = self.hash_table
        self.hash_table = [None] * self.bin_count
        for cur_value in cur_table:
            if(cur_value is not None):
                self.__setitem__(cur_value.keys()[0], cur_value.values()[0])

    # Will get the value for the corresponding key
    def __getitem__(self, key):
        """
        >>> ohd= OpenAddressHashDict()
        >>> ohd.__setitem__(57, 'Supraj')
        >>> ohd.__getitem__(57)
        'Supraj'
        >>> ohd.__getitem__(58)
        'Key 58 is not present in the table'
        """
        return_string = "Key " + str(key) + " is not present in the table"
        index = self.hash_function(key) % self.bin_count
        i = 0
        value_at_index = self.hash_table[index]
        while (value_at_index is not None):
            if(value_at_index.keys()[0] == key):
                return_string = str(value_at_index.values()[0])
                break
            else:
                i += 1
                index = (self.hash_function(key) + i) % self.bin_count
                value_at_index = self.hash_table[index]
        return return_string

    # Will insert the items in the Hash Table
    def __setitem__(self, key, value):
        """
        >>> ohd= OpenAddressHashDict()
        >>> ohd.__setitem__(57, 'Supraj')

        """
        index = self.hash_function(key) % self.bin_count
        item = {key: value}
        i = 0
        value_at_index = self.hash_table[index]
        while (value_at_index is not None):
            if(value_at_index.keys()[0] == -1):
                break
            i += 1
            index = (self.hash_function(key) + i) % self.bin_count
            value_at_index = self.hash_table[index]

        self.hash_table[index] = item
        if(self.load_factor > self.max_load):
            self.rebuild(self.bin_count)

    # Will delete the item with 'key'
    def __delitem__(self, key):
        """
        >>> ohd= OpenAddressHashDict()
        >>> ohd.__setitem__(57, 'Supraj')
        >>> ohd.__delitem__(57)
        'Key 57 is successfully deleted'
        >>> ohd.__delitem__(57)
        'Key 57 is not present in the table'
        """
        return_string = "Key " + str(key) + " is not present in the table"
        index = self.hash_function(key) % self.bin_count
        i = 0
        value_at_index = self.hash_table[index]
        while (value_at_index is not None):
            if(value_at_index.keys()[0] == key):
                self.hash_table[index] = {-1: 'DELETED'}
                return_string = "Key " + str(key) + " is successfully deleted"
                break
            else:
                i += 1
                index = (self.hash_function(key) + i) % self.bin_count
                value_at_index = self.hash_table[index]
        return return_string

    # Will check if the key is present in the Hash Table
    def __contains__(self, key):
        """
        >>> ohd= OpenAddressHashDict()
        >>> ohd.__setitem__(57, 'Supraj')
        >>> ohd.__contains__(57)
        'Key 57 is present in the table with value Supraj'
        >>> ohd.__contains__(58)
        'Key 58 is not present in the table'
        """
        return_string = "Key " + str(key) + " is not present in the table"
        index = self.hash_function(key) % self.bin_count
        i = 0
        value_at_index = self.hash_table[index]
        while (value_at_index is not None):
            if(value_at_index.keys()[0] == key):
                return_string = "Key " + str(key) + " is present in the table with value " + value_at_index.values()[0]
                break
            else:
                i += 1
                index = (self.hash_function(key) + i) % self.bin_count
                value_at_index = self.hash_table[index]
        return return_string

    # Will give the number of elements in the table
    def __len__(self):
        """
        >>> ohd= OpenAddressHashDict()
        >>> ohd.__setitem__(57, 'Supraj')
        >>> ohd.__setitem__(58, 'Sriram')
        >>> ohd.__len__()
        2
        """
        i = 0
        for value in self.hash_table:
            if value is not None:
                if value.keys()[0] is not -1:
                    i += 1
        return i

    # Will print all the values in the hash table
    def display(self):
        """
        >>> ohd= OpenAddressHashDict()
        >>> ohd.__setitem__(57, 'Supraj')
        >>> ohd.__setitem__(58, 'Sriram')
        >>> ohd.display()
        0- None
        1- None
        2- None
        3- None
        4- None
        5- None
        6- None
        7- {57: 'Supraj'}
        8- {58: 'Sriram'}
        9- None
        """
        i = 0
        for value in self.hash_table:
            print_string = str(i) + "- " + "None"
            if(value is not None):
                print_string = str(i) + "- " + str(value)
            i += 1
            print print_string


class BinaryTreeNode(object):
    def __init__(self, data=None, left=None, right=None, parent=None):
        super(BinaryTreeNode, self).__init__()
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent


class BinarySearchTreeDict(object):

    def __init__(self):
        super(BinarySearchTreeDict, self).__init__()
        self.root = None

    # Gives the height of the tree
    @property
    def height(self):
        """
        >>> bst = BinarySearchTreeDict()
        >>> print bst.height
        -1
        >>> bst.__setitem__(57, 'Supraj')
        >>> print bst.height
        0
        >>> bst.__setitem__(58, 'Sriram')
        >>> print bst.height
        1
        """
        return tree_height(self.root)

    def inorder_keys(self):
        """
        >>> bst = BinarySearchTreeDict()
        >>> bst.__setitem__(57, 'Supraj')
        >>> bst.__setitem__(58, 'Sriram')
        >>> bst.__setitem__(46, 'Rathna')
        >>> bst.inorder_keys()
        In order tree traversal:46->57->58
        """
        print "In order tree traversal:" + "->".join([str(item.keys()[0]) for item in self.tree_in_order(self.root)])

    def postorder_keys(self):
        """
        >>> bst = BinarySearchTreeDict()
        >>> bst.__setitem__(57, 'Supraj')
        >>> bst.__setitem__(58, 'Sriram')
        >>> bst.__setitem__(46, 'Rathna')
        >>> bst.postorder_keys()
        Post order tree traversal:46->58->57
        """
        print "Post order tree traversal:" + "->".join([str(item) for item in self.tree_post_order(self.root)])

    def preorder_keys(self):
        """
        >>> bst = BinarySearchTreeDict()
        >>> bst.__setitem__(57, 'Supraj')
        >>> bst.__setitem__(58, 'Sriram')
        >>> bst.__setitem__(46, 'Rathna')
        >>> bst.preorder_keys()
        Pre order tree traversal:57->46->58
        """
        print "Pre order tree traversal:" + "->".join([str(item) for item in self.tree_pre_order(self.root)])

    # Prints the key value pair items in the tree
    def items(self):
        """
        >>> bst = BinarySearchTreeDict()
        >>> bst.__setitem__(57, 'Supraj')
        >>> bst.__setitem__(58, 'Sriram')
        >>> bst.__setitem__(46, 'Rathna')
        >>> bst.items()
        Items:{46: 'Rathna'}->{57: 'Supraj'}->{58: 'Sriram'}
        """
        print "Items:" + "->".join([str(item) for item in self.tree_in_order(self.root)])

    # Will return the value for the corresponding key
    def __getitem__(self, key):
        """
        >>> bst = BinarySearchTreeDict()
        >>> bst.__setitem__(57, 'Supraj')
        >>> bst.__getitem__(57)
        'Supraj'
        >>> bst.__getitem__(58)
        'No item with key 58 in the tree'
        """
        return_string = "No item with key " + str(key) + " in the tree"
        cur_node = tree_search(self.root, key)
        if (cur_node is not None):
            return_string = str(cur_node.data.get(cur_node.data.keys()[0]))
        return return_string

    # Adding the element in the tree
    def __setitem__(self, key, value):
        """
        >>> bst = BinarySearchTreeDict()
        >>> bst.__setitem__(57, 'Supraj')

        """
        cur_data = {key: value}
        cur_node = BinaryTreeNode(data=cur_data)
        if (self.root is None):
            self.root = cur_node
        else:
            tree_insert(self.root, cur_node)

    # Deleting the element from the tree
    def __delitem__(self, key):
        """
        >>> bst = BinarySearchTreeDict()
        >>> bst.__setitem__(57, 'Supraj')
        >>> bst.__delitem__(57)
        'Item 57 deleted successfully'
        >>> bst.__delitem__(57)
        'No item with key 57 in the tree'
        """
        return_string = "No item with key " + str(key) + " in the tree"
        cur_node = tree_search(self.root, key)
        if(cur_node is not None):
            if(cur_node.left is None):
                transplant(self, cur_node, cur_node.right)
            elif(cur_node.right is None):
                transplant(self, cur_node, cur_node.left)
            else:
                successor_node = tree_minimum(cur_node.right)
                if(successor_node.parent.data.keys()[0] is not cur_node.data.keys()[0]):
                    transplant(self, successor_node, successor_node.right)
                    successor_node.right = cur_node.right
                    successor_node.right.parent = successor_node
                transplant(self, cur_node, successor_node)
                successor_node.left = cur_node.left
                successor_node.left.parent = successor_node
            return_string = "Item " + str(key) + " deleted successfully"
        return return_string

    # Checks if an element with 'key' is present in the tree
    def __contains__(self, key):
        """
        >>> bst = BinarySearchTreeDict()
        >>> bst.__setitem__(57, 'Supraj')
        >>> bst.__contains__(57)
        'Item with key 57 is found and its value is Supraj'
        >>> bst.__contains__(58)
        'No item with key 58 in the tree'
        """
        return_string = "No item with key " + str(key) + " in the tree"
        cur_node = tree_search(self.root, key)
        if (cur_node is not None):
            return_string = "Item with key " + str(key) + " is found and its value is " + str(cur_node.data.get(cur_node.data.keys()[0]))
        return return_string

    # Gives the number of elements in the tree
    def __len__(self):
        """
        >>> bst = BinarySearchTreeDict()
        >>> bst.__setitem__(57, 'Supraj')
        >>> bst.__setitem__(58, 'Sriram')
        >>> bst.__setitem__(46, 'Rathna')
        >>> bst.__len__()
        3
        """
        return tree_length(self.root)

    # Displays the keys in in-oder and pre-order
    def display(self):
        """
        >>> bst = BinarySearchTreeDict()
        >>> bst.__setitem__(57, 'Supraj')
        >>> bst.__setitem__(58, 'Sriram')
        >>> bst.__setitem__(46, 'Rathna')
        >>> bst.display()
        In order tree traversal:46->57->58
        Pre order tree traversal:57->46->58
        """
        self.inorder_keys()
        self.preorder_keys()

    def tree_in_order(self, cur_root):
        if cur_root is not None:
            for item in self.tree_in_order(cur_root.left):
                yield item
            yield cur_root.data
            for item in self.tree_in_order(cur_root.right):
                yield item
        else:
            StopIteration()

    def tree_pre_order(self, cur_root):
        if cur_root is not None:
            yield cur_root.data.keys()[0]
            for item in self.tree_pre_order(cur_root.left):
                yield item
            for item in self.tree_pre_order(cur_root.right):
                yield item
        else:
            StopIteration()

    def tree_post_order(self, cur_root):
        if cur_root is not None:
            for item in self.tree_post_order(cur_root.left):
                yield item
            for item in self.tree_post_order(cur_root.right):
                yield item
            yield cur_root.data.keys()[0]
        else:
            StopIteration()


# Will insert cur_node in the tree
def tree_insert(cur_root, cur_node):
    cur_node_key = cur_node.data.keys()[0]
    cur_root_key = cur_root.data.keys()[0]
    if(cur_node_key < cur_root_key):
        if(cur_root.left is None):
            cur_node.parent = cur_root
            cur_root.left = cur_node
        else:
            tree_insert(cur_root.left, cur_node)
    elif(cur_node_key >= cur_root_key):
        if(cur_root.right is None):
            cur_node.parent = cur_root
            cur_root.right = cur_node
        else:
            tree_insert(cur_root.right, cur_node)


# Will search for the a node with key equal to 'key'
def tree_search(cur_root, key):
    return_node = None
    while(cur_root is not None):
        if(cur_root.data.keys()[0] == key):
            return_node = cur_root
            break
        elif(key < cur_root.data.keys()[0]):
            cur_root = cur_root.left
        elif(key > cur_root.data.keys()[0]):
            cur_root = cur_root.right
    return return_node


# Will give the height of the tree
def tree_height(cur_root):
    return_int = -1
    if(cur_root is not None):
        left = tree_height(cur_root.left)
        right = tree_height(cur_root.right)
        if(left > right):
            return_int = left + 1
        else:
            return_int = right + 1
    return return_int


# Will give the number of elements in the tree
def tree_length(cur_root):
    return_int = 0
    if(cur_root is not None):
        left = tree_length(cur_root.left)
        right = tree_length(cur_root.right)
        return_int = left + right + 1
    return return_int


# Will transplant nodes u and v
def transplant(self, u, v):
    if(u.parent is None):
        self.root = v
    elif(u.data.keys()[0] is u.parent.left.data.keys()[0]):
        u.parent.left = v
    else:
        u.parent.right = v
    if(v is not None):
        v.parent = u.parent


# Will give the node with the minimum value in the tree
def tree_minimum(cur_root):
    while cur_root.left is not None:
        cur_root = cur_root.left
    return cur_root


def terrible_hash(bin):
    """A terrible hash function that can be used for testing.

    A hash function should produce unpredictable results,
    but it is useful to see what happens to a hash table when
    you use the worst-possible hash function.  The function
    returned from this factory function will always return
    the same number, regardless of the key.

    :param bin:
        The result of the hash function, regardless of which
        item is used.

    :return:
        A python function that can be passes into the constructor
        of a hash table to use for hashing objects.

    Doc test for chained
    >>> chd = ChainedHashDict(hashfunc=terrible_hash(10))
    >>> chd.__setitem__(57, 'Supraj')
    >>> chd.__setitem__(58, 'Sri')
    >>> chd.display()
    0- None
    1- None
    2- None
    3- None
    4- None
    5- None
    6- None
    7- None
    8- None
    9- List:{58: 'Sri'}->{57: 'Supraj'}

    Doc test for Open Adress Hashing
    >>> ohd = OpenAddressHashDict(hashfunc=terrible_hash(10))
    >>> ohd.__setitem__(57, 'Supraj')
    >>> ohd.__setitem__(58, 'Sri')
    >>> ohd.display()
    0- {58: 'Sri'}
    1- None
    2- None
    3- None
    4- None
    5- None
    6- None
    7- None
    8- None
    9- {57: 'Supraj'}

    """

    def hashfunc(item):
        return bin - 1
    return hashfunc


def main():
    bst_output()
    sll_output()
    chd_output()
    ohd_output()


def bst_output():
    bst = BinarySearchTreeDict()
    print "-----Binary Search Tree output-----"
    print "The height of the tree with no elements is " + str(bst.height)
    print "The length of the tree with no elements is " + str(bst.__len__())
    bst.__setitem__(57, 'Supraj')
    bst.__setitem__(58, 'Sri ram')
    print "The height of the tree after inserting 57 and 58 is " + str(bst.height)
    print "The length of the tree after inserting 57 and 58 is " + str(bst.__len__())
    print "Inserting elements with keys 46, 31, 32, 50 and 47..."
    bst.__setitem__(46, 'Rathnakar')
    bst.__setitem__(31, 'Yoga')
    bst.__setitem__(32, 'Sachin')
    bst.__setitem__(50, 'Ramesh')
    bst.__setitem__(47, 'Tendulkar')
    print "The value of the item with key 57 is " + bst.__getitem__(57)
    print "The value of the item with key 58 is " + bst.__getitem__(58)
    print "Trying to get the value for the key 99 which is not present in the tree..."
    print bst.__getitem__(99)
    print bst.__contains__(57)
    print bst.__contains__(58)
    print "Trying to check if the key 99 is present in the tree..."
    print bst.__contains__(99)
    print "Deleting the element 46 from the tree..."
    print bst.__delitem__(46)
    print "Height of the tree now is " + str(bst.height)
    print "Length of the tree now is " + str(bst.__len__())
    print "Checking if 46 is still present in the list after deletion..."
    print bst.__contains__(46)
    bst.inorder_keys()
    bst.postorder_keys()
    bst.preorder_keys()
    bst.items()
    print "Display..."
    bst.display()
    print "Deleting the head node..."
    print bst.__delitem__(57)
    bst.items()
    print "Display..."
    bst.display()
    print "\n \n"


def sll_output():
    sll = SinglyLinkedList()
    print "-----Singly Linked List Output-----"
    print "Adding elements 10, 20, 30, 40, 50, 60, 70, 80..."
    sll.prepend(10)
    sll.prepend(20)
    sll.prepend(30)
    sll.prepend(40)
    sll.prepend(50)
    sll.prepend(60)
    sll.prepend(70)
    sll.prepend(80)
    print "List of elements are " + sll.__repr__()
    print "The length of the list is " + str(sll.__len__())
    print "Deleting the head node with value 80..."
    print sll.remove(80)
    print "Trying to delete the element 80 again..."
    print sll.remove(80)
    print "Checking if 80 is still in the list..."
    print sll.__contains__(80)
    print "Deleting element 40..."
    print sll.remove(40)
    print "The new length is " + str(sll.__len__())
    print "Adding dictionary elements..."
    sll2 = SinglyLinkedList()
    item = {10: 'Supraj'}
    item2 = {20: 'Rathna'}
    sll2.prepend(item)
    sll2.prepend(item2)
    print "The dictionary elements in the list are..."
    print sll2.__repr__()
    print "Deleting dictionary with key 20..."
    print sll2.remove_dictionary(20)
    print sll2.__repr__()
    print "The dictionary with key 10 is " + str(sll2.__get__dictionary__node__(10))
    print "\n \n"


def chd_output():
    chd = ChainedHashDict(hashfunc=hash_function(10))
    print "-----Chained Hash Dictionary Output-----"
    print "Initial load factor is " + str(chd.load_factor)
    print "Initial bin count is " + str(chd.bin_count)
    print "Initial length is " + str(chd.__len__())
    chd.__setitem__(57, 'Supraj')
    chd.__setitem__(58, 'Sri')
    chd.__setitem__(46, 'Rathna')
    chd.__setitem__(36, 'Dup')
    chd.__setitem__(1, 'One')
    chd.__setitem__(2, 'Two')
    chd.__setitem__(16, 'Sixteen')
    print "Table..."
    chd.display()
    print "Load Factor now is " + str(chd.load_factor)
    print "Adding new elements with keys 3, 4, 5, 6...."
    chd.__setitem__(3, 'Three')
    chd.__setitem__(4, 'Four')
    chd.__setitem__(5, 'Five')
    chd.__setitem__(6, 'Six')
    print "The table was rebuilt..."
    print "New load factor is " + str(chd.load_factor)
    print "New bin count is " + str(chd.bin_count)
    print "New length is " + str(chd.__len__())
    print "New Table..."
    chd.display()
    print "The value for key 57 is " + str(chd.__getitem__(57))
    print "Checking if the key 57 is in the table..."
    print chd.__contains__(57)
    print "Deleting element with key 57..."
    print chd.__delitem__(57)
    print "Checking if 57 is present in the table..."
    print chd.__contains__(57)
    print "Deleting elements 5, 6, 36, 46..."
    chd.__delitem__(5)
    chd.__delitem__(6)
    chd.__delitem__(36)
    chd.__delitem__(46)
    print "Table after deletion..."
    chd.display()

    print "Using Terrible Hashing..."
    chd2 = ChainedHashDict(hashfunc=terrible_hash(10))
    chd2.__setitem__(57, 'Supraj')
    chd2.__setitem__(58, 'Sri')
    chd2.__setitem__(46, 'Rathna')
    chd2.__setitem__(36, 'Dup')
    chd2.__setitem__(1, 'One')
    chd2.__setitem__(2, 'Two')
    chd2.__setitem__(16, 'Sixteen')
    print "Current Table..."
    chd2.display()
    chd2.__setitem__(3, 'Three')
    print "Rebuilt table..."
    chd2.display()
    print "\n \n"


def ohd_output():
    ohd = OpenAddressHashDict()
    print "-----Open Address Hash Dictionary Output-----"
    print "Initial load factor is " + str(ohd.load_factor)
    print "Initial bin count is " + str(ohd.bin_count)
    print "Initial length is " + str(ohd.__len__())
    ohd.__setitem__(57, 'Supraj')
    ohd.__setitem__(58, 'Sri')
    ohd.__setitem__(46, 'Rathna')
    ohd.__setitem__(36, 'Dup')
    ohd.__setitem__(1, 'One')
    ohd.__setitem__(2, 'Two')
    ohd.__setitem__(16, 'Sixteen')
    print "Table..."
    ohd.display()
    print "Load Factor now is " + str(ohd.load_factor)
    print "Adding new elements with keys 3, 4, 5, 6...."
    ohd.__setitem__(3, 'Three')
    ohd.__setitem__(4, 'Four')
    ohd.__setitem__(5, 'Five')
    ohd.__setitem__(6, 'Six')
    print "The table was rebuilt..."
    print "New load factor is " + str(ohd.load_factor)
    print "New bin count is " + str(ohd.bin_count)
    print "New length is " + str(ohd.__len__())
    print "New Table..."
    ohd.display()
    print "The value for key 57 is " + str(ohd.__getitem__(57))
    print "Checking if the key 57 is in the table..."
    print ohd.__contains__(57)
    print "Deleting element with key 57..."
    print ohd.__delitem__(57)
    print "Checking if 57 is present in the table..."
    print ohd.__contains__(57)
    print "Deleting elements 5, 6, 36, 46..."
    ohd.__delitem__(5)
    ohd.__delitem__(6)
    ohd.__delitem__(36)
    ohd.__delitem__(46)
    print "Inserting element with key 65, this will be inserted in the bin '5'"
    ohd.__setitem__(65, 'SixtyFive')
    print "Table after deletion..."
    ohd.display()

    print "Using Terrible Hashing..."
    ohd2 = OpenAddressHashDict(hashfunc=terrible_hash(10))
    ohd2.__setitem__(57, 'Supraj')
    ohd2.__setitem__(58, 'Sri')
    ohd2.__setitem__(46, 'Rathna')
    ohd2.__setitem__(36, 'Dup')
    ohd2.__setitem__(1, 'One')
    ohd2.__setitem__(2, 'Two')
    ohd2.__setitem__(16, 'Sixteen')
    print "Current Table..."
    ohd2.display()
    ohd2.__setitem__(3, 'Three')
    print "Rebuilt table..."
    ohd2.display()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
