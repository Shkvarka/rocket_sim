import random

from RocketSolution import AttackRocketSolution


class LaunchPoint:
    def __init__(self, position, launch_type, launch_frequency, arsenal: list):
        self.position = position
        self.launch_type = launch_type  # 'attacking' или 'defense'
        self.launch_frequency = launch_frequency
        self.arsenal = arsenal
        self.simulation = None  # should be set later
        self.time_since_last_launch = 0

        self.load_rockets()

        self.attackSolutionFinder = AttackRocketSolution()

    def load_rockets(self):
        for rocket in self.arsenal:
            rocket.set_launching_point(self)
            rocket.set_position(self.position)

    def add_simulation(self, simulation):
        self.simulation = simulation
        self.attackSolutionFinder.set_simulation(simulation)

    def launch_rocket(self):
        loaded_rocket = None

        if self.launch_type == 'attacking':
            # Логика выбора режима запуска и параметров ракеты
            if self.arsenal:
                mode = self.select_launch_mode()  # Выбор режима запуска
                loaded_rocket = self.arsenal.pop()
                angle, trajectory = self.calculate_launch_parameters(mode, loaded_rocket)
                loaded_rocket.set_angle(angle)
        elif self.launch_type == 'defense':
            # # Логика определения цели и параметров ракеты ПВО
            # target = self.detect_enemy_rocket()
            # target = True  # TESTING!
            # if target:
            #     velocity, acceleration = self.calculate_intercept_parameters(target)
            #     new_rocket = self.arsenal.pop() if self.arsenal else None
            #     # new_rocket = Rocket(position=self.position, velocity=velocity, acceleration=acceleration)
            loaded_rocket = self.arsenal.pop() if self.arsenal else None

        if loaded_rocket:
            self.simulation.rockets.append(loaded_rocket)  # Добавление ракеты в симуляцию

    def select_launch_mode(self):
        # Логика выбора режима запуска
        # Может быть случайным или основываться на какой-либо стратегии
        return 'precise'

    def calculate_launch_parameters(self, mode, loaded_rocket):
        # Расчет параметров запуска в зависимости от выбранного режима
        if mode == 'precise':
            # Расчет для точного попадания в здание
            target = self.select_target()  # Выбор цели (здания)
            angle, trajectory = self.attackSolutionFinder.calculate_launch_parameters(loaded_rocket, target)
            return angle, trajectory
        elif mode == 'near_miss':
            # Расчет для прохождения мимо здания
            pass
        elif mode == 'random':
            # Случайный выбор параметров
            pass
        return None

    def select_target(self):
        # Выбор случайного здания в качестве цели
        random.shuffle(self.simulation.buildings_to_destroy)
        return [(self.simulation.buildings_to_destroy.pop())]

    def update(self, time_delta):
        # Обновление времени с последнего запуска
        self.time_since_last_launch += time_delta

        # Проверка, пора ли запускать ракету
        if self.time_since_last_launch >= self.launch_frequency:
            self.launch_rocket()
            self.time_since_last_launch = 0
