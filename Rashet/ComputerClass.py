class ComputerClass:
    def __init__(self, name, workstations, servers):
        self.name = name
        self.workstations = workstations
        self.servers = servers

    def display(self):
        print(f"Имя компьютерного класса: {self.name}, Список рабочих станций в классе: {self.workstations},\
         Обслуживающие сервера: {self.servers}")
