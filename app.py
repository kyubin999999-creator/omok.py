import streamlit as st

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="방구석 오목 실험실", page_icon="⚫", layout="centered")

st.title("⚫ 방구석 척척 오목 게임 ⚪")
st.markdown("친구와 모니터 앞에 앉아 가볍게 내기 한판! 5개의 돌을 먼저 일렬로 잇는 사람이 승리합니다.")

st.divider()

# --- 오목판 크기 설정 (가볍게 즐기기 좋은 10x10 사이즈) ---
BOARD_SIZE = 10

# --- 게임 상태 초기화 (세션 스테이트) ---
if "omok_board" not in st.session_state:
    st.session_state.omok_board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.omok_turn = "⚫"
    st.session_state.omok_winner = None

# --- 게임 리셋 함수 ---
def reset_omok():
    st.session_state.omok_board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.omok_turn = "⚫"
    st.session_state.omok_winner = None

# --- 승리 조건 체크 함수 (가로, 세로, 대각선 5개 연속 검사) ---
def check_omok_winner(board):
    # 체크할 4가지 방향: (행 이동, 열 이동) -> 가로, 세로, 우하 대각선, 우상 대각선
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == "":
                continue
            
            stone = board[r][c]
            
            for dr, dc in directions:
                count = 1
                for i in range(1, 5):
                    nr, nc = r + dr * i, c + dc * i
                    # 오목판 범위 안에 있고 같은 색의 돌인지 확인
                    if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == stone:
                        count += 1
                    else:
                        break
                
                if count == 5:
                    return stone # 승리한 돌의 모양 반환
    return None

# --- 상단 레이아웃: 전광판 및 초기화 버튼 ---
col_status, col_reset = st.columns([3, 1])

with col_status:
    if st.session_state.omok_winner:
        st.balloons() # 축하 풍선 이펙트!
        st.success(f"🎉 **게임 종료! {st.session_state.omok_winner} 플레이어 승리!**")
    else:
        st.info(f"🏃‍♂️ 현재 차례: **{st.session_state.omok_turn}** (돌을 놓을 자리를 누르세요)")

with col_reset:
    if st.button("🔄 게임 리셋", use_container_width=True):
        reset_omok()
        st.rerun()

st.write("")

# --- 메인 레이아웃: 오목판 그리기 ---
# Streamlit의 columns를 활용해 바둑판 모양의 격자 버튼을 만듭니다.
for r in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE)
    for c in range(BOARD_SIZE):
        cell_content = st.session_state.omok_board[r][c]
        
        # 돌이 없으면 격자무늬(➕), 있으면 해당 돌 모양표시
        button_label = cell_content if cell_content != "" else "➕"
        
        # 이미 돌이 놓여있거나 승리자가 나왔다면 버튼 비활성화
        is_disabled = (cell_content != "") or (st.session_state.omok_winner is not None)
        
        # 각 버튼마다 고유의 key를 부여합니다.
        if cols[c].button(button_label, key=f"omok_{r}_{c}", disabled=is_disabled, use_container_width=True):
            # 현재 차례의 돌을 오목판에 배치
            st.session_state.omok_board[r][c] = st.session_state.omok_turn
            
            # 승패 확인
            winner = check_omok_winner(st.session_state.omok_board)
            if winner:
                st.session_state.omok_winner = winner
            else:
                # 차례 교대
                st.session_state.omok_turn = "⚪" if st.session_state.omok_turn == "⚫" else "⚫"
            
            # 화면 실시간 갱신
            st.rerun()
