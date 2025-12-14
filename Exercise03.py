""" Завдання 3

Порівняйте ефективність алгоритмів пошуку підрядка: Боєра-Мура, Кнута-Морріса-Пратта та Рабіна-Карпа на основі двох текстових файлів (стаття 1, стаття 2). Використовуючи timeit, треба виміряти час виконання кожного алгоритму для двох видів підрядків: одного, що дійсно існує в тексті, та іншого — вигаданого (вибір підрядків за вашим бажанням). На основі отриманих даних визначте найшвидший алгоритм для кожного тексту окремо та в цілому. """

import timeit
import statistics
import matplotlib.pyplot as plt


###### Algorithms

###### Boyer Moore
def build_shift_table(pattern):
    table = {}
    length = len(pattern)

    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text: str, pattern: str) -> int:
    if pattern == "":
        return 0
    if len(pattern) > len(text):
        return -1

    shift_table = build_shift_table(pattern)
    m = len(pattern)
    n = len(text)

    i = 0
    while i <= n - m:
        j = m - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i  # found

        # shift using the "bad character" rule
        i += shift_table.get(text[i + m - 1], m)

    return -1  # not found

###### Knut-Morris-Pratt 
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено


###### Rabin-Karp
def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)
    
    # Базове число для хешування та модуль
    base = 256 
    modulus = 101  
    
    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    
    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

# ===================== timemeasure, open file, plot =====================

def measure_time_search(search_func, text: str, pattern: str, repeats: int = 7) -> float:
    times = []
    for _ in range(repeats):
        start = timeit.default_timer()
        search_func(text, pattern)
        times.append(timeit.default_timer() - start)
    return statistics.median(times)


def reading_text_file(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def summarize_for_plot(algorithms: dict, text: str, phrases: list[str], repeats: int = 7):
    """
    Returns:
      summary = {
        algo_name: {
          "found_time": [...],
          "not_found_time": [...],
          "found_med": float or None,
          "not_found_med": float or None,
          "found_count": int,
          "not_found_count": int,
        }, ...
      }
    """
    summary = {}

    for algo_name, func in algorithms.items():
        found_times = []
        not_found_times = []

        for phrase in phrases:
            idx = func(text, phrase)
            t = measure_time_search(func, text, phrase, repeats=repeats)

            if idx != -1:
                found_times.append(t)
            else:
                not_found_times.append(t)

        summary[algo_name] = {
            "found_times": found_times,
            "not_found_times": not_found_times,
            "found_med": statistics.median(found_times) if found_times else None,
            "not_found_med": statistics.median(not_found_times) if not_found_times else None,
            "found_count": len(found_times),
            "not_found_count": len(not_found_times),
        }

    return summary


def plot_summary(summary: dict, title: str):
    algos = list(summary.keys())

    found_vals = [(summary[a]["found_med"] or 0.0) for a in algos]
    not_found_vals = [(summary[a]["not_found_med"] or 0.0) for a in algos]

    x = list(range(len(algos)))
    width = 0.35

    plt.figure()
    plt.bar([i - width/2 for i in x], found_vals, width, label="Found (median)")
    plt.bar([i + width/2 for i in x], not_found_vals, width, label="Not found (median)")

    plt.xticks(x, algos, rotation=20, ha="right")
    plt.ylabel("Time (seconds)")
    plt.title(title)
    plt.legend()
    plt.tight_layout()

    # Optional: show found/not_found counts above each algorithm
    for i, a in enumerate(algos):
        fc = summary[a]["found_count"]
        nfc = summary[a]["not_found_count"]
        y = max(found_vals[i], not_found_vals[i])
        plt.text(i, y, f"F:{fc} / NF:{nfc}", ha="center", va="bottom")

    plt.show()


# ===================== Main =====================

def main():
    algorithms = {
        "Boyer Moore": boyer_moore_search,
        "Knuth–Morris–Pratt": kmp_search,
        "Rabin Karp": rabin_karp_search,
    }

    search_phrases = [
        "AMD Ryzen 5 3600",
        "Бінарні діаграми рішень (BDD)",
        "elementToSearch",
        "Ознаки того, що задачу можливо вирішити",
        "int pos = startIndex + (((lastIndex-startIndex) / (integers[lastIndex]-integers[startIndex]))*(elementToSearch - integers[startIndex]))",
        "https://uk.wikipedia.org/wiki/GPGPU",
        "https",
    ]

    # Put your real filenames here
    text1 = reading_text_file("article01.txt")
    text2 = reading_text_file("article02.txt")

    # Build summaries (per text)
    summary1 = summarize_for_plot(algorithms, text1, search_phrases, repeats=7)
    summary2 = summarize_for_plot(algorithms, text2, search_phrases, repeats=7)

    # Plot two graphs: one per text file
    plot_summary(summary1, "Article 1: substring search time (median) + found status")
    plot_summary(summary2, "Article 2: substring search time (median) + found status")

    # (Optional) print fastest per text in each category
    def fastest(summary, key):
        # key in {"found_med", "not_found_med"}
        candidates = [(a, summary[a][key]) for a in summary if summary[a][key] is not None]
        return min(candidates, key=lambda x: x[1])[0] if candidates else None

    print("Article 1 fastest (FOUND):", fastest(summary1, "found_med"))
    print("Article 1 fastest (NOT FOUND):", fastest(summary1, "not_found_med"))
    print("Article 2 fastest (FOUND):", fastest(summary2, "found_med"))
    print("Article 2 fastest (NOT FOUND):", fastest(summary2, "not_found_med"))


if __name__ == "__main__":
    main()