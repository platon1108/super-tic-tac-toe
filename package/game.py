import pygame
import sys

from package.board import Board


WIDTH, HEIGHT = 600, 600
CELL = WIDTH // 9  # Размер одной ячейки (9x9 сетка)
FPS = 60  # Частота кадров

clock = pygame.time.Clock()  # Таймер для контроля FPS
pygame.init() # Инициализация Pygame
pygame.display.set_caption("Супер крестики-нолики")  # Заголовок окна

screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Окно
font = pygame.font.SysFont(None, 40)  # Обычный шрифт
big_font = pygame.font.SysFont(None, 100)  # Большой шрифт

def main():
    """Главная функция игры"""
    game = Board(screen, font, big_font)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game.resetting:
                # Обработка клика мыши
                mx, my = pygame.mouse.get_pos()
                x, y = mx // CELL, my // CELL
                b_idx, c_idx = game.get_cell(x, y)
                game.make_move(b_idx, c_idx)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game.reset()  # Сброс игры по клавише R

        game.update()
        game.draw()
        clock.tick(FPS)  # Поддержание стабильного FPS

if __name__ == '__main__':
    main()
