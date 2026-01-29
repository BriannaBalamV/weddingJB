from __future__ import annotations

import base64
import textwrap  # ✅ ADDED (fix HTML being shown as code block)
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# CONFIG (EDIT THIS)
# =========================================================
@dataclass
class EventInfo:
    title: str
    date_str: str
    time_str: str
    place: str
    maps_url: str


COUPLE_1 = "Jesús Alberto"
COUPLE_2 = "Brianna Ayelen"
EVENT_DATE_TIME = "2026-03-22 12:00:00"   # YYYY-MM-DD HH:MM:SS (for countdown)

HERO_SUBTITLE = "NO FALTES A NUESTRA BODA"
HERO_DATE_TEXT = "22 MARZO, 2026"

INTRO_TITLE = "¡Nos Casamos!"
INTRO_TEXT = (
    "Después de escribir juntos una hermosa historia de amor, "
    "con el corazón lleno de gratitud compartimos esta gran noticia.\n\n"
    
    "Dios, en Su perfecto tiempo, unió nuestros caminos, "
    "fortaleció nuestra unión y nos enseñó a amar con fe y bajo Su bendición,"
    "decidimos unir nuestras vidas y comenzar una nueva etapa.\n\n"

    "Nos complace invitarte a celebrar el comienzo de una nueva etapa en nuestras vidas..."
)

PARENTS_NOVIO = ["Jesús Tejeda", "Evelin Sanchez"]
PARENTS_NOVIA = ["Vladimir Balam", "Enalyn Velasco"]
PADRINOS = ["Dalyn Velasco Pérez", "si"]

CEREMONIA = EventInfo(
    title="Ceremonia y Recepción",
    date_str="Domingo, 22 de Marzo de 2026",
    time_str="12:00 p.m.",
    place="Hotel Posada Señorial Cholula, Puebla",
    maps_url="https://maps.app.goo.gl/trKVWXCfvHpht5gG8",
)

# ✅ FIX: RECEPCION was referenced later but not defined
RECEPCION = CEREMONIA

# ✅ UPDATED ONLY: Dress code content (as requested)
DRESS_CODE = "<b>ETIQUETA</b>"
DRESS_NOTE = (
    "El color <b>blanco</b> esta reservado para la novia.<br><br>"
)

WHATSAPP_E164 = "52" + "9991943438"  # digits only, no '+' and no spaces
RSVP_TITLE = "Confirmación de Asistencia al Evento"

THANKS_TEXT = "Muchas gracias por su atención. Esperamos contar con su presencia."
FOOTER_LINE_1 = "Con cariño"
FOOTER_LINE_2 = f"{COUPLE_1} & {COUPLE_2}"

# Theme
THEME_TEXT = "#f5f0e8"
THEME_ACCENT = "#d7c29a"     # gold-ish
CARD_BG = "transparent"
CARD_TEXT = "#ffffff"
THEME_OVERLAY = "rgba(0,0,0,0.55)"


# =========================================================
# Assets (AUTO-DETECT)
# Accepts: .jpg .jpeg .png .webp
# =========================================================
ASSETS = Path(__file__).parent / "assets"
IMG_EXTS = ("jpg", "jpeg", "png", "webp")


def pick_asset(stem: str) -> Path | None:
    for ext in IMG_EXTS:
        p = ASSETS / f"{stem}.{ext}"
        if p.exists():
            return p
    return None


HERO_IMG = pick_asset("hero")
BG_IMG = pick_asset("bg")               # optional
STORY_LEFT_IMG = pick_asset("story_left")
STORY_RIGHT_IMG = pick_asset("story_right")

MUSIC_FILE = ASSETS / "song.mp3"        # optional (mp3)


def gallery_files(max_items: int = 8) -> list[Path]:
    files: list[Path] = []
    for ext in IMG_EXTS:
        files += sorted(ASSETS.glob(f"gallery*.{ext}"))
    # de-dup + stable order
    seen: set[Path] = set()
    out: list[Path] = []
    for f in files:
        r = f.resolve()
        if r in seen:
            continue
        seen.add(r)
        out.append(f)
    return out[:max_items]


# =========================================================
# Helpers
# =========================================================
def mime_for(path: Path) -> str:
    suf = path.suffix.lower().lstrip(".")
    if suf == "jpg":
        suf = "jpeg"
    if suf in ("jpeg", "png", "webp"):
        return f"image/{suf}"
    return "application/octet-stream"


def data_uri(path: Path) -> str:
    b = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime_for(path)};base64,{b}"


def audio_uri_mp3(path: Path) -> str:
    b = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:audio/mpeg;base64,{b}"


def wa_link(phone_e164: str, msg: str) -> str:
    return f"https://wa.me/{phone_e164}?text={quote(msg)}"

