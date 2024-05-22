class User:
    def __init__(self, username, password, needs_resolution, needs_db, needs_gis):
        self.username = username
        self.password = password
        self.needs_resolution = needs_resolution
        self.needs_db = needs_db
        self.needs_gis = needs_gis
        self.workstation = None
        self.spent_time = 0
        self.attemps = 0

    def display(self):
        print(f"Процессор: {self.username}, Объем памяти: {self.password}, Объем диска: {self.needs_resolution},\
         Вероятность поломки: {self.needs_db}, Потребность СУБД: {self.needs_gis}, Работает за рабочей станцией\
         :{self.workstation}, Рабочее время: {self.spent_time}, Пытался пересесть: {self.attemps}")
