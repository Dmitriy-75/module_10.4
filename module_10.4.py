# Задача "Потоки гостей в кафе":

import random
from threading import Thread
from time import sleep
from queue import Queue


# Класс Table:
# Объекты этого класса должны создаваться следующим способом - Table(1)
# Обладать атрибутами number - номер стола и guest - гость, который сидит за этим столом (по умолчанию None)

class Table():
    def __init__(self, number):
        self.number = number
        self.guest = None

# Класс Guest:
# Должен наследоваться от класса Thread (быть потоком).
# Объекты этого класса должны создаваться следующим способом - Guest('Vasya').
# Обладать атрибутом name - имя гостя.
# Обладать методом run, где происходит ожидание случайным образом от 3 до 10 секунд.
class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        pause = random.randint(3, 10)
        sleep(pause)

# Класс Cafe:
# Объекты этого класса должны создаваться следующим способом - Cafe(Table(1), Table(2),....)
# Обладать атрибутами queue - очередь (объект класса Queue) и tables - столы в этом кафе (любая коллекция).
# Обладать методами guest_arrival (прибытие гостей) и discuss_guests (обслужить гостей).


class Cafe:
    list_thr_guest = []

    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = list(tables)

    def guest_arrival(self, *guests):
        list_guests = list(guests)
        list_tables = self.tables
        len_list_guests = len(list_guests)

        for i in range(min(len_list_guests, len(self.tables))):
            list_tables[i].guest = guests[i]
            thr_quest = guests[i]
            thr_quest.start()
            Cafe.list_thr_guest.append(thr_quest)
            print(f'{list_guests[i].name} сел(-а) за стол номер {list_tables[i].number}')
        if len_list_guests > min(len_list_guests, len(self.tables)):
            for i in range(min(len_list_guests, len(self.tables)), len_list_guests):
                self.queue.put(guests[i])
                print(f'{list_guests[i].name} в очереди')

    def discuss_guests(self):
        while not (self.queue.empty()) or Cafe.check_table(self):
            for table in self.tables:
                if not (table.guest is None) and not (table.guest.is_alive()):
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest = None
                if (not (self.queue.empty())) and table.guest is None:
                    table.guest = self.queue.get()
                    print(f'{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                    thr_quest = table.guest
                    thr_quest.start()
                    Cafe.list_thr_guest.append(thr_quest)

    def check_table(self):
        for table in self.tables:
            if table.guest is not None:
                return True
        return False


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
# cafe.guest_arrival(*guests)
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
for thr in Cafe.list_thr_guest:
    thr.join()