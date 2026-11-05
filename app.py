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
    page_title="BALAMATH | Factor Común IF0003",
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
        height: 100dvh !important;
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

# Fondos GIF
bg_game_b64 = get_base64_file("background_gif.gif") or get_base64_file("background.gif")
bg_reg_b64 = get_base64_file("background_gif_2.gif") or get_base64_file("background_2.gif") or bg_game_b64

# Audio
audio_bg_b64 = get_base64_file("background.mp3")

# Personajes
ricky_b64 = get_base64_file("ricky.png")
ariana_b64 = get_base64_file("ariana.png")

# Íconos de Comodines
joker_reveal_b64 = get_base64_file("joker_reveal.png")
joker_reroll_b64 = get_base64_file("joker_reroll.png")
joker_skip_b64 = get_base64_file("joker_skip.png")

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
        font-weight: normal;
        font-style: normal;
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

bg_game_tag = f'<img id="bg-game" class="screen-bg" style="display:none;" src="data:image/gif;base64,{bg_game_b64}" alt="Game BG" />' if bg_game_b64 else '<div id="bg-game" class="screen-bg procedural-game" style="display:none;"></div>'
bg_reg_tag = f'<img id="bg-reg" class="screen-bg" style="display:block;" src="data:image/gif;base64,{bg_reg_b64}" alt="Register BG" />' if bg_reg_b64 else '<div id="bg-reg" class="screen-bg procedural-reg" style="display:block;"></div>'

audio_html_tag = ""
if audio_bg_b64:
    audio_html_tag = f"""
    <audio id="bg-music" loop preload="auto" crossorigin="anonymous">
        <source src="data:audio/mp3;base64,{audio_bg_b64}" type="audio/mp3">
    </audio>
    """

ricky_img_tag = f'<img src="data:image/png;base64,{ricky_b64}" class="w-full h-full object-contain pixelated" alt="Ricky" />' if ricky_b64 else '<div class="text-xs font-hud font-bold">[CHICO]</div>'
ariana_img_tag = f'<img src="data:image/png;base64,{ariana_b64}" class="w-full h-full object-contain pixelated" alt="Ariana" />' if ariana_b64 else '<div class="text-xs font-hud font-bold">[CHICA]</div>'

reveal_icon_tag = f'<img src="data:image/png;base64,{joker_reveal_b64}" class="w-7 h-7 sm:w-9 sm:h-9 object-contain pixelated" alt="Revelar" />' if joker_reveal_b64 else '<span class="text-cyan-400 font-hud text-[12px]">👁</span>'
reroll_icon_tag = f'<img src="data:image/png;base64,{joker_reroll_b64}" class="w-7 h-7 sm:w-9 sm:h-9 object-contain pixelated" alt="Revolver" />' if joker_reroll_b64 else '<span class="text-purple-400 font-hud text-[12px]">⟲</span>'
skip_icon_tag = f'<img src="data:image/png;base64,{joker_skip_b64}" class="w-7 h-7 sm:w-9 sm:h-9 object-contain pixelated" alt="Saltar" />' if joker_skip_b64 else '<span class="text-yellow-400 font-hud text-[12px]">⏭</span>'

