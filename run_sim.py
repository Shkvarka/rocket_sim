from rocket import Rocket
from simulation import Simulation

if __name__ == "__main__":
    # # Создание симуляции
    # sim = Simulation()
    #
    # # Добавление ракет в симуляцию
    # sim.add_rocket(Rocket(position=(0, 0), velocity=(1, 2), acceleration=(0.1, -0.1)))
    # sim.add_rocket(Rocket(position=(10, 10), velocity=(-1, -1), acceleration=(0, 0.1)))
    #
    # sim.run(duration=60)  # Запуск симуляции на 60 секунд
    #
    # plt.show()  # Отображение графика

    # blue = Rocket(position=(100, 100), velocity=(5, -5), acceleration=(0, 0), max_acceleration_time=30, rocket_type='defense', gravity=0.5)
    # red = Rocket(position=(500, 200), velocity=(0, 0), acceleration=(0.2, 0), max_acceleration_time=30, rocket_type='attacking', gravity=0.5)
    # red_ = Rocket(position=(200, 200), velocity=(0, 2), acceleration=(0.2, 0), max_acceleration_time=30, rocket_type='attacking', gravity=0.5)

    blue = Rocket(position=(100, 100), velocity=(5, 0), acceleration=(0, 0), max_acceleration_time=30, rocket_type='defense', gravity=0.5)
    red = Rocket(position=(400, 100), velocity=(-5, 0), acceleration=(0, 0), max_acceleration_time=30, rocket_type='attacking', gravity=0.5)
    red_ = Rocket(position=(300, 200), velocity=(0, 2), acceleration=(0.2, 0), max_acceleration_time=30, rocket_type='attacking', gravity=0.5)


    # Добавление ракеты в симуляцию и запуск
    sim = Simulation(debug_mode=True)
    sim.add_rocket(blue)
    sim.add_rocket(red)
    sim.add_rocket(red_)
    sim.run(duration=10)
