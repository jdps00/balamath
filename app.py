"""
Arcana Alquimia / Balatro: Factor Común - Motor Canvas Pixel Art Nativo (16-Bit)
Resolución virtual de 480x270 reescalada por entero (Crisp Pixels)
Curso: IF0003 Matemática Básica para Informática Empresarial
Universidad de Costa Rica - Recinto de Paraíso
"""

import os
import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Factor Común Pixel Art | IF0003",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    .stApp {
        background-color: #0b0c10;
    }
    iframe {
        border: none !important;
        width: 100vw !important;
        height: 100vh !important;
        overflow: hidden !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

current_dir = os.path.dirname(os.path.abspath(__file__))

def get_base64_file(filename):
    full_path = os.path.join(current_dir, filename)
    if os.path.exists(full_path):
        with open(full_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None

video_b64 = None
video_mime = "video/mp4"
for v_name in ["fakcpg.mp4", "faKcpg.mp4", "fakcpg.gif", "faKcpg.gif"]:
    b64 = get_base64_file(v_name)
    if b64:
        video_b64 = b64
        if v_name.endswith(".gif"):
            video_mime = "image/gif"
        break

balatro_font_b64 = get_base64_file("balatro.otf")
daydream_font_b64 = get_base64_file("Daydream DEMO.otf") or get_base64_file("Daydream.otf")
kiwisoda_font_b64 = get_base64_file("KiwiSoda.ttf") or get_base64_file("kiwisoda.ttf")

font_face_css = ""
if daydream_font_b64:
    font_face_css += f"""
    @font-face {{
        font-family: 'DaydreamFont';
        src: url(data:font/otf;base64,{daydream_font_b64}) format('opentype');
    }}
    """
if kiwisoda_font_b64:
    font_face_css += f"""
    @font-face {{
        font-family: 'KiwiSodaFont';
        src: url(data:font/ttf;base64,{kiwisoda_font_b64}) format('truetype');
    }}
    """
if balatro_font_b64:
    font_face_css += f"""
    @font-face {{
        font-family: 'BalatroFont';
        src: url(data:font/otf;base64,{balatro_font_b64}) format('opentype');
    }}
    """

video_html_tag = ""
if video_b64:
    if "gif" in video_mime:
        video_html_tag = f'<img id="bg-media" class="video-bg filter-ronda-1" src="data:{video_mime};base64,{video_b64}" alt="Background" />'
    else:
        video_html_tag = f"""
        <video id="bg-media" class="video-bg filter-ronda-1" autoplay muted loop playsinline>
            <source src="data:{video_mime};base64,{video_b64}" type="{video_mime}">
        </video>
        """
else:
    video_html_tag = '<div id="bg-media" class="procedural-bg filter-ronda-1"></div>'

GAME_HTML = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Factor Común Pixel Art</title>
    <style>
        {font_face_css}

        :root {{
            --font-head: 'DaydreamFont', monospace;
            --font-math: 'BalatroFont', 'KiwiSodaFont', monospace;
            --font-ui: 'KiwiSodaFont', monospace;
        }}

        * {{
            box-sizing: border-box;
            margin: 0; padding: 0;
            user-select: none;
            -webkit-tap-highlight-color: transparent;
        }}

        body, html {{
            width: 100%; height: 100%;
            overflow: hidden;
            background-color: #05070a;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .video-bg {{
            position: fixed;
            top: 50%; left: 50%;
            min-width: 100%; min-height: 100%;
            width: auto; height: auto;
            transform: translate(-50%, -50%) scale(1.05);
            z-index: 1;
            object-fit: cover;
            pointer-events: none;
            transition: filter 1s steps(4);
            image-rendering: pixelated;
        }}

        .procedural-bg {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: radial-gradient(circle at center, #1b4d36, #07120c);
            z-index: 1;
        }}

        .bg-tint-overlay {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: radial-gradient(circle at center, rgba(16, 45, 32, 0.45) 0%, rgba(3, 8, 6, 0.92) 100%);
            mix-blend-mode: multiply;
            pointer-events: none;
            z-index: 2;
        }}

        .filter-ronda-1 {{ filter: hue-rotate(95deg) saturate(140%) brightness(0.72) contrast(1.2); }}
        .filter-ronda-2 {{ filter: hue-rotate(50deg) saturate(160%) brightness(0.8) contrast(1.25); }}
        .filter-ronda-3 {{ filter: hue-rotate(150deg) saturate(130%) brightness(0.68) contrast(1.2); }}

        /* LIENZO DE BAJA RESOLUCIÓN NATIVO */
        #game-canvas {{
            position: relative;
            z-index: 5;
            image-rendering: pixelated;
            image-rendering: crisp-edges;
            width: 100vw;
            height: 100vh;
            object-fit: contain;
            cursor: pointer;
        }}
    </style>
