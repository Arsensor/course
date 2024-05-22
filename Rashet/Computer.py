import random
from abc import ABC, abstractmethod

class Computer(ABC):
    def __init__(self, processor, memory, disk_capacity, failure_probability):
        self.processor = processor
        self.memory = memory
        self.disk_capacity = disk_capacity
        self.failure_probability = failure_probability
        self.is_working = True

    @abstractmethod
    def display(self):
        print(f"Процессор: {self.processor}, Объем памяти: {self.memory}, Объем диска: {self.disk_capacity},\
         Вероятность поломки: {self.failure_probability}")

    def is_broken(self):
        if random.random() < self.failure_probability:
            self.is_working = False
            return True
        return False

    def chanse_to_working(self):
        if random.random() > (1 - self.failure_probability):
            self.is_working = True
            return True
        return False