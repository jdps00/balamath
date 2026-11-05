"""
Balatro: Factor Común - Dark Fantasy 8-Bit Edition
Curso: IF0003 Matemática Básica para Informática Empresarial
Universidad de Costa Rica - Recinto de Paraíso
"""

import os
import glob
import zipfile
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
        background-color: #030406;
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

def get_font_from_zip(zip_pattern, ttf_name_substring="DOS"):
    zip_files = glob.glob(os.path.join(current_dir, zip_pattern))
    for zf in zip_files:
        try:
            with zipfile.ZipFile(zf, "r") as z:
                for name in z.namelist():
                    if ttf_name_substring.lower() in name.lower() and name.lower().endswith(".ttf"):
                        return base64.b64encode(z.read(name)).decode("utf-8")
        except Exception:
            continue
    return None

# Fondos GIF según el estado
bg_game_b64 = get_base64_file("background_gif.gif") or get_base64_file("background.gif")
bg_reg_b64 = get_base64_file("background_gif_2.gif") or get_base64_file("background_2.gif") or bg_game_b64

# Audio de fondo
audio_bg_b64 = get_base64_file("background.mp3")

# Imágenes de personajes Pokémon
ricky_b64 = get_base64_file("ricky.png")
ariana_b64 = get_base64_file("ariana.png")

# Fuentes con soporte de lectura directa en ZIP
dos_font_b64 = (
    get_base64_file("Perfect DOS VGA 437 Win.ttf") or 
    get_base64_file("Perfect DOS VGA 437.ttf") or
    get_font_from_zip("*dos*.zip", "DOS") or
    get_font_from_zip("*.zip", "DOS")
)

