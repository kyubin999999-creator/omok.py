pip install pygame
python omok_game/omok.py
import pygame
import sys

# Pygame 초기화
pygame.init()

# 게임 설정
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
LINE_WIDTH = 2
CELL_SIZE = SCREEN_WIDTH // 15  # 15x15 보드
BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
PLAYER1_COLOR = (255, 0, 0)  # 플레이어 1 (X) 빨간색
PLAYER2_COLOR = (0, 0, 255)  # 플레이어 2 (O) 파란색

# 화면 설정
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("오목 게임")

# 오목판 초기화
def initialize_board():
    return [['.' for _ in range(15)] for _ in range(15)]  # '.'은 빈칸을 의미

# 보드 그리기
def draw_board(board):
    # 배경 그리기
    screen.fill(BACKGROUND_COLOR)

    # 가로, 세로 라인 그리기
    for row in range(16):
        pygame.draw.line(screen, LINE_COLOR, (0, row * CELL_SIZE), (SCREEN_WIDTH, row * CELL_SIZE), LINE_WIDTH)
    for col in range(16):
        pygame.draw.line(screen, LINE_COLOR, (col * CELL_SIZE, 0), (col * CELL_SIZE, SCREEN_HEIGHT), LINE_WIDTH)

    # 돌 그리기
    for row in range(15):
        for col in range(15):
            if board[row][col] == 'X':  # 플레이어 1 (X)
                pygame.draw.circle(screen, PLAYER1_COLOR, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
            elif board[row][col] == 'O':  # 플레이어 2 (O)
                pygame.draw.circle(screen, PLAYER2_COLOR, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

    pygame.display.update()

# 사용자 입력 처리
def place_stone(board, player, x, y):
    row = y // CELL_SIZE
    col = x // CELL_SIZE

    if 0 <= row < 15 and 0 <= col < 15 and board[row][col] == '.':
        board[row][col] = 'X' if player == 1 else 'O'
        return True
    return False

# 승리 조건 확인
def check_winner(board, player):
    stone = 'X' if player == 1 else 'O'
    
    # 가로 체크
    for row in range(15):
        for col in range(11):  # 15-5+1 = 11, 가로로 5칸씩 확인
            if all(board[row][col + i] == stone for i in range(5)):
                return True
    
    # 세로 체크
    for col in range(15):
        for row in range(11):
            if all(board[row + i][col] == stone for i in range(5)):
                return True
    
    # 대각선 (왼쪽 상단 -> 오른쪽 하단) 체크
    for row in range(11):
        for col in range(11):
            if all(board[row + i][col + i] == stone for i in range(5)):
                return True
    
    # 대각선 (왼쪽 하단 -> 오른쪽 상단) 체크
    for row in range(4, 15):
        for col in range(11):
            if all(board[row - i][col + i] == stone for i in range(5)):
                return True
    
    return False

# 게임 실행
def play_game():
    board = initialize_board()
    player = 1  # 첫 번째 플레이어는 'X'

    # 게임 루프
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 마우스 클릭 처리
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()  # 마우스 위치
                if place_stone(board, player, x, y):  # 돌 놓기
                    if check_winner(board, player):  # 승리 체크
                        draw_board(board)
                        print(f"플레이어 {player}가 이겼습니다!")
                        pygame.time.wait(2000)  # 2초 후 종료
                        pygame.quit()
                        sys.exit()
                    player = 2 if player == 1 else 1  # 플레이어 변경

        draw_board(board)

# 게임 실행
if __name__ == "__main__":
    play_game()