# ✅ ADDED: Auto-resize script (This helps fix gaps if supported)
AUTO_RESIZE_SCRIPT = """
<script>
  function resizeIframe() {
    const body = document.body;
    const height = body.scrollHeight;
    window.parent.postMessage({type: 'streamlit:setFrameHeight', height: height}, '*');
  }
  window.addEventListener('load', resizeIframe);
  window.addEventListener('resize', resizeIframe);
  setTimeout(resizeIframe, 300);
</script>
"""

# =========================================================
# Page
# =========================================================
st.set_page_config(page_title=f"{COUPLE_1} & {COUPLE_2}", page_icon="💍", layout="wide")

hero_uri = data_uri(HERO_IMG) if HERO_IMG else ""
bg_uri = data_uri(BG_IMG) if BG_IMG else ""
left_uri = data_uri(STORY_LEFT_IMG) if STORY_LEFT_IMG else ""
right_uri = data_uri(STORY_RIGHT_IMG) if STORY_RIGHT_IMG else ""
music_uri = audio_uri_mp3(MUSIC_FILE) if MUSIC_FILE.exists() else ""

gal_paths = gallery_files(8)
gal_uris = [data_uri(p) for p in gal_paths]

# Global CSS
st.markdown(
    f"""
<style>
/* ✅ Wedding invitation fonts (apply to ALL invitation) */
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Cormorant+Garamond:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {{
  font-family: 'Cormorant Garamond', serif;
}}

.stApp {{
  background: linear-gradient({THEME_OVERLAY}, {THEME_OVERLAY}){"," if bg_uri else ""} {f'url("{bg_uri}")' if bg_uri else ""};
  background-size: cover;
  background-attachment: fixed;
  background-position: center center;
  background-repeat: no-repeat;
}}

.section {{
  width: 100%;
  border-radius: 22px;
  padding: 44px 36px;
  margin: 18px 0;
}}

.h-serif {{
  font-family: 'Cinzel', serif;
  color: {THEME_TEXT};
}}

.p-muted {{
  color: rgba(245,240,232,0.88);
}}

.hr-soft {{
  border: none;
  height: 1px;
  background: rgba(255,255,255,0.18);
  margin: 18px 0;
}}

.card {{
  background: {CARD_BG};
  color: {CARD_TEXT};
  border-radius: 16px;
  padding: 18px 18px;
  box-shadow: 0 10px 26px rgba(0,0,0,0.18);
}}

.btn-link {{
  display: inline-block;
  background: #111;
  color: #fff;
  padding: 10px 16px;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 600;
}}

.small-center {{
  text-align: center;
}}

.gold {{
  color: {THEME_ACCENT};
}}

.icon-big {{
  font-size: 36px;
  line-height: 1;
}}

/* ✅ RSVP form styling (transparent card + form look) */
div[data-testid="stForm"] {{
  background: transparent !important;
  border: 1px solid rgba(245,240,232,0.22);
  border-radius: 18px;
  padding: 18px 18px 14px 18px;
  box-shadow: 0 10px 26px rgba(0,0,0,0.18);
}}

div[data-testid="stForm"] label {{
  color: rgba(245,240,232,0.92) !important;
  font-style: italic;
  font-size: 16px;
}}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
div[data-testid="stNumberInput"] input {{
  background: rgba(255,255,255,0.10) !important;
  color: rgba(245,240,232,0.95) !important;
  border: 1px solid rgba(245,240,232,0.20) !important;
  border-radius: 12px !important;
}}

div[data-testid="stTextArea"] textarea {{
  min-height: 140px !important;
}}

div[data-testid="stSelectbox"] svg {{
  fill: rgba(245,240,232,0.9) !important;
}}

div[data-testid="stFormSubmitButton"] button {{
  width: 100% !important;
  background: rgba(215,194,154,0.78) !important;
  color: #111 !important;
  border: none !important;
  border-radius: 12px !important;
  padding: 0.65rem 1rem !important;
  font-weight: 700 !important;
}}

div[data-testid="stFormSubmitButton"] button:hover {{
  filter: brightness(1.05);
  transform: translateY(-1px);
}}

/* =========================
   Fancy scroll animations
   ========================= */
@media (prefers-reduced-motion: reduce) {{
  .reveal-target,
  .reveal-target.reveal-in,
  .reveal-child,
  .reveal-in .reveal-child {{
    opacity: 1 !important;
    transform: none !important;
    filter: none !important;
    transition: none !important;
  }}
}}

.reveal-target {{
  opacity: 0;
  transform: translateY(22px) scale(0.985);
  filter: blur(8px);
  transition:
    opacity 850ms cubic-bezier(.2,.8,.2,1),
    transform 850ms cubic-bezier(.2,.8,.2,1),
    filter 900ms cubic-bezier(.2,.8,.2,1);
  will-change: opacity, transform, filter;
}}

.reveal-target.reveal-in {{
  opacity: 1;
  transform: translateY(0) scale(1);
  filter: blur(0);
}}

.reveal-left {{
  transform: translateX(-26px) translateY(10px) scale(0.985);
}}
.reveal-right {{
  transform: translateX(26px) translateY(10px) scale(0.985);
}}
.reveal-pop {{
  transform: translateY(18px) scale(0.97);
}}

.reveal-child {{
  opacity: 0;
  transform: translateY(10px);
  filter: blur(6px);
  transition:
    opacity 650ms cubic-bezier(.2,.8,.2,1),
    transform 650ms cubic-bezier(.2,.8,.2,1),
    filter 750ms cubic-bezier(.2,.8,.2,1);
  transition-delay: var(--d, 0ms);
  will-change: opacity, transform, filter;
}}

.reveal-in .reveal-child {{
  opacity: 1;
  transform: translateY(0);
  filter: blur(0);
}}

.card, .btn-link {{
  transition: transform 220ms ease, box-shadow 220ms ease, filter 220ms ease;
}}

.card:hover {{
  transform: translateY(-2px);
  box-shadow: 0 18px 44px rgba(0,0,0,0.35);
}}

.btn-link:hover {{
  transform: translateY(-1px);
  filter: brightness(1.05);
}}

/* ✅ FIX MOBILE EMPTY SPACES (ONLY ON PHONE) */
@media (max-width: 768px) {{
  /* iOS Safari often creates weird spacing with fixed backgrounds */
  .stApp {{
    background-attachment: scroll !important;
  }}

  /* Reduce Streamlit default block gaps */
  div[data-testid="stVerticalBlock"] {{
    gap: 0.35rem !important;
  }}

  /* Many Streamlit blocks wrap in element-container with bottom margin */
  .element-container {{
    margin-bottom: 0.35rem !important;
  }}

  /* Sections tighter on mobile */
  .section {{
    padding: 20px 14px !important;
    margin: 8px 0 !important;
  }}

  .hr-soft {{
    margin: 12px 0 !important;
  }}
}}
</style>
""",
    unsafe_allow_html=True,
)

