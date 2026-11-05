"""
Balatro: Factor Común - Edición Dark Fantasy Grimorio RPG
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

# Video o fondo animado
video_b64 = None
video_mime = "video/mp4"
for v_name in ["background_gif.gif", "background.gif", "fakcpg.mp4", "faKcpg.mp4", "fakcpg.gif", "faKcpg.gif"]:
    b64 = get_base64_file(v_name)
    if b64:
        video_b64 = b64
        if v_name.endswith(".gif"):
            video_mime = "image/gif"
        break

# Audio de fondo
audio_bg_b64 = get_base64_file("background.mp3")

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

GAME_HTML = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Balatro: Factor Común</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;900&family=Press+Start+2P&family=VT323&display=swap" rel="stylesheet">
    
    <style>
        :root {{
            --font-pixel-hud: 'Press Start 2P', monospace;
            --font-pixel-sub: 'VT323', monospace;
            --font-rpg: 'Cinzel', serif;
            
            /* Paleta Dark Fantasy RPG */
            --parchment-bg: #dfd4bc;
            --parchment-dark: #caa778;
            --iron-dark: #12151c;
            --iron-mid: #252b38;
            --iron-border: #08090d;
            --gold-trim: #b88a38;
            --gold-bright: #e7ba5d;
            --ruby-seal: #87141b;
        }}

        * {{
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }}

        body {{
            color: #ede4d0;
            font-family: var(--font-pixel-hud);
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

        /* FONDOS */
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
            background: radial-gradient(circle at center, rgba(10, 14, 18, 0.45) 0%, rgba(3, 4, 6, 0.94) 100%);
            mix-blend-mode: multiply;
            pointer-events: none;
            z-index: -2;
        }}

        .filter-ronda-1 {{ filter: hue-rotate(95deg) saturate(140%) brightness(0.72) contrast(1.15); }}
        .filter-ronda-2 {{ filter: hue-rotate(60deg) saturate(150%) brightness(0.8) contrast(1.2); }}
        .filter-ronda-3 {{ filter: hue-rotate(150deg) saturate(135%) brightness(0.68) contrast(1.15); }}

        /* ========================================================
           INTERFAZ DARK FANTASY & GRIMORIO (INSPIRADA EN LA IMAGEN)
           ======================================================== */
        
        /* Panel Grimorio de Madera y Hierro */
        .rpg-frame-wood {{
            background: #181d26;
            border: 4px solid var(--iron-border);
            border-radius: 4px;
            box-shadow: 
                inset 2px 2px 0 #3a455a, 
                inset -2px -2px 0 #0b0d12,
                0 0 0 2px var(--gold-trim),
                0 10px 0 #000000;
            position: relative;
        }}

        /* Esquinas de Hierro Forjado Decorativas */
        .rpg-frame-wood::before {{
            content: '';
            position: absolute;
            top: -3px; left: -3px; width: 8px; height: 8px;
            border-top: 3px solid var(--gold-bright);
            border-left: 3px solid var(--gold-bright);
            pointer-events: none;
        }}
        .rpg-frame-wood::after {{
            content: '';
            position: absolute;
            bottom: -3px; right: -3px; width: 8px; height: 8px;
            border-bottom: 3px solid var(--gold-bright);
            border-right: 3px solid var(--gold-bright);
            pointer-events: none;
        }}

        /* Placa de Pergamino Envejecido */
        .rpg-parchment-slot {{
            background: var(--parchment-bg);
            border: 3px solid #332717;
            box-shadow: 
                inset 2px 2px 0 #ffffff,
                inset -2px -2px 0 #9c845b,
                0 0 0 1px #594427;
            color: #1a140d;
            position: relative;
        }}

        /* Estandarte de Título Gótico */
        .rpg-title-banner {{
            background: linear-gradient(180deg, #9b1920 0%, #630c11 100%);
            border: 3px solid #000000;
            box-shadow: 
                inset 2px 2px 0 #e44d56,
                inset -2px -2px 0 #350508,
                0 0 0 2px var(--gold-trim),
                0 6px 0 #000000;
            color: #ffffff;
            text-shadow: 2px 2px 0 #000000;
        }}

        /* Botón Táctil Dorado / Fuego */
        .rpg-btn-action {{
            font-family: var(--font-pixel-hud);
            background: linear-gradient(180deg, #d35f1f 0%, #993708 100%);
            border: 3px solid #000000;
            border-radius: 4px;
            box-shadow: 
                inset 2px 2px 0 #fca168,
                inset -2px -2px 0 #4f1701,
                0 0 0 1px var(--gold-trim),
                0 7px 0 #000000;
            color: #ffffff;
            text-shadow: 2px 2px 0 #000000;
            transition: transform 0.05s steps(2), box-shadow 0.05s steps(2);
        }}
        .rpg-btn-action:hover {{
            background: linear-gradient(180deg, #e36e2f 0%, #aa420f 100%);
        }}
        .rpg-btn-action:active {{
            transform: translateY(5px);
            box-shadow: 
                inset 2px 2px 0 #4f1701,
                inset -2px -2px 0 #fca168,
                0 2px 0 #000000;
        }}

        .rpg-btn-blue {{
            font-family: var(--font-pixel-hud);
            background: linear-gradient(180deg, #186ba3 0%, #0d4267 100%);
            border: 3px solid #000000;
            border-radius: 4px;
            box-shadow: 
                inset 2px 2px 0 #49a8e8,
                inset -2px -2px 0 #062338,
                0 0 0 1px var(--gold-trim),
                0 5px 0 #000000;
            color: #ffffff;
            text-shadow: 2px 2px 0 #000000;
        }}

        /* Cajas de Comodines en Hierro & Gema */
        .rpg-relic-box {{
            font-family: var(--font-pixel-hud);
            background: #141720;
            border: 3px solid #000000;
            border-radius: 4px;
            box-shadow: 
                inset 2px 2px 0 #2e374d,
                inset -2px -2px 0 #07080c,
                0 0 0 1px var(--gold-trim),
                0 5px 0 #000000;
            transition: transform 0.05s steps(2), box-shadow 0.05s steps(2);
        }}
        .rpg-relic-box:active {{
            transform: translateY(3px);
            box-shadow: inset 2px 2px 0 #07080c, inset -2px -2px 0 #2e374d, 0 2px 0 #000000;
        }}

        /* ========================================================
           SECCIÓN INTACTA: CARTAS DE BALATRO (CSS NO TOCADO)
           ======================================================== */
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
        }}
        .card-pip-br {{
            position: absolute;
            bottom: 6px; right: 8px;
            display: flex; flex-direction: column; align-items: center;
            line-height: 0.95;
            transform: rotate(180deg);
            pointer-events: none;
        }}

        .pip-val {{
            font-size: 13px;
            font-weight: bold;
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
            color: #1a1c22;
            text-align: center;
            line-height: 1;
            white-space: nowrap;
            letter-spacing: -0.5px;
            font-weight: bold;
            text-shadow: 1px 1px 0 rgba(0,0,0,0.12);
        }}

        .len-1 {{ font-size: 2.1rem; }}
        .len-2 {{ font-size: 1.85rem; }}
        .len-3 {{ font-size: 1.55rem; }}
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
            .len-1 {{ font-size: 1.55rem !important; }}
            .len-2 {{ font-size: 1.35rem !important; }}
            .len-3 {{ font-size: 1.15rem !important; }}
            .len-4 {{ font-size: 0.95rem !important; }}
            .len-5 {{ font-size: 0.82rem !important; }}
            .len-many {{ font-size: 0.72rem !important; }}
            .pip-val {{ font-size: 10px !important; }}
            .pip-suit {{ font-size: 9px !important; }}
            #hand-container {{ min-height: 200px !important; }}
        }}

        @keyframes flame-flicker {{
            0% {{ text-shadow: 0 0 10px #ff5a00, 0 -5px 15px #ff9c00, 0 -10px 20px #ffce00; transform: scale(1); }}
            50% {{ text-shadow: 0 0 22px #ff5a00, 0 -10px 28px #ff9c00, 0 -15px 32px #ffce00; transform: scale(1.1); }}
            100% {{ text-shadow: 0 0 10px #ff5a00, 0 -5px 15px #ff9c00, 0 -10px 20px #ffce00; transform: scale(1); }}
        }}
        .score-flame {{ color: #fff; animation: flame-flicker 0.6s infinite alternate; font-family: var(--font-pixel-hud); }}

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

    <!-- INTRO MODAL ESTILO GRIMORIO DARK FANTASY -->
    <div id="intro-modal" class="fixed inset-0 bg-black/85 z-[1000] flex items-center justify-center p-4 backdrop-blur-sm">
        <div class="rpg-frame-wood max-w-sm w-full p-6 text-center">
            
            <!-- Banner Estandarte -->
            <div class="rpg-title-banner py-3 px-4 mb-5 inline-block w-full">
                <h1 class="text-base sm:text-lg tracking-wider font-pixel-hud">FACTOR COMÚN</h1>
                <p class="text-[9px] text-amber-200 tracking-widest mt-1 font-pixel-hud">MATEMÁTICA BÁSICA • UCR</p>
            </div>
            
            <!-- Pergamino de Registro -->
            <div class="rpg-parchment-slot p-4 mb-5 text-left">
                <label class="block text-[10px] text-[#4d3a22] font-bold mb-2 tracking-wider font-pixel-hud">APODO DEL JUGADOR:</label>
                <input type="text" id="username-input" class="w-full bg-[#f6efe1] border-2 border-[#5c462b] text-[#241a0d] p-3 text-center uppercase tracking-wider text-sm font-bold font-pixel-hud outline-none focus:border-[#b88a38]" placeholder="TU NOMBRE" maxlength="12">
            </div>

            <button onclick="startGameFromIntro()" class="rpg-btn-action w-full py-4 text-xs sm:text-sm font-bold tracking-wider">
                ENTRAR AL JUEGO ➔
            </button>
        </div>
    </div>

    <!-- BOTONES AUXILIARES INFERIORES -->
    <div class="fixed bottom-3 left-3 z-40">
        <button onclick="toggleTutorial()" class="rpg-btn-blue text-[10px] sm:text-xs px-3.5 py-2 font-pixel-hud">
            [ ? ] GUÍA
        </button>
    </div>
    <div class="fixed bottom-3 right-3 z-40">
        <!-- RANKING EN DESARROLLO -->
        <button onclick="showRankNotice()" class="rpg-relic-box text-[10px] sm:text-xs text-amber-200 px-3.5 py-2 font-pixel-hud relative cursor-pointer" title="Módulo en desarrollo">
            [ RANK ]
            <span class="absolute -top-2 -right-2 bg-yellow-500 text-black text-[8px] font-bold px-1 border border-black">DEV</span>
        </button>
    </div>

    <!-- PANEL GUÍA TUTORIAL -->
    <div id="tutorial-panel" class="fixed left-0 top-0 h-full w-72 sm:w-80 bg-[#12151c] border-r-4 border-black p-4 flex flex-col z-50 transform -translate-x-full transition-transform duration-300 shadow-2xl">
        <div class="flex justify-between items-center mb-4 border-b-2 border-white/10 pb-2">
            <div class="rpg-title-banner px-3 py-1 text-[10px] font-pixel-hud">GUÍA FACTORIZACIÓN</div>
            <button onclick="toggleTutorial()" class="text-white text-sm font-bold font-pixel-hud">[ X ]</button>
        </div>
        <div class="rpg-parchment-slot p-3 text-2xl text-center mb-3 font-['VT323']">
            4x² + 6x
        </div>
        <p class="text-[9px] text-[#e7ba5d] text-center mb-3 font-pixel-hud">MCD = 2, VARIABLE COMÚN = x</p>
        <div class="rpg-parchment-slot p-3 text-2xl text-center mb-4 font-['VT323'] text-emerald-900 font-bold">
            2x · (2x + 3)
        </div>
        <div class="text-base text-gray-300 leading-snug font-['VT323'] space-y-2">
            <p>1. Selecciona 2 o más cartas que compartan divisores o variables comunes.</p>
            <p>2. Presiona "JUGAR MANO" para acumular fichas multiplicadas.</p>
            <p>3. Las cartas no jugadas permanecen en tu mano para la siguiente ronda.</p>
        </div>
    </div>

    <!-- ========================================================
         HUD SUPERIOR DARK FANTASY (ORGANIZACIÓN VERTICAL)
         ======================================================== -->
    <header class="flex justify-between items-center z-10 max-w-5xl mx-auto w-full gap-2 px-1">
        <!-- CAJA DE NIVEL Y RONDA -->
        <div class="rpg-frame-wood px-3.5 py-2.5 text-center min-w-[110px] sm:min-w-[140px] flex flex-col items-center justify-center">
            <span class="text-[9px] sm:text-[10px] text-gray-400 font-pixel-hud tracking-wider">NIVEL</span>
            <span id="level-display" class="text-lg sm:text-2xl text-[#e7ba5d] font-pixel-hud font-bold leading-tight my-0.5">1</span>
            <span class="text-[8px] sm:text-[9px] text-gray-300 font-pixel-hud tracking-wider">RONDA <span id="round-display" class="text-white">1</span>/3</span>
        </div>

        <!-- RELIQUIAS / COMODINES -->
        <div class="flex justify-center gap-2 sm:gap-3">
            <button id="btn-joker-reveal" onclick="useJoker('reveal')" title="Revelar factor" class="rpg-relic-box px-3 py-2 text-center relative active:translate-y-1">
                <span class="block text-[10px] sm:text-xs text-cyan-300 font-pixel-hud font-bold">REVELAR</span>
                <span id="qty-reveal" class="absolute -top-2 -right-2 bg-red-600 text-white text-[8px] sm:text-[9px] px-1.5 py-0.5 rounded-sm border border-black font-pixel-hud">1</span>
            </button>

            <button id="btn-joker-reroll" onclick="useJoker('reroll')" title="Cambiar mano" class="rpg-relic-box px-3 py-2 text-center relative active:translate-y-1">
                <span class="block text-[10px] sm:text-xs text-purple-300 font-pixel-hud font-bold">REVOLVER</span>
                <span id="qty-reroll" class="absolute -top-2 -right-2 bg-purple-600 text-white text-[8px] sm:text-[9px] px-1.5 py-0.5 rounded-sm border border-black font-pixel-hud">1</span>
            </button>

            <button id="btn-joker-skip" onclick="useJoker('skip')" title="Saltar 1 ronda" class="rpg-relic-box px-3 py-2 text-center relative active:translate-y-1 opacity-40">
                <span class="block text-[10px] sm:text-xs text-amber-300 font-pixel-hud font-bold">SALTAR</span>
                <span id="qty-skip" class="absolute -top-2 -right-2 bg-amber-500 text-black text-[8px] sm:text-[9px] px-1.5 py-0.5 rounded-sm border border-black font-pixel-hud">0</span>
            </button>
        </div>

        <!-- CAJA DE PUNTOS Y JUGADOR -->
        <div class="rpg-frame-wood px-3.5 py-2.5 text-center min-w-[110px] sm:min-w-[140px] flex flex-col items-center justify-center">
            <span class="text-[9px] sm:text-[10px] text-gray-400 font-pixel-hud tracking-wider">PUNTOS</span>
            <span id="total-score" class="text-base sm:text-xl text-[#e7ba5d] font-pixel-hud font-bold leading-tight my-0.5">0</span>
            <span id="user-display-tag" class="text-[8px] sm:text-[9px] text-gray-300 font-pixel-hud truncate max-w-[95px]">JUGADOR</span>
        </div>
    </header>

    <!-- ÁREA CENTRAL DE CARTAS -->
    <main class="flex-grow flex flex-col items-center justify-center relative w-full max-w-5xl mx-auto my-auto">
        <div id="hand-container" class="flex justify-center items-center flex-wrap gap-2.5 sm:gap-4 w-full px-2 mb-6"></div>

        <button id="btn-play" onclick="playHand()" disabled class="rpg-frame-wood bg-[#12151c] text-gray-500 px-8 py-3.5 sm:px-12 sm:py-4 text-xs sm:text-sm tracking-widest opacity-40 cursor-not-allowed font-pixel-hud">
            JUGAR MANO
        </button>

        <div id="flame-score-container" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 hidden opacity-0 transition-opacity duration-300 z-40 pointer-events-none text-center">
            <div id="flame-score" class="text-4xl sm:text-6xl score-flame tracking-wider drop-shadow-[0_0_35px_#ff4500]">0</div>
        </div>
    </main>

    <!-- ========================================================
         VENTANA DE FIN DE NIVEL REDISEÑADA (GRIMORIO RPG)
         ======================================================== -->
    <div id="level-modal" class="fixed inset-0 bg-black/85 z-50 hidden flex items-center justify-center backdrop-blur-sm p-4">
        <div class="rpg-frame-wood max-w-sm w-full p-6 text-center">
            
            <!-- Estandarte Superior -->
            <div class="rpg-title-banner py-3 px-4 mb-4 inline-block w-full">
                <h2 class="text-xs sm:text-sm tracking-wider font-pixel-hud">NIVEL COMPLETADO</h2>
            </div>
            
            <!-- Estrellas / Sellos -->
            <div class="flex justify-center gap-3 my-3 text-2xl sm:text-3xl font-pixel-hud" id="modal-stars"></div>
            
            <!-- Pergamino Interior con Desglose -->
            <div class="rpg-parchment-slot p-3 mb-5 font-['VT323'] text-lg sm:text-xl leading-snug text-left">
                <div id="modal-desc" class="space-y-1"></div>
            </div>

            <!-- Botón de Siguiente Nivel -->
            <button onclick="nextLevel()" class="rpg-btn-action w-full py-4 text-xs sm:text-sm tracking-wider font-pixel-hud">
                SIGUIENTE NIVEL ➔
            </button>
        </div>
    </div>

    <!-- ALERTA BALATRO -->
    <div id="alert-modal" class="fixed top-12 left-1/2 -translate-x-1/2 rpg-title-banner text-[10px] sm:text-xs px-5 py-3 z-50 hidden transition-opacity text-center max-w-[90vw] font-pixel-hud">
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
        function spawnParticles(x, y, count=30) {{
            const colors = ['#e7ba5d', '#0077c8', '#87141b', '#ffffff'];
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

        function startGameFromIntro() {{
            const input = document.getElementById('username-input').value.trim();
            if(input) playerName = input.toUpperCase();
            
            document.getElementById('intro-modal').classList.add('hidden');
            document.getElementById('user-display-tag').textContent = playerName;
            
            SFX.select();
            startBackgroundMusic();
            startRound();
            updateUI();
        }}

        function showRankNotice() {{
            SFX.hover();
            showAlert("[RANKING EN INTEGRACIÓN]");
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
            const suitColor = (suit === '♥' || suit === '♦') ? '#87141b' : '#186ba3';

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
                btnPlay.className = "rpg-btn-action px-8 py-3.5 sm:px-12 sm:py-4 text-xs sm:text-sm tracking-widest cursor-pointer";
            }} else {{
                btnPlay.disabled = true;
                btnPlay.className = "rpg-frame-wood bg-[#12151c] text-gray-500 px-8 py-3.5 sm:px-12 sm:py-4 text-xs sm:text-sm tracking-widest opacity-40 cursor-not-allowed";
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
                    starContainer.innerHTML += `<span class="text-[#e7ba5d] drop-shadow-[0_2px_0_#000]">★</span>`;
                }} else {{
                    starContainer.innerHTML += `<span class="text-stone-400">☆</span>`;
                }}
            }}

            let bonusScore = stars * 1000 * level;
            score += bonusScore;
            document.getElementById('total-score').textContent = score.toLocaleString();

            let bonusItemText = "";
            if(stars === 3) {{
                comodines.skip++;
                updateUI();
                bonusItemText = `<div class="text-emerald-900 font-bold mt-1">[+] RELIQUIA "SALTAR" OBTENIDA</div>`;
            }}

            desc.innerHTML = `
                <div class="flex justify-between border-b border-[#a8936f] pb-1 text-[#2d2215]">
                    <span>PRECISIÓN DE MANO:</span>
                    <span class="text-[#87141b] font-bold">${{Math.round(precision * 100)}}%</span>
                </div>
                <div class="flex justify-between border-b border-[#a8936f] py-1 text-[#2d2215]">
                    <span>BONO DE NIVEL:</span>
                    <span class="text-emerald-900 font-bold">+${{bonusScore.toLocaleString()}} PTS</span>
                </div>
                <div>
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
