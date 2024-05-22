from Computer import Computer


class Workstation(Computer):
    def __init__(self, processor, memory, disk_capacity, failure_probability, display_resolution):
        super().__init__(processor, memory, disk_capacity, failure_probability)
        self.display_resolution = display_resolution
        self.user = None

    def display(self):
        print(f"Процессор: {self.processor}, Объем памяти: {self.memory}, Объем диска: {self.disk_capacity},\
         Вероятность поломки: {self.failure_probability}, Разрешение экрана: {self.display_resolution}")

