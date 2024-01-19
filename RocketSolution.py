from rocket import Rocket

import copy
import math
import random
import numpy as np
import pygame
from scipy.optimize import minimize

Nfeval = 1


class AttackRocketSolution:
    def __init__(self):
        # Инициализация параметров симуляции
        self.trajectory = None
        self.simulation = None
        self.color = random.randint(50, 250)
        pass


    def calculate_launch_parameters(self, rocket: Rocket, building: list):
        """
        Рассчитывает начальный вектор скорости ракеты для попадания в цель.

        :param launching_position: Координаты точки запуска (x, y).
        :param target_position: Координаты области цели [(x, y), (x1, y1), (x2, y2), (x3, y3)].
        :param initial_speed: Начальная скорость ракеты, скалярная величина
        :param acceleration: ускорение, скалярная величина
        :param max_acceleration_time: максимальная длительность ускорения ракеты
        :param deceleration: Замедление ракеты (симуляция трения воздуха, скалярное значение)
        :param gravity: Гравитация (вектор - действует постоянно, направлен вниз)

        :return: Вектор начальной скорости (velocity_x, velocity_y).
        """
        # Реализация вычисления начального вектора скорости для попадания по цели

        trajectory = None

        # Предварительное определение функции для расчета траектории
        def trajectory(v0, launching_position, target_position, acceleration, max_acceleration_time, deceleration, gravity):
            # Здесь должен быть ваш код для расчета траектории
            # Например, вы можете использовать физические уравнения для моделирования движения ракеты
            pass

        # Функция оптимизации для поиска лучшего начального вектора скорости
        def objective_function(angle):
            # Ваш код для определения, насколько хорошо данное v0 соответствует цели
            # Например, вы можете рассчитать разницу между конечной позицией ракеты и целью

            test_rocket = Rocket(position=copy.deepcopy(rocket.position), start_velocity_scalar=rocket.start_velocity_scalar, acceleration=rocket.acceleration,
                                 max_acceleration_time=rocket.max_acceleration_time, rocket_type=rocket.rocket_type)

            guess_angle = angle[0]
            speed = test_rocket.start_velocity_scalar
            angle_rad = math.radians(guess_angle)
            missile_vx = speed * math.cos(angle_rad)
            missile_vy = -1 * speed * math.sin(angle_rad)

            test_rocket.set_velocity((missile_vx, missile_vy))
            test_rocket.set_position(rocket.position)

            from simulation import GLOBAL_TIME_STEP
            while not test_rocket.is_destroyed:
                test_rocket.update(GLOBAL_TIME_STEP)
                if test_rocket.check_collision_with_building(*building) or test_rocket.check_ground_collision():
                    test_rocket.destroy()
                    self.trajectory = test_rocket.path
                    test_rocket.path = []

            pygame.draw.lines(self.simulation.screen, (self.color, 0, 0), False, self.trajectory, 1)
            pygame.display.flip()

            target_center = pygame.Rect(*building).center

            distance = math.sqrt((test_rocket.position[0]-target_center[0])**2 + (test_rocket.position[1]-target_center[1])**2)
            return distance
        ##Print callback function
        def printx(Xi):
            global Nfeval
            # print('At iterate {0:4d},  f={1: 3.6f} '.format(Nfeval, objective_function(Xi)) + '\n')
            Nfeval += 1

        # Использование оптимизатора для поиска лучшего начального вектора скорости
        bounds = [(-20.0, 89.99)]
        # result = minimize(objective_function, x0=np.array([1]), callback=printx, method='Nelder-Mead')
        result = minimize(objective_function, x0=np.array([1]), bounds=bounds,  callback=printx, method='Powell')
        # result = minimize(objective_function, x0=np.array([10]), callback=printx)

        # Возвращение результата оптимизации как начального вектора скорости
        solution_angle = result.x
        print(f'result: {result}')
        return solution_angle, self.trajectory

    def set_simulation(self, simulation):
        self.simulation = simulation


# Пример использования класса
# target_position = [(600, 560, 40, 40)]
# atck_rckt_col = AttackRocketSolution()
# solution_angle = atck_rckt_col.calculate_launch_parameters(Rocket(id=2, position=(0, 600), start_velocity_scalar=10, acceleration=17, max_acceleration_time=30, rocket_type='attacking', gravity=9.81), target_position)
