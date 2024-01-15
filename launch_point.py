from random import random


class LaunchPoint:
    def __init__(self, position, launch_type, launch_frequency, arsenal: list):
        self.position = position
        self.launch_type = launch_type  # 'attacking' или 'defense'
        self.launch_frequency = launch_frequency
        self.arsenal = arsenal
        self.simulation = None  # should be set later
        self.time_since_last_launch = 0

        self.load_rockets()

    def load_rockets(self):
        for rocket in self.arsenal:
            rocket.set_launching_point(self)
            rocket.set_position(self.position)

    def add_simulation(self, simulation):
        self.simulation = simulation

    def launch_rocket(self):
        if self.launch_type == 'attacking':
            # Логика выбора режима запуска и параметров ракеты
            mode = self.select_launch_mode()  # Выбор режима запуска
            target, velocity, acceleration = self.calculate_launch_parameters(mode)
            # new_rocket = Rocket(position=self.position, velocity=velocity, acceleration=acceleration, rocket_type='attacking')
            new_rocket = self.arsenal.pop() if self.arsenal else None
        elif self.launch_type == 'defense':
            # # Логика определения цели и параметров ракеты ПВО
            # target = self.detect_enemy_rocket()
            # target = True  # TESTING!
            # if target:
            #     velocity, acceleration = self.calculate_intercept_parameters(target)
            #     new_rocket = self.arsenal.pop() if self.arsenal else None
            #     # new_rocket = Rocket(position=self.position, velocity=velocity, acceleration=acceleration)
            new_rocket = self.arsenal.pop() if self.arsenal else None

        if new_rocket:
            self.simulation.rockets.append(new_rocket)  # Добавление ракеты в симуляцию

    def select_launch_mode(self):
        # Логика выбора режима запуска
        # Может быть случайным или основываться на какой-либо стратегии
        return 0

    def calculate_launch_parameters(self, mode):
        target = velocity = acceleration = 0
        # Расчет параметров запуска в зависимости от выбранного режима
        if mode == 'precise':
            # Расчет для точного попадания в здание
            target = self.select_target()  # Выбор цели (здания)
            velocity, acceleration = self.calculate_trajectory(target)
            return target, velocity, acceleration
            pass
        elif mode == 'near_miss':
            # Расчет для прохождения мимо здания
            pass
        elif mode == 'random':
            # Случайный выбор параметров
            pass
        return target, velocity, acceleration

    def select_target(self):
        # Выбор случайного здания в качестве цели
        return random.choice(self.simulation.buildings)

    def calculate_trajectory(self, target):
        # Расчет траектории для точного попадания в цель
        # Это может потребовать расчета начальной скорости и угла запуска
        # Учитываем положение точки запуска, положение цели, гравитацию и т.д.
        return 0, 0

    def update(self, time_delta):
        # Обновление времени с последнего запуска
        self.time_since_last_launch += time_delta

        # Проверка, пора ли запускать ракету
        if self.time_since_last_launch >= self.launch_frequency:
            self.launch_rocket()
            self.time_since_last_launch = 0
