def generate_sequence(n: int) -> str:
    """
    Генерирует последовательность 122333444455555...
    где каждое число повторяется столько раз, чему оно равно
    """
    result = []
    current_number = 1

    while len(result) < n:
        # Добавляем текущее число current_number раз
        for _ in range(current_number):
            result.append(str(current_number))
            if len(result) == n:
                break
        current_number += 1

    return ''.join(result)


def main():
    # Тестовые примеры
    test_cases = [1, 5, 10, 15, 20]

    for n in test_cases:
        sequence = generate_sequence(n)
        print(f"n={n}: {sequence}")

    # Интерактивный режим
    print("\n" + "=" * 50)
    while True:
        try:
            user_input = input("\nВведите количество элементов (или 'q' для выхода): ")
            if user_input.lower() == 'q':
                break

            n = int(user_input)
            if n <= 0:
                print("Число должно быть положительным!")
                continue

            sequence = generate_sequence(n)
            print(f"Первые {n} элементов: {sequence}")

        except ValueError:
            print("Пожалуйста, введите целое число!")


if __name__ == "__main__":
    main()
