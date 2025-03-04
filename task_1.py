import random
import time
from collections import OrderedDict

class LRUCache:
    """ Реалізація LRU-кешу з обмеженням у 1000 записів """
    def __init__(self, capacity=1000):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, L, R):
        """ Отримує значення з кешу, якщо воно там є """
        if (L, R) in self.cache:
            self.cache.move_to_end((L, R))  
            return self.cache[(L, R)]
        return None

    def put(self, L, R, result):
        """ Зберігає суму діапазону в кеш """
        if len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)  
        self.cache[(L, R)] = result

    def clear(self):
        """ Очищає кеш (при оновленні масиву) """
        self.cache.clear()

# Створюємо кеш
lru_cache = LRUCache()

# Розмір масиву
N = 100_000

# Генеруємо масив випадкових чисел
array = [random.randint(1, 1000) for _ in range(N)]

# Кількість запитів
Q = 50_000

# Генерація випадкових запитів (Range та Update)
queries = []
for _ in range(Q):
    if random.random() < 0.5:
        L = random.randint(0, N - 1)
        R = random.randint(L, N - 1)
        queries.append(("Range", L, R))
    else:
        index = random.randint(0, N - 1)
        value = random.randint(1, 1000)
        queries.append(("Update", index, value))

# Функція обчислення суми без кешу
def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])

# Функція оновлення масиву без кешу
def update_no_cache(array, index, value):
    array[index] = value

# Функція обчислення суми з кешем
def range_sum_with_cache(array, L, R):
    cached_result = lru_cache.get(L, R)
    if cached_result is not None:
        return cached_result 

    result = sum(array[L:R+1])  
    lru_cache.put(L, R, result)  
    return result

# Функція оновлення масиву з кешем
def update_with_cache(array, index, value):
    array[index] = value 
    keys_to_remove = [key for key in lru_cache.cache.keys() if key[0] <= index <=key[1]] 
    for key in keys_to_remove:
        del lru_cache.cache[key]

# Перед тестуванням кешу заповнюємо його першими 10 Range-запитами
for i in range(10):
    if queries[i][0] == "Range":
        range_sum_with_cache(array, queries[i][1], queries[i][2])

# Вибираємо випадкові запити для тестування
L, R = queries[0][1], queries[0][2]
index, value = queries[1][1], queries[1][2]

# Виконання запитів без кешу
start_time_no_cache = time.perf_counter()
range_sum_no_cache(array, L, R)
update_no_cache(array, index, value)
end_time_no_cache = time.perf_counter()
time_no_cache = end_time_no_cache - start_time_no_cache

# Виконання запитів з кешем
start_time_with_cache = time.perf_counter()
range_sum_with_cache(array, L, R)
update_with_cache(array, index, value)
end_time_with_cache = time.perf_counter()
time_with_cache = end_time_with_cache - start_time_with_cache

# Вивід результатів
print(f"Час виконання без кешування: {time_no_cache:.6f} секунд")
print(f"Час виконання з LRU-кешем: {time_with_cache:.6f} секунд")
