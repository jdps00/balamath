"""
Balatro Factor Común - Motor Canvas Pixel Art 16-Bit Nativo
Curso: IF0003 Matemática Básica para Informática Empresarial
Universidad de Costa Rica - Recinto de Paraíso
"""

import os
import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Factor Común Arcana | IF0003",
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
        overflow: hidden;
    }
    .stApp {
        background-color: #0c0d12;
    }
    iframe {
        border: none !important;
        width: 100vw !important;
        height: 100vh !important;
        display: block;
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

daydream_b64 = get_base64_file("Daydream DEMO.otf") or get_base64_file("Daydream.otf")
kiwisoda_b64 = get_base64_file("KiwiSoda.ttf") or get_base64_file("kiwisoda.ttf")
balatro_b64 = get_base64_file("balatro.otf")

font_face_css = ""
if daydream_b64:
    font_face_css += f"""
    @font-face {{
        font-family: 'DaydreamFont';
        src: url(data:font/otf;base64,{daydream_b64}) format('opentype');
    }}
    """
if kiwisoda_b64:
    font_face_css += f"""
    @font-face {{
        font-family: 'KiwiSodaFont';
        src: url(data:font/ttf;base64,{kiwisoda_font_b64}) format('truetype');
    }}
    """
if balatro_b64:
    font_face_css += f"""
    @font-face {{
        font-family: 'BalatroFont';
        src: url(data:font/otf;base64,{balatro_b64}) format('opentype');
    }}
    """

video_tag = ""
if video_b64:
    if "gif" in video_mime:
        video_tag = f'<img id="bg-media" class="video-bg filter-ronda-1" src="data:{video_mime};base64,{video_b64}" alt="Background" />'
    else:
        video_tag = f"""
        <video id="bg-media" class="video-bg filter-ronda-1" autoplay muted loop playsinline>
            <source src="data:{video_mime};base64,{video_b64}" type="{video_mime}">
        </video>
        """
else:
    video_tag = '<div id="bg-media" class="procedural-bg filter-ronda-1"></div>'

GAME_HTML = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Factor Común 16-Bit</title>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap" rel="stylesheet">
    <style>
        {font_face_css}

        :root {{
            --font-pixel: 'DaydreamFont', 'Press Start 2P', monospace;
            --font-sub: 'KiwiSodaFont', 'VT323', monospace;
        }}

        * {{
            box-sizing: border-box;
            user-select: none;
            -webkit-tap-highlight-color: transparent;
            margin: 0; padding: 0;
        }}

        html, body {{
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            background: #08090d;
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
            z-index: -3;
            object-fit: cover;
            pointer-events: none;
            transition: filter 1s steps(4);
            image-rendering: pixelated;
        }}

        .procedural-bg {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: radial-gradient(circle at center, #1b4933, #070e0a);
            z-index: -3;
        }}

        .bg-tint-overlay {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: radial-gradient(circle at center, rgba(14, 38, 28, 0.42) 0%, rgba(4, 11, 8, 0.93) 100%);
            mix-blend-mode: multiply;
            pointer-events: none;
            z-index: -2;
        }}

        .filter-ronda-1 {{ filter: hue-rotate(95deg) saturate(140%) brightness(0.72) contrast(1.2); }}
        .filter-ronda-2 {{ filter: hue-rotate(50deg) saturate(160%) brightness(0.8) contrast(1.25); }}
        .filter-ronda-3 {{ filter: hue-rotate(150deg) saturate(130%) brightness(0.68) contrast(1.2); }}

        /* LIENZO VIRTUAL EN BAJA RESOLUCIÓN (480x270) ESCALADO SIN FILTROS */
        #gameCanvas {{
            image-rendering: pixelated;
            image-rendering: crisp-edges;
            width: 100vw;
            height: 100vh;
            max-width: 100vw;
            max-height: 100vh;
            object-fit: contain;
            display: block;
            z-index: 10;
        }}
    </style>
