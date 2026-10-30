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
        background-color: #0d2119;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Detección y conversión a Base64 del video o GIF de fondo
video_b64 = None
video_mime = "video/mp4"

for video_candidate in [
    "fakcpg.mp4", "faKcpg.mp4", "fakcpg.MP4",
    "fakcpg.gif", "faKcpg.gif", "fakcpg.GIF",
    "background.mp4", "background.gif"
]:
    if os.path.exists(video_candidate):
        with open(video_candidate, "rb") as vf:
            video_b64 = base64.b64encode(vf.read()).decode("utf-8")
            if video_candidate.lower().endswith(".gif"):
                video_mime = "image/gif"
            else:
                video_mime = "video/mp4"
        break

# Inyección dinámica de las fuentes personalizadas
font_faces = ""

# 1. Fuente Balatro Oficial (balatro.otf)
balatro_font_path = None
for fname in ["balatro.otf", "Balatro.otf", "balatro.ttf"]:
    if os.path.exists(fname):
        balatro_font_path = fname
        break

if balatro_font_path:
    with open(balatro_font_path, "rb") as f:
        bfont_b64 = base64.b64encode(f.read()).decode("utf-8")
        font_faces += f"""
        @font-face {{
            font-family: 'BalatroFont';
            src: url('data:font/otf;base64,{bfont_b64}') format('opentype');
            font-display: swap;
        }}
        """

# 2. Fuentes secundarias de respaldo si existen en la carpeta
for f_pattern, f_family, f_fmt in [
    (["Pixelta.ttf", "pixelta.ttf"], "PixeltaFont", "truetype"),
    (["Daydream DEMO.otf", "daydream demo.otf", "Daydream.otf"], "DaydreamFont", "opentype"),
    (["KiwiSoda.ttf", "kiwisoda.ttf"], "KiwiSodaFont", "truetype"),
]:
    fpath = None
    for fname in f_pattern:
        if os.path.exists(fname):
            fpath = fname
            break
    if fpath:
        with open(fpath, "rb") as f:
            f_b64 = base64.b64encode(f.read()).decode("utf-8")
            font_faces += f"""
            @font-face {{
                font-family: '{f_family}';
                src: url('data:font/{'opentype' if f_fmt=='opentype' else 'truetype'};base64,{f_b64}') format('{f_fmt}');
                font-display: swap;
            }}
            """

