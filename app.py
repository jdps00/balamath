"""
Balatro Factor Común - Aplicación Educativa en Streamlit
Curso: IF0003 Matemática Básica para Informática Empresarial
Universidad de Costa Rica - Recinto de Paraíso
"""

import os
import base64
import streamlit as st
import streamlit.components.v1 as components

# Configuración de página optimizada para móvil y proyector
st.set_page_config(
    page_title="Balatro: Factor Común | IF0003",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS complementarios de Streamlit
st.markdown(
    """
    <style>
    /* Ocultar barra superior y pie de página de Streamlit para inmersión completa */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0.2rem;
        padding-bottom: 0.2rem;
        padding-left: 0.2rem;
        padding-right: 0.2rem;
        max-width: 100% !important;
    }
    .stApp {
        background-color: #06110d;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------------
# CARGA Y CODIFICACIÓN EN BASE64 DE VIDEO Y FUENTES LOCALES
# ---------------------------------------------------------------------------
def get_base64_encoded_file(filename):
    """Codifica un archivo local a Base64 si existe en el directorio."""
    for candidate in [filename, filename.lower(), filename.upper()]:
        if os.path.exists(candidate):
            with open(candidate, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
    return None

# Buscar video de fondo (fakcpg.mp4 o .gif)
bg_video_b64 = (
    get_base64_encoded_file("fakcpg.mp4")
    or get_base64_encoded_file("faKcpg.mp4")
    or get_base64_encoded_file("fakcpg.gif")
    or get_base64_encoded_file("faKcpg.gif")
)

# Cargar fuentes locales
font_daydream_b64 = (
    get_base64_encoded_file("Daydream DEMO.otf")
    or get_base64_encoded_file("Daydream.otf")
    or get_base64_encoded_file("Daydream.ttf")
)

font_kiwisoda_b64 = (
    get_base64_encoded_file("KiwiSoda.ttf")
    or get_base64_encoded_file("KiwiSoda.otf")
)

# Inyección condicional de @font-face en base64
font_faces_css = ""
if font_daydream_b64:
    font_faces_css += f"""
    @font-face {{
        font-family: 'Daydream';
        src: url(data:font/otf;base64,{font_daydream_b64}) format('opentype');
        font-weight: normal;
        font-style: normal;
    }}
    """
else:
    font_faces_css += """
    @font-face {
        font-family: 'Daydream';
        src: local('Press Start 2P');
    }
    """

if font_kiwisoda_b64:
    font_faces_css += f"""
    @font-face {{
        font-family: 'KiwiSoda';
        src: url(data:font/ttf;base64,{font_kiwisoda_b64}) format('truetype');
        font-weight: normal;
        font-style: normal;
    }}
    """
else:
    font_faces_css += """
    @font-face {
        font-family: 'KiwiSoda';
        src: local('VT323');
    }
    """

# Elemento HTML del video de fondo si existe
if bg_video_b64:
    bg_video_html = f"""
    <video id="bg-video-element" class="bg-layer round-hue-1" autoplay muted loop playsinline>
        <source src="data:video/mp4;base64,{bg_video_b64}" type="video/mp4">
    </video>
    """
else:
    bg_video_html = """
    <div id="bg-video-element" class="bg-fallback-swirl round-hue-1"></div>
    """

# ---------------------------------------------------------------------------
# CÓDIGO HTML, CSS Y JAVASCRIPT COMPLETO DEL JUEGO
# ---------------------------------------------------------------------------
GAME_HTML = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Balatro Factor Común</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap" rel="stylesheet">
    
    <style>
        {font_faces_css}

        :root {{
            --balatro-blue: #2d82d7;
            --balatro-red: #d73a3a;
            --balatro-yellow: #f5d342;
        }}

        * {{
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }}

        body {{
            color: white;
            font-family: 'KiwiSoda', 'VT323', monospace;
            overflow: hidden;
            user-select: none;
            margin: 0;
            height: 100vh;
            width: 100vw;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background-color: #06110d;
        }}

        .font-arcade {{ font-family: 'Daydream', 'Press Start 2P', cursive; }}
        .font-body {{ font-family: 'KiwiSoda', 'VT323', monospace; }}

        /* VIDEO / ANIMACIÓN DE FONDO CON TRANSICIÓN DE TONALIDAD */
        .bg-layer {{
            position: fixed;
            top: 50%;
            left: 50%;
            width: 110vw;
            height: 110vh;
            transform: translate(-50%, -50%);
            object-fit: cover;
            z-index: -3;
            pointer-events: none;
            transition: filter 1.2s ease-in-out;
        }}

        /* Fondo de respaldo procedural si el archivo de video no está presente */
        @keyframes bg-swirl-alt {{
            0% {{ transform: translate(-50%, -50%) rotate(0deg) scale(1.1); }}
            50% {{ transform: translate(-50%, -50%) rotate(180deg) scale(1.25); }}
            100% {{ transform: translate(-50%, -50%) rotate(360deg) scale(1.1); }}
        }}
        .bg-fallback-swirl {{
            position: fixed;
            top: 50%;
            left: 50%;
            width: 140vw;
            height: 140vh;
            z-index: -3;
            background: 
                radial-gradient(circle at center, transparent 20%, rgba(6, 17, 13, 0.85) 75%),
                conic-gradient(from 0deg at 50% 50%, #0d2119, #1b533a, #237b4f, #0d2119, #3ca871, #133a28, #0d2119);
            animation: bg-swirl-alt 22s linear infinite;
            transition: filter 1.2s ease-in-out;
        }}

        /* CAMBIO DE TONALIDADES POR RONDA */
        .round-hue-1 {{ filter: contrast(125%) brightness(85%) hue-rotate(0deg); }}
        .round-hue-2 {{ filter: contrast(140%) brightness(95%) hue-rotate(-35deg); }}
        .round-hue-3 {{ filter: contrast(130%) brightness(85%) hue-rotate(45deg); }}

        /* ========================================================
           CARTAS PIXEL ART BLANCAS (ESTILO NAIRES BALATRO)
           ======================================================== */
        .balatro-card {{
            width: 98px;
            height: 146px;
            background-color: #fbfbfb;
            border-radius: 6px;
            border: 3px solid #1a1a24;
            box-shadow: 
                inset -2px -2px 0px 0px #cfd3dc,
                inset 2px 2px 0px 0px #ffffff,
                0 6px 0px 0px #0b0c10,
                0 10px 14px rgba(0,0,0,0.5);
            color: #111;
            position: relative;
            transition: transform 0.18s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.18s ease;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 5px 6px;
            image-rendering: pixelated;
        }}

        .balatro-card .card-corner {{
            font-family: 'Daydream', cursive;
            font-size: 8px;
            line-height: 1;
            color: #2b2b36;
            text-shadow: 1px 1px 0px #fff;
            user-select: none;
        }}

        .balatro-card .card-corner-bottom {{
            transform: rotate(180deg);
        }}

        .balatro-card .term-center {{
            display: flex;
            align-items: center;
            justify-content: center;
            flex-grow: 1;
            text-align: center;
        }}

        /* Balanceo orgánico continuo estilo Balatro */
        @keyframes balatro-sway-1 {{
            0%, 100% {{ transform: translateY(0px) rotate(-1.5deg); }}
            50% {{ transform: translateY(-7px) rotate(1.2deg); }}
        }}
        @keyframes balatro-sway-2 {{
            0%, 100% {{ transform: translateY(-4px) rotate(1.4deg); }}
            50% {{ transform: translateY(3px) rotate(-1.8deg); }}
        }}
        @keyframes balatro-sway-3 {{
            0%, 100% {{ transform: translateY(2px) rotate(-0.8deg); }}
            50% {{ transform: translateY(-6px) rotate(1.6deg); }}
        }}

        .idle-sway-1 {{ animation: balatro-sway-1 3.2s ease-in-out infinite; }}
        .idle-sway-2 {{ animation: balatro-sway-2 3.8s ease-in-out infinite; }}
        .idle-sway-3 {{ animation: balatro-sway-3 4.1s ease-in-out infinite; }}

        .balatro-card:hover {{
            transform: translateY(-14px) scale(1.05) rotate(0deg) !important;
            animation-play-state: paused;
            border-color: #2d82d7;
            box-shadow: 
                inset -2px -2px 0px 0px #cbd5e1,
                inset 2px 2px 0px 0px #ffffff,
                0 0 0 3px #2d82d7,
                0 12px 18px rgba(0,0,0,0.6);
            z-index: 20;
        }}

        .balatro-card.selected {{
            transform: translateY(-24px) scale(1.08) rotate(0deg) !important;
            animation-play-state: paused;
            border-color: var(--balatro-yellow) !important;
            box-shadow: 
                inset -2px -2px 0px 0px #fde68a,
                inset 2px 2px 0px 0px #ffffff,
                0 0 0 3px var(--balatro-yellow),
                0 0 0 5px var(--balatro-blue),
                0 16px 22px rgba(0,0,0,0.7) !important;
            z-index: 30;
        }}

        @media (max-width: 640px) {{
            .balatro-card {{ width: 80px !important; height: 120px !important; padding: 4px 5px !important; }}
            .balatro-card .card-corner {{ font-size: 7px !important; }}
            .balatro-card .term-text {{ font-size: 1.35rem !important; }}
            #hand-container {{ min-height: 240px !important; }}
        }}

        /* Efecto Flotante de Puntuación con Fuego */
        @keyframes flame-flicker {{
            0% {{ text-shadow: 0 0 10px #ff5a00, 0 -5px 15px #ff9c00, 0 -10px 20px #ffce00; transform: scale(1); }}
            50% {{ text-shadow: 0 0 20px #ff5a00, 0 -10px 25px #ff9c00, 0 -15px 30px #ffce00; transform: scale(1.1); }}
            100% {{ text-shadow: 0 0 10px #ff5a00, 0 -5px 15px #ff9c00, 0 -10px 20px #ffce00; transform: scale(1); }}
        }}
        .score-flame {{ color: #fff; animation: flame-flicker 0.6s infinite alternate; }}

        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            20% {{ transform: translateX(-8px) rotate(-3deg); }}
            40% {{ transform: translateX(8px) rotate(3deg); }}
            60% {{ transform: translateX(-8px) rotate(-3deg); }}
            80% {{ transform: translateX(8px) rotate(3deg); }}
        }}
        .animate-shake {{ animation: shake 0.35s ease-in-out; }}

        #fx-canvas {{ position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 50; }}

        .lb-scroll::-webkit-scrollbar {{ width: 4px; }}
        .lb-scroll::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.2); border-radius: 4px; }}
    </style>
</head>
<body class="p-2 sm:p-4">
    <!-- CAPA DE VIDEO O FONDO DINÁMICO -->
    {bg_video_html}

    <canvas id="fx-canvas"></canvas>

    <!-- INTRO MODAL (Usuario del estudiante) -->
    <div id="intro-modal" class="fixed inset-0 bg-black/95 z-[1000] flex items-center justify-center p-4 backdrop-blur-md">
        <div class="bg-[#151821] border-4 border-emerald-500 rounded-2xl max-w-sm w-full p-6 text-center shadow-[0_0_50px_rgba(16,185,129,0.4)]">
            <h1 class="font-arcade text-2xl sm:text-3xl text-emerald-400 mb-2 animate-pulse leading-snug" style="text-shadow: 0 0 20px #10b981;">
                FACTOR<br>COMÚN
            </h1>
            <p class="font-arcade text-[9px] text-gray-300 mb-6 mt-4">INGRESA TU USUARIO</p>
            <input type="text" id="username-input" class="w-full bg-black border-2 border-white/20 text-white font-arcade p-3 rounded mb-6 text-center focus:border-yellow-400 outline-none uppercase text-xs" placeholder="TU NOMBRE" maxlength="12">
            <button onclick="startGameFromIntro()" class="w-full bg-emerald-500 hover:bg-emerald-400 text-black font-arcade py-4 rounded-xl text-xs transition-transform active:scale-95 shadow-[0_0_20px_rgba(16,185,129,0.5)] cursor-pointer">
                ENTRAR AL JUEGO
            </button>
        </div>
    </div>

    <!-- BOTONES INFERIORES FIJOS -->
    <div class="fixed bottom-3 left-3 z-40">
        <button onclick="toggleTutorial()" class="bg-purple-900/90 border-2 border-purple-400 text-white font-arcade text-[10px] p-3 rounded-xl shadow-[0_0_15px_rgba(168,85,247,0.5)] hover:scale-105 transition-transform cursor-pointer">
            💡 TUTO
        </button>
    </div>
    <div class="fixed bottom-3 right-3 z-40">
        <button onclick="toggleLeaderboard()" class="bg-blue-900/90 border-2 border-blue-400 text-white font-arcade text-[10px] p-3 rounded-xl shadow-[0_0_15px_rgba(59,130,246,0.5)] hover:scale-105 transition-transform cursor-pointer">
            🏆 RANK
        </button>
    </div>

    <!-- PANEL TUTORIAL LATERAL -->
    <div id="tutorial-panel" class="fixed left-0 top-0 h-full w-64 sm:w-72 bg-black/95 border-r-2 border-purple-500/50 p-4 flex flex-col z-50 transform -translate-x-full transition-transform duration-300 shadow-2xl">
        <div class="flex justify-between items-center mb-6 border-b border-purple-500/30 pb-2 mt-2">
            <h3 class="font-arcade text-[11px] text-purple-400">💡 ¿CÓMO JUGAR?</h3>
            <button onclick="toggleTutorial()" class="text-white text-xl cursor-pointer">✕</button>
        </div>
        <div class="text-2xl bg-black/50 p-3 rounded-xl border border-gray-700 mb-4 text-center">
            🍎🍉 <span class="text-pink-500">+</span> 🍎🍌
        </div>
        <p class="text-[10px] text-gray-300 font-arcade text-center mb-4 leading-relaxed">SACA LO QUE<br>TIENEN EN COMÚN (🍎)</p>
        <div class="text-2xl bg-purple-900/30 p-3 rounded-xl border border-purple-500 text-center mb-6">
            🍎<span class="text-gray-400 text-lg">(</span>🍉 <span class="text-pink-500 text-lg">+</span> 🍌<span class="text-gray-400 text-lg">)</span>
        </div>
        <p class="text-[9px] text-gray-400 font-arcade text-center leading-relaxed">
            1. Selecciona las cartas que comparten factores numéricos o algebraicos.<br><br>
            2. Presiona "JUGAR MANO".<br><br>
            3. ¡Arma el mayor combo posible!
        </p>
    </div>

    <!-- PANEL LATERAL DE RANKING (25 JUGADORES) -->
    <aside id="leaderboard-panel" class="fixed right-0 top-0 h-full w-64 sm:w-72 bg-black/95 border-l-2 border-blue-500/50 p-3 flex flex-col z-50 transform translate-x-full transition-transform duration-300 shadow-2xl">
        <div class="flex justify-between items-center mb-2 border-b border-blue-500/30 pb-2 mt-2">
            <button onclick="toggleLeaderboard()" class="text-white text-xl cursor-pointer">✕</button>
            <div class="text-right">
                <h3 class="font-arcade text-[9px] text-yellow-400">🏆 RANKING EN VIVO</h3>
                <span class="text-[8px] font-arcade text-emerald-400">● 25 JUGADORES</span>
            </div>
        </div>
        <div class="text-[8px] text-gray-400 font-arcade mb-2 text-center">AULA COMPITIENDO EN TIEMPO REAL</div>
        <div id="leaderboard" class="flex-grow overflow-y-auto lb-scroll flex flex-col gap-1 pr-1 font-body">
            <!-- Inyectado por JS -->
        </div>
    </aside>

    <!-- HEADER SUPERIOR: NIVEL, COMODINES Y PUNTAJE -->
    <header class="flex justify-between items-center z-10 max-w-5xl mx-auto w-full gap-2 px-1">
        <!-- Nivel & Ronda -->
        <div class="bg-black/80 border-2 border-emerald-500/60 rounded-xl px-3 py-2 text-center min-w-[85px] sm:min-w-[110px] shadow-lg">
            <div class="text-[8px] sm:text-[9px] text-gray-400 uppercase font-arcade">NIVEL <span id="level-display" class="text-emerald-400 text-xs sm:text-base">1</span></div>
            <div class="text-[8px] sm:text-[9px] text-gray-400 mt-0.5 font-arcade">RONDA <span id="round-display" class="text-white">1</span>/3</div>
        </div>

        <!-- 3 Comodines Balatro -->
        <div class="flex justify-center gap-1.5 sm:gap-3">
            <button id="btn-joker-reveal" onclick="useJoker('reveal')" title="Revelar factor predominante" class="bg-blue-900 border-2 border-blue-400 rounded-xl p-2 sm:p-2.5 text-lg sm:text-2xl relative shadow-[0_0_12px_rgba(59,130,246,0.5)] active:scale-95 transition-transform cursor-pointer">
                👁️
                <span id="qty-reveal" class="absolute -top-1.5 -right-1.5 bg-red-600 text-white text-[8px] font-arcade px-1 rounded-full border border-black">1</span>
            </button>
            <button id="btn-joker-reroll" onclick="useJoker('reroll')" title="Cambiar mano actual" class="bg-purple-900 border-2 border-purple-400 rounded-xl p-2 sm:p-2.5 text-lg sm:text-2xl relative shadow-[0_0_12px_rgba(168,85,247,0.5)] active:scale-95 transition-transform cursor-pointer">
                🎲
                <span id="qty-reroll" class="absolute -top-1.5 -right-1.5 bg-red-600 text-white text-[8px] font-arcade px-1 rounded-full border border-black">1</span>
            </button>
            <button id="btn-joker-skip" onclick="useJoker('skip')" title="Saltar nivel (se desbloquea con 3 estrellas)" class="bg-yellow-700 border-2 border-yellow-400 rounded-xl p-2 sm:p-2.5 text-lg sm:text-2xl relative shadow-[0_0_12px_rgba(234,179,8,0.5)] active:scale-95 transition-transform opacity-40 cursor-pointer">
                ⏭️
                <span id="qty-skip" class="absolute -top-1.5 -right-1.5 bg-red-600 text-white text-[8px] font-arcade px-1 rounded-full border border-black">0</span>
            </button>
        </div>

        <!-- Puntaje Global y Rango -->
        <div class="bg-black/80 border-2 border-red-500/60 rounded-xl px-3 py-2 text-center min-w-[85px] sm:min-w-[110px] shadow-lg">
            <div class="text-[8px] sm:text-[9px] text-gray-400 uppercase font-arcade">PUNTOS</div>
            <div id="total-score" class="text-sm sm:text-lg text-emerald-400 font-arcade mt-0.5">0</div>
            <div class="text-[8px] text-gray-300 font-arcade opacity-75">Rank: <span id="player-rank">#25</span></div>
        </div>
    </header>

    <!-- ZONA CENTRAL DE JUEGO -->
    <main class="flex-grow flex flex-col items-center justify-center relative w-full max-w-5xl mx-auto my-auto">
        <!-- Contenedor de 6 cartas de juego -->
        <div id="hand-container" class="flex justify-center items-center flex-wrap gap-2 sm:gap-3 w-full px-2 mb-4">
            <!-- Inyectado por JS -->
        </div>

        <!-- Botón Jugar Mano -->
        <button id="btn-play" onclick="playHand()" disabled class="bg-gray-800 text-gray-500 border-2 border-gray-700 px-8 py-3.5 sm:px-12 sm:py-4 rounded-xl font-arcade text-[10px] sm:text-xs shadow-2xl transition-all disabled:opacity-40 cursor-not-allowed">
            JUGAR MANO
        </button>

        <!-- Efecto Fuego Puntos Flotantes -->
        <div id="flame-score-container" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 hidden opacity-0 transition-opacity duration-300 z-40 pointer-events-none text-center">
            <div id="flame-score" class="font-arcade text-3xl sm:text-5xl score-flame tracking-wider drop-shadow-[0_0_35px_#ff4500]">0</div>
        </div>
    </main>

    <!-- MODAL NIVEL COMPLETADO (ESTRELLAS Y PRECISIÓN) -->
    <div id="level-modal" class="fixed inset-0 bg-black/90 z-50 hidden flex items-center justify-center backdrop-blur-md p-4">
        <div class="bg-[#151821] border-4 border-yellow-400 rounded-2xl max-w-md w-full p-6 text-center shadow-[0_0_50px_rgba(245,211,66,0.3)]">
            <h2 class="font-arcade text-base sm:text-lg text-yellow-300 mb-2">NIVEL COMPLETADO</h2>
            <div class="flex justify-center gap-3 my-5" id="modal-stars"></div>
            <p id="modal-desc" class="text-gray-300 text-[10px] sm:text-xs font-arcade leading-relaxed mb-6"></p>
            <button onclick="nextLevel()" class="w-full bg-[#f5d342] hover:bg-[#e5c332] text-black font-arcade py-4 rounded-xl text-xs transition-transform active:scale-95 shadow-lg cursor-pointer">
                SIGUIENTE NIVEL ➔
            </button>
        </div>
    </div>

    <!-- ALERTA DE COMODÍN -->
    <div id="alert-modal" class="fixed top-12 left-1/2 -translate-x-1/2 bg-blue-600 border-2 border-white text-white font-arcade text-[10px] sm:text-xs px-5 py-3 rounded-xl shadow-2xl z-50 hidden transition-opacity text-center max-w-[90vw]">
        <span id="alert-text"></span>
    </div>

    <script>
        /* SÍNTESIS DE AUDIO PROCEDURAL */
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

        /* PARTÍCULAS CANVAS */
        const cvs = document.getElementById('fx-canvas'); const ctx = cvs.getContext('2d');
        let particles = [];
        window.onresize = () => {{ cvs.width = window.innerWidth; cvs.height = window.innerHeight; }};
        window.onresize();
        function spawnParticles(x, y, count=30) {{
            const colors = ['#f5d342', '#2d82d7', '#d73a3a', '#ffffff'];
            for(let i=0; i<count; i++) {{
                const angle = Math.random() * Math.PI * 2; const speed = 2 + Math.random() * 7;
                particles.push({{ x, y, vx: Math.cos(angle)*speed, vy: Math.sin(angle)*speed-2, color: colors[Math.floor(Math.random()*colors.length)], size: 3+Math.random()*4, life: 1.0, decay: 0.02+Math.random()*0.02 }});
            }}
        }}
        function renderParticles() {{
            ctx.clearRect(0,0,cvs.width,cvs.height);
            for(let i=particles.length-1; i>=0; i--) {{
                const p = particles[i];
                p.x += p.vx; p.y += p.vy; p.vy += 0.15; p.life -= p.decay;
                if(p.life<=0){{ particles.splice(i,1); continue; }}
                ctx.fillStyle = p.color; ctx.globalAlpha = p.life; ctx.fillRect(p.x, p.y, p.size, p.size);
            }}
            ctx.globalAlpha = 1; requestAnimationFrame(renderParticles);
        }}
        renderParticles();

        /* RANKING SIMULADO DE 25 COMPAÑEROS DE CLASE */
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
                div.className = `flex justify-between items-center text-[10px] p-1.5 rounded ${{p.isPlayer ? 'bg-blue-600/70 border border-cyan-400 font-bold' : 'bg-white/5 text-gray-300'}}`;
                div.innerHTML = `
                    <span>${{medal}} ${{p.name}} ${{p.isPlayer ? '(TÚ)' : ''}}</span>
                    <span class="text-yellow-300 font-arcade text-[9px]">${{p.score.toLocaleString()}}</span>
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

        /* CAMBIO DE COLOR DE FONDO SEGÚN LA RONDA */
        function updateBackgroundForRound() {{
            const bgEl = document.getElementById('bg-video-element');
            if (!bgEl) return;
            
            bgEl.classList.remove('round-hue-1', 'round-hue-2', 'round-hue-3');
            if(round === 1) bgEl.classList.add('round-hue-1');
            else if (round === 2) bgEl.classList.add('round-hue-2');
            else if (round === 3) bgEl.classList.add('round-hue-3');
        }}

        /* LÓGICA DE JUEGO INFINITO Y MATEMÁTICAS */
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
            return {{ c, x, y, str: formatTerm(c,x,y), selected: false, id: nextCardId++ }};
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
                el.className = `balatro-card ${{card.selected ? 'selected' : swayClass}}`;
                
                let tSize = 'text-2xl sm:text-3xl';
                if(card.str.length > 5) tSize = 'text-xl sm:text-2xl';
                if(card.str.length > 8) tSize = 'text-lg sm:text-xl';

                // Etiqueta de esquina estilo naipe pixel art
                let cornerRank = "🂠";
                if (card.x > 0 && card.y > 0) cornerRank = "xy";
                else if (card.x === 2) cornerRank = "x²";
                else if (card.x === 3) cornerRank = "x³";
                else if (card.x === 1) cornerRank = "x";
                else if (card.y > 0) cornerRank = "y";
                else cornerRank = Math.abs(card.c) || "#";

                el.innerHTML = `
                    <div class="flex justify-between items-center w-full">
                        <span class="card-corner">${{cornerRank}}</span>
                        <span class="text-[9px] font-arcade opacity-40">♦</span>
                    </div>
                    <div class="term-center">
                        <span class="term-text font-body ${{tSize}} font-bold tracking-tight text-[#111] px-1">${{card.str}}</span>
                    </div>
                    <div class="flex justify-between items-center w-full">
                        <span class="text-[9px] font-arcade opacity-40">♦</span>
                        <span class="card-corner card-corner-bottom">${{cornerRank}}</span>
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
                btnPlay.className = "bg-[#2d82d7] hover:bg-[#1a5fa6] text-white border-2 border-cyan-300 px-8 py-3.5 sm:px-12 sm:py-4 rounded-xl font-arcade text-[10px] sm:text-xs shadow-[0_0_20px_rgba(45,130,215,0.6)] cursor-pointer transform active:scale-95 transition-all";
            }} else {{
                btnPlay.disabled = true;
                btnPlay.className = "bg-gray-800 text-gray-500 border-2 border-gray-700 px-8 py-3.5 sm:px-12 sm:py-4 rounded-xl font-arcade text-[10px] sm:text-xs opacity-40 cursor-not-allowed";
            }}
        }}

        function playHand() {{
            const selected = hand.filter(c => c.selected);
            const info = getCommonFactorInfo(selected);

            if(selected.length < 2 || !info || !info.isValid) {{
                SFX.error();
                handContainer.classList.add('animate-shake');
                levelStats.errors++;
                setTimeout(() => handContainer.classList.remove('animate-shake'), 400);
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
            spawnParticles(window.innerWidth/2, window.innerHeight/2, 45);

            // Reutilización: Se eliminan las jugadas, las no jugadas persisten
            hand = hand.filter(c => !c.selected);

            setTimeout(() => {{
                flameContainer.style.opacity = '0';
                setTimeout(() => flameContainer.classList.add('hidden'), 250);
                
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
                    starContainer.innerHTML += `<span class="text-yellow-400 text-3xl sm:text-4xl drop-shadow-[0_0_15px_rgba(245,211,66,0.8)] animate-pulse">★</span>`;
                }} else {{
                    starContainer.innerHTML += `<span class="text-gray-700 text-3xl sm:text-4xl">★</span>`;
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
                desc.innerHTML = `Precisión: ${{Math.round(precision*100)}}%. Dejaste términos atrás o hubo fallos.<br>Bono: +${{bonusScore.toLocaleString()}} pts`;
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
                setTimeout(() => el.classList.add('hidden'), 300);
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
                    showAlert(`🔎 FACTOR DOMINANTE:<br><br><span class="text-yellow-300 text-sm sm:text-base">${{bestFactor}}</span> (en ${{maxSubset}} cartas)`);
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

# Renderizar el juego dentro del marco de Streamlit (Adaptable a celular y proyector)
components.html(GAME_HTML, height=720, scrolling=False)

# Barra lateral informativa para la presentación académica
with st.sidebar:
    st.header("🧮 Balatro: Factor Común")
    st.caption("UCR • IF0003 Matemática Básica")
    st.markdown(
        """
        **Mecánica Didáctica:**
        - **3 Rondas por Nivel:** La dificultad de los términos algebraicos escala exponencialmente.
        - **Factor Común Monomio:** Identificar divisores numéricos (MCD) y variables con menor exponente.
        - **Reutilización:** Las cartas no seleccionadas persisten en la siguiente ronda.
        - **Comodines:**
          - 👁️ *Lupa:* Revela el factor común dominante.
          - 🎲 *Dado:* Reroll completo de la mano actual.
          - ⏭️ *Salto:* Se desbloquea con 3 estrellas (precisión perfecta).
        """
    )
