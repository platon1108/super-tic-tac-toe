import pygame

RED = (255, 0, 0)  # Цвет X
BLUE = (0, 0, 255)  # Цвет O


class Animation:
    """Класс для анимированного отображения символов X и O"""
    def __init__(self, value, pos, font, screen):
        self.value = value  # 'X' или 'O'
        self.pos = pos  # Позиция на экране
        self.scale = 0.1  # Начальный масштаб (для анимации)
        self.done = False  # Флаг завершения анимации
        self.font = font # Шрифт
        self.screen = screen # Экран

    def update(self):
        """Обновление анимации - увеличение масштаба"""
        if self.scale < 1.0:
            self.scale += 0.1
        else:
            self.done = True  # Анимация завершена

    def draw(self):
        """Отрисовка символа с текущим масштабом"""
        if self.value:
            color = RED if self.value == 'X' else BLUE
            text = self.font.render(self.value, True, color)
            # Масштабирование текста
            scaled = pygame.transform.scale(text, 
                (int(text.get_width() * self.scale), 
                 int(text.get_height() * self.scale)))
            rect = scaled.get_rect(center=self.pos)
            self.screen.blit(scaled, rect)