</head>
<body>
    {video_tag}
    <div class="bg-tint-overlay"></div>
    <canvas id="gameCanvas" width="480" height="270"></canvas>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        ctx.imageSmoothingEnabled = false;

        /* SÍNTESIS PROCEDURAL WEB AUDIO */
        const aCtx = new (window.AudioContext || window.webkitAudioContext)();
        function playTone(freq, type, dur, vol=0.1) {{
            try {{
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
            }} catch(e) {{}}
        }}

        const SFX = {{
            hover: () => playTone(360, 'sine', 0.06, 0.03),
            select: () => playTone(580, 'triangle', 0.1, 0.12),
            error: () => {{ playTone(120, 'sawtooth', 0.22, 0.25); setTimeout(() => playTone(85, 'sawtooth', 0.3, 0.25), 90); }},
            flamePop: () => {{ playTone(220, 'sine', 0.3, 0.28); setTimeout(() => playTone(340, 'triangle', 0.2, 0.22), 60); }},
            star: () => {{ playTone(880, 'sine', 0.25, 0.2); setTimeout(()=>playTone(1174, 'sine', 0.35, 0.2), 90); }},
            discard: () => playTone(240, 'triangle', 0.14, 0.14),
            winRound: () => {{ playTone(523, 'sine', 0.25, 0.2); setTimeout(() => playTone(784, 'sine', 0.3, 0.2), 140); }}
        }};

        let isBgmPlaying = false;
        function playBGM() {{
            if(isBgmPlaying) return;
            isBgmPlaying = true;
            if(aCtx.state === 'suspended') aCtx.resume();
            const notes = [220, 261.63, 329.63, 392.00, 440, 392.00, 329.63, 261.63]; 
            let step = 0;
            setInterval(() => {{
                if(aCtx.state === 'suspended') return;
                const freq = notes[step % notes.length];
                step++;
                const osc = aCtx.createOscillator();
                const gain = aCtx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(freq, aCtx.currentTime);
                gain.gain.setValueAtTime(0.012, aCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.0001, aCtx.currentTime + 0.35);
                osc.connect(gain);
                gain.connect(aCtx.destination);
                osc.start();
                osc.stop(aCtx.currentTime + 0.35);
            }}, 270);
        }}

        /* PALETA ESTRICTA 16-BIT RETRO */
        const C = {{
            black: '#08090d',
            darkWood: '#1b1716',
            woodBorder: '#2e2622',
            goldHighlight: '#d4a34b',
            goldDark: '#78561d',
            parchment: '#dfd2b5',
            parchmentShadow: '#b09e7c',
            parchmentDeep: '#928062',
            inkDark: '#1a191b',
            redGem: '#c93038',
            redGemLight: '#f55d64',
            blueGem: '#2670b8',
            blueGemLight: '#59a6f2',
            panelBg: '#212631',
            panelBorder: '#0e1117',
            panelBevel: '#3d4659',
            btnOrange: '#d65422',
            btnOrangeLight: '#f28355',
            btnOrangeDark: '#7a2b0c',
            btnDisabled: '#2a303c',
            btnDisabledText: '#566072'
        }};

        /* ESTADO DEL JUEGO */
        let gameState = 'INTRO';
        let level = 1;
        let round = 1;
        let score = 0;
        let hand = [];
        let nextCardId = 0;
        let levelStats = {{ optimalPossible: 0, actualCorrect: 0, errors: 0 }};
        let comodines = {{ reveal: 1, reroll: 1, skip: 0 }};
        let playerName = "ESTUDIANTE";

        let showLeaderboard = false;
        let showTutorial = false;
        let activeAlert = null;
        let alertTimer = 0;
        let flameScoreText = null;
        let flameScoreTimer = 0;
        let particles = [];
        let starsAwarded = 0;

        /* COORDENADAS VIRTUALES DEL JUEGO (480x270) */
        const CARDS_Y = 126;
        const CARD_W = 56;
        const CARD_H = 84;
        const CARD_SPACING = 8;
        const PLAY_BTN = {{ x: 180, y: 226, w: 120, h: 26 }};

        /* RANKING COMPAÑEROS */
        const classNames = ["Andrey_U", "Fabiola_P", "Bryan_Q", "Daniela_CR", "Nath_V", "Isaac_H", "Carlos_S", "M_Estela", "K_Navas", "Diego_R", "K_Mora", "Josue_B", "Maria_F", "Valeria_G", "Seidy_T", "Allan_P", "Cesar_O", "Monica_V", "Lucia_Z", "R_Arias", "Erick_L", "S_Díaz", "Karla_C", "Luis_M"];
        let leaderboardData = [];
        function initLeaderboard() {{
            leaderboardData = classNames.map(n => ({{ name: n, score: Math.floor(Math.random() * 1100 + 400), isPlayer: false }}));
            leaderboardData.push({{ name: playerName, score: score, isPlayer: true }});
            leaderboardData.sort((a,b) => b.score - a.score);
            setInterval(() => {{
                leaderboardData.forEach(p => {{
                    if(!p.isPlayer && Math.random() > 0.45) {{
                        p.score += Math.floor(Math.random() * 260);
                    }}
                }});
                leaderboardData.sort((a,b) => b.score - a.score);
            }}, 3500);
        }}

        /* MATEMÁTICA Y EXPRESIONES */
        function gcd(a, b) {{ a = Math.abs(a); b = Math.abs(b); return b === 0 ? a : gcd(b, a % b); }}

        function toSuperscript(num) {{
            const map = {{ '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵' }};
            return num.toString().split('').map(d => map[d] || d).join('');
        }}

        function formatTerm(c, x, y) {{
            let s = "";
            if (c === -1 && (x > 0 || y > 0)) s += "-";
            else if (c !== 1 || (x === 0 && y === 0)) s += c;
            if (x === 1) s += "x"; 
            else if (x > 1) s += `x${{toSuperscript(x)}}`;
            if (y === 1) s += "y"; 
            else if (y > 1) s += `y${{toSuperscript(y)}}`;
            return s;
        }}

        function getCardCornerRank(card) {{
            if (card.x > 0 && card.y === 0) return card.x === 1 ? "X" : `X${{toSuperscript(card.x)}}`;
            if (card.y > 0 && card.x === 0) return card.y === 1 ? "Y" : `Y${{toSuperscript(card.y)}}`;
            if (card.x > 0 && card.y > 0) return "XY";
            return Math.abs(card.c).toString();
        }}

        function updateBackgroundForRound() {{
            const bg = document.getElementById('bg-media');
            if(!bg) return;
            bg.classList.remove('filter-ronda-1', 'filter-ronda-2', 'filter-ronda-3');
            if(round === 1) bg.classList.add('filter-ronda-1');
            else if (round === 2) bg.classList.add('filter-ronda-2');
            else if (round === 3) bg.classList.add('filter-ronda-3');
        }}

        function generateTerm(forceFactor = null) {{
            let maxCoef = Math.max(4, level * 3);
            let maxX = Math.min(3, Math.ceil(level / 2));
            let maxY = level > 2 ? Math.min(2, Math.floor(level / 3)) : 0;

            let c = Math.floor(Math.random() * maxCoef) + 1;
            if(Math.random() > 0.75) c *= -1;
            let x = Math.floor(Math.random() * (maxX + 1));
            let y = Math.floor(Math.random() * (maxY + 1));

            if (forceFactor) {{
                c = forceFactor.c * (Math.floor(Math.random()*3)+1);
                x = forceFactor.x + Math.floor(Math.random()*2);
                y = forceFactor.y + (forceFactor.y>0 ? Math.floor(Math.random()*2) : 0);
            }}

            if (c === 0) c = 1;
            const suits = ['♠', '♥', '♦', '♣'];
            const suit = suits[Math.floor(Math.random() * suits.length)];
            const isRed = (suit === '♥' || suit === '♦');

            return {{
                c, x, y,
                str: formatTerm(c,x,y),
                suit,
                isRed,
                selected: false,
                swayOffset: Math.random() * Math.PI * 2,
                id: nextCardId++
            }};
        }}

        function getCommonFactorInfo(cards) {{
            if(cards.length < 2) return null;
            let commC = cards[0].c, commX = cards[0].x, commY = cards[0].y;
            for(let i=1; i<cards.length; i++){{
                commC = gcd(commC, cards[i].c);
                commX = Math.min(commX, cards[i].x);
                commY = Math.min(commY, cards[i].y);
            }}
            return {{ c: commC, x: commX, y: commY, isValid: commC > 1 || commX > 0 || commY > 0 }};
        }}

        function calculateOptimalPlays(currentHand) {{
            let maxSubset = 0;
            const n = currentHand.length;
            for(let i=1; i < (1<<n); i++) {{
                let subset = [];
                for(let j=0; j<n; j++) if((i & (1<<j))) subset.push(currentHand[j]);
                if(subset.length > 1) {{
                    const info = getCommonFactorInfo(subset);
                    if(info.isValid && subset.length > maxSubset) maxSubset = subset.length;
                }}
            }}
            return maxSubset;
        }}

        function startRound() {{
            updateBackgroundForRound();
            let needed = 6 - hand.length;
            let plantedC = (Math.random() > 0.5) ? (Math.floor(Math.random()*3)+2) : 1;
            let plantedX = (plantedC === 1 || Math.random() > 0.4) ? 1 : 0;
            let forceFactor = {{ c: plantedC, x: plantedX, y: 0 }};
            if(Math.random() < 0.1) forceFactor = null;
            let forceCount = forceFactor ? (Math.floor(Math.random() * 4) + 3) : 0;

            for(let i=0; i<needed; i++) {{
                if(forceCount > 0) {{
                    hand.push(generateTerm(forceFactor));
                    forceCount--;
                }} else {{
                    hand.push(generateTerm(null));
                }}
            }}
            levelStats.optimalPossible += calculateOptimalPlays(hand);
        }}

        function playHand() {{
            const selected = hand.filter(c => c.selected);
            const info = getCommonFactorInfo(selected);

            if(selected.length < 2 || !info || !info.isValid) {{
                SFX.error();
                levelStats.errors++;
                triggerShake();
                return;
            }}

            levelStats.actualCorrect += selected.length;
            let basePts = 50 * level;
            let mult = selected.length * selected.length;
            let handScore = basePts * mult;
            score += handScore;

            const p = leaderboardData.find(x => x.isPlayer);
            if(p) p.score = score;
            leaderboardData.sort((a,b) => b.score - a.score);

            SFX.flamePop();
            flameScoreText = `+${{handScore.toLocaleString()}}`;
            flameScoreTimer = 70;
            spawnParticles(240, 150, 45);

            hand = hand.filter(c => !c.selected);

            setTimeout(() => {{
                round++;
                if(round > 3) {{
                    endLevel();
                }} else {{
                    startRound();
                }}
            }}, 900);
        }}

        function endLevel() {{
            let precision = levelStats.optimalPossible > 0 ? (levelStats.actualCorrect / levelStats.optimalPossible) : 1;
            precision -= (levelStats.errors * 0.1);
            if(precision < 0) precision = 0;

            starsAwarded = 0;
            if(precision >= 0.88) starsAwarded = 3;
            else if (precision >= 0.5) starsAwarded = 2;
            else if (precision >= 0.2) starsAwarded = 1;

            let bonus = starsAwarded * 1000 * level;
            score += bonus;
            const p = leaderboardData.find(x => x.isPlayer);
            if(p) p.score = score;
            leaderboardData.sort((a,b) => b.score - a.score);

            if(starsAwarded === 3) comodines.skip++;
            gameState = 'LEVEL_COMPLETE';
            SFX.winRound();
        }}

        function nextLevel() {{
            level++;
            round = 1;
            hand = [];
            levelStats = {{ optimalPossible: 0, actualCorrect: 0, errors: 0 }};
            gameState = 'PLAYING';
            startRound();
        }}

        function showAlert(msg) {{
            activeAlert = msg;
            alertTimer = 140;
        }}

        function useJoker(type) {{
            if(comodines[type] <= 0) return;
            if(type === 'reveal') {{
                comodines.reveal--;
                let bestFactor = null;
                let maxSubset = 1;
                const n = hand.length;
                for(let i=1; i < (1<<n); i++) {{
                    let subset = [];
                    for(let j=0; j<n; j++) if((i & (1<<j))) subset.push(hand[j]);
                    if(subset.length > 1) {{
                        const info = getCommonFactorInfo(subset);
                        if(info.isValid && subset.length > maxSubset) {{
                            maxSubset = subset.length;
                            bestFactor = formatTerm(info.c, info.x, info.y);
                        }}
                    }}
                }}
                SFX.select();
                if(maxSubset > 1) {{
                    showAlert(`FACTOR: ${{bestFactor}} (en ${{maxSubset}} cartas)`);
                }} else {{
                    showAlert("Sin factor detectable");
                }}
            }} else if (type === 'reroll') {{
                comodines.reroll--;
                SFX.discard();
                hand = [];
                startRound();
                showAlert("¡MANO DESCARTADA!");
            }} else if (type === 'skip') {{
                comodines.skip--;
                SFX.winRound();
                levelStats.actualCorrect = 1; 
                levelStats.optimalPossible = 1;
                levelStats.errors = 0;
                endLevel();
            }}
        }}

        /* PARTÍCULAS */
        function spawnParticles(x, y, count=35) {{
            const colors = [C.goldHighlight, C.redGemLight, C.blueGemLight, '#ffffff'];
            for(let i=0; i<count; i++) {{
                const angle = Math.random() * Math.PI * 2;
                const spd = 1.5 + Math.random() * 4;
                particles.push({{
                    x, y,
                    vx: Math.cos(angle)*spd,
                    vy: Math.sin(angle)*spd - 1.2,
                    color: colors[Math.floor(Math.random()*colors.length)],
                    size: 2,
                    life: 1.0,
                    decay: 0.025 + Math.random()*0.02
                }});
            }}
        }}

        let shakeFrames = 0;
        function triggerShake() {{ shakeFrames = 14; }}

        /* DIBUJO PROCEDURAL EN CANVAS PIXEL ART 16-BIT */
        function drawPixelCard(x, y, w, h, card, isSelected, swayY) {{
            const actualY = Math.floor(y + swayY + (isSelected ? -16 : 0));
            const X = Math.floor(x);
            const Y = actualY;

            // Sombra dura 16-bit
            ctx.fillStyle = C.black;
            ctx.fillRect(X + 2, Y + 3, w, h);

            // Chasis exterior muescado a 45°
            ctx.fillStyle = isSelected ? C.goldHighlight : C.woodBorder;
            ctx.fillRect(X + 2, Y, w - 4, h);
            ctx.fillRect(X, Y + 2, w, h - 4);

            ctx.fillStyle = isSelected ? '#fff3b0' : C.darkWood;
            ctx.fillRect(X + 3, Y + 1, w - 6, h - 2);
            ctx.fillRect(X + 1, Y + 3, w - 2, h - 6);

            // Borde biselado
            ctx.fillStyle = C.parchmentDeep;
            ctx.fillRect(X + 4, Y + 4, w - 8, h - 8);

            // Pergamino interior
            ctx.fillStyle = C.parchment;
            ctx.fillRect(X + 5, Y + 5, w - 10, h - 10);

            // Ribete perimetral
            ctx.strokeStyle = C.parchmentShadow;
            ctx.lineWidth = 1;
            ctx.strokeRect(X + 7.5, Y + 7.5, w - 15, h - 15);

            // Broches de esquinas
            const gemColor = card.isRed ? C.redGem : C.blueGem;
            const gemLight = card.isRed ? C.redGemLight : C.blueGemLight;
            
            // Broche Superior Izquierdo
            ctx.fillStyle = C.black;
            ctx.fillRect(X + 6, Y + 6, 8, 8);
            ctx.fillStyle = gemColor;
            ctx.fillRect(X + 7, Y + 7, 6, 6);
            ctx.fillStyle = gemLight;
            ctx.fillRect(X + 7, Y + 7, 2, 2);

            // Rango de esquina
            ctx.font = '8px KiwiSodaFont, monospace';
            ctx.fillStyle = C.inkDark;
            ctx.textAlign = 'left';
            ctx.fillText(getCardCornerRank(card), X + 16, Y + 14);

            // Palo
            ctx.font = '7px KiwiSodaFont, monospace';
            ctx.fillStyle = card.isRed ? C.redGem : C.blueGem;
            ctx.fillText(card.suit, X + 8, Y + 22);

            // Estandarte central para el monomio
            const bannerY = Y + Math.floor(h / 2) - 14;
            const bannerH = 24;
            ctx.fillStyle = C.parchmentDeep;
            ctx.fillRect(X + 7, bannerY, w - 14, bannerH);
            ctx.fillStyle = '#ebdcc0';
            ctx.fillRect(X + 8, bannerY + 1, w - 16, bannerH - 2);

            ctx.fillStyle = C.goldDark;
            ctx.fillRect(X + 8, bannerY + 1, w - 16, 1);
            ctx.fillRect(X + 8, bannerY + bannerH - 2, w - 16, 1);

            // Expresión matemática
            ctx.fillStyle = C.inkDark;
            ctx.textAlign = 'center';
            const strLen = card.str.length;
            if (strLen <= 2) {{
                ctx.font = '16px KiwiSodaFont, monospace';
            }} else if (strLen <= 4) {{
                ctx.font = '13px KiwiSodaFont, monospace';
            }} else {{
                ctx.font = '11px KiwiSodaFont, monospace';
            }}
            ctx.fillText(card.str, X + Math.floor(w / 2), bannerY + 17);

            // Broche Inferior Derecho
            ctx.fillStyle = C.black;
            ctx.fillRect(X + w - 14, Y + h - 14, 8, 8);
            ctx.fillStyle = gemColor;
            ctx.fillRect(X + w - 13, Y + h - 13, 6, 6);
            ctx.fillStyle = gemLight;
            ctx.fillRect(X + w - 13, Y + h - 13, 2, 2);
        }}

        function drawPixelPanel(x, y, w, h) {{
            ctx.fillStyle = C.black;
            ctx.fillRect(x + 2, y + 2, w, h);

            ctx.fillStyle = C.panelBorder;
            ctx.fillRect(x, y, w, h);

            ctx.fillStyle = C.panelBevel;
            ctx.fillRect(x + 1, y + 1, w - 2, 1);
            ctx.fillRect(x + 1, y + 1, 1, h - 2);

            ctx.fillStyle = C.panelBg;
            ctx.fillRect(x + 2, y + 2, w - 4, h - 4);
        }}

        function drawPixelButton(x, y, w, h, text, isEnabled) {{
            ctx.fillStyle = C.black;
            ctx.fillRect(x + 1, y + 2, w, h);

            if (isEnabled) {{
                ctx.fillStyle = C.btnOrangeDark;
                ctx.fillRect(x, y, w, h);

                ctx.fillStyle = C.btnOrangeLight;
                ctx.fillRect(x + 1, y + 1, w - 2, 1);
                ctx.fillRect(x + 1, y + 1, 1, h - 2);

                ctx.fillStyle = C.btnOrange;
                ctx.fillRect(x + 2, y + 2, w - 4, h - 4);

                ctx.font = '10px DaydreamFont, monospace';
                ctx.fillStyle = '#ffffff';
                ctx.textAlign = 'center';
                ctx.fillText(text, x + Math.floor(w/2), y + Math.floor(h/2) + 4);
            }} else {{
                ctx.fillStyle = C.black;
                ctx.fillRect(x, y, w, h);
                ctx.fillStyle = C.btnDisabled;
                ctx.fillRect(x + 2, y + 2, w - 4, h - 4);

                ctx.font = '10px DaydreamFont, monospace';
                ctx.fillStyle = C.btnDisabledText;
                ctx.textAlign = 'center';
                ctx.fillText(text, x + Math.floor(w/2), y + Math.floor(h/2) + 4);
            }}
        }}

        /* BUCLE PRINCIPAL DE DIBUJO */
        let frameCount = 0;
        function render() {{
            frameCount++;
            ctx.clearRect(0, 0, 480, 270);

            let offX = 0, offY = 0;
            if(shakeFrames > 0) {{
                shakeFrames--;
                offX = (Math.random() > 0.5 ? 2 : -2);
                offY = (Math.random() > 0.5 ? 2 : -2);
            }}

            ctx.save();
            ctx.translate(offX, offY);

            if (gameState === 'INTRO') {{
                drawIntroModal();
            }} else {{
                drawGameScene();
            }}

            if (showLeaderboard) drawLeaderboardOverlay();
            if (showTutorial) drawTutorialOverlay();
            if (gameState === 'LEVEL_COMPLETE') drawLevelCompleteModal();

            if (alertTimer > 0) {{
                alertTimer--;
                drawPixelPanel(120, 18, 240, 22);
                ctx.font = '9px KiwiSodaFont, monospace';
                ctx.fillStyle = C.goldHighlight;
                ctx.textAlign = 'center';
                ctx.fillText(activeAlert, 240, 32);
            }}

            for(let i=particles.length-1; i>=0; i--) {{
                const p = particles[i];
                p.x += p.vx; p.y += p.vy;
                p.vy += 0.12;
                p.life -= p.decay;
                if(p.life <= 0) {{ particles.splice(i,1); continue; }}
                ctx.fillStyle = p.color;
                ctx.fillRect(Math.floor(p.x), Math.floor(p.y), p.size, p.size);
            }}

            if (flameScoreTimer > 0) {{
                flameScoreTimer--;
                const bounce = Math.sin(frameCount * 0.5) * 3;
                ctx.font = '16px DaydreamFont, monospace';
                ctx.fillStyle = C.black;
                ctx.textAlign = 'center';
                ctx.fillText(flameScoreText, 242, 116 + bounce);
                ctx.fillStyle = C.goldHighlight;
                ctx.fillText(flameScoreText, 240, 115 + bounce);
            }}

            ctx.restore();
            requestAnimationFrame(render);
        }}

        function drawGameScene() {{
            drawPixelPanel(10, 8, 86, 28);
            ctx.font = '7px DaydreamFont, monospace';
            ctx.fillStyle = '#9aa8bf';
            ctx.textAlign = 'center';
            ctx.fillText(`NIVEL ${{level}}`, 53, 19);
            ctx.font = '8px KiwiSodaFont, monospace';
            ctx.fillStyle = C.goldHighlight;
            ctx.fillText(`RONDA ${{round}}/3`, 53, 30);

            const jx = 180;
            drawPixelPanel(jx, 8, 30, 28);
            ctx.font = '14px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('👁️', jx + 15, 27);
            drawBadge(jx + 24, 7, comodines.reveal, C.redGem);

            drawPixelPanel(jx + 36, 8, 30, 28);
            ctx.fillText('🎲', jx + 51, 27);
            drawBadge(jx + 60, 7, comodines.reroll, '#8e44ad');

            drawPixelPanel(jx + 72, 8, 30, 28);
            ctx.fillText('⏭️', jx + 87, 27);
            drawBadge(jx + 96, 7, comodines.skip, '#f39c12');

            drawPixelPanel(384, 8, 86, 28);
            ctx.font = '7px DaydreamFont, monospace';
            ctx.fillStyle = '#9aa8bf';
            ctx.textAlign = 'center';
            ctx.fillText('PUNTOS', 427, 18);
            ctx.font = '11px KiwiSodaFont, monospace';
            ctx.fillStyle = C.goldHighlight;
            ctx.fillText(score.toLocaleString(), 427, 30);

            drawPixelPanel(10, 238, 48, 22);
            ctx.font = '8px DaydreamFont, monospace';
            ctx.fillStyle = '#ffffff';
            ctx.textAlign = 'center';
            ctx.fillText('TUTO', 34, 253);

            drawPixelPanel(422, 238, 48, 22);
            ctx.fillStyle = C.goldHighlight;
            ctx.fillText('RANK', 446, 253);

            const totalCardsWidth = hand.length * CARD_W + (hand.length - 1) * CARD_SPACING;
            const startX = Math.floor((480 - totalCardsWidth) / 2);

            hand.forEach((card, idx) => {{
                const cx = startX + idx * (CARD_W + CARD_SPACING);
                const sway = Math.sin(frameCount * 0.04 + card.swayOffset) * 2;
                drawPixelCard(cx, CARDS_Y, CARD_W, CARD_H, card, card.selected, sway);
            }});

            const selectedCount = hand.filter(c => c.selected).length;
            drawPixelButton(PLAY_BTN.x, PLAY_BTN.y, PLAY_BTN.w, PLAY_BTN.h, 'JUGAR MANO', selectedCount >= 1);
        }}

        function drawBadge(x, y, count, color) {{
            ctx.fillStyle = C.black;
            ctx.fillRect(x - 4, y - 4, 10, 10);
            ctx.fillStyle = color;
            ctx.fillRect(x - 3, y - 3, 8, 8);
            ctx.font = '7px KiwiSodaFont, monospace';
            ctx.fillStyle = '#ffffff';
            ctx.textAlign = 'center';
            ctx.fillText(count.toString(), x + 1, y + 4);
        }}

        function drawIntroModal() {{
            drawPixelPanel(130, 60, 220, 150);
            
            ctx.fillStyle = C.redGem;
            ctx.fillRect(140, 72, 200, 26);
            ctx.fillStyle = C.redGemLight;
            ctx.fillRect(141, 73, 198, 1);
            ctx.font = '11px DaydreamFont, monospace';
            ctx.fillStyle = '#ffffff';
            ctx.textAlign = 'center';
            ctx.fillText('FACTOR COMÚN', 240, 89);

            ctx.font = '9px KiwiSodaFont, monospace';
            ctx.fillStyle = '#9aa8bf';
            ctx.fillText('APRENDIZ EN EL AULA (TÚ):', 240, 116);

            ctx.fillStyle = C.black;
            ctx.fillRect(160, 126, 160, 22);
            ctx.font = '12px KiwiSodaFont, monospace';
            ctx.fillStyle = C.goldHighlight;
            ctx.fillText(playerName, 240, 141);

            drawPixelButton(160, 164, 160, 28, 'ENTRAR', true);
        }}

        function drawLeaderboardOverlay() {{
            ctx.fillStyle = 'rgba(0,0,0,0.7)';
            ctx.fillRect(0,0,480,270);

            drawPixelPanel(110, 25, 260, 220);
            ctx.font = '10px DaydreamFont, monospace';
            ctx.fillStyle = C.goldHighlight;
            ctx.textAlign = 'center';
            ctx.fillText('RANKING EN VIVO', 240, 44);

            ctx.font = '8px KiwiSodaFont, monospace';
            ctx.fillStyle = '#9aa8bf';
            ctx.fillText('PULSA EN CUALQUIER LUGAR PARA CERRAR', 240, 56);

            const displayList = leaderboardData.slice(0, 7);
            displayList.forEach((entry, idx) => {{
                const ry = 72 + idx * 21;
                ctx.fillStyle = entry.isPlayer ? '#224a38' : '#141822';
                ctx.fillRect(124, ry, 232, 17);
                ctx.strokeStyle = entry.isPlayer ? C.goldHighlight : '#000';
                ctx.strokeRect(124.5, ry + 0.5, 231, 16);

                ctx.font = '10px KiwiSodaFont, monospace';
                ctx.fillStyle = entry.isPlayer ? C.goldHighlight : '#ffffff';
                ctx.textAlign = 'left';
                ctx.fillText(`#${{idx+1}} ${{entry.name}} ${{entry.isPlayer ? '(TÚ)' : ''}}`, 132, ry + 12);

                ctx.textAlign = 'right';
                ctx.fillText(entry.score.toLocaleString(), 348, ry + 12);
            }});
        }}

        function drawTutorialOverlay() {{
            ctx.fillStyle = 'rgba(0,0,0,0.7)';
            ctx.fillRect(0,0,480,270);

            drawPixelPanel(110, 30, 260, 210);
            ctx.font = '10px DaydreamFont, monospace';
            ctx.fillStyle = C.goldHighlight;
            ctx.textAlign = 'center';
            ctx.fillText('CÓMO JUGAR', 240, 50);

            ctx.fillStyle = '#11151e';
            ctx.fillRect(130, 65, 220, 32);
            ctx.font = '13px KiwiSodaFont, monospace';
            ctx.fillStyle = '#ffffff';
            ctx.fillText('🍎🍉 + 🍎🍌 = 🍎(🍉 + 🍌)', 240, 85);

            ctx.font = '9px KiwiSodaFont, monospace';
            ctx.fillStyle = '#cad3e2';
            ctx.textAlign = 'left';
            const lines = [
                '1. Selecciona 2 o más cartas que tengan',
                '   un divisor común (MCD) o letras con exponente.',
                '2. Presiona JUGAR MANO para purificar la fórmula.',
                '3. Las cartas no usadas quedan para la próxima ronda.'
            ];
            lines.forEach((l, idx) => ctx.fillText(l, 126, 120 + idx * 17));

            drawPixelButton(180, 202, 120, 24, 'ENTENDIDO', true);
        }}

        function drawLevelCompleteModal() {{
            ctx.fillStyle = 'rgba(0,0,0,0.8)';
            ctx.fillRect(0,0,480,270);

            drawPixelPanel(120, 45, 240, 180);
            ctx.font = '11px DaydreamFont, monospace';
            ctx.fillStyle = C.goldHighlight;
            ctx.textAlign = 'center';
            ctx.fillText('NIVEL COMPLETADO', 240, 72);

            for(let i=0; i<3; i++) {{
                ctx.font = '24px sans-serif';
                ctx.fillStyle = (i < starsAwarded) ? C.goldHighlight : '#3a4252';
                ctx.fillText('★', 200 + i * 40, 112);
            }}

            ctx.font = '9px KiwiSodaFont, monospace';
            ctx.fillStyle = '#cad3e2';
            ctx.fillText(starsAwarded === 3 ? '¡PRECISIÓN PERFECTA! (+1 SALTO)' : 'Nivel purificado con éxito.', 240, 142);
            ctx.fillText(`Puntos totales: ${{score.toLocaleString()}}`, 240, 160);

            drawPixelButton(170, 180, 140, 26, 'SIGUIENTE', true);
        }}

        function getCanvasCoords(evt) {{
            const rect = canvas.getBoundingClientRect();
            const scaleX = 480 / rect.width;
            const scaleY = 270 / rect.height;
            const clientX = evt.touches ? evt.touches[0].clientX : evt.clientX;
            const clientY = evt.touches ? evt.touches[0].clientY : evt.clientY;
            return {{
                x: Math.floor((clientX - rect.left) * scaleX),
                y: Math.floor((clientY - rect.top) * scaleY)
            }};
        }}

        function handlePointer(pt) {{
            if (aCtx.state === 'suspended') aCtx.resume();

            if (gameState === 'INTRO') {{
                if (pt.x >= 160 && pt.x <= 320 && pt.y >= 164 && pt.y <= 192) {{
                    SFX.select();
                    playBGM();
                    gameState = 'PLAYING';
                    initLeaderboard();
                    startRound();
                }}
                return;
            }}

            if (showLeaderboard) {{
                showLeaderboard = false;
                SFX.hover();
                return;
            }}

            if (showTutorial) {{
                showTutorial = false;
                SFX.hover();
                return;
            }}

            if (gameState === 'LEVEL_COMPLETE') {{
                if (pt.x >= 170 && pt.x <= 310 && pt.y >= 180 && pt.y <= 206) {{
                    SFX.select();
                    nextLevel();
                }}
                return;
            }}

            // TUTO
            if (pt.x >= 10 && pt.x <= 58 && pt.y >= 238 && pt.y <= 260) {{
                showTutorial = true;
                SFX.hover();
                return;
            }}

            // RANK
            if (pt.x >= 422 && pt.x <= 470 && pt.y >= 238 && pt.y <= 260) {{
                showLeaderboard = true;
                SFX.hover();
                return;
            }}

            // Comodines
            const jx = 180;
            if (pt.y >= 8 && pt.y <= 36) {{
                if (pt.x >= jx && pt.x <= jx + 30) {{ useJoker('reveal'); return; }}
                if (pt.x >= jx + 36 && pt.x <= jx + 66) {{ useJoker('reroll'); return; }}
                if (pt.x >= jx + 72 && pt.x <= jx + 102) {{ useJoker('skip'); return; }}
            }}

            // JUGAR MANO
            if (pt.x >= PLAY_BTN.x && pt.x <= PLAY_BTN.x + PLAY_BTN.w &&
                pt.y >= PLAY_BTN.y && pt.y <= PLAY_BTN.y + PLAY_BTN.h) {{
                playHand();
                return;
            }}

            // Cartas
            const totalCardsWidth = hand.length * CARD_W + (hand.length - 1) * CARD_SPACING;
            const startX = Math.floor((480 - totalCardsWidth) / 2);

            for (let i = 0; i < hand.length; i++) {{
                const cx = startX + i * (CARD_W + CARD_SPACING);
                const cy = CARDS_Y + (hand[i].selected ? -16 : 0);
                if (pt.x >= cx && pt.x <= cx + CARD_W && pt.y >= cy && pt.y <= cy + CARD_H) {{
                    hand[i].selected = !hand[i].selected;
                    if(hand[i].selected) SFX.select(); else SFX.hover();
                    return;
                }}
            }}
        }}

        canvas.addEventListener('click', (e) => handlePointer(getCanvasCoords(e)));
        canvas.addEventListener('touchstart', (e) => {{
            e.preventDefault();
            handlePointer(getCanvasCoords(e));
        }}, {{ passive: false }});

        requestAnimationFrame(render);
    </script>
</body>
</html>
"""

components.html(GAME_HTML, height=720, scrolling=False)

with st.sidebar:
    st.header("🃏 Balatro: Factor Común")
    st.caption("UCR • IF0003 Matemática Básica")
    st.markdown(
        """
        **Mecánica Didáctica:**
        - **Motor Pixel Art Canvas:** Renderizado nativo a 480×270 px con escalado entero.
        - **Factor Común Monomio:** Hallar MCD numérico y variable de menor exponente.
        - **Persistencia:** Naipes no seleccionados se conservan para la siguiente ronda.
        """
    )
