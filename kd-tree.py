'''
Creator George Maroulis Jan 2019
Language : Python 3.6
'''

from random import uniform
from numpy import isclose
import time


class KDTree:
    def __init__(self):
        self.root = None
        self.dim = 0

    def create(self, data):
        """Creates root node"""
        self.dim = len(data[0]) - 1
        spa = 0
        if len(data) == 1:
            lp = None
            rp = None
            median = 0
        else:
            data.sort(key=lambda data: data[spa])
            median = self.__findmiddle(data, spa)
            if median == 0:
                lp = None
                rp = data[median + 1:]
            elif median == len(data) - 1:
                rp = None
                lp = data[:median]
            else:
                lp = data[:median]
                rp = data[median + 1:]
        self.root = KDNode(0, data[median], lp, rp, 0)
        self.__addnext(self.root, 1)

    def __addnext(self, node, layer):
        """Recursion for every node"""
        if node.lp is not None:
            data = node.lp
            spa = node.spa + 1
            if spa > self.dim:
                spa = 0
            if len(data) == 1:
                lp = None
                rp = None
                median = 0
            else:
                data.sort(key=lambda data: data[spa])
                median = self.__findmiddle(data, spa)
                if median == 0:
                    lp = None
                    rp = data[median + 1:]
                elif median == len(data)-1:
                    rp = None
                    lp = data[:median]
                else:
                    lp = data[:median]
                    rp = data[median + 1:]
            node.lp = KDNode(spa, data[median], lp, rp, layer)
            self.__addnext(node.lp, layer + 1)
        if node.rp is not None:
            data = node.rp
            spa = node.spa + 1
            if spa > self.dim:
                spa = 0
            if len(data) == 1:
                lp = None
                rp = None
                median = 0
            else:
                data.sort(key=lambda data: data[spa])
                median = self.__findmiddle(data, spa)
                if median == 0:
                    lp = None
                    rp = data[median + 1:]
                elif median == len(data)-1:
                    rp = None
                    lp = data[:median]
                else:
                    lp = data[:median]
                    rp = data[median + 1:]
            node.rp = KDNode(spa, data[median], lp, rp, layer)
            self.__addnext(node.rp, layer + 1)

    def __findmiddle(self, input_list, spa):
        middle = float(len(input_list)) / 2
        if middle % 2 != 0:
            middle = int(middle - .5)
        else:
            middle = int(middle)
        for i in range(middle, 0, -1):
            if i > 0:
                if isclose(input_list[i][spa], input_list[i - 1][spa]):
                    middle = i - 1
                else:
                    break
        return middle

    def insert(self, data, node=None):
        if node is None:
            node = self.root
        spa = node.spa
        if node.data[spa] > data[spa]:
            spa = spa + 1
            if spa > self.dim:
                spa = 0
            if node.lp is None:
                node.lp = KDNode(spa, data, None, None, node.layer + 1)
                return 1
            else:
                return self.insert(data, node.lp)
        elif node.data[spa] <= data[spa]:
            spa = spa + 1
            if spa > self.dim:
                spa = 0
            if node.rp is None:
                node.rp = KDNode(spa, data, None, None, node.layer + 1)
                return 1
            else:
                return self.insert(data, node.rp)

    def delete(self, data, node=None, father=None):
        if node is None:
            node = self.root
        spa = node.spa
        res = isclose(node.data, data)
        if sum(res) == self.dim + 1:
            if node.lp is None and node.rp is None:
                if father.lp is node:
                    father.lp = None
                else:
                    father.rp = None
                return 1
            else:
                if node.rp is not None:
                    mnode = self.__findmin(node.rp, spa)
                    node.data = mnode.data
                    return self.delete(node.data, node.rp, node)
                elif node.lp is not None:
                    mnode = self.__findmin(node.lp, spa)
                    node.data = mnode.data
                    node.rp = node.lp
                    node.lp = None
                    return self.delete(node.data, node.rp, node)
        elif node.data[spa] > data[spa]:
            if node.lp is None:
                return 0
            return self.delete(data, node.lp, node)
        elif node.data[spa] <= data[spa]:
            if node.rp is None:
                return 0
            return self.delete(data, node.rp, node)

    def __findmin(self, node, spa):
        nds = list()
        if node.lp is not None:
            nds.append(node.lp)
        if node.rp is not None:
            nds.append(node.rp)
        mi = node.data[spa]
        mnode = node
        while len(nds) > 0:
            if nds[0].lp is not None:
                nds.append(nds[0].lp)
            if nds[0].rp is not None:
                nds.append(nds[0].rp)
            if nds[0].data[spa] <= mi:
                mi = nds[0].data[spa]
                mnode = nds[0]
            nds.remove(nds[0])
        return mnode

    def exact_search(self, data, node=None):
        if node is None:
            node = self.root
        spa = node.spa
        if node.data[spa] > data[spa]:
            if node.lp is None:
                return 0
            return self.exact_search(data, node.lp)
        elif node.data[spa] < data[spa]:
            if node.rp is None:
                return 0
            return self.exact_search(data, node.rp)
        elif isclose(node.data, data).all:
            return 1
        elif isclose(node.data[spa], data[spa]):
            if node.rp is None:
                return 0
            return self.exact_search(data, node.rp)

    def range_search(self, data, rll, node=None):
        if node is None:
            node = self.root
        spa = node.spa
        if node.data[spa] >= data[0][spa] and node.data[spa] <= data[1][spa]:
            flag = 0
            for i in range(len(data[0])):
                if data[0][i] <= node.data[i] and data[1][i] >= node.data[i]:
                    flag += 1
            if flag == self.dim + 1:
                rll.append(node.data)
            if node.lp is not None:
                rll = self.range_search(data, rll, node.lp)
            if node.rp is not None:
                rll = self.range_search(data, rll, node.rp)
        elif node.data[spa] > data[1][spa]:
            if node.lp is not None:
                rll = self.range_search(data, rll, node.lp)
        elif node.data[spa] <= data[0][spa]:
            if node.rp is not None:
                rll = self.range_search(data, rll, node.rp)
        return rll

    def kNN(self, data, k, nnl=None, node=None, father=None):
        if nnl is None:
            if node is None:
                node = self.root
            spa = node.spa
            if node.data[spa] > data[spa]:
                if node.lp is None:
                    nnl = list()
                    nnl.append(node.data)
                    nnl = self.kNN(data, k, nnl, node, father)
                else:
                    nnl = self.kNN(data, k, nnl, node.lp, node)
            elif node.data[spa] <= data[spa]:
                if node.rp is None:
                    nnl = list()
                    nnl.append(node.data)
                    nnl = self.kNN(data, k, nnl, node, father)
                else:
                    nnl = self.kNN(data, k, nnl, node.rp, node)

        if nnl is not None and father is not None:
            if father.rp == node and father.lp is not None:
                if len(nnl) <= k - 1:
                    nnl.append(father.lp.data)
                else:
                    for i in range(k):
                        osum = 0
                        nsum = 0
                        for j in range(len(data)):
                            nsum += abs(father.lp.data[j] - data[j])
                            osum += abs(nnl[i][j] - data[j])
                        if nsum < osum:
                            nnl[i] = father.lp.data
                            break
            elif father.lp == node and father.rp is not None:
                if len(nnl) <= k - 1:
                    nnl.append(father.rp.data)
                else:
                    for i in range(k):
                        osum = 0
                        nsum = 0
                        for j in range(len(data)):
                            nsum += abs(father.rp.data[j] - data[j])
                            osum += abs(nnl[i][j] - data[j])
                        if nsum < osum:
                            nnl[i] = father.rp.data
                            break
        return nnl


