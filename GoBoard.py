import pygame
import sys

# 初始化Pygame
pygame.init()

# 设置屏幕大小和颜色
size = 800
screen = pygame.display.set_mode((size, size))
pygame.display.set_caption("Go Game")
bg_color = (245, 222, 179)
line_color = (0, 0, 0)
black_color = (0, 0, 0)
white_color = (255, 255, 255)

# 棋盘大小和格子大小
board_size = 19
cell_size = size // (board_size + 1)

class GoBoard:
    def __init__(self, size=19):
        self.size = size
        self.board = [['.' for _ in range(size)] for _ in range(size)]
        self.current_color = 'B'
        self.ko_point = None
        self.ko_color = None

    def place_stone(self, x, y):
        if self.board[x][y] == '.' and (x, y) != self.ko_point:
            self.board[x][y] = '●' if self.current_color == 'B' else '○'
            captured_stones = self.remove_captured_stones(x, y)
            if not self.has_liberty(x, y, self.board[x][y], set()) and not captured_stones:
                self.board[x][y] = '.'
                return False
            if len(captured_stones) == 1:
                self.ko_point = captured_stones[0]
                self.ko_color = self.board[x][y]
            else:
                self.ko_point = None
                self.ko_color = None
            self.current_color = 'W' if self.current_color == 'B' else 'B'
            return True
        return False

    def remove_captured_stones(self, x, y):
        opponent_color = '○' if self.board[x][y] == '●' else '●'
        captured_stones = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if self.is_on_board(nx, ny) and self.board[nx][ny] == opponent_color:
                visited = set()
                if not self.has_liberty(nx, ny, opponent_color, visited):
                    captured_stones.extend(visited)
        for cx, cy in captured_stones:
            self.board[cx][cy] = '.'
        return captured_stones

    def has_liberty(self, x, y, color, visited):
        if (x, y) in visited:
            return False
        visited.add((x, y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if self.is_on_board(nx, ny):
                if self.board[nx][ny] == '.':
                    return True
                if self.board[nx][ny] == color and self.has_liberty(nx, ny, color, visited):
                    return True
        return False

    def is_on_board(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

def draw_board(screen, board):
    screen.fill(bg_color)
    for i in range(board_size):
        pygame.draw.line(screen, line_color, (cell_size, cell_size + i * cell_size), (size - cell_size, cell_size + i * cell_size))
        pygame.draw.line(screen, line_color, (cell_size + i * cell_size, cell_size), (cell_size + i * cell_size, size - cell_size))
    for x in range(board.size):
        for y in range(board.size):
            if board.board[x][y] == '●':
                pygame.draw.circle(screen, black_color, (cell_size + y * cell_size, cell_size + x * cell_size), cell_size // 2 - 2)
            elif board.board[x][y] == '○':
                pygame.draw.circle(screen, white_color, (cell_size + y * cell_size, cell_size + x * cell_size), cell_size // 2 - 2)

def main():
    board = GoBoard()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x = (x - cell_size) // cell_size
                y = (y - cell_size) // cell_size
                if 0 <= x < board_size and 0 <= y < board_size:
                    if board.place_stone(y, x):
                        draw_board(screen, board)
                        pygame.display.flip()

        draw_board(screen, board)
        pygame.display.flip()

if __name__ == "__main__":
    main()