# ✅ Fancy scroll animations JS (targets parent DOM)
components.html(
    """
<script>
(function () {
  try {
    const doc = window.parent.document;

    const obs = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add("reveal-in");
          obs.unobserve(e.target);
        }
      });
    }, {
      threshold: 0.14,
      rootMargin: "0px 0px -12% 0px"
    });

    function staggerChildren(el) {
      const kids = Array.from(el.querySelectorAll(":scope > *"));
      kids.forEach((k, i) => {
        k.classList.add("reveal-child");
        k.style.setProperty("--d", `${Math.min(i, 8) * 90}ms`);
      });
    }

    function setup() {
      const sections = Array.from(doc.querySelectorAll(".section"));
      const cards = Array.from(doc.querySelectorAll(".card"));

      sections.forEach((el, i) => {
        if (!el.classList.contains("reveal-target")) {
          el.classList.add("reveal-target");
          el.classList.add(i % 2 === 0 ? "reveal-left" : "reveal-right");
          staggerChildren(el);
          obs.observe(el);
        }
      });

      cards.forEach((el) => {
        if (!el.classList.contains("reveal-target")) {
          el.classList.add("reveal-target", "reveal-pop");
          staggerChildren(el);
          obs.observe(el);
        }
      });
    }

    setup();
    setTimeout(setup, 450);
    setTimeout(setup, 1200);

    const mo = new MutationObserver(() => setup());
    mo.observe(doc.body, { childList: true, subtree: true });

  } catch (err) {
    console.warn("Fancy scroll reveal init failed:", err);
  }
})();
</script>
""",
    height=1,
)

# =========================================================
# HERO with AUTOPLAY (best-effort)
# =========================================================
if not hero_uri:
    st.error("Missing hero image. Add one of: assets/hero.jpg | hero.jpeg | hero.png | hero.webp")
