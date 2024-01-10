class Rocket:
    def __init__(self, position, velocity, acceleration, max_acceleration_time, rocket_type, deceleration=0.2, gravity=-0.1, impact_radius=50):
        self.position = position
        self.velocity = velocity
        self.path = [position]  # Добавляем начальное положение в путь
        self.acceleration = acceleration
        self.max_acceleration_time = max_acceleration_time
        self.acceleration_time = 0
        self.gravity = gravity
        self.deceleration = deceleration
        self.rocket_type = rocket_type  # 'attacking' или 'defense'
        self.impact_radius = impact_radius  # Радиус поражения для ракет ПВО
        self.is_destroyed = False  # Статус уничтожения ракеты

    def update(self, time_delta):
        # Добавим проверку, не уничтожена ли ракета
        if self.is_destroyed:
            return  # Не обновляем положение или скорость уничтоженной ракеты

        if self.acceleration_time < self.max_acceleration_time:
            self.velocity = tuple(v + a * time_delta for v, a in zip(self.velocity, self.acceleration))
            self.acceleration_time += time_delta
        else:
            # Применение замедления после исчерпания топлива
            vx, vy = self.velocity
            vx = max(vx - self.deceleration * time_delta, 0) if vx > 0 else min(vx + self.deceleration * time_delta, 0)
            vy -= self.deceleration * time_delta
            self.velocity = (vx, vy)

        # Применение гравитации к вертикальной скорости
        vx, vy = self.velocity
        vy += self.gravity * time_delta
        self.velocity = (vx, vy)

        # Обновление положения
        self.position = tuple(p + v * time_delta for p, v in zip(self.position, self.velocity))
        self.path.append(self.position)


    def destroy(self):
        # Логика уничтожения ракеты
        self.is_destroyed = True
        # Здесь может быть реализация визуализации уничтожения, если потребуется

    def check_collision(self, other_rocket):
        # Проверяем, не уничтожена ли ракета
        if self.is_destroyed or other_rocket.is_destroyed:
            return False

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