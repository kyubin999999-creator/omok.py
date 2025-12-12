mkdir omok_game
cd omok_game
touch omok.py
# 15x15 오목판 초기화
def initialize_board():
    board = [['.' for _ in range(15)] for _ in range(15)]  # '.'은 빈칸을 의미
    return board

# 보드 출력 함수
def print_board(board):
    print("  " + " ".join(str(i) for i in range(15)))  # 열 번호 출력
    for i in range(15):
        print(f"{i} " + " ".join(board[i]))  # 행 번호와 함께 보드 출력
# 사용자 입력 받기
def place_stone(board, player):
    while True:
        try:
            row = int(input(f"플레이어 {player}, 행 번호를 입력하세요 (0-14): "))
            col = int(input(f"플레이어 {player}, 열 번호를 입력하세요 (0-14): "))
            if board[row][col] == '.':  # 빈칸에만 놓을 수 있음
                board[row][col] = 'X' if player == 1 else 'O'  # 'X'는 플레이어 1, 'O'는 플레이어 2
                break
            else:
                print("이미 돌이 놓여진 곳입니다. 다른 곳에 놓아주세요.")
        except (ValueError, IndexError):
            print("잘못된 입력입니다. 다시 입력해주세요.")
# 승리 조건 확인 함수
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
# 게임 진행
def play_game():
    board = initialize_board()  # 보드 초기화
    player = 1  # 첫 번째 플레이어는 'X'
    while True:
        print_board(board)  # 보드 출력
        place_stone(board, player)  # 돌 놓기
        if check_winner(board, player):  # 승리 조건 체크
            print_board(board)
            print(f"플레이어 {player}가 이겼습니다!")
            break
        # 플레이어 변경
        player = 2 if player == 1 else 1
# 게임 실행
if __name__ == "__main__":
    play_game()
