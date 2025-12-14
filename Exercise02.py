""" Завдання 2

Реалізуйте двійковий пошук для відсортованого масиву з дробовими числами. Написана функція для двійкового пошуку повинна повертати кортеж, де першим елементом є кількість ітерацій, потрібних для знаходження елемента. Другим елементом має бути "верхня межа" — це найменший елемент, який є більшим або рівним заданому значенню. """


def binary_search(arr, x):
    low = 0
    high = len(arr)-1
    mid = 0
    iterations = 0
    upper = None

    while low <= high:
        mid = (high + low) // 2
        iterations += 1              # Count steps

        if arr[mid] >= x:
            upper = arr[mid]         # верхня межа
            high = mid - 1
        else:
            low = mid + 1

    return iterations, upper


arr = [2.3, 3.2, 4.1, 10.5, 40.12, 45.12, 47.01]
xs = [10.1, 30.2, 3, 48, 43, 40]

for i in xs:
    iters, upper = binary_search(arr, i)
    print(f" x = {i} -> number of iterations = {iters}, upper bound = {upper}")
