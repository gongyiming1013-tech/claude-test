# Python OOP Coding Guidelines

## Language
- Use **Python** as the primary language.
- All comments, docstrings, and documentation must be in **English**.

## Naming & Style (PEP8)
- Class names: `PascalCase` (e.g., `LRUCache`, `FileParser`)
- Methods / functions / variables: `snake_case` (e.g., `get_value`, `max_size`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_CAPACITY`)
- Private members: prefix with `_` (e.g., `self._cache`, `def _evict()`)

## Type Hints
All method signatures must include type hints.
```python
def get(self, key: str) -> Optional[int]:
def put(self, key: str, value: int) -> None:
```

## Class Structure
Organize every class in this order:
1. Class docstring
2. `__init__`
3. Public methods
4. Private helpers

```python
class MyClass:
    """One-line summary of what this class does."""

    def __init__(self, ...):
        ...

    # --- Public API ---
    def public_method(self) -> None:
        ...

    # --- Private Helpers ---
    def _helper(self) -> None:
        ...
```

## OOP / OOD Principles

### Design Flow (TDD)
Always follow this order:
1. Define abstract class / interface first
2. Write test cases against the interface
3. Then implement concrete classes to pass the tests

```python
from abc import ABC, abstractmethod

class Cache(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[int]:
        pass

    @abstractmethod
    def put(self, key: str, value: int) -> None:
        pass

class LRUCache(Cache):
    def get(self, key: str) -> Optional[int]:
        ...
```

### SOLID Principles
Follow SOLID, but do NOT over-engineer:
- **S — Single Responsibility**: One class, one job.
- **O — Open/Closed**: Add new behavior via new classes, not by modifying existing ones.
- **L — Liskov Substitution**: Subclasses must be drop-in replacements for their parent.
- **I — Interface Segregation**: Keep interfaces small and focused.
- **D — Dependency Inversion**: Depend on abstractions, inject concrete implementations.

### Encapsulation
- Expose the minimum public API necessary.
- All internal state and helpers must be private (`_`-prefixed).
- Each class should have a single, clear responsibility.

## Error Handling
- Define a base custom exception per domain, with specific subclasses.
- Put boundary checks at the top of methods (guard clause pattern).
- Do NOT overuse try/except — only catch where recovery is possible.

```python
class CacheError(Exception):
    """Base exception for cache operations."""
    pass

class KeyNotFoundError(CacheError):
    pass

def get(self, key: str) -> int:
    if key not in self._store:
        raise KeyNotFoundError(f"Key '{key}' not found.")
    ...
```

## Design Patterns
Keep it simple. Only use these common patterns when appropriate:
- **Strategy** — swappable algorithms
- **Observer** — event notification
- **Factory Method** — conditional object creation
- **Singleton** — global unique instance
- **Iterator** — custom traversal via `__iter__`

Do NOT use complex patterns (Builder, Abstract Factory, nested Decorators)
unless the problem explicitly requires them.

## Comments & Docstrings
- Every class and public method must have a docstring.
- Inline comments explain **why**, not **what**.
- Do not over-comment obvious code.

```python
class LRUCache(Cache):
    """
    Least Recently Used cache with O(1) get/put.

    Uses a doubly linked list + hash map for fast access and eviction.
    """

    def get(self, key: str) -> Optional[int]:
        """Retrieve value by key. Returns None if not found."""
        # Move to head since this is the most recently accessed
        ...
```

## Testing & Coverage
- Use `pytest` as the test framework with `pytest-cov` for coverage monitoring.
- **Minimum test coverage: 95%.** Tests will fail if coverage drops below this threshold.
- Run tests with: `python -m pytest` (coverage is configured automatically via `pytest.ini`).
- Every public class and method must have corresponding test cases.

## General Rules
- Prefer clarity over cleverness.
- Keep each class and method concise and focused.
- When proposing a solution, briefly explain the design rationale.
