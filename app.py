"""
Balatro: Factor Común - Edición Dark Fantasy 8-Bit
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
        margin: 0 !important;
        max-width: 100% !important;
    }
    .stApp {
        background-color: #050608;
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

# Fondos GIF por estado
bg_game_b64 = get_base64_file("background_gif.gif") or get_base64_file("background.gif")
bg_reg_b64 = get_base64_file("background_gif_2.gif") or get_base64_file("background_2.gif") or bg_game_b64

# Audio de fondo
audio_bg_b64 = get_base64_file("background.mp3")

# Imágenes de selección de personajes
ricky_b64 = get_base64_file("ricky.png")
ariana_b64 = get_base64_file("ariana.png")

# Tipografías
balatro_font_b64 = get_base64_file("balatro.otf")
dos_font_b64 = (
    get_base64_file("Perfect DOS VGA 437 Win.ttf") or 
    get_base64_file("Perfect DOS VGA 437.ttf") or
    get_base64_file("perfect_dos_vga_437.ttf")
)

font_face_css = ""
if dos_font_b64:
    font_face_css += f"""
    @font-face {{
        font-family: 'DosVgaFont';
        src: url(data:font/ttf;base64,{dos_font_b64}) format('truetype');
        font-weight: normal;
        font-style: normal;
    }}
    """
else:
    font_face_css += """
    @font-face {
        font-family: 'DosVgaFont';
        src: local('Press Start 2P'), local('Courier New'), monospace;
        font-weight: bold;
    }
    """

if balatro_font_b64:
    font_face_css += f"""
    @font-face {{
        font-family: 'BalatroFont';
        src: url(data:font/otf;base64,{balatro_font_b64}) format('opentype');
    }}
    """
else:
    font_face_css += """
    @font-face {
        font-family: 'BalatroFont';
        src: local('Press Start 2P'), sans-serif;
        font-weight: bold;
    }
    """

bg_game_tag = f'<img id="bg-game" class="screen-bg hidden" src="data:image/gif;base64,{bg_game_b64}" alt="Game BG" />' if bg_game_b64 else '<div id="bg-game" class="screen-bg hidden procedural-game"></div>'
bg_reg_tag = f'<img id="bg-reg" class="screen-bg" src="data:image/gif;base64,{bg_reg_b64}" alt="Register BG" />' if bg_reg_b64 else '<div id="bg-reg" class="screen-bg procedural-reg"></div>'

audio_html_tag = ""
if audio_bg_b64:
    audio_html_tag = f"""
    <audio id="bg-music" loop preload="auto">
        <source src="data:audio/mp3;base64,{audio_bg_b64}" type="audio/mp3">
    </audio>
    """

ricky_img_tag = f'<img src="data:image/png;base64,{ricky_b64}" class="w-full h-full object-contain pixelated" alt="Ricky" />' if ricky_b64 else '<div class="text-3xl font-dos">CHICO</div>'
ariana_img_tag = f'<img src="data:image/png;base64,{ariana_b64}" class="w-full h-full object-contain pixelated" alt="Ariana" />' if ariana_b64 else '<div class="text-3xl font-dos">CHICA</div>'

GAME_HTML = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Balatro: Factor Común 8-Bit</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    
    <style>
        {font_face_css}

        :root {{
            --font-dos: 'DosVgaFont', 'Press Start 2P', monospace;
            --font-balatro: 'BalatroFont', 'Press Start 2P', sans-serif;
            --color-dark-iron: #0b0d12;
            --color-border-dark: #191e28;
            --color-blood-red: #9e1a22;
            --color-card-cream: #ece5d3;
        }}

        * {{
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
            image-rendering: pixelated;
        }}

        .pixelated {{
            image-rendering: pixelated;
            image-rendering: crisp-edges;
        }}

        body {{
            color: #f0e6d2;
            font-family: var(--font-balatro);
            overflow: hidden;
            user-select: none;
            margin: 0;
            height: 100vh;
            width: 100vw;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background-color: #050608;
        }}

        .font-dos {{ font-family: var(--font-dos); }}
        .font-balatro {{ font-family: var(--font-balatro); }}

        /* FONDOS */
        .screen-bg {{
            position: fixed;
            top: 50%; left: 50%;
            min-width: 100%; min-height: 100%;
            width: auto; height: auto;
            transform: translate(-50%, -50%) scale(1.05);
            z-index: -3;
            object-fit: cover;
            pointer-events: none;
            image-rendering: pixelated;
        }}

        .procedural-reg {{
            background: radial-gradient(circle at center, #181d26, #07090d);
        }}
        .procedural-game {{
            background: radial-gradient(circle at center, #1b3d2b, #050c07);
        }}

        .bg-dark-overlay {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: radial-gradient(circle at center, rgba(10, 14, 18, 0.45) 0%, rgba(3, 4, 6, 0.92) 100%);
            pointer-events: none;
            z-index: -2;
        }}

        /* CAJAS Y PANELES 8-BIT AUTÉNTICOS (SIN BORDES REDONDEADOS) */
        .pixel-box-8bit {{
            background: #1e2430;
            border: 4px solid #000000;
            box-shadow: 
                inset 3px 3px 0 #3a455a,
                inset -3px -3px 0 #0d1017,
                0 6px 0 #000000;
            position: relative;
        }}

        .pixel-inner-slot {{
            background: #0d1017;
            border: 3px solid #000000;
            box-shadow: inset 2px 2px 0 #000000;
        }}

        .pixel-badge-red {{
            background: #8f1920;
            border: 3px solid #000000;
            box-shadow: 
                inset 2px 2px 0 #c7363e,
                inset -2px -2px 0 #4f0a0e,
                0 4px 0 #000000;
            color: #ffffff;
            text-shadow: 2px 2px 0 #000000;
        }}

        .pixel-btn-action {{
            font-family: var(--font-dos);
            background: #d85a1a;
            border: 4px solid #000000;
            box-shadow: 
                inset 3px 3px 0 #ff884d,
                inset -3px -3px 0 #7a2b05,
                0 6px 0 #000000;
            color: #ffffff;
            text-shadow: 2px 2px 0 #000000;
            transition: transform 0.05s steps(2);
        }}
        .pixel-btn-action:hover {{ background: #ea6927; }}
        .pixel-btn-action:active {{
            transform: translateY(4px);
            box-shadow: 
                inset 3px 3px 0 #7a2b05,
                inset -3px -3px 0 #ff884d,
                0 2px 0 #000000;
        }}

        .pixel-btn-blue {{
            font-family: var(--font-dos);
            background: #1b629b;
            border: 3px solid #000000;
            box-shadow: 
                inset 2px 2px 0 #4593d6,
                inset -2px -2px 0 #0a3152,
                0 4px 0 #000000;
            color: #ffffff;
            text-shadow: 2px 2px 0 #000000;
        }}

        /* SELECCIÓN DE PERSONAJE POKÉMON 8-BIT */
        .char-slot-8bit {{
            background: #12161f;
            border: 3px solid #000000;
            box-shadow: inset 2px 2px 0 #283142;
            cursor: pointer;
            transition: transform 0.08s steps(2);
        }}
        .char-slot-8bit:hover {{
            border-color: #f1b31c;
            background: #1a202c;
            transform: translateY(-2px);
        }}
        .char-slot-8bit.selected {{
            border-color: #f1b31c;
            background: #232b3b;
            box-shadow: inset 0 0 0 2px #f1b31c, 0 4px 0 #000000;
        }}

        /* ========================================================
           CARTAS 8-BIT / DARK FANTASY (BORDE PIXELADO REAL)
           ======================================================== */
        .card-8bit {{
            width: 104px;
            height: 150px;
            background: var(--color-card-cream);
            border: 4px solid #000000;
            /* Bisel duro de pixel art */
            box-shadow: 
                inset 3px 3px 0 #ffffff,
                inset -3px -3px 0 #b3a992,
                0 7px 0 #000000;
            position: relative;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.08s steps(3);
        }}

        /* Marco interior rústico punteado */
        .card-frame-inner {{
            position: absolute;
            top: 4px; left: 4px; right: 4px; bottom: 4px;
            border: 2px solid #ccc0a2;
            pointer-events: none;
        }}

        /* Esquinas */
        .pip-corner-tl {{
            position: absolute;
            top: 6px; left: 7px;
            display: flex; flex-direction: column; align-items: center;
            line-height: 1;
            pointer-events: none;
            font-family: var(--font-dos);
        }}
        .pip-corner-br {{
            position: absolute;
            bottom: 6px; right: 7px;
            display: flex; flex-direction: column; align-items: center;
            line-height: 1;
            transform: rotate(180deg);
            pointer-events: none;
            font-family: var(--font-dos);
        }}

        .corner-text {{
            font-size: 13px;
            font-weight: bold;
            letter-spacing: -0.5px;
        }}
        .corner-suit-icon {{
            font-size: 11px;
            margin-top: 1px;
        }}

        /* Contenedor central del monomio */
        .term-box-center {{
            max-width: 86%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            z-index: 2;
            pointer-events: none;
        }}

        .term-math-pixel {{
            font-family: var(--font-dos);
            color: #12141a;
            line-height: 1;
            white-space: nowrap;
            letter-spacing: -1px;
            font-weight: bold;
            text-shadow: 1px 1px 0 #ffffff;
        }}

        .len-1 {{ font-size: 2.1rem; }}
        .len-2 {{ font-size: 1.85rem; }}
        .len-3 {{ font-size: 1.55rem; }}
        .len-4 {{ font-size: 1.3rem; }}
        .len-5 {{ font-size: 1.1rem; }}
        .len-many {{ font-size: 0.9rem; }}

        /* Oscilación escalonada en píxeles */
        @keyframes sway-8bit-1 {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-7px); }}
        }}
        @keyframes sway-8bit-2 {{
            0%, 100% {{ transform: translateY(-5px); }}
            50% {{ transform: translateY(3px); }}
        }}
        @keyframes sway-8bit-3 {{
            0%, 100% {{ transform: translateY(2px); }}
            50% {{ transform: translateY(-6px); }}
        }}

        .idle-sway-1 {{ animation: sway-8bit-1 3s steps(5) infinite; }}
        .idle-sway-2 {{ animation: sway-8bit-2 3.6s steps(5) infinite; }}
        .idle-sway-3 {{ animation: sway-8bit-3 4s steps(5) infinite; }}

        .card-8bit:hover {{
            transform: translateY(-16px) !important;
            animation-play-state: paused;
            box-shadow: 
                inset 3px 3px 0 #ffffff,
                inset -3px -3px 0 #b3a992,
                0 14px 0 #000000;
            z-index: 20;
        }}
        .card-8bit.selected {{
            transform: translateY(-26px) !important;
            animation-play-state: paused;
            border-color: #f1b31c;
            box-shadow: 
                inset 3px 3px 0 #fff7b8,
                inset -3px -3px 0 #ab7c07,
                0 0 0 3px #f1b31c,
                0 14px 0 #000000 !important;
            z-index: 30;
        }}

        @media (max-width: 640px) {{
            .card-8bit {{ width: 84px !important; height: 122px !important; }}
            .len-1 {{ font-size: 1.55rem !important; }}
            .len-2 {{ font-size: 1.35rem !important; }}
            .len-3 {{ font-size: 1.15rem !important; }}
            .len-4 {{ font-size: 0.95rem !important; }}
            .len-5 {{ font-size: 0.82rem !important; }}
            .len-many {{ font-size: 0.72rem !important; }}
            .corner-text {{ font-size: 11px !important; }}
            .corner-suit-icon {{ font-size: 9px !important; }}
            #hand-container {{ min-height: 200px !important; }}
        }}

        @keyframes flame-flicker-8bit {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.12); }}
        }}
        .score-flame {{
            color: #ffffff;
            font-family: var(--font-dos);
            text-shadow: 3px 3px 0 #9e1a22, -3px -3px 0 #d85a1a;
            animation: flame-flicker-8bit 0.25s steps(2) infinite;
        }}

        @keyframes shake-8bit {{
            0%, 100% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-8px); }}
            75% {{ transform: translateX(8px); }}
        }}
        .animate-shake {{ animation: shake-8bit 0.22s steps(4); }}

        #fx-canvas {{ position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 50; }}
    </style>
</head>
<body class="p-2 sm:p-4">
    {bg_reg_tag}
    {bg_game_tag}
    {audio_html_tag}
    <div class="bg-dark-overlay"></div>
    <canvas id="fx-canvas"></canvas>

    <!-- INTRO MODAL DARK FANTASY 8-BIT -->
    <div id="intro-modal" class="fixed inset-0 bg-black/85 z-[1000] flex items-center justify-center p-4">
        <div class="pixel-box-8bit max-w-sm w-full p-6 text-center">
            
            <div class="pixel-badge-red py-3 px-4 mb-5 transform -rotate-1 inline-block w-full">
                <h1 class="text-xl sm:text-2xl tracking-wide font-balatro">FACTOR COMÚN</h1>
                <p class="text-[10px] opacity-90 tracking-widest mt-1 font-dos">DARK FANTASY • UCR</p>
            </div>
            
            <!-- PASO 1: NOMBRE -->
            <div id="step-name">
                <div class="pixel-inner-slot p-4 mb-5 text-left">
                    <label class="block text-xs text-gray-400 mb-2 tracking-wider font-dos">APODO DEL JUGADOR:</label>
                    <input type="text" id="username-input" class="w-full bg-[#07090d] border-2 border-[#2b3547] text-white p-3 text-center uppercase tracking-wider text-base font-bold font-dos outline-none focus:border-[#f1b31c]" placeholder="TU NOMBRE" maxlength="12">
                </div>
                <button onclick="goToGenderStep()" class="pixel-btn-action w-full py-4 text-xs font-bold tracking-wider">
                    CONTINUAR ➔
                </button>
            </div>

            <!-- PASO 2: ELECCIÓN DE PERSONAJE POKÉMON -->
            <div id="step-gender" class="hidden">
                <div class="pixel-inner-slot p-3 mb-4 text-center">
                    <p class="text-xs text-yellow-300 font-dos mb-3">¿ERES CHICO O CHICA?</p>
                    <div class="grid grid-cols-2 gap-3">
                        <div id="opt-boy" onclick="selectGender('boy')" class="char-slot-8bit p-2 flex flex-col items-center">
                            <div class="w-20 h-20 sm:w-24 sm:h-24 flex items-center justify-center mb-1">
                                {ricky_img_tag}
                            </div>
                            <span class="text-xs font-bold text-gray-300 font-dos">CHICO</span>
                        </div>
                        <div id="opt-girl" onclick="selectGender('girl')" class="char-slot-8bit p-2 flex flex-col items-center">
                            <div class="w-20 h-20 sm:w-24 sm:h-24 flex items-center justify-center mb-1">
                                {ariana_img_tag}
                            </div>
                            <span class="text-xs font-bold text-gray-300 font-dos">CHICA</span>
                        </div>
                    </div>
                </div>
                <button id="btn-start-game" onclick="startGame()" disabled class="pixel-box-8bit bg-[#12161f] text-gray-500 w-full py-3.5 text-xs font-bold tracking-wider opacity-40 cursor-not-allowed">
                    ENTRAR AL JUEGO
                </button>
            </div>

        </div>
    </div>

    <!-- BOTONES INFERIORES -->
    <div class="fixed bottom-3 left-3 z-40">
        <button onclick="toggleTutorial()" class="pixel-btn-blue text-xs px-3.5 py-2">
            💡 TUTO
        </button>
    </div>
    <div class="fixed bottom-3 right-3 z-40">
        <!-- RANK DESHABILITADO -->
        <button onclick="showRankNotice()" class="pixel-box-8bit bg-[#131720] border-[#000] text-gray-400 text-xs px-3.5 py-2 cursor-pointer relative font-dos" title="Módulo en desarrollo por compañero">
            🏆 RANK
            <span class="absolute -top-2 -right-2 bg-yellow-500 text-black text-[8px] font-bold px-1 border border-black">DEV</span>
        </button>
    </div>

    <!-- PANEL TUTORIAL -->
    <div id="tutorial-panel" class="fixed left-0 top-0 h-full w-72 sm:w-80 bg-[#141720] border-r-4 border-black p-4 flex flex-col z-50 transform -translate-x-full transition-transform duration-200 shadow-2xl">
        <div class="flex justify-between items-center mb-4 border-b-2 border-white/10 pb-2">
            <div class="pixel-badge-red px-3 py-1 text-xs font-dos">CÓMO JUGAR</div>
            <button onclick="toggleTutorial()" class="text-white text-base font-bold">✕</button>
        </div>
        <div class="pixel-inner-slot p-3 text-2xl text-center mb-3">
            🍎🍉 <span class="text-red-400">+</span> 🍎🍌
        </div>
        <p class="text-xs text-yellow-300 text-center mb-3 font-dos">SACA LO QUE SE REPITE (🍎)</p>
        <div class="pixel-inner-slot p-3 text-2xl text-center mb-4">
            🍎<span class="text-gray-400">(</span>🍉 <span class="text-red-400">+</span> 🍌<span class="text-gray-400">)</span>
        </div>
        <div class="text-xs text-gray-300 leading-relaxed font-dos space-y-2">
            <p>1. Selecciona 2 o más cartas que compartan divisores o variables comunes.</p>
            <p>2. Presiona "JUGAR MANO" para acumular fichas multiplicadas.</p>
            <p>3. Las cartas no seleccionadas permanecen en tu mano para la siguiente ronda.</p>
        </div>
    </div>

    <!-- HEADER SUPERIOR -->
    <header class="flex justify-between items-center z-10 max-w-5xl mx-auto w-full gap-2 px-1">
        <div class="pixel-box-8bit px-3.5 py-2 text-center min-w-[95px] sm:min-w-[125px]">
            <div class="text-[10px] text-gray-400 font-dos">NIVEL <span id="level-display" class="text-yellow-400 text-sm font-dos">1</span></div>
            <div class="text-[9px] text-gray-300 mt-0.5 font-dos">RONDA <span id="round-display" class="text-white">1</span>/3</div>
        </div>

        <!-- 3 Comodines -->
        <div class="flex justify-center gap-1.5 sm:gap-2.5">
            <button id="btn-joker-reveal" onclick="useJoker('reveal')" title="Revelar factor" class="pixel-box-8bit p-2 text-base sm:text-xl relative active:translate-y-1">
                👁️
                <span id="qty-reveal" class="absolute -top-2 -right-2 bg-red-600 text-white text-[9px] px-1 border border-black font-dos">1</span>
            </button>
            <button id="btn-joker-reroll" onclick="useJoker('reroll')" title="Cambiar mano" class="pixel-box-8bit p-2 text-base sm:text-xl relative active:translate-y-1">
                🎲
                <span id="qty-reroll" class="absolute -top-2 -right-2 bg-red-600 text-white text-[9px] px-1 border border-black font-dos">1</span>
            </button>
            <!-- Comodín que salta 1 RONDA -->
            <button id="btn-joker-skip" onclick="useJoker('skip')" title="Saltar 1 Ronda" class="pixel-box-8bit p-2 text-base sm:text-xl relative active:translate-y-1 opacity-40">
                ⏭️
                <span id="qty-skip" class="absolute -top-2 -right-2 bg-yellow-500 text-black text-[9px] px-1 border border-black font-dos">0</span>
            </button>
        </div>

        <div class="pixel-box-8bit px-3.5 py-2 text-center min-w-[95px] sm:min-w-[125px]">
            <div class="text-[10px] text-gray-400 font-dos">PUNTOS</div>
            <div id="total-score" class="text-sm sm:text-lg text-yellow-400 mt-0.5 font-dos font-bold">0</div>
            <div id="user-display-tag" class="text-[9px] text-gray-400 truncate max-w-[85px] mx-auto font-dos">JUGADOR</div>
        </div>
    </header>

    <!-- ÁREA DE CARTAS 8-BIT -->
    <main class="flex-grow flex flex-col items-center justify-center relative w-full max-w-5xl mx-auto my-auto">
        <div id="hand-container" class="flex justify-center items-center flex-wrap gap-2.5 sm:gap-4 w-full px-2 mb-6"></div>

        <button id="btn-play" onclick="playHand()" disabled class="pixel-box-8bit bg-[#131720] text-gray-600 px-8 py-3.5 sm:px-12 sm:py-4 text-xs sm:text-sm tracking-widest opacity-40 cursor-not-allowed font-dos">
            JUGAR MANO
        </button>

        <div id="flame-score-container" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 hidden opacity-0 transition-opacity duration-200 z-40 pointer-events-none text-center">
            <div id="flame-score" class="text-3xl sm:text-5xl score-flame tracking-wider">0</div>
        </div>
    </main>

    <!-- MODAL FIN DE NIVEL -->
    <div id="level-modal" class="fixed inset-0 bg-black/85 z-50 hidden flex items-center justify-center p-4">
        <div class="pixel-box-8bit max-w-sm w-full p-6 text-center">
            <div class="pixel-badge-red py-2 px-4 mb-4 transform -rotate-1 inline-block w-full">
                <h2 class="text-lg sm:text-xl font-balatro">NIVEL COMPLETADO</h2>
            </div>
            <div class="flex justify-center gap-3 my-4" id="modal-stars"></div>
            <p id="modal-desc" class="pixel-inner-slot p-3 text-gray-200 text-xs leading-relaxed mb-5 font-dos"></p>
            <button onclick="nextLevel()" class="pixel-btn-action w-full py-3.5 text-xs tracking-wider">
                SIGUIENTE NIVEL ➔
            </button>
        </div>
    </div>

    <!-- ALERTA BALATRO -->
    <div id="alert-modal" class="fixed top-12 left-1/2 -translate-x-1/2 pixel-badge-red text-xs px-5 py-3 z-50 hidden text-center max-w-[90vw] font-dos">
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

        function startBackgroundMusic() {{
            const bgm = document.getElementById('bg-music');
            if (bgm) {{
                bgm.volume = 0.45;
                bgm.play().catch(() => {{}});
            }}
        }}

        const cvs = document.getElementById('fx-canvas'); const ctx = cvs.getContext('2d');
        let particles = [];
        window.onresize = () => {{ cvs.width = window.innerWidth; cvs.height = window.innerHeight; }};
        window.onresize();
        function spawnParticles(x, y, count=35) {{
            const colors = ['#f1b31c', '#1b629b', '#9e1a22', '#ffffff'];
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

        let playerName = "JUGADOR";
        let playerGender = null;

        function goToGenderStep() {{
            const input = document.getElementById('username-input').value.trim();
            if(input) playerName = input.toUpperCase();
            document.getElementById('step-name').classList.add('hidden');
            document.getElementById('step-gender').classList.remove('hidden');
            SFX.select();
        }}

        function selectGender(gender) {{
            playerGender = gender;
            document.getElementById('opt-boy').classList.remove('selected');
            document.getElementById('opt-girl').classList.remove('selected');
            
            if(gender === 'boy') {{
                document.getElementById('opt-boy').classList.add('selected');
            }} else {{
                document.getElementById('opt-girl').classList.add('selected');
            }}

            const btn = document.getElementById('btn-start-game');
            btn.disabled = false;
            btn.className = "pixel-btn-action w-full py-3.5 text-xs font-bold tracking-wider cursor-pointer";
            SFX.select();
        }}

        function startGame() {{
            if (!playerGender) return;
            document.getElementById('intro-modal').classList.add('hidden');
            document.getElementById('user-display-tag').textContent = `${{playerGender === 'boy' ? '👦' : '👧'}} ${{playerName}}`;
            
            // Cambiar fondo de registro a fondo de juego
            const bgReg = document.getElementById('bg-reg');
            const bgGame = document.getElementById('bg-game');
            if (bgReg) bgReg.classList.add('hidden');
            if (bgGame) bgGame.classList.remove('hidden');

            SFX.winRound();
            startBackgroundMusic();
            startRound();
            updateUI();
        }}

        function showRankNotice() {{
            SFX.hover();
            showAlert("🏆 Módulo de Ranking en desarrollo.");
        }}

        function toggleTutorial() {{
            SFX.hover();
            document.getElementById('tutorial-panel').classList.toggle('-translate-x-full');
        }}

        let level = 1;
        let round = 1;
        let score = 0;
        let hand = [];
        let nextCardId = 0;
        let levelStats = {{ optimalPossible: 0, actualCorrect: 0, errors: 0 }};
        let comodines = {{ reveal: 1, reroll: 1, skip: 1 }};

        const handContainer = document.getElementById('hand-container');
        const btnPlay = document.getElementById('btn-play');

        function gcd(a, b) {{ a=Math.abs(a); b=Math.abs(b); return b === 0 ? a : gcd(b, a % b); }}

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
            const suitColor = (suit === '♥' || suit === '♦') ? '#9e1a22' : '#1b629b';

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
                el.className = `card-8bit ${{card.selected ? 'selected' : swayClass}}`;
                
                const cornerRank = getCardCornerRank(card);

                let lenClass = "len-1";
                const l = card.str.length;
                if(l === 2) lenClass = "len-2";
                else if(l === 3) lenClass = "len-3";
                else if(l === 4) lenClass = "len-4";
                else if(l === 5) lenClass = "len-5";
                else if(l > 5) lenClass = "len-many";

                el.innerHTML = `
                    <div class="card-frame-inner"></div>
                    <div class="pip-corner-tl" style="color: ${{card.suitColor}};">
                        <span class="corner-text">${{cornerRank}}</span>
                        <span class="corner-suit-icon">${{card.suit}}</span>
                    </div>
                    <div class="term-box-center">
                        <span class="term-math-pixel ${{lenClass}}">${{card.str}}</span>
                    </div>
                    <div class="pip-corner-br" style="color: ${{card.suitColor}};">
                        <span class="corner-text">${{cornerRank}}</span>
                        <span class="corner-suit-icon">${{card.suit}}</span>
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
                btnPlay.className = "pixel-btn-action px-8 py-3.5 sm:px-12 sm:py-4 text-xs sm:text-sm tracking-widest cursor-pointer";
            }} else {{
                btnPlay.disabled = true;
                btnPlay.className = "pixel-box-8bit bg-[#131720] text-gray-600 px-8 py-3.5 sm:px-12 sm:py-4 text-xs sm:text-sm tracking-widest opacity-40 cursor-not-allowed";
            }}
        }}

        function playHand() {{
            const selected = hand.filter(c => c.selected);
            const info = getCommonFactorInfo(selected);

            if(selected.length < 2 || !info || !info.isValid) {{
                SFX.error();
                handContainer.classList.add('animate-shake');
                levelStats.errors++;
                setTimeout(() => handContainer.classList.remove('animate-shake'), 250);
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
                setTimeout(() => flameContainer.classList.add('hidden'), 200);
                
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
                desc.innerHTML = `¡PRECISIÓN PURA!<br>Ganaste un comodín SALTAR RONDA.<br>Bono: +${{bonusScore.toLocaleString()}} pts`;
            }} else {{
                desc.innerHTML = `Precisión: ${{Math.round(precision*100)}}%.<br>Bono: +${{bonusScore.toLocaleString()}} pts`;
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
                showAlert("⏭️ ¡RONDA SALTADA!");
                
                round++;
                if(round > 3) {{
                    levelStats.actualCorrect = Math.max(1, levelStats.actualCorrect);
                    levelStats.optimalPossible = Math.max(1, levelStats.optimalPossible);
                    endLevel();
                }} else {{
                    startRound();
                }}
            }}
            updateUI();
        }}
    </script>
</body>
</html>
"""

components.html(GAME_HTML, height=720, scrolling=False)
