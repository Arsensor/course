import random
import string
import time
import tkinter as tk
from tkinter import scrolledtext
from Workstation import Workstation
from Server import Server
from User import User
from ComputerClass import ComputerClass


class NetworkSimulation:
    def __init__(self, stats):
        self.stats = stats
        self.computer_classes = []
        self.users = []
        self.is_running = False

    def generate_user(self):
        username = ''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 8)))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(8, 12)))
        needs_resolution = random.choice([100, 300, 500, 1000])
        needs_dbms = random.choice([True, False])
        needs_gis = random.choice([True, False])
        return User(username, password, needs_resolution, needs_dbms, needs_gis)

    def generate_workstations(self):
        workstations = []
        for i in range(random.randint(1, 6)):
            processor = random.choice(["Intel", "Amd"])
            memory = random.choice([1000, 1500, 2000, 4000])
            disk_capacity = random.choice([0.5, 1, 1.5, 2])
            failure_probability = random.choice([0.001, 0.02, 0.05, 0.3])
            display_resolution = random.choice([480, 720, 1240, 1920])
            workstations.append(Workstation(processor, memory, disk_capacity, failure_probability, display_resolution))
        return workstations

    def generate_servers(self):
        servers = []
        processor = random.choice(["Intel", "Amd"])
        memory = random.choice([1000, 1500, 2000, 4000])
        disk_capacity = random.choice([0.5, 1, 1.5, 2])
        failure_probability = random.choice([0.0001, 0.002, 0.05, 0.3])
        name = ''.join(random.choices(string.ascii_uppercase, k=4))
        has_db = random.choice([True, False])
        has_gis = random.choice([True, False])
        has_resilience = random.choice([True, False])
        servers.append(
            Server(processor, memory, disk_capacity, failure_probability, name, has_db, has_gis, has_resilience))
        return servers

    def generate_computer_class(self):
        name = ''.join(random.choices(string.ascii_uppercase, k=5))
        workstations = self.generate_workstations()
        servers = self.generate_servers()
        return ComputerClass(name, workstations, servers)

    def search_workstation(self, user):
        for computer_class in self.computer_classes:
            for server in computer_class.servers:
                if server.is_working and server.has_db >= user.needs_db and server.has_gis >= user.needs_gis:
                    for workstation in computer_class.workstations:
                        if workstation.is_working and workstation.display_resolution >= user.needs_resolution and not workstation.user:
                            return workstation
        return None

    def simulate(self, output_text):
        self.is_running = True
        for i in range(random.randint(10, 20)):
            computer_class = self.generate_computer_class()
            output_text.insert(tk.END, f"Новый компьютерный класс: {computer_class.name}\n")
            self.computer_classes.append(computer_class)
        while self.is_running:
            user = self.generate_user()
            output_text.insert(tk.END, f"Новый пользователь: {user.username}, Пароль: {user.password}\n")
            self.users.append(user)

            output_text.see(tk.END)
            window.update()

            for computer_class in self.computer_classes:
                for server in computer_class.servers:
                    if server.is_working and server.is_broken():
                        server.is_working = False
                        output_text.insert(tk.END, f"{server.name} сервер отключен\n")
                        output_text.see(tk.END)
                        window.update()
                        if server.has_resilience:
                            stats[0] += 1
                        break
                    if not server.is_working and server.chanse_to_working():
                        server.is_working = True
                        output_text.insert(tk.END, f"{server.name} сервер подключен\n")
                        output_text.see(tk.END)
                        window.update()
                        break

            for user in self.users:
                user.spent_time += 1
                stats[1].append(user.spent_time)
                if user.workstation:
                    if random.random() > 0.975:
                        workstation = user.workstation
                        workstation.user = None
                        output_text.insert(tk.END, f"Пользователь {user.username} покинул место\n")
                        output_text.see(tk.END)
                        window.update()
                    else:
                        workstation = user.workstation
                        is_broken = workstation.is_broken()
                        if is_broken:
                            workstation.user = None
                            user.workstation = None
                            output_text.insert(tk.END, f"У пользователя {user.username} сломалась рабочая станция\n")
                            user.attemps += 1
                            output_text.see(tk.END)
                            window.update()
                else:
                    workstation = self.search_workstation(user)
                    if workstation:
                        user.workstation = workstation
                        workstation.user = user
                        output_text.insert(tk.END, f"Пользователь {user.username} за рабочей станцией\n")
                        output_text.see(tk.END)
                        window.update()
                    else:
                        user.attemps += 1
                        stats[2] += 1
                        if user.attemps == 3:
                            self.users.remove(user)
                            output_text.insert(tk.END,
                                               f"Пользователь {user.username} покинул место. Не нашел рабочую станцию\n")
                            output_text.see(tk.END)
                            window.update()
                        else:
                            if user.needs_db:
                                stats[3] += 1
                            if user.needs_gis:
                                stats[4] += 1
                            self.users.remove(user)
                            output_text.insert(tk.END,
                                               f"Для пользователя {user.username} - нет подходящих рабочих станций\n")
                            output_text.see(tk.END)
                            window.update()
            output_text.insert(tk.END, "\n" * 1)
            output_text.see(tk.END)
            window.update()
            time.sleep(2.5)

    def stop_simulation(self):
        self.is_running = False

    def workstations_count(self):
        count_all = 0
        with_db = 0
        with_gis = 0
        with_resolution = 0
        working = 0

        for computer_class in self.computer_classes:
            count_all += len(computer_class.workstations)

        for computer_class in self.computer_classes:
            for server in computer_class.servers:
                if server.has_db:
                    with_db += len(computer_class.workstations)
                    break
        for computer_class in self.computer_classes:
            for server in computer_class.servers:
                if server.has_gis:
                    with_gis += len(computer_class.workstations)
                    break
        for computer_class in self.computer_classes:
            for workstation in computer_class.workstations:
                if workstation.display_resolution:
                    with_resolution += len(computer_class.workstations)
                    break

        for computer_class in self.computer_classes:
            for workstation in computer_class.workstations:
                if not workstation.is_broken():
                    working += 1

        broken_workstations = count_all - working
        return count_all, with_db, with_gis, with_resolution, working, broken_workstations

    def servers_count(self):
        all_servers = []
        servers_with_db = []
        servers_with_gis = []
        broken_servers = []
        for computer_class in self.computer_classes:
            for server in computer_class.servers:
                if server not in all_servers:
                    all_servers.append(server)
                if server.is_broken() and server not in broken_servers:
                    broken_servers.append(server)

        for computer_class in self.computer_classes:
            for server in computer_class.servers:
                if server.has_db and server not in servers_with_db:
                    servers_with_db.append(server)
                    break

        for computer_class in self.computer_classes:
            for server in computer_class.servers:
                if server.has_gis and server not in servers_with_gis:
                    servers_with_gis.append(server)
                    break

        return len(all_servers), len(servers_with_db), len(servers_with_gis), len(broken_servers)

    def show_stat(self):
        server_stats = self.servers_count()
        workstation_stats = self.workstations_count()
        output_text.insert(tk.END, "\n" * 3)
        output_text.insert(tk.END, f"Рабочих станций - {workstation_stats[0]}\n")
        output_text.insert(tk.END, f"Рабочих станций с разрешением - {workstation_stats[3]}\n")
        output_text.insert(tk.END, f"Рабочих станций с СУБД - {workstation_stats[1]}\n")
        output_text.insert(tk.END, f"Рабочих станций с ГИС - {workstation_stats[2]}\n")
        output_text.insert(tk.END, f"Исправных рабочих станций - {workstation_stats[4]}\n")
        output_text.insert(tk.END, f"Серверов - {server_stats[0]}\n")
        output_text.insert(tk.END, f"Серверов с СУБД - {server_stats[1]}\n")
        output_text.insert(tk.END, f"Серверов с ГИС - {server_stats[2]}\n")
        output_text.insert(tk.END, f"Сломанных компьютеров - {server_stats[3] + workstation_stats[5]}\n")
        output_text.insert(tk.END, f"Сломанных рабочих станций - {workstation_stats[5]}\n")
        output_text.insert(tk.END, f"Сломанных серверов - {server_stats[3]}\n")
        output_text.insert(tk.END, f"Серверов с резервированием, которые вышли из строя один раз - {stats[0]}\n")
        output_text.insert(tk.END, f"Время работы пользователей - {sum(stats[1])}\n")
        output_text.insert(tk.END, f"Среднее время работы пользователей - {round(sum(stats[1]) / len(stats[1]))}\n")
        output_text.insert(tk.END, f"Попытки пользователей пересесть - {stats[2]}\n")
        output_text.insert(tk.END, f"Попытки пользователей пересесть с требованием СУБД - {stats[3]}\n")
        output_text.insert(tk.END, f"Попытки пользователей пересесть с требованием ГИС - {stats[4]}\n")
        output_text.insert(tk.END, "\n" * 3)
        output_text.see(tk.END)
        window.update()


def start_simulation():
    simulation_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    network.simulate(output_text)


def stop_simulation():
    network.stop_simulation()
    simulation_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)


def show_stats():
    network.show_stat()


stats = [0, [], 0, 0, 0]
network = NetworkSimulation(stats)

window = tk.Tk()
window.title("Компьютерные классы")

output_text = scrolledtext.ScrolledText(window, width=100, height=25)
output_text.pack(pady=10)

simulation_button = tk.Button(window, text="Запустить симуляцию", command=start_simulation)
simulation_button.pack()

stop_button = tk.Button(window, text="Остановить симуляцию", command=stop_simulation, state=tk.DISABLED)
stop_button.pack()

show_stats = tk.Button(window, text="Показать статистику", command=show_stats)
show_stats.pack()

window.mainloop()