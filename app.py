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

# Fondos GIF por estado (Se mantienen exactamente iguales)
bg_game_b64 = get_base64_file("background_gif.gif") or get_base64_file("background.gif")
bg_reg_b64 = get_base64_file("background_gif_2.gif") or get_base64_file("background_2.gif") or bg_game_b64

# Audio de fondo
audio_bg_b64 = get_base64_file("background.mp3")

# Imágenes de selección de personajes
ricky_b64 = get_base64_file("ricky.png")
ariana_b64 = get_base64_file("ariana.png")

# Tipografías locales
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

bg_game_tag = f'<img id="bg-game" class="screen-bg hidden" src="data:image/gif;base64,{bg_game_game_b64}" alt="Game BG" />' if (bg_game_b64 and 'bg_game_game_b64' in locals()) else (f'<img id="bg-game" class="screen-bg hidden" src="data:image/gif;base64,{bg_game_b64}" alt="Game BG" />' if bg_game_b64 else '<div id="bg-game" class="screen-bg hidden procedural-game"></div>')
bg_reg_tag = f'<img id="bg-reg" class="screen-bg" src="data:image/gif;base64,{bg_reg_b64}" alt="Register BG" />' if bg_reg_b64 else '<div id="bg-reg" class="screen-bg procedural-reg"></div>'

audio_html_tag = ""
if audio_bg_b64:
    audio_html_tag = f"""
    <audio id="bg-music" loop preload="auto">
        <source src="data:audio/mp3;base64,{audio_bg_b64}" type="audio/mp3">
    </audio>
    """

ricky_img_tag = f'<img src="data:image/png;base64,{ricky_b64}" class="w-full h-full object-contain pixelated" alt="Ricky" />' if ricky_b64 else '<div class="text-xs font-hud font-bold">[CHICO]</div>'
ariana_img_tag = f'<img src="data:image/png;base64,{ariana_b64}" class="w-full h-full object-contain pixelated" alt="Ariana" />' if ariana_b64 else '<div class="text-xs font-hud font-bold">[CHICA]</div>'

