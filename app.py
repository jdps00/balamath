"""
Balatro Factor Común - Edición Pixel Art 16-Bit Auténtica
Curso: IF0003 Matemática Básica para Informática Empresarial
Universidad de Costa Rica - Recinto de Paraíso
"""

import os
import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Balatro: Factor Común | IF0003",
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
        max-width: 100% !important;
    }
    .stApp {
        background-color: #050a08;
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

GAME_HTML = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Balatro Factor Común</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap" rel="stylesheet">
    
    <style>
        {font_face_css}

        :root {{
            --pixel-font-title: 'DaydreamFont', 'Press Start 2P', monospace;
            --pixel-font-math: 'BalatroFont', 'KiwiSodaFont', 'Press Start 2P', monospace;
            --pixel-font-body: 'KiwiSodaFont', 'VT323', monospace;
        }}

        * {{
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
            image-rendering: pixelated;
        }}

        body {{
            color: #ffffff;
            font-family: var(--pixel-font-title);
            overflow: hidden;
            user-select: none;
            margin: 0;
            height: 100vh;
            width: 100vw;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background-color: #070e0b;
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
            background: radial-gradient(circle at center, #1b4d36, #07120c);
            z-index: -3;
        }}

        .bg-tint-overlay {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: radial-gradient(circle at center, rgba(20, 60, 42, 0.4) 0%, rgba(4, 14, 9, 0.9) 100%);
            mix-blend-mode: multiply;
            pointer-events: none;
            z-index: -2;
        }}

        .filter-ronda-1 {{ filter: hue-rotate(95deg) saturate(140%) brightness(0.72) contrast(1.2); }}
        .filter-ronda-2 {{ filter: hue-rotate(50deg) saturate(160%) brightness(0.8) contrast(1.25); }}
        .filter-ronda-3 {{ filter: hue-rotate(150deg) saturate(130%) brightness(0.68) contrast(1.2); }}

        /* CAJAS Y BOTONES EN PIXEL ART SÓLIDO */
        .pixel-panel {{
            background: #252b36;
            border: 4px solid #0a0b0e;
            box-shadow: 
                inset 3px 3px 0 #465166, 
                inset -3px -3px 0 #13161c,
                0 6px 0 #050608;
            position: relative;
        }}

        .pixel-panel-inner {{
            background: #11141a;
            border: 3px solid #0a0b0e;
            box-shadow: inset 2px 2px 0 #000000;
        }}

        .pixel-badge-red {{
            background: #d9383a;
            border: 3px solid #0a0b0e;
            box-shadow: 
                inset 2px 2px 0 #f67375, 
                inset -2px -2px 0 #851a1b,
                0 4px 0 #4a0d0e;
            color: #ffffff;
            text-shadow: 2px 2px 0 #000000;
        }}

        .pixel-btn-orange {{
            font-family: var(--pixel-font-title);
            background: #e85d26;
            border: 4px solid #0a0b0e;
            box-shadow: 
                inset 3px 3px 0 #ff8c5c, 
                inset -3px -3px 0 #8e3009,
                0 6px 0 #4a1703;
            color: #ffffff;
            text-shadow: 2px 2px 0 #000000;
            transition: transform 0.05s steps(2);
        }}
        .pixel-btn-orange:hover {{ background: #f86e36; }}
        .pixel-btn-orange:active {{
            transform: translateY(4px);
            box-shadow: 
                inset 3px 3px 0 #8e3009, 
                inset -3px -3px 0 #ff8c5c,
                0 2px 0 #4a1703;
        }}

        .pixel-btn-blue {{
            font-family: var(--pixel-font-title);
            background: #1f78c1;
            border: 3px solid #0a0b0e;
            box-shadow: 
                inset 2px 2px 0 #5aa7e8, 
                inset -2px -2px 0 #0d4472,
                0 5px 0 #06233d;
            color: #ffffff;
            text-shadow: 2px 2px 0 #000000;
        }}

        /* ========================================================
           CARTAS PIXEL ART 16-BIT (ESTILO BALATRO COMPLETO)
           ======================================================== */
        .balatro-pixel-card {{
            width: 106px;
            height: 152px;
            background: #fbf8eb;
            border: 4px solid #0d0f14;
            /* Biselado duro de naipe físico en pixel art */
            box-shadow: 
                inset 3px 3px 0 #ffffff,
                inset -3px -3px 0 #c7bea9,
                0 7px 0 #08090d;
            position: relative;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.08s steps(3);
        }}

        /* Borde interior pixelado */
        .card-inner-pixel-box {{
            position: absolute;
            top: 4px; left: 4px; right: 4px; bottom: 4px;
            border: 2px solid #ddd5be;
            pointer-events: none;
        }}

        /* Esquina superior izquierda */
        .pixel-pip-tl {{
            position: absolute;
            top: 5px; left: 6px;
            display: flex; flex-direction: column; align-items: center;
            line-height: 1;
            pointer-events: none;
        }}

        /* Esquina inferior derecha rotada */
        .pixel-pip-br {{
            position: absolute;
            bottom: 5px; right: 6px;
            display: flex; flex-direction: column; align-items: center;
            line-height: 1;
            transform: rotate(180deg);
            pointer-events: none;
        }}

        .pip-rank-pixel {{
            font-family: var(--pixel-font-title);
            font-size: 11px;
            letter-spacing: -0.5px;
            font-weight: bold;
        }}

        .pip-suit-pixel {{
            font-size: 11px;
            margin-top: 1px;
        }}

        /* Término algebraico central en pixel art */
        .math-center-pixel {{
            font-family: var(--pixel-font-math);
            font-size: 2.2rem;
            font-weight: bold;
            color: #151821;
            text-align: center;
            padding: 0 4px;
            line-height: 1;
            z-index: 2;
            letter-spacing: -1px;
            text-shadow: 1px 1px 0 rgba(0,0,0,0.15);
        }}

        /* Animación de balanceo en pasos de pixel */
        @keyframes pixel-sway-1 {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-7px); }}
        }}
        @keyframes pixel-sway-2 {{
            0%, 100% {{ transform: translateY(-5px); }}
            50% {{ transform: translateY(3px); }}
        }}
        @keyframes pixel-sway-3 {{
            0%, 100% {{ transform: translateY(2px); }}
            50% {{ transform: translateY(-6px); }}
        }}

        .idle-sway-1 {{ animation: pixel-sway-1 3s steps(5) infinite; }}
        .idle-sway-2 {{ animation: pixel-sway-2 3.6s steps(5) infinite; }}
        .idle-sway-3 {{ animation: pixel-sway-3 4s steps(5) infinite; }}

        .balatro-pixel-card:hover {{
            transform: translateY(-16px) !important;
            animation-play-state: paused;
            box-shadow: 
                inset 3px 3px 0 #ffffff,
                inset -3px -3px 0 #c7bea9,
                0 14px 0 #08090d;
            z-index: 20;
        }}

        .balatro-pixel-card.selected {{
            transform: translateY(-26px) !important;
            animation-play-state: paused;
            border-color: #f1b31c;
            box-shadow: 
                inset 3px 3px 0 #fff7b8,
                inset -3px -3px 0 #a97705,
                0 0 0 4px #f1b31c,
                0 14px 0 #4f3600 !important;
            z-index: 30;
        }}

        @media (max-width: 640px) {{
            .balatro-pixel-card {{ width: 86px !important; height: 124px !important; }}
            .math-center-pixel {{ font-size: 1.55rem !important; }}
            .pip-rank-pixel {{ font-size: 9px !important; }}
            .pip-suit-pixel {{ font-size: 8px !important; }}
            #hand-container {{ min-height: 190px !important; }}
        }}

        /* FUEGO DE PUNTOS PIXEL */
        @keyframes pixel-flame {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.12); }}
        }}
        .score-flame-pixel {{
            color: #ffffff;
            font-family: var(--pixel-font-title);
            text-shadow: 3px 3px 0 #d9383a, -3px -3px 0 #f1b31c, 3px -3px 0 #e85d26;
            animation: pixel-flame 0.25s steps(2) infinite;
        }}

        @keyframes shake-pixel {{
            0%, 100% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-8px); }}
            75% {{ transform: translateX(8px); }}
        }}
        .animate-shake {{ animation: shake-pixel 0.22s steps(4); }}

        #fx-canvas {{ position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 50; }}
        .lb-scroll::-webkit-scrollbar {{ width: 6px; }}
        .lb-scroll::-webkit-scrollbar-thumb {{ background: #465166; border: 1px solid #0a0b0e; }}
    </style>
</head>
<body class="p-2 sm:p-4">
    {video_html_tag}
    <div class="bg-tint-overlay"></div>
    <canvas id="fx-canvas"></canvas>

    <!-- INTRO MODAL -->
    <div id="intro-modal" class="fixed inset-0 bg-black/85 z-[1000] flex items-center justify-center p-4">
        <div class="pixel-panel max-w-sm w-full p-6 text-center">
            <div class="pixel-badge-red py-3 px-4 mb-5">
                <h1 class="text-xl sm:text-2xl tracking-wider">FACTOR COMÚN</h1>
                <p class="text-[9px] tracking-widest mt-1 opacity-90">MATEMÁTICA BÁSICA • UCR</p>
            </div>
            
            <div class="pixel-panel-inner p-4 mb-5 text-left">
                <label class="block text-[9px] text-gray-400 mb-2 tracking-wider">APODO DEL JUGADOR:</label>
                <input type="text" id="username-input" class="w-full bg-[#08090c] border-2 border-[#313947] focus:border-[#f1b31c] text-white p-3 text-center uppercase text-xs outline-none" placeholder="TU NOMBRE" maxlength="12">
            </div>

            <button onclick="startGameFromIntro()" class="pixel-btn-orange w-full py-4 text-xs tracking-wider">
                ENTRAR AL JUEGO
            </button>
        </div>
    </div>

    <!-- BOTONES INFERIORES -->
    <div class="fixed bottom-3 left-3 z-40">
        <button onclick="toggleTutorial()" class="pixel-btn-blue text-[9px] sm:text-[10px] px-3.5 py-2.5">
            💡 TUTO
        </button>
    </div>
    <div class="fixed bottom-3 right-3 z-40">
        <button onclick="toggleLeaderboard()" class="pixel-btn-orange text-[9px] sm:text-[10px] px-3.5 py-2.5">
            🏆 RANK
        </button>
    </div>

    <!-- PANEL TUTORIAL -->
    <div id="tutorial-panel" class="fixed left-0 top-0 h-full w-72 sm:w-80 bg-[#191d24] border-r-4 border-black p-4 flex flex-col z-50 transform -translate-x-full transition-transform duration-200">
        <div class="flex justify-between items-center mb-4 border-b-2 border-white/20 pb-2">
            <div class="pixel-badge-red px-3 py-1 text-[9px]">CÓMO JUGAR</div>
            <button onclick="toggleTutorial()" class="text-white text-base">✕</button>
        </div>
        <div class="pixel-panel-inner p-3 text-2xl text-center mb-3">
            🍎🍉 <span class="text-red-400">+</span> 🍎🍌
        </div>
        <p class="text-[9px] text-yellow-300 text-center mb-3">SACA LO QUE SE REPITE (🍎)</p>
        <div class="pixel-panel-inner p-3 text-2xl text-center mb-4">
            🍎<span class="text-gray-400">(</span>🍉 <span class="text-red-400">+</span> 🍌<span class="text-gray-400">)</span>
        </div>
        <div class="text-[13px] text-gray-300 leading-relaxed font-['KiwiSodaFont',monospace] space-y-2">
            <p>1. Selecciona 2 o más cartas que compartan divisores o variables con exponentes comunes.</p>
            <p>2. Presiona "JUGAR MANO" para acumular puntos calculados por el algoritmo.</p>
            <p>3. Las cartas no jugadas permanecen en la mesa para la siguiente ronda.</p>
        </div>
    </div>

    <!-- PANEL CLASIFICACIÓN -->
    <aside id="leaderboard-panel" class="fixed right-0 top-0 h-full w-72 sm:w-80 bg-[#191d24] border-l-4 border-black p-4 flex flex-col z-50 transform translate-x-full transition-transform duration-200">
        <div class="flex justify-between items-center mb-3 border-b-2 border-white/20 pb-2">
            <button onclick="toggleLeaderboard()" class="text-white text-base">✕</button>
            <div class="pixel-badge-red px-3 py-1 text-[9px]">POSICIONES</div>
        </div>
        <div class="text-[9px] text-gray-400 mb-2 text-center">COMPITIENDO EN EL AULA</div>
        <div id="leaderboard" class="flex-grow overflow-y-auto lb-scroll flex flex-col gap-1.5 pr-1"></div>
    </aside>

    <!-- HEADER SUPERIOR -->
    <header class="flex justify-between items-center z-10 max-w-5xl mx-auto w-full gap-2 px-1">
        <div class="pixel-panel px-3 py-2 text-center min-w-[95px] sm:min-w-[125px]">
            <div class="text-[8px] sm:text-[9px] text-gray-400">NIVEL <span id="level-display" class="text-yellow-400 text-xs sm:text-sm">1</span></div>
            <div class="text-[7px] sm:text-[8px] text-gray-300 mt-0.5">RONDA <span id="round-display" class="text-white">1</span>/3</div>
        </div>

        <!-- 3 Comodines Pixel -->
        <div class="flex justify-center gap-1.5 sm:gap-2.5">
            <button id="btn-joker-reveal" onclick="useJoker('reveal')" title="Revelar factor" class="pixel-panel p-2 text-base sm:text-lg relative active:translate-y-1">
                👁️
                <span id="qty-reveal" class="absolute -top-2 -right-2 bg-red-600 text-white text-[8px] px-1 border border-black">1</span>
            </button>
            <button id="btn-joker-reroll" onclick="useJoker('reroll')" title="Cambiar mano" class="pixel-panel p-2 text-base sm:text-lg relative active:translate-y-1">
                🎲
                <span id="qty-reroll" class="absolute -top-2 -right-2 bg-red-600 text-white text-[8px] px-1 border border-black">1</span>
            </button>
            <button id="btn-joker-skip" onclick="useJoker('skip')" title="Saltar nivel" class="pixel-panel p-2 text-base sm:text-lg relative active:translate-y-1 opacity-40">
                ⏭️
                <span id="qty-skip" class="absolute -top-2 -right-2 bg-yellow-500 text-black text-[8px] px-1 border border-black">0</span>
            </button>
        </div>

        <div class="pixel-panel px-3 py-2 text-center min-w-[95px] sm:min-w-[125px]">
            <div class="text-[8px] sm:text-[9px] text-gray-400">PUNTOS</div>
            <div id="total-score" class="font-['KiwiSodaFont',monospace] text-xl sm:text-2xl text-yellow-400 leading-none mt-1">0</div>
            <div class="text-[7px] text-gray-400 mt-0.5">Rank: <span id="player-rank">#25</span></div>
        </div>
    </header>

    <!-- ÁREA DE NAIPES PIXEL ART -->
    <main class="flex-grow flex flex-col items-center justify-center relative w-full max-w-5xl mx-auto my-auto">
        <div id="hand-container" class="flex justify-center items-center flex-wrap gap-2.5 sm:gap-4 w-full px-2 mb-6"></div>

        <button id="btn-play" onclick="playHand()" disabled class="pixel-panel bg-[#151820] text-gray-500 px-8 py-3.5 sm:px-12 sm:py-4 text-xs sm:text-sm tracking-widest opacity-40 cursor-not-allowed">
            JUGAR MANO
        </button>

        <div id="flame-score-container" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 hidden opacity-0 transition-opacity duration-200 z-40 pointer-events-none text-center">
            <div id="flame-score" class="text-3xl sm:text-5xl score-flame-pixel tracking-wider">0</div>
        </div>
    </main>

    <!-- MODAL FIN DE NIVEL -->
    <div id="level-modal" class="fixed inset-0 bg-black/85 z-50 hidden flex items-center justify-center p-4">
        <div class="pixel-panel max-w-sm w-full p-6 text-center">
            <div class="pixel-badge-red py-2 px-4 mb-4">
                <h2 class="text-lg sm:text-xl">NIVEL COMPLETADO</h2>
            </div>
            <div class="flex justify-center gap-3 my-4" id="modal-stars"></div>
            <p id="modal-desc" class="pixel-panel-inner p-3 text-gray-200 font-['KiwiSodaFont',monospace] text-base leading-relaxed mb-5"></p>
            <button onclick="nextLevel()" class="pixel-btn-orange w-full py-3.5 text-xs tracking-wider">
                SIGUIENTE NIVEL ➔
            </button>
        </div>
    </div>

    <!-- ALERTA PIXEL -->
    <div id="alert-modal" class="fixed top-12 left-1/2 -translate-x-1/2 pixel-badge-red font-['KiwiSodaFont',monospace] text-base px-5 py-2.5 z-50 hidden text-center max-w-[90vw]">
        <span id="alert-text"></span>
    </div>

    <script>
        const aCtx = new (window.AudioContext || window.webkitAudioContext)();
        function playTone(freq, type, dur, vol=0.1) {{
            try {{
                if(aCtx.state === 'suspended') aCtx.resume();
                const osc = aCtx.createOscillator(); const gain = aCtx.createGain();
                osc.type = type; osc.frequency.setValueAtTime(freq, aCtx.currentTime);
                gain.gain.setValueAtTime(vol, aCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.0001, aCtx.currentTime + dur);
                osc.connect(gain); gain.connect(aCtx.destination);
                osc.start(); osc.stop(aCtx.currentTime + dur);
            }} catch(e) {{}}
        }}

        const SFX = {{
            hover: () => playTone(320, 'sine', 0.08, 0.04),
            select: () => playTone(540, 'triangle', 0.12, 0.12),
            error: () => {{ playTone(130, 'sawtooth', 0.25, 0.25); setTimeout(() => playTone(90, 'sawtooth', 0.35, 0.25), 100); }},
            flamePop: () => {{ playTone(180, 'sawtooth', 0.28, 0.25); setTimeout(() => playTone(240, 'sawtooth', 0.2, 0.2), 60); }},
            star: () => {{ playTone(880, 'sine', 0.3, 0.2); setTimeout(()=>playTone(1100, 'sine', 0.4, 0.2), 100); }},
            discard: () => playTone(240, 'triangle', 0.15, 0.15),
            winRound: () => {{ playTone(440, 'sine', 0.3, 0.2); setTimeout(() => playTone(659, 'sine', 0.3, 0.2), 150); }}
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

        const cvs = document.getElementById('fx-canvas'); const ctx = cvs.getContext('2d');
        let particles = [];
        window.onresize = () => {{ cvs.width = window.innerWidth; cvs.height = window.innerHeight; }};
        window.onresize();
        function spawnParticles(x, y, count=35) {{
            const colors = ['#f1b31c', '#1d72b8', '#d9383a', '#ffffff'];
            for(let i=0; i<count; i++) {{
                const angle = Math.random() * Math.PI * 2; const speed = 2 + Math.random() * 7;
                particles.push({{ x, y, vx: Math.cos(angle)*speed, vy: Math.sin(angle)*speed-2, color: colors[Math.floor(Math.random()*colors.length)], size: 4, life: 1.0, decay: 0.03 }});
            }}
        }}
        function renderParticles() {{
            ctx.clearRect(0,0,cvs.width,cvs.height);
            for(let i=particles.length-1; i>=0; i--) {{
                const p = particles[i];
                p.x += p.vx; p.y += p.vy; p.vy += 0.18; p.life -= p.decay;
                if(p.life<=0){{ particles.splice(i,1); continue; }}
                ctx.fillStyle = p.color; ctx.globalAlpha = p.life; ctx.fillRect(Math.floor(p.x), Math.floor(p.y), p.size, p.size);
            }}
            ctx.globalAlpha = 1; requestAnimationFrame(renderParticles);
        }}
        renderParticles();

        const names = ["Andrey_U", "Fabiola_P", "Bryan_Q", "Daniela_CR", "Nath_V", "Isaac_H", "Carlos_S", "M_Estela", "K_Navas", "Diego_R", "K_Mora", "Josue_B", "Maria_F", "Valeria_G", "Seidy_T", "Allan_P", "Cesar_O", "Monica_V", "Lucia_Z", "R_Arias", "Erick_L", "S_Díaz", "Karla_C", "Luis_M"];
        let leaderboardData = [];
        let playerName = "ESTUDIANTE";
        
        function initLeaderboard() {{
            leaderboardData = names.map(n => ({{ name: n, score: Math.floor(Math.random() * 1100 + 400), level: 1 }}));
            leaderboardData.push({{ name: playerName, score: score, level: level, isPlayer: true }});
            updateLeaderboardUI();
            setInterval(simulateClassroomActivity, 4000);
        }}

        function simulateClassroomActivity() {{
            leaderboardData.forEach(p => {{
                if(!p.isPlayer && Math.random() > 0.45) {{
                    p.score += Math.floor(Math.random() * 300 * Math.max(1, p.level));
                    if(p.score > 2000 * p.level) p.level++;
                }}
            }});
            updateLeaderboardUI();
        }}

        function updateLeaderboardUI() {{
            const playerEntry = leaderboardData.find(p => p.isPlayer);
            if(playerEntry) {{
                playerEntry.score = score;
                playerEntry.level = level;
            }}

            leaderboardData.sort((a,b) => b.score - a.score);
            const container = document.getElementById('leaderboard');
            if(!container) return;
            container.innerHTML = '';

            let playerRank = 25;
            leaderboardData.forEach((p, idx) => {{
                if(p.isPlayer) playerRank = idx + 1;
                
                const medal = idx === 0 ? "🥇" : idx === 1 ? "🥈" : idx === 2 ? "🥉" : `#${{idx+1}}`;
                const div = document.createElement('div');
                div.className = `flex justify-between items-center text-sm p-1.5 ${{p.isPlayer ? 'bg-[#1f78c1] text-white border-2 border-white' : 'pixel-panel-inner text-gray-300'}}`;
                div.innerHTML = `
                    <span class="truncate max-w-[130px] font-['KiwiSodaFont',monospace]">${{medal}} ${{p.name}} ${{p.isPlayer ? '(TÚ)' : ''}}</span>
                    <span class="text-yellow-400 font-['KiwiSodaFont',monospace] font-bold">${{p.score.toLocaleString()}}</span>
                `;
                container.appendChild(div);
            }});

            const rankEl = document.getElementById('player-rank');
            if (rankEl) rankEl.textContent = `#${{playerRank}}`;
        }}

        function toggleTutorial() {{
            SFX.hover();
            document.getElementById('tutorial-panel').classList.toggle('-translate-x-full');
        }}

        function toggleLeaderboard() {{
            SFX.hover();
            document.getElementById('leaderboard-panel').classList.toggle('translate-x-full');
        }}

        function startGameFromIntro() {{
            const input = document.getElementById('username-input').value.trim();
            if(input) playerName = input.toUpperCase();
            
            document.getElementById('intro-modal').classList.add('hidden');
            SFX.select();
            playBGM();
            
            initLeaderboard();
            startRound();
            updateUI();
        }}

        let level = 1;
        let round = 1;
        let score = 0;
        let hand = [];
        let nextCardId = 0;
        let levelStats = {{ optimalPossible: 0, actualCorrect: 0, errors: 0 }};
        let comodines = {{ reveal: 1, reroll: 1, skip: 0 }};

        const handContainer = document.getElementById('hand-container');
        const btnPlay = document.getElementById('btn-play');

        function gcd(a, b) {{ a=Math.abs(a); b=Math.abs(b); return b === 0 ? a : gcd(b, a % b); }}

        function formatTerm(c, x, y) {{
            let s = "";
            if (c === -1 && (x>0||y>0)) s += "-";
            else if (c !== 1 || (x===0&&y===0)) s += c;
            
            if (x === 1) s += "x"; else if (x > 1) s += `x^${{x}}`;
            if (y === 1) s += "y"; else if (y > 1) s += `y^${{y}}`;
            return s;
        }}

        function getCardCornerRank(card) {{
            if (card.x > 0 && card.y === 0) return card.x === 1 ? "X" : `X${{card.x}}`;
            if (card.y > 0 && card.x === 0) return card.y === 1 ? "Y" : `Y${{card.y}}`;
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
            const suitColor = (suit === '♥' || suit === '♦') ? '#d9383a' : '#1f78c1';

            return {{ c, x, y, str: formatTerm(c,x,y), suit, suitColor, selected: false, id: nextCardId++ }};
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
                for(let j=0; j<n; j++) {{
                    if((i & (1<<j))) subset.push(hand[j]);
                }}
                if(subset.length > 1) {{
                    const info = getCommonFactorInfo(subset);
                    if(info.isValid && subset.length > maxSubset) maxSubset = subset.length;
                }}
            }}
            return maxSubset;
        }}

        function startRound() {{
            document.getElementById('level-display').textContent = level;
            document.getElementById('round-display').textContent = round;
            
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
            renderCards();
            updateUI();
        }}

        function renderCards() {{
            handContainer.innerHTML = '';
            hand.forEach((card, idx) => {{
                const el = document.createElement('div');
                const swayClass = idx % 3 === 0 ? 'idle-sway-1' : (idx % 3 === 1 ? 'idle-sway-2' : 'idle-sway-3');
                el.className = `balatro-pixel-card ${{card.selected ? 'selected' : swayClass}}`;
                
                const cornerRank = getCardCornerRank(card);

                el.innerHTML = `
                    <div class="card-inner-pixel-box"></div>
                    <div class="pixel-pip-tl" style="color: ${{card.suitColor}};">
                        <span class="pip-rank-pixel">${{cornerRank}}</span>
                        <span class="pip-suit-pixel">${{card.suit}}</span>
                    </div>
                    <div class="math-center-pixel">${{card.str}}</div>
                    <div class="pixel-pip-br" style="color: ${{card.suitColor}};">
                        <span class="pip-rank-pixel">${{cornerRank}}</span>
                        <span class="pip-suit-pixel">${{card.suit}}</span>
                    </div>
                `;
                
                el.onclick = () => {{
                    card.selected = !card.selected;
                    if(card.selected) SFX.select(); else SFX.hover();
                    renderCards();
                    updatePlayButton();
                }};
                handContainer.appendChild(el);
            }});
        }}

        function updatePlayButton() {{
            const selected = hand.filter(c => c.selected);
            if(selected.length > 0) {{
                btnPlay.disabled = false;
                btnPlay.className = "pixel-btn-orange px-8 py-3.5 sm:px-12 sm:py-4 text-xs sm:text-sm tracking-widest cursor-pointer";
            }} else {{
                btnPlay.disabled = true;
                btnPlay.className = "pixel-panel bg-[#151820] text-gray-500 px-8 py-3.5 sm:px-12 sm:py-4 text-xs sm:text-sm tracking-widest opacity-40 cursor-not-allowed";
            }}
        }}

        function playHand() {{
            const selected = hand.filter(c => c.selected);
            const info = getCommonFactorInfo(selected);

            if(selected.length < 2 || !info || !info.isValid) {{
                SFX.error();
                handContainer.classList.add('animate-shake');
                levelStats.errors++;
                setTimeout(() => handContainer.classList.remove('animate-shake'), 220);
                return;
            }}

            btnPlay.disabled = true;
            levelStats.actualCorrect += selected.length;
            
            let basePts = 50 * level;
            let mult = selected.length * selected.length;
            let handScore = basePts * mult;
            score += handScore;
            
            document.getElementById('total-score').textContent = score.toLocaleString();
            
            SFX.flamePop();
            const flameScore = document.getElementById('flame-score');
            const flameContainer = document.getElementById('flame-score-container');
            flameScore.textContent = "+" + handScore.toLocaleString();
            flameContainer.classList.remove('hidden');
            flameContainer.style.opacity = '1';
            spawnParticles(window.innerWidth/2, window.innerHeight/2, 40);

            hand = hand.filter(c => !c.selected);

            setTimeout(() => {{
                flameContainer.style.opacity = '0';
                setTimeout(() => flameContainer.classList.add('hidden'), 150);
                
                round++;
                if(round > 3) {{
                    endLevel();
                }} else {{
                    startRound();
                }}
            }}, 1100);
        }}

        function endLevel() {{
            let precision = levelStats.optimalPossible > 0 ? (levelStats.actualCorrect / levelStats.optimalPossible) : 1;
            precision -= (levelStats.errors * 0.1);
            if(precision < 0) precision = 0;

            let stars = 0;
            if(precision >= 0.88) stars = 3;
            else if (precision >= 0.5) stars = 2;
            else if (precision >= 0.2) stars = 1;

            const modal = document.getElementById('level-modal');
            const starContainer = document.getElementById('modal-stars');
            const desc = document.getElementById('modal-desc');

            starContainer.innerHTML = '';
            for(let i=0; i<3; i++) {{
                setTimeout(() => SFX.star(), i * 250);
                if(i < stars) {{
                    starContainer.innerHTML += `<span class="text-yellow-400 text-3xl sm:text-4xl">★</span>`;
                }} else {{
                    starContainer.innerHTML += `<span class="text-gray-600 text-3xl sm:text-4xl">★</span>`;
                }}
            }}

            let bonusScore = stars * 1000 * level;
            score += bonusScore;
            document.getElementById('total-score').textContent = score.toLocaleString();

            if(stars === 3) {{
                comodines.skip++;
                updateUI();
                desc.innerHTML = `¡PRECISIÓN PERFECTA!<br>Ganaste un comodín SALTAR NIVEL.<br>Bono: +${{bonusScore.toLocaleString()}} pts`;
            }} else {{
                desc.innerHTML = `Precisión: ${{Math.round(precision*100)}}%. Hubo términos sin factorizar.<br>Bono: +${{bonusScore.toLocaleString()}} pts`;
            }}

            modal.classList.remove('hidden');
        }}

        function nextLevel() {{
            document.getElementById('level-modal').classList.add('hidden');
            level++;
            round = 1;
            hand = [];
            levelStats = {{ optimalPossible: 0, actualCorrect: 0, errors: 0 }};
            startRound();
        }}

        function updateUI() {{
            document.getElementById('qty-reveal').textContent = comodines.reveal;
            document.getElementById('qty-reroll').textContent = comodines.reroll;
            document.getElementById('qty-skip').textContent = comodines.skip;
            
            document.getElementById('btn-joker-reveal').style.opacity = comodines.reveal > 0 ? '1' : '0.4';
            document.getElementById('btn-joker-reroll').style.opacity = comodines.reroll > 0 ? '1' : '0.4';
            document.getElementById('btn-joker-skip').style.opacity = comodines.skip > 0 ? '1' : '0.4';
        }}

        function showAlert(msg) {{
            const el = document.getElementById('alert-modal');
            document.getElementById('alert-text').innerHTML = msg;
            el.classList.remove('hidden');
            el.style.opacity = '1';
            setTimeout(() => {{
                el.style.opacity = '0';
                setTimeout(() => el.classList.add('hidden'), 200);
            }}, 2600);
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
                    showAlert(`🔎 FACTOR DOMINANTE: <b>${{bestFactor}}</b> (en ${{maxSubset}} cartas)`);
                }} else {{
                    showAlert(`🔎 No hay factores comunes detectables en esta mano.`);
                }}
            }} 
            else if (type === 'reroll') {{
                comodines.reroll--;
                SFX.discard();
                hand = [];
                startRound();
                showAlert("🎲 ¡MANO CAMBIADA!");
            }}
            else if (type === 'skip') {{
                comodines.skip--;
                SFX.winRound();
                levelStats.actualCorrect = 1; 
                levelStats.optimalPossible = 1;
                levelStats.errors = 0;
                endLevel();
            }}
            updateUI();
        }}
    </script>
</body>
</html>
"""

components.html(GAME_HTML, height=720, scrolling=False)

with st.sidebar:
    st.header("🧮 Balatro: Factor Común")
    st.caption("UCR • IF0003 Matemática Básica")
    st.markdown(
        """
        **Mecánica Didáctica:**
        - **3 Rondas por Nivel:** Escala la complejidad de los monomios.
        - **Factor Común Monomio:** Hallar MCD numérico y variable de menor exponente.
        - **Reutilización:** Cartas no jugadas pasan a la siguiente ronda.
        """
    )
