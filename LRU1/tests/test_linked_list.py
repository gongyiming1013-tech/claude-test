"""Tests for _Node and _DoublyLinkedList."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from linked_list import _Node, _DoublyLinkedList
from exceptions import CacheError


class TestNode:
    """Tests for the _Node data holder."""

    def test_create_node(self) -> None:
        node = _Node("key1", 100)
        assert node.key == "key1"
        assert node.value == 100
        assert node.prev is None
        assert node.next is None

    def test_node_repr(self) -> None:
        node = _Node("x", 42)
        result = repr(node)
        assert "x" in result
        assert "42" in result


class TestDoublyLinkedList:
    """Tests for the _DoublyLinkedList container."""

    def test_empty_list(self) -> None:
        dll = _DoublyLinkedList()
        assert dll.size == 0

    def test_add_to_front_single(self) -> None:
        dll = _DoublyLinkedList()
        node = _Node("a", 1)
        dll.add_to_front(node)
        assert dll.size == 1

    def test_add_to_front_multiple_preserves_order(self) -> None:
        """Most recently added node should be at the front."""
        dll = _DoublyLinkedList()
        node_a = _Node("a", 1)
        node_b = _Node("b", 2)
        node_c = _Node("c", 3)
        dll.add_to_front(node_a)
        dll.add_to_front(node_b)
        dll.add_to_front(node_c)
        assert dll.size == 3
        # Removing from the back should return the earliest added node
        removed = dll.remove_last()
        assert removed.key == "a"

    def test_remove_node(self) -> None:
        dll = _DoublyLinkedList()
        node = _Node("a", 1)
        dll.add_to_front(node)
        dll.remove(node)
        assert dll.size == 0

    def test_remove_middle_node(self) -> None:
        """Removing a node from the middle should keep the list connected."""
        dll = _DoublyLinkedList()
        node_a = _Node("a", 1)
        node_b = _Node("b", 2)
        node_c = _Node("c", 3)
        dll.add_to_front(node_a)
        dll.add_to_front(node_b)
        dll.add_to_front(node_c)
        dll.remove(node_b)
        assert dll.size == 2
        # Remaining order: c (front) -> a (back)
        removed = dll.remove_last()
        assert removed.key == "a"

    def test_move_to_front(self) -> None:
        """Moving a node to front should make it the most recent."""
        dll = _DoublyLinkedList()
        node_a = _Node("a", 1)
        node_b = _Node("b", 2)
        node_c = _Node("c", 3)
        dll.add_to_front(node_a)
        dll.add_to_front(node_b)
        dll.add_to_front(node_c)
        # Current order: c -> b -> a
        # Move 'a' to front
        dll.move_to_front(node_a)
        # Now order: a -> c -> b
        removed = dll.remove_last()
        assert removed.key == "b"

    def test_remove_last(self) -> None:
        dll = _DoublyLinkedList()
        node_a = _Node("a", 1)
        node_b = _Node("b", 2)
        dll.add_to_front(node_a)
        dll.add_to_front(node_b)
        removed = dll.remove_last()
        assert removed.key == "a"
        assert dll.size == 1

    def test_remove_last_from_empty_list_raises(self) -> None:
        dll = _DoublyLinkedList()
        with pytest.raises(CacheError):
            dll.remove_last()

    def test_clear(self) -> None:
        dll = _DoublyLinkedList()
        for i in range(5):
            dll.add_to_front(_Node(f"key{i}", i))
        assert dll.size == 5
        dll.clear()
        assert dll.size == 0

    def test_repr_empty(self) -> None:
        dll = _DoublyLinkedList()
        assert "[]" in repr(dll)

    def test_repr_with_nodes(self) -> None:
        dll = _DoublyLinkedList()
        dll.add_to_front(_Node("a", 1))
        dll.add_to_front(_Node("b", 2))
        result = repr(dll)
        assert "b" in result
        assert "a" in result