balatro_font_b64 = (
    get_base64_file("balatro.otf") or 
    get_font_from_zip("*balatro*.zip", "balatro")
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
        src: local('Courier New'), monospace;
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
        src: local('DosVgaFont'), monospace;
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

ricky_img_tag = f'<img src="data:image/png;base64,{ricky_b64}" class="w-full h-full object-contain pixelated" alt="Ricky" />' if ricky_b64 else '<div class="font-dos text-base text-cyan-400 font-bold">[CHICO]</div>'
ariana_img_tag = f'<img src="data:image/png;base64,{ariana_b64}" class="w-full h-full object-contain pixelated" alt="Ariana" />' if ariana_b64 else '<div class="font-dos text-base text-rose-400 font-bold">[CHICA]</div>'

GAME_HTML = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Balatro: Factor Común</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        {font_face_css}

        :root {{
            --font-dos: 'DosVgaFont', monospace;
            --font-balatro: 'BalatroFont', 'DosVgaFont', monospace;
            --dark-iron: #090b10;
            --border-steel: #232a3a;
            --blood-seal: #8a171e;
            --gold-relic: #d4a017;
            --card-cream: #f4edd9;
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
            color: #ece4d0;
            font-family: var(--font-dos);
            overflow: hidden;
            user-select: none;
            margin: 0;
            height: 100vh;
            width: 100vw;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background-color: #030406;
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

        .procedural-reg {{ background: radial-gradient(circle at center, #141724, #05060a); }}
        .procedural-game {{ background: radial-gradient(circle at center, #142820, #030805); }}

        .bg-vignette {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: radial-gradient(circle at center, rgba(5, 7, 10, 0.35) 0%, rgba(2, 3, 5, 0.94) 100%);
            pointer-events: none;
            z-index: -2;
        }}

        /* ========================================================
           ARQUITECTURA DE UI PIXEL ART 8-BIT ESTRICTA
           ======================================================== */
        .px-panel {{
            background: #141822;
            border: 4px solid #000000;
            box-shadow: 
                inset 3px 3px 0 #2e374d,
                inset -3px -3px 0 #080a0e,
                0 6px 0 #000000;
            position: relative;
        }}

        .px-panel-slot {{
            background: #080a0f;
            border: 3px solid #000000;
            box-shadow: inset 2px 2px 0 #1b2130, inset -2px -2px 0 #000000;
        }}

        .px-badge-blood {{
            background: #8b181e;
            border: 4px solid #000000;
            box-shadow: 
                inset 3px 3px 0 #ba2f36,
                inset -3px -3px 0 #4a070b,
                0 6px 0 #000000;
            color: #ffffff;
            text-shadow: 2px 2px 0 #000000;
        }}

        .px-btn-primary {{
            font-family: var(--font-dos);
            background: #c95116;
            border: 4px solid #000000;
            box-shadow: 
                inset 4px 4px 0 #ff8244,
                inset -4px -4px 0 #6e2503,
                0 6px 0 #000000;
            color: #ffffff;
            text-shadow: 2px 2px 0 #000000;
            transition: transform 0.05s steps(2);
        }}
        .px-btn-primary:hover {{ background: #dc5e1e; }}
        .px-btn-primary:active {{
            transform: translateY(4px);
            box-shadow: 
                inset 4px 4px 0 #6e2503,
                inset -4px -4px 0 #ff8244,
                0 2px 0 #000000;
        }}

        .px-btn-cyan {{
            font-family: var(--font-dos);
            background: #12588c;
            border: 3px solid #000000;
            box-shadow: 
                inset 3px 3px 0 #2a83c7,
                inset -3px -3px 0 #092c47,
                0 5px 0 #000000;
            color: #ffffff;
            text-shadow: 2px 2px 0 #000000;
        }}

        /* SELECCIÓN DE PERSONAJE 8-BIT */
        .char-card-pixel {{
            background: #0d1017;
            border: 3px solid #000000;
            box-shadow: inset 2px 2px 0 #1c2436;
            cursor: pointer;
            transition: transform 0.08s steps(2);
        }}
        .char-card-pixel:hover {{
            border-color: #d4a017;
            background: #131824;
            transform: translateY(-2px);
        }}
        .char-card-pixel.selected {{
            border-color: #d4a017;
            background: #192030;
            box-shadow: inset 0 0 0 3px #d4a017, 0 4px 0 #000000;
        }}

        /* ========================================================
           CARTAS FÍSICAS BALATRO (CONSERVA TU FORMATO)
           ======================================================== */
        .balatro-card {{
            width: 104px;
            height: 150px;
            background: var(--card-cream);
            border: 4px solid #000000;
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

        .card-inner-frame {{
            position: absolute;
            top: 4px; left: 4px; right: 4px; bottom: 4px;
            border: 2px dashed rgba(60, 50, 35, 0.25);
            pointer-events: none;
        }}

        .card-pip-tl {{
            position: absolute;
            top: 6px; left: 7px;
            display: flex; flex-direction: column; align-items: center;
            line-height: 1;
            pointer-events: none;
            font-family: var(--font-dos);
        }}
        .card-pip-br {{
            position: absolute;
            bottom: 6px; right: 7px;
            display: flex; flex-direction: column; align-items: center;
            line-height: 1;
            transform: rotate(180deg);
            pointer-events: none;
            font-family: var(--font-dos);
        }}

        .pip-val {{
            font-size: 13px;
            font-weight: bold;
            letter-spacing: -0.5px;
        }}
        .pip-suit {{
            font-size: 11px;
            margin-top: 1px;
        }}

        .term-container {{
            max-width: 86%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            z-index: 2;
            pointer-events: none;
        }}

        .term-main {{
            font-family: var(--font-dos);
            color: #12141a;
            line-height: 1;
            white-space: nowrap;
            letter-spacing: -0.5px;
            font-weight: bold;
            text-shadow: 1px 1px 0 rgba(255,255,255,0.7);
        }}

        .term-main sup, .pip-val sup {{
            font-size: 0.65em;
            vertical-align: super;
            line-height: 0;
            font-family: var(--font-dos);
        }}

        .len-1 {{ font-size: 2.3rem; }}
        .len-2 {{ font-size: 1.95rem; }}
        .len-3 {{ font-size: 1.65rem; }}
        .len-4 {{ font-size: 1.35rem; }}
        .len-5 {{ font-size: 1.15rem; }}
        .len-many {{ font-size: 0.95rem; }}

        @keyframes balatro-sway-1 {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-7px); }}
        }}
        @keyframes balatro-sway-2 {{
            0%, 100% {{ transform: translateY(-5px); }}
            50% {{ transform: translateY(3px); }}
        }}
        @keyframes balatro-sway-3 {{
            0%, 100% {{ transform: translateY(2px); }}
            50% {{ transform: translateY(-6px); }}
        }}

        .idle-sway-1 {{ animation: balatro-sway-1 3s steps(5) infinite; }}
        .idle-sway-2 {{ animation: balatro-sway-2 3.6s steps(5) infinite; }}
        .idle-sway-3 {{ animation: balatro-sway-3 4s steps(5) infinite; }}

        .balatro-card:hover {{
            transform: translateY(-16px) !important;
            animation-play-state: paused;
            box-shadow: 
                inset 3px 3px 0 #ffffff,
                inset -3px -3px 0 #b3a992,
                0 14px 0 #000000;
            z-index: 20;
        }}
        .balatro-card.selected {{
            transform: translateY(-26px) !important;
            animation-play-state: paused;
            border-color: #d4a017;
            box-shadow: 
                inset 3px 3px 0 #fff7b8,
                inset -3px -3px 0 #ab7c07,
                0 0 0 3px #d4a017,
                0 14px 0 #000000 !important;
            z-index: 30;
        }}

        @media (max-width: 640px) {{
            .balatro-card {{ width: 84px !important; height: 122px !important; }}
            .len-1 {{ font-size: 1.65rem !important; }}
            .len-2 {{ font-size: 1.4rem !important; }}
            .len-3 {{ font-size: 1.15rem !important; }}
            .len-4 {{ font-size: 0.95rem !important; }}
            .len-5 {{ font-size: 0.82rem !important; }}
            .len-many {{ font-size: 0.72rem !important; }}
            .pip-val {{ font-size: 11px !important; }}
            .pip-suit {{ font-size: 9px !important; }}
            #hand-container {{ min-height: 200px !important; }}
        }}

        /* ICONOS PIXEL ART SVG (CERO EMOJIS) */
        .px-icon {{
            display: inline-block;
            vertical-align: middle;
            image-rendering: pixelated;
        }}

        /* RETROALIMENTACIÓN DE PUNTOS */
        @keyframes float-score-pixel {{
            0% {{ transform: translate(-50%, -40%) scale(0.9); opacity: 0; }}
            20% {{ transform: translate(-50%, -50%) scale(1.1); opacity: 1; }}
            80% {{ transform: translate(-50%, -55%) scale(1); opacity: 1; }}
            100% {{ transform: translate(-50%, -65%) scale(0.95); opacity: 0; }}
        }}
        .score-splash-8bit {{
            font-family: var(--font-dos);
            color: #ffffff;
            text-shadow: 4px 4px 0 #8b181e, -3px -3px 0 #c95116;
            animation: float-score-pixel 1.1s steps(6) forwards;
        }}

        @keyframes shake-pixel {{
            0%, 100% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-8px); }}
            75% {{ transform: translateX(8px); }}
        }}
        .animate-shake {{ animation: shake-pixel 0.22s steps(4); }}
    </style>
</head>
<body class="p-2 sm:p-4">
    {bg_reg_tag}
    {bg_game_tag}
    {audio_html_tag}
    <div class="bg-vignette"></div>

    <!-- MODAL INICIO / REGISTRO DARK FANTASY 8-BIT -->
    <div id="intro-modal" class="fixed inset-0 bg-black/85 z-[1000] flex items-center justify-center p-4">
        <div class="px-panel max-w-md w-full p-6 sm:p-8 text-center">
            
            <div class="px-badge-blood py-3.5 px-4 mb-6 transform -rotate-1 inline-block w-full">
                <h1 class="text-2xl sm:text-3xl tracking-wide font-balatro">FACTOR COMÚN</h1>
                <p class="text-xs sm:text-sm text-yellow-300 tracking-widest mt-1 font-dos">MATEMÁTICA BÁSICA • UCR</p>
            </div>
            
            <!-- PASO 1: NOMBRE -->
            <div id="step-name">
                <div class="px-panel-slot p-4 mb-6 text-left">
                    <label class="block text-xs sm:text-sm text-gray-400 mb-2 tracking-wider font-dos">APODO DEL JUGADOR:</label>
                    <input type="text" id="username-input" class="w-full bg-[#05070a] border-2 border-[#2b3547] text-[#d4a017] p-3 text-center uppercase tracking-wider text-base sm:text-lg font-bold font-dos outline-none focus:border-[#d4a017]" placeholder="TU NOMBRE" maxlength="12">
                </div>
                <button onclick="goToGenderStep()" class="px-btn-primary w-full py-4 text-sm sm:text-base font-bold tracking-wider">
                    CONTINUAR ➔
                </button>
            </div>

            <!-- PASO 2: SELECCIÓN POKÉMON -->
            <div id="step-gender" class="hidden">
                <div class="px-panel-slot p-4 mb-5 text-center">
                    <p class="text-xs sm:text-sm text-yellow-300 font-dos mb-4">ELIGE TU PERSONAJE</p>
                    <div class="grid grid-cols-2 gap-4">
                        <div id="opt-boy" onclick="selectGender('boy')" class="char-card-pixel p-3 flex flex-col items-center">
                            <div class="w-24 h-24 sm:w-28 sm:h-28 flex items-center justify-center mb-2">
                                {ricky_img_tag}
                            </div>
                            <span class="text-xs sm:text-sm font-bold text-gray-200 font-dos">[ CHICO ]</span>
                        </div>
                        <div id="opt-girl" onclick="selectGender('girl')" class="char-card-pixel p-3 flex flex-col items-center">
                            <div class="w-24 h-24 sm:w-28 sm:h-28 flex items-center justify-center mb-2">
                                {ariana_img_tag}
                            </div>
                            <span class="text-xs sm:text-sm font-bold text-gray-200 font-dos">[ CHICA ]</span>
                        </div>
                    </div>
                </div>
                <button id="btn-start-game" onclick="startGame()" disabled class="px-panel bg-[#0d1017] text-gray-600 w-full py-4 text-sm font-bold tracking-wider opacity-40 cursor-not-allowed">
                    INICIAR PARTIDA
                </button>
            </div>

        </div>
    </div>

    <!-- BOTONES AUXILIARES INFERIORES -->
    <div class="fixed bottom-3 left-3 z-40">
        <button onclick="toggleTutorial()" class="px-btn-cyan text-xs sm:text-sm px-4 py-2 font-dos">
            [ ? ] GUÍA
        </button>
    </div>
    <div class="fixed bottom-3 right-3 z-40">
        <!-- RANK DESHABILITADO -->
        <button onclick="showRankNotice()" class="px-panel bg-[#0d1017] text-gray-500 text-xs sm:text-sm px-4 py-2 cursor-pointer relative font-dos" title="En desarrollo por compañero">
            [ RANK ]
            <span class="absolute -top-2 -right-2 bg-yellow-500 text-black text-[9px] font-bold px-1.5 border border-black">DEV</span>
        </button>
    </div>

    <!-- PANEL GUÍA DIDÁCTICA -->
    <div id="tutorial-panel" class="fixed left-0 top-0 h-full w-72 sm:w-80 bg-[#10141d] border-r-4 border-black p-4 sm:p-5 flex flex-col z-50 transform -translate-x-full transition-transform duration-200 shadow-2xl">
        <div class="flex justify-between items-center mb-4 border-b-2 border-white/10 pb-2">
            <div class="px-badge-blood px-3 py-1 text-xs font-dos">REGLAS DE FACTORIZACIÓN</div>
            <button onclick="toggleTutorial()" class="text-white text-base font-bold font-dos">[ X ]</button>
        </div>
        <div class="px-panel-slot p-3 text-xl text-center mb-3 font-dos">
            4x² + 6x
        </div>
        <p class="text-xs text-yellow-300 text-center mb-3 font-dos">MCD = 2, VARIABLE COMÚN = x</p>
        <div class="px-panel-slot p-3 text-xl text-center mb-4 font-dos text-emerald-400">
            2x · (2x + 3)
        </div>
        <div class="text-xs text-gray-300 leading-relaxed font-dos space-y-2">
            <p>1. Selecciona 2 o más cartas que compartan factor común numérico o literal.</p>
            <p>2. Presiona "JUGAR MANO" para resolver y multiplicar tus fichas.</p>
            <p>3. Las cartas no usadas permanecen en tu mano para la siguiente ronda.</p>
        </div>
    </div>

    <!-- HUD SUPERIOR EN PIXEL ART -->
    <header class="flex justify-between items-center z-10 max-w-5xl mx-auto w-full gap-2 px-1">
        <!-- Nivel y Ronda -->
        <div class="px-panel px-3.5 py-2.5 text-center min-w-[110px] sm:min-w-[140px]">
            <div class="text-xs text-gray-400 font-dos">NIVEL <span id="level-display" class="text-yellow-400 text-base font-dos font-bold">1</span></div>
            <div class="text-[11px] text-gray-300 mt-0.5 font-dos">RONDA <span id="round-display" class="text-white font-bold">1</span>/3</div>
        </div>

        <!-- 3 Comodines (Iconos pixel art procedimentales) -->
        <div class="flex justify-center gap-2 sm:gap-3">
            <!-- REVELAR -->
            <button id="btn-joker-reveal" onclick="useJoker('reveal')" title="Revelar Factor Común" class="px-panel p-2 sm:p-2.5 relative active:translate-y-1">
                <svg class="px-icon w-6 h-6" viewBox="0 0 16 16" fill="none">
                    <rect x="5" y="5" width="6" height="6" fill="#4deeea"/>
                    <rect x="2" y="7" width="3" height="2" fill="#1b827e"/>
                    <rect x="11" y="7" width="3" height="2" fill="#1b827e"/>
                    <rect x="7" y="2" width="2" height="3" fill="#1b827e"/>
                    <rect x="7" y="11" width="2" height="3" fill="#1b827e"/>
                    <rect x="7" y="7" width="2" height="2" fill="#000000"/>
                </svg>
                <span id="qty-reveal" class="absolute -top-2 -right-2 bg-red-600 text-white text-[10px] px-1.5 border border-black font-dos">1</span>
            </button>

            <!-- REROLL -->
            <button id="btn-joker-reroll" onclick="useJoker('reroll')" title="Revolver Mano" class="px-panel p-2 sm:p-2.5 relative active:translate-y-1">
                <svg class="px-icon w-6 h-6" viewBox="0 0 16 16" fill="none">
                    <rect x="2" y="2" width="12" height="12" fill="#7b2cbf"/>
                    <rect x="3" y="3" width="10" height="10" fill="#9d4edd"/>
                    <rect x="4" y="4" width="2" height="2" fill="#ffffff"/>
                    <rect x="10" y="4" width="2" height="2" fill="#ffffff"/>
                    <rect x="7" y="7" width="2" height="2" fill="#ffffff"/>
                    <rect x="4" y="10" width="2" height="2" fill="#ffffff"/>
                    <rect x="10" y="10" width="2" height="2" fill="#ffffff"/>
                </svg>
                <span id="qty-reroll" class="absolute -top-2 -right-2 bg-purple-600 text-white text-[10px] px-1.5 border border-black font-dos">1</span>
            </button>

            <!-- SALTAR 1 RONDA -->
            <button id="btn-joker-skip" onclick="useJoker('skip')" title="Saltar 1 Ronda" class="px-panel p-2 sm:p-2.5 relative active:translate-y-1 opacity-40">
                <svg class="px-icon w-6 h-6" viewBox="0 0 16 16" fill="none">
                    <rect x="2" y="3" width="3" height="10" fill="#d4a017"/>
                    <rect x="5" y="5" width="2" height="6" fill="#d4a017"/>
                    <rect x="7" y="7" width="2" height="2" fill="#d4a017"/>
                    <rect x="9" y="3" width="3" height="10" fill="#f1b31c"/>
                    <rect x="12" y="5" width="2" height="6" fill="#f1b31c"/>
                </svg>
                <span id="qty-skip" class="absolute -top-2 -right-2 bg-yellow-500 text-black text-[10px] px-1.5 border border-black font-dos">0</span>
            </button>
        </div>

        <!-- Puntos y Jugador -->
        <div class="px-panel px-3.5 py-2.5 text-center min-w-[110px] sm:min-w-[140px]">
            <div class="text-xs text-gray-400 font-dos">PUNTOS</div>
            <div id="total-score" class="text-base sm:text-xl text-yellow-400 font-dos font-bold leading-tight">0</div>
            <div id="user-display-tag" class="text-[10px] text-gray-300 truncate max-w-[100px] mx-auto font-dos">JUGADOR</div>
        </div>
    </header>

    <!-- ÁREA CENTRAL DE CARTAS -->
    <main class="flex-grow flex flex-col items-center justify-center relative w-full max-w-5xl mx-auto my-auto">
        <div id="hand-container" class="flex justify-center items-center flex-wrap gap-2.5 sm:gap-4 w-full px-2 mb-6"></div>

        <button id="btn-play" onclick="playHand()" disabled class="px-panel bg-[#0d1017] text-gray-600 px-9 py-3.5 sm:px-14 sm:py-4 text-xs sm:text-sm tracking-widest opacity-40 cursor-not-allowed font-dos">
            JUGAR MANO
        </button>

        <div id="flame-score-container" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 hidden z-40 pointer-events-none text-center">
            <div id="flame-score" class="text-4xl sm:text-6xl score-splash-8bit tracking-wider">0</div>
        </div>
    </main>

    <!-- MODAL FIN DE NIVEL -->
    <div id="level-modal" class="fixed inset-0 bg-black/85 z-50 hidden flex items-center justify-center p-4">
        <div class="px-panel max-w-sm w-full p-6 text-center">
            <div class="px-badge-blood py-2 px-4 mb-4 transform -rotate-1 inline-block w-full">
                <h2 class="text-lg sm:text-xl font-balatro">NIVEL COMPLETADO</h2>
            </div>
            <div class="flex justify-center gap-3 my-4 font-dos text-2xl text-yellow-400" id="modal-stars"></div>
            <p id="modal-desc" class="px-panel-slot p-3 text-gray-200 text-xs sm:text-sm leading-relaxed mb-5 font-dos"></p>
            <button onclick="nextLevel()" class="px-btn-primary w-full py-3.5 text-xs sm:text-sm tracking-wider">
                SIGUIENTE NIVEL ➔
            </button>
        </div>
    </div>

    <!-- ALERTA BALATRO -->
    <div id="alert-modal" class="fixed top-12 left-1/2 -translate-x-1/2 px-badge-blood text-xs sm:text-sm px-5 py-3 z-50 hidden text-center max-w-[90vw] font-dos">
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
            error: () => {{ playTone(130, 'sawtooth', 0.25, 0.25); setTimeout(() => playTone(90, 'sawtooth', 0.25, 0.25), 100); }},
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
            btn.className = "px-btn-primary w-full py-4 text-sm font-bold tracking-wider cursor-pointer";
            SFX.select();
        }}

        function startGame() {{
            if (!playerGender) return;
            document.getElementById('intro-modal').classList.add('hidden');
            document.getElementById('user-display-tag').textContent = `[${{playerGender === 'boy' ? 'CHICO' : 'CHICA'}}] ${{playerName}}`;
            
            // Alternar de fondo de registro al de partida activa
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
            showAlert("MODULO EN DESARROLLO POR COMPANERO.");
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

        function formatTerm(c, x, y) {{
            let s = "";
            if (c === -1 && (x > 0 || y > 0)) s += "-";
            else if (c !== 1 || (x === 0 && y === 0)) s += c;
            
            if (x === 1) s += "x"; 
            else if (x > 1) s += `x<sup>${{x}}</sup>`;
            
            if (y === 1) s += "y"; 
            else if (y > 1) s += `y<sup>${{y}}</sup>`;
            return s;
        }}

        function getCardCornerRank(card) {{
            if (card.x > 0 && card.y === 0) return card.x === 1 ? "X" : `X<sup>${{card.x}}</sup>`;
            if (card.y > 0 && card.x === 0) return card.y === 1 ? "Y" : `Y<sup>${{card.y}}</sup>`;
            if (card.x > 0 && card.y > 0) return "XY";
            return Math.abs(card.c).toString();
        }}

        function getTermRawLength(card) {{
            let len = Math.abs(card.c).toString().length;
            if(card.c < 0) len++;
            if(card.x > 0) len += (card.x > 1 ? 2 : 1);
            if(card.y > 0) len += (card.y > 1 ? 2 : 1);
            return len;
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
            const suitColor = (suit === '♥' || suit === '♦') ? '#8b181e' : '#12588c';

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
                el.className = `balatro-card ${{card.selected ? 'selected' : swayClass}}`;
                
                const cornerRank = getCardCornerRank(card);
                const rawLen = getTermRawLength(card);

                let lenClass = "len-1";
                if(rawLen === 2) lenClass = "len-2";
                else if(rawLen === 3) lenClass = "len-3";
                else if(rawLen === 4) lenClass = "len-4";
                else if(rawLen === 5) lenClass = "len-5";
                else if(rawLen > 5) lenClass = "len-many";

                el.innerHTML = `
                    <div class="card-inner-frame"></div>
                    <div class="card-pip-tl" style="color: ${{card.suitColor}};">
                        <span class="pip-val">${{cornerRank}}</span>
                        <span class="pip-suit">${{card.suit}}</span>
                    </div>
                    <div class="term-container">
                        <span class="term-main ${{lenClass}}">${{card.str}}</span>
                    </div>
                    <div class="card-pip-br" style="color: ${{card.suitColor}};">
                        <span class="pip-val">${{cornerRank}}</span>
                        <span class="pip-suit">${{card.suit}}</span>
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
                btnPlay.className = "px-btn-primary px-9 py-3.5 sm:px-14 sm:py-4 text-xs sm:text-sm tracking-widest cursor-pointer font-dos";
            }} else {{
                btnPlay.disabled = true;
                btnPlay.className = "px-panel bg-[#0d1017] text-gray-600 px-9 py-3.5 sm:px-14 sm:py-4 text-xs sm:text-sm tracking-widest opacity-40 cursor-not-allowed font-dos";
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

            hand = hand.filter(c => !c.selected);

            setTimeout(() => {{
                flameContainer.classList.add('hidden');
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
                    starContainer.innerHTML += `<span>[★]</span>`;
                }} else {{
                    starContainer.innerHTML += `<span class="text-gray-600">[☆]</span>`;
                }}
            }}

            let bonusScore = stars * 1000 * level;
            score += bonusScore;
            document.getElementById('total-score').textContent = score.toLocaleString();

            if(stars === 3) {{
                comodines.skip++;
                updateUI();
                desc.innerHTML = `PRECISIÓN PERFECTA.<br>OBTUVISTE: SALTAR 1 RONDA.<br>BONO: +${{bonusScore.toLocaleString()}} PTS`;
            }} else {{
                desc.innerHTML = `PRECISIÓN: ${{Math.round(precision*100)}}%.<br>BONO: +${{bonusScore.toLocaleString()}} PTS`;
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
            setTimeout(() => {{
                el.classList.add('hidden');
            }}, 2400);
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
                    showAlert(`FACTOR: <b>${{bestFactor}}</b> (EN ${{maxSubset}} CARTAS)`);
                }} else {{
                    showAlert(`NO HAY FACTORES COMUNES.`);
                }}
            }} 
            else if (type === 'reroll') {{
                comodines.reroll--;
                SFX.discard();
                hand = [];
                startRound();
                showAlert("MANO REVOLVIDA.");
            }}
            else if (type === 'skip') {{
                comodines.skip--;
                SFX.winRound();
                showAlert("RONDA SALTADA.");
                
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