else:
    hero_html = f"""
    <div id="hero" style="
      width:100%;
      height:92vh;
      min-height:550px;
      max-height: 800px;
      border-radius:24px;
      overflow:hidden;
      position:relative;
      background-image:
        linear-gradient({THEME_OVERLAY}, {THEME_OVERLAY}),
        url('{hero_uri}');
      background-size:cover;
      background-position:center 38%;
      box-shadow: 0 14px 40px rgba(0,0,0,0.35);
    ">

      <div style="
        position:absolute; inset:0;
        display:flex; flex-direction:column;
        align-items:center; justify-content:flex;
        padding: 90px 20px;

        text-align:center; padding: 20px;
      ">
        <div style="font-family:'Cinzel',serif; font-size: clamp(44px, 6vw, 92px); font-weight:700; color:{THEME_TEXT}; letter-spacing:1px;">
          {COUPLE_1} <span style="color:{THEME_ACCENT}; font-weight:600;">&</span> {COUPLE_2}
        </div>

        <div style="margin-top:10px; font-size: 14px; letter-spacing:2px; color: rgba(245,240,232,0.9); font-weight:600;">
          {HERO_SUBTITLE}
        </div>

        <div style="margin-top:14px; font-size: 20px; color: rgba(245,240,232,0.95);">
          {HERO_DATE_TEXT}
        </div>

        <div id="tapNote" style="
          margin-top:18px;
          padding:8px 12px;
          border-radius: 999px;
          background: rgba(0,0,0,0.35);
          color: rgba(245,240,232,0.92);
          font-size: 12px;
          display:none;
        ">
          Toca en cualquier parte para activar la música 🔊
        </div>
      </div>

      <div style="position:absolute; right:16px; top:50%; transform:translateY(-50%);">
        <button id="musicBtn"
          style="
            width:48px; height:48px; border-radius:12px;
            border:none; cursor:pointer;
            background: rgba(0,0,0,0.55);
            color: white; font-size: 22px;
            box-shadow: 0 10px 24px rgba(0,0,0,0.25);
          "
          title="Música"
        >🔈</button>
      </div>

      <audio id="bgm" {'src="' + music_uri + '"' if music_uri else ''} autoplay loop playsinline></audio>

      <script>
        const btn = document.getElementById("musicBtn");
        const audio = document.getElementById("bgm");
        const note = document.getElementById("tapNote");

        let playing = false;

        function setIcon() {{
          btn.innerText = playing ? "🔊" : "🔈";
        }}

        function showNote(show) {{
          note.style.display = show ? "inline-block" : "none";
        }}

        async function tryPlay(unmuted) {{
          if (!audio || !audio.src) {{
            showNote(false);
            return;
          }}
          audio.loop = true;
          audio.muted = !unmuted;

          try {{
            await audio.play();
            playing = true;
            setIcon();
            showNote(false);
          }} catch (e) {{
            playing = false;
            setIcon();
            showNote(true);
          }}
        }}

        window.addEventListener("load", () => {{
          tryPlay(false); // muted autoplay
        }});

        document.addEventListener("click", () => {{
          tryPlay(true);
        }}, {{ once: true }});

        btn.addEventListener("click", async (e) => {{
          e.stopPropagation();
          if (!audio || !audio.src) {{
            alert("No hay música cargada. Sube assets/song.mp3");
            return;
          }}
          if (!playing) {{
            await tryPlay(true);
          }} else {{
            audio.pause();
            playing = false;
            setIcon();
          }}
        }});

        setIcon();
      </script>
    </div>
    """
    # ✅ FIX: height=600 (RESTORED) + append auto-resize script
    components.html(hero_html + AUTO_RESIZE_SCRIPT, height=600)

