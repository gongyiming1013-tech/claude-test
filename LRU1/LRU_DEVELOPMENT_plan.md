# LRU Cache — Implementation Plan

## Context
Design and implement a production-quality LRU Cache in Python with O(1) operations, following OOP/OOD best practices defined in `/Users/mgong2/claude-test/CLAUDE.md`. The project starts from an empty directory (`LRU1/`).

## Class Hierarchy

```
Exception
  └── CacheError                     (base exception)
        ├── CacheCapacityError       (invalid capacity)
        └── CacheKeyError            (key not found)

ABC
  └── Cache[K, V]                    (abstract interface)
        └── LRUCache[K, V]           (concrete implementation)

ThreadSafeCache[K, V]                (composition wrapper for concurrency)

_Node[K, V]                          (internal linked list node)
_DoublyLinkedList[K, V]              (internal linked list with sentinel nodes)
```

## File Structure

```
LRU1/
├── exceptions.py          # CacheError, CacheCapacityError, CacheKeyError
├── cache_interface.py     # Cache ABC
├── linked_list.py         # _Node, _DoublyLinkedList
├── lru_cache.py           # LRUCache
├── thread_safe_cache.py   # ThreadSafeCache (RLock wrapper)
├── __init__.py            # Public re-exports
└── tests/
    ├── __init__.py
    ├── test_linked_list.py
    ├── test_lru_cache.py
    └── test_thread_safe_cache.py
```

## Implementation Order (Test-First / TDD)

| Step | File | What | Dependencies |
|------|------|------|-------------|
| 1 | `exceptions.py` | Custom exception hierarchy | None |
| 2 | `cache_interface.py` | `Cache` ABC (interface/contract) | exceptions |
| 3 | `linked_list.py` | `_Node`, `_DoublyLinkedList` (skeleton/interface) | exceptions |
| 4 | `tests/test_linked_list.py` | **Tests first** for linked list | step 3 |
| 5 | `linked_list.py` | Implement `_DoublyLinkedList` to pass tests | step 4 |
| 6 | `tests/test_lru_cache.py` | **Tests first** for LRUCache | steps 1-2 |
| 7 | `lru_cache.py` | Implement `LRUCache` to pass tests | step 6 |
| 8 | `tests/test_thread_safe_cache.py` | **Tests first** for ThreadSafeCache | step 2 |
| 9 | `thread_safe_cache.py` | Implement `ThreadSafeCache` to pass tests | step 8 |
| 10 | `__init__.py` | Public API exports | all above |

## Key Design Decisions

1. **Interface first** — `Cache` ABC defines contract before any implementation (per CLAUDE.md)
2. **Sentinel nodes** — `_DoublyLinkedList` uses dummy head/tail to eliminate None checks
3. **Composition for thread safety** — `ThreadSafeCache` wraps any `Cache`, not inheritance
4. **RLock** — reentrant lock to prevent deadlock if methods call each other
5. **Generic types** — `Cache[K, V]` for flexibility, not locked to `str`/`int`
6. **`get` returns `Optional[V]`** — cache miss is normal, not exceptional; `delete` raises on missing key

## Core Algorithm (O(1) get/put)

**`get(key)`**: dict lookup → move node to list front → return value
**`put(key, value)`**: if exists: update + move to front; if full: evict tail; create node → add to front + dict

## Verification
- Run `python -m pytest tests/` for all unit tests
- Test scenarios: basic get/put, eviction, update, delete, clear, capacity=1, capacity validation, `__contains__`, `__len__`, thread safety
