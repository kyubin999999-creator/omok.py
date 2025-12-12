# 15x15 오목판 초기화
def initialize_board():
    return [['.' for _ in range(15)] for _ in range(15)]  # '.'은 빈칸을 의미

# 보드 출력 함수
def print_board(board):
    print("    " + " ".join([f"{i:2}" for i in range(15)]))  # 열 번호 출력
    print("   +" + "---+" * 15)  # 경계선

    for i in range(15):
        row_display = f"{i:2} |"  # 행 번호와 왼쪽 경계선
        for j in range(15):
            if board[i][j] == 'X':  # 플레이어 1 (X)는 빨간색
                row_display += f" X |"
            elif board[i][j] == 'O':  # 플레이어 2 (O)는 파란색
                row_display += f" O |"
            else:
                row_display += " . |"  # 빈칸은 점으로 표시
        print(row_display)  # 한 행 출력
        print("   +" + "---+" * 15)  # 경계선 출력
if __name__ == "__main__":
    board = initialize_board()  # 보드 초기화
    print_board(board)  # 보드 출력
