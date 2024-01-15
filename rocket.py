import numpy as np

float_formatter = "{:.2f}".format
np.set_printoptions(formatter={'float_kind':float_formatter})


class Rocket:
    def __init__(self, position, velocity, acceleration, max_acceleration_time, rocket_type, deceleration=1.2, gravity=-9.81,
                 impact_radius=50, id=1):
        self.id = id
        self.position = np.array(position, dtype=float)  # Текущая позиция ракеты (x, y)
        self.velocity = np.array(velocity, dtype=float)  # Текущая скорость ракеты (vx, vy)
        self.launch_point = None
        self.path = []  # Добавляем начальное положение в путь
        self.acceleration = acceleration  # Скалярное ускорение ракеты
        self.max_acceleration_time = max_acceleration_time  # Время ускорения
        self.acceleration_time = 0  # Текущее время ускорения
        self.gravity = gravity  # Гравитация, воздействующая на ракету
        self.deceleration = deceleration  # Замедление ракеты
        self.rocket_type = rocket_type  # Тип ракеты (например, 'defense' или 'enemy')
        # self.rocket_type = launch_point.launch_type  # Тип ракеты (например, 'defense' или 'enemy')
        self.impact_radius = impact_radius  # Радиус поражения для ракет ПВО
        self.is_destroyed = False  # Статус уничтожения ракеты

    def set_launching_point(self, launch_point):
        self.launch_point = launch_point

    def set_position(self, position):
        self.position = np.array(position, dtype=float)  # Текущая позиция ракеты (x, y)
        self.path = [position]

    def update(self, time_step):
        # Добавим проверку, не уничтожена ли ракета
        if self.is_destroyed:
            return  # Не обновляем положение или скорость уничтоженной ракеты

        if self.id == 2:

            print(f"Velocity vector: {self.velocity}, module: {np.linalg.norm(self.velocity)}")
            print(f"Gravity vector: {(0, self.gravity)}")
            print(f"Acceleration vector: {self.normalize(self.velocity) * self.acceleration}")

        # Обновление вектора скорости в зависимости от ускорения и гравитации
        if self.acceleration_time < self.max_acceleration_time:
            # Направление ускорения совпадает с текущим направлением скорости
            acceleration_vector = self.normalize(self.velocity) * self.acceleration
            self.velocity += acceleration_vector * time_step
            self.acceleration_time += time_step
        else:
            # Учет замедления (сопротивление воздуха)
            deceleration_vector = -self.normalize(self.velocity) * self.deceleration
            self.velocity += deceleration_vector * time_step

        # Воздействие гравитации на ракету
        gravity_vector = (0, self.gravity)
        self.velocity += np.array(gravity_vector) * time_step

        # Обновление позиции ракеты
        self.position += self.velocity * time_step
        self.path.append([float(i) for i in self.position])

    @staticmethod
    def normalize(vector):
        # Нормализация вектора для получения направления
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm

    def destroy(self):
        # Логика уничтожения ракеты
        self.is_destroyed = True
        # Здесь может быть реализация визуализации уничтожения, если потребуется

    def check_collision(self, other_rocket):
        # Проверяем, не уничтожена ли ракета
        if self.is_destroyed or other_rocket.is_destroyed:
            return False
        if self.rocket_type == other_rocket.rocket_type:
            return False
        # if self.position[1] < 0:
        #     return True


        # Расчет расстояния между ракетами
        distance = ((self.position[0] - other_rocket.position[0]) ** 2 + (self.position[1] - other_rocket.position[1]) ** 2) ** 0.5

        # Проверяем, находится ли другая ракета в радиусе поражения
        if distance <= self.impact_radius:
            return True

        return False
    def check_collision_with_building(self, building):
        # Проверяем столкновение с зданием
        bx, by, bw, bh = building  # Координаты и размеры здания
        rx, ry = self.position  # Положение ракеты
        return (bx <= rx <= bx + bw) and (by <= ry <= by + bh)