GAME_HTML = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>BALAMATH: Factor Común 8-Bit</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap" rel="stylesheet">
    
    <style>
        {font_face_css}

        :root {{
            --font-hud: 'Press Start 2P', monospace;
            --font-sub: 'VT323', monospace;
            --font-dos: 'DosVgaFont', 'Press Start 2P', monospace;
            --font-balatro: 'BalatroFont', 'Press Start 2P', sans-serif;
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

        html, body {{
            height: 100dvh;
            width: 100vw;
            margin: 0;
            padding: 0;
            overflow: hidden;
            user-select: none;
            background-color: transparent;
            color: #d8ceb9;
            font-family: var(--font-hud);
        }}

        body {{
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .font-hud {{ font-family: var(--font-hud); }}
        .font-sub {{ font-family: var(--font-sub); }}
        .font-dos {{ font-family: var(--font-dos); }}
        .font-balatro {{ font-family: var(--font-balatro); }}

        /* FONDOS */
        .screen-bg {{
            position: fixed;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            z-index: 0;
            object-fit: cover;
            pointer-events: none;
            image-rendering: pixelated;
        }}

        #bg-reg {{
            filter: brightness(1.20);
        }}

        .procedural-reg {{ background: radial-gradient(circle at center, #262e3d, #0d121a); }}
        .procedural-game {{ background: radial-gradient(circle at center, #1b3d2b, #050c07); }}

        .bg-dark-overlay {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: 
                linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.38) 50%),
                radial-gradient(circle at center, rgba(14, 11, 22, 0.32) 0%, rgba(2, 3, 5, 0.88) 100%);
            background-size: 100% 4px, 100% 100%;
            pointer-events: none;
            z-index: 1;
        }}

        /* PANELES DARK FANTASY RECTOS */
        .pixel-df-panel {{
            background: #11141c;
            border: 3px solid #000000;
            box-shadow: 
                inset 3px 3px 0 #2e3648,
                inset -3px -3px 0 #08090d,
                0 0 0 2px #3c2a1e,
                0 6px 0 #000000;
            position: relative;
        }}

        .pixel-df-slot {{
            background: #080a0e;
            border: 2px solid #000000;
            box-shadow: 
                inset 2px 2px 0 #000000,
                inset -2px -2px 0 #1b202c;
        }}

        .pixel-df-banner-crimson {{
            background: linear-gradient(180deg, #9b1c24 0%, #590d12 100%);
            border: 3px solid #000000;
            box-shadow: 
                inset 3px 3px 0 #d9434d,
                inset -3px -3px 0 #280306,
                0 0 0 1px #ff8a7a,
                0 5px 0 #000000;
            color: #f7e8ce;
            text-shadow: 2px 2px 0 #000000;
            transform: none !important;
        }}

        .pixel-df-btn-flame {{
            font-family: var(--font-hud);
            background: linear-gradient(180deg, #d35422 0%, #872506 100%);
            border: 3px solid #000000;
            box-shadow: 
                inset 3px 3px 0 #ff8a50,
                inset -3px -3px 0 #3a0e02,
                0 0 0 2px #d4a340,
                0 6px 0 #000000;
            color: #ffffff;
            text-shadow: 2px 2px 0 #000000;
            transition: transform 0.05s steps(2), box-shadow 0.05s steps(2);
            cursor: pointer;
        }}
        .pixel-df-btn-flame:active {{
            transform: translateY(4px);
            box-shadow: 
                inset 3px 3px 0 #3a0e02,
                inset -3px -3px 0 #ff8a50,
                0 0 0 2px #d4a340,
                0 2px 0 #000000;
        }}

        .pixel-df-btn-arcane {{
            font-family: var(--font-hud);
            background: #172233;
            border: 2px solid #000000;
            box-shadow: 
                inset 2px 2px 0 #384e6f,
                inset -2px -2px 0 #090e17,
                0 4px 0 #000000;
            color: #a7c8e8;
            text-shadow: 2px 2px 0 #000000;
            transition: transform 0.05s steps(2);
        }}
        .pixel-df-btn-arcane:active {{
            transform: translateY(2px);
            box-shadow: inset 2px 2px 0 #090e17, inset -2px -2px 0 #384e6f, 0 2px 0 #000;
        }}

        /* COMODINES: 10% MÁS GRANDES (49px en PC, 40px en móvil) */
        .btn-relic-slot {{
            background: #131720;
            border: 2px solid #000000;
            box-shadow: 
                inset 2px 2px 0 #2d3648,
                inset -2px -2px 0 #06070a,
                0 4px 0 #000000;
            transition: transform 0.05s steps(2);
            width: 49px;
            height: 49px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .btn-relic-slot:hover {{ border-color: #d4a340; }}
        .btn-relic-slot:active {{
            transform: translateY(2px);
            box-shadow: inset 2px 2px 0 #06070a, inset -2px -2px 0 #2d3648, 0 2px 0 #000000;
        }}

        .char-slot-crypt {{
            background: #090c12;
            border: 2px solid #000000;
            box-shadow: 
                inset 2px 2px 0 #1b212e,
                inset -2px -2px 0 #040507,
                0 3px 0 #000;
            cursor: pointer;
            transition: transform 0.08s steps(2);
        }}
        .char-slot-crypt.selected {{
            border-color: #d4a340;
            background: #1b2230;
            box-shadow: inset 0 0 0 2px #d4a340, 0 0 8px rgba(212, 163, 64, 0.4), 0 4px 0 #000000;
        }}

        /* CARTAS BALATRO ORIGINALES */
        .card-8bit {{
            width: 104px;
            height: 150px;
            background: var(--color-card-cream);
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

        .card-frame-inner {{
            position: absolute;
            top: 4px; left: 4px; right: 4px; bottom: 4px;
            border: 2px solid #ccc0a2;
            pointer-events: none;
        }}

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

        .corner-text {{ font-size: 13px; font-weight: bold; letter-spacing: -0.5px; }}
        .corner-suit-icon {{ font-size: 11px; margin-top: 1px; }}

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
            transform: translateY(-12px) !important;
            animation-play-state: paused;
            box-shadow: inset 3px 3px 0 #ffffff, inset -3px -3px 0 #b3a992, 0 12px 0 #000000;
            z-index: 20;
        }}
        .card-8bit.selected {{
            transform: translateY(-20px) !important;
            animation-play-state: paused;
            border-color: #f1b31c;
            box-shadow: 
                inset 3px 3px 0 #fff7b8,
                inset -3px -3px 0 #ab7c07,
                0 0 0 3px #f1b31c,
                0 12px 0 #000000 !important;
            z-index: 30;
        }}

        /* RESPONSIVIDAD PARA TELÉFONOS */
        @media (max-width: 640px) {{
            .card-8bit {{
                width: 68px !important;
                height: 98px !important;
                border-width: 3px !important;
                box-shadow: inset 2px 2px 0 #fff, inset -2px -2px 0 #b3a992, 0 4px 0 #000 !important;
            }}
            .card-8bit.selected {{
                transform: translateY(-12px) !important;
                box-shadow: inset 2px 2px 0 #fff7b8, inset -2px -2px 0 #ab7c07, 0 0 0 2px #f1b31c, 0 8px 0 #000 !important;
            }}
            .card-8bit:hover {{
                transform: translateY(-6px) !important;
            }}
            .len-1 {{ font-size: 1.25rem !important; }}
            .len-2 {{ font-size: 1.1rem !important; }}
            .len-3 {{ font-size: 0.95rem !important; }}
            .len-4 {{ font-size: 0.8rem !important; }}
            .len-5 {{ font-size: 0.7rem !important; }}
            .len-many {{ font-size: 0.6rem !important; }}
            .corner-text {{ font-size: 9px !important; }}
            .corner-suit-icon {{ font-size: 8px !important; }}
            .pip-corner-tl {{ top: 2px !important; left: 3px !important; }}
            .pip-corner-br {{ bottom: 2px !important; right: 3px !important; }}
            #hand-container {{ gap: 6px !important; min-height: 120px !important; margin-bottom: 10px !important; }}
            .btn-relic-slot {{ width: 40px !important; height: 40px !important; }}
        }}

        @keyframes flame-flicker-8bit {{
            0%, 100% {{ transform: scale(1); filter: brightness(1); }}
            50% {{ transform: scale(1.12); filter: brightness(1.25); }}
        }}
        .score-flame {{
            color: #ffe6a3;
            font-family: var(--font-hud);
            text-shadow: 3px 3px 0 #9e1a22, -3px -3px 0 #d85a1a, 0 0 12px rgba(216, 90, 26, 0.8);
            animation: flame-flicker-8bit 0.25s steps(2) infinite;
        }}

        @keyframes shake-8bit {{
            0%, 100% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-8px); }}
            75% {{ transform: translateX(8px); }}
        }}
        .animate-shake {{ animation: shake-8bit 0.22s steps(4); }}

        #fx-canvas {{ position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 50; }}

        #fade-overlay {{
            position: fixed;
            inset: 0;
            background: #000;
            opacity: 0;
            pointer-events: none;
            z-index: 9999;
            transition: opacity 0.4s steps(4);
        }}
    </style>
</head>
<body class="p-2 sm:p-4">
    {bg_reg_tag}
    {bg_game_tag}
    {audio_html_tag}
    <div class="bg-dark-overlay"></div>
    <canvas id="fx-canvas"></canvas>
    <div id="fade-overlay"></div>

    <!-- INTRO / REGISTRO BALAMATH -->
    <div id="intro-modal" class="fixed inset-0 z-[1000] flex items-center justify-center p-3 sm:p-4">
        <div class="pixel-df-panel max-w-xs sm:max-w-sm w-full p-4 sm:p-6 text-center">
            
            <div class="pixel-df-banner-crimson py-2.5 px-3 mb-4 inline-block w-full">
                <h1 class="text-sm sm:text-base tracking-widest font-hud text-[#fff1d0]">BALAMATH</h1>
                <p class="text-[7px] sm:text-[8px] opacity-90 tracking-widest mt-1 font-hud text-amber-200">FACTOR COMÚN • UCR IF0003</p>
            </div>
            
            <!-- PASO 1: NOMBRE -->
            <div id="step-name">
                <div class="pixel-df-slot p-3 mb-4 text-left">
                    <label class="block text-[8px] sm:text-[9px] text-[#a99878] mb-1.5 tracking-wider font-hud">APODO DEL JUGADOR:</label>
                    <input type="text" id="username-input" class="w-full bg-[#050608] border-2 border-[#333d4f] text-[#d4a340] p-2.5 text-center uppercase tracking-wider text-xs sm:text-sm font-bold font-hud outline-none focus:border-[#d4a340]" placeholder="TU NOMBRE" maxlength="12">
                </div>
                <button onclick="goToGenderStep()" class="pixel-df-btn-flame w-full py-3.5 text-xs font-bold tracking-wider">
                    CONTINUAR ➔
                </button>
            </div>

            <!-- PASO 2: SELECCIÓN DE PERSONAJE -->
            <div id="step-gender" class="hidden">
                <div class="pixel-df-slot p-2 sm:p-3 mb-3 text-center">
                    <p class="text-[8px] sm:text-[9px] text-[#d4a340] font-hud mb-2 tracking-wider">ELIGE TU PERSONAJE</p>
                    <div class="grid grid-cols-2 gap-2 sm:gap-3">
                        <div id="opt-boy" onclick="selectGender('boy')" class="char-slot-crypt p-1.5 flex flex-col items-center">
                            <div class="w-16 h-16 sm:w-20 sm:h-20 flex items-center justify-center mb-1">
                                {ricky_img_tag}
                            </div>
                            <span class="text-[8px] sm:text-[9px] font-bold text-gray-300 font-hud">[CHICO]</span>
                        </div>
                        <div id="opt-girl" onclick="selectGender('girl')" class="char-slot-crypt p-1.5 flex flex-col items-center">
                            <div class="w-16 h-16 sm:w-20 sm:h-20 flex items-center justify-center mb-1">
                                {ariana_img_tag}
                            </div>
                            <span class="text-[8px] sm:text-[9px] font-bold text-gray-300 font-hud">[CHICA]</span>
                        </div>
                    </div>
                </div>
                <button id="btn-start-game" onclick="startGameWithTransition()" disabled class="pixel-df-panel bg-[#0d0f14] text-stone-600 w-full py-3 text-xs font-bold tracking-wider opacity-40 cursor-not-allowed">
                    ENTRAR AL JUEGO ➔
                </button>
            </div>

        </div>
    </div>

    <!-- CONTENIDO DEL JUEGO -->
    <div id="game-ui" class="hidden flex flex-col justify-between h-full w-full relative z-10">
        <!-- BOTONES INFERIORES -->
        <div class="fixed bottom-2 sm:bottom-3 left-2 sm:left-3 z-40 flex gap-2">
            <button onclick="toggleTutorial()" class="pixel-df-btn-arcane text-[8px] sm:text-xs px-2.5 sm:px-3.5 py-1.5 sm:py-2 font-hud">
                [ ? ] TUTO
            </button>
            <button id="btn-audio-mute" onclick="toggleMute()" class="pixel-df-btn-arcane text-[8px] sm:text-xs px-2 sm:px-3 py-1.5 sm:py-2 font-hud">
                [♪ MUTE]
            </button>
        </div>

        <div class="fixed bottom-2 sm:bottom-3 right-2 sm:right-3 z-40">
            <button onclick="showRankNotice()" class="pixel-df-panel bg-[#0d1017] text-stone-400 text-[8px] sm:text-xs px-2.5 sm:px-3.5 py-1.5 sm:py-2 cursor-pointer relative font-hud">
                [ RANK ]
                <span class="absolute -top-2 -right-2 bg-[#8b1820] text-amber-200 text-[7px] font-bold px-1 py-0.5 border border-black">DEV</span>
            </button>
        </div>

        <!-- PANEL TUTORIAL -->
        <div id="tutorial-panel" class="fixed left-0 top-0 h-full w-72 sm:w-80 bg-[#0d1017] border-r-4 border-black p-3 sm:p-4 flex flex-col z-50 transform -translate-x-full transition-transform duration-200 shadow-2xl overflow-y-auto">
            <div class="flex justify-between items-center mb-3 border-b-2 border-[#2b3548] pb-2">
                <div class="pixel-df-banner-crimson px-2.5 py-1 text-[8px] sm:text-[9px] font-hud">GUÍA FACTORIZACIÓN</div>
                <button onclick="toggleTutorial()" class="text-amber-200 text-xs font-bold font-hud hover:text-white">[ ✕ ]</button>
            </div>
            
            <div class="pixel-df-slot p-2 sm:p-3 text-xl sm:text-2xl text-center mb-2 font-sub text-stone-200">
                4x² + 6x
            </div>
            <p class="text-[8px] text-[#d4a340] text-center mb-3 font-hud">MCD = 2 | VARIABLE = x</p>
            <div class="pixel-df-slot p-2 sm:p-3 text-xl sm:text-2xl text-center mb-3 font-sub text-emerald-400 border border-emerald-900/60">
                2x · (2x + 3)
            </div>

            <div class="text-xs sm:text-sm text-stone-300 leading-snug font-sub space-y-2">
                <p>1. Selecciona 2 o más cartas que compartan divisores o variables comunes.</p>
                <p>2. Presiona "JUGAR MANO" para acumular fichas multiplicadas.</p>
                <p>3. Las cartas no seleccionadas permanecen en tu mano para la siguiente ronda.</p>
            </div>
        </div>

        <!-- HEADER SUPERIOR -->
        <header class="flex justify-between items-center z-10 max-w-5xl mx-auto w-full gap-1.5 sm:gap-2 px-1 pt-1">
            <div class="pixel-df-panel px-2 sm:px-3 py-1.5 sm:py-2 text-center min-w-[85px] sm:min-w-[130px] flex flex-col items-center justify-center">
                <span class="text-[7px] sm:text-[9px] text-[#8e98aa] font-hud tracking-wider">NIVEL</span>
                <span id="level-display" class="text-sm sm:text-2xl text-[#d4a340] font-hud font-bold leading-tight my-0.5">1</span>
                <span class="text-[6px] sm:text-[8px] text-[#c8b99c] font-hud tracking-wider">RONDA <span id="round-display" class="text-white">1</span>/3</span>
            </div>

            <!-- COMODINES: 10% MÁS GRANDES -->
            <div class="flex justify-center gap-2 sm:gap-3">
                <button id="btn-joker-reveal" onclick="useJoker('reveal')" title="Revelar factor" class="btn-relic-slot relative">
                    {reveal_icon_tag}
                    <span id="qty-reveal" class="absolute -top-1.5 -right-1.5 bg-[#8b1820] text-amber-200 text-[7px] sm:text-[8px] px-1 py-0.5 border border-black font-hud">1</span>
                </button>
                <button id="btn-joker-reroll" onclick="useJoker('reroll')" title="Cambiar mano" class="btn-relic-slot relative">
                    {reroll_icon_tag}
                    <span id="qty-reroll" class="absolute -top-1.5 -right-1.5 bg-[#51237a] text-purple-200 text-[7px] sm:text-[8px] px-1 py-0.5 border border-black font-hud">1</span>
                </button>
                <button id="btn-joker-skip" onclick="useJoker('skip')" title="Saltar 1 Ronda" class="btn-relic-slot relative opacity-40">
                    {skip_icon_tag}
                    <span id="qty-skip" class="absolute -top-1.5 -right-1.5 bg-[#8b6508] text-amber-100 text-[7px] sm:text-[8px] px-1 py-0.5 border border-black font-hud">0</span>
                </button>
            </div>

            <div class="pixel-df-panel px-2 sm:px-3 py-1.5 sm:py-2 text-center min-w-[85px] sm:min-w-[130px] flex flex-col items-center justify-center">
                <span class="text-[7px] sm:text-[9px] text-[#8e98aa] font-hud tracking-wider">PUNTOS</span>
                <span id="total-score" class="text-xs sm:text-xl text-[#d4a340] font-hud font-bold leading-tight my-0.5">0</span>
                <span id="user-display-tag" class="text-[6px] sm:text-[8px] text-[#c8b99c] font-hud truncate max-w-[70px] sm:max-w-[95px]">JUGADOR</span>
            </div>
        </header>

        <!-- ÁREA CENTRAL DE CARTAS -->
        <main class="flex-grow flex flex-col items-center justify-center relative w-full max-w-5xl mx-auto my-auto px-1">
            <div id="hand-container" class="flex justify-center items-center flex-wrap w-full px-1 mb-3 sm:mb-6"></div>

            <button id="btn-play" onclick="playHand()" disabled class="pixel-df-panel bg-[#0d0f14] text-stone-600 px-6 py-2.5 sm:px-12 sm:py-4 text-xs sm:text-sm tracking-widest opacity-40 cursor-not-allowed font-hud">
                JUGAR MANO
            </button>

            <div id="flame-score-container" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 hidden opacity-0 transition-opacity duration-200 z-40 pointer-events-none text-center">
                <div id="flame-score" class="text-2xl sm:text-5xl score-flame tracking-wider">0</div>
            </div>
        </main>
    </div>

    <!-- MODAL FIN DE NIVEL -->
    <div id="level-modal" class="fixed inset-0 bg-black/90 z-50 hidden flex items-center justify-center p-3 sm:p-4">
        <div class="pixel-df-panel max-w-xs sm:max-w-sm w-full p-4 sm:p-6 text-center">
            
            <div class="pixel-df-banner-crimson py-2.5 px-3 mb-3 inline-block w-full">
                <h2 class="text-xs sm:text-sm font-bold tracking-wider font-hud">NIVEL COMPLETADO</h2>
            </div>
            
            <div class="flex justify-center gap-2 sm:gap-3 my-2 text-xl sm:text-3xl font-hud" id="modal-stars"></div>
            
            <div class="pixel-df-slot p-2.5 sm:p-3 text-stone-200 mb-4 font-sub text-base sm:text-xl leading-snug text-left">
                <div id="modal-desc" class="space-y-1"></div>
            </div>
            
            <button onclick="nextLevelWithTransition()" class="pixel-df-btn-flame w-full py-3.5 text-xs sm:text-sm tracking-wider font-hud">
                SIGUIENTE NIVEL ➔
            </button>
        </div>
    </div>

    <!-- MODAL DERROTA (GAME OVER TRAS 5 ERRORES SEGUIDOS) -->
    <div id="gameover-modal" class="fixed inset-0 bg-black/95 z-50 hidden flex items-center justify-center p-3 sm:p-4">
        <div class="pixel-df-panel max-w-xs sm:max-w-sm w-full p-4 sm:p-6 text-center border-red-700">
            <div class="pixel-df-banner-crimson py-2.5 px-3 mb-3 inline-block w-full bg-gradient-to-b from-red-900 to-black">
                <h2 class="text-xs sm:text-sm font-bold tracking-wider font-hud text-red-200">SIN INTENTOS</h2>
            </div>
            <div class="pixel-df-slot p-3 text-stone-300 mb-4 font-sub text-base sm:text-lg text-center leading-snug">
                Has acumulado <span class="text-red-400 font-bold font-hud">5 FALLOS</span> consecutivos sin hallar factor común.
            </div>
            <button onclick="retryCurrentLevel()" class="pixel-df-btn-flame w-full py-3.5 text-xs sm:text-sm tracking-wider font-hud">
                REINTENTAR NIVEL ➔
            </button>
        </div>
    </div>

    <!-- NOTIFICACIONES CENTRADAS, DURACIÓN CORTA Y DISMISS AL TOCAR -->
    <div id="alert-modal" onclick="dismissAlert()" class="fixed top-[35%] left-1/2 -translate-x-1/2 -translate-y-1/2 pixel-df-banner-crimson text-[9px] sm:text-xs px-5 py-3 z-50 hidden text-center max-w-[85vw] font-hud cursor-pointer shadow-2xl transition-opacity duration-150">
        <span id="alert-text"></span>
    </div>

    <script>
        let aCtx = null;
        let bgAudioEl = document.getElementById('bg-music');
        let bgSourceNode = null;
        let convolverNode = null;
        let lowPassNode = null;
        let highPassNode = null;
        let dryGain = null;
        let wetGain = null;
        let masterMusicGain = null;
        let isMuted = false;

        // Volumen reducido un 25% (0.45 * 0.75 = 0.3375)
        const DEFAULT_VOLUME = 0.3375;

        function buildImpulseResponse(duration = 2.4, decay = 3.2) {{
            const rate = aCtx.sampleRate;
            const length = rate * duration;
            const impulse = aCtx.createBuffer(2, length, rate);
            const left = impulse.getChannelData(0);
            const right = impulse.getChannelData(1);
            for (let i = 0; i < length; i++) {{
                const n = i / length;
                const e = Math.exp(-n * decay);
                left[i] = ((Math.random() * 2) - 1) * e;
                right[i] = ((Math.random() * 2) - 1) * e;
            }}
            return impulse;
        }}

        function initAudioEngine() {{
            if (aCtx) return;
            try {{
                aCtx = new (window.AudioContext || window.webkitAudioContext)();
                if (bgAudioEl) {{
                    bgSourceNode = aCtx.createMediaElementSource(bgAudioEl);

                    // Filtros para efecto teléfono/atrapado
                    highPassNode = aCtx.createBiquadFilter();
                    highPassNode.type = 'highpass';
                    highPassNode.frequency.setValueAtTime(480, aCtx.currentTime); // Corta graves

                    lowPassNode = aCtx.createBiquadFilter();
                    lowPassNode.type = 'lowpass';
                    lowPassNode.frequency.setValueAtTime(2800, aCtx.currentTime); // Corta agudos / encerrado
                    lowPassNode.Q.setValueAtTime(1.5, aCtx.currentTime);

                    convolverNode = aCtx.createConvolver();
                    convolverNode.buffer = buildImpulseResponse(2.4, 3.2);

                    dryGain = aCtx.createGain();
                    wetGain = aCtx.createGain();
                    masterMusicGain = aCtx.createGain();

                    masterMusicGain.gain.setValueAtTime(DEFAULT_VOLUME, aCtx.currentTime);

                    // Cadena de enrutamiento
                    bgSourceNode.connect(highPassNode);
                    highPassNode.connect(lowPassNode);

                    // Señal seca
                    lowPassNode.connect(dryGain);
                    // Señal con reverb
                    lowPassNode.connect(convolverNode);
                    convolverNode.connect(wetGain);

                    dryGain.connect(masterMusicGain);
                    wetGain.connect(masterMusicGain);

                    masterMusicGain.connect(aCtx.destination);
                    
                    setCryptAudioMode(true);
                }}
            }} catch(e) {{}}
        }}

        function setCryptAudioMode(enabled) {{
            if (!aCtx || !bgAudioEl) return;
            const now = aCtx.currentTime;
            if (enabled) {{
                bgAudioEl.playbackRate = 0.78;
                // Efecto teléfono (480Hz - 2800Hz)
                highPassNode.frequency.setValueAtTime(480, now);
                lowPassNode.frequency.setValueAtTime(2800, now);
                dryGain.gain.setValueAtTime(0.40, now);
                // 40% menos de reverb (0.85 * 0.60 = 0.51)
                wetGain.gain.setValueAtTime(0.51, now);
            }} else {{
                bgAudioEl.playbackRate = 1.0;
                // Plano/completo para el juego
                highPassNode.frequency.setValueAtTime(20, now);
                lowPassNode.frequency.setValueAtTime(20000, now);
                dryGain.gain.setValueAtTime(1.0, now);
                wetGain.gain.setValueAtTime(0.0, now);
            }}
        }}

        function toggleMute() {{
            isMuted = !isMuted;
            const btn = document.getElementById('btn-audio-mute');
            if (masterMusicGain) {{
                masterMusicGain.gain.setValueAtTime(isMuted ? 0 : DEFAULT_VOLUME, aCtx.currentTime);
            }} else if (bgAudioEl) {{
                bgAudioEl.muted = isMuted;
            }}
            btn.textContent = isMuted ? "[♪ PLAY]" : "[♪ MUTE]";
        }}

        function playTone(freq, type, dur, vol=0.1) {{
            try {{
                if (!aCtx) aCtx = new (window.AudioContext || window.webkitAudioContext)();
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
            hover: () => playTone(300, 'sine', 0.08, 0.04),
            select: () => playTone(510, 'triangle', 0.12, 0.12),
            error: () => {{ playTone(120, 'sawtooth', 0.25, 0.25); setTimeout(() => playTone(80, 'sawtooth', 0.35, 0.25), 100); }},
            flamePop: () => {{ playTone(170, 'sawtooth', 0.28, 0.25); setTimeout(() => playTone(230, 'sawtooth', 0.2, 0.2), 60); }},
            star: () => {{ playTone(860, 'sine', 0.3, 0.2); setTimeout(()=>playTone(1080, 'sine', 0.4, 0.2), 100); }},
            discard: () => playTone(220, 'triangle', 0.15, 0.15),
            winRound: () => {{ playTone(420, 'sine', 0.3, 0.2); setTimeout(() => playTone(630, 'sine', 0.3, 0.2), 150); }}
        }};

        window.addEventListener('click', function initPlay() {{
            initAudioEngine();
            if (bgAudioEl && bgAudioEl.paused && !isMuted) {{
                bgAudioEl.play().catch(() => {{}});
            }}
            window.removeEventListener('click', initPlay);
        }}, {{ once: true }});

        const cvs = document.getElementById('fx-canvas'); const ctx = cvs.getContext('2d');
        let particles = [];
        window.onresize = () => {{ cvs.width = window.innerWidth; cvs.height = window.innerHeight; }};
        window.onresize();

        function spawnParticles(x, y, count=35) {{
            const colors = ['#f4b41b', '#1b629b', '#c92a35', '#ffffff'];
            for(let i=0; i<count; i++) {{
                const angle = Math.random() * Math.PI * 2; const speed = 2 + Math.random() * 7;
                particles.push({{ x, y, vx: Math.cos(angle)*speed, vy: Math.sin(angle)*speed-2, color: colors[Math.floor(Math.random()*colors.length)], size: 4, life: 1.0, decay: 0.03 }});
            }}
        }}

        function spawnSkipParticles() {{
            const colors = ['#9e1a22', '#d4a340', '#ff4d4d', '#ffdb70', '#ffffff'];
            const w = window.innerWidth;
            const h = window.innerHeight;
            for(let i=0; i<90; i++) {{
                const angle = (Math.PI * 1.5) + (Math.random() - 0.5) * 1.4;
                const speed = 4 + Math.random() * 9;
                particles.push({{
                    x: Math.random() * w,
                    y: h + 10,
                    vx: Math.cos(angle) * speed,
                    vy: Math.sin(angle) * speed,
                    color: colors[Math.floor(Math.random() * colors.length)],
                    size: Math.floor(Math.random() * 5) + 3,
                    life: 1.0,
                    decay: 0.018
                }});
            }}
        }}

        function renderParticles() {{
            ctx.clearRect(0,0,cvs.width,cvs.height);
            for(let i=particles.length-1; i>=0; i--) {{
                const p = particles[i];
                p.x += p.vx; p.y += p.vy; p.vy += 0.14; p.life -= p.decay;
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
            btn.className = "pixel-df-btn-flame w-full py-3 text-xs font-bold tracking-wider cursor-pointer";
            SFX.select();
        }}

        function startGameWithTransition() {{
            if (!playerGender) return;
            SFX.winRound();

            const fade = document.getElementById('fade-overlay');
            fade.style.opacity = '1';

            setTimeout(() => {{
                document.getElementById('intro-modal').classList.add('hidden');
                document.getElementById('game-ui').classList.remove('hidden');
                document.getElementById('user-display-tag').textContent = `${{playerGender === 'boy' ? '[CHICO]' : '[CHICA]'}} ${{playerName}}`;
                
                const bgReg = document.getElementById('bg-reg');
                const bgGame = document.getElementById('bg-game');
                if (bgReg) bgReg.style.display = 'none';
                if (bgGame) bgGame.style.display = 'block';

                setCryptAudioMode(false);

                startRound();
                updateUI();

                setTimeout(() => {{
                    fade.style.opacity = '0';
                }}, 150);
            }}, 400);
        }}

        function showRankNotice() {{
            SFX.hover();
            showAlert("[RANKING EN DESARROLLO]");
        }}

        function toggleTutorial() {{
            SFX.hover();
            document.getElementById('tutorial-panel').classList.toggle('-translate-x-full');
        }}

        /* ========================================================
           ESTADO Y DIFICULTAD (+18% MÁS EXIGENTE ENTRE NIVELES)
           ======================================================== */
        let level = 1;
        let round = 1;
        let score = 0;
        let hand = [];
        let nextCardId = 0;
        let consecutiveErrors = 0; // Rastreador de fallos seguidos
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
            // Escalamiento +18% más agresivo de coeficientes y exponentes
            let maxCoef = Math.max(4, Math.floor(level * 3.54));
            let maxX = Math.min(4, Math.ceil(level * 0.59));
            let maxY = level > 2 ? Math.min(3, Math.floor(level * 0.39)) : 0;

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
            const suitColor = (suit === '♥' || suit === '♦') ? '#c92a35' : '#1b629b';

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
            
            // Mayor variabilidad y menor probabilidad de mano regalada
            if(Math.random() < 0.18) forceFactor = null;
            let forceCount = forceFactor ? (Math.floor(Math.random() * 3) + 3) : 0;

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
                btnPlay.className = "pixel-df-btn-flame px-6 py-2.5 sm:px-12 sm:py-4 text-xs sm:text-sm tracking-widest cursor-pointer";
            }} else {{
                btnPlay.disabled = true;
                btnPlay.className = "pixel-df-panel bg-[#0d0f14] text-stone-600 px-6 py-2.5 sm:px-12 sm:py-4 text-xs sm:text-sm tracking-widest opacity-40 cursor-not-allowed font-hud";
            }}
        }}

        function playHand() {{
            const selected = hand.filter(c => c.selected);
            const info = getCommonFactorInfo(selected);

            if(selected.length < 2 || !info || !info.isValid) {{
                SFX.error();
                handContainer.classList.add('animate-shake');
                levelStats.errors++;
                consecutiveErrors++;
                setTimeout(() => handContainer.classList.remove('animate-shake'), 250);

                // Sistema de 5 oportunidades
                if(consecutiveErrors >= 5) {{
                    triggerGameOver();
                    return;
                }} else if(consecutiveErrors === 3) {{
                    showAlert("¡CUIDADO! TE QUEDAN 2 INTENTOS");
                }} else if(consecutiveErrors === 4) {{
                    showAlert("¡PELIGRO! TE QUEDA 1 INTENTO");
                }}

                return;
            }}

            // Mano válida: resetea errores consecutivos
            consecutiveErrors = 0;
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

        function triggerGameOver() {{
            setCryptAudioMode(true);
            document.getElementById('gameover-modal').classList.remove('hidden');
        }}

        function retryCurrentLevel() {{
            document.getElementById('gameover-modal').classList.add('hidden');
            consecutiveErrors = 0;
            round = 1;
            hand = [];
            levelStats = {{ optimalPossible: 0, actualCorrect: 0, errors: 0 }};
            setCryptAudioMode(false);
            startRound();
            showAlert("[NIVEL REINICIADO]");
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

            setCryptAudioMode(true);

            starContainer.innerHTML = '';
            for(let i=0; i<3; i++) {{
                setTimeout(() => SFX.star(), i * 250);
                if(i < stars) {{
                    starContainer.innerHTML += `<span class="text-[#d4a340] drop-shadow-[0_2px_0_#000]">★</span>`;
                }} else {{
                    starContainer.innerHTML += `<span class="text-stone-700">☆</span>`;
                }}
            }}

            let bonusScore = stars * 1000 * level;
            score += bonusScore;
            document.getElementById('total-score').textContent = score.toLocaleString();

            let bonusItemText = "";
            if(stars === 3) {{
                comodines.skip++;
                updateUI();
                bonusItemText = `<div class="text-emerald-400 font-bold">[+] COMODÍN "SALTAR" DESBLOQUEADO</div>`;
            }}

            desc.innerHTML = `
                <div class="flex justify-between border-b border-[#2b3548] pb-1">
                    <span>PRECISIÓN DE MANO:</span>
                    <span class="text-[#d4a340] font-bold">${{Math.round(precision * 100)}}%</span>
                </div>
                <div class="flex justify-between border-b border-[#2b3548] py-1">
                    <span>BONO POR ESTRELLAS:</span>
                    <span class="text-emerald-400 font-bold">+${{bonusScore.toLocaleString()}} PTS</span>
                </div>
                <div class="pt-1">
                    ${{bonusItemText}}
                </div>
            `;

            modal.classList.remove('hidden');
        }}

        // Transición cinemática idéntica a la inicial al pasar de nivel
        function nextLevelWithTransition() {{
            const fade = document.getElementById('fade-overlay');
            fade.style.opacity = '1';

            setTimeout(() => {{
                document.getElementById('level-modal').classList.add('hidden');
                setCryptAudioMode(false);
                level++;
                round = 1;
                hand = [];
                consecutiveErrors = 0;
                levelStats = {{ optimalPossible: 0, actualCorrect: 0, errors: 0 }};
                startRound();

                setTimeout(() => {{
                    fade.style.opacity = '0';
                }}, 150);
            }}, 400);
        }}

        function updateUI() {{
            document.getElementById('qty-reveal').textContent = comodines.reveal;
            document.getElementById('qty-reroll').textContent = comodines.reroll;
            document.getElementById('qty-skip').textContent = comodines.skip;
            
            document.getElementById('btn-joker-reveal').style.opacity = comodines.reveal > 0 ? '1' : '0.4';
            document.getElementById('btn-joker-reroll').style.opacity = comodines.reroll > 0 ? '1' : '0.4';
            document.getElementById('btn-joker-skip').style.opacity = comodines.skip > 0 ? '1' : '0.4';
        }}

        let alertTimeout = null;

        function showAlert(msg) {{
            const el = document.getElementById('alert-modal');
            document.getElementById('alert-text').innerHTML = msg;
            
            if (alertTimeout) clearTimeout(alertTimeout);
            
            el.classList.remove('hidden');
            el.style.opacity = '1';

            // Duración más corta (1.6 segundos)
            alertTimeout = setTimeout(() => {{
                dismissAlert();
            }}, 1600);
        }}

        function dismissAlert() {{
            const el = document.getElementById('alert-modal');
            el.style.opacity = '0';
            setTimeout(() => {{
                el.classList.add('hidden');
            }}, 150);
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
                    showAlert(`[FACTOR]: ${{bestFactor}} (${{maxSubset}} CARTAS)`);
                }} else {{
                    showAlert(`[SIN FACTOR COMÚN]`);
                }}
            }} 
            else if (type === 'reroll') {{
                comodines.reroll--;
                SFX.discard();
                hand = [];
                startRound();
                showAlert("[MANO REVOLVIDA]");
            }}
            else if (type === 'skip') {{
                comodines.skip--;
                SFX.winRound();
                spawnSkipParticles();
                showAlert("[RONDA SALTADA]");
                
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
