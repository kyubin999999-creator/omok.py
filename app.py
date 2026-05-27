import streamlit as st
import streamlit.components.v1 as components

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="방구석 3D 대국실", page_icon="🎲", layout="centered")

st.title("🎲 방구석 3D 보드게임 대국실 👑")
st.markdown("하나의 앱에서 즐기는 최고급 3D 그래픽 게임! 친구와 마주 앉아 명승부를 펼쳐보세요.")

# --- 스트림릿 내장 탭 기능으로 게임 분리 ---
tab1, tab2 = st.tabs(["⚫ 3D 정식 오목", "👑 3D 정통 체스"])

# ==============================================================================
# 🗂️ TAB 1: 3D 정식 오목 (33/44 금수 완벽판)
# ==============================================================================
with tab1:
    st.subheader("🥋 프로 규격 15x15 오목 (렌주룰 적용)")
    
    omok_js = """
    <div style="text-align: center; font-family: 'Malgun Gothic', sans-serif;">
        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 500px; margin: 0 auto 15px auto;">
            <div id="o-status" style="padding: 10px 15px; background: #e0f2fe; color: #0369a1; border-radius: 8px; font-weight: bold; font-size: 15px; border: 1px solid #bae6fd;">
                🏃‍♂️ 현재 차례: 흑돌 (⚫)
            </div>
            <button id="o-reset" style="padding: 10px 15px; background: #ef4444; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 13px;">
                🔄 게임 리셋
            </button>
        </div>
        <canvas id="omokCanvas" width="500" height="500" style="border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.15); cursor: pointer;"></canvas>
    </div>
    <script>
        const oCanvas = document.getElementById('omokCanvas');
        const oCtx = oCanvas.getContext('2d');
        const oStatus = document.getElementById('o-status');
        const oReset = document.getElementById('o-reset');

        const O_SIZE = 15; const O_PAD = 25;
        const O_CELL = (oCanvas.width - O_PAD * 2) / (O_SIZE - 1);
        let oBoard = Array(O_SIZE).fill(null).map(() => Array(O_SIZE).fill(''));
        let oTurn = 'black'; let oWinner = null;

        function drawOBoard() {
            oCtx.shadowBlur = 0; oCtx.shadowOffsetX = 0; oCtx.shadowOffsetY = 0;
            oCtx.fillStyle = '#eec590'; oCtx.fillRect(0, 0, oCanvas.width, oCanvas.height);
            oCtx.strokeStyle = '#5c4033'; oCtx.lineWidth = 1.2;
            for (let i = 0; i < O_SIZE; i++) {
                oCtx.beginPath(); oCtx.moveTo(O_PAD, O_PAD + i * O_CELL); oCtx.lineTo(oCanvas.width - O_PAD, O_PAD + i * O_CELL); oCtx.stroke();
                oCtx.beginPath(); oCtx.moveTo(O_PAD + i * O_CELL, O_PAD); oCtx.lineTo(O_PAD + i * O_CELL, oCanvas.height - O_PAD); oCtx.stroke();
            }
            oCtx.fillStyle = '#5c4033';
            [3, 7, 11].forEach(r => [3, 7, 11].forEach(c => {
                if((r===7&&c===7)||(r!==7&&c!==7)){ oCtx.beginPath(); oCtx.arc(O_PAD+c*O_CELL, O_PAD+r*O_CELL, 4, 0, Math.PI*2); oCtx.fill(); }
            }));
        }

        function drawOSymmetricStone(row, col, color) {
            const x = O_PAD + col * O_CELL; const y = O_PAD + row * O_CELL; const r = O_CELL * 0.44;
            oCtx.save(); oCtx.shadowColor = 'rgba(0,0,0,0.3)'; oCtx.shadowBlur = 4; oCtx.shadowOffsetX = 2; oCtx.shadowOffsetY = 3;
            oCtx.beginPath();
            let g = oCtx.createRadialGradient(x - r*0.3, y - r*0.3, r*0.05, x, y, r);
            if (color === 'black') { g.addColorStop(0, '#666'); g.addColorStop(0.2, '#222'); g.addColorStop(1, '#050505'); }
            else { g.addColorStop(0, '#fff'); g.addColorStop(0.5, '#eaeaea'); g.addColorStop(1, '#aaa'); }
            oCtx.fillStyle = g; oCtx.arc(x, y, r, 0, Math.PI * 2); oCtx.fill(); oCtx.restore();
        }

        function renderO() { drawOBoard(); for(let r=0; r<O_SIZE; r++) for(let c=0; c<O_SIZE; c++) if(oBoard[r][c]!=='') drawOSymmetricStone(r,c,oBoard[r][c]); }
        function checkOWin(r, c, col) {
            const dirs = [[0,1], [1,0], [1,1], [1,-1]];
            for (let [dr, dc] of dirs) {
                let cnt = 1;
                let nr = r + dr, nc = c + dc; while(nr>=0&&nr<O_SIZE&&nc>=0&&nc<O_SIZE&&oBoard[nr][nc]===col) { cnt++; nr+=dr; nc+=dc; }
                nr = r - dr; nc = c - dc; while(nr>=0&&nr<O_SIZE&&nc>=0&&nc<O_SIZE&&oBoard[nr][nc]===col) { cnt++; nr-=dr; nc-=dc; }
                if (cnt === 5) return true;
            }
            return false;
        }

        function checkForbidden(row, col, color) {
            if (color !== 'black') return false;
            oBoard[row][col] = color;
            let threes = 0, fours = 0;
            const dirs = [[0,1], [1,0], [1,1], [1,-1]];
            for (let [dr, dc] of dirs) {
                let segments = 0;
                for (let start = -4; start <= 0; start++) {
                    let match = 0, wall = false;
                    for (let i = 0; i < 5; i++) {
                        let nr = row + dr*(start+i), nc = col + dc*(start+i);
                        if (nr>=0&&nr<O_SIZE&&nc>=0&&nc<O_SIZE) { if(oBoard[nr][nc]===color) match++; else if(oBoard[nr][nc]!=='') { wall=true; break; } }
                        else { wall=true; break; }
                    }
                    if (!wall) {
                        let lr = row+dr*(start-1), lc = col+dc*(start-1), rr = row+dr*(start+5), rc = col+dc*(start+5);
                        let lOp = lr>=0&&lr<O_SIZE&&lc>=0&&lc<O_SIZE&&oBoard[lr][lc]==='';
                        let rOp = rr>=0&&rr<O_SIZE&&rc>=0&&rc<O_SIZE&&oBoard[rr][rc]==='';
                        if (match === 3 && lOp && rOp) segments = 1;
                        if (match === 4) segments = 1;
                    }
                }
                if (oBoard[row][col] === color) { // 가상 체크 카운트 분배
                    let m2=0; for(let i=-4; i<=4; i++) { let nr=row+dr*i, nc=col+dc*i; if(nr>=0&&nr<O_SIZE&&nc>=0&&nc<O_SIZE&&oBoard[nr][nc]===color) m2++; }
                    if(m2===3 && segments) threes++; if(m2===4 && segments) fours++;
                }
            }
            oBoard[row][col] = '';
            return { t3: threes >= 2, f4: fours >= 2 };
        }

        oCanvas.addEventListener('click', function(e) {
            if (oWinner) return;
            const rect = oCanvas.getBoundingClientRect();
            const col = Math.round((e.clientX - rect.left - O_PAD) / O_CELL);
            const row = Math.round((e.clientY - rect.top - O_PAD) / O_CELL);
            if (row>=0 && row<O_SIZE && col>=0 && col<O_SIZE && oBoard[row][col]==='') {
                let f = checkForbidden(row, col, oTurn);
                if (f.t3) { oStatus.style.background='#fee2e2'; oStatus.style.color='#991b1b'; oStatus.innerHTML="⚠️ 흑은 33 자리에 둘 수 없습니다!"; return; }
                if (f.f4) { oStatus.style.background='#fee2e2'; oStatus.style.color='#991b1b'; oStatus.innerHTML="⚠️ 흑은 44 자리에 둘 수 없습니다!"; return; }
                
                oBoard[row][col] = oTurn; renderO();
                if (checkOWin(row, col, oTurn)) {
                    oWinner = oTurn; oStatus.style.background='#dcfce7'; oStatus.style.color='#15803d';
                    oStatus.innerHTML = `🎉 승리: ${oWinner==='black'?'흑돌':'백돌'} 플레이어!`; return;
                }
                oTurn = oTurn === 'black' ? 'white' : 'black';
                oStatus.style.background='#e0f2fe'; oStatus.style.color='#0369a1';
                oStatus.innerHTML = `🏃‍♂️ 현재 차례: ${oTurn==='black'?'흑돌 (⚫)':'백돌 (⚪)'}`;
            }
        });

        oReset.addEventListener('click', function() {
            oBoard = Array(O_SIZE).fill(null).map(() => Array(O_SIZE).fill(''));
            oTurn = 'black'; oWinner = null; oStatus.style.background='#e0f2fe'; oStatus.style.color='#0369a1';
            oStatus.innerHTML = "🏃‍♂️ 현재 차례: 흑돌 (⚫)"; drawOBoard();
        });
        drawOBoard();
    </script>
    """
    components.html(omok_js, height=580)

# ==============================================================================
# 🗂️ TAB 2: 3D 정통 체스 (말 선택 및 실시간 행마법 연산)
# ==============================================================================
with tab2:
    st.subheader("👑 고급 대리석 질감의 3D 체스 대국장")
    
    chess_js = """
    <div style="text-align: center; font-family: 'Malgun Gothic', sans-serif;">
        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 500px; margin: 0 auto 15px auto;">
            <div id="c-status" style="padding: 10px 15px; background: #f3e8ff; color: #6b21a8; border-radius: 8px; font-weight: bold; font-size: 15px; border: 1px solid #e9d5ff;">
                ⚪ 백돌(White) 선공 차례입니다
            </div>
            <button id="c-reset" style="padding: 10px 15px; background: #ef4444; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 13px;">
                🔄 게임 리셋
            </button>
        </div>
        <canvas id="chessCanvas" width="500" height="500" style="border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.2); cursor: pointer;"></canvas>
    </div>

    <script>
        const cCanvas = document.getElementById('chessCanvas');
        const cCtx = cCanvas.getContext('2d');
        const cStatus = document.getElementById('c-status');
        const cReset = document.getElementById('c-reset');

        const C_CELL = cCanvas.width / 8;
        let cTurn = 'w'; // 'w': 백, 'b': 흑
        let selectedPiece = null; // {r, c} 형태

        // 정통 체스 초기 배치 대입
        let cBoard = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bP','bP','bP','bP','bP','bP','bP','bP'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['wP','wP','wP','wP','wP','wP','wP','wP'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR']
        ];

        // 기물 유니코드 맵 표기
        const pieceIcons = {
            'wK':'♔', 'wQ':'♕', 'wR':'♖', 'wB':'♗', 'wN':'♘', 'wP':'♙',
            'bK':'♚', 'bQ':'♛', 'bR':'♜', 'bB':'♝', 'bN':'♞', 'bP':'♟'
        };

        // --- 1. 3D 고급 대리석 체스판 렌더링 ---
        function drawChessBoard() {
            for (let r = 0; r < 8; r++) {
                for (let c = 0; c < 8; c++) {
                    // 번갈아 가며 밝은 칸, 어두운 칸 그라데이션 지정 (3D 깊이감)
                    let x = c * C_CELL; let y = r * C_CELL;
                    let g = cCtx.createLinearGradient(x, y, x + C_CELL, y + C_CELL);
                    
                    if ((r + c) % 2 === 0) {
                        g.addColorStop(0, '#f0d9b5'); g.addColorStop(1, '#e2c699'); // 밝은 대리석 색상
                    } else {
                        g.addColorStop(0, '#b58863'); g.addColorStop(1, '#9c6f4a'); // 어두운 원목 색상
                    }
                    cCtx.fillStyle = g; cCtx.fillRect(x, y, C_CELL, C_CELL);

                    // 선택된 기물 하이라이트 효과
                    if (selectedPiece && selectedPiece.r === r && selectedPiece.c === c) {
                        cCtx.fillStyle = 'rgba(255, 235, 59, 0.4)';
                        cCtx.fillRect(x, y, C_CELL, C_CELL);
                    }
                }
            }
        }

        // --- 2. 3D 구체/광원 레이어 입체 기물 텍스트 드로잉 ---
        function drawPieces() {
            cCtx.textAlign = 'center';
            cCtx.textBaseline = 'middle';
            cCtx.font = 'bold 36px "Segoe UI Symbol", sans-serif';

            for (let r = 0; r < 8; r++) {
                for (let c = 0; c < 8; c++) {
                    let p = cBoard[r][c];
                    if (p !== '') {
                        let x = c * C_CELL + C_CELL / 2;
                        let y = r * C_CELL + C_CELL / 2;

                        // [3D 디테일] 체스 말 하단 입체 그림자 효과 주입
                        cCtx.save();
                        cCtx.shadowColor = 'rgba(0, 0, 0, 0.4)';
                        cCtx.shadowBlur = 4; cCtx.shadowOffsetX = 2; cCtx.shadowOffsetY = 3;

                        // 입체 말 출력
                        cCtx.fillStyle = p[0] === 'w' ? '#ffffff' : '#1e1e1e';
                        // 검은 말 테두리 선 보정으로 가독성 확보
                        if(p[0]==='b') { cCtx.strokeStyle = '#fff'; cCtx.lineWidth = 1; cCtx.strokeText(pieceIcons[p], x, y); }
                        else { cCtx.strokeStyle = '#000'; cCtx.lineWidth = 1; cCtx.strokeText(pieceIcons[p], x, y); }
                        
                        cCtx.fillText(pieceIcons[p], x, y);
                        cCtx.restore();
                    }
                }
            }
        }

        function renderChess() { drawChessBoard(); drawPieces(); }

        // --- 3. 기본 행마법 검사 (간이 필터 알고리즘) ---
        function isValidMove(sr, sc, tr, tc, piece) {
            if (sr === tr && sc === tc) return false;
            let pType = piece[1]; let pColor = piece[0];
            let target = cBoard[tr][tc];
            if (target !== '' && target[0] === pColor) return false; // 아군 처단 금지

            let dr = tr - sr; let dc = tc - sc;

            switch(pType) {
                case 'P': // 폰 (단순 전진 및 대각 잡기 기초)
                    let dir = pColor === 'w' ? -1 : 1;
                    let startRow = pColor === 'w' ? 6 : 1;
                    if (dc === 0 && cBoard[tr][tc] === '') {
                        if (dr === dir) return true;
                        if (sr === startRow && dr === dir * 2 && cBoard[sr+dir][sc] === '') return true;
                    }
                    if (Math.abs(dc) === 1 && dr === dir && target !== '' && target[0] !== pColor) return true;
                    return false;
                case 'R': // 룩 (직선)
                    if (dr !== 0 && dc !== 0) return false;
                    return true; 
                case 'N': // 나이트 (L자 점프)
                    if ((Math.abs(dr)===2 && Math.abs(dc)===1) || (Math.abs(dr)===1 && Math.abs(dc)===2)) return true;
                    return false;
                case 'B': // 비숍 (대각선)
                    if (Math.abs(dr) !== Math.abs(dc)) return false;
                    return true;
                case 'Q': // 퀸 (직선 + 대각선)
                    if (dr !== 0 && dc !== 0 && Math.abs(dr) !== Math.abs(dc)) return false;
                    return true;
                case 'K': // 킹 (주변 1칸)
                    if (Math.abs(dr) <= 1 && Math.abs(dc) <= 1) return true;
                    return false;
            }
            return false;
        }

        // --- 4. 마우스 클릭 제어 ---
        cCanvas.addEventListener('click', function(e) {
            const rect = cCanvas.getBoundingClientRect();
            const c = Math.floor((e.clientX - rect.left) / C_CELL);
            const r = Math.floor((e.clientY - rect.top) / C_CELL);
            
            let clickedPiece = cBoard[r][c];

            if (selectedPiece === null) {
                // 내 말 선택하기
                if (clickedPiece !== '' && clickedPiece[0] === cTurn) {
                    selectedPiece = {r, c};
                    renderChess();
                }
            } else {
                // 이동 경로 입력하기
                let srcPiece = cBoard[selectedPiece.r][selectedPiece.c];
                if (isValidMove(selectedPiece.r, selectedPiece.c, r, c, srcPiece)) {
                    // 착수 및 이동 처리
                    cBoard[r][c] = srcPiece;
                    cBoard[selectedPiece.r][selectedPiece.c] = '';
                    
                    selectedPiece = null;
                    cTurn = cTurn === 'w' ? 'b' : 'w';
                    cStatus.style.background = cTurn === 'w' ? '#f3e8ff' : '#1e293b';
                    cStatus.style.color = cTurn === 'w' ? '#6b21a8' : '#f8fafc';
                    cStatus.innerHTML = cTurn === 'w' ? "⚪ 백돌(White) 차례입니다" : "⚫ 흑돌(Black) 차례입니다";
                } else {
                    // 취소 혹은 다른 아군 말 다시 선택
                    if (clickedPiece !== '' && clickedPiece[0] === cTurn) {
                        selectedPiece = {r, c};
                    } else {
                        selectedPiece = null;
                    }
                }
                renderChess();
            }
        });

        cReset.addEventListener('click', function() {
            cBoard = [
                ['bR','bN','bB','bQ','bK','bB','bN','bR'],
                ['bP','bP','bP','bP','bP','bP','bP','bP'],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['wP','wP','wP','wP','wP','wP','wP','wP'],
                ['wR','wN','wB','wQ','wK','wB','wN','wR']
            ];
            cTurn = 'w'; selectedPiece = null;
            cStatus.style.background = '#f3e8ff'; cStatus.style.color = '#6b21a8';
            cStatus.innerHTML = "⚪ 백돌(White) 선공 차례입니다";
            renderChess();
        });

        renderChess();
    </script>
    """
    components.html(chess_js, height=580)
    st.caption("💡 [말 조작 방법] 움직일 내 기물을 한 번 누르면 노랗게 하이라이트됩니다. 그 후 이동할 빈칸이나 적 기물을 누르면 이동(공격)합니다.")
