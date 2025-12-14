
# Додайте метод delete для видалення пар ключ-значення таблиці # HashTable , яка реалізована в конспекті.


class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        key_hash = self.hash_function(key)
        key_value = [key, value]

        if self.table[key_hash] is None:
            self.table[key_hash] = list([key_value])
            return True
        else:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.table[key_hash].append(key_value)
            return True

    def get(self, key):
        key_hash = self.hash_function(key)
        if self.table[key_hash] is not None:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None
    
    def delete(self, key):
        index = self.hash_function(key)

        for i, pair in enumerate(self.table[index]):
            if pair[0] == key:
                del self.table[index][i]
                return True
        return False
    
    def show_state(self, title="STATE"):
        print(f"\n--- {title} ---")
        for index, bucket in enumerate(H.table):
            if bucket:
                print(f"{index}: {bucket}")
    

# Тестуємо нашу хеш-таблицю:
H = HashTable(5)
# H.insert("apple", 10)
# H.insert("orange", 20)
# H.insert("banana", 30)

# print(H.get("apple"))   # Виведе: 10
# print(H.get("orange"))  # Виведе: 20
# print(H.get("banana"))  # Виведе: 30

# H.delete("banana")
# print(H.get("banana"))  # Виведе: 30


# ---------------- TESTS ----------------
H = HashTable(5)

print("== Basic inserts ==")
H.insert("apple", 10)
H.insert("orange", 20)
H.insert("banana", 30)

assert H.get("apple") == 10
assert H.get("orange") == 20
assert H.get("banana") == 30
assert H.get("missing") is None

H.show_state("After inserts")

print("\n== Update existing key ==")
H.insert("apple", 999)
assert H.get("apple") == 999
H.show_state("After updating apple")

print("\n== Delete existing key ==")
assert H.delete("apple") is True
assert H.get("apple") is None
H.show_state("After deleting apple")

print("\n== Delete non-existing key ==")
assert H.delete("ugjhg") is False
assert H.delete("does_not_exist") is False

print("\n✅ Basic tests passed!")