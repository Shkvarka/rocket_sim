from launch_point import LaunchPoint
from rocket import Rocket
from simulation import Simulation

import math

if __name__ == "__main__":

    defense_arsenal = [
        Rocket(position=(100, 100), velocity=(5, 0), acceleration=0, max_acceleration_time=30, rocket_type='defense', gravity=0.5)
    ]
    attacking_arsenal = [
        Rocket(position=(400, 100), velocity=(-5, 0), acceleration=1, max_acceleration_time=30, rocket_type='attacking', gravity=0.5),
        Rocket(position=(300, 200), velocity=(4, 2), acceleration=0.2, max_acceleration_time=30, rocket_type='attacking', gravity=0.5)
    ]

    angle = 66.6
    speed = 3
    init_gravity = 9.81
    angle_rad = math.radians(angle)
    missile_vx = speed * math.cos(angle_rad)
    missile_vy = -1 * speed * math.sin(angle_rad)

    attacking_arsenal_test = [
        Rocket(id = 2, position=(400, 100), velocity=(missile_vx, missile_vy), acceleration=17, max_acceleration_time=30, rocket_type='attacking', gravity=init_gravity),
    ]

    my_launch_points = [
        LaunchPoint(position=(100, 100), launch_type='defense', launch_frequency=3, arsenal=defense_arsenal),
        LaunchPoint(position=(400, 100), launch_type='attacking', launch_frequency=3, arsenal=attacking_arsenal),
        LaunchPoint(position=(0, 600), launch_type='attacking', launch_frequency=3, arsenal=attacking_arsenal_test)
    ]


    # Добавление ракеты в симуляцию и запуск
    sim = Simulation(debug_mode=True, width=800, height=1000)
    sim.add_launch_points(my_launch_points)
    sim.run(duration=10)