</head>
<body>
    {video_html_tag}
    <div class="bg-tint-overlay"></div>
    <canvas id="game-canvas" width="480" height="270"></canvas>

    <script>
        const canvas = document.getElementById('game-canvas');
        const ctx = canvas.getContext('2d');
        ctx.imageSmoothingEnabled = false;

        const V_WIDTH = 480;
        const V_HEIGHT = 270;

        // Audio procedural
        const aCtx = new (window.AudioContext || window.webkitAudioContext)();
        function playTone(freq, type, dur, vol=0.1) {
            try {
                if(aCtx.state === 'suspended') aCtx.resume();
                const osc = aCtx.createOscillator();
                const gain = aCtx.createGain();
                osc.type = type;
                osc.frequency.setValueAtTime(freq, aCtx.currentTime);
                gain.gain.setValueAtTime(vol, aCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.0001, aCtx.currentTime + dur);
                osc.connect(gain);
                gain.connect(aCtx.destination);
                osc.start();
                osc.stop(aCtx.currentTime + dur);
            } catch(e) {}
        }

        const SFX = {
            hover: () => playTone(340, 'sine', 0.05, 0.03),
            select: () => playTone(560, 'triangle', 0.1, 0.12),
            error: () => { playTone(130, 'sawtooth', 0.2, 0.25); setTimeout(() => playTone(90, 'sawtooth', 0.25, 0.25), 90); },
            flamePop: () => { playTone(200, 'sawtooth', 0.25, 0.25); setTimeout(() => playTone(300, 'sawtooth', 0.2, 0.2), 60); },
            star: () => { playTone(880, 'sine', 0.25, 0.2); setTimeout(()=>playTone(1174, 'sine', 0.35, 0.2), 90); },
            discard: () => playTone(240, 'triangle', 0.15, 0.12),
            winRound: () => { playTone(440, 'sine', 0.25, 0.2); setTimeout(() => playTone(659, 'sine', 0.3, 0.2), 140); }
        };

        // Estado del Juego
        let gameState = 'INTRO'; // 'INTRO', 'PLAY', 'LEVEL_COMPLETE'
        let level = 1;
        let round = 1;
        let score = 0;
        let hand = [];
        let nextCardId = 0;
        let playerName = 'ESTUDIANTE';
        let comodines = { reveal: 1, reroll: 1, skip: 0 };
        let levelStats = { optimalPossible: 0, actualCorrect: 0, errors: 0 };
        let alertMessage = null;
        let alertTimer = 0;
        let shakeFrames = 0;
        let starsWon = 0;
        let bonusWon = 0;

        // Ranking simulado
        const names = ["K_Navas", "Allan_P", "Monica_V", "Bryan_Q", "Maria_F", "Daniela_CR", "Josue_B", "Fabiola_P", "Diego_R", "Valeria_G", "M_Estela", "R_Arias", "Luis_M", "Isaac_H", "Carlos_S", "Andrey_U", "Nath_V", "Seidy_T", "Cesar_O", "Lucia_Z", "Erick_L", "S_Díaz", "Karla_C"];
        let leaderboard = names.map(n => ({ name: n, score: Math.floor(Math.random() * 900 + 500) }));
        leaderboard.push({ name: playerName, score: 0, isPlayer: true });

        setInterval(() => {
            leaderboard.forEach(p => {
                if(!p.isPlayer && Math.random() > 0.45) {
                    p.score += Math.floor(Math.random() * 250);
                }
            });
            const me = leaderboard.find(p => p.isPlayer);
            if(me) { me.score = score; me.name = playerName; }
            leaderboard.sort((a,b) => b.score - a.score);
        }, 3500);

        function gcd(a, b) { a=Math.abs(a); b=Math.abs(b); return b === 0 ? a : gcd(b, a % b); }

        function toSuperscript(num) {
            const map = { '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵' };
            return num.toString().split('').map(d => map[d] || d).join('');
        }

        function formatTerm(c, x, y) {
            let s = "";
            if (c === -1 && (x > 0 || y > 0)) s += "-";
            else if (c !== 1 || (x === 0 && y === 0)) s += c;
            if (x === 1) s += "x"; 
            else if (x > 1) s += `x${toSuperscript(x)}`;
            if (y === 1) s += "y"; 
            else if (y > 1) s += `y${toSuperscript(y)}`;
            return s;
        }

        function getCornerRank(c, x, y) {
            if (x > 0 && y === 0) return x === 1 ? "X" : `X${toSuperscript(x)}`;
            if (y > 0 && x === 0) return y === 1 ? "Y" : `Y${toSuperscript(y)}`;
            if (x > 0 && y > 0) return "XY";
            return Math.abs(c).toString();
        }

        function generateTerm(forceFactor = null) {
            let maxCoef = Math.max(4, level * 3);
            let maxX = Math.min(3, Math.ceil(level / 2));
            let maxY = level > 2 ? Math.min(2, Math.floor(level / 3)) : 0;

            let c = Math.floor(Math.random() * maxCoef) + 1;
            if(Math.random() > 0.75) c *= -1;
            let x = Math.floor(Math.random() * (maxX + 1));
            let y = Math.floor(Math.random() * (maxY + 1));

            if (forceFactor) {
                c = forceFactor.c * (Math.floor(Math.random()*3)+1);
                x = forceFactor.x + Math.floor(Math.random()*2);
                y = forceFactor.y + (forceFactor.y>0 ? Math.floor(Math.random()*2) : 0);
            }
            if (c === 0) c = 1;

            const suits = ['♠', '♥', '♦', '♣'];
            const suit = suits[Math.floor(Math.random() * suits.length)];
            const suitColor = (suit === '♥' || suit === '♦') ? '#d63739' : '#1f78c1';

            return {
                id: nextCardId++,
                c, x, y,
                str: formatTerm(c, x, y),
                corner: getCornerRank(c, x, y),
                suit, suitColor,
                selected: false,
                swayOffset: Math.random() * 10
            };
        }

        function getCommonFactorInfo(cards) {
            if(cards.length < 2) return null;
            let commC = cards[0].c, commX = cards[0].x, commY = cards[0].y;
            for(let i=1; i<cards.length; i++){
                commC = gcd(commC, cards[i].c);
                commX = Math.min(commX, cards[i].x);
                commY = Math.min(commY, cards[i].y);
            }
            return { c: commC, x: commX, y: commY, isValid: commC > 1 || commX > 0 || commY > 0 };
        }

        function calculateOptimalPlays(currentHand) {
            let maxSubset = 0;
            const n = currentHand.length;
            for(let i=1; i < (1<<n); i++) {
                let subset = [];
                for(let j=0; j<n; j++) if((i & (1<<j))) subset.push(currentHand[j]);
                if(subset.length > 1) {
                    const info = getCommonFactorInfo(subset);
                    if(info.isValid && subset.length > maxSubset) maxSubset = subset.length;
                }
            }
            return maxSubset;
        }

        function updateBackgroundForRound() {
            const bg = document.getElementById('bg-media');
            if(!bg) return;
            bg.classList.remove('filter-ronda-1', 'filter-ronda-2', 'filter-ronda-3');
            if(round === 1) bg.classList.add('filter-ronda-1');
            else if (round === 2) bg.classList.add('filter-ronda-2');
            else if (round === 3) bg.classList.add('filter-ronda-3');
        }

        function startRound() {
            updateBackgroundForRound();
            let needed = 6 - hand.length;
            let plantedC = (Math.random() > 0.5) ? (Math.floor(Math.random()*3)+2) : 1;
            let plantedX = (plantedC === 1 || Math.random() > 0.4) ? 1 : 0;
            let forceFactor = { c: plantedC, x: plantedX, y: 0 };
            if(Math.random() < 0.1) forceFactor = null;
            let forceCount = forceFactor ? (Math.floor(Math.random() * 4) + 3) : 0;

            for(let i=0; i<needed; i++) {
                if(forceCount > 0) {
                    hand.push(generateTerm(forceFactor));
                    forceCount--;
                } else {
                    hand.push(generateTerm(null));
                }
            }
            levelStats.optimalPossible += calculateOptimalPlays(hand);
        }

        function playHand() {
            const selected = hand.filter(c => c.selected);
            const info = getCommonFactorInfo(selected);

            if(selected.length < 2 || !info || !info.isValid) {
                SFX.error();
                shakeFrames = 15;
                levelStats.errors++;
                return;
            }

            levelStats.actualCorrect += selected.length;
            let basePts = 50 * level;
            let mult = selected.length * selected.length;
            let handScore = basePts * mult;
            score += handScore;
            
            SFX.flamePop();
            alertMessage = `+${handScore} PUNTOS`;
            alertTimer = 60;

            hand = hand.filter(c => !c.selected);
            round++;
            if(round > 3) {
                endLevel();
            } else {
                startRound();
            }
        }

        function endLevel() {
            let precision = levelStats.optimalPossible > 0 ? (levelStats.actualCorrect / levelStats.optimalPossible) : 1;
            precision -= (levelStats.errors * 0.1);
            if(precision < 0) precision = 0;

            starsWon = 0;
            if(precision >= 0.88) starsWon = 3;
            else if (precision >= 0.5) starsWon = 2;
            else if (precision >= 0.2) starsWon = 1;

            bonusWon = starsWon * 1000 * level;
            score += bonusWon;
            if(starsWon === 3) comodines.skip++;

            SFX.star();
            gameState = 'LEVEL_COMPLETE';
        }

        function nextLevel() {
            level++;
            round = 1;
            hand = [];
            levelStats = { optimalPossible: 0, actualCorrect: 0, errors: 0 };
            gameState = 'PLAY';
            startRound();
        }

        // ========================================================
        // DIBUJADO DE PIXEL ART PROCEDURAL EN CANVAS (ESTILO REFERENCIAS)
        // ========================================================

        // Marco con muescas a 45° en las 4 esquinas (tarot/rol táctico)
        function drawChamferedBox(ctx, x, y, w, h, cut, fillCol, borderCol, shadowCol) {
            // Sombra sólida
            if (shadowCol) {
                ctx.fillStyle = shadowCol;
                ctx.beginPath();
                ctx.moveTo(x + cut + 2, y + 4);
                ctx.lineTo(x + w - cut + 2, y + 4);
                ctx.lineTo(x + w + 2, y + cut + 4);
                ctx.lineTo(x + w + 2, y + h - cut + 4);
                ctx.lineTo(x + w - cut + 2, y + h + 4);
                ctx.lineTo(x + cut + 2, y + h + 4);
                ctx.lineTo(x + 2, y + h - cut + 4);
                ctx.lineTo(x + 2, y + cut + 4);
                ctx.closePath();
                ctx.fill();
            }

            // Borde exterior
            ctx.fillStyle = borderCol;
            ctx.beginPath();
            ctx.moveTo(x + cut, y);
            ctx.lineTo(x + w - cut, y);
            ctx.lineTo(x + w, y + cut);
            ctx.lineTo(x + w, y + h - cut);
            ctx.lineTo(x + w - cut, y + h);
            ctx.lineTo(x + cut, y + h);
            ctx.lineTo(x, y + h - cut);
            ctx.lineTo(x, y + cut);
            ctx.closePath();
            ctx.fill();

            // Relleno interior
            ctx.fillStyle = fillCol;
            ctx.beginPath();
            ctx.moveTo(x + cut + 1, y + 2);
            ctx.lineTo(x + w - cut - 1, y + 2);
            ctx.lineTo(x + w - 2, y + cut + 1);
            ctx.lineTo(x + w - 2, y + h - cut - 1);
            ctx.lineTo(x + w - cut - 1, y + h - 2);
            ctx.lineTo(x + cut + 1, y + h - 2);
            ctx.lineTo(x + 2, y + h - cut - 1);
            ctx.lineTo(x + 2, y + cut + 1);
            ctx.closePath();
            ctx.fill();
        }

        // DIBUJO DE CARTA (Inspiración Tarot / Runa 16-Bit)
        function drawPixelCard(card, x, y, w, h, isHovered) {
            let shakeX = 0;
            if (shakeFrames > 0) {
                shakeX = (shakeFrames % 2 === 0 ? 3 : -3);
            }

            const elevY = card.selected ? -16 : (isHovered ? -8 : 0);
            const drawX = Math.floor(x + shakeX);
            const drawY = Math.floor(y + elevY);

            // 1. Chasis exterior oscuro de madera/hierro
            const borderCol = card.selected ? '#f1b31c' : '#14171d';
            const shadowCol = card.selected ? '#754d03' : '#080a0e';
            const bodyCol = '#252932';
            drawChamferedBox(ctx, drawX, drawY, w, h, 6, bodyCol, borderCol, shadowCol);

            // 2. Ventana interior de pergamino rúnico
            const pad = 5;
            const innerX = drawX + pad;
            const innerY = drawY + pad;
            const innerW = w - (pad * 2);
            const innerH = h - (pad * 2);

            ctx.fillStyle = card.selected ? '#fff9e6' : '#e8dfcb';
            ctx.fillRect(innerX, innerY, innerW, innerH);

            // Dithering/trama rústica en la base del pergamino
            ctx.fillStyle = card.selected ? '#faedbe' : '#d2c6aa';
            for (let py = innerY + innerH - 14; py < innerY + innerH; py += 2) {
                for (let px = innerX; px < innerX + innerW; px += 2) {
                    ctx.fillRect(px, py, 1, 1);
                }
            }

            // Filete decorativo de tarot interior (marco doble pixelado)
            ctx.strokeStyle = card.selected ? '#d49b14' : '#8f7d63';
            ctx.lineWidth = 1;
            ctx.strokeRect(innerX + 3, innerY + 3, innerW - 6, innerH - 6);

            // Muescas ornamentales en las 4 esquinas del ribete
            ctx.fillStyle = card.selected ? '#d49b14' : '#8f7d63';
            ctx.fillRect(innerX + 3, innerY + 3, 3, 3);
            ctx.fillRect(innerX + innerW - 6, innerY + 3, 3, 3);
            ctx.fillRect(innerX + 3, innerY + innerH - 6, 3, 3);
            ctx.fillRect(innerX + innerW - 6, innerY + innerH - 6, 3, 3);

            // 3. Gemas de esquina con Rango y Palo
            ctx.font = '6px var(--font-head)';
            ctx.fillStyle = card.suitColor;
            ctx.textAlign = 'left';
            ctx.fillText(card.corner, innerX + 5, innerY + 12);
            ctx.font = '8px monospace';
            ctx.fillText(card.suit, innerX + 5, innerY + 22);

            // Invertido inferior derecho
            ctx.save();
            ctx.translate(innerX + innerW - 5, innerY + innerH - 5);
            ctx.rotate(Math.PI);
            ctx.font = '6px var(--font-head)';
            ctx.fillStyle = card.suitColor;
            ctx.textAlign = 'left';
            ctx.fillText(card.corner, 0, 7);
            ctx.font = '8px monospace';
            ctx.fillText(card.suit, 0, 17);
            ctx.restore();

            // 4. Placa de Estandarte / Pergamino Central para el Monomio
            const bannerW = innerW - 12;
            const bannerH = 34;
            const bannerX = innerX + 6;
            const bannerY = innerY + (innerH / 2) - (bannerH / 2);

            // Placa
            ctx.fillStyle = '#1b1d24';
            ctx.fillRect(bannerX, bannerY, bannerW, bannerH);
            ctx.strokeStyle = card.selected ? '#f1b31c' : '#454e60';
            ctx.strokeRect(bannerX, bannerY, bannerW, bannerH);

            // Remaches de la placa
            ctx.fillStyle = card.selected ? '#ffd966' : '#8898b5';
            ctx.fillRect(bannerX + 1, bannerY + 1, 2, 2);
            ctx.fillRect(bannerX + bannerW - 3, bannerY + 1, 2, 2);
            ctx.fillRect(bannerX + 1, bannerY + bannerH - 3, 2, 2);
            ctx.fillRect(bannerX + bannerW - 3, bannerY + bannerH - 3, 2, 2);

            // 5. Monomio algebraico (autoescalado)
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            let fSize = 16;
            if (card.str.length === 3) fSize = 14;
            else if (card.str.length === 4) fSize = 12;
            else if (card.str.length >= 5) fSize = 10;

            ctx.font = `bold ${fSize}px var(--font-math)`;
            ctx.fillStyle = '#000000';
            ctx.fillText(card.str, bannerX + (bannerW / 2) + 1, bannerY + (bannerH / 2) + 1);
            ctx.fillStyle = card.selected ? '#ffd447' : '#ffffff';
            ctx.fillText(card.str, bannerX + (bannerW / 2), bannerY + (bannerH / 2));
        }

        // Layout de cartas en pantalla
        const CARD_W = 54;
        const CARD_H = 88;
        const GAP = 12;
        const TOTAL_HAND_W = (6 * CARD_W) + (5 * GAP);
        const START_X = Math.floor((V_WIDTH - TOTAL_HAND_W) / 2);
        const START_Y = 102;

        let mouseX = -1;
        let mouseY = -1;

        // Bucle de Renderizado
        let ticks = 0;
        function render() {
            ticks++;
            if (shakeFrames > 0) shakeFrames--;

            ctx.clearRect(0, 0, V_WIDTH, V_HEIGHT);

            if (gameState === 'INTRO') {
                // Modal de bienvenida en baja resolución
                const modalW = 220;
                const modalH = 150;
                const modalX = Math.floor((V_WIDTH - modalW) / 2);
                const modalY = Math.floor((V_HEIGHT - modalH) / 2);

                drawChamferedBox(ctx, modalX, modalY, modalW, modalH, 6, '#1e222a', '#0d0f14', '#05070a');

                // Título
                drawChamferedBox(ctx, modalX + 12, modalY + 12, modalW - 24, 32, 4, '#d63739', '#540f10', null);
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.font = '10px var(--font-head)';
                ctx.fillStyle = '#ffffff';
                ctx.fillText('FACTOR COMUN', modalX + (modalW / 2), modalY + 24);
                ctx.font = '6px var(--font-head)';
                ctx.fillStyle = '#ffc5c6';
                ctx.fillText('MATEMATICA BASICA UCR', modalX + (modalW / 2), modalY + 36);

                // Campo de usuario
                ctx.fillStyle = '#101217';
                ctx.fillRect(modalX + 24, modalY + 60, modalW - 48, 24);
                ctx.strokeStyle = '#434c5f';
                ctx.strokeRect(modalX + 24, modalY + 60, modalW - 48, 24);

                ctx.font = '12px var(--font-ui)';
                ctx.fillStyle = '#ffd447';
                ctx.fillText(playerName, modalX + (modalW / 2), modalY + 73);

                // Botón Iniciar
                drawChamferedBox(ctx, modalX + 24, modalY + 98, modalW - 48, 28, 4, '#e85d26', '#4a1703', '#280c01');
                ctx.font = '8px var(--font-head)';
                ctx.fillStyle = '#ffffff';
                ctx.fillText('ENTRAR AL JUEGO', modalX + (modalW / 2), modalY + 112);

            } else if (gameState === 'PLAY' || gameState === 'LEVEL_COMPLETE') {
                // 1. Barra Superior (Nivel, Comodines, Puntaje)
                // Nivel / Ronda
                drawChamferedBox(ctx, 10, 8, 80, 30, 4, '#1b1f28', '#0b0c10', '#06070a');
                ctx.textAlign = 'center';
                ctx.font = '6px var(--font-head)';
                ctx.fillStyle = '#9ca8ba';
                ctx.fillText(`NIVEL ${level}`, 50, 18);
                ctx.fillStyle = '#f1b31c';
                ctx.fillText(`RONDA ${round}/3`, 50, 29);

                // 3 Comodines de Reliquia
                const jokers = [
                    { id: 'reveal', icon: '👁️', qty: comodines.reveal, col: '#1f78c1' },
                    { id: 'reroll', icon: '🎲', qty: comodines.reroll, col: '#8b38c2' },
                    { id: 'skip', icon: '⏭️', qty: comodines.skip, col: '#c48914' }
                ];
                jokers.forEach((j, idx) => {
                    const jx = 186 + (idx * 38);
                    drawChamferedBox(ctx, jx, 8, 30, 30, 4, '#1b1f28', '#0b0c10', '#06070a');
                    ctx.font = '12px monospace';
                    ctx.fillText(j.icon, jx + 15, 23);
                    // Badge contador
                    ctx.fillStyle = j.qty > 0 ? '#d63739' : '#444';
                    ctx.fillRect(jx + 20, 5, 12, 10);
                    ctx.font = '6px var(--font-head)';
                    ctx.fillStyle = '#fff';
                    ctx.fillText(j.qty.toString(), jx + 26, 12);
                });

                // Puntos y Rango
                drawChamferedBox(ctx, 390, 8, 80, 30, 4, '#1b1f28', '#0b0c10', '#06070a');
                ctx.textAlign = 'center';
                ctx.font = '6px var(--font-head)';
                ctx.fillStyle = '#9ca8ba';
                ctx.fillText('PUNTOS', 430, 17);
                ctx.font = '12px var(--font-ui)';
                ctx.fillStyle = '#ffd447';
                ctx.fillText(score.toLocaleString(), 430, 29);

                // 2. Renderizado de las 6 Cartas de Tarot
                hand.forEach((card, idx) => {
                    const cx = START_X + (idx * (CARD_W + GAP));
                    const cy = START_Y;
                    const isHover = (mouseX >= cx && mouseX <= cx + CARD_W && mouseY >= cy - 20 && mouseY <= cy + CARD_H);
                    drawPixelCard(card, cx, cy, CARD_W, CARD_H, isHover);
                });

                // 3. Botón "JUGAR MANO" (Placa de piedra labrada estilo BLITZ)
                const selCount = hand.filter(c => c.selected).length;
                const canPlay = selCount >= 2;
                const btnW = 140;
                const btnH = 26;
                const btnX = Math.floor((V_WIDTH - btnW) / 2);
                const btnY = 222;

                const btnFill = canPlay ? '#e85d26' : '#232731';
                const btnBorder = canPlay ? '#4a1703' : '#0e1015';
                const btnShadow = canPlay ? '#280c01' : '#07080a';
                drawChamferedBox(ctx, btnX, btnY, btnW, btnH, 4, btnFill, btnBorder, btnShadow);

                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.font = '8px var(--font-head)';
                ctx.fillStyle = canPlay ? '#ffffff' : '#626b7c';
                ctx.fillText('JUGAR MANO', btnX + (btnW / 2), btnY + (btnH / 2) + 1);

                // 4. Mensajes de Puntos o Alertas Flotantes
                if (alertTimer > 0) {
                    alertTimer--;
                    ctx.font = '10px var(--font-head)';
                    ctx.fillStyle = '#ffd447';
                    ctx.fillText(alertMessage, Math.floor(V_WIDTH / 2), 85);
                }

                // 5. Modal de Fin de Nivel
                if (gameState === 'LEVEL_COMPLETE') {
                    ctx.fillStyle = 'rgba(0,0,0,0.7)';
                    ctx.fillRect(0, 0, V_WIDTH, V_HEIGHT);

                    const mw = 220;
                    const mh = 135;
                    const mx = Math.floor((V_WIDTH - mw) / 2);
                    const my = Math.floor((V_HEIGHT - mh) / 2);

                    drawChamferedBox(ctx, mx, my, mw, mh, 6, '#1e222a', '#0d0f14', '#05070a');
                    drawChamferedBox(ctx, mx + 12, my + 10, mw - 24, 26, 4, '#d63739', '#540f10', null);

                    ctx.font = '9px var(--font-head)';
                    ctx.fillStyle = '#ffffff';
                    ctx.fillText('NIVEL COMPLETADO', mx + (mw / 2), my + 23);

                    // Estrellas pixeladas
                    let starStr = '';
                    for (let s = 0; s < 3; s++) {
                        starStr += (s < starsWon ? '★ ' : '☆ ');
                    }
                    ctx.font = '18px monospace';
                    ctx.fillStyle = '#f1b31c';
                    ctx.fillText(starStr.trim(), mx + (mw / 2), my + 54);

                    ctx.font = '11px var(--font-ui)';
                    ctx.fillStyle = '#ffffff';
                    ctx.fillText(`+${bonusWon.toLocaleString()} BONO DE PRECISION`, mx + (mw / 2), my + 76);

                    // Botón Siguiente
                    drawChamferedBox(ctx, mx + 30, my + 92, mw - 60, 26, 4, '#e85d26', '#4a1703', '#280c01');
                    ctx.font = '8px var(--font-head)';
                    ctx.fillStyle = '#ffffff';
                    ctx.fillText('SIGUIENTE NIVEL', mx + (mw / 2), my + 106);
                }
            }

            requestAnimationFrame(render);
        }

        // Mapeo preciso de clics al lienzo virtual 480x270
        canvas.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            const scaleX = V_WIDTH / rect.width;
            const scaleY = V_HEIGHT / rect.height;
            mouseX = Math.floor((e.clientX - rect.left) * scaleX);
            mouseY = Math.floor((e.clientY - rect.top) * scaleY);
        });

        canvas.addEventListener('click', (e) => {
            const rect = canvas.getBoundingClientRect();
            const scaleX = V_WIDTH / rect.width;
            const scaleY = V_HEIGHT / rect.height;
            const cx = Math.floor((e.clientX - rect.left) * scaleX);
            const cy = Math.floor((e.clientY - rect.top) * scaleY);

            if (gameState === 'INTRO') {
                const modalW = 220;
                const modalH = 150;
                const modalX = Math.floor((V_WIDTH - modalW) / 2);
                const modalY = Math.floor((V_HEIGHT - modalH) / 2);

                // Botón Iniciar
                if (cx >= modalX + 24 && cx <= modalX + modalW - 24 && cy >= modalY + 98 && cy <= modalY + 126) {
                    SFX.select();
                    gameState = 'PLAY';
                    startRound();
                }
            } else if (gameState === 'LEVEL_COMPLETE') {
                const mw = 220;
                const mh = 135;
                const mx = Math.floor((V_WIDTH - mw) / 2);
                const my = Math.floor((V_HEIGHT - mh) / 2);
                if (cx >= mx + 30 && cx <= mx + mw - 30 && cy >= my + 92 && cy <= my + 118) {
                    SFX.select();
                    nextLevel();
                }
            } else if (gameState === 'PLAY') {
                // Clic en cartas
                hand.forEach((card, idx) => {
                    const cardX = START_X + (idx * (CARD_W + GAP));
                    const cardY = START_Y;
                    if (cx >= cardX && cx <= cardX + CARD_W && cy >= cardY - 20 && cy <= cardY + CARD_H) {
                        card.selected = !card.selected;
                        if (card.selected) SFX.select();
                        else SFX.hover();
                    }
                });

                // Clic en JUGAR MANO
                const btnW = 140;
                const btnH = 26;
                const btnX = Math.floor((V_WIDTH - btnW) / 2);
                const btnY = 222;
                if (cx >= btnX && cx <= btnX + btnW && cy >= btnY && cy <= btnY + btnH) {
                    playHand();
                }

                // Clic en Comodines
                const jokers = ['reveal', 'reroll', 'skip'];
                jokers.forEach((type, idx) => {
                    const jx = 186 + (idx * 38);
                    if (cx >= jx && cx <= jx + 30 && cy >= 8 && cy <= 38) {
                        useJoker(type);
                    }
                });
            }
        });

        function useJoker(type) {
            if (comodines[type] <= 0) return;
            if (type === 'reveal') {
                comodines.reveal--;
                let bestFactor = null;
                let maxSubset = 1;
                const n = hand.length;
                for (let i = 1; i < (1 << n); i++) {
                    let subset = [];
                    for (let j = 0; j < n; j++) if ((i & (1 << j))) subset.push(hand[j]);
                    if (subset.length > 1) {
                        const info = getCommonFactorInfo(subset);
                        if (info.isValid && subset.length > maxSubset) {
                            maxSubset = subset.length;
                            bestFactor = formatTerm(info.c, info.x, info.y);
                        }
                    }
                }
                SFX.select();
                if (maxSubset > 1) {
                    alertMessage = `FACTOR: ${bestFactor} (${maxSubset} CARTAS)`;
                } else {
                    alertMessage = `SIN FACTOR COMUN`;
                }
                alertTimer = 90;
            } else if (type === 'reroll') {
                comodines.reroll--;
                SFX.discard();
                hand = [];
                startRound();
                alertMessage = '¡MANO CAMBIADA!';
                alertTimer = 60;
            } else if (type === 'skip') {
                comodines.skip--;
                SFX.winRound();
                levelStats.actualCorrect = 1;
                levelStats.optimalPossible = 1;
                levelStats.errors = 0;
                endLevel();
            }
        }

        // Iniciar bucle
        requestAnimationFrame(render);
    </script>
</body>
</html>
"""

components.html(GAME_HTML, height=720, scrolling=False)
