# Импорт необходимых библиотек
import pygame

from package.animation import Animation

WIDTH, HEIGHT = 600, 600
CELL = WIDTH // 9  # Размер одной ячейки (9x9 сетка)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)  # Фон активной доски
LIGHT_BLUE = (173, 216, 230)  # Для мигания выигравших досок
RED = (255, 0, 0)  # Цвет X
BLUE = (0, 0, 255)  # Цвет O

class Board:
    """Класс для управления игровой логикой Ultimate Tic-Tac-Toe"""
    def __init__(self, screen, font, big_font):
        # 9 досок 3x3 (основная структура данных)
        self.boards = [[['' for _ in range(3)] for _ in range(3)] for _ in range(9)]
        # Главная доска для отслеживания победителей отдельных досок
        self.main_board = ['' for _ in range(9)]
        self.current_player = 'X'  # Текущий игрок
        self.active_board = -1  # Активная доска (-1 означает любую доску)
        self.winner = None  # Победитель игры
        self.symbols = []  # Список анимированных символов
        self.flash_boards = {}  # Доски, которые нужно подсвечивать (при победе)
        self.win_line = None  # Линия победы на главной доске
        self.resetting = False  # Флаг сброса игры
        self.reset_alpha = 0  # Альфа-канал для анимации сброса
        self.screen = screen
        self.font = font
        self.big_font = big_font

    def get_cell(self, x, y):
        """Преобразует координаты пикселей в индексы доски и ячейки"""
        big_x, small_x = x // 3, x % 3  # Большая и малая координата X
        big_y, small_y = y // 3, y % 3  # Большая и малая координата Y
        board_index = big_y * 3 + big_x  # Индекс доски (0-8)
        cell_index = small_y * 3 + small_x  # Индекс ячейки в доске (0-8)
        return board_index, cell_index

    def make_move(self, board_index, cell_index):
        """Обрабатывает ход игрока"""
        if self.winner or self.resetting:  # Если игра завершена или сбрасывается
            return
        if self.active_board != -1 and self.active_board != board_index:
            return  # Ход не на активной доске

        row, col = divmod(cell_index, 3)  # Преобразуем индекс в строку и столбец
        if self.boards[board_index][row][col] == '' and self.main_board[board_index] == '':
            # Делаем ход
            self.boards[board_index][row][col] = self.current_player
            # Координаты для анимации
            cx = ((board_index % 3) * 3 + col) * CELL + CELL // 2
            cy = ((board_index // 3) * 3 + row) * CELL + CELL // 2
            self.symbols.append(Animation(self.current_player, (cx, cy), self.font, self.screen))

            # Проверяем победу на доске и в игре
            self.check_board_win(board_index)
            self.check_main_win()

            # Устанавливаем следующую активную доску
            self.active_board = cell_index
            if self.main_board[self.active_board] != '':
                self.active_board = -1  # Если доска уже завершена, можно ходить на любую

            self.current_player = 'O' if self.current_player == 'X' else 'X'  # Смена игрока

    def check_board_win(self, board_index):
        """Проверяет победу на указанной доске"""
        board = self.boards[board_index]
        # Проверка строк
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != '':
                self.main_board[board_index] = board[i][0]
                self.flash_boards[board_index] = 10  # Начинаем мигание
                return
        # Проверка столбцов
            if board[0][i] == board[1][i] == board[2][i] != '':
                self.main_board[board_index] = board[0][i]
                self.flash_boards[board_index] = 10
                return
        # Проверка диагоналей
        if board[0][0] == board[1][1] == board[2][2] != '':
            self.main_board[board_index] = board[0][0]
            self.flash_boards[board_index] = 10
            return
        if board[0][2] == board[1][1] == board[2][0] != '':
            self.main_board[board_index] = board[0][2]
            self.flash_boards[board_index] = 10
            return
        # Проверка на ничью
        if all(cell != '' for row in board for cell in row):
            self.main_board[board_index] = '-'

    def check_main_win(self):
        """Проверяет победу в основной игре"""
        b = self.main_board
        # Все возможные выигрышные комбинации
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Горизонтальные
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Вертикальные
            (0, 4, 8), (2, 4, 6)             # Диагональные
        ]
        for a, b1, c in wins:
            if self.main_board[a] == self.main_board[b1] == self.main_board[c] != '' and self.main_board[a] != '-':
                self.winner = self.main_board[a]
                self.win_line = (a, c)  # Запоминаем линию победы
                return
        # Проверка на ничью в основной игре
        if all(cell != '' for cell in self.main_board):
            self.winner = '-'

    def update(self):
        """Обновление состояния игры (анимации, мигания и т.д.)"""
        # Обновление анимированных символов
        for s in self.symbols:
            if not s.done:
                s.update()

        # Обновление мигающих досок
        for b in list(self.flash_boards):
            self.flash_boards[b] -= 1
            if self.flash_boards[b] <= 0:
                del self.flash_boards[b]

        # Обработка сброса игры
        if self.resetting:
            self.reset_alpha += 10
            if self.reset_alpha >= 255:
                self.__init__(self.screen, self.font, self.big_font)  # Полный сброс игры

    def reset(self):
        """Инициирует сброс игры с анимацией"""
        self.resetting = True
        self.reset_alpha = 0

    def draw(self):
        """Отрисовка всей игры"""
        self.screen.fill(WHITE)

        # Отрисовка всех 9 досок
        for bi in range(9):
            ox = (bi % 3) * 3  # Смещение по X
            oy = (bi // 3) * 3  # Смещение по Y

            # Отрисовка фона доски
            rect = pygame.Rect((ox * CELL, oy * CELL, CELL * 3, CELL * 3))
            if bi in self.flash_boards:  # Мигание для выигравшей доски
                color = LIGHT_BLUE if self.flash_boards[bi] % 2 == 0 else WHITE
                pygame.draw.rect(self.screen, color, rect)
            elif self.active_board == -1 or self.active_board == bi:  # Подсветка активной доски
                pygame.draw.rect(self.screen, GRAY, rect)

            # Отрисовка символов на доске
            for y in range(3):
                for x in range(3):
                    cx = (ox + x) * CELL
                    cy = (oy + y) * CELL
                    val = self.boards[bi][y][x]
                    if val:
                        text = self.font.render(val, True, RED if val == 'X' else BLUE)
                        self.screen.blit(text, (cx + 20, cy + 10))

            # Отрисовка большого символа для выигравшей доски
            winner = self.main_board[bi]
            if winner in ['X', 'O']:
                center_x = ox * CELL + CELL * 3 // 2
                center_y = oy * CELL + CELL * 3 // 2
                color = RED if winner == 'X' else BLUE
                big_text = self.big_font.render(winner, True, color)
                big_rect = big_text.get_rect(center=(center_x, center_y))
                self.screen.blit(big_text, big_rect)

        # Отрисовка анимированных символов
        for s in self.symbols:
            if not s.done:
                s.draw()

        # Отрисовка сетки
        for i in range(1, 9):
            width = 3 if i % 3 == 0 else 1  # Более толстые линии для границ больших досок
            pygame.draw.line(self.screen, BLACK, (i * CELL, 0), (i * CELL, HEIGHT), width)
            pygame.draw.line(self.screen, BLACK, (0, i * CELL), (WIDTH, i * CELL), width)

        # Отрисовка сообщения о победе
        if self.winner:
            if self.win_line:  # Отрисовка линии победы
                a, c = self.win_line
                ax, ay = (a % 3) * 3 + 1, (a // 3) * 3 + 1
                cx, cy = (c % 3) * 3 + 1, (c // 3) * 3 + 1
                pygame.draw.line(self.screen, RED if self.winner == 'X' else BLUE,
                                 (ax * CELL + CELL // 2, ay * CELL + CELL // 2),
                                 (cx * CELL + CELL // 2, cy * CELL + CELL // 2), 5)
            msg = "Ничья!" if self.winner == '-' else f"{self.winner} выиграл!"
            text = self.font.render(msg, True, BLACK)
            self.screen.blit(text, (WIDTH // 2 - 80, HEIGHT - 40))

        # Отрисовка анимации сброса
        if self.resetting:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(min(255, self.reset_alpha))
            overlay.fill(WHITE)
            self.screen.blit(overlay, (0, 0))

        pygame.display.flip()

