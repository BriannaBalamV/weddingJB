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
    "Después de compartir una hermosa historia de amor, "
    "nos complace invitarte a celebrar el comienzo de una nueva etapa en nuestras vidas..."
)

PARENTS_NOVIO = ["Jesús Tejeda", "Evelin Sanchez"]
PARENTS_NOVIA = ["Vladimir Balam", "Enalyn Velasco"]
PADRINOS = ["si", "si"]

CEREMONIA = EventInfo(
    title="Ceremonia y Recepción",
    date_str="Domingo, 22 de Marzo de 2026",
    time_str="12:00 p.m.",
    place="Hotel Posada Señorial Cholula, Puebla",
    maps_url="https://maps.app.goo.gl/trKVWXCfvHpht5gG8",
)

# ✅ FIX: RECEPCION was referenced later but not defined
RECEPCION = CEREMONIA

DRESS_CODE = "Formal"
DRESS_NOTE = "Evitar color blanco (opcional)."

WHATSAPP_E164 = "52" + "2219683400"  # digits only, no '+' and no spaces
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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;800&family=Montserrat:wght@300;400;600&display=swap');

html, body, [class*="css"] {{
  font-family: 'Montserrat', system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
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
  font-family: 'Playfair Display', serif;
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
</style>
""",
    unsafe_allow_html=True,
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
        <div style="font-family:'Playfair Display',serif; font-size: clamp(44px, 6vw, 92px); font-weight:800; color:{THEME_TEXT}; letter-spacing:1px;">
          {COUPLE_1} <span style="color:{THEME_ACCENT}; font-weight:600;">&</span> {COUPLE_2}
        </div>

        <div style="margin-top:10px; font-size: 14px; letter-spacing:2px; color: rgba(245,240,232,0.9); font-weight:600;">
          {HERO_SUBTITLE}
        </div>

        <div style="margin-top:14px; font-family:'Playfair Display',serif; font-size: 18px; color: rgba(245,240,232,0.95);">
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
    components.html(hero_html, height=600)

# =========================================================
# INTRO
# =========================================================
st.markdown(
    f"""
<div class="section">
  <div class="small-center">
    <div class="h-serif" style="font-size:56px; font-weight:800;">{INTRO_TITLE}</div>
    <div class="p-muted" style="max-width: 900px; margin: 14px auto 0; font-size:16px;">
      {INTRO_TEXT}
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# =========================================================
# STORY + COUNTDOWN (center)
# =========================================================
countdown_html = f"""
<style>
  html, body {{ margin:0; padding:0; }}
</style>
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
  font-family: 'Playfair Display', serif;
">
  <div style="display:flex; justify-content:space-around; gap:10px; text-align:center;">
    <div><div id="d" style="font-size:26px; font-weight:800;">--</div><div style="opacity:.9;">Días</div></div>
    <div><div id="h" style="font-size:26px; font-weight:800;">--</div><div style="opacity:.9;">Hrs</div></div>
    <div><div id="m" style="font-size:26px; font-weight:800;">--</div><div style="opacity:.9;">Mins</div></div>
    <div><div id="s" style="font-size:26px; font-weight:800;">--</div><div style="opacity:.9;">Segs</div></div>
  </div>
</div>

<script>
  const target = new Date("{EVENT_DATE_TIME.replace(" ", "T")}").getTime();

  function tick() {{
    const now = new Date().getTime();
    let diff = Math.max(0, target - now);

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
    components.html(countdown_html, height=210)
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
<div class="h-serif small-center" style="font-size:42px; font-weight:700;">
¡Celebra con nosotros este día tan maravilloso!
</div>

<div class="hr-soft"></div>

<div style="display:flex; gap:20px; justify-content:space-between; flex-wrap:wrap; margin-top: 10px;">

<div style="flex:1; min-width: 220px; text-align:center;">
<div class="h-serif" style="font-size:22px; font-weight:700;">Padres de la Novia</div>
<div class="p-muted" style="margin-top:10px; font-size:16px;">
{PARENTS_NOVIA[1]}<br><span class="gold">&</span><br>{PARENTS_NOVIA[0]}
</div>
</div>

<div style="flex:1; min-width: 220px; text-align:center;">
<div class="h-serif" style="font-size:22px; font-weight:700;">Padres del Novio</div>
<div class="p-muted" style="margin-top:10px; font-size:16px;">
{PARENTS_NOVIO[0]}<br><span class="gold">&</span><br>{PARENTS_NOVIO[1]}
</div>
</div>

<div style="flex:1; min-width: 220px; text-align:center;">
<div class="h-serif" style="font-size:22px; font-weight:700;">Padrinos</div>
<div class="p-muted" style="margin-top:10px; font-size:16px;">
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
  <div style="font-family:'Playfair Display',serif; font-size:28px; font-weight:800; margin-top:6px;">
    {RECEPCION.title}
  </div>
  <div style="margin-top:12px; font-size:16px;">
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
# DRESS CODE
# =========================================================
st.markdown(
    f"""
<div class="section">
  <div class="h-serif small-center" style="font-size:40px; font-weight:800;">Código de Vestimenta</div>
  <div class="small-center p-muted" style="margin-top: 10px; font-size:18px;">
    <b style="color:{THEME_TEXT};">{DRESS_CODE}</b><br>
    {DRESS_NOTE}
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# =========================================================
# GALLERY SLIDER (✅ carousel)
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
        height: clamp(320px, 50vw, 560px);   /* ✅ FIXED: clamp (not lamp) */
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
        z-index: 99999;   /* ✅ always on top */
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

        <!-- ✅ MOVED INSIDE viewport so they overlay the image -->
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
  <div class="h-serif small-center" style="font-size:40px; font-weight:800;">Galería</div>
  <div class="small-center p-muted" style="margin-top: 10px;">{THANKS_TEXT}</div>
</div>
""",
        unsafe_allow_html=True,
    )
    components.html(gallery_html, height=560)
else:
    st.markdown(
        """
<div class="section">
  <div class="h-serif small-center" style="font-size:40px; font-weight:800;">Galería</div>
  <div class="small-center p-muted" style="margin-top: 10px;">
    Agrega fotos en /assets con nombres como: gallery1.jpg / gallery2.png / gallery3.jpeg ...
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

# =========================================================
# RSVP FORM
# =========================================================
st.markdown(
    f"""
<div class="section">
  <div class="h-serif small-center" style="font-size:40px; font-weight:800;">{RSVP_TITLE} <span class="gold">🟢</span></div>
</div>
""",
    unsafe_allow_html=True,
)

left_sp, form_col, right_sp = st.columns([1, 2, 1], gap="large")
with form_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    with st.form("rsvp_form", clear_on_submit=False):
        nombre = st.text_input("Nombre", value="")
        invitados = st.number_input("Invitados", min_value=0, max_value=20, value=0, step=1)
        submitted = st.form_submit_button("Confirmar Asistencia")

    if submitted:
        msg = (
            f"Hola! Soy {nombre.strip() or '___'}. "
            f"Confirmo mi asistencia a la boda de {COUPLE_1} & {COUPLE_2}. "
            f"Invitados: {int(invitados)}."
        )
        link = wa_link(WHATSAPP_E164, msg)
        st.success("Listo ✅ Ahora confirma por WhatsApp:")
        st.link_button("Abrir WhatsApp", link, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    f"""
<div class="section small-center" style="padding: 26px 16px;">
  <div class="p-muted">{FOOTER_LINE_1}</div>
  <div class="h-serif" style="font-size:22px; font-weight:700;">{FOOTER_LINE_2}</div>
  <div style="margin-top:10px; opacity:0.6; font-size:12px;">© {datetime.now().year}</div>
</div>
""",
    unsafe_allow_html=True,
)
