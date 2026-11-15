from typing import List, Dict


def rod_cutting_memo(length: int, prices: List[int], cut_cost: float = 1.5) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через мемоїзацію (Top-Down)
    з урахуванням фіксованої вартості розрізу C = 1.5 (Варіант 1).
    """
    if length <= 0 or not prices or len(prices) != length or any(p <= 0 for p in prices):
        raise ValueError("Некоректні вхідні дані")

    memo = {}

    def helper(n: int):
        if n == 0:
            return 0.0, []
        if n in memo:
            return memo[n]

        max_val = float("-inf")
        best_cuts = []

        for i in range(1, n + 1):
            rem_profit, rem_cuts = helper(n - i)
            # Якщо i < n, виконується розріз, який коштує cut_cost
            current_cut_cost = cut_cost if i < n else 0.0
            current_profit = prices[i - 1] - current_cut_cost + rem_profit

            if current_profit > max_val:
                max_val = current_profit
                best_cuts = [i] + rem_cuts

        memo[n] = (max_val, best_cuts)
        return memo[n]

    max_profit, cuts = helper(length)
    return {
        "max_profit": round(max_profit, 2),
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1 if cuts else 0
    }


def rod_cutting_table(length: int, prices: List[int], cut_cost: float = 1.5) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію (Bottom-Up)
    з урахуванням фіксованої вартості розрізу C = 1.5 (Варіант 1).
    """
    if length <= 0 or not prices or len(prices) != length or any(p <= 0 for p in prices):
        raise ValueError("Некоректні вхідні дані")

    dp = [0.0] * (length + 1)
    first_cut = [0] * (length + 1)

    for j in range(1, length + 1):
        max_val = float("-inf")
        for i in range(1, j + 1):
            # Розріз потрібен лише якщо відрізаємо частину меншу за поточну довжину j
            current_cut_cost = cut_cost if i < j else 0.0
            current_profit = prices[i - 1] - current_cut_cost + dp[j - i]

            if current_profit > max_val:
                max_val = current_profit
                first_cut[j] = i
        dp[j] = max_val

    cuts = []
    n = length
    while n > 0:
        cuts.append(first_cut[n])
        n -= first_cut[n]

    cuts.reverse()

    return {
        "max_profit": round(dp[length], 2),
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1 if cuts else 0
    }


def run_tests():
    """Функція для запуску всіх тестів"""
    test_cases = [
        # Тест 1: Базовий випадок (без вартості розрізу прибуток 12 за [2,2,1],
        # з C=1.5 два розрізи коштують 3.0 -> чистий прибуток 9.0, а цілий стрижень дає 10.0)
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Базовий випадок (вигідніше не різати через вартість C=1.5)"
        },
        # Тест 2: Випадок, де розріз вигідний навіть зі штрафом C=1.5
        {
            "length": 4,
            "prices": [1, 6, 7, 9],
            "name": "Вигідний розріз попри C=1.5 (6 + 6 - 1.5 = 10.5 > 9)"
        },
        # Тест 3: Всі розрізи по 1
        {
            "length": 4,
            "prices": [4, 5, 6, 7],
            "name": "Рівномірні розрізи (4*4 - 3*1.5 = 11.5 > 7)"
        }
    ]

    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\nРезультат мемоїзації:")
        print(f"Максимальний чистий прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\nРезультат табуляції:")
        print(f"Максимальний чистий прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        assert memo_result["max_profit"] == table_result["max_profit"]
        print("\nПеревірка пройшла успішно!")


if __name__ == "__main__":
    run_tests()