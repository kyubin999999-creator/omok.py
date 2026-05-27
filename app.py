import streamlit as st
import streamlit.components.v1 as components

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="프로 정식 오목 실험실", page_icon="⚫", layout="centered")

st.title("🥋 프로 정식 규격 3D 오목 게임 ⚪")
st.markdown("표준 대회 규격인 **15x15 바둑판**에 흑돌 **33 및 44 금지 룰**이 모두 적용된 정식 오목입니다.")

st.divider()

# --- HTML5 Canvas 기반의 정밀 오목 엔진 내장 ---
js_code = """
<div style="text-align: center; font-family: 'Malgun Gothic', sans-serif;">
    <div style="display: flex; justify-content: space-between; align-items: center; max-width: 530px; margin: 0 auto 15px auto;">
        <div id="status-box" style="padding: 10px 20px; background: #e0f2fe; color: #0369a1; border-radius: 8px; font-weight: bold; font-size: 16px; border: 1px solid #bae6fd;">
            🏃‍♂️ 현재 차례: 흑돌 (⚫)
        </div>
        <button id="reset-btn" style="padding: 10px 15px; background: #ef4444; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 14px; transition: 0.2s;">
            🔄 게임 리셋
        </button>
    </div>

    <canvas id="omokCanvas" width="530" height="530" style="border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.15); cursor: pointer;"></canvas>
</div>

<script>
    const canvas = document.getElementById('omokCanvas');
    const ctx = canvas.getContext('2d');
    const statusBox = document.getElementById('status-box');
    const resetBtn = document.getElementById('reset-btn');

    const BOARD_SIZE = 15; 
    const PADDING = 30;
    const CELL_SIZE = (canvas.width - PADDING * 2) / (BOARD_SIZE - 1);
    
    let board = Array(BOARD_SIZE).fill(null).map(() => Array(BOARD_SIZE).fill(''));
    let currentTurn = 'black'; 
    let winner = null;

    // --- 1. 15x15 나무 바둑판 및 화점 그리기 ---
    function drawBoard() {
        ctx.shadowBlur = 0; ctx.shadowOffsetX = 0; ctx.shadowOffsetY = 0;
        ctx.fillStyle = '#eec590';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.strokeStyle = '#c69a63'; ctx.lineWidth = 4;
        ctx.strokeRect(2, 2, canvas.width - 4, canvas.height - 4);

        ctx.strokeStyle = '#5c4033'; ctx.lineWidth = 1.5;
        for (let i = 0; i < BOARD_SIZE; i++) {
            ctx.beginPath(); ctx.moveTo(PADDING, PADDING + i * CELL_SIZE); ctx.lineTo(canvas.width - PADDING, PADDING + i * CELL_SIZE); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(PADDING + i * CELL_SIZE, PADDING); ctx.lineTo(PADDING + i * CELL_SIZE, canvas.height - PADDING); ctx.stroke();
        }

        const starPoints = [3, 7, 11];
        ctx.fillStyle = '#5c4033';
        for (let r of starPoints) {
            for (let c of starPoints) {
                if ((r === 7 && c === 7) || (r !== 7 && c !== 7)) {
                    ctx.beginPath(); ctx.arc(PADDING + c * CELL_SIZE, PADDING + r * CELL_SIZE, 4.5, 0, Math.PI * 2); ctx.fill();
                }
            }
        }
    }

    // --- 2. 3D 구체 바둑돌 그리기 ---
    function drawStone(row, col, color) {
        const x = PADDING + col * CELL_SIZE;
        const y = PADDING + row * CELL_SIZE;
        const radius = CELL_SIZE * 0.44;

        ctx.save();
        ctx.shadowColor = 'rgba(0, 0, 0, 0.35)'; ctx.shadowBlur = 5; ctx.shadowOffsetX = 2; ctx.shadowOffsetY = 3;

        ctx.beginPath();
        let gradient = ctx.createRadialGradient(x - radius*0.3, y - radius*0.3, radius*0.05, x, y, radius);
        if (color === 'black') {
            gradient.addColorStop(0, '#666666'); gradient.addColorStop(0.2, '#222222'); gradient.addColorStop(1, '#050505');   
        } else {
            gradient.addColorStop(0, '#ffffff'); gradient.addColorStop(0.5, '#eaeaea'); gradient.addColorStop(1, '#aaaaaa');   
        }
        ctx.fillStyle = gradient;
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }

    function render() {
        drawBoard();
        for (let r = 0; r < BOARD_SIZE; r++) {
            for (let c = 0; c < BOARD_SIZE; c++) {
                if (board[r][c] !== '') drawStone(r, c, board[r][c]);
            }
        }
    }

    // --- 3. 오목 승리 검사 ---
    function checkWin(row, col, color) {
        const dirs = [[0,1], [1,0], [1,1], [1,-1]];
        for (let [dr, dc] of dirs) {
            let count = 1;
            let r = row + dr, c = col + dc;
            while(r>=0 && r<BOARD_SIZE && c>=0 && c<BOARD_SIZE && board[r][c] === color) { count++; r+=dr; c+=dc; }
            r = row - dr; c = col - dc;
            while(r>=0 && r<BOARD_SIZE && c>=0 && c<BOARD_SIZE && board[r][c] === color) { count++; r-=dr; c-=dc; }
            if (count === 5) return true;
        }
        return false;
    }

    // --- 4. 🔥 흑돌 금수 규칙 (33 및 44) 판정 알고리즘 ---
    function checkForbiddenMove(row, col, color) {
        if (color !== 'black') return { forbidden: false, msg: '' }; 

        const dirs = [[0,1], [1,0], [1,1], [1,-1]];
        let openThreeCount = 0;
        let fourCount = 0;

        // 시뮬레이션을 위해 임시 착수
        board[row][col] = color;

        for (let [dr, dc] of dirs) {
            let line = Array(9).fill('');
            for (let i = -4; i <= 4; i++) {
                let r = row + dr * i;
                let c = col + dc * i;
                if (r >= 0 && r < BOARD_SIZE && c >= 0 && c < BOARD_SIZE) {
                    line[i + 4] = board[r][c];
                } else {
                    line[i + 4] = 'wall';
                }
            }

            let lineStr = line.map(v => v === '' ? '.' : (v === 'black' ? 'X' : 'O')).join('');

            // [A] 열린 3 (33 검사용 활구 감지)
            if (lineStr.includes('.XXX.') || lineStr.includes('.X.XX.') || lineStr.includes('.XX.X.')) {
                openThreeCount++;
            }

            // [B] 4 (44 검사용 모든 4 구조 감지: 닫힌 4, 열린 4 모두 포함)
            // .XXXX. (열린 4) 또는 OXXXX. / .XXXXO / X.XXX / XX.XX / XXX.X (닫힌 4 계열)
            // 이 중 한 곳만 더 두면 5가 완성되는 상태를 '4'라고 합니다.
            let isFour = false;
            // 9칸짜리 문자열에서 돌 하나를 뺐을 때 완벽한 연속 4개가 되는 변형 알고리즘 적용
            for (let i = 0; i < 9; i++) {
                if (line[i] === '') {
                    // 빈 공간에 가상으로 돌을 하나 더 놓았을 때 5개가 연속되는지 체크
                    line[i] = 'black';
                    let tempStr = line.map(v => v === '' ? '.' : (v === 'black' ? 'X' : 'O')).join('');
                    if (tempStr.includes('XXXXX')) {
                        isFour = true;
                    }
                    line[i] = ''; // 원상 복구
                }
            }
            if (isFour) fourCount++;
        }

        // 임시 착수 해제
        board[row][col] = '';

        // 최종 판단
        if (openThreeCount >= 2) {
            return { forbidden: true, msg: "⚠️ [금수] 흑돌은 33(쌍삼) 자리에 둘 수 없습니다!" };
        }
        if (fourCount >= 2) {
            return { forbidden: true, msg: "⚠️ [금수] 흑돌은 44(쌍사) 자리에 둘 수 없습니다!" };
        }

        return { forbidden: false, msg: '' };
    }

    // --- 5. 클릭 및 착수 이벤트 ---
    canvas.addEventListener('click', function(e) {
        if (winner) return;

        const rect = canvas.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;

        const col = Math.round((mouseX - PADDING) / CELL_SIZE);
        const row = Math.round((mouseY - PADDING) / CELL_SIZE);

        if (row >= 0 && row < BOARD_SIZE && col >= 0 && col < BOARD_SIZE) {
            if (board[row][col] === '') {
                
                // 금수 규칙 체크 (33, 44)
                let check = checkForbiddenMove(row, col, currentTurn);
                if (check.forbidden) {
                    statusBox.style.background = '#fee2e2'; statusBox.style.color = '#991b1b'; statusBox.style.borderColor = '#fca5a5';
                    statusBox.innerHTML = check.msg;
                    return;
                }

                // 돌 놓기
                board[row][col] = currentTurn;
                render();

                if (checkWin(row, col, currentTurn)) {
                    winner = currentTurn;
                    statusBox.style.background = '#dcfce7'; statusBox.style.color = '#15803d'; statusBox.style.borderColor = '#bbf7d0';
                    statusBox.innerHTML = `🎉 승리: ${winner === 'black' ? '흑돌(⚫)' : '백돌(⚪)'} 플레이어 승리!`;
                    return;
                }

                currentTurn = currentTurn === 'black' ? 'white' : 'black';
                statusBox.style.background = '#e0f2fe'; statusBox.style.color = '#0369a1'; statusBox.style.borderColor = '#bae6fd';
                statusBox.innerHTML = `🏃‍♂️ 현재 차례: ${currentTurn === 'black' ? '흑돌 (⚫)' : '백돌 (⚪)'}`;
            }
        }
    });

    // --- 6. 리셋 기능 ---
    resetBtn.addEventListener('click', function() {
        board = Array(BOARD_SIZE).fill(null).map(() => Array(BOARD_SIZE).fill(''));
        currentTurn = 'black'; winner = null;
        statusBox.style.background = '#e0f2fe'; statusBox.style.color = '#0369a1'; statusBox.style.borderColor = '#bae6fd';
        statusBox.innerHTML = "🏃‍♂️ 현재 차례: 흑돌 (⚫)";
        drawBoard();
    });

    drawBoard();
</script>
"""

components.html(js_code, height=600)

st.divider()
st.markdown("""
### 🧠 오목 정식 렌주룰(Renju Rule) 안내
* **정식 15x15 바둑판** 위에서 대국이 이루어집니다.
* 선공인 **흑돌(⚫)**은 너무 유리하기 때문에 **33(쌍삼)** 자리와 **44(쌍사)** 자리에 모두 돌을 둘 수 없습니다. 
* 후공인 **백돌(⚪)**은 아무런 제약이 없으므로 33, 44를 전략적으로 마음껏 활용하여 승리를 쟁취할 수 있습니다.
""")
