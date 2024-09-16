from typing import Optional


class Node:
    def __init__(self, value: int):
        self.value = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None


class BinarySearchTree:
    def __init__(self):
        self.root: Optional[Node] = None

    def insert(self, value: int):
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, current_node: Node, value: int):
        if value < current_node.value:
            if current_node.left is None:
                current_node.left = Node(value)
            else:
                self._insert_recursive(current_node.left, value)
        else:
            if current_node.right is None:
                current_node.right = Node(value)
            else:
                self._insert_recursive(current_node.right, value)

    def search(self, value: int) -> bool:
        if self.root is None:
            return False
        else:
            return self._search_recursive(self.root, value)

    def _search_recursive(self, current_node: Node | None, value: int) -> bool:
        if current_node is None:
            return False
        if current_node.value == value:
            return True
        if value < current_node.value:
            return self._search_recursive(current_node.left, value)
        else:
            return self._search_recursive(current_node.right, value)

    def inorder_traversal(self) -> list[int]:
        if self.root is None:
            return []
        else:
            return self._inorder_traversal_recursive(self.root)

    def _inorder_traversal_recursive(self, current_node: Node | None) -> list[int]:
        if current_node is None:
            return []
        else:
            return (
                self._inorder_traversal_recursive(current_node.left)
                + [current_node.value]
                + self._inorder_traversal_recursive(current_node.right)
            )

    def delete(self, value: int):
        if self.root is None:
            return
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, current_node: Node | None, value: int) -> Node | None:
        if current_node is None:
            return
        if value < current_node.value:
            current_node.left = self._delete_recursive(current_node.left, value)
        elif value > current_node.value:
            current_node.right = self._delete_recursive(current_node.right, value)
        else:
            if current_node.left is None and current_node.right is None:
                return None
            elif current_node.left is None:
                return current_node.right
            elif current_node.right is None:
                return current_node.left
            else:
                min_node = self._find_min(current_node.right)
                current_node.value = min_node.value
                current_node.right = self._delete_recursive(
                    current_node.right, min_node.value
                )
        return current_node

    def _find_min(self, node: Node) -> Node:
        current = node
        while current.left is not None:
            current = current.left
        return current


if __name__ == "__main__":
    # Create a new BST
    bst = BinarySearchTree()

    # Insert some values
    values_to_insert = [5, 3, 7, 2, 4, 6, 8]
    for value in values_to_insert:
        bst.insert(value)
    print(f"Inserted values: {values_to_insert}")

    # Test in-order traversal
    print(f"In-order traversal: {bst.inorder_traversal()}")

    # Test search
    value_to_search = 4
    print(f"Searching for {value_to_search}: {bst.search(value_to_search)}")
    value_to_search = 9
    print(f"Searching for {value_to_search}: {bst.search(value_to_search)}")

    # Test deletion
    value_to_delete = 3
    print(f"Deleting {value_to_delete}")
    bst.delete(value_to_delete)
    print(f"In-order traversal after deletion: {bst.inorder_traversal()}")

    # Test deleting root
    value_to_delete = 5
    print(f"Deleting root {value_to_delete}")
    bst.delete(value_to_delete)
    print(f"In-order traversal after deleting root: {bst.inorder_traversal()}")
