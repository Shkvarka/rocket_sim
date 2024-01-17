from launch_point import LaunchPoint
from rocket import Rocket
from simulation import Simulation

import math

if __name__ == "__main__":

    init_gravity = 9.81
    acceleration = 17
    max_acceleration_time = 15

    defense_arsenal = [
        Rocket(position=(100, 100), start_velocity_scalar=10, acceleration=acceleration, max_acceleration_time=max_acceleration_time, rocket_type='attacking', gravity=init_gravity)
    ]
    attacking_arsenal = [
        Rocket(position=(400, 100), start_velocity_scalar=10, acceleration=acceleration, max_acceleration_time=max_acceleration_time, rocket_type='attacking', gravity=init_gravity),
        Rocket(position=(300, 200), start_velocity_scalar=10, acceleration=acceleration, max_acceleration_time=max_acceleration_time, rocket_type='attacking', gravity=init_gravity)
    ]

    angle = 73.03
    speed = 11

    angle_rad = math.radians(angle)
    missile_vx = speed * math.cos(angle_rad)
    missile_vy = -1 * speed * math.sin(angle_rad)

    attacking_arsenal_test = [
        # Rocket(id=2, position=(0, 600), velocity=(missile_vx, missile_vy), acceleration=27, max_acceleration_time=30, rocket_type='attacking', gravity=9.81)
        Rocket(id=2, position=(0, 600), start_velocity_scalar=10, acceleration=acceleration, max_acceleration_time=30, rocket_type='attacking', gravity=init_gravity)
        # Rocket(id = 2, position=(400, 100), velocity=(missile_vx, missile_vy), acceleration=17, max_acceleration_time=30, rocket_type='attacking', gravity=init_gravity),
    ]

    my_launch_points = [
        # LaunchPoint(position=(100, 100), launch_type='defense', launch_frequency=3, arsenal=defense_arsenal),
        LaunchPoint(position=(0, 600), launch_type='attacking', launch_frequency=3, arsenal=attacking_arsenal),
        LaunchPoint(position=(0, 600), launch_type='attacking', launch_frequency=3, arsenal=attacking_arsenal_test)
    ]


    # Добавление ракеты в симуляцию и запуск
    sim = Simulation(debug_mode=True, width=1300, height=600)
    sim.add_launch_points(my_launch_points)
    sim.run(duration=60)
