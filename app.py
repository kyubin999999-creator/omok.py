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

    // --- 4. 🛠️ 새롭고 확실한 33/44 열린 선 카운팅 알고리즘 ---
    // 특정 자리에 돌을 놓았을 때 활성화되는 '열린 n'의 개수를 세어줍니다.
    function countOpenLines(row, col, color, targetCount) {
        const dirs = [[0,1], [1,0], [1,1], [1,-1]];
        let lineCount = 0;

        for (let [dr, dc] of dirs) {
            let segments = [];
            // 해당 방향축으로 총 5개 연속이 만들어질 수 있는 모든 5칸 짜리 범위를 조사
            for (let start = -4; start <= 0; start++) {
                let match = 0;
                let emptySpaces = [];
                let hasOpponentOrWall = false;

                for (let i = 0; i < 5; i++) {
                    let r = row + dr * (start + i);
                    let c = col + dc * (start + i);

                    if (r >= 0 && r < BOARD_SIZE && c >= 0 && c < BOARD_SIZE) {
                        if (board[r][c] === color) {
                            match++;
                        } else if (board[r][c] === '') {
                            emptySpaces.push({r, c});
                        } else {
                            hasOpponentOrWall = true;
                            break;
                        }
                    } else {
                        hasOpponentOrWall = true;
                        break;
                    }
                }

                // 상대방 돌이나 벽으로 막히지 않고, 우리 돌이 원하는 개수만큼 들어가 있는 상태
                if (!hasOpponentOrWall && match === targetCount) {
                    // 양 끝이 열려있는지(활구인지) 추가 체크를 위한 검증
                    let leftR = row + dr * (start - 1);
                    let leftC = col + dc * (start - 1);
                    let rightR = row + dr * (start + 5);
                    let rightC = col + dc * (start + 5);

                    let leftOpen = leftR >= 0 && leftR < BOARD_SIZE && leftC >= 0 && leftC < BOARD_SIZE && board[leftR][leftC] === '';
                    let rightOpen = rightR >= 0 && rightR < BOARD_SIZE && rightC >= 0 && rightC < BOARD_SIZE && board[rightR][rightC] === '';
                    
                    if (targetCount === 3 && leftOpen && rightOpen) {
                        // 33은 '양쪽이 모두 열린 3'이어야 금수입니다.
                        if (!segments.includes(dr + "-" + dc)) {
                            segments.push(dr + "-" + dc);
                        }
                    } else if (targetCount === 4) {
                        // 44는 한쪽만 열려있어도(닫힌 4 포함) 하나 더 두면 5가 되므로 무조건 금수입니다.
                        if (!segments.includes(dr + "-" + dc)) {
                            segments.push(dr + "-" + dc);
                        }
                    }
                }
            }
            lineCount += segments.length;
        }
        return lineCount;
    }

    function checkForbiddenMove(row, col, color) {
        if (color !== 'black') return { forbidden: false, msg: '' };

        // 1. 임시 착수
        board[row][col] = color;

        // 2. 이 자리를 두어 동시에 만들어진 '열린 3'과 '4'의 개수를 파악
        // 자기가 방금 놓은 돌을 포함하여 계산하므로 targetCount는 각각 3과 4가 됩니다.
        let threes = countOpenLines(row, col, 'black', 3);
        let fours = countOpenLines(row, col, 'black', 4);

        // 3. 원상 복구
        board[row][col] = '';

        if (threes >= 2) {
            return { forbidden: true, msg: "⚠️ [금수] 흑돌은 33(쌍삼) 자리에 둘 수 없습니다!" };
        }
        if (fours >= 2) {
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
                
                // 금수 규칙 실시간 작동 체크
                let check = checkForbiddenMove(row, col, currentTurn);
                if (check.forbidden) {
                    statusBox.style.background = '#fee2e2'; statusBox.style.color = '#991b1b'; statusBox.style.borderColor = '#fca5a5';
                    statusBox.innerHTML = check.msg;
                    return; // 함수를 즉시 종료하여 돌이 안 놓이게 막음
                }

                // 통과되면 돌 놓기
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