class KDNode:
    def __init__(self, spa, data, lp, rp, layer):
        self.spa = spa
        self.data = data
        self.lp = lp
        self.rp = rp
        self.layer = layer


def create_input(size, dim, mn, mx):
    try:
        f = open("dataset.txt", "w+")
        for i in range(size):
            for j in range(dim):
                f.write("{} ".format(uniform(mn, mx)))
            f.write("\n")
        f.close()
    except IOError:
        print("Unable to create the file")
        exit(0)


def get_input(filename, dim, size):
    try:
        f = open(filename, "r")
        inputdata = []
        for i in range(size):
            dt = f.readline()
            dt = dt[:-1]
            dt = dt.split(" ")
            tp = []
            for j in range(dim):
                tp.append(float(dt[j]))
            tp = tuple(tp)
            inputdata.append(tp)
        f.close()
        return inputdata
    except IOError:
        print("Unable to open the file {}. Maybe it doesn't exist".format(filename))
        exit(0)
    except ValueError:
        print("Wrong dimentions or size")
        menu()


def menu():
    try:
        ch = int(input("Give your choise's corresponding number\n1. I already have a dataset\n2. Create a random dataset\n"))
    except ValueError:
        print("Input must be integer")
        menu()
    if ch == 1:
        filename = input("Give the dataset's directory : ")
        try:
            dim = int(input("Give your dataset's dimentions : "))
            size = int(input("Give your dataset's size : "))
        except ValueError:
            print("Must be integers")
            menu()
        inputdata = get_input(filename, dim, size)
        print("I loaded the dataset")
    elif ch == 2:
        try:
            size = int(input("Give me the number of elements you want me to create : "))
            dim = int(input("Give the dimentions you prefer : "))
            mx = float(input("Give me the max value of the elements : "))
            mn = float(input("Give me the min value of the elements : "))
        except ValueError:
            print("Must be numbers")
            menu()
        create_input(size, dim, mx, mn)
        inputdata = get_input('dataset.txt', dim, size)
        print("I created a dataset named dataset.txt in ./")
    else:
        menu()
    print("Creating the tree")
    tree = KDTree()
    start = time.time()
    tree.create(inputdata)
    print('It took', time.time() - start, 'seconds to initialize the tree with {} elements.'.format(len(inputdata)))
    after_load_menu(tree)


def after_load_menu(tree):
    print("\n")
    try:
        ch = int(input("Give your choise's corresponding number\n1. Perform an exact search\n2. Perform a range search\n3. Perform an insertion\n4. Perform a deletion\n5. Find kNN\n6. Exit\n"))
    except ValueError:
        print("Input must be integer")
        after_load_menu(tree)
    if ch == 1:
        to_find = []
        for i in range(tree.dim + 1):
            try:
                to_find.append(float(input("Give me the value for dimention {} : ".format(i + 1))))
            except ValueError:
                print("Must be numbers")
                after_load_menu(tree)
        to_find = tuple(to_find)
        start = time.time()
        if tree.exact_search(to_find):
            print("Found it")
        else:
            print("Not in the dataset")
        print('It took', time.time() - start, 'seconds to perform an exact search.')
        after_load_menu(tree)
    elif ch == 2:
        to_find1 = []
        to_find2 = []
        for i in range(tree.dim + 1):
            try:
                to_find1.append(float(input("Give me the value for dimention {} for min : ".format(i + 1))))
            except ValueError:
                print("Must be numbers")
                after_load_menu(tree)
        to_find1 = tuple(to_find1)
        for i in range(tree.dim + 1):
            try:
                to_find2.append(float(input("Give me the value for dimention {} for max : ".format(i + 1))))
            except ValueError:
                print("Must be numbers")
                after_load_menu(tree)
        to_find2 = tuple(to_find2)
        start = time.time()
        rll = tree.range_search([to_find1, to_find2], [])
        print("Found {} elements in that range".format(len(rll)))
        print('It took', time.time() - start, 'seconds to perform an range search.')
        try:
            ch1 = int(input("1. Show me the results and move on\n2. Move on\n"))
        except ValueError:
            print("Must be an integer")
            after_load_menu(tree)
        if ch1 == 1:
            print(rll)
        after_load_menu(tree)
    elif ch == 3:
        to_insert = []
        for i in range(tree.dim + 1):
            try:
                to_insert.append(float(input("Give me the value for dimention {} to insert : ".format(i + 1))))
            except ValueError:
                print("Must be numbers")
                after_load_menu(tree)
        to_insert = tuple(to_insert)
        start = time.time()
        if not tree.insert(to_insert):
            print("Failed to insert element")
        else:
            print("Inserted successfully")
        print('It took', time.time() - start, 'seconds to perform an insertion.')
        after_load_menu(tree)
    elif ch == 4:
        to_delete = []
        for i in range(tree.dim + 1):
            try:
                to_delete.append(float(input("Give me the value for dimention {} to delete : ".format(i + 1))))
            except ValueError:
                print("Must be numbers")
                after_load_menu(tree)
        to_delete = tuple(to_delete)
        start = time.time()
        if tree.delete(to_delete):
            print("Element deleted")
        else:
            print("Element not in the dataset")
        print('It took', time.time() - start, 'seconds to delete an element.')
        after_load_menu(tree)
    elif ch == 5:
        to_kNN = []
        for i in range(tree.dim + 1):
            try:
                to_kNN.append(float(input("Give me the value for dimention {} to find kNN : ".format(i + 1))))
            except ValueError:
                print("Must be numbers")
                after_load_menu(tree)
        try:
            k = int(input("How many neighbors : "))
        except ValueError:
            print("Must be integer")
            after_load_menu(tree)
        to_kNN = tuple(to_kNN)
        start = time.time()
        kNN = tree.kNN(to_kNN, k)
        print("I found {} {}NN in {} second ".format(kNN, k, time.time() - start))
        after_load_menu(tree)
    elif ch == 6:
        exit(0)
    else:
        after_load_menu(tree)


menu()
