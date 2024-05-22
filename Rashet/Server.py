from Computer import Computer


class Server(Computer):
    def __init__(self, processor, memory, disk_capacity, failure_probability, name, has_db, has_gis, has_resilience):
        super().__init__(processor, memory, disk_capacity, failure_probability)
        self.name = name
        self.has_db = has_db
        self.has_gis = has_gis
        self.has_resilience = has_resilience

    def display(self):
        print(f"Процессор: {self.processor}, Объем памяти: {self.memory}, Объем диска: {self.disk_capacity},\
         Вероятность поломки: {self.failure_probability}, Имя сервера: {self.name}, Наличие СУБД:{self.has_db},\
          Наличие ГИС:{self.has_gis}, Наличие резервированного копирования:{self.has_resilience}")
