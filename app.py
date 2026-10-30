"""
Arcana Alquimia: Factor Común - Aplicación Educativa en Streamlit
Curso: IF0003 Matemática Básica para Informática Empresarial
Universidad de Costa Rica - Recinto de Paraíso
"""

import os
import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Alquimia Arcana: Factor Común | IF0003",
    page_icon="⚗️",
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
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
        max-width: 100% !important;
    }
    .stApp {
        background-color: #08100d;
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

font_face_css = ""
if daydream_b64:
    font_face_css += f"""
    @font-face {{
        font-family: 'DaydreamFont';
        src: url(data:font/otf;base64,{daydream_b64}) format('opentype');
        font-weight: normal;
        font-style: normal;
    }}
    """
else:
    font_face_css += """
    @font-face {
        font-family: 'DaydreamFont';
        src: local('Press Start 2P'), local('Courier New');
        font-weight: bold;
    }
    """

if kiwisoda_b64:
    font_face_css += f"""
    @font-face {{
        font-family: 'KiwiSodaFont';
        src: url(data:font/ttf;base64,{kiwisoda_b64}) format('truetype');
        font-weight: normal;
        font-style: normal;
    }}
    """
else:
    font_face_css += """
    @font-face {
        font-family: 'KiwiSodaFont';
        src: local('VT323'), local('Courier New');
        font-weight: bold;
    }
    """

if video_b64:
    if "gif" in video_mime:
        video_html_tag = f'<img id="bg-media" class="video-bg filter-ronda-1" src="data:{video_mime};base64,{video_b64}" alt="Caldero" />'
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
    <title>Alquimia Arcana: Factor Común</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        {font_face_css}

        :root {{
            --font-title: 'DaydreamFont', cursive, monospace;
            --font-body: 'KiwiSodaFont', monospace;
            --gold-bright: #ffd447;
            --gold-dark: #b8860b;
            --alchemy-cyan: #4deeea;
            --magic-purple: #9d4edd;
        }}

        * {{
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }}

        body {{
            color: #f4ebd9;
            font-family: var(--font-body);
            overflow: hidden;
            user-select: none;
            margin: 0;
            height: 100vh;
            width: 100vw;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background-color: #08100d;
        }}

        .font-pixel-title {{ font-family: var(--font-title); }}
        .font-pixel-body {{ font-family: var(--font-body); }}

        /* VIDEO DEL CALDERO DE FONDO */
        .video-bg {{
            position: fixed;
            top: 50%; left: 50%;
            min-width: 100%; min-height: 100%;
            width: auto; height: auto;
            transform: translate(-50%, -50%) scale(1.06);
            z-index: -3;
            object-fit: cover;
            pointer-events: none;
            transition: filter 1.3s ease-in-out;
        }}

        .procedural-bg {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: radial-gradient(circle at center, #1b4931, #08120c);
            z-index: -3;
        }}

        .bg-cauldron-overlay {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: radial-gradient(circle at center, rgba(14, 46, 31, 0.45) 0%, rgba(4, 13, 9, 0.92) 100%);
            mix-blend-mode: multiply;
            pointer-events: none;
            z-index: -2;
        }}

        .filter-ronda-1 {{ filter: hue-rotate(95deg) saturate(140%) brightness(0.72) contrast(1.15); }}
        .filter-ronda-2 {{ filter: hue-rotate(40deg) saturate(160%) brightness(0.82) contrast(1.2); }}
        .filter-ronda-3 {{ filter: hue-rotate(150deg) saturate(130%) brightness(0.68) contrast(1.18); }}

        /* PANELES DE PIEDRA RUNICA Y ORO ALQUÍMICO */
        .alch-stone-panel {{
            background: #1a1c23;
            border: 4px solid #0f1116;
            border-radius: 8px;
            box-shadow: 0 6px 0 #08090b, 0 12px 20px rgba(0,0,0,0.85), inset 0 0 0 2px #393e4d;
            position: relative;
        }}

        .alch-inner-plate {{
            background: #111318;
            border: 2px solid #282c37;
            border-radius: 6px;
            box-shadow: inset 0 3px 6px rgba(0,0,0,0.7);
        }}

        .alch-banner-gold {{
            background: linear-gradient(180deg, #c99318 0%, #8c6307 100%);
            border: 3px solid #0f1116;
            border-radius: 6px;
            box-shadow: 0 4px 0 #4f3803;
            color: #ffffff;
            text-shadow: 2px 2px 0 #281d02;
        }}

        .alch-btn-gold {{
            font-family: var(--font-title);
            background: linear-gradient(180deg, #dfa92a 0%, #aa770d 100%);
            border: 3px solid #14161d;
            border-radius: 8px;
            box-shadow: 0 6px 0 #573c03, 0 8px 14px rgba(0,0,0,0.6);
            color: #ffffff;
            text-shadow: 2px 2px 0 #2d1e01;
            transition: transform 0.08s ease, box-shadow 0.08s ease;
        }}
        .alch-btn-gold:hover {{
            background: linear-gradient(180deg, #ecc045 0%, #be8913 100%);
        }}
        .alch-btn-gold:active {{
            transform: translateY(4px);
            box-shadow: 0 2px 0 #573c03, 0 3px 6px rgba(0,0,0,0.6);
        }}

        .alch-btn-transmute {{
            font-family: var(--font-title);
            background: linear-gradient(180deg, #3aa773 0%, #1f6b47 100%);
            border: 3px solid #0f1116;
            border-radius: 10px;
            box-shadow: 0 7px 0 #0d3823, 0 10px 18px rgba(0,0,0,0.7);
            color: #ffffff;
            text-shadow: 2px 2px 0 #082215;
            transition: transform 0.08s ease, box-shadow 0.08s ease;
        }}
        .alch-btn-transmute:hover {{
            background: linear-gradient(180deg, #4bc68b 0%, #298559 100%);
        }}
        .alch-btn-transmute:active {{
            transform: translateY(4px);
            box-shadow: 0 3px 0 #0d3823, 0 4px 8px rgba(0,0,0,0.7);
        }}

        /* ========================================================
           TALISMANES / FRASCOS ALQUÍMICOS (EN VEZ DE NAIPES)
           ======================================================== */
        .alch-reagent {{
            width: 108px;
            height: 154px;
            background: linear-gradient(180deg, #2b313d 0%, #1c2028 65%, #13161c 100%);
            border: 3px solid #0f1116;
            border-radius: 14px 14px 18px 18px;
            box-shadow: 0 7px 0 #090a0d, 0 12px 18px rgba(0,0,0,0.7), inset 0 0 0 2px #444c5f;
            position: relative;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            padding: 8px 6px;
            transition: transform 0.16s cubic-bezier(0.2, 0.9, 0.3, 1.2), box-shadow 0.16s ease, border-color 0.16s ease;
        }}

        /* Cuello de frasco de alquimia */
        .reagent-neck {{
            width: 44px;
            height: 9px;
            background: #b58b29;
            border: 2px solid #0f1116;
            border-radius: 4px;
            box-shadow: 0 2px 0 #5f4810, inset 0 1px 0 rgba(255,255,255,0.4);
            margin-bottom: 2px;
        }}

        /* Glifo de cabecera (Tipo de reactivo) */
        .reagent-header-glyph {{
            font-family: var(--font-title);
            font-size: 10px;
            letter-spacing: 1px;
            line-height: 1;
            padding: 2px 6px;
            border-radius: 4px;
            border: 1px solid rgba(0,0,0,0.4);
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.5);
        }}

        /* Contenedor del término central */
        .reagent-core {{
            flex-grow: 1;
            width: 90%;
            margin: 4px 0;
            background: radial-gradient(circle at center, rgba(30, 48, 41, 0.75) 0%, rgba(13, 20, 18, 0.95) 100%);
            border: 2px solid #2f3e37;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
            box-shadow: inset 0 0 12px rgba(0,0,0,0.8);
        }}

        /* Líquido mágico en el fondo del frasco */
        .reagent-liquid-glow {{
            position: absolute;
            bottom: -15px; left: -10%; width: 120%; height: 50%;
            border-radius: 50%;
            opacity: 0.35;
            filter: blur(8px);
            pointer-events: none;
        }}

        .term-math {{
            font-family: var(--font-body);
            font-size: 2.25rem;
            font-weight: bold;
            color: #ffffff;
            text-align: center;
            line-height: 1;
            letter-spacing: -0.5px;
            text-shadow: 2px 2px 0 #000, 0 0 12px rgba(255,255,255,0.3);
            z-index: 2;
        }}

        .reagent-pedestal {{
            font-family: var(--font-title);
            font-size: 8px;
            color: #a4b2c6;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }}

        /* Flotación mágica en reposo */
        @keyframes reagent-hover-1 {{
            0%, 100% {{ transform: translateY(0px) rotate(-1.5deg); }}
            50% {{ transform: translateY(-8px) rotate(1.2deg); }}
        }}
        @keyframes reagent-hover-2 {{
            0%, 100% {{ transform: translateY(-5px) rotate(1.4deg); }}
            50% {{ transform: translateY(4px) rotate(-1.6deg); }}
        }}
        @keyframes reagent-hover-3 {{
            0%, 100% {{ transform: translateY(2px) rotate(-1deg); }}
            50% {{ transform: translateY(-7px) rotate(1.6deg); }}
        }}

        .idle-sway-1 {{ animation: reagent-hover-1 3.2s ease-in-out infinite; }}
        .idle-sway-2 {{ animation: reagent-hover-2 3.8s ease-in-out infinite; }}
        .idle-sway-3 {{ animation: reagent-hover-3 4.1s ease-in-out infinite; }}

        .alch-reagent:hover {{
            transform: translateY(-16px) scale(1.06) rotate(0deg) !important;
            animation-play-state: paused;
            box-shadow: 0 14px 0 #090a0d, 0 20px 25px rgba(0,0,0,0.8), inset 0 0 0 2px #626e89;
            z-index: 20;
        }}

        /* Estado seleccionado (Activo en el caldero) */
        .alch-reagent.selected {{
            transform: translateY(-26px) scale(1.1) rotate(0deg) !important;
            animation-play-state: paused;
            border-color: #ffd447;
            box-shadow: 0 14px 0 #7e5c08, 0 0 0 3px #ffd447, 0 22px 30px rgba(0,0,0,0.9), 0 0 20px rgba(255,212,71,0.5) !important;
            z-index: 30;
        }}
        .alch-reagent.selected .reagent-core {{
            border-color: #ffd447;
            background: radial-gradient(circle at center, rgba(50, 75, 45, 0.85) 0%, rgba(18, 30, 20, 0.95) 100%);
        }}

        @media (max-width: 640px) {{
            .alch-reagent {{ width: 86px !important; height: 128px !important; }}
            .reagent-neck {{ width: 34px !important; height: 7px !important; }}
            .reagent-header-glyph {{ font-size: 8px !important; }}
            .term-math {{ font-size: 1.65rem !important; }}
            .reagent-pedestal {{ font-size: 7px !important; }}
            #hand-container {{ min-height: 180px !important; }}
        }}

        /* LLAMA DE ESENCIA TRANSMUTADA */
        @keyframes essence-burn {{
            0% {{ text-shadow: 0 0 10px #4deeea, 0 -6px 18px #22c55e, 0 -12px 25px #ffd447; transform: scale(1); }}
            50% {{ text-shadow: 0 0 25px #4deeea, 0 -10px 30px #22c55e, 0 -18px 36px #ffd447; transform: scale(1.12); }}
            100% {{ text-shadow: 0 0 10px #4deeea, 0 -6px 18px #22c55e, 0 -12px 25px #ffd447; transform: scale(1); }}
        }}
        .essence-flame {{
            color: #ffffff;
            font-family: var(--font-title);
            animation: essence-burn 0.6s infinite alternate;
        }}

        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            20% {{ transform: translateX(-8px) rotate(-3deg); }}
            40% {{ transform: translateX(8px) rotate(3deg); }}
            60% {{ transform: translateX(-8px) rotate(-3deg); }}
            80% {{ transform: translateX(8px) rotate(3deg); }}
        }}
        .animate-shake {{ animation: shake 0.35s ease-in-out; }}

        #fx-canvas {{ position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 50; }}
        .lb-scroll::-webkit-scrollbar {{ width: 5px; }}
        .lb-scroll::-webkit-scrollbar-thumb {{ background: #444c5f; border-radius: 4px; }}
    </style>
</head>
<body class="p-2 sm:p-4">
    {video_html_tag}
    <div class="bg-cauldron-overlay"></div>
    <canvas id="fx-canvas"></canvas>

    <!-- INTRO MODAL: PÓRTICO ARCANO -->
    <div id="intro-modal" class="fixed inset-0 bg-black/85 z-[1000] flex items-center justify-center p-4 backdrop-blur-sm">
        <div class="alch-stone-panel max-w-sm w-full p-6 text-center">
            <div class="alch-banner-gold py-3 px-4 mb-5 transform -rotate-1 inline-block w-full">
                <h1 class="font-pixel-title text-xl sm:text-2xl tracking-wide">ALQUIMIA ARCANA</h1>
                <p class="font-pixel-body text-sm text-yellow-100 tracking-widest mt-1">TRANSMUTACIÓN • FACTOR COMÚN</p>
            </div>
            
            <div class="alch-inner-plate p-4 mb-5 text-left">
                <label class="block font-pixel-title text-[9px] text-gray-400 mb-2 tracking-wider">NOMBRE DEL APRENDIZ:</label>
                <input type="text" id="username-input" class="w-full bg-[#090b0e] border-2 border-[#2b313e] focus:border-[#ffd447] text-[#ffd447] font-pixel-body text-xl p-3 text-center uppercase tracking-widest outline-none rounded" placeholder="TU NOMBRE" maxlength="12">
            </div>

            <button onclick="startGameFromIntro()" class="alch-btn-gold w-full py-4 text-xs sm:text-sm tracking-widest">
                INICIAR TRANSMUTACIÓN
            </button>
        </div>
    </div>

    <!-- BOTONES AUXILIARES INFERIORES -->
    <div class="fixed bottom-3 left-3 z-40">
        <button onclick="toggleTutorial()" class="alch-stone-panel font-pixel-title text-[9px] sm:text-[10px] text-yellow-300 px-3.5 py-2.5 active:translate-y-1">
            📜 GRIMORIO
        </button>
    </div>
    <div class="fixed bottom-3 right-3 z-40">
        <button onclick="toggleLeaderboard()" class="alch-stone-panel font-pixel-title text-[9px] sm:text-[10px] text-cyan-300 px-3.5 py-2.5 active:translate-y-1">
            🏆 LOGIA
        </button>
    </div>

    <!-- GRIMORIO (TUTORIAL DIDÁCTICO) -->
    <div id="tutorial-panel" class="fixed left-0 top-0 h-full w-72 sm:w-80 bg-[#14161c] border-r-4 border-[#090a0d] p-4 flex flex-col z-50 transform -translate-x-full transition-transform duration-300 shadow-2xl">
        <div class="flex justify-between items-center mb-4 border-b-2 border-white/10 pb-2">
            <div class="alch-banner-gold font-pixel-title px-3 py-1 text-[10px]">REGLAS ALQUÍMICAS</div>
            <button onclick="toggleTutorial()" class="text-white text-xl font-bold">✕</button>
        </div>
        <div class="alch-inner-plate p-3 text-2xl text-center mb-3">
            🍎🍉 <span class="text-emerald-400">+</span> 🍎🍌
        </div>
        <p class="font-pixel-title text-[9px] text-yellow-300 text-center mb-3">DESTILA EL ELEMENTO COMÚN (🍎)</p>
        <div class="alch-inner-plate p-3 text-2xl text-center mb-4">
            🍎<span class="text-gray-400">(</span>🍉 <span class="text-emerald-400">+</span> 🍌<span class="text-gray-400">)</span>
        </div>
        <div class="font-pixel-body text-base text-gray-300 leading-relaxed space-y-2">
            <p>1. Selecciona 2 o más reactivos que compartan divisores o letras con exponentes comunes.</p>
            <p>2. Presiona <b>"TRANSMUTAR"</b> para purificar la fórmula y ganar esencia alquímica.</p>
            <p>3. Los reactivos no transmutados permanecerán en tu mesa para la siguiente fase.</p>
        </div>
    </div>

    <!-- LOGIA ARCANA (RANKING DEL AULA) -->
    <aside id="leaderboard-panel" class="fixed right-0 top-0 h-full w-72 sm:w-80 bg-[#14161c] border-l-4 border-[#090a0d] p-4 flex flex-col z-50 transform translate-x-full transition-transform duration-300 shadow-2xl">
        <div class="flex justify-between items-center mb-3 border-b-2 border-white/10 pb-2">
            <button onclick="toggleLeaderboard()" class="text-white text-xl font-bold">✕</button>
            <div class="alch-banner-gold font-pixel-title px-3 py-1 text-[10px]">MAESTROS ALQUIMISTAS</div>
        </div>
        <div class="font-pixel-body text-xs text-gray-400 mb-2 text-center">APRENDICES EN VIVO • IF0003</div>
        <div id="leaderboard" class="flex-grow overflow-y-auto lb-scroll flex flex-col gap-1.5 pr-1"></div>
    </aside>

    <!-- HEADER SUPERIOR: CALDERO, RELIQUIAS Y ESENCIA -->
    <header class="flex justify-between items-center z-10 max-w-5xl mx-auto w-full gap-2 px-1">
        <div class="alch-stone-panel px-3.5 py-2 text-center min-w-[95px] sm:min-w-[125px]">
            <div class="font-pixel-title text-[8px] sm:text-[9px] text-gray-400">ETAPA <span id="level-display" class="text-yellow-400 text-xs sm:text-sm">1</span></div>
            <div class="font-pixel-title text-[7px] sm:text-[8px] text-gray-300 mt-0.5">FASE <span id="round-display" class="text-cyan-300">1</span>/3</div>
        </div>

        <!-- 3 Reliquias Mágicas (Comodines) -->
        <div class="flex justify-center gap-1.5 sm:gap-2.5">
            <button id="btn-joker-reveal" onclick="useJoker('reveal')" title="Ojo de Adivino: Detecta la esencia dominante" class="alch-stone-panel p-2 sm:p-2.5 text-base sm:text-xl relative active:translate-y-1">
                👁️
                <span id="qty-reveal" class="font-pixel-title absolute -top-2 -right-2 bg-emerald-600 text-white text-[8px] px-1 rounded-full border border-black">1</span>
            </button>
            <button id="btn-joker-reroll" onclick="useJoker('reroll')" title="Revolver Caldero: Genera nuevos reactivos" class="alch-stone-panel p-2 sm:p-2.5 text-base sm:text-xl relative active:translate-y-1">
                🌪️
                <span id="qty-reroll" class="font-pixel-title absolute -top-2 -right-2 bg-purple-600 text-white text-[8px] px-1 rounded-full border border-black">1</span>
            </button>
            <button id="btn-joker-skip" onclick="useJoker('skip')" title="Piedra Filosofal: Transmutación perfecta inmediata" class="alch-stone-panel p-2 sm:p-2.5 text-base sm:text-xl relative active:translate-y-1 opacity-40">
                💎
                <span id="qty-skip" class="font-pixel-title absolute -top-2 -right-2 bg-yellow-500 text-black text-[8px] px-1 rounded-full border border-black">0</span>
            </button>
        </div>

        <div class="alch-stone-panel px-3.5 py-2 text-center min-w-[95px] sm:min-w-[125px]">
            <div class="font-pixel-title text-[8px] sm:text-[9px] text-gray-400">ESENCIA</div>
            <div id="total-score" class="font-pixel-body text-xl sm:text-2xl text-yellow-400 leading-none mt-1">0</div>
            <div class="font-pixel-title text-[7px] text-gray-400 mt-0.5">Rango: <span id="player-rank">#25</span></div>
        </div>
    </header>

    <!-- ZONA CENTRAL DE TRANSMUTACIÓN -->
    <main class="flex-grow flex flex-col items-center justify-center relative w-full max-w-5xl mx-auto my-auto">
        <div id="hand-container" class="flex justify-center items-center flex-wrap gap-2.5 sm:gap-4 w-full px-2 mb-6"></div>

        <button id="btn-play" onclick="playHand()" disabled class="alch-stone-panel bg-[#15171d] text-gray-500 font-pixel-title px-8 py-3.5 sm:px-12 sm:py-4 text-xs sm:text-sm tracking-widest opacity-40 cursor-not-allowed">
            TRANSMUTAR
        </button>

        <div id="flame-score-container" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 hidden opacity-0 transition-opacity duration-300 z-40 pointer-events-none text-center">
            <div id="flame-score" class="text-3xl sm:text-5xl essence-flame tracking-wider drop-shadow-[0_0_35px_#4deeea]">0</div>
        </div>
    </main>

    <!-- MODAL FIN DE ETAPA -->
    <div id="level-modal" class="fixed inset-0 bg-black/85 z-50 hidden flex items-center justify-center backdrop-blur-sm p-4">
        <div class="alch-stone-panel max-w-sm w-full p-6 text-center">
            <div class="alch-banner-gold py-2 px-4 mb-4 transform -rotate-1 inline-block w-full">
                <h2 class="font-pixel-title text-lg sm:text-xl">ETAPA PURIFICADA</h2>
            </div>
            <div class="flex justify-center gap-3 my-4" id="modal-stars"></div>
            <p id="modal-desc" class="alch-inner-plate p-3 text-gray-200 font-pixel-body text-base leading-relaxed mb-5"></p>
            <button onclick="nextLevel()" class="alch-btn-gold w-full py-3.5 text-xs tracking-wider">
                SIGUIENTE ETAPA ➔
            </button>
        </div>
    </div>

    <!-- ALERTA ARCANAS -->
    <div id="alert-modal" class="fixed top-12 left-1/2 -translate-x-1/2 alch-banner-gold font-pixel-body text-base sm:text-lg px-5 py-2.5 z-50 hidden transition-opacity text-center max-w-[90vw]">
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
            hover: () => playTone(360, 'sine', 0.08, 0.03),
            select: () => playTone(580, 'triangle', 0.12, 0.12),
            error: () => {{ playTone(120, 'sawtooth', 0.25, 0.25); setTimeout(() => playTone(80, 'sawtooth', 0.35, 0.25), 100); }},
            flamePop: () => {{ playTone(220, 'sine', 0.35, 0.3); setTimeout(() => playTone(330, 'triangle', 0.25, 0.25), 60); }},
            star: () => {{ playTone(880, 'sine', 0.3, 0.2); setTimeout(()=>playTone(1174, 'sine', 0.4, 0.2), 100); }},
            discard: () => playTone(260, 'triangle', 0.15, 0.15),
            winRound: () => {{ playTone(523, 'sine', 0.3, 0.2); setTimeout(() => playTone(784, 'sine', 0.3, 0.2), 150); }}
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
            const colors = ['#4deeea', '#ffd447', '#22c55e', '#ffffff', '#9d4edd'];
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

        const names = ["Alquimista_U", "Fabiola_P", "Bryan_Q", "Daniela_CR", "Nath_V", "Isaac_H", "Carlos_S", "M_Estela", "K_Navas", "Diego_R", "K_Mora", "Josue_B", "Maria_F", "Valeria_G", "Seidy_T", "Allan_P", "Cesar_O", "Monica_V", "Lucia_Z", "R_Arias", "Erick_L", "S_Díaz", "Karla_C", "Luis_M"];
        let leaderboardData = [];
        let playerName = "APRENDIZ";
        
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
                div.className = `flex justify-between items-center text-sm p-1.5 rounded ${{p.isPlayer ? 'bg-[#1b4332] text-[#ffd447] border border-[#ffd447] font-bold' : 'alch-inner-plate text-gray-300'}}`;
                div.innerHTML = `
                    <span class="truncate max-w-[130px] font-pixel-body">${{medal}} ${{p.name}} ${{p.isPlayer ? '(TÚ)' : ''}}</span>
                    <span class="text-yellow-400 font-pixel-body font-bold">${{p.score.toLocaleString()}}</span>
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

        function getReagentMetadata(card) {{
            if (card.x > 0 && card.y === 0) return {{ rune: card.x === 1 ? "X" : `X${{card.x}}`, type: "AZUFRE", color: "#eab308", glow: "#ca8a04" }};
            if (card.y > 0 && card.x === 0) return {{ rune: card.y === 1 ? "Y" : `Y${{card.y}}`, type: "MERCURIO", color: "#38bdf8", glow: "#0284c7" }};
            if (card.x > 0 && card.y > 0) return {{ rune: "XY", type: "ETHER", color: "#c084fc", glow: "#9333ea" }};
            return {{ rune: Math.abs(card.c).toString(), type: "SAL", color: "#4ade80", glow: "#16a34a" }};
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
                el.className = `alch-reagent ${{card.selected ? 'selected' : swayClass}}`;
                
                const meta = getReagentMetadata(card);

                el.innerHTML = `
                    <div class="reagent-neck"></div>
                    <div class="reagent-header-glyph" style="background: ${{meta.color}}22; color: ${{meta.color}}; border-color: ${{meta.color}}66;">
                        ${{meta.rune}}
                    </div>
                    <div class="reagent-core">
                        <div class="reagent-liquid-glow" style="background: ${{meta.glow}};"></div>
                        <div class="term-math">${{card.str}}</div>
                    </div>
                    <div class="reagent-pedestal">${{meta.type}}</div>
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
                btnPlay.className = "alch-btn-transmute px-8 py-3.5 sm:px-12 sm:py-4 text-xs sm:text-sm tracking-widest cursor-pointer";
            }} else {{
                btnPlay.disabled = true;
                btnPlay.className = "alch-stone-panel bg-[#15171d] text-gray-500 font-pixel-title px-8 py-3.5 sm:px-12 sm:py-4 text-xs sm:text-sm tracking-widest opacity-40 cursor-not-allowed";
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
            flameScore.textContent = "+" + handScore.toLocaleString() + " ESENCIA";
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
                    starContainer.innerHTML += `<span class="text-yellow-400 text-3xl sm:text-4xl drop-shadow-[0_4px_0_#573c03]">★</span>`;
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
                desc.innerHTML = `¡PURIFICACIÓN PERFECTA!<br>Obtuviste la reliquia PIEDRA FILOSOFAL.<br>Bono arcano: +${{bonusScore.toLocaleString()}} esencia`;
            }} else {{
                desc.innerHTML = `Precisión: ${{Math.round(precision*100)}}%. Quedaron reactivos sin destilar.<br>Bono arcano: +${{bonusScore.toLocaleString()}} esencia`;
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
                    showAlert(`👁️ FACTOR DOMINANTE: <b>${{bestFactor}}</b> (en ${{maxSubset}} reactivos)`);
                }} else {{
                    showAlert(`👁️ No hay factores comunes detectables en esta mesa.`);
                }}
            }} 
            else if (type === 'reroll') {{
                comodines.reroll--;
                SFX.discard();
                hand = [];
                startRound();
                showAlert("🌪️ ¡CALDERO REVUELTO!");
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
    st.header("⚗️ Alquimia: Factor Común")
    st.caption("UCR • IF0003 Matemática Básica")
    st.markdown(
        """
        **Mecánica Didáctica:**
        - **3 Fases por Etapa:** La complejidad de los reactivos monomios escala.
        - **Factor Común:** Extraer el MCD numérico y las variables comunes de menor exponente.
        - **Persistencia:** Los reactivos no transmutados se conservan en la siguiente fase.
        """
    )