# Código HTML, CSS y JavaScript completo del juego Balatro Factor Común
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
        {font_faces}

        :root {{
            --balatro-blue: #2d82d7;
            --balatro-red: #d73a3a;
            --balatro-yellow: #f5d342;
            --card-white: #fdfbf7;
        }}

        * {{
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }}

        /* Tipografías con prioridad en BalatroFont */
        .font-balatro {{
            font-family: 'BalatroFont', 'PixeltaFont', 'DaydreamFont', 'Press Start 2P', monospace;
            letter-spacing: 0.5px;
        }}

        .font-arcade {{
            font-family: 'BalatroFont', 'DaydreamFont', 'Press Start 2P', monospace;
        }}

        .font-ui {{
            font-family: 'BalatroFont', 'KiwiSodaFont', 'VT323', monospace;
        }}

        /* VIDEO / ANIMACIÓN DE FONDO CON FILTRO DE CONTRASTE CINEMATOGRÁFICO */
        #bg-video-container {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            z-index: -3;
        }}

        .bg-media {{
            position: absolute;
            top: 50%;
            left: 50%;
            min-width: 100%;
            min-height: 100%;
            width: auto;
            height: auto;
            transform: translate(-50%, -50%) scale(1.08);
            object-fit: cover;
            transition: filter 1.2s ease-in-out;
        }}

        /* Tonalidades de rotación verde Balatro por ronda */
        .bg-round-1 {{
            filter: hue-rotate(95deg) saturate(145%) contrast(125%) brightness(72%);
        }}
        .bg-round-2 {{
            filter: hue-rotate(120deg) saturate(160%) contrast(135%) brightness(80%);
        }}
        .bg-round-3 {{
            filter: hue-rotate(65deg) saturate(135%) contrast(120%) brightness(68%);
        }}

        /* Capa oscura radial para dar máximo contraste y profundidad a las cartas */
        .bg-tint-overlay {{
            position: fixed;
            inset: 0;
            background: radial-gradient(circle at center, rgba(10, 24, 18, 0.45) 0%, rgba(5, 12, 9, 0.82) 100%);
            pointer-events: none;
            z-index: -1;
        }}

        /* Fallback si no hay video cargado */
        @keyframes bg-swirl-fallback {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        .fallback-swirl {{
            background: linear-gradient(-45deg, #0d2119, #1a4f3b, #091711, #133a28);
            background-size: 400% 400%;
            animation: bg-swirl-fallback 15s ease infinite;
        }}

        body {{
            color: white;
            font-family: 'BalatroFont', 'KiwiSodaFont', 'VT323', monospace;
            overflow: hidden;
            user-select: none;
            margin: 0;
            height: 100vh;
            width: 100vw;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        /* ========================================================
           CARTAS ESTILO BALATRO AUTÉNTICO
           ======================================================== */
        .balatro-card {{
            width: 108px;
            height: 154px;
            background: #ffffff;
            background: linear-gradient(175deg, #ffffff 0%, #fdfcfa 65%, #f4ede0 100%);
            border-radius: 9px;
            box-shadow: 
                0 4px 0 #1b1e26,
                0 8px 18px rgba(0,0,0,0.55),
                inset 0 0 0 2px #ffffff,
                inset 0 0 0 4px #e5dccb;
            color: #1a1c23;
            position: relative;
            transition: transform 0.18s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.18s ease;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: stretch;
            padding: 6px 7px;
            border: 2px solid #20222b;
        }}

        .balatro-card::before {{
            content: "";
            position: absolute;
            inset: 5px;
            border-radius: 5px;
            border: 1px solid rgba(0, 0, 0, 0.07);
            pointer-events: none;
        }}

        /* Balanceo oscilante continuo de Balatro */
        @keyframes balatro-sway-1 {{
            0%, 100% {{ transform: translateY(0px) rotate(-1.8deg); }}
            50% {{ transform: translateY(-7px) rotate(1.4deg); }}
        }}
        @keyframes balatro-sway-2 {{
            0%, 100% {{ transform: translateY(-4px) rotate(1.6deg); }}
            50% {{ transform: translateY(3px) rotate(-1.7deg); }}
        }}
        @keyframes balatro-sway-3 {{
            0%, 100% {{ transform: translateY(2px) rotate(-1deg); }}
            50% {{ transform: translateY(-6px) rotate(1.8deg); }}
        }}

        .idle-sway-1 {{ animation: balatro-sway-1 3.4s ease-in-out infinite; }}
        .idle-sway-2 {{ animation: balatro-sway-2 3.9s ease-in-out infinite; }}
        .idle-sway-3 {{ animation: balatro-sway-3 4.2s ease-in-out infinite; }}

        .balatro-card:hover {{
            transform: translateY(-16px) scale(1.05) rotate(0deg) !important;
            animation-play-state: paused;
            box-shadow: 
                0 6px 0 #1b1e26,
                0 16px 26px rgba(0,0,0,0.7),
                inset 0 0 0 2px #ffffff,
                0 0 16px rgba(245,211,66,0.6);
            z-index: 25;
        }}

        .balatro-card.selected {{
            transform: translateY(-24px) scale(1.07) rotate(0deg) !important;
            animation-play-state: paused;
            border-color: #f5d342;
            box-shadow: 
                0 6px 0 #b38b14,
                0 18px 28px rgba(0,0,0,0.8), 
                0 0 0 3px #f5d342, 
                0 0 22px rgba(245,211,66,0.85),
                inset 0 0 0 2px #ffffff !important;
            z-index: 30;
        }}

        /* Esquinas de naipes Balatro */
        .card-corner {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            line-height: 1;
            width: 18px;
            user-select: none;
        }}
        .card-corner.top-left {{
            align-self: flex-start;
        }}
        .card-corner.bottom-right {{
            align-self: flex-end;
            transform: rotate(180deg);
        }}

        .corner-rank {{
            font-size: 0.75rem;
            font-weight: 900;
            line-height: 1;
        }}
        .corner-suit {{
            font-size: 0.65rem;
            line-height: 1;
            margin-top: 1px;
        }}

        /* Contenedor central del término algebraico */
        .card-center-term {{
            flex-grow: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 2px;
            color: #171920;
        }}

        .term-value {{
            font-family: 'BalatroFont', monospace;
            font-weight: bold;
            line-height: 1.1;
            text-shadow: 0 1px 1px rgba(0,0,0,0.12);
        }}

        .card-suit-red {{
            color: #d83a3a;
        }}
        .card-suit-blue {{
            color: #1e5ba3;
        }}

        @media (max-width: 640px) {{
            .balatro-card {{ width: 84px !important; height: 122px !important; padding: 4px 5px !important; }}
            .corner-rank {{ font-size: 0.62rem !important; }}
            .corner-suit {{ font-size: 0.55rem !important; }}
            #hand-container {{ min-height: 220px !important; }}
        }}

        /* Botón Jugar Mano en estado deshabilitado más nítido */
        .btn-play-disabled {{
            background: rgba(18, 20, 26, 0.85) !important;
            color: #6b7280 !important;
            border: 2px solid rgba(255, 255, 255, 0.15) !important;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4) !important;
            cursor: not-allowed !important;
        }}

        /* Efectos de Fuego y Puntaje */
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
    <!-- CONTENEDOR DE FONDO (VIDEO LOCAL O FALLBACK PROCEDURAL) -->
    <div id="bg-video-container">
        {f'<video id="bg-media" class="bg-media bg-round-1" autoplay muted loop playsinline><source src="data:{video_mime};base64,{video_b64}" type="{video_mime}"></video>' if video_b64 else '<div id="bg-media" class="bg-media fallback-swirl bg-round-1 w-full h-full"></div>'}
    </div>
    <div class="bg-tint-overlay"></div>

    <canvas id="fx-canvas"></canvas>

    <!-- INTRO MODAL (User Nickname) -->
    <div id="intro-modal" class="fixed inset-0 bg-black/95 z-[1000] flex items-center justify-center p-4 backdrop-blur-md">
        <div class="bg-[#151821] border-4 border-emerald-500 rounded-2xl max-w-sm w-full p-6 text-center shadow-[0_0_50px_rgba(16,185,129,0.4)]">
            <h1 class="font-balatro text-3xl sm:text-4xl text-emerald-400 mb-2 animate-pulse" style="text-shadow: 0 0 20px #10b981;">FACTOR<br>COMÚN</h1>
            <p class="font-balatro text-[10px] text-gray-300 mb-6 mt-4">INGRESA TU USUARIO</p>
            <input type="text" id="username-input" class="w-full bg-black border-2 border-white/20 text-white font-balatro p-3 rounded mb-6 text-center focus:border-yellow-400 outline-none uppercase" placeholder="TU NOMBRE" maxlength="12">
            <button onclick="startGameFromIntro()" class="w-full bg-emerald-500 hover:bg-emerald-400 text-black font-balatro py-4 rounded-xl text-sm transition-transform active:scale-95 shadow-[0_0_20px_rgba(16,185,129,0.5)]">
                ENTRAR AL JUEGO
            </button>
        </div>
    </div>

    <!-- BOTONES INFERIORES FIJOS (MÓVIL / ESCRITORIO) -->
    <div class="fixed bottom-3 left-3 z-40">
        <button onclick="toggleTutorial()" class="bg-purple-900/90 border-2 border-purple-400 text-white font-balatro text-xs p-3 rounded-xl shadow-[0_0_15px_rgba(168,85,247,0.5)] hover:scale-105 transition-transform">
            💡 TUTO
        </button>
    </div>
    <div class="fixed bottom-3 right-3 z-40">
        <button onclick="toggleLeaderboard()" class="bg-blue-900/90 border-2 border-blue-400 text-white font-balatro text-xs p-3 rounded-xl shadow-[0_0_15px_rgba(59,130,246,0.5)] hover:scale-105 transition-transform">
            🏆 RANK
        </button>
    </div>

    <!-- TUTORIAL LATERAL CON EMOJIS -->
    <div id="tutorial-panel" class="fixed left-0 top-0 h-full w-64 sm:w-72 bg-black/95 border-r-2 border-purple-500/50 p-4 flex flex-col z-50 transform -translate-x-full transition-transform duration-300 shadow-2xl">
        <div class="flex justify-between items-center mb-6 border-b border-purple-500/30 pb-2 mt-2">
            <h3 class="font-balatro text-[12px] text-purple-400">💡 ¿CÓMO JUGAR?</h3>
            <button onclick="toggleTutorial()" class="text-white text-xl">✕</button>
        </div>
        <div class="text-2xl bg-black/50 p-3 rounded-xl border border-gray-700 mb-4 text-center">
            🍎🍉 <span class="text-pink-500">+</span> 🍎🍌
        </div>
        <p class="text-[11px] text-gray-300 font-balatro text-center mb-4 leading-relaxed">SACA LO QUE<br>TIENEN EN COMÚN (🍎)</p>
        <div class="text-3xl bg-purple-900/30 p-3 rounded-xl border border-purple-500 text-center mb-6">
            🍎<span class="text-gray-400 text-xl">(</span>🍉 <span class="text-pink-500 text-xl">+</span> 🍌<span class="text-gray-400 text-xl">)</span>
        </div>
        <p class="text-[10px] text-gray-400 font-balatro text-center leading-relaxed">
            1. Selecciona las cartas que comparten factores numéricos o letras.<br><br>
            2. Presiona "JUGAR MANO".<br><br>
            3. Haz el mayor combo posible.
        </p>
    </div>

    <!-- PANEL LATERAL DESPLEGABLE DE RANKING (25 JUGADORES) -->
    <aside id="leaderboard-panel" class="fixed right-0 top-0 h-full w-64 sm:w-72 bg-black/95 border-l-2 border-blue-500/50 p-3 flex flex-col z-50 transform translate-x-full transition-transform duration-300 shadow-2xl">
        <div class="flex justify-between items-center mb-2 border-b border-blue-500/30 pb-2 mt-2">
            <button onclick="toggleLeaderboard()" class="text-white text-xl">✕</button>
            <div class="text-right">
                <h3 class="font-balatro text-[10px] text-yellow-400">🏆 RANKING EN VIVO</h3>
                <span id="sync-status" class="text-[8px] font-balatro text-emerald-400">● 25 JUGADORES</span>
            </div>
        </div>
        <div class="text-[9px] text-gray-400 font-balatro mb-2 text-center">AULA COMPITIENDO EN TIEMPO REAL</div>
        <div id="leaderboard" class="flex-grow overflow-y-auto lb-scroll flex flex-col gap-1 pr-1">
            <!-- Inyectado por JS -->
        </div>
    </aside>

    <!-- HEADER SUPERIOR: NIVEL, COMODINES Y PUNTAJE -->
    <header class="flex justify-between items-center z-10 max-w-5xl mx-auto w-full gap-2 px-1">
        <!-- Nivel & Ronda -->
        <div class="bg-black/75 border-2 border-emerald-500/60 rounded-xl px-3 py-2 text-center min-w-[85px] sm:min-w-[110px]">
            <div class="text-[9px] sm:text-[11px] text-gray-400 uppercase font-balatro">NIVEL <span id="level-display" class="text-emerald-400 text-sm sm:text-lg">1</span></div>
            <div class="text-[8px] sm:text-[10px] text-gray-400 mt-0.5 font-balatro">RONDA <span id="round-display" class="text-white">1</span>/3</div>
        </div>

        <!-- 3 Comodines Balatro -->
        <div class="flex justify-center gap-1.5 sm:gap-3">
            <button id="btn-joker-reveal" onclick="useJoker('reveal')" title="Revelar factor predominante" class="bg-blue-900 border-2 border-blue-400 rounded-xl p-2 sm:p-2.5 text-lg sm:text-2xl relative shadow-[0_0_12px_rgba(59,130,246,0.5)] active:scale-95 transition-transform">
                👁️
                <span id="qty-reveal" class="absolute -top-1.5 -right-1.5 bg-red-600 text-white text-[9px] font-balatro px-1 rounded-full border border-black">1</span>
            </button>
            <button id="btn-joker-reroll" onclick="useJoker('reroll')" title="Cambiar mano actual" class="bg-purple-900 border-2 border-purple-400 rounded-xl p-2 sm:p-2.5 text-lg sm:text-2xl relative shadow-[0_0_12px_rgba(168,85,247,0.5)] active:scale-95 transition-transform">
                🎲
                <span id="qty-reroll" class="absolute -top-1.5 -right-1.5 bg-red-600 text-white text-[9px] font-balatro px-1 rounded-full border border-black">1</span>
            </button>
            <button id="btn-joker-skip" onclick="useJoker('skip')" title="Saltar nivel (gana con 3 estrellas)" class="bg-yellow-700 border-2 border-yellow-400 rounded-xl p-2 sm:p-2.5 text-lg sm:text-2xl relative shadow-[0_0_12px_rgba(234,179,8,0.5)] active:scale-95 transition-transform opacity-40">
                ⏭️
                <span id="qty-skip" class="absolute -top-1.5 -right-1.5 bg-red-600 text-white text-[9px] font-balatro px-1 rounded-full border border-black">0</span>
            </button>
        </div>

        <!-- Puntaje Global y Rango -->
        <div class="bg-black/75 border-2 border-red-500/60 rounded-xl px-3 py-2 text-center min-w-[85px] sm:min-w-[110px]">
            <div class="text-[9px] sm:text-[11px] text-gray-400 uppercase font-balatro">PUNTOS</div>
            <div id="total-score" class="text-base sm:text-xl text-emerald-400 font-balatro mt-0.5">0</div>
            <div class="text-[8px] text-gray-300 font-balatro opacity-75">Rank: <span id="player-rank">#25</span></div>
        </div>
    </header>

    <!-- ZONA CENTRAL DE JUEGO -->
    <main class="flex-grow flex flex-col items-center justify-center relative w-full max-w-5xl mx-auto my-auto">
        <!-- Contenedor de cartas -->
        <div id="hand-container" class="flex justify-center items-center flex-wrap gap-2 sm:gap-3.5 w-full px-2 mb-6">
            <!-- Renderizado dinámico -->
        </div>

        <!-- Botón Jugar Mano -->
        <button id="btn-play" onclick="playHand()" disabled class="btn-play-disabled px-8 py-3.5 sm:px-12 sm:py-4 rounded-xl font-balatro text-xs sm:text-sm shadow-2xl transition-all">
            JUGAR MANO
        </button>

        <!-- Efecto Fuego Puntos Flotantes -->
        <div id="flame-score-container" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 hidden opacity-0 transition-opacity duration-300 z-40 pointer-events-none text-center">
            <div id="flame-score" class="font-balatro text-4xl sm:text-6xl score-flame tracking-wider drop-shadow-[0_0_35px_#ff4500]">0</div>
        </div>
    </main>

    <!-- MODAL NIVEL COMPLETADO (ESTRELLAS Y PRECISIÓN) -->
    <div id="level-modal" class="fixed inset-0 bg-black/90 z-50 hidden flex items-center justify-center backdrop-blur-md p-4">
        <div class="bg-[#151821] border-4 border-yellow-400 rounded-2xl max-w-md w-full p-6 text-center shadow-[0_0_50px_rgba(245,211,66,0.3)]">
            <h2 class="font-balatro text-xl sm:text-2xl text-yellow-300 mb-2">NIVEL COMPLETADO</h2>
            <div class="flex justify-center gap-3 my-5" id="modal-stars"></div>
            <p id="modal-desc" class="text-gray-300 text-[11px] sm:text-xs font-balatro leading-relaxed mb-6"></p>
            <button onclick="nextLevel()" class="w-full bg-[#f5d342] hover:bg-[#e5c332] text-black font-balatro py-4 rounded-xl text-xs transition-transform active:scale-95 shadow-lg">
                SIGUIENTE NIVEL ➔
            </button>
        </div>
    </div>

    <!-- ALERTA DE COMODÍN -->
    <div id="alert-modal" class="fixed top-12 left-1/2 -translate-x-1/2 bg-blue-600 border-2 border-white text-white font-balatro text-[11px] sm:text-xs px-5 py-3 rounded-xl shadow-2xl z-50 hidden transition-opacity text-center max-w-[90vw]">
        <span id="alert-text"></span>
    </div>

    <script>
        /* SÍNTESIS DE AUDIO PROCEDURAL (Web Audio API) */
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

        /* CLASIFICACIÓN DE ALUMNOS (25 PARTICIPANTES) */
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
                    p.score += Math.floor(Math.random() * 320 * Math.max(1, p.level));
                    if(p.score > 2200 * p.level) p.level++;
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
                div.className = `flex justify-between items-center text-[9px] font-balatro p-1.5 rounded ${{p.isPlayer ? 'bg-blue-600/70 border border-cyan-400 font-bold' : 'bg-white/5 text-gray-300'}}`;
                div.innerHTML = `
                    <span class="truncate max-w-[130px]">${{medal}} ${{p.name}} ${{p.isPlayer ? '(TÚ)' : ''}}</span>
                    <span class="text-yellow-300">${{p.score.toLocaleString()}}</span>
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

        function updateBackgroundForRound() {{
            const media = document.getElementById('bg-media');
            if(!media) return;
            media.classList.remove('bg-round-1', 'bg-round-2', 'bg-round-3');
            if(round === 1) media.classList.add('bg-round-1');
            else if(round === 2) media.classList.add('bg-round-2');
            else if(round === 3) media.classList.add('bg-round-3');
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
                for(let j=0; j<n; j++) {{
                    if((i & (1<<j))) subset.push(currentHand[j]);
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
                el.className = `balatro-card ${{card.selected ? 'selected' : swayClass}}`;
                
                // Tamaño dinámico del término con BalatroFont
                let tSize = 'text-2xl sm:text-3xl';
                if(card.str.length >= 4) tSize = 'text-xl sm:text-2xl';
                if(card.str.length >= 7) tSize = 'text-lg sm:text-xl';
                if(card.str.length >= 10) tSize = 'text-base sm:text-lg';

                // Palo y color estilo Balatro (Corazones rojos / Picas azules)
                const isRed = (card.c < 0 || (idx % 2 === 0));
                const suit = isRed ? '♥' : '♠';
                const suitClass = isRed ? 'card-suit-red' : 'card-suit-blue';

                // Rango de la esquina: si tiene potencia x², x o el número simplificado
                let cornerRank = '';
                if(card.x > 0 && card.y > 0) cornerRank = 'XY';
                else if(card.x > 1) cornerRank = `X²`;
                else if(card.x === 1) cornerRank = 'X';
                else if(card.y > 0) cornerRank = 'Y';
                else cornerRank = Math.abs(card.c).toString();

                el.innerHTML = `
                    <div class="card-corner top-left ${{suitClass}} font-balatro">
                        <span class="corner-rank">${{cornerRank}}</span>
                        <span class="corner-suit">${{suit}}</span>
                    </div>
                    <div class="card-center-term">
                        <span class="term-value ${{tSize}}">
                            ${{card.str}}
                        </span>
                    </div>
                    <div class="card-corner bottom-right ${{suitClass}} font-balatro">
                        <span class="corner-rank">${{cornerRank}}</span>
                        <span class="corner-suit">${{suit}}</span>
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
                btnPlay.className = "bg-[#2d82d7] hover:bg-[#1a5fa6] text-white border-2 border-cyan-300 px-8 py-3.5 sm:px-12 sm:py-4 rounded-xl font-balatro text-xs sm:text-sm shadow-[0_0_20px_rgba(45,130,215,0.6)] transition-all transform active:scale-95 cursor-pointer";
            }} else {{
                btnPlay.disabled = true;
                btnPlay.className = "btn-play-disabled px-8 py-3.5 sm:px-12 sm:py-4 rounded-xl font-balatro text-xs sm:text-sm shadow-2xl transition-all";
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
                    starContainer.innerHTML += `<span class="text-yellow-400 text-4xl sm:text-5xl drop-shadow-[0_0_15px_rgba(245,211,66,0.8)] animate-pulse">★</span>`;
                }} else {{
                    starContainer.innerHTML += `<span class="text-gray-700 text-4xl sm:text-5xl">★</span>`;
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
                    showAlert(`🔎 FACTOR DOMINANTE:<br><br><span class="text-yellow-300 text-base sm:text-lg">${{bestFactor}}</span> (en ${{maxSubset}} cartas)`);
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
components.html(GAME_HTML, height=730, scrolling=False)

# Barra lateral informativa para la presentación
with st.sidebar:
    st.header("🧮 Balatro: Factor Común")
    st.caption("UCR • IF0003 Matemática Básica")
    st.markdown(
        """
        **Mecánica Didáctica:**
        - **3 Rondas por Nivel:** La dificultad de los términos algebraicos escala conforme aumentas de nivel.
        - **Factor Común Monomio:** Seleccionar los términos que comparten letras y divisores numéricos comunes (MCD).
        - **Reutilización:** Las cartas no seleccionadas se conservan en la siguiente ronda.
        - **Comodines:**
          - 👁️ *Lupa:* Revela el factor común dominante.
          - 🎲 *Dado:* Reroll completo de la mano actual.
          - ⏭️ *Salto:* Se desbloquea con 3 estrellas (precisión perfecta).
        """
    )
