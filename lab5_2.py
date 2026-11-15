from typing import List, Dict
from dataclasses import dataclass
from itertools import combinations


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера.
    Варіант 1: У межах однієї групи пріоритету першою формується та друкується
    партія, яка максимізує сукупний об'єм використаного простору.
    """
    jobs = [PrintJob(**job) for job in print_jobs]
    printer = PrinterConstraints(**constraints)

    # Групуємо завдання за пріоритетами (1 - найвищий, 3 - найнижчий)
    priorities = sorted({job.priority for job in jobs})

    print_order = []
    total_time = 0

    for priority in priorities:
        remaining_jobs = [job for job in jobs if job.priority == priority]
        priority_batches = []

        while remaining_jobs:
            best_combo = None
            best_volume = -1.0

            # Перебираємо допустимі розміри партії від 1 до max_items
            max_k = min(printer.max_items, len(remaining_jobs))
            for k in range(1, max_k + 1):
                for combo in combinations(remaining_jobs, k):
                    combo_volume = sum(item.volume for item in combo)
                    if combo_volume <= printer.max_volume and combo_volume > best_volume:
                        best_volume = combo_volume
                        best_combo = combo

            # Захист на випадок, якщо окрема модель перевищує max_volume
            if best_combo is None:
                best_combo = (remaining_jobs[0],)
                best_volume = remaining_jobs[0].volume

            priority_batches.append((best_volume, best_combo))

            # Видаляємо вибрані завдання з пулу поточного пріоритету
            selected_ids = {item.id for item in best_combo}
            remaining_jobs = [job for job in remaining_jobs if job.id not in selected_ids]

        # Сортуємо партії одного пріоритету за спаданням сумарного об'єму
        priority_batches.sort(key=lambda x: x[0], reverse=True)

        for _, batch in priority_batches:
            total_time += max(item.print_time for item in batch)
            print_order.extend(item.id for item in batch)

    return {
        "print_order": print_order,
        "total_time": total_time
    }


def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету (M2 + M3 = 270 см³ > M1 + M2 = 250 см³)
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},   # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}   # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму (кожна модель друкується окремо;
    # у межах пріоритету 1: M1 (250) іде перед M2 (200))
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет — пріоритет партії з найбільшим об'ємом):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()