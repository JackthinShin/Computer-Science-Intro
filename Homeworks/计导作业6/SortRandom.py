import random
import time

def bubble_sort(a: list):
    n = len(a)
    for i in range(n - 1):
        for j in range(0, n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]

def quick_sort(a: list, low: int, high: int):
    if low < high:
        x = random.randint(low, high)
        a[x], a[high] = a[high], a[x]
        p = a[high]
        i = low - 1
        for j in range(low, high):
            if a[j] < p:
                i += 1
                a[i], a[j] = a[j], a[i]
        a[i + 1], a[high] = a[high], a[i + 1]
        p = i + 1
        quick_sort(a, low, p - 1)
        quick_sort(a, p + 1, high)

a = [random.randint(0, 100000) for _ in range(100000)]
start = time.perf_counter()
bubble_sort(a)
end = time.perf_counter()
print(f"Bubble sort on 100000 elems: {end - start:.6f} s")

a = [random.randint(0, 100000) for _ in range(100000)]
start = time.perf_counter()
quick_sort(a, 0, len(a) - 1)
end = time.perf_counter()
print(f"Quick sort on 100000 elems: {end - start:.6f} s")