GAME_HTML = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Balatro: Factor Común 8-Bit Dark Fantasy</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap" rel="stylesheet">
    
    <style>
        {font_face_css}

        :root {{
            --font-hud: 'Press Start 2P', monospace;
            --font-sub: 'VT323', monospace;
            --font-dos: 'DosVgaFont', 'Press Start 2P', monospace;
            --font-balatro: 'BalatroFont', 'Press Start 2P', sans-serif;
            
            /* Paleta Dark Fantasy Pixel Art */
            --df-obsidian: #090a0f;
            --df-iron-slate: #151922;
            --df-iron-light: #2b3242;
            --df-crypt-stone: #1e1b18;
            --df-gold-relic: #d4a340;
            --df-gold-dark: #6e4e13;
            --df-blood-crimson: #8b1820;
            --df-blood-light: #c52834;
            --df-parchment: #c8b99c;
            --df-mystic-cyan: #228b96;
            --df-mystic-purple: #6a3489;
            
            /* Configuración cartas original */
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
            color: var(--df-parchment);
            font-family: var(--font-hud);
            overflow: hidden;
            user-select: none;
            margin: 0;
            height: 100vh;
            width: 100vw;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background-color: #040508;
        }}

        .font-hud {{ font-family: var(--font-hud); }}
        .font-sub {{ font-family: var(--font-sub); }}
        .font-dos {{ font-family: var(--font-dos); }}
        .font-balatro {{ font-family: var(--font-balatro); }}

        /* FONDOS (INTACTOS) */
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

        .procedural-reg {{ background: radial-gradient(circle at center, #181d26, #07090d); }}
        .procedural-game {{ background: radial-gradient(circle at center, #1b3d2b, #050c07); }}

        /* TRAMA DARK FANTASY + SCANLINES CRT */
        .bg-dark-overlay {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: 
                linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.45) 50%),
                radial-gradient(circle at center, rgba(14, 11, 22, 0.4) 0%, rgba(2, 3, 5, 0.94) 100%);
            background-size: 100% 4px, 100% 100%;
            pointer-events: none;
            z-index: -2;
        }}

        /* ========================================================
           GUI PIXEL ART DARK FANTASY: HIERRO, RUNAS Y PIEDRA
           ======================================================== */
        
        /* Cajas de piedra de calabozo con remaches pixelados */
        .pixel-df-panel {{
            background: #11141c;
            border: 4px solid #000000;
            box-shadow: 
                inset 4px 4px 0 #2e3648,
                inset -4px -4px 0 #08090d,
                0 0 0 2px #3c2a1e,
                0 8px 0 #000000;
            position: relative;
        }}

        /* Remaches en las 4 esquinas de los paneles principales */
        .pixel-df-panel::before {{
            content: "◆";
            position: absolute;
            top: 3px; left: 4px;
            font-size: 7px;
            color: #d4a340;
            text-shadow: 1px 1px 0 #000;
            pointer-events: none;
        }}
        .pixel-df-panel::after {{
            content: "◆";
            position: absolute;
            top: 3px; right: 4px;
            font-size: 7px;
            color: #d4a340;
            text-shadow: 1px 1px 0 #000;
            pointer-events: none;
        }}

        /* Hueco o altar tallado hundido */
        .pixel-df-slot {{
            background: #080a0e;
            border: 3px solid #000000;
            box-shadow: 
                inset 3px 3px 0 #000000,
                inset -2px -2px 0 #1b202c;
        }}

        /* Estandarte de Sangre / Pergamino Profano */
        .pixel-df-banner-crimson {{
            background: linear-gradient(180deg, #9b1c24 0%, #590d12 100%);
            border: 4px solid #000000;
            box-shadow: 
                inset 3px 3px 0 #d9434d,
                inset -3px -3px 0 #280306,
                0 0 0 1px #ff8a7a,
                0 6px 0 #000000;
            color: #f7e8ce;
            text-shadow: 2px 2px 0 #000000;
        }}

        /* Botón de Acción Principal: Fuego y Cobre Demoníaco */
        .pixel-df-btn-flame {{
            font-family: var(--font-hud);
            background: linear-gradient(180deg, #d35422 0%, #872506 100%);
            border: 4px solid #000000;
            box-shadow: 
                inset 3px 3px 0 #ff8a50,
                inset -3px -3px 0 #3a0e02,
                0 0 0 2px #d4a340,
                0 8px 0 #000000;
            color: #ffffff;
            text-shadow: 2px 2px 0 #000000;
            transition: transform 0.05s steps(2), box-shadow 0.05s steps(2);
            cursor: pointer;
        }}
        .pixel-df-btn-flame:hover {{
            background: linear-gradient(180deg, #ea632b 0%, #9e2e0a 100%);
        }}
        .pixel-df-btn-flame:active {{
            transform: translateY(6px);
            box-shadow: 
                inset 3px 3px 0 #3a0e02,
                inset -3px -3px 0 #ff8a50,
                0 0 0 2px #d4a340,
                0 2px 0 #000000;
        }}

        /* Botón Secundario Rúnico / Pergamino */
        .pixel-df-btn-arcane {{
            font-family: var(--font-hud);
            background: #172233;
            border: 3px solid #000000;
            box-shadow: 
                inset 2px 2px 0 #384e6f,
                inset -2px -2px 0 #090e17,
                0 5px 0 #000000;
            color: #a7c8e8;
            text-shadow: 2px 2px 0 #000000;
            transition: transform 0.05s steps(2);
        }}
        .pixel-df-btn-arcane:hover {{ background: #1e2c42; }}
        .pixel-df-btn-arcane:active {{
            transform: translateY(3px);
            box-shadow: inset 2px 2px 0 #090e17, inset -2px -2px 0 #384e6f, 0 2px 0 #000;
        }}

        /* Tótems / Comodines Alquímicos */
        .btn-relic-slot {{
            font-family: var(--font-hud);
            background: #131720;
            border: 3px solid #000000;
            box-shadow: 
                inset 2px 2px 0 #2d3648,
                inset -2px -2px 0 #06070a,
                0 5px 0 #000000;
            transition: transform 0.05s steps(2);
        }}
        .btn-relic-slot:hover {{
            border-color: #3f3123;
        }}
        .btn-relic-slot:active {{
            transform: translateY(3px);
            box-shadow: inset 2px 2px 0 #06070a, inset -2px -2px 0 #2d3648, 0 2px 0 #000000;
        }}

        /* Nicho de Héroes / Personajes */
        .char-slot-crypt {{
            background: #090c12;
            border: 3px solid #000000;
            box-shadow: 
                inset 3px 3px 0 #1b212e,
                inset -2px -2px 0 #040507,
                0 4px 0 #000;
            cursor: pointer;
            transition: transform 0.08s steps(2);
        }}
        .char-slot-crypt:hover {{
            border-color: #d4a340;
            background: #141a24;
            transform: translateY(-2px);
        }}
        .char-slot-crypt.selected {{
            border-color: #d4a340;
            background: #1b2230;
            box-shadow: 
                inset 0 0 0 2px #d4a340,
                0 0 10px rgba(212, 163, 64, 0.4),
                0 5px 0 #000000;
        }}

        /* ========================================================
           CARTAS 8-BIT / BALATRO (CONSERVADAS 100% INTACTAS)
           ======================================================== */
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

        .corner-text {{
            font-size: 13px;
            font-weight: bold;
            letter-spacing: -0.5px;
        }}
        .corner-suit-icon {{
            font-size: 11px;
            margin-top: 1px;
        }}

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
    </style>
</head>
<body class="p-2 sm:p-4">
    {bg_reg_tag}
    {bg_game_tag}
    {audio_html_tag}
    <div class="bg-dark-overlay"></div>
    <canvas id="fx-canvas"></canvas>

    <!-- INTRO / REGISTRO: ESTILO NÉBULA OSCURA -->
    <div id="intro-modal" class="fixed inset-0 bg-black/90 z-[1000] flex items-center justify-center p-4">
        <div class="pixel-df-panel max-w-sm w-full p-6 text-center">
            
            <div class="pixel-df-banner-crimson py-3 px-4 mb-5 transform -rotate-1 inline-block w-full">
                <h1 class="text-xs sm:text-base tracking-wider font-hud text-[#fff1d0]">FACTOR COMÚN</h1>
                <p class="text-[8px] opacity-90 tracking-widest mt-1 font-hud text-amber-200">DARK FANTASY • IF0003</p>
            </div>
            
            <!-- PASO 1: NOMBRE -->
            <div id="step-name">
                <div class="pixel-df-slot p-4 mb-5 text-left">
                    <label class="block text-[9px] text-[#a99878] mb-2 tracking-wider font-hud">NOMBRE DEL INVOCADOR:</label>
                    <input type="text" id="username-input" class="w-full bg-[#050608] border-2 border-[#333d4f] text-[#d4a340] p-3 text-center uppercase tracking-wider text-sm font-bold font-hud outline-none focus:border-[#d4a340]" placeholder="TU NOMBRE" maxlength="12">
                </div>
                <button onclick="goToGenderStep()" class="pixel-df-btn-flame w-full py-4 text-xs font-bold tracking-wider">
                    CONTINUAR ➔
                </button>
            </div>

            <!-- PASO 2: ELECCIÓN DE PERSONAJE -->
            <div id="step-gender" class="hidden">
                <div class="pixel-df-slot p-3 mb-4 text-center">
                    <p class="text-[9px] text-[#d4a340] font-hud mb-3 tracking-wider">SELECCIONA TU HERMANO DE SANGRE</p>
                    <div class="grid grid-cols-2 gap-3">
                        <div id="opt-boy" onclick="selectGender('boy')" class="char-slot-crypt p-2 flex flex-col items-center">
                            <div class="w-20 h-20 sm:w-24 sm:h-24 flex items-center justify-center mb-1">
                                {ricky_img_tag}
                            </div>
                            <span class="text-[9px] font-bold text-gray-300 font-hud">[CHICO]</span>
                        </div>
                        <div id="opt-girl" onclick="selectGender('girl')" class="char-slot-crypt p-2 flex flex-col items-center">
                            <div class="w-20 h-20 sm:w-24 sm:h-24 flex items-center justify-center mb-1">
                                {ariana_img_tag}
                            </div>
                            <span class="text-[9px] font-bold text-gray-300 font-hud">[CHICA]</span>
                        </div>
                    </div>
                </div>
                <button id="btn-start-game" onclick="startGame()" disabled class="pixel-df-panel bg-[#0d0f14] text-stone-600 w-full py-3.5 text-xs font-bold tracking-wider opacity-40 cursor-not-allowed">
                    INICIAR PACTO ➔
                </button>
            </div>

        </div>
    </div>

    <!-- BOTONES AUXILIARES INFERIORES -->
    <div class="fixed bottom-3 left-3 z-40">
        <button onclick="toggleTutorial()" class="pixel-df-btn-arcane text-[9px] sm:text-xs px-3.5 py-2 font-hud flex items-center gap-1.5">
            <span class="text-amber-400">❖</span> TOMO [?]
        </button>
    </div>
    <div class="fixed bottom-3 right-3 z-40">
        <button onclick="showRankNotice()" class="pixel-df-panel bg-[#0d1017] text-stone-400 text-[9px] sm:text-xs px-3.5 py-2 cursor-pointer relative font-hud">
            [ CRÓNICA ]
            <span class="absolute -top-2 -right-2 bg-[#8b1820] text-amber-200 text-[7px] font-bold px-1.5 py-0.5 border border-black">DEV</span>
        </button>
    </div>

    <!-- TOMO DE GUÍA / TUTORIAL -->
    <div id="tutorial-panel" class="fixed left-0 top-0 h-full w-72 sm:w-80 bg-[#0d1017] border-r-4 border-black p-4 flex flex-col z-50 transform -translate-x-full transition-transform duration-200 shadow-2xl">
        <div class="flex justify-between items-center mb-4 border-b-2 border-[#2b3548] pb-2">
            <div class="pixel-df-banner-crimson px-3 py-1 text-[9px] font-hud">TOMO: FACTOR COMÚN</div>
            <button onclick="toggleTutorial()" class="text-amber-200 text-xs font-bold font-hud hover:text-white">[ ✕ ]</button>
        </div>
        <div class="pixel-df-slot p-3 text-2xl text-center mb-3 font-sub text-stone-200">
            4x² + 6x
        </div>
        <p class="text-[8px] text-[#d4a340] text-center mb-3 font-hud">MCD = 2 | VARIABLE = x</p>
        <div class="pixel-df-slot p-3 text-2xl text-center mb-4 font-sub text-emerald-400 border border-emerald-900/60">
            2x · (2x + 3)
        </div>
        <div class="text-base text-stone-300 leading-snug font-sub space-y-2">
            <p>1. Selecciona 2 o más runas que compartan divisores o variables comunes.</p>
            <p>2. Presiona "JUGAR MANO" para canalizar fichas multiplicadas.</p>
            <p>3. Las runas descartadas permanecerán en tu mano para la siguiente ronda.</p>
        </div>
    </div>

    <!-- ========================================================
         HEADER SUPERIOR: RELICARIOS DARK FANTASY
         ======================================================== -->
    <header class="flex justify-between items-center z-10 max-w-5xl mx-auto w-full gap-2 px-1">
        <!-- CAJA DE NIVEL Y RONDA -->
        <div class="pixel-df-panel px-3.5 py-2.5 text-center min-w-[110px] sm:min-w-[140px] flex flex-col items-center justify-center">
            <span class="text-[8px] sm:text-[9px] text-[#8e98aa] font-hud tracking-wider">CALABOZO</span>
            <span id="level-display" class="text-base sm:text-2xl text-[#d4a340] font-hud font-bold leading-tight my-0.5">1</span>
            <span class="text-[7px] sm:text-[8px] text-[#c8b99c] font-hud tracking-wider">RONDA <span id="round-display" class="text-white">1</span>/3</span>
        </div>

        <!-- RELICARIOS / COMODINES EN TEXTO ARCADE -->
        <div class="flex justify-center gap-2 sm:gap-3">
            <button id="btn-joker-reveal" onclick="useJoker('reveal')" title="Revelar factor" class="btn-relic-slot px-3 py-2 text-center relative">
                <span class="block text-[9px] sm:text-[11px] text-cyan-400 font-hud font-bold">REVELAR</span>
                <span id="qty-reveal" class="absolute -top-2 -right-2 bg-[#8b1820] text-amber-200 text-[8px] px-1.5 py-0.5 border border-black font-hud">1</span>
            </button>
            <button id="btn-joker-reroll" onclick="useJoker('reroll')" title="Revolver mano" class="btn-relic-slot px-3 py-2 text-center relative">
                <span class="block text-[9px] sm:text-[11px] text-purple-400 font-hud font-bold">REVOLVER</span>
                <span id="qty-reroll" class="absolute -top-2 -right-2 bg-[#51237a] text-purple-200 text-[8px] px-1.5 py-0.5 border border-black font-hud">1</span>
            </button>
            <button id="btn-joker-skip" onclick="useJoker('skip')" title="Saltar 1 Ronda" class="btn-relic-slot px-3 py-2 text-center relative opacity-40">
                <span class="block text-[9px] sm:text-[11px] text-amber-400 font-hud font-bold">SALTAR</span>
                <span id="qty-skip" class="absolute -top-2 -right-2 bg-[#8b6508] text-amber-100 text-[8px] px-1.5 py-0.5 border border-black font-hud">0</span>
            </button>
        </div>

        <!-- CAJA DE PUNTOS Y JUGADOR -->
        <div class="pixel-df-panel px-3.5 py-2.5 text-center min-w-[110px] sm:min-w-[140px] flex flex-col items-center justify-center">
            <span class="text-[8px] sm:text-[9px] text-[#8e98aa] font-hud tracking-wider">ALMAS</span>
            <span id="total-score" class="text-base sm:text-xl text-[#d4a340] font-hud font-bold leading-tight my-0.5">0</span>
            <span id="user-display-tag" class="text-[7px] sm:text-[8px] text-[#c8b99c] font-hud truncate max-w-[95px]">JUGADOR</span>
        </div>
    </header>

    <!-- ÁREA DE CARTAS -->
    <main class="flex-grow flex flex-col items-center justify-center relative w-full max-w-5xl mx-auto my-auto">
        <div id="hand-container" class="flex justify-center items-center flex-wrap gap-2.5 sm:gap-4 w-full px-2 mb-6"></div>

        <button id="btn-play" onclick="playHand()" disabled class="pixel-df-panel bg-[#0d0f14] text-stone-600 px-8 py-3.5 sm:px-12 sm:py-4 text-xs sm:text-sm tracking-widest opacity-40 cursor-not-allowed font-hud">
            JUGAR MANO
        </button>

        <div id="flame-score-container" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 hidden opacity-0 transition-opacity duration-200 z-40 pointer-events-none text-center">
            <div id="flame-score" class="text-3xl sm:text-5xl score-flame tracking-wider">0</div>
        </div>
    </main>

    <!-- MODAL FIN DE NIVEL -->
    <div id="level-modal" class="fixed inset-0 bg-black/90 z-50 hidden flex items-center justify-center p-4">
        <div class="pixel-df-panel max-w-sm w-full p-6 text-center">
            
            <div class="pixel-df-banner-crimson py-3 px-4 mb-4 transform -rotate-1 inline-block w-full">
                <h2 class="text-xs sm:text-sm font-bold tracking-wider font-hud">SELLO COMPLETADO</h2>
            </div>
            
            <div class="flex justify-center gap-3 my-3 text-2xl sm:text-3xl font-hud" id="modal-stars"></div>
            
            <div class="pixel-df-slot p-3 text-stone-200 mb-5 font-sub text-lg sm:text-xl leading-snug text-left">
                <div id="modal-desc" class="space-y-1"></div>
            </div>
            
            <button onclick="nextLevel()" class="pixel-df-btn-flame w-full py-4 text-xs sm:text-sm tracking-wider font-hud">
                DESCENDER MÁS ➔
            </button>
        </div>
    </div>

    <!-- ALERTA BALATRO OSCURA -->
    <div id="alert-modal" class="fixed top-12 left-1/2 -translate-x-1/2 pixel-df-banner-crimson text-[9px] sm:text-xs px-5 py-3 z-50 hidden text-center max-w-[90vw] font-hud">
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
            hover: () => playTone(300, 'sine', 0.08, 0.04),
            select: () => playTone(510, 'triangle', 0.12, 0.12),
            error: () => {{ playTone(120, 'sawtooth', 0.25, 0.25); setTimeout(() => playTone(80, 'sawtooth', 0.35, 0.25), 100); }},
            flamePop: () => {{ playTone(170, 'sawtooth', 0.28, 0.25); setTimeout(() => playTone(230, 'sawtooth', 0.2, 0.2), 60); }},
            star: () => {{ playTone(860, 'sine', 0.3, 0.2); setTimeout(()=>playTone(1080, 'sine', 0.4, 0.2), 100); }},
            discard: () => playTone(220, 'triangle', 0.15, 0.15),
            winRound: () => {{ playTone(420, 'sine', 0.3, 0.2); setTimeout(() => playTone(630, 'sine', 0.3, 0.2), 150); }}
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
            const colors = ['#d4a340', '#8b1820', '#d35422', '#ffffff'];
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
            btn.className = "pixel-df-btn-flame w-full py-3.5 text-xs font-bold tracking-wider cursor-pointer";
            SFX.select();
        }}

        function startGame() {{
            if (!playerGender) return;
            document.getElementById('intro-modal').classList.add('hidden');
            document.getElementById('user-display-tag').textContent = `${{playerGender === 'boy' ? '[CHICO]' : '[CHICA]'}} ${{playerName}}`;
            
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
            showAlert("[CRÓNICA EN DESARROLLO]");
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
                btnPlay.className = "pixel-df-btn-flame px-8 py-3.5 sm:px-12 sm:py-4 text-xs sm:text-sm tracking-widest cursor-pointer";
            }} else {{
                btnPlay.disabled = true;
                btnPlay.className = "pixel-df-panel bg-[#0d0f14] text-stone-600 px-8 py-3.5 sm:px-12 sm:py-4 text-xs sm:text-sm tracking-widest opacity-40 cursor-not-allowed font-hud";
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
                bonusItemText = `<div class="text-emerald-400 font-bold">[+] RELIQUIA "SALTAR" DESBLOQUEADA</div>`;
            }}

            desc.innerHTML = `
                <div class="flex justify-between border-b border-[#2b3548] pb-1">
                    <span>PRECISIÓN DE MANO:</span>
                    <span class="text-[#d4a340] font-bold">${{Math.round(precision * 100)}}%</span>
                </div>
                <div class="flex justify-between border-b border-[#2b3548] py-1">
                    <span>BONO DE ALMAS:</span>
                    <span class="text-emerald-400 font-bold">+${{bonusScore.toLocaleString()}} PTS</span>
                </div>
                <div class="pt-1">
                    ${{bonusItemText}}
                </div>
            `;

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
                showAlert("[MANO PURIFICADA]");
            }}
            else if (type === 'skip') {{
                comodines.skip--;
                SFX.winRound();
                showAlert("[RONDA TRASCENDIDA]");
                
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
