"""
Balatro Factor Común - Edición UCR
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
        background-color: #0b1712;
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

# Video de fondo
video_b64 = None
video_mime = "video/mp4"
for v_name in ["fakcpg.mp4", "faKcpg.mp4", "fakcpg.gif", "faKcpg.gif"]:
    b64 = get_base64_file(v_name)
    if b64:
        video_b64 = b64
        if v_name.endswith(".gif"):
            video_mime = "image/gif"
        break

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
        src: local('Courier New'), monospace;
        font-weight: bold;
    }
    """

if balatro_font_b64:
    font_face_css += f"""
    @font-face {{
        font-family: 'BalatroFont';
        src: url(data:font/otf;base64,{balatro_font_b64}) format('opentype');
        font-weight: normal;
        font-style: normal;
    }}
    """
else:
    font_face_css += """
    @font-face {
        font-family: 'BalatroFont';
        src: local('Impact'), local('Arial Black'), sans-serif;
        font-weight: bold;
    }
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

audio_html_tag = ""
if audio_bg_b64:
    audio_html_tag = f"""
    <audio id="bg-music" loop preload="auto">
        <source src="data:audio/mp3;base64,{audio_bg_b64}" type="audio/mp3">
    </audio>
    """

ricky_img_tag = f'<img src="data:image/png;base64,{ricky_b64}" class="w-full h-full object-contain pixelated" alt="Ricky" />' if ricky_b64 else '<div class="text-3xl">👦</div>'
ariana_img_tag = f'<img src="data:image/png;base64,{ariana_b64}" class="w-full h-full object-contain pixelated" alt="Ariana" />' if ariana_b64 else '<div class="text-3xl">👧</div>'

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
            --font-balatro: 'BalatroFont', sans-serif;
            --balatro-blue: #0077c8;
            --balatro-red: #ea2e35;
            --balatro-yellow: #f1b31c;
            --balatro-orange: #ef5b25;
            --balatro-card-bg: #fbf8eb;
        }}

        * {{
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }}

        .pixelated {{
            image-rendering: pixelated;
            image-rendering: crisp-edges;
        }}

        body {{
            color: white;
            font-family: var(--font-balatro);
            overflow: hidden;
            user-select: none;
            margin: 0;
            height: 100vh;
            width: 100vw;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background-color: #0b1712;
        }}

        .font-dos {{ font-family: var(--font-dos); }}
        .font-balatro {{ font-family: var(--font-balatro); }}

        /* VIDEO Y FONDOS */
        .video-bg {{
            position: fixed;
            top: 50%; left: 50%;
            min-width: 100%; min-height: 100%;
            width: auto; height: auto;
            transform: translate(-50%, -50%) scale(1.05);
            z-index: -3;
            object-fit: cover;
            pointer-events: none;
            transition: filter 1.2s ease-in-out;
        }}

        .procedural-bg {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: radial-gradient(circle at center, #1b533d, #081a13);
            z-index: -3;
        }}

        .bg-tint-overlay {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: radial-gradient(circle at center, rgba(16, 56, 38, 0.45) 0%, rgba(5, 18, 12, 0.88) 100%);
            mix-blend-mode: multiply;
            pointer-events: none;
            z-index: -2;
        }}

        .filter-ronda-1 {{ filter: hue-rotate(95deg) saturate(140%) brightness(0.72) contrast(1.15); }}
        .filter-ronda-2 {{ filter: hue-rotate(60deg) saturate(150%) brightness(0.8) contrast(1.2); }}
        .filter-ronda-3 {{ filter: hue-rotate(150deg) saturate(135%) brightness(0.68) contrast(1.15); }}

        /* PANELES BALATRO */
        .balatro-box {{
            background: #2b313b;
            border: 4px solid #171b21;
            border-radius: 12px;
            box-shadow: 0 10px 0 #121418, 0 16px 25px rgba(0,0,0,0.85);
            position: relative;
        }}

        .balatro-box-inner {{
            background: #1e2229;
            border: 3px solid #111418;
            border-radius: 8px;
        }}

        .balatro-header-badge {{
            background: #e12d39;
            border: 3px solid #14171c;
            border-radius: 8px;
            box-shadow: 0 5px 0 #8c161d;
            color: #ffffff;
            text-shadow: 2px 2px 0 #570b10;
        }}

        .balatro-input {{
            background: #111317;
            border: 3px solid #363c48;
            border-radius: 8px;
            box-shadow: inset 0 4px 6px rgba(0,0,0,0.7);
            color: #ffffff;
            font-family: var(--font-dos);
        }}
        .balatro-input:focus {{
            border-color: #f1b31c;
            outline: none;
        }}

        .balatro-btn-orange {{
            background: #ef5b25;
            border: 3px solid #171b21;
            border-radius: 8px;
            box-shadow: 0 6px 0 #9e330e, 0 8px 12px rgba(0,0,0,0.6);
            color: #ffffff;
            text-shadow: 2px 2px 0 #5d1b04;
            transition: transform 0.08s ease, box-shadow 0.08s ease;
        }}
        .balatro-btn-orange:hover {{ background: #f86a36; }}
        .balatro-btn-orange:active {{
            transform: translateY(4px);
            box-shadow: 0 2px 0 #9e330e, 0 3px 6px rgba(0,0,0,0.6);
        }}

        .balatro-btn-blue {{
            background: #0077c8;
            border: 3px solid #171b21;
            border-radius: 8px;
            box-shadow: 0 6px 0 #004677, 0 8px 12px rgba(0,0,0,0.6);
            color: #ffffff;
            text-shadow: 2px 2px 0 #002844;
            transition: transform 0.08s ease, box-shadow 0.08s ease;
        }}

        /* SELECCIÓN DE PERSONAJE ESTILO POKÉMON */
        .char-card {{
            background: #1b2029;
            border: 3px solid #14161d;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
            box-shadow: 0 4px 0 #0d0f14;
        }}
        .char-card:hover {{
            transform: translateY(-4px);
            border-color: #0077c8;
            box-shadow: 0 8px 0 #0d0f14;
        }}
        .char-card.selected {{
            border-color: #f1b31c;
            box-shadow: 0 0 0 3px #f1b31c, 0 6px 0 #8c6000;
            background: #252e3d;
            transform: translateY(-4px);
        }}

        /* CARTAS BALATRO */
        .balatro-card {{
            width: 104px;
            height: 148px;
            background: linear-gradient(175deg, #ffffff 0%, #f6f3ea 70%, #ece6d8 100%);
            border-radius: 10px;
            border: 2px solid #232731;
            box-shadow: 0 6px 0 #12141a, 0 10px 18px rgba(0,0,0,0.65);
            position: relative;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.16s cubic-bezier(0.2, 0.9, 0.3, 1.2), box-shadow 0.16s ease;
        }}

        .card-inner-frame {{
            position: absolute;
            top: 5px; left: 5px; right: 5px; bottom: 5px;
            border: 1px dashed rgba(50, 50, 50, 0.22);
            border-radius: 6px;
            pointer-events: none;
        }}

        .card-pip-tl {{
            position: absolute;
            top: 6px; left: 8px;
            display: flex; flex-direction: column; align-items: center;
            line-height: 0.95;
            pointer-events: none;
            font-family: var(--font-dos);
        }}
        .card-pip-br {{
            position: absolute;
            bottom: 6px; right: 8px;
            display: flex; flex-direction: column; align-items: center;
            line-height: 0.95;
            transform: rotate(180deg);
            pointer-events: none;
            font-family: var(--font-dos);
        }}

        .pip-val {{
            font-size: 15px;
            font-weight: bold;
        }}
        .pip-suit {{
            font-size: 12px;
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
            color: #1a1c22;
            text-align: center;
            line-height: 1;
            white-space: nowrap;
            letter-spacing: -0.5px;
            font-weight: bold;
            text-shadow: 1px 1px 0 rgba(0,0,0,0.12);
        }}

        .len-1 {{ font-size: 2.2rem; }}
        .len-2 {{ font-size: 1.95rem; }}
        .len-3 {{ font-size: 1.65rem; }}
        .len-4 {{ font-size: 1.35rem; }}
        .len-5 {{ font-size: 1.15rem; }}
        .len-many {{ font-size: 0.95rem; }}

        @keyframes balatro-sway-1 {{
            0%, 100% {{ transform: translateY(0px) rotate(-1.5deg); }}
            50% {{ transform: translateY(-7px) rotate(1.2deg); }}
        }}
        @keyframes balatro-sway-2 {{
            0%, 100% {{ transform: translateY(-5px) rotate(1.3deg); }}
            50% {{ transform: translateY(3px) rotate(-1.7deg); }}
        }}
        @keyframes balatro-sway-3 {{
            0%, 100% {{ transform: translateY(2px) rotate(-0.9deg); }}
            50% {{ transform: translateY(-6px) rotate(1.5deg); }}
        }}

        .idle-sway-1 {{ animation: balatro-sway-1 3.2s ease-in-out infinite; }}
        .idle-sway-2 {{ animation: balatro-sway-2 3.8s ease-in-out infinite; }}
        .idle-sway-3 {{ animation: balatro-sway-3 4.1s ease-in-out infinite; }}

        .balatro-card:hover {{
            transform: translateY(-16px) scale(1.05) rotate(0deg) !important;
            animation-play-state: paused;
            box-shadow: 0 12px 0 #12141a, 0 18px 24px rgba(0,0,0,0.7);
            z-index: 20;
        }}
        .balatro-card.selected {{
            transform: translateY(-26px) scale(1.08) rotate(0deg) !important;
            animation-play-state: paused;
            border-color: #f1b31c;
            box-shadow: 0 12px 0 #9e330e, 0 0 0 3px #f1b31c, 0 20px 28px rgba(0,0,0,0.8) !important;
            z-index: 30;
        }}

        @media (max-width: 640px) {{
            .balatro-card {{ width: 84px !important; height: 122px !important; }}
            .len-1 {{ font-size: 1.6rem !important; }}
            .len-2 {{ font-size: 1.4rem !important; }}
            .len-3 {{ font-size: 1.15rem !important; }}
            .len-4 {{ font-size: 0.95rem !important; }}
            .len-5 {{ font-size: 0.82rem !important; }}
            .len-many {{ font-size: 0.72rem !important; }}
            .pip-val {{ font-size: 12px !important; }}
            .pip-suit {{ font-size: 10px !important; }}
            #hand-container {{ min-height: 200px !important; }}
        }}

        @keyframes flame-flicker {{
            0% {{ text-shadow: 0 0 10px #ff5a00, 0 -5px 15px #ff9c00, 0 -10px 20px #ffce00; transform: scale(1); }}
            50% {{ text-shadow: 0 0 22px #ff5a00, 0 -10px 28px #ff9c00, 0 -15px 32px #ffce00; transform: scale(1.1); }}
            100% {{ text-shadow: 0 0 10px #ff5a00, 0 -5px 15px #ff9c00, 0 -10px 20px #ffce00; transform: scale(1); }}
        }}
        .score-flame {{ color: #fff; animation: flame-flicker 0.6s infinite alternate; font-family: var(--font-dos); }}

        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            20% {{ transform: translateX(-8px) rotate(-3deg); }}
            40% {{ transform: translateX(8px) rotate(3deg); }}
            60% {{ transform: translateX(-8px) rotate(-3deg); }}
            80% {{ transform: translateX(8px) rotate(3deg); }}
        }}
        .animate-shake {{ animation: shake 0.35s ease-in-out; }}

        #fx-canvas {{ position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 50; }}
    </style>
</head>
<body class="p-2 sm:p-4">
    {video_html_tag}
    {audio_html_tag}
    <div class="bg-tint-overlay"></div>
    <canvas id="fx-canvas"></canvas>

    <!-- INTRO MODAL ESTILO BALATRO: PASO 1 (NOMBRE) Y PASO 2 (GÉNERO POKÉMON) -->
    <div id="intro-modal" class="fixed inset-0 bg-black/85 z-[1000] flex items-center justify-center p-4 backdrop-blur-sm">
        <div class="balatro-box max-w-sm w-full p-6 text-center">
            
            <div class="balatro-header-badge py-3 px-4 mb-5 transform -rotate-1 inline-block w-full">
                <h1 class="text-2xl sm:text-3xl tracking-wide font-balatro">FACTOR COMÚN</h1>
                <p class="text-[11px] opacity-90 tracking-widest mt-1 font-dos">MATEMÁTICA BÁSICA • UCR</p>
            </div>
            
            <!-- PASO 1: NOMBRE -->
            <div id="step-name">
                <div class="balatro-box-inner p-4 mb-5 text-left">
                    <label class="block text-xs text-gray-300 mb-2 tracking-wider font-dos">APODO DEL JUGADOR:</label>
                    <input type="text" id="username-input" class="balatro-input w-full p-3 text-center uppercase tracking-wider text-base font-bold font-dos" placeholder="TU NOMBRE" maxlength="12">
                </div>
                <button onclick="goToGenderStep()" class="balatro-btn-orange w-full py-4 text-sm font-bold tracking-wider font-balatro">
                    CONTINUAR ➔
                </button>
            </div>

            <!-- PASO 2: ELECCIÓN DE PERSONAJE POKÉMON -->
            <div id="step-gender" class="hidden">
                <div class="balatro-box-inner p-3 mb-4 text-center">
                    <p class="text-xs text-yellow-300 font-dos mb-3">¿ERES CHICO O CHICA?</p>
                    <div class="grid grid-cols-2 gap-3">
                        <div id="opt-boy" onclick="selectGender('boy')" class="char-card p-2 flex flex-col items-center">
                            <div class="w-20 h-20 sm:w-24 sm:h-24 flex items-center justify-center mb-1">
                                {ricky_img_tag}
                            </div>
                            <span class="text-xs font-bold text-gray-300 font-dos">CHICO</span>
                        </div>
                        <div id="opt-girl" onclick="selectGender('girl')" class="char-card p-2 flex flex-col items-center">
                            <div class="w-20 h-20 sm:w-24 sm:h-24 flex items-center justify-center mb-1">
                                {ariana_img_tag}
                            </div>
                            <span class="text-xs font-bold text-gray-300 font-dos">CHICA</span>
                        </div>
                    </div>
                </div>
                <button id="btn-start-game" onclick="startGame()" disabled class="balatro-box bg-[#1b1e25] text-gray-500 w-full py-3.5 text-sm font-bold tracking-wider opacity-40 cursor-not-allowed font-balatro">
                    ENTRAR AL JUEGO
                </button>
            </div>

        </div>
    </div>

    <!-- BOTONES INFERIORES -->
    <div class="fixed bottom-3 left-3 z-40">
        <button onclick="toggleTutorial()" class="balatro-btn-blue text-xs sm:text-sm px-4 py-2 font-dos">
            💡 TUTO
        </button>
    </div>
    <div class="fixed bottom-3 right-3 z-40">
        <!-- RANK DESHABILITADO -->
        <button onclick="showRankNotice()" class="balatro-box bg-[#1b1e25] border-[#101318] text-gray-500 text-xs sm:text-sm px-4 py-2 cursor-pointer relative font-dos" title="Módulo en desarrollo por otro compañero">
            🏆 RANK
            <span class="absolute -top-2 -right-2 bg-yellow-500 text-black text-[9px] font-bold px-1 rounded-sm border border-black">DEV</span>
        </button>
    </div>

    <!-- PANEL TUTORIAL -->
    <div id="tutorial-panel" class="fixed left-0 top-0 h-full w-72 bg-[#1b1f26] border-r-4 border-[#121418] p-4 flex flex-col z-50 transform -translate-x-full transition-transform duration-300 shadow-2xl">
        <div class="flex justify-between items-center mb-4 border-b-2 border-white/10 pb-2">
            <div class="balatro-header-badge px-3 py-1 text-xs font-dos">CÓMO JUGAR</div>
            <button onclick="toggleTutorial()" class="text-white text-lg font-bold">✕</button>
        </div>
        <div class="balatro-box-inner p-3 text-2xl text-center mb-3">
            🍎🍉 <span class="text-red-400">+</span> 🍎🍌
        </div>
        <p class="text-xs text-yellow-300 text-center mb-3 font-dos">SACA LO QUE SE REPITE (🍎)</p>
        <div class="balatro-box-inner p-3 text-2xl text-center mb-4">
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
        <div class="balatro-box px-3.5 py-2 text-center min-w-[100px] sm:min-w-[130px]">
            <div class="text-xs text-gray-400 font-dos">NIVEL <span id="level-display" class="text-yellow-400 text-base font-dos">1</span></div>
            <div class="text-xs text-gray-300 mt-0.5 font-dos">RONDA <span id="round-display" class="text-white">1</span>/3</div>
        </div>

        <!-- 3 Comodines -->
        <div class="flex justify-center gap-1.5 sm:gap-2.5">
            <button id="btn-joker-reveal" onclick="useJoker('reveal')" title="Revelar factor" class="balatro-box p-2 sm:p-2.5 text-base sm:text-xl relative active:translate-y-1">
                👁️
                <span id="qty-reveal" class="absolute -top-2 -right-2 bg-red-600 text-white text-[10px] px-1.5 rounded-full border border-black font-dos">1</span>
            </button>
            <button id="btn-joker-reroll" onclick="useJoker('reroll')" title="Cambiar mano" class="balatro-box p-2 sm:p-2.5 text-base sm:text-xl relative active:translate-y-1">
                🎲
                <span id="qty-reroll" class="absolute -top-2 -right-2 bg-red-600 text-white text-[10px] px-1.5 rounded-full border border-black font-dos">1</span>
            </button>
            <!-- Comodín que salta UNA RONDA -->
            <button id="btn-joker-skip" onclick="useJoker('skip')" title="Saltar 1 Ronda" class="balatro-box p-2 sm:p-2.5 text-base sm:text-xl relative active:translate-y-1 opacity-40">
                ⏭️
                <span id="qty-skip" class="absolute -top-2 -right-2 bg-red-600 text-white text-[10px] px-1.5 rounded-full border border-black font-dos">0</span>
            </button>
        </div>

        <div class="balatro-box px-3.5 py-2 text-center min-w-[100px] sm:min-w-[130px]">
            <div class="text-xs text-gray-400 font-dos">PUNTOS</div>
            <div id="total-score" class="text-base sm:text-xl text-yellow-400 mt-0.5 font-dos font-bold">0</div>
            <div id="user-display-tag" class="text-[10px] text-gray-400 truncate max-w-[90px] mx-auto font-dos">JUGADOR</div>
        </div>
    </header>

    <!-- ÁREA DE CARTAS -->
    <main class="flex-grow flex flex-col items-center justify-center relative w-full max-w-5xl mx-auto my-auto">
        <div id="hand-container" class="flex justify-center items-center flex-wrap gap-2.5 sm:gap-4 w-full px-2 mb-6"></div>

        <button id="btn-play" onclick="playHand()" disabled class="balatro-box bg-[#1b1e25] text-gray-500 px-8 py-3.5 sm:px-12 sm:py-4 text-xs sm:text-sm tracking-widest opacity-40 cursor-not-allowed font-balatro">
            JUGAR MANO
        </button>

        <div id="flame-score-container" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 hidden opacity-0 transition-opacity duration-300 z-40 pointer-events-none text-center">
            <div id="flame-score" class="text-4xl sm:text-6xl score-flame tracking-wider drop-shadow-[0_0_35px_#ff4500]">0</div>
        </div>
    </main>

    <!-- MODAL FIN DE NIVEL -->
    <div id="level-modal" class="fixed inset-0 bg-black/85 z-50 hidden flex items-center justify-center backdrop-blur-sm p-4">
        <div class="balatro-box max-w-sm w-full p-6 text-center">
            <div class="balatro-header-badge py-2 px-4 mb-4 transform -rotate-1 inline-block w-full">
                <h2 class="text-xl sm:text-2xl font-balatro">NIVEL COMPLETADO</h2>
            </div>
            <div class="flex justify-center gap-3 my-4" id="modal-stars"></div>
            <p id="modal-desc" class="balatro-box-inner p-3 text-gray-200 text-xs leading-relaxed mb-5 font-dos"></p>
            <button onclick="nextLevel()" class="balatro-btn-orange w-full py-3.5 text-xs tracking-wider font-balatro">
                SIGUIENTE NIVEL ➔
            </button>
        </div>
    </div>

    <!-- ALERTA BALATRO -->
    <div id="alert-modal" class="fixed top-12 left-1/2 -translate-x-1/2 balatro-header-badge text-xs sm:text-sm px-5 py-3 z-50 hidden transition-opacity text-center max-w-[90vw] font-dos">
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

        // Reproducción de background.mp3
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
        function spawnParticles(x, y, count=30) {{
            const colors = ['#f1b31c', '#0077c8', '#ea2e35', '#ffffff'];
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
            btn.className = "balatro-btn-orange w-full py-3.5 text-sm font-bold tracking-wider cursor-pointer font-balatro";
            SFX.select();
        }}

        function startGame() {{
            if (!playerGender) return;
            document.getElementById('intro-modal').classList.add('hidden');
            document.getElementById('user-display-tag').textContent = `${{playerGender === 'boy' ? '👦' : '👧'}} ${{playerName}}`;
            
            SFX.winRound();
            startBackgroundMusic();
            startRound();
            updateUI();
        }}

        function showRankNotice() {{
            SFX.hover();
            showAlert("🏆 Módulo de Ranking en integración por compañero de equipo.");
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
            const suitColor = (suit === '♥' || suit === '♦') ? '#ea2e35' : '#0077c8';

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
                
                const cornerRank = getCardCornerRank(card);

                let lenClass = "len-1";
                const l = card.str.length;
                if(l === 2) lenClass = "len-2";
                else if(l === 3) lenClass = "len-3";
                else if(l === 4) lenClass = "len-4";
                else if(l === 5) lenClass = "len-5";
                else if(l > 5) lenClass = "len-many";

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
                btnPlay.className = "balatro-btn-orange px-8 py-3.5 sm:px-12 sm:py-4 text-xs sm:text-sm tracking-widest cursor-pointer font-balatro";
            }} else {{
                btnPlay.disabled = true;
                btnPlay.className = "balatro-box bg-[#1b1e25] text-gray-500 px-8 py-3.5 sm:px-12 sm:py-4 text-xs sm:text-sm tracking-widest opacity-40 cursor-not-allowed font-balatro";
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
                    starContainer.innerHTML += `<span class="text-yellow-400 text-3xl sm:text-4xl drop-shadow-[0_4px_0_#9e330e]">★</span>`;
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
                desc.innerHTML = `¡PRECISIÓN PERFECTA!<br>Ganaste un comodín SALTAR RONDA.<br>Bono: +${{bonusScore.toLocaleString()}} pts`;
            }} else {{
                desc.innerHTML = `Precisión: ${{Math.round(precision*100)}}%.<br>Bono obtenido: +${{bonusScore.toLocaleString()}} pts`;
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
