import streamlit as st
import streamlit.components.v1 as components

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="방구석 3D 마스터 대국실", page_icon="🎲", layout="centered")

st.title("🎲 3D 입체 타격감 보드게임 대국실 👑")
st.markdown("체스의 **폰 변신**, 체커의 **연속 콤보 사냥**, **킹 진화** 및 **가두기 패배 규칙**까지 완벽하게 적용된 최종 버전입니다.")

# --- 3개의 탭 구성 ---
tab1, tab2, tab3 = st.tabs(["⚫ 3D 정식 오목", "👑 3D 타격감 체스", "🏁 3D 타격감 체커"])

# ==============================================================================
# 🗂️ TAB 1: 3D 정식 오목 (렌주룰 33/44 금수 완벽 적용)
# ==============================================================================
with tab1:
    st.subheader("🥋 프로 규격 15x15 오목 (렌주룰 적용)")
    omok_js = """
    <div style="text-align: center; font-family: 'Malgun Gothic', sans-serif;">
        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 500px; margin: 0 auto 15px auto;">
            <div id="o-status" style="padding: 10px 15px; background: #e0f2fe; color: #0369a1; border-radius: 8px; font-weight: bold; font-size: 15px; border: 1px solid #bae6fd;">🏃‍♂️ 현재 차례: 흑돌 (⚫)</div>
            <button id="o-reset" style="padding: 10px 15px; background: #ef4444; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 13px;">🔄 게임 리셋</button>
        </div>
        <canvas id="omokCanvas" width="500" height="500" style="border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.15); cursor: pointer;"></canvas>
    </div>
    <script>
        const oCanvas = document.getElementById('omokCanvas'); const oCtx = oCanvas.getContext('2d');
        const oStatus = document.getElementById('o-status'); const oReset = document.getElementById('o-reset');
        const O_SIZE = 15; const O_PAD = 25; const O_CELL = (oCanvas.width - O_PAD * 2) / (O_SIZE - 1);
        let oBoard = Array(O_SIZE).fill(null).map(() => Array(O_SIZE).fill('')); let oTurn = 'black'; let oWinner = null;
        function drawOBoard() {
            oCtx.fillStyle = '#eec590'; oCtx.fillRect(0, 0, oCanvas.width, oCanvas.height); oCtx.strokeStyle = '#5c4033'; oCtx.lineWidth = 1.2;
            for (let i = 0; i < O_SIZE; i++) {
                oCtx.beginPath(); oCtx.moveTo(O_PAD, O_PAD + i * O_CELL); oCtx.lineTo(oCanvas.width - O_PAD, O_PAD + i * O_CELL); oCtx.stroke();
                oCtx.beginPath(); oCtx.moveTo(O_PAD + i * O_CELL, O_PAD); oCtx.lineTo(O_PAD + i * O_CELL, oCanvas.height - O_PAD); oCtx.stroke();
            }
            oCtx.fillStyle = '#5c4033'; [3, 7, 11].forEach(r => [3, 7, 11].forEach(c => { if((r===7&&c===7)||(r!==7&&c!==7)){ oCtx.beginPath(); oCtx.arc(O_PAD+c*O_CELL, O_PAD+r*O_CELL, 4, 0, Math.PI*2); oCtx.fill(); } }));
        }
        function drawOSymmetricStone(row, col, color) {
            const x = O_PAD + col * O_CELL; const y = O_PAD + row * O_CELL; const r = O_CELL * 0.44; oCtx.save(); oCtx.shadowColor = 'rgba(0,0,0,0.3)'; oCtx.shadowBlur = 4; oCtx.shadowOffsetX = 2; oCtx.shadowOffsetY = 3;
            oCtx.beginPath(); let g = oCtx.createRadialGradient(x - r*0.3, y - r*0.3, r*0.05, x, y, r); if (color === 'black') { g.addColorStop(0, '#666'); g.addColorStop(0.2, '#222'); g.addColorStop(1, '#050505'); } else { g.addColorStop(0, '#fff'); g.addColorStop(0.5, '#eaeaea'); g.addColorStop(1, '#aaa'); }
            oCtx.fillStyle = g; oCtx.arc(x, y, r, 0, Math.PI * 2); oCtx.fill(); oCtx.restore();
        }
        function renderO() { drawOBoard(); for(let r=0; r<O_SIZE; r++) for(let c=0; c<O_SIZE; c++) if(oBoard[r][c]!=='') drawOSymmetricStone(r,c,oBoard[r][c]); }
        function checkOWin(r, c, col) {
            const dirs = [[0,1], [1,0], [1,1], [1,-1]];
            for (let [dr, dc] of dirs) {
                let cnt = 1; let nr = r + dr, nc = c + dc; while(nr>=0&&nr<O_SIZE&&nc>=0&&nc<O_SIZE&&oBoard[nr][nc]===col) { cnt++; nr+=dr; nc+=dc; }
                nr = r - dr; nc = c - dc; while(nr>=0&&nr<O_SIZE&&nc>=0&&nc<O_SIZE&&oBoard[nr][nc]===col) { cnt++; nr-=dr; nc-=dc; } if (cnt === 5) return true;
            } return false;
        }
        function checkForbidden(row, col, color) {
            if (color !== 'black') return false; oBoard[row][col] = color; let threes = 0, fours = 0; const dirs = [[0,1], [1,0], [1,1], [1,-1]];
            for (let [dr, dc] of dirs) {
                let segments = 0; for (let start = -4; start <= 0; start++) {
                    let match = 0, wall = false; for (let i = 0; i < 5; i++) {
                        let nr = row + dr*(start+i), nc = col + dc*(start+i); if (nr>=0&&nr<O_SIZE&&nc>=0&&nc<O_SIZE) { if(oBoard[nr][nc]===color) match++; else if(oBoard[nr][nc]!=='') { wall=true; break; } } else { wall=true; break; }
                    }
                    if (!wall) {
                        let lr = row+dr*(start-1), lc = col+dc*(start-1), rr = row+dr*(start+5), rc = col+dc*(start+5);
                        let lOp = lr>=0&&lr<O_SIZE&&lc>=0&&lc<O_SIZE&&oBoard[lr][lc]===''; let rOp = rr>=0&&rr<O_SIZE&&rc>=0&&rc<O_SIZE&&oBoard[rr][rc]==='';
                        if (match === 3 && lOp && rOp) segments = 1; if (match === 4) segments = 1;
                    }
                }
                if (oBoard[row][col] === color) { let m2=0; for(let i=-4; i<=4; i++) { let nr=row+dr*i, nc=col+dc*i; if(nr>=0&&nr<O_SIZE&&nc>=0&&nc<O_SIZE&&oBoard[nr][nc]===color) m2++; } if(m2===3 && segments) threes++; if(m2===4 && segments) fours++; }
            } oBoard[row][col] = ''; return { t3: threes >= 2, f4: fours >= 2 };
        }
        oCanvas.addEventListener('click', function(e) {
            if (oWinner) return; const rect = oCanvas.getBoundingClientRect(); const col = Math.round((e.clientX - rect.left - O_PAD) / O_CELL); const row = Math.round((e.clientY - rect.top - O_PAD) / O_CELL);
            if (row>=0 && row<O_SIZE && col>=0 && col<O_SIZE && oBoard[row][col]==='') {
                let f = checkForbidden(row, col, oTurn); if (f.t3) { oStatus.style.background='#fee2e2'; oStatus.style.color='#991b1b'; oStatus.innerHTML="⚠️ 흑은 33 자리에 둘 수 없습니다!"; return; } if (f.f4) { oStatus.style.background='#fee2e2'; oStatus.style.color='#991b1b'; oStatus.innerHTML="⚠️ 흑은 44 자리에 둘 수 없습니다!"; return; }
                oBoard[row][col] = oTurn; renderO(); if (checkOWin(row, col, oTurn)) { oWinner = oTurn; oStatus.style.background='#dcfce7'; oStatus.style.color='#15803d'; oStatus.innerHTML = `🎉 승리: ${oWinner==='black'?'흑돌':'백돌'} 플레이어!`; return; }
                oTurn = oTurn === 'black' ? 'white' : 'black'; oStatus.style.background='#e0f2fe'; oStatus.style.color='#0369a1'; oStatus.innerHTML = `🏃‍♂️ 현재 차례: ${oTurn==='black'?'흑돌 (⚫)':'백돌 (⚪)'}`;
            }
        });
        oReset.addEventListener('click', function() { oBoard = Array(O_SIZE).fill(null).map(() => Array(O_SIZE).fill('')); oTurn = 'black'; oWinner = null; oStatus.style.background='#e0f2fe'; oStatus.style.color='#0369a1'; oStatus.innerHTML = "🏃‍♂️ 현재 차례: 흑돌 (⚫)"; drawOBoard(); });
        drawOBoard();
    </script>
    """
    components.html(omok_js, height=580)

# ==============================================================================
# 🗂️ TAB 2: 3D 타격감 체스 (이동/사냥 가이드 가시성 유지 + 폰 퀸 자동 승격)
# ==============================================================================
with tab2:
    st.subheader("👑 이동/사냥 시각 가이드 및 폰 퀸 변신(Promotion)이 도입된 3D 체스")
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
        <canvas id="chessCanvas" width="500" height="500" style="border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.3); cursor: pointer; background: #000;"></canvas>
    </div>

    <script>
        const cCanvas = document.getElementById('chessCanvas'); const cCtx = cCanvas.getContext('2d');
        const cStatus = document.getElementById('c-status'); const cReset = document.getElementById('c-reset');
        const C_CELL = cCanvas.width / 8; let cTurn = 'w'; let selectedPiece = null; let cWinner = null;
        let shakeTime = 0; let shakeIntensity = 0; let particles = [];
        let movedPieces = { 'wK': false, 'wR_left': false, 'wR_right': false, 'bK': false, 'bR_left': false, 'bR_right': false };

        let cBoard = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'], ['bP','bP','bP','bP','bP','bP','bP','bP'],
            ['','','','','','','',''], ['','','','','','','',''], ['','','','','','','',''], ['','','','','','','',''],
            ['wP','wP','wP','wP','wP','wP','wP','wP'], ['wR','wN','wB','wQ','wK','wB','wN','wR']
        ];
        const pieceIcons = { 'wK':'♔', 'wQ':'♕', 'wR':'♖', 'wB':'♗', 'wN':'♘', 'wP':'♙', 'bK':'♚', 'bQ':'♛', 'bR':'♜', 'bB':'♝', 'bN':'♞', 'bP':'♟' };

        function createExplosion(x, y, pieceType) {
            let count = pieceType === 'K' || pieceType === 'Q' ? 60 : 30; shakeTime = 15; shakeIntensity = pieceType === 'K' ? 15 : 6;
            for (let i = 0; i < count; i++) {
                let angle = Math.random() * Math.PI * 2; let speed = Math.random() * 5 + 2;
                particles.push({ x, y, vx: Math.cos(angle)*speed, vy: Math.sin(angle)*speed, radius: Math.random()*4+2, alpha: 1, decay: Math.random()*0.02+0.015, color: ['#ff4500','#ff8c00','#ffd700','#ffffff'][Math.floor(Math.random()*4)] });
            }
        }

        function isValidMove(sr, sc, tr, tc, piece) {
            if (sr === tr && sc === tc) return false; let pType = piece[1]; let pColor = piece[0]; let target = cBoard[tr][tc]; if (target !== '' && target[0] === pColor) return false; 
            let dr = tr - sr; let dc = tc - sc; let stepR = dr === 0 ? 0 : dr / Math.abs(dr); let stepC = dc === 0 ? 0 : dc / Math.abs(dc);
            if (pType === 'K' && Math.abs(dc) === 2 && dr === 0) {
                if (movedPieces[pColor + 'K']) return false; 
                if (dc === 2 && sc === 4) { if (movedPieces[pColor + 'R_right']) return false; if (cBoard[sr][5] === '' && cBoard[sr][6] === '') return 'castling_right'; }
                if (dc === -2 && sc === 4) { if (movedPieces[pColor + 'R_left']) return false; if (cBoard[sr][1] === '' && cBoard[sr][2] === '' && cBoard[sr][3] === '') return 'castling_left'; }
                return false;
            }
            if (pType === 'R' || pType === 'B' || pType === 'Q') {
                if (pType === 'R' && dr !== 0 && dc !== 0) return false; if (pType === 'B' && Math.abs(dr) !== Math.abs(dc)) return false; if (pType === 'Q' && dr !== 0 && dc !== 0 && Math.abs(dr) !== Math.abs(dc)) return false;
                let currR = sr + stepR; let currC = sc + stepC; while (currR !== tr || currC !== tc) { if (cBoard[currR][currC] !== '') return false; currR += stepR; currC += stepC; } return true;
            }
            switch(pType) {
                case 'P': 
                    let dir = pColor === 'w' ? -1 : 1; let startRow = pColor === 'w' ? 6 : 1;
                    if (dc === 0 && cBoard[tr][tc] === '') { if (dr === dir) return true; if (sr === startRow && dr === dir * 2 && cBoard[sr+dir][sc] === '') return true; }
                    if (Math.abs(dc) === 1 && dr === dir && target !== '' && target[0] !== pColor) return true; return false;
                case 'N': if ((Math.abs(dr)===2 && Math.abs(dc)===1) || (Math.abs(dr)===1 && Math.abs(dc)===2)) return true; return false;
                case 'K': if (Math.abs(dr) <= 1 && Math.abs(dc) <= 1) return true; return false;
            } return false;
        }

        function drawChessBoard() {
            for (let r = 0; r < 8; r++) {
                for (let c = 0; c < 8; c++) {
                    let x = c * C_CELL; let y = r * C_CELL; let g = cCtx.createLinearGradient(x, y, x + C_CELL, y + C_CELL);
                    if ((r + c) % 2 === 0) { g.addColorStop(0, '#f0d9b5'); g.addColorStop(1, '#e2c699'); } else { g.addColorStop(0, '#b58863'); g.addColorStop(1, '#9c6f4a'); }
                    cCtx.fillStyle = g; cCtx.fillRect(x, y, C_CELL, C_CELL);
                    if (selectedPiece && selectedPiece.r === r && selectedPiece.c === c) { cCtx.fillStyle = 'rgba(255, 235, 59, 0.45)'; cCtx.fillRect(x, y, C_CELL, C_CELL); }
                    if (selectedPiece) {
                        let srcPiece = cBoard[selectedPiece.r][selectedPiece.c]; let moveType = isValidMove(selectedPiece.r, selectedPiece.c, r, c, srcPiece);
                        if (moveType) {
                            let targetPiece = cBoard[r][c];
                            if (targetPiece !== '') { cCtx.fillStyle = 'rgba(239, 68, 68, 0.35)'; cCtx.fillRect(x, y, C_CELL, C_CELL); cCtx.strokeStyle = '#ef4444'; cCtx.lineWidth = 3; cCtx.strokeRect(x+1.5, y+1.5, C_CELL-3, C_CELL-3); } 
                            else {
                                if (moveType === 'castling_right' || moveType === 'castling_left') { cCtx.fillStyle = 'rgba(33, 150, 243, 0.3)'; cCtx.fillRect(x, y, C_CELL, C_CELL); cCtx.beginPath(); cCtx.arc(x + C_CELL/2, y + C_CELL/2, 7, 0, Math.PI * 2); cCtx.fillStyle = '#1976d2'; cCtx.fill(); } 
                                else { cCtx.fillStyle = 'rgba(76, 175, 80, 0.2)'; cCtx.fillRect(x, y, C_CELL, C_CELL); cCtx.beginPath(); cCtx.arc(x + C_CELL/2, y + C_CELL/2, 6, 0, Math.PI * 2); cCtx.fillStyle = '#2e7d32'; cCtx.fill(); }
                            }
                        }
                    }
                }
            }
        }

        function drawPieces() {
            cCtx.textAlign = 'center'; cCtx.textBaseline = 'middle'; cCtx.font = 'bold 36px "Segoe UI Symbol", sans-serif';
            for (let r = 0; r < 8; r++) {
                for (let c = 0; c < 8; c++) {
                    let p = cBoard[r][c];
                    if (p !== '') {
                        let x = c * C_CELL + C_CELL / 2; let y = r * C_CELL + C_CELL / 2; cCtx.save();
                        if (p[0] !== cTurn && !cWinner) { cCtx.globalAlpha = 0.35; } else { cCtx.globalAlpha = 1.0; }
                        cCtx.shadowColor = 'rgba(0, 0, 0, 0.4)'; cCtx.shadowBlur = 4; cCtx.shadowOffsetX = 2; cCtx.shadowOffsetY = 3; cCtx.fillStyle = p[0] === 'w' ? '#ffffff' : '#1e1e1e';
                        if(p[0]==='b') { cCtx.strokeStyle = '#fff'; cCtx.lineWidth = 1; cCtx.strokeText(pieceIcons[p], x, y); } else { cCtx.strokeStyle = '#000'; cCtx.lineWidth = 1; cCtx.strokeText(pieceIcons[p], x, y); }
                        cCtx.fillText(pieceIcons[p], x, y); cCtx.restore();
                    }
                }
            }
        }

        function updateAndDrawParticles() {
            for (let i = particles.length - 1; i >= 0; i--) {
                let p = particles[i]; p.x += p.vx; p.y += p.vy; p.alpha -= p.decay; if (p.alpha <= 0) { particles.splice(i, 1); continue; }
                cCtx.save(); cCtx.globalAlpha = p.alpha; cCtx.shadowBlur = 8; cCtx.shadowColor = p.color; cCtx.beginPath(); cCtx.arc(p.x, p.y, p.radius, 0, Math.PI*2); cCtx.fillStyle = p.color; cCtx.fill(); cCtx.restore();
            }
        }

        function drawGameOverOverlay() {
            if (!cWinner) return;
            let overlayGrad = cCtx.createRadialGradient(cCanvas.width/2, cCanvas.height/2, 50, cCanvas.width/2, cCanvas.height/2, cCanvas.width*0.7); overlayGrad.addColorStop(0, 'rgba(15, 23, 42, 0.88)'); overlayGrad.addColorStop(1, 'rgba(2, 6, 23, 0.99)'); cCtx.fillStyle = overlayGrad; cCtx.fillRect(0, 0, cCanvas.width, cCanvas.height);
            cCtx.textAlign = 'center'; cCtx.textBaseline = 'middle'; cCtx.save(); cCtx.shadowColor = '#ef4444'; cCtx.shadowBlur = 20; cCtx.font = 'bold 54px "Impact", "Arial Black", sans-serif'; cCtx.fillStyle = '#ef4444'; cCtx.fillText('GAME OVER', cCanvas.width / 2, cCanvas.height / 2 - 40); cCtx.restore();
            cCtx.save(); cCtx.font = 'bold 22px "Malgun Gothic", sans-serif'; cCtx.fillStyle = '#f8fafc'; cCtx.shadowColor = 'rgba(255, 255, 255, 0.3)'; cCtx.shadowBlur = 4; let winnerText = cWinner === 'w' ? '👑 백돌 플레이어 승리 👑' : '👑 흑돌 플레이어 승리 👑'; cCtx.fillText(winnerText, cCanvas.width / 2, cCanvas.height / 2 + 30);
            cCtx.font = '14px "Malgun Gothic", sans-serif'; cCtx.fillStyle = '#94a3b8'; cCtx.fillText('상단의 [게임 리셋] 버튼을 누르면 재경기가 가능합니다.', cCanvas.width / 2, cCanvas.height / 2 + 80); cCtx.restore();
        }

        function gameLoop() {
            cCtx.clearRect(0, 0, cCanvas.width, cCanvas.height); cCtx.save();
            if (shakeTime > 0) { cCtx.translate((Math.random()-0.5)*shakeIntensity, (Math.random()-0.5)*shakeIntensity); shakeTime--; }
            drawChessBoard(); drawPieces(); cCtx.restore(); updateAndDrawParticles(); drawGameOverOverlay(); requestAnimationFrame(gameLoop);
        }

        cCanvas.addEventListener('click', function(e) {
            if (cWinner) return; const rect = cCanvas.getBoundingClientRect(); const c = Math.floor((e.clientX - rect.left) / C_CELL); const r = Math.floor((e.clientY - rect.top) / C_CELL); let clickedPiece = cBoard[r][c];
            if (selectedPiece === null) { if (clickedPiece !== '' && clickedPiece[0] === cTurn) { selectedPiece = {r, c}; } } 
            else {
                let srcPiece = cBoard[selectedPiece.r][selectedPiece.c]; let moveType = isValidMove(selectedPiece.r, selectedPiece.c, r, c, srcPiece);
                if (moveType) {
                    let pColor = srcPiece[0]; let targetPiece = cBoard[r][c];
                    if (moveType === 'castling_right') { cBoard[r][c] = srcPiece; cBoard[selectedPiece.r][selectedPiece.c] = ''; cBoard[r][5] = pColor + 'R'; cBoard[r][7] = ''; } 
                    else if (moveType === 'castling_left') { cBoard[r][c] = srcPiece; cBoard[selectedPiece.r][selectedPiece.c] = ''; cBoard[r][3] = pColor + 'R'; cBoard[r][0] = ''; } 
                    else { 
                        if (targetPiece !== '') { createExplosion(c*C_CELL+C_CELL/2, r*C_CELL+C_CELL/2, targetPiece[1]); if (targetPiece[1] === 'K') cWinner = cTurn; } 
                        if (srcPiece[1] === 'P' && (r === 0 || r === 7)) { cBoard[r][c] = pColor + 'Q'; } else { cBoard[r][c] = srcPiece; }
                        cBoard[selectedPiece.r][selectedPiece.c] = ''; 
                    }
                    if (srcPiece === 'wK') movedPieces['wK'] = true; if (srcPiece === 'bK') movedPieces['bK'] = true;
                    selectedPiece = null;
                    if (cWinner) { cStatus.style.background = '#dcfce7'; cStatus.style.color = '#15803d'; cStatus.innerHTML = `🎉 대국 종료! ${cWinner === 'w' ? '백돌' : '흑돌'} 승리!`; } 
                    else { cTurn = cTurn === 'w' ? 'b' : 'w'; cStatus.style.background = cTurn === 'w' ? '#f3e8ff' : '#1e293b'; cTurn === 'w' ? cStatus.style.color = '#6b21a8' : cStatus.style.color = '#f8fafc'; cStatus.innerHTML = cTurn === 'w' ? "⚪ 백돌(White) 차례입니다" : "⚫ 흑돌(Black) 차례입니다"; }
                } else { if (clickedPiece !== '' && clickedPiece[0] === cTurn) { selectedPiece = {r, c}; } else { selectedPiece = null; } }
            }
        });
        cReset.addEventListener('click', function() { location.reload(); });
        gameLoop();
    </script>
    """
    components.html(chess_js, height=580)

# ==============================================================================
# 🗂️ TAB 3: 3D 타격감 체커 (🔥 연속 콤보 사냥 + 킹 진화 + 가두기Blocked 판정 탑재)
# ==============================================================================
with tab3:
    st.subheader("🏁 콤보 연타 사냥, 킹(👑) 진화 및 가두기 차단 규칙이 반영된 3D 체커")
    checkers_js = """
    <div style="text-align: center; font-family: 'Malgun Gothic', sans-serif;">
        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 500px; margin: 0 auto 15px auto;">
            <div id="ck-status" style="padding: 10px 15px; background: #fee2e2; color: #991b1b; border-radius: 8px; font-weight: bold; font-size: 15px; border: 1px solid #fca5a5;">
                🔴 레드(Red) 플레이어 차례입니다
            </div>
            <button id="ck-reset" style="padding: 10px 15px; background: #ef4444; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 13px;">
                🔄 게임 리셋
            </button>
        </div>
        <canvas id="ckCanvas" width="500" height="500" style="border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.3); cursor: pointer; background: #000;"></canvas>
    </div>

    <script>
        const ckCanvas = document.getElementById('ckCanvas'); const ckCtx = ckCanvas.getContext('2d');
        const ckStatus = document.getElementById('ck-status'); const ckReset = document.getElementById('ck-reset');
        const CK_CELL = ckCanvas.width / 8;
        let ckTurn = 'r'; let ckSel = null; let ckWinner = null;
        let ckShakeTime = 0; let ckParticles = [];
        let comboMode = false;

        let ckBoard = Array(8).fill(null).map(() => Array(8).fill(''));
        for(let r=0; r<3; r++) for(let c=0; c<8; c++) if((r+c)%2===1) ckBoard[r][c] = 'b';
        for(let r=5; r<8; r++) for(let c=0; c<8; c++) if((r+c)%2===1) ckBoard[r][c] = 'r';

        function createCkExplosion(x, y) {
            ckShakeTime = 15;
            for (let i = 0; i < 35; i++) {
                let angle = Math.random() * Math.PI * 2; let speed = Math.random() * 5 + 2;
                ckParticles.push({ x, y, vx: Math.cos(angle)*speed, vy: Math.sin(angle)*speed, radius: Math.random()*4+2, alpha: 1, decay: Math.random()*0.02+0.015, color: ['#ff3b30','#ff9500','#ffcc00'][Math.floor(Math.random()*3)] });
            }
        }

        function isValidCkMove(sr, sc, tr, tc, p) {
            if (ckBoard[tr][tc] !== '') return false;
            let dr = tr - sr; let dc = tc - sc;
            let isKing = p.length === 2; let baseColor = p[0];

            if (!comboMode && Math.abs(dc) === 1) {
                if (isKing && Math.abs(dr) === 1) return { jump: false };
                if (!isKing && dr === (baseColor === 'r' ? -1 : 1)) return { jump: false };
            }
            if (Math.abs(dc) === 2) {
                let validRowJump = false;
                if (isKing && Math.abs(dr) === 2) validRowJump = true;
                if (!isKing && dr === (baseColor === 'r' ? -2 : 2)) validRowJump = true;

                if (validRowJump) {
                    let midR = sr + (dr / 2); let midC = sc + (dc / 2);
                    let target = ckBoard[midR][midC];
                    if (target !== '' && target[0] !== baseColor) { return { jump: true, mr: midR, mc: midC }; }
                }
            }
            return false;
        }

        function hasMoreJumps(r, c, p) {
            let scanTargets = [[2,2], [2,-2], [-2,2], [-2,-2]];
            for (let [dr, dc] of scanTargets) {
                let tr = r + dr; let tc = c + dc;
                if (tr >= 0 && tr < 8 && tc >= 0 && tc < 8) { if (isValidCkMove(r, c, tr, tc, p)?.jump) return true; }
            } return false;
        }

        function drawCkBoard() {
            for (let r = 0; r < 8; r++) {
                for (let c = 0; c < 8; c++) {
                    let x = c * CK_CELL; let y = r * CK_CELL;
                    ckCtx.fillStyle = (r + c) % 2 === 0 ? '#f0d9b5' : '#2b2b2b'; ckCtx.fillRect(x, y, CK_CELL, CK_CELL);
                    if (ckSel && ckSel.r === r && ckSel.c === c) { ckCtx.fillStyle = 'rgba(255, 235, 59, 0.4)'; ckCtx.fillRect(x, y, CK_CELL, CK_CELL); }
                    if (ckSel) {
                        let res = isValidCkMove(ckSel.r, ckSel.c, r, c, ckBoard[ckSel.r][ckSel.c]);
                        if (res) {
                            if (res.jump) {
                                ckCtx.fillStyle = 'rgba(239, 68, 68, 0.35)'; ckCtx.fillRect(x, y, CK_CELL, CK_CELL);
                                ckCtx.strokeStyle = '#ef4444'; ckCtx.lineWidth = 3; ckCtx.strokeRect(x+1.5, y+1.5, CK_CELL-3, CK_CELL-3);
                            } else { ckCtx.fillStyle = 'rgba(76, 175, 80, 0.25)'; ckCtx.fillRect(x, y, CK_CELL, CK_CELL); }
                        }
                    }
                }
            }
        }

        function drawCkPieces() {
            for (let r = 0; r < 8; r++) {
                for (let c = 0; c < 8; c++) {
                    let p = ckBoard[r][c];
                    if (p !== '') {
                        let x = c * CK_CELL + CK_CELL / 2; let y = r * CK_CELL + CK_CELL / 2; ckCtx.save();
                        if (p[0] !== ckTurn && !ckWinner) { ckCtx.globalAlpha = 0.35; } else { ckCtx.globalAlpha = 1.0; }
                        ckCtx.shadowColor = 'rgba(0, 0, 0, 0.5)'; ckCtx.shadowBlur = 6; ckCtx.shadowOffsetX = 2; ckCtx.shadowOffsetY = 4;
                        ckCtx.beginPath(); ckCtx.arc(x, y, CK_CELL * 0.38, 0, Math.PI * 2);
                        ckCtx.fillStyle = p[0] === 'r' ? '#ef4444' : '#1e293b'; ckCtx.fill();
                        ckCtx.strokeStyle = '#fff'; ckCtx.lineWidth = 2; ckCtx.stroke();
                        if (p.length === 2) { ckCtx.font = '16px serif'; ckCtx.fillStyle = '#ffd700'; ckCtx.textAlign = 'center'; ckCtx.textBaseline = 'middle'; ckCtx.fillText('👑', x, y); } 
                        else { ckCtx.beginPath(); ckCtx.arc(x, y, CK_CELL * 0.22, 0, Math.PI * 2); ckCtx.strokeStyle = 'rgba(255,255,255,0.4)'; ckCtx.lineWidth = 1.5; ckCtx.stroke(); }
                        ckCtx.restore();
                    }
                }
            }
        }

        function updateCkParticles() {
            for (let i = ckParticles.length - 1; i >= 0; i--) {
                let p = ckParticles[i]; p.x += p.vx; p.y += p.vy; p.alpha -= p.decay; if (p.alpha <= 0) { ckParticles.splice(i, 1); continue; }
                ckCtx.save(); ckCtx.globalAlpha = p.alpha; ckCtx.shadowBlur = 8; ckCtx.shadowColor = p.color; ckCtx.beginPath(); ckCtx.arc(p.x, p.y, p.radius, 0, Math.PI*2); ckCtx.fillStyle = p.color; ckCtx.fill(); ckCtx.restore();
            }
        }

        function drawCkGameOver() {
            if (!ckWinner) return;
            let grad = ckCtx.createRadialGradient(ckCanvas.width/2, ckCanvas.height/2, 50, ckCanvas.width/2, ckCanvas.height/2, ckCanvas.width*0.7); grad.addColorStop(0, 'rgba(15, 23, 42, 0.9)'); grad.addColorStop(1, 'rgba(2, 6, 23, 0.98)'); ckCtx.fillStyle = grad; ckCtx.fillRect(0, 0, ckCanvas.width, ckCanvas.height);
            ckCtx.textAlign = 'center'; ckCtx.textBaseline = 'middle'; ckCtx.save(); ckCtx.shadowColor = '#ef4444'; ckCtx.shadowBlur = 20; ckCtx.font = 'bold 54px "Impact", sans-serif'; ckCtx.fillStyle = '#ef4444'; ckCtx.fillText('GAME OVER', ckCanvas.width / 2, ckCanvas.height / 2 - 40); ckCtx.restore();
            ckCtx.font = 'bold 22px "Malgun Gothic", sans-serif'; ckCtx.fillStyle = '#f8fafc'; let txt = ckWinner === 'r' ? '👑 RED PLAYER WIN 👑' : '👑 BLACK PLAYER WIN 👑'; ckCtx.fillText(txt, ckCanvas.width / 2, ckCanvas.height / 2 + 30);
        }

        function ckLoop() {
            ckCtx.clearRect(0, 0, ckCanvas.width, ckCanvas.height); ckCtx.save(); if (ckShakeTime > 0) { ckCtx.translate((Math.random()-0.5)*8, (Math.random()-0.5)*8); ckShakeTime--; }
            drawCkBoard(); drawCkPieces(); ckCtx.restore(); updateCkParticles(); drawCkGameOver(); requestAnimationFrame(ckLoop);
        }

        ckCanvas.addEventListener('click', function(e) {
            if (ckWinner) return; const rect = ckCanvas.getBoundingClientRect(); const c = Math.floor((e.clientX - rect.left) / CK_CELL); const r = Math.floor((e.clientY - rect.top) / CK_CELL); let p = ckBoard[r][c];

            if (ckSel === null) { if (p !== '' && p[0] === ckTurn && !comboMode) { ckSel = {r, c}; } } 
            else {
                let movingPiece = ckBoard[ckSel.r][ckSel.c]; let res = isValidCkMove(ckSel.r, ckSel.c, r, c, movingPiece);
                if (res) {
                    if (res.jump) { ckBoard[res.mr][res.mc] = ''; createCkExplosion(res.mc*CK_CELL+CK_CELL/2, res.mr*CK_CELL+CK_CELL/2); }
                    ckBoard[r][c] = movingPiece; ckBoard[ckSel.r][ckSel.c] = '';
                    if (ckTurn === 'r' && r === 0 && movingPiece === 'r') { ckBoard[r][c] = 'rK'; movingPiece = 'rK'; }
                    if (ckTurn === 'b' && r === 7 && movingPiece === 'b') { ckBoard[r][c] = 'bK'; movingPiece = 'bK'; }

                    if (res.jump && hasMoreJumps(r, c, movingPiece)) {
                        comboMode = true; ckSel = { r, c };
                        ckStatus.style.background = '#fef08a'; ckStatus.style.color = '#854d0e'; ckStatus.innerHTML = `🔥 연속 콤보 사냥 찬스! 추가로 적을 격파하세요!`;
                        return;
                    }
                    comboMode = false; ckSel = null;

                    // --- ⚙️ 정밀 승리 및 블로킹(Blocked) 탐지 엔진 ---
                    let rCount = 0; let bCount = 0;
                    for(let i=0; i<8; i++) for(let j=0; j<8; j++) { if(ckBoard[i][j][0]==='r') rCount++; if(ckBoard[i][j][0]==='b') bCount++; }

                    if (rCount === 0) { ckWinner = 'b'; }
                    else if (bCount === 0) { ckWinner = 'r'; }
                    else {
                        let nextTurn = (ckTurn === 'r' ? 'b' : 'r'); let hasValidMove = false;
                        for(let i=0; i<8; i++) {
                            for(let j=0; j<8; j++) {
                                if(ckBoard[i][j] !== '' && ckBoard[i][j][0] === nextTurn) {
                                    let testMoves = [[1,1], [1,-1], [-1,1], [-1,-1], [2,2], [2,-2], [-2,2], [-2,-2]];
                                    for(let [dr, dc] of testMoves) {
                                        let tr = i + dr; let tc = j + dc;
                                        if(tr >= 0 && tr < 8 && tc >= 0 && tc < 8) {
                                            if(isValidCkMove(i, j, tr, tc, ckBoard[i][j])) { hasValidMove = true; break; }
                                        }
                                    }
                                } if(hasValidMove) break;
                            } if(hasValidMove) break;
                        }
                        if(!hasValidMove) { ckWinner = ckTurn; } // 다음 사람이 이동 불가능하면 현재 플레이어 패승!
                    }

                    if (!ckWinner) {
                        ckTurn = ckTurn === 'r' ? 'b' : 'r';
                        ckStatus.style.background = ckTurn === 'r' ? '#fee2e2' : '#1e293b'; ckStatus.style.color = ckTurn === 'r' ? '#991b1b' : '#f8fafc';
                        ckStatus.innerHTML = ckTurn === 'r' ? "🔴 레드(Red) 플레이어 차례입니다" : "⚫ 블랙(Black) 플레이어 차례입니다";
                    } else {
                        ckStatus.style.background = '#dcfce7'; ckStatus.style.color = '#15803d';
                        ckStatus.innerHTML = `🎉 대국 종료! 기물 전멸 혹은 사방을 완벽히 가둬버린 [${ckWinner==='r'?'레드':'블랙'}]의 짜릿한 승리입니다!`;
                    }
                } else { if (!comboMode && p !== '' && p[0] === ckTurn) { ckSel = {r, c}; } else if (!comboMode) { ckSel = null; } }
            }
        });

        ckReset.addEventListener('click', function() { location.reload(); });
        ckLoop();
    </script>
    """
    components.html(checkers_js, height=580)
    st.caption("🏆 [체커 완전 규칙 정보] 내 모든 기물이 상대방 돌에 완벽히 가로막혀 더 이상 전진이나 점프를 할 수 없는 '이동 불능(Blocked)' 상태가 되면 정식 체커 규칙에 따라 그 즉시 가둔 사람이 판정승을 거두게 됩니다.")
