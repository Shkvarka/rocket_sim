import pygame

class Simulation:
    def __init__(self, debug_mode=False, width=800, height=600):
        self.debug_mode = debug_mode
        pygame.font.init()  # Инициализация модуля шрифтов
        self.font = pygame.font.Font(None, 18)  # Создание объекта шрифта
        self.rockets = []
        self.buildings = [(200, 550, 50, 50), (400, 530, 70, 70), (600, 560, 40, 40)]  # Примеры зданий (x, y, width, height)
        self.width = width
        self.height = height
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_text(self, text, position, color=(0, 0, 0)):
        # Рендер текста
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def add_rocket(self, rocket):
        self.rockets.append(rocket)

    def display_state(self):
        self.screen.fill((255, 255, 255))  # Заливаем фон белым

        pygame.draw.rect(self.screen, (0, 128, 0), pygame.Rect(0, self.height - 20, self.width, 20))  # Земля

        for building in self.buildings:
            pygame.draw.rect(self.screen, (128, 128, 128), pygame.Rect(*building))  # Здания


        if self.debug_mode:
            for i, rocket in enumerate(self.rockets):
                color = (0, 0, 255) if i == 0 else (255, 0, 0)
                # Рисуем пройденную траекторию
                if len(rocket.path) > 1:
                    pygame.draw.lines(self.screen, color, False, rocket.path, 1)

                # Отображаем скорость и ускорение
                self.draw_text(f"Velocity: {rocket.velocity}", (400, 0 + i * 40), color)
                self.draw_text(f"Acceleration: {rocket.acceleration}, is on: {rocket.acceleration_time < rocket.max_acceleration_time}, is destroyed: {rocket.is_destroyed}", (400, 15 + i * 40), color)

        for i, rocket in enumerate(self.rockets):
            color = (0, 0, 255) if i == 0 else (255, 0, 0)  # Синий или красный
            pygame.draw.rect(self.screen, color, pygame.Rect(rocket.position[0] - 5, rocket.position[1] - 5, 10, 10))

            if self.debug_mode and rocket.rocket_type == 'defense':
                # Отображение радиуса поражения ракеты ПВО
                pygame.draw.circle(self.screen, (255, 165, 0), (int(rocket.position[0]), int(rocket.position[1])), rocket.impact_radius, 1)

            for rocket in self.rockets:
                if rocket.is_destroyed:
                    # Визуализация уничтожения ракеты
                    # Например, мигание оранжевым цветом три раза
                    pass

        pygame.display.flip()  # Обновляем полное содержимое дисплея

    def check_collision_with_building(self, rocket, building):
        # Проверяем столкновение с зданием
        bx, by, bw, bh = building  # Координаты и размеры здания
        rx, ry = rocket.position  # Положение ракеты
        return (bx <= rx <= bx + bw) and (by <= ry <= by + bh)

    def run(self, duration):
        running = True
        start_time = pygame.time.get_ticks()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            current_time = pygame.time.get_ticks()
            if current_time - start_time > duration * 1000:  # Преобразуем секунды в миллисекунды
                running = False

            # Проверка столкновений между ракетами
            for i in range(len(self.rockets)):
                for j in range(i + 1, len(self.rockets)):
                    if self.rockets[i].check_collision(self.rockets[j]):
                        # Если произошло столкновение, уничтожаем обе ракеты
                        self.rockets[i].destroy()
                        self.rockets[j].destroy()

            # Проверка столкновений ракет с зданиями
            for rocket in self.rockets:
                if rocket.rocket_type == 'attacking' and not rocket.is_destroyed:
                    for building in self.buildings:
                        if self.check_collision_with_building(rocket, building):
                            rocket.destroy()
                            break  # Выходим из цикла после столкновения

            for rocket in self.rockets:
                rocket.update(1)  # Предполагаем фиксированный шаг времени

            self.display_state()
            pygame.time.delay(100)  # Задержка для уменьшения скорости анимации

        pygame.quit()