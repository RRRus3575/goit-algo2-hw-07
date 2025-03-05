from functools import lru_cache
import timeit
import matplotlib.pyplot as plt

# --- Реалізація Splay Tree ---
class Node:
    def __init__(self, key, value, parent=None):
        self.key = key 
        self.value = value  
        self.parent = parent
        self.left_node = None
        self.right_node = None

class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        """Вставка нового значення в кеш"""
        if self.root is None:
            self.root = Node(key, value)
        else:
            self._insert_node(key, value, self.root)

    def _insert_node(self, key, value, current_node):
        if key < current_node.key:
            if current_node.left_node:
                self._insert_node(key, value, current_node.left_node)
            else:
                current_node.left_node = Node(key, value, current_node)
                self._splay(current_node.left_node)
        else:
            if current_node.right_node:
                self._insert_node(key, value, current_node.right_node)
            else:
                current_node.right_node = Node(key, value, current_node)
                self._splay(current_node.right_node)

    def find(self, key):
        """Пошук числа Фібоначчі в кеші"""
        node = self.root
        while node is not None:
            if key < node.key:
                node = node.left_node
            elif key > node.key:
                node = node.right_node
            else:
                self._splay(node)  
                return node.value
        return None  

    def _splay(self, node):
        """Переміщення вузла до кореня"""
        while node.parent is not None:
            if node.parent.parent is None:  # Zig-ситуація
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif node == node.parent.left_node and node.parent == node.parent.parent.left_node:  # Zig-Zig
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif node == node.parent.right_node and node.parent == node.parent.parent.right_node:  # Zig-Zig
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else:  # Zig-Zag
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_right(self, node):
        left_child = node.left_node
        if left_child is None:
            return
        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left_node:
            node.parent.left_node = left_child
        else:
            node.parent.right_node = left_child
        left_child.right_node = node
        node.parent = left_child

    def _rotate_left(self, node):
        right_child = node.right_node
        if right_child is None:
            return
        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child
        right_child.left_node = node
        node.parent = right_child


# --- Функції для обчислення Фібоначчі ---
fib_cache = SplayTree()

@lru_cache(maxsize=1000)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

def fibonacci_splay(n, tree):
    if n <= 1:
        return n
    cached_value = tree.find(n)
    if cached_value is not None:
        return cached_value  

    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)  
    return result


# --- Вимірювання часу ---
n_values = list(range(0, 951, 50))
times_lru = []
times_splay = []

for n in n_values:
    time_lru = timeit.timeit(lambda: fibonacci_lru(n), number=5)
    time_splay = timeit.timeit(lambda: fibonacci_splay(n, fib_cache), number=5)
    times_lru.append(time_lru)
    times_splay.append(time_splay)

# --- Вивід таблиці ---
print(f"{'n':<10}{'LRU Cache Time (s)':<25}{'Splay Tree Time (s)':<25}")
print("-" * 60)
for i in range(len(n_values)):
    print(f"{n_values[i]:<10}{times_lru[i]:<25.10f}{times_splay[i]:<25.10f}")

# --- Побудова графіка ---
plt.figure(figsize=(10, 6))
plt.plot(n_values, times_lru, marker="o", linestyle="-", label="LRU Cache")
plt.plot(n_values, times_splay, marker="x", linestyle="-", label="Splay Tree")

plt.xlabel("Число Фібоначчі (n)")
plt.ylabel("Середній час виконання (секунди)")
plt.title("Порівняння часу виконання для LRU Cache та Splay Tree")
plt.legend()
plt.grid()

plt.show()