# =========================================================
# INTRO
# =========================================================
st.markdown(
    f"""
<div class="section">
  <div class="small-center">
    <div class="h-serif" style="font-size:56px; font-weight:700;">{INTRO_TITLE}</div>
    <div class="p-muted" style="max-width: 900px; margin: 14px auto 0; font-size:18px;">
      {INTRO_TEXT}
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# =========================================================
# STORY + CALENDAR + COUNTDOWN (center)
# =========================================================
countdown_html = f"""
<style>
  html, body {{ margin:0; padding:0; }}

  .cal-title {{
    text-align:center;
    font-family:'Cinzel',serif;
    color: {THEME_TEXT};
    margin-bottom: 10px;
  }}
  .cal-title .big {{
    font-size: 44px;
    font-weight: 700;
    line-height: 1;
  }}
  .cal-title .small {{
    font-size: 28px;
    font-weight: 400;
    opacity: .95;
  }}

  .cal-box {{
    width:100%;
    max-width: 520px;
    margin: 0 auto 14px auto;
    padding: 14px 14px 10px 14px;
    box-sizing: border-box;
    border: 2px solid rgba(215,194,154,0.55);
    border-radius: 14px;
    background: rgba(0,0,0,0.18);
  }}

  .dow {{
    display:grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 8px;
    margin-bottom: 8px;
    font-family:'Cormorant Garamond',serif;
    color: rgba(245,240,232,0.85);
    font-size: 14px;
    letter-spacing: .6px;
    text-align:center;
  }}

  .grid {{
    display:grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 8px;
  }}

  .cell {{
    height: 34px;
    border-radius: 10px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-family:'Cormorant Garamond',serif;
    color: rgba(245,240,232,0.92);
    font-size: 15px;
    background: rgba(255,255,255,0.03);
  }}

  .empty {{
    background: transparent;
  }}

  .target {{
    position: relative;
    border: 2px solid rgba(215,194,154,0.95);
    background: rgba(215,194,154,0.10);
    font-weight: 600;
  }}

  .target::after {{
    content: "♡";
    position: absolute;
    top: -10px;
    right: -8px;
    font-size: 14px;
    color: rgba(215,194,154,0.95);
  }}
</style>

<div class="cal-title">
  <div class="big" id="calDay">--</div>
  <div class="small"><span id="calMonthName">--</span> <span style="opacity:.85;">de</span> <span id="calYear">----</span></div>
</div>

<div class="cal-box">
  <div class="dow">
    <div>Lu</div><div>Ma</div><div>Mi</div><div>Ju</div><div>Vi</div><div>Sá</div><div>Do</div>
  </div>
  <div class="grid" id="calGrid"></div>
</div>

<div style="
  width:100%;
  max-width: 520px;
  margin: 0 auto;
  box-sizing: border-box;
  border: 2px solid rgba(215,194,154,0.65);
  border-radius: 14px;
  padding: 14px 10px;
  background: rgba(0,0,0,0.25);
  color: {THEME_TEXT};
  font-family: 'Cinzel', serif;
">
  <div style="display:flex; justify-content:space-around; gap:10px; text-align:center;">
    <div><div id="d" style="font-size:26px; font-weight:700;">--</div><div style="opacity:.9;">Días</div></div>
    <div><div id="h" style="font-size:26px; font-weight:700;">--</div><div style="opacity:.9;">Hrs</div></div>
    <div><div id="m" style="font-size:26px; font-weight:700;">--</div><div style="opacity:.9;">Mins</div></div>
    <div><div id="s" style="font-size:26px; font-weight:700;">--</div><div style="opacity:.9;">Segs</div></div>
  </div>
</div>

<script>
  const targetDate = new Date("{EVENT_DATE_TIME.replace(" ", "T")}");
  const targetMs = targetDate.getTime();

  const monthNames = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"];

  const y = targetDate.getFullYear();
  const m = targetDate.getMonth();
  const day = targetDate.getDate();

  document.getElementById("calDay").innerText = String(day).padStart(2,"0");
  document.getElementById("calMonthName").innerText = monthNames[m];
  document.getElementById("calYear").innerText = y;

  const first = new Date(y, m, 1);
  const startDow = (first.getDay() + 6) % 7;
  const daysInMonth = new Date(y, m + 1, 0).getDate();

  const grid = document.getElementById("calGrid");
  grid.innerHTML = "";

  for (let i=0; i<startDow; i++) {{
    const div = document.createElement("div");
    div.className = "cell empty";
    grid.appendChild(div);
  }}

  for (let d=1; d<=daysInMonth; d++) {{
    const div = document.createElement("div");
    div.className = "cell" + (d === day ? " target" : "");
    div.innerText = d;
    grid.appendChild(div);
  }}

  function tick() {{
    const now = new Date().getTime();
    let diff = Math.max(0, targetMs - now);

    const days = Math.floor(diff / (1000*60*60*24));
    diff -= days * (1000*60*60*24);
    const hrs = Math.floor(diff / (1000*60*60));
    diff -= hrs * (1000*60*60);
    const mins = Math.floor(diff / (1000*60));
    diff -= mins * (1000*60);
    const secs = Math.floor(diff / 1000);

    document.getElementById("d").innerText = days;
    document.getElementById("h").innerText = hrs;
    document.getElementById("m").innerText = mins;
    document.getElementById("s").innerText = secs;
  }}

  tick();
  setInterval(tick, 1000);
</script>
"""

colL, colC, colR = st.columns([1.2, 1.0, 1.2], vertical_alignment="center", gap="large")
with colL:
    if left_uri:
        st.image(left_uri, use_container_width=True)
    else:
        st.info("Add story_left.jpg/.jpeg/.png/.webp in assets/")
with colC:
    # ✅ FIX: height=720 (RESTORED) + append auto-resize script
    components.html(countdown_html + AUTO_RESIZE_SCRIPT, height=720)
with colR:
    if right_uri:
        st.image(right_uri, use_container_width=True)
    else:
        st.info("Add story_right.jpg/.jpeg/.png/.webp in assets/")

# =========================================================
# PARENTS / PADRINOS
# =========================================================
st.markdown(
f"""<div class="section">
<div class="h-serif small-center" style="font-size:35px; font-weight:600;">
¡Celebra con nosotros este día tan maravilloso!
</div>

<div class="hr-soft"></div>

<div style="display:flex; gap:20px; justify-content:space-between; flex-wrap:wrap; margin-top: 10px;">

<div style="flex:1; min-width: 220px; text-align:center;">
<div class="h-serif" style="font-size:22px; font-weight:600;">Padres de la Novia</div>
<div class="p-muted" style="margin-top:10px; font-size:18px;">
{PARENTS_NOVIA[0]}<br><span class="gold">&</span><br>{PARENTS_NOVIA[1]}
</div>
</div>

<div style="flex:1; min-width: 220px; text-align:center;">
<div class="h-serif" style="font-size:22px; font-weight:600;">Padres del Novio</div>
<div class="p-muted" style="margin-top:10px; font-size:18px;">
{PARENTS_NOVIO[0]}<br><span class="gold">&</span><br>{PARENTS_NOVIO[1]}
</div>
</div>

<div style="flex:1; min-width: 220px; text-align:center;">
<div class="h-serif" style="font-size:22px; font-weight:600;">Padrinos</div>
<div class="p-muted" style="margin-top:10px; font-size:18px;">
{PADRINOS[0]}<br><span class="gold">&</span><br>{PADRINOS[1]}
</div>
</div>

</div>
</div>""",
unsafe_allow_html=True,
)

# =========================================================
# CEREMONIA / RECEPCION
# =========================================================
c2 = st.container()
with c2:
    st.markdown(
        f"""
<div class="card small-center">
  <div class="icon-big">🥂</div>
  <div class="h-serif" style="font-size:28px; font-weight:600; margin-top:6px;">
    {RECEPCION.title}
  </div>
  <div style="margin-top:12px; font-size:18px;">
    <div><b>{RECEPCION.date_str}</b></div>
    <div style="margin-top:2px;">{RECEPCION.time_str}</div>
    <div style="margin-top:12px;">{RECEPCION.place}</div>
  </div>
  <div style="margin-top:14px;">
    <a class="btn-link" href="{RECEPCION.maps_url}" target="_blank">Ver mapa!</a>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

# =========================================================
# DRESS CODE ✅ (icons rendered correctly)
# =========================================================
DRESS_ICON_SVG = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <path d="M22 18
           Q26 12 32 12
           Q38 12 42 18
           L38 26
           L44 54
           Q32 58 20 54
           L26 26
           Z"
        fill="none"
        stroke="{THEME_TEXT}"
        stroke-width="2.8"
        stroke-linecap="round"
        stroke-linejoin="round"/>
  <path d="M27 16 Q32 19 37 16"
        fill="none"
        stroke="{THEME_ACCENT}"
        stroke-width="2.2"
        stroke-linecap="round"
        opacity="0.95"/>
  <path d="M26 26 Q32 30 38 26"
        fill="none"
        stroke="{THEME_ACCENT}"
        stroke-width="2.2"
        stroke-linecap="round"
        opacity="0.9"/>
</svg>"""

TUX_ICON_SVG = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<path d="M26 12h12" fill="none" stroke="{THEME_TEXT}" stroke-width="2.6" stroke-linecap="round"/>
<path d="M26 12l6 10 6-10" fill="none" stroke="{THEME_ACCENT}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M20 20l6-8 6 10-6 10-6-8" fill="none" stroke="{THEME_TEXT}" stroke-width="2.6" stroke-linejoin="round"/>
<path d="M44 20l-6-8-6 10 6 10 6-8" fill="none" stroke="{THEME_TEXT}" stroke-width="2.6" stroke-linejoin="round"/>
<path d="M28 22v30c0 2 8 2 8 0V22" fill="none" stroke="{THEME_TEXT}" stroke-width="2.6" stroke-linecap="round"/>
<path d="M28 32h8" fill="none" stroke="{THEME_ACCENT}" stroke-width="2.2" stroke-linecap="round" opacity="0.9"/>
<path d="M24 54h16" fill="none" stroke="{THEME_TEXT}" stroke-width="2.6" stroke-linecap="round" opacity="0.9"/>
</svg>"""

dress_icon_uri = "data:image/svg+xml;base64," + base64.b64encode(DRESS_ICON_SVG.encode("utf-8")).decode("utf-8")
tux_icon_uri = "data:image/svg+xml;base64," + base64.b64encode(TUX_ICON_SVG.encode("utf-8")).decode("utf-8")

st.markdown(
    textwrap.dedent(f"""<div class="section">
  <div class="h-serif small-center" style="font-size:40px; font-weight:600; text-transform:uppercase; letter-spacing:1px;">
    CÓDIGO DE VESTIMENTA.
  </div>

  <div class="h-serif small-center" style="margin-top:14px; font-size:30px; font-weight:500; letter-spacing:6px; text-transform:uppercase; opacity:.95;">
    {DRESS_CODE}
  </div>

  <div style="margin-top:18px; display:flex; justify-content:center; align-items:center; gap:46px;">
    <img src="{dress_icon_uri}" style="width:96px; height:96px; display:block;" />
    <img src="{tux_icon_uri}" style="width:96px; height:96px; display:block;" />
  </div>

  <div class="small-center p-muted" style="margin-top:18px; font-size:22px; line-height:1.25;">
    {DRESS_NOTE}
  </div>
</div>""").lstrip(),
    unsafe_allow_html=True,
)

# =========================================================
# REGALOS ✅ (new section)
# =========================================================
GIFT_ICON_SVG = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 130">
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <rect x="22" y="46" width="86" height="58" rx="10" stroke="{THEME_ACCENT}" stroke-width="2.6" opacity="0.95"/>
    <path d="M22 54 L65 84 L108 54" stroke="{THEME_ACCENT}" stroke-width="2.6" opacity="0.95"/>
    <path d="M22 104 L60 78" stroke="{THEME_ACCENT}" stroke-width="2.2" opacity="0.6"/>
    <path d="M108 104 L70 78" stroke="{THEME_ACCENT}" stroke-width="2.2" opacity="0.6"/>

    <path d="M65 75
             C62 69 54 69 54 76
             C54 83 65 90 65 90
             C65 90 76 83 76 76
             C76 69 68 69 65 75 Z"
          fill="{THEME_ACCENT}" opacity="0.55" stroke="none"/>

    <rect x="132" y="46" width="86" height="58" rx="10" stroke="{THEME_ACCENT}" stroke-width="2.6" opacity="0.95"/>
    <path d="M132 54 L175 84 L218 54" stroke="{THEME_ACCENT}" stroke-width="2.6" opacity="0.95"/>
    <path d="M132 104 L170 78" stroke="{THEME_ACCENT}" stroke-width="2.2" opacity="0.6"/>
    <path d="M218 104 L180 78" stroke="{THEME_ACCENT}" stroke-width="2.2" opacity="0.6"/>

    <path d="M175 75
             C172 69 164 69 164 76
             C164 83 175 90 175 90
             C175 90 186 83 186 76
             C186 69 178 69 175 75 Z"
          fill="{THEME_ACCENT}" opacity="0.55" stroke="none"/>

    <path d="M60 46 Q65 36 75 36" stroke="{THEME_TEXT}" stroke-width="2.0" opacity="0.25"/>
    <path d="M180 46 Q175 36 165 36" stroke="{THEME_TEXT}" stroke-width="2.0" opacity="0.25"/>
  </g>
</svg>"""

gift_icon_uri = "data:image/svg+xml;base64," + base64.b64encode(GIFT_ICON_SVG.encode("utf-8")).decode("utf-8")

st.markdown(
    textwrap.dedent(f"""<div class="section">
  <div class="h-serif small-center" style="font-size:48px; font-weight:600;">Regalos</div>

  <div class="small-center p-muted" style="margin-top: 16px; font-size:24px; font-style: italic; line-height: 1.25;">
    “Tu presencia es el mejor regalo en este día tan especial”
  </div>

  <div class="small-center p-muted" style="margin-top: 14px; font-size:22px; line-height: 1.25;">
    Pero si deseas obsequiarnos algo, puedes hacerlo de la siguiente forma:
  </div>

  <div style="margin-top:22px; display:flex; justify-content:center; align-items:center;">
    <img src="{gift_icon_uri}" style="width: 260px; max-width: 72%; height:auto; display:block;" />
  </div>

  <div class="small-center p-muted" style="margin-top: 22px; font-size:22px; line-height: 1.25;">
    Durante la recepción habrá una caja donde se podrá depositar
    <b style="color:{THEME_TEXT};">sobrecitos con efectivo</b>.
  </div>
</div>""").lstrip(),
    unsafe_allow_html=True,
)

# =========================================================
# RSVP FORM  ✅ (dynamic enable/disable)
# =========================================================
st.markdown(
    f"""
<div class="section">
  <div class="h-serif small-center" style="font-size:34px; font-weight:600;">{RSVP_TITLE} <span class="gold">🟢</span></div>
</div>
""",
    unsafe_allow_html=True,
)

left_sp, form_col, right_sp = st.columns([1, 2, 1], gap="large")
with form_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    nombre = st.text_input("Nombre", value="", key="rsvp_nombre")

    asistencia = st.selectbox(
        "¿Asistirás?",
        ["Selecciona una opción", "Sí", "No"],
        index=0,
        key="rsvp_asistencia",
    )

    personas = st.selectbox(
        "¿Cuántas personas asistirán?",
        ["Selecciona el número de personas"] + [str(i) for i in range(1, 11)],
        index=0,
        disabled=(asistencia != "Sí"),
        key="rsvp_personas",
    )

    comentarios = st.text_area(
        "Comentarios y Felicitaciones",
        value="",
        height=140,
        key="rsvp_comentarios",
    )

    confirmar = st.button("Confirmar", key="rsvp_confirmar")

    if confirmar:
        if not nombre.strip():
            st.warning("Por favor escribe tu nombre.")
        elif asistencia == "Selecciona una opción":
            st.warning("Por favor selecciona si asistirás.")
        elif asistencia == "Sí" and personas == "Selecciona el número de personas":
            st.warning("Por favor selecciona el número de personas.")
        else:
            n_personas = int(personas) if asistencia == "Sí" else 0

            msg = (
                f"Hola! Soy {nombre.strip()}. "
                f"\nConfirmación de asistencia a su boda: {asistencia} . "
                f"\nPersonas: {n_personas}."
            )
            if comentarios.strip():
                msg += f"\n\nComentarios: {comentarios.strip()}"

            link = wa_link(WHATSAPP_E164, msg)
            st.success("Listo ✅ Ahora para terminar abre WhatsApp y manda el mensaje de confirmación prellenado:")
            st.link_button("Abrir WhatsApp", link, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# GALLERY SLIDER (✅ carousel)  ✅ MOVED: right after RSVP
# =========================================================
if gal_uris:
    slides = "".join(
        f"""
        <div class="slide">
          <img src="{u}" />
        </div>
        """
        for u in gal_uris
    )

    gallery_html = f"""
    <style>
      html, body {{ margin:0; padding:0; }}

      .wrap {{
        width: 100%;
        max-width: 860px;
        margin: 0 auto;
        position: relative;
        overflow: visible;
      }}

      .viewport {{
        width: 100%;
        height: clamp(320px, 50vw, 560px);
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 16px 34px rgba(0,0,0,0.30);
        background: rgba(0,0,0,0.18);
        position: relative;
        z-index: 1;
      }}

      .track {{
        display: flex;
        width: 100%;
        height: 100%;
        transition: transform 420ms ease;
        will-change: transform;
      }}

      .slide {{
        flex: 0 0 100%;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
      }}

      .slide img {{
        width: 100%;
        height: 100%;
        object-fit: contain;
        object-position: center;
        display: block;
      }}

      .navbtn {{
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        width: 48px; height: 48px;
        border-radius: 999px;
        border: none;
        cursor: pointer;
        background: rgba(0,0,0,0.55);
        color: white;
        font-size: 26px;
        z-index: 99999;
      }}
      .prev {{ left: 18px; }}
      .next {{ right: 18px; }}

      .dots {{
        display:flex;
        justify-content:center;
        gap: 8px;
        margin-top: 12px;
      }}

      .dot {{
        width: 8px; height: 8px;
        border-radius: 999px;
        background: rgba(255,255,255,0.45);
        cursor:pointer;
      }}

      .dot.active {{
        background: rgba(255,255,255,0.95);
      }}
    </style>

    <div class="wrap">
      <div class="viewport">
        <div class="track" id="track">
          {slides}
        </div>

        <button class="navbtn prev" id="prevBtn">‹</button>
        <button class="navbtn next" id="nextBtn">›</button>
      </div>

      <div class="dots" id="dots"></div>
    </div>

    <script>
      const track = document.getElementById("track");
      const slideEls = Array.from(track.querySelectorAll(".slide"));
      const dotsDiv = document.getElementById("dots");
      const prevBtn = document.getElementById("prevBtn");
      const nextBtn = document.getElementById("nextBtn");

      let idx = 0;

      function renderDots() {{
        dotsDiv.innerHTML = "";
        slideEls.forEach((_, i) => {{
          const d = document.createElement("div");
          d.className = "dot" + (i === idx ? " active" : "");
          d.onclick = () => {{
            idx = i;
            render();
          }};
          dotsDiv.appendChild(d);
        }});
      }}

      function render() {{
        track.style.transform = `translateX(${{-idx * 100}}%)`;
        renderDots();
      }}

      function move(step) {{
        if (slideEls.length === 0) return;
        idx = (idx + step + slideEls.length) % slideEls.length;
        render();
      }}

      prevBtn.onclick = () => move(-1);
      nextBtn.onclick = () => move(1);

      document.addEventListener("keydown", (e) => {{
        if (e.key === "ArrowLeft") move(-1);
        if (e.key === "ArrowRight") move(1);
      }});

      render();
    </script>
    """

    st.markdown(
        f"""
<div class="section">
  <div class="h-serif small-center" style="margin-top: 10px; font-size:20px;">{THANKS_TEXT}</div>
</div>
""",
        unsafe_allow_html=True,
    )
    # ✅ FIX: height=560 (RESTORED) + append auto-resize script
    components.html(gallery_html + AUTO_RESIZE_SCRIPT, height=560)
else:
    st.markdown(
        """
<div class="section">
  <div class="h-serif small-center" style="font-size:40px; font-weight:600;">Galería</div>
  <div class="small-center p-muted" style="margin-top: 10px;">
    Agrega fotos en /assets con nombres como: gallery1.jpg / gallery2.png / gallery3.jpeg ...
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    f"""
<div class="section small-center" style="padding: 8px 16px;">
  <div class="p-muted">{FOOTER_LINE_1}</div>
  <div class="h-serif" style="font-size:22px; font-weight:600;">{FOOTER_LINE_2}</div>
  <div style="margin-top:10px; opacity:0.6; font-size:12px;">© {datetime.now().year}</div>
</div>
""",
    unsafe_allow_html=True,
)