import streamlit as st
import streamlit.components.v1 as components

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="3D 입체 오목 실험실", page_icon="⚫", layout="centered")

st.title("🎬 3D 입체 방구석 오목 게임 ⚪")
st.markdown("은은한 조명을 받는 3D 입체 바둑돌과 나무 바둑판입니다. 친구와 함께 번갈아 두며 즐겨보세요!")

st.divider()

# --- HTML5 Canvas 기반의 3D 오목 게임 내장 ---
js_code = """
<div style="text-align: center; font-family: 'Malgun Gothic', sans-serif;">
    <div style="display: flex; justify-content: space-between; align-items: center; max-width: 460px; margin: 0 auto 15px auto;">
        <div id="status-box" style="padding: 10px 20px; background: #e0f2fe; color: #0369a1; border-radius: 8px; font-weight: bold; font-size: 16px; border: 1px solid #bae6fd;">
            🏃‍♂️ 현재 차례: 흑돌 (⚫)
        </div>
        <button id="reset-btn" style="padding: 10px 15px; background: #ef4444; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 14px; transition: 0.2s;">
            🔄 게임 리셋
        </button>
    </div>

    <canvas id="omokCanvas" width="460" height="460" style="border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.15); cursor: pointer;"></canvas>
</div>

<script>
    const canvas = document.getElementById('omokCanvas');
    const ctx = canvas.getContext('2d');
    const statusBox = document.getElementById('status-box');
    const resetBtn = document.getElementById('reset-btn');

    const BOARD_SIZE = 10;
    const PADDING = 35;
    const CELL_SIZE = (canvas.width - PADDING * 2) / (BOARD_SIZE - 1);
    
    let board = Array(BOARD_SIZE).fill(null).map(() => Array(BOARD_SIZE).fill(''));
    let currentTurn = 'black'; // 'black' 또는 'white'
    let winner = null;

    // --- 1. 바둑판 배경 및 격자 그리기 ---
    function drawBoard() {
        ctx.shadowBlur = 0;
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 0;

        // 따뜻한 원목 느낌 배경색
        ctx.fillStyle = '#eec590';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // 은은한 나무 테두리 선
        ctx.strokeStyle = '#c69a63';
        ctx.lineWidth = 4;
        ctx.strokeRect(2, 2, canvas.width - 4, canvas.height - 4);

        // 바둑판 격자선 그리기
        ctx.strokeStyle = '#5c4033';
        ctx.lineWidth = 1.5;
        
        for (let i = 0; i < BOARD_SIZE; i++) {
            // 가로선
            ctx.beginPath();
            ctx.moveTo(PADDING, PADDING + i * CELL_SIZE);
            ctx.lineTo(canvas.width - PADDING, PADDING + i * CELL_SIZE);
            ctx.stroke();

            // 세로선
            ctx.beginPath();
            ctx.moveTo(PADDING + i * CELL_SIZE, PADDING);
            ctx.lineTo(PADDING + i * CELL_SIZE, canvas.height - PADDING);
            ctx.stroke();
        }

        // 바둑판 중심점(화점) 찍기
        ctx.fillStyle = '#5c4033';
        ctx.beginPath();
        ctx.arc(canvas.width / 2, canvas.height / 2, 4, 0, Math.PI * 2);
        ctx.fill();
    }

    // --- 2. 입체적인 3D 바둑돌 그리기 ---
    function drawStone(row, col, color) {
        const x = PADDING + col * CELL_SIZE;
        const y = PADDING + row * CELL_SIZE;
        const radius = CELL_SIZE * 0.43;

        ctx.save();

        // 바닥에 떨어지는 은은한 돌 그림자 효과
        ctx.shadowColor = 'rgba(0, 0, 0, 0.35)';
        ctx.shadowBlur = 6;
        ctx.shadowOffsetX = 3;
        ctx.shadowOffsetY = 4;

        // 입체 구체 느낌을 내기 위한 방사형 그라데이션 적용
        ctx.beginPath();
        let gradient = ctx.createRadialGradient(
            x - radius * 0.3, y - radius * 0.3, radius * 0.1, // 하이라이트 빛점
            x, y, radius                                      // 돌 외곽선
        );

        if (color === 'black') {
            gradient.addColorStop(0, '#666666');   
            gradient.addColorStop(0.2, '#222222'); 
            gradient.addColorStop(1, '#050505');   
        } else {
            gradient.addColorStop(0, '#ffffff');   
            gradient.addColorStop(0.6, '#eaeaea'); 
            gradient.addColorStop(1, '#bbbbbb');   
        }

        ctx.fillStyle = gradient;
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }

    // --- 3. 모든 돌 다시 그리기 (오타 수정 완료!) ---
    function render() {
        drawBoard();
        for (let r = 0; r < BOARD_SIZE; r++) {
            for (let c = 0; c < BOARD_SIZE; c++) {
                if (board[r][c] !== '') {
                    drawStone(r, c, board[r][c]);
                }
            }
        }
    }

    // --- 4. 오목 승리 판정 알고리즘 ---
    function checkWin(row, col, color) {
        const dirs = [[0,1], [1,0], [1,1], [1,-1]];
        for (let [dr, dc] of dirs) {
            let count = 1;
            
            // 정방향 탐색
            let r = row + dr, c = col + dc;
            while(r >= 0 && r < BOARD_SIZE && c >= 0 && c < BOARD_SIZE && board[r][c] === color) {
                count++; r += dr; c += dc;
            }
            // 역방향 탐색
            r = row - dr; c = col - dc;
            while(r >= 0 && r < BOARD_SIZE && c >= 0 && c < BOARD_SIZE && board[r][c] === color) {
                count++; r -= dr; c -= dc;
            }
            
            if (count === 5) return true;
        }
        return false;
    }

    // --- 5. 클릭 이벤트 처리 (가장 가까운 교차점에 돌 배치) ---
    canvas.addEventListener('click', function(e) {
        if (winner) return;

        const rect = canvas.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;

        const col = Math.round((mouseX - PADDING) / CELL_SIZE);
        const row = Math.round((mouseY - PADDING) / CELL_SIZE);

        if (row >= 0 && row < BOARD_SIZE && col >= 0 && col < BOARD_SIZE) {
            if (board[row][col] === '') {
                board[row][col] = currentTurn;
                render();

                if (checkWin(row, col, currentTurn)) {
                    winner = currentTurn;
                    statusBox.style.background = '#dcfce7';
                    statusBox.style.color = '#15803d';
                    statusBox.style.borderColor = '#bbf7d0';
                    statusBox.style.fontSize = '18px';
                    statusBox.innerHTML = `🎉 승리: ${winner === 'black' ? '흑돌(⚫)' : '백돌(⚪)'} 플레이어 승리!`;
                    return;
                }

                currentTurn = currentTurn === 'black' ? 'white' : 'black';
                statusBox.innerHTML = `跑‍♂️ 현재 차례: ${currentTurn === 'black' ? '흑돌 (⚫)' : '백돌 (⚪)'}`;
            }
        }
    });

    // --- 6. 리셋 버튼 이벤트 ---
    resetBtn.addEventListener('click', function() {
        board = Array(BOARD_SIZE).fill(null).map(() => Array(BOARD_SIZE).fill(''));
        currentTurn = 'black';
        winner = null;
        statusBox.style.background = '#e0f2fe';
        statusBox.style.color = '#0369a1';
        statusBox.style.borderColor = '#bae6fd';
        statusBox.style.fontSize = '16px';
        statusBox.innerHTML = "🏃‍♂️ 현재 차례: 흑돌 (⚫)";
        drawBoard();
    });

    // 최초 실행
    drawBoard();
</script>
"""

components.html(js_code, height=530)

st.divider()
st.caption("💡 선과 선이 만나는 교차점 근처를 누르면 자석처럼 착 달라붙으며 3D 바둑돌이 놓입니다.")
