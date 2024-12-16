from typing import List
import math

class Statistics:
    def __init__(self, data: List[float]):
        self.data = data

    def mean(self) -> float:
        if not self.data:
            raise ValueError("Данные пусты.")
        return sum(self.data) / len(self.data)

    def median(self) -> float:
        if not self.data:
            raise ValueError("Данные пусты.")
        sorted_data = sorted(self.data)
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2
        return sorted_data[mid]

    def variance(self) -> float:
        if len(self.data) < 2:
            raise ValueError("Для вычисления дисперсии требуется минимум два числа.")
        m = self.mean()
        return sum((x - m) ** 2 for x in self.data) / len(self.data)

    def standard_deviation(self) -> float:
        return math.sqrt(self.variance())

    def min_max(self) -> (float, float):
        if not self.data:
            raise ValueError("Данные пусты.")
        return min(self.data), max(self.data)

    def count_above(self, threshold: float) -> int:
        return sum(1 for x in self.data if x > threshold)

    def normalize(self) -> List[float]:
        if not self.data:
            raise ValueError("Данные пусты.")
        min_val, max_val = self.min_max()
        if min_val == max_val:
            raise ValueError("Все элементы одинаковы, нормализация невозможна.")
        return [(x - min_val) / (max_val - min_val) for x in self.data]

