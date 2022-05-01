# Red black tree implementation
from enum import Enum


class Color(Enum):
    RED = 1
    BLACK = 2


class Node:
    # initialize node
    def __init__(self, value, color=Color.RED):
        self.value = value
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    def is_leaf(self):
        return self.left is None and self.right is None

    def is_left_child(self):
        return self.parent.left == self

    def is_right_child(self):
        return self.parent.right == self


class RedBlackTree:
    # initialize red black tree
    def __init__(self):
        self.nil = Node(None, Color.BLACK)
        self.root = self.nil
        self.nil.left = self.nil
        self.nil.right = self.nil
        self.nil.parent = self.nil

    def insert(self, value):
        if self.search(value):
            print("ERROR: Word already in the dictionary!")
            return False

        new_node = Node(value)
        temp_node = self.root
        parent = self.nil
        while temp_node != self.nil:
            parent = temp_node
            if value.casefold() < temp_node.value.casefold():
                temp_node = temp_node.left
            else:
                temp_node = temp_node.right
        new_node.parent = parent
        if parent == self.nil:
            self.root = new_node
        elif value.casefold() < parent.value.casefold():
            parent.left = new_node
        else:
            parent.right = new_node
        new_node.left = self.nil
        new_node.right = self.nil
        self.insert_fixup(new_node)
        return True

    def insert_fixup(self, new_node):
        while new_node.parent.color == Color.RED:
            # left parent case
            if new_node.parent.is_left_child():
                uncle = new_node.parent.parent.right
                # recolor case
                if uncle.color == Color.RED:
                    new_node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    new_node.parent.parent.color = Color.RED
                    new_node = new_node.parent.parent
                else:
                    # uncle black

                    if new_node.is_right_child():
                        # Left Right Case
                        new_node = new_node.parent
                        self.left_rotate(new_node)
                    # left left case and continuation of left right case
                    new_node.parent.color = Color.BLACK
                    new_node.parent.parent.color = Color.RED
                    self.right_rotate(new_node.parent.parent)
            # right parent case
            else:
                # recolor
                uncle = new_node.parent.parent.left
                if uncle.color == Color.RED:
                    new_node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    new_node.parent.parent.color = Color.RED
                    new_node = new_node.parent.parent
                else:
                    if new_node.is_left_child():
                        # right left case
                        new_node = new_node.parent
                        self.right_rotate(new_node)
                    # right right case and continuation of right left case
                    new_node.parent.color = Color.BLACK
                    new_node.parent.parent.color = Color.RED
                    self.left_rotate(new_node.parent.parent)
        self.root.color = Color.BLACK

    def left_rotate(self, new_node):
        temp_node = new_node.right
        new_node.right = temp_node.left
        if temp_node.left != self.nil:
            temp_node.left.parent = new_node
        temp_node.parent = new_node.parent
        if new_node.parent == self.nil:
            self.root = temp_node
        elif new_node.is_left_child():
            new_node.parent.left = temp_node
        else:
            new_node.parent.right = temp_node
        temp_node.left = new_node
        new_node.parent = temp_node

    def right_rotate(self, new_node):
        temp_node = new_node.left
        new_node.left = temp_node.right
        if temp_node.right != self.nil:
            temp_node.right.parent = new_node
        temp_node.parent = new_node.parent
        if new_node.parent == self.nil:
            self.root = temp_node
        elif new_node.is_right_child():
            new_node.parent.right = temp_node
        else:
            new_node.parent.left = temp_node
        temp_node.right = new_node
        new_node.parent = temp_node

    def search(self, value):
        temp_node = self.root
        while temp_node != self.nil:
            if value.casefold() == temp_node.value.casefold():
                return True
            elif value.casefold() < temp_node.value.casefold():
                temp_node = temp_node.left
            else:
                temp_node = temp_node.right
        return False

    def height(self, node):
        if node == self.nil:
            return 0
        else:
            return 1 + max(self.height(node.left), self.height(node.right))

    def size(self, node):
        if node == self.nil:
            return 0
        else:
            return 1 + self.size(node.left) + self.size(node.right)

    def inorder(self, node):
        if node != self.nil:
            self.inorder(node.left)
            print(node.value)
            self.inorder(node.right)

    # read string from dictionary.txt and insert into red black tree
    def read_dictionary(self, file_name):
        with open(file_name, 'r') as f:
            for line in f:
                self.insert(line.strip())

def main():
    tree = RedBlackTree()
    print("Loading dictionary...")
    tree.read_dictionary("EN-US-Dictionary.txt")
    print("Loading done!")
    print("Height: " + str(tree.height(tree.root)))
    print("Size: " + str(tree.size(tree.root)))
    while True:
        fn = input("1. Search\n2. Insert\n3. Print Height\n4. Print Size\n5. Exit\n")
        if fn == "1":
            word = input("Enter word: ")
            if tree.search(word):
                print("Found")
            else:
                print("Not Found")
        elif fn == "2":
            word = input("Enter word: ")
            if tree.insert(word):
                print("Inserted", word)
                print("Updated Size: " + str(tree.size(tree.root)))
                print("Updated Height: " + str(tree.height(tree.root)))
        elif fn == "3":
            print("Height: " + str(tree.height(tree.root)))
        elif fn == "4":
            print("Size: " + str(tree.size(tree.root)))
        elif fn == "5":
            break
        else:
            print("Invalid input!")


if __name__ == "__main__":
    main()