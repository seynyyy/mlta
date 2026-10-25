def get_min_coins():
    n = int(input("Введіть суму n (n <= 1000): "))
    
    coins = [1, 2, 3, 5]
    # Ініціалізуємо масив значеннями, більшими за максимально можливе
    dp = [n + 1] * (n + 1)
    dp[0] = 0
    
    for i in range(1, n + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
                
    print(f"Мінімальна кількість монет: {dp[n]}")


def decimal_to_binary():
    n = int(input("Введіть число n (1 <= n <= 10000): "))
    
    if n == 0:
        print("Двійкове представлення: 0")
        return
        
    # Знаходимо максимальний показник ступеня двійки, що не перевищує n
    k = 0
    while (2 ** (k + 1)) <= n:
        k += 1
        
    binary_representation = []
    
    # Жадібно формуємо число
    for i in range(k, -1, -1):
        power = 2 ** i
        if n >= power:
            binary_representation.append("1")
            n -= power
        else:
            binary_representation.append("0")
            
    print(f"Двійкове представлення: {''.join(binary_representation)}")

if __name__ == "__main__":
    get_min_coins()
    decimal_to_binary()