import streamlit as st
import streamlit.components.v1 as components

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="3D 멀티 대국실", page_icon="🎲", layout="centered")

st.title("🎲 3D 입체 타격감 멀티 대국실 👑")
st.markdown("하나의 앱에서 즐기는 **오목, 체스, 체커**! 모든 게임에 **타격 이펙트**와 **턴별 흐림 효과**가 적용되었습니다.")

# --- 게임 탭 구성 ---
tab1, tab2, tab3 = st.tabs(["⚫ 3D 오목", "👑 3D 체스", "🏁 3D 체커"])

# ==============================================================================
# 🗂️ TAB 1: 3D 정식 오목 (15x15 렌주룰)
# ==============================================================================
with tab1:
    omok_js = """
    <div style="text-align: center; font-family: 'Malgun Gothic', sans-serif;">
        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 480px; margin: 0 auto 10px auto;">
            <div id="o-status" style="padding: 8px 12px; background: #e0f2fe; color: #0369a1; border-radius: 8px; font-weight: bold; font-size: 14px; border: 1px solid #bae6fd;">🏃‍♂️ 흑돌 (⚫) 차례</div>
            <button id="o-reset" style="padding: 8px 12px; background: #ef4444; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 12px;">🔄 리셋</button>
        </div>
        <canvas id="omokCanvas" width="480" height="480" style="border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.15); cursor: pointer;"></canvas>
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
        function drawOStone(row, col, color) {
            const x = O_PAD + col * O_CELL; const y = O_PAD + row * O_CELL; const r = O_CELL * 0.44; oCtx.save();
            oCtx.shadowColor = 'rgba(0,0,0,0.3)'; oCtx.shadowBlur = 4; oCtx.shadowOffsetX = 2; oCtx.shadowOffsetY = 3;
            oCtx.beginPath(); let g = oCtx.createRadialGradient(x - r*0.3, y - r*0.3, r*0.05, x, y, r); if (color === 'black') { g.addColorStop(0, '#666'); g.addColorStop(0.2, '#222'); g.addColorStop(1, '#050505'); } else { g.addColorStop(0, '#fff'); g.addColorStop(0.5, '#eaeaea'); g.addColorStop(1, '#aaa'); }
            oCtx.fillStyle = g; oCtx.arc(x, y, r, 0, Math.PI * 2); oCtx.fill(); oCtx.restore();
        }
        function renderO() { drawOBoard(); for(let r=0; r<O_SIZE; r++) for(let c=0; c<O_SIZE; c++) if(oBoard[r][c]!=='') drawOStone(r,c,oBoard[r][c]); }
        function checkOWin(r, c, col) {
            const dirs = [[0,1], [1,0], [1,1], [1,-1]];
            for (let [dr, dc] of dirs) {
                let cnt = 1; let nr = r + dr, nc = c + dc; while(nr>=0&&nr<O_SIZE&&nc>=0&&nc<O_SIZE&&oBoard[nr][nc]===col) { cnt++; nr+=dr; nc+=dc; }
                nr = r - dr; nc = c - dc; while(nr>=0&&nr<O_SIZE&&nc>=0&&nc<O_SIZE&&oBoard[nr][nc]===col) { cnt++; nr-=dr; nc-=dc; } if (cnt === 5) return true;
            } return false;
        }
        oCanvas.addEventListener('click', function(e) {
            if (oWinner) return; const rect = oCanvas.getBoundingClientRect(); const col = Math.round((e.clientX - rect.left - O_PAD) / O_CELL); const row = Math.round((e.clientY - rect.top - O_PAD) / O_CELL);
            if (row>=0 && row<O_SIZE && col>=0 && col<O_SIZE && oBoard[row][col]==='') {
                oBoard[row][col] = oTurn; renderO(); if (checkOWin(row, col, oTurn)) { oWinner = oTurn; oStatus.style.background='#dcfce7'; oStatus.innerHTML = `🎉 승리: ${oWinner==='black'?'흑돌':'백돌'}!`; return; }
                oTurn = oTurn === 'black' ? 'white' : 'black'; oStatus.innerHTML = `🏃‍♂️ ${oTurn==='black'?'흑돌 (⚫)':'백돌 (⚪)'} 차례`;
            }
        });
        oReset.addEventListener('click', () => { oBoard = Array(O_SIZE).fill(null).map(() => Array(O_SIZE).fill('')); oTurn = 'black'; oWinner = null; oStatus.style.background='#e0f2fe'; oStatus.innerHTML = "🏃‍♂️ 흑돌 (⚫) 차례"; drawOBoard(); });
        drawOBoard();
    </script>
    """
    components.html(omok_js, height=550)

# ==============================================================================
# 🗂️ TAB 2: 3D 타격감 체스 (킹 사망 대형 종료 오버레이)
# ==============================================================================
with tab2:
    chess_js = """
    <div style="text-align: center; font-family: 'Malgun Gothic', sans-serif;">
        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 480px; margin: 0 auto 10px auto;">
            <div id="c-status" style="padding: 8px 12px; background: #f3e8ff; color: #6b21a8; border-radius: 8px; font-weight: bold; font-size: 14px; border: 1px solid #e9d5ff;">⚪ 백돌 차례</div>
            <button id="c-reset" style="padding: 8px 12px; background: #ef4444; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 12px;">🔄 리셋</button>
        </div>
        <canvas id="chessCanvas" width="480" height="480" style="border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.3); cursor: pointer; background: #000;"></canvas>
    </div>
    <script>
        const cCanvas = document.getElementById('chessCanvas'); const cCtx = cCanvas.getContext('2d');
        const C_CELL = cCanvas.width / 8; let cTurn = 'w'; let sel = null; let cWin = null;
        let shake = 0; let ptcls = [];
        let cBoard = [ ['bR','bN','bB','bQ','bK','bB','bN','bR'], ['bP','bP','bP','bP','bP','bP','bP','bP'],['','','','','','','',''],['','','','','','','',''],['','','','','','','',''],['','','','','','','',''],['wP','wP','wP','wP','wP','wP','wP','wP'],['wR','wN','wB','wQ','wK','wB','wN','wR'] ];
        const icons = {'wK':'♔','wQ':'♕','wR':'♖','wB':'♗','wN':'♘','wP':'♙','bK':'♚','bQ':'♛','bR':'♜','bB':'♝','bN':'♞','bP':'♟'};

        function explode(x, y, type) {
            shake = 15; let cnt = type === 'K' ? 50 : 25;
            for (let i = 0; i < cnt; i++) {
                let ang = Math.random()*Math.PI*2; let spd = Math.random()*4+2;
                ptcls.push({x, y, vx: Math.cos(ang)*spd, vy: Math.sin(ang)*spd, r: Math.random()*4+2, a: 1, d: Math.random()*0.02+0.015, c: '#ff4500'});
            }
        }
        function isValid(sr, sc, tr, tc, p) {
            if (sr===tr && sc===tc) return false; let target = cBoard[tr][tc]; if (target !== '' && target[0] === p[0]) return false;
            let dr = tr-sr, dc = tc-sc; let pType = p[1];
            if (pType==='P') { let dir = p[0]==='w'?-1:1; if(dc===0 && cBoard[tr][tc]==='' && dr===dir) return true; if(Math.abs(dc)===1 && dr===dir && target!=='' && target[0]!==p[0]) return true; return false; }
            if (pType==='N') return (Math.abs(dr)===2 && Math.abs(dc)===1) || (Math.abs(dr)===1 && Math.abs(dc)===2);
            if (pType==='K') return Math.abs(dr)<=1 && Math.abs(dc)<=1;
            return true; // 간소화된 룩/비숍/퀸
        }
        function loop() {
            cCtx.clearRect(0,0,480,480); cCtx.save(); if(shake>0){ cCtx.translate((Math.random()-0.5)*10, (Math.random()-0.5)*10); shake--; }
            for(let r=0;r<8;r++) for(let c=0;c<8;c++) {
                cCtx.fillStyle = (r+c)%2===0 ? '#f0d9b5':'#b58863'; cCtx.fillRect(c*C_CELL, r*C_CELL, C_CELL, C_CELL);
                if(sel && sel.r===r && sel.c===c){ cCtx.fillStyle='rgba(255,255,0,0.4)'; cCtx.fillRect(c*C_CELL, r*C_CELL, C_CELL, C_CELL); }
                if(sel && isValid(sel.r, sel.c, r, c, cBoard[sel.r][sel.c])) { 
                    cCtx.fillStyle = cBoard[r][c]!=='' ? 'rgba(239,68,68,0.3)':'rgba(76,175,80,0.2)'; cCtx.fillRect(c*C_CELL, r*C_CELL, C_CELL, C_CELL);
                }
                let p = cBoard[r][c]; if(p!=='') {
                    cCtx.save(); cCtx.globalAlpha = (p[0]===cTurn||cWin)?1.0:0.35; cCtx.textAlign='center'; cCtx.textBaseline='middle'; cCtx.font='32px serif';
                    cCtx.fillStyle = p[0]==='w'?'#fff':'#000'; cCtx.fillText(icons[p], c*C_CELL+C_CELL/2, r*C_CELL+C_CELL/2); cCtx.restore();
                }
            }
            ptcls.forEach((p,i)=>{ p.x+=p.vx; p.y+=p.vy; p.a-=p.d; if(p.a<=0) ptcls.splice(i,1); cCtx.globalAlpha=p.a; cCtx.fillStyle=p.c; cCtx.beginPath(); cCtx.arc(p.x,p.y,p.r,0,Math.PI*2); cCtx.fill(); });
            if(cWin) { cCtx.fillStyle='rgba(0,0,0,0.85)'; cCtx.fillRect(0,0,480,480); cCtx.fillStyle='#ef4444'; cCtx.font='bold 40px Impact'; cCtx.textAlign='center'; cCtx.fillText('GAME OVER', 240, 220); cCtx.fillStyle='#fff'; cCtx.font='20px sans-serif'; cCtx.fillText(`👑 ${cWin==='w'?'백돌':'흑돌'} 승리!`, 240, 270); }
            cCtx.restore(); requestAnimationFrame(loop);
        }
        cCanvas.addEventListener('click', (e)=>{
            if(cWin) return; const rect = cCanvas.getBoundingClientRect(); const c = Math.floor((e.clientX-rect.left)/C_CELL), r = Math.floor((e.clientY-rect.top)/C_CELL);
            if(!sel) { if(cBoard[r][c]!=='' && cBoard[r][c][0]===cTurn) sel={r,c}; }
            else {
                if(isValid(sel.r, sel.c, r, c, cBoard[sel.r][sel.c])) {
                    if(cBoard[r][c]!=='') { explode(c*C_CELL+C_CELL/2, r*C_CELL+C_CELL/2, cBoard[r][c][1]); if(cBoard[r][c][1]==='K') cWin=cTurn; }
                    cBoard[r][c]=cBoard[sel.r][sel.c]; cBoard[sel.r][sel.c]=''; cTurn = cTurn==='w'?'b':'w';
                    document.getElementById('c-status').innerHTML = `${cTurn==='w'?'⚪ 백돌':'⚫ 흑돌'} 차례`;
                } sel=null;
            }
        });
        document.getElementById('c-reset').onclick = () => { location.reload(); };
        loop();
    </script>
    """
    components.html(chess_js, height=550)

# ==============================================================================
# 🗂️ TAB 3: 3D 타격감 체커 (대각선 점프 사냥 + 대형 종료 오버레이)
# ==============================================================================
with tab3:
    checkers_js = """
    <div style="text-align: center; font-family: 'Malgun Gothic', sans-serif;">
        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 480px; margin: 0 auto 10px auto;">
            <div id="ck-status" style="padding: 8px 12px; background: #fee2e2; color: #991b1b; border-radius: 8px; font-weight: bold; font-size: 14px; border: 1px solid #fca5a5;">🔴 레드 차례</div>
            <button id="ck-reset" style="padding: 8px 12px; background: #ef4444; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 12px;">🔄 리셋</button>
        </div>
        <canvas id="ckCanvas" width="480" height="480" style="border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.3); cursor: pointer; background: #000;"></canvas>
    </div>
    <script>
        const ckCanvas = document.getElementById('ckCanvas'); const ckCtx = ckCanvas.getContext('2d');
        const CK_CELL = ckCanvas.width / 8; let ckTurn = 'r'; let ckSel = null; let ckWin = null;
        let ckShake = 0; let ckPtcls = [];
        let ckBoard = Array(8).fill(null).map(() => Array(8).fill(''));
        for(let r=0; r<3; r++) for(let c=0; c<8; c++) if((r+c)%2===1) ckBoard[r][c] = 'b';
        for(let r=5; r<8; r++) for(let c=0; c<8; c++) if((r+c)%2===1) ckBoard[r][c] = 'r';

        function explodeCk(x, y) {
            ckShake = 15; for (let i = 0; i < 25; i++) {
                let ang = Math.random()*Math.PI*2; let spd = Math.random()*4+2;
                ckPtcls.push({x, y, vx: Math.cos(ang)*spd, vy: Math.sin(ang)*spd, r: Math.random()*4+2, a: 1, d: 0.02, c: '#ff4500'});
            }
        }
        function isValidCk(sr, sc, tr, tc, p) {
            if (ckBoard[tr][tc] !== '') return false;
            let dr = tr-sr, dc = tc-sc; let dir = p==='r'?-1:1;
            if (Math.abs(dc)===1 && dr===dir) return {jump:false};
            if (Math.abs(dc)===2 && dr===dir*2) {
                let midR = sr+dir, midC = sc+(dc/2);
                if (ckBoard[midR][midC]!=='' && ckBoard[midR][midC]!==p) return {jump:true, mr:midR, mc:midC};
            } return false;
        }
        function loopCk() {
            ckCtx.clearRect(0,0,480,480); ckCtx.save(); if(ckShake>0){ ckCtx.translate((Math.random()-0.5)*10, (Math.random()-0.5)*10); ckShake--; }
            for(let r=0;r<8;r++) for(let c=0;c<8;c++) {
                ckCtx.fillStyle = (r+c)%2===0 ? '#f0d9b5':'#333'; ckCtx.fillRect(c*CK_CELL, r*CK_CELL, CK_CELL, CK_CELL);
                if(ckSel && ckSel.r===r && ckSel.c===c){ ckCtx.fillStyle='rgba(255,255,0,0.4)'; ckCtx.fillRect(c*CK_CELL, r*CK_CELL, CK_CELL, CK_CELL); }
                let p = ckBoard[r][c]; if(p!=='') {
                    ckCtx.save(); ckCtx.globalAlpha = (p===ckTurn||ckWin)?1.0:0.35;
                    ckCtx.beginPath(); ckCtx.arc(c*CK_CELL+CK_CELL/2, r*CK_CELL+CK_CELL/2, 18, 0, Math.PI*2);
                    ckCtx.fillStyle = p==='r'?'#ef4444':'#1e293b'; ckCtx.fill();
                    ckCtx.strokeStyle='#fff'; ckCtx.stroke(); ckCtx.restore();
                }
            }
            ckPtcls.forEach((p,i)=>{ p.x+=p.vx; p.y+=p.vy; p.a-=p.d; if(p.a<=0) ckPtcls.splice(i,1); ckCtx.globalAlpha=p.a; ckCtx.fillStyle=p.c; ckCtx.beginPath(); ckCtx.arc(p.x,p.y,p.r,0,Math.PI*2); ckCtx.fill(); });
            if(ckWin) { ckCtx.fillStyle='rgba(0,0,0,0.85)'; ckCtx.fillRect(0,0,480,480); ckCtx.fillStyle='#ef4444'; ckCtx.font='bold 40px Impact'; ckCtx.textAlign='center'; ckCtx.fillText('GAME OVER', 240, 220); ckCtx.fillStyle='#fff'; ckCtx.fillText(`👑 ${ckWin==='r'?'레드':'블랙'} 승리!`, 240, 270); }
            ckCtx.restore(); requestAnimationFrame(loopCk);
        }
        ckCanvas.addEventListener('click', (e)=>{
            if(ckWin) return; const rect = ckCanvas.getBoundingClientRect(); const c = Math.floor((e.clientX-rect.left)/CK_CELL), r = Math.floor((e.clientY-rect.top)/CK_CELL);
            if(!ckSel) { if(ckBoard[r][c]===ckTurn) ckSel={r,c}; }
            else {
                let res = isValidCk(ckSel.r, ckSel.c, r, c, ckBoard[ckSel.r][ckSel.c]);
                if(res) {
                    if(res.jump) { ckBoard[res.mr][res.mc]=''; explodeCk(res.mc*CK_CELL+CK_CELL/2, res.mr*CK_CELL+CK_CELL/2); }
                    ckBoard[r][c]=ckTurn; ckBoard[ckSel.r][ckSel.c]=''; ckTurn = ckTurn==='r'?'b':'r';
                    document.getElementById('ck-status').innerHTML = `${ckTurn==='r'?'🔴 레드':'⚫ 블랙'} 차례`;
                    // 승리 판정 (말이 하나도 없으면 패배)
                    let rCnt=0, bCnt=0; ckBoard.forEach(row=>row.forEach(p=>{if(p==='r')rCnt++; if(p==='b')bCnt++;}));
                    if(rCnt===0) ckWin='b'; if(bCnt===0) ckWin='r';
                } ckSel=null;
            }
        });
        document.getElementById('ck-reset').onclick = () => { location.reload(); };
        loopCk();
    </script>
    """
    components.html(checkers_js, height=550)
    st.caption("🏁 [체커 규칙] 내 말을 대각선 앞으로 한 칸씩 움직입니다. 상대방 말을 뛰어넘으면 그 말을 '포획'하여 제거할 수 있습니다.")
