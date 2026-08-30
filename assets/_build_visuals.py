#!/usr/bin/env python3
"""Baut alex-banner.svg und alex-engineer-id.svg aus den Portraet-PNGs.

WARUM EIN GENERATOR STATT HANDGEPFLEGTER SVGs
---------------------------------------------
GitHub bindet README-Bilder als <img src="..."> ein. Ein so eingebettetes SVG
laeuft im "secure static mode": der Browser laedt daraus grundsaetzlich keine
externen Ressourcen nach - auch keine relativen. Ein <image href="alex-profile.png">
im SVG bliebe auf github.com also schlicht leer.

Damit bleibt nur die Einbettung als data:-URI. Weil ein Base64-Block von Hand
nicht wartbar ist, liegt der Vektorteil hier als Template und das Bild wird beim
Build hineingerechnet. Bild tauschen heisst: PNG ersetzen, Skript laufen lassen.

    python3 assets/_build_visuals.py

Die Ausgabe-SVGs sind danach eigenstaendig - keine externen Referenzen, kein
JavaScript, nur SVG, CSS-Animation und SMIL.

Die eingebettete Kopie ist bewusst klein: das Portraet erscheint auf der Karte
mit rund 216 CSS-Pixeln, eingebettet werden 420x420 als JPEG (~24 KB). Das
vollaufloesende Asset bleibt daneben als assets/alex-profile.webp erhalten -
verlustfrei, 900x900 - und dient als Quelle fuer diesen Build.
"""
from __future__ import annotations

import base64
import shutil
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

HERE = Path(__file__).parent

# Quelle, Zuschnitt und Zielaufloesung je Bild.
# Zielaufloesung ~2x der Darstellungsgroesse auf GitHub, damit es auf
# Retina-Displays scharf bleibt, ohne die Datei aufzublaehen.
class Source(NamedTuple):
    """Ein Quellbild samt Zuschnitt und Zielaufloesung."""
    src: str
    crop: str
    size: str
    quality: str
    extra: list[str] = []


SOURCES: dict[str, Source] = {
    "portrait": Source(
        # Quelle ist bereits quadratisch zugeschnitten (Kopf + Oberkoerper),
        # deshalb hier nur noch skalieren.
        src="alex-profile.webp",
        crop="660x660+70+0",       # Gesicht in den Kreismittelpunkt ruecken
        size="420x420",
        quality="85",
        extra=["-modulate", "100,104,100"],   # Saettigung leicht an die Palette angeglichen
    ),
    "figure": Source(
        src="alex-hero-figure.png",
        crop="966x1428+60+20",     # ganze Person, links etwas beschnitten
        size="620x916",
        quality="76",
    ),
}


def encode(name: str, spec: Source, tmp: Path) -> str:
    """Schneidet, skaliert und kodiert ein Quellbild als data:-URI."""
    src = HERE / spec.src
    if not src.exists():
        sys.exit(f"Quellbild fehlt: {src}")
    out = tmp / f"{name}.jpg"
    _ = subprocess.run(
        ["magick", str(src), "-crop", spec.crop, "+repage",
         "-resize", spec.size, *spec.extra, "-quality", spec.quality, str(out)],
        check=True,
    )
    b64 = base64.b64encode(out.read_bytes()).decode("ascii")
    print(f"  {name:<9} {spec.size:>9}  jpeg {out.stat().st_size / 1024:6.1f} KB"
          f"  ->  base64 {len(b64) / 1024:6.1f} KB")
    return f"data:image/jpeg;base64,{b64}"


# ─────────────────────────────────────────────────────────────────────────────
# BANNER
# ─────────────────────────────────────────────────────────────────────────────
BANNER = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720" role="img" aria-label="Alexander Schneider — System Integration. Linux, Networking, DevOps, Security. Infrastructure Engineer im Rechenzentrum.">
<title>Alexander Schneider — System Integration</title>
<desc>Dunkles Infrastruktur-Panel: links Terminal-Prompt, Name und wechselnde Rollen, in der Mitte ein Infrastruktur-Stack von Edge bis Mesh, rechts Alexander Schneider als Infrastructure Engineer vor Serverracks.</desc>

<defs>
  <style><![CDATA[
    .mono{font-family:ui-monospace,"SFMono-Regular","JetBrains Mono","IBM Plex Mono",Menlo,Consolas,"Liberation Mono",monospace}
    .sans{font-family:Inter,"Inter var",system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}

    @keyframes rise{from{opacity:0;transform:translate(0,10px)}to{opacity:1;transform:translate(0,0)}}
    @keyframes riseS{from{opacity:0;transform:translate(0,6px)}to{opacity:1;transform:translate(0,0)}}
    @keyframes slideL{from{opacity:0;transform:translate(-14px,0)}to{opacity:1;transform:translate(0,0)}}
    @keyframes fade{from{opacity:0}to{opacity:1}}
    @keyframes caret{0%,45%{opacity:1}46%,100%{opacity:0}}
    @keyframes pulseLed{0%,100%{opacity:.35}50%{opacity:1}}
    @keyframes scan{0%{transform:translate(0,-140px)}100%{transform:translate(0,840px)}}
    @keyframes roleIn{
      0%{opacity:0;transform:translate(0,9px)}
      2.2%{opacity:1;transform:translate(0,0)}
      13.8%{opacity:1;transform:translate(0,0)}
      16.6%{opacity:0;transform:translate(0,-9px)}
      100%{opacity:0;transform:translate(0,-9px)}
    }
    @keyframes stackLed{0%,100%{opacity:.3}50%{opacity:.95}}
    @keyframes haloBreathe{0%,100%{opacity:.30}50%{opacity:.52}}
    @keyframes figIn{from{clip-path:inset(100% 0 0 0)}to{clip-path:inset(0 0 0 0)}}

    .anim{opacity:0}
    .t-name1 {animation:rise .7s cubic-bezier(.2,.7,.2,1) 1.50s forwards}
    .t-name2 {animation:rise .7s cubic-bezier(.2,.7,.2,1) 1.62s forwards}
    .t-rule  {animation:fade .5s ease 1.90s forwards}
    .t-sub   {animation:riseS .6s cubic-bezier(.2,.7,.2,1) 2.00s forwards}
    .t-tech  {animation:riseS .6s cubic-bezier(.2,.7,.2,1) 2.14s forwards}
    .t-role  {animation:fade .5s ease 2.10s forwards}
    .t-claim {animation:riseS .6s cubic-bezier(.2,.7,.2,1) 2.60s forwards}
    .t-st1   {animation:slideL .5s ease 2.84s forwards}
    .t-st2   {animation:slideL .5s ease 2.96s forwards}
    .t-st3   {animation:slideL .5s ease 3.08s forwards}
    .t-meta  {animation:fade .7s ease 3.34s forwards}
    .t-div   {animation:fade .8s ease 1.20s forwards}
    .t-stack {animation:fade .7s ease .70s forwards}
    .t-hud   {animation:fade .8s ease 1.90s forwards}
    .t-cap   {animation:fade .7s ease 2.40s forwards}

    .caret{opacity:0;animation:caret 1.05s step-end 1.45s infinite}
    .led{animation:pulseLed 3.4s ease-in-out infinite}
    .scanline{animation:scan 12s linear 2s infinite}
    .halo{animation:haloBreathe 7s ease-in-out 2s infinite}
    .figReveal{animation:figIn 1.7s cubic-bezier(.25,.7,.2,1) .75s backwards}

    .role{opacity:0;animation:roleIn 18s ease-in-out infinite}
    .r1{animation-delay:2.2s}.r2{animation-delay:5.2s}.r3{animation-delay:8.2s}
    .r4{animation-delay:11.2s}.r5{animation-delay:14.2s}.r6{animation-delay:17.2s}

    .sl1{animation:stackLed 2.7s ease-in-out infinite}
    .sl2{animation:stackLed 3.3s ease-in-out .4s infinite}
    .sl3{animation:stackLed 2.4s ease-in-out .8s infinite}
    .sl4{animation:stackLed 3.6s ease-in-out .2s infinite}
    .sl5{animation:stackLed 3.0s ease-in-out 1.1s infinite}

    @media (prefers-reduced-motion:reduce){
      .anim{opacity:1!important;animation:none!important;transform:none!important}
      .role{opacity:0!important;animation:none!important;transform:none!important}
      .r1{opacity:1!important}
      .caret{opacity:1!important;animation:none!important}
      .led,.scanline,.halo,.sl1,.sl2,.sl3,.sl4,.sl5{animation:none!important}
      .figReveal{animation:none!important;clip-path:none!important}
    }
  ]]></style>

  <linearGradient id="bg" x1="0" y1="0" x2=".62" y2="1">
    <stop offset="0%" stop-color="#0B1015"/>
    <stop offset="52%" stop-color="#080C11"/>
    <stop offset="100%" stop-color="#070A0D"/>
  </linearGradient>
  <radialGradient id="glowL" cx="16%" cy="28%" r="58%">
    <stop offset="0%" stop-color="#2388FF" stop-opacity=".13"/>
    <stop offset="100%" stop-color="#2388FF" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="figHalo" cx="50%" cy="42%" r="58%">
    <stop offset="0%" stop-color="#0E4E7A" stop-opacity=".55"/>
    <stop offset="55%" stop-color="#0B2E4A" stop-opacity=".26"/>
    <stop offset="100%" stop-color="#00C2FF" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="vign" cx="46%" cy="46%" r="78%">
    <stop offset="55%" stop-color="#000" stop-opacity="0"/>
    <stop offset="100%" stop-color="#000" stop-opacity=".5"/>
  </radialGradient>

  <linearGradient id="nameG" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#FFFFFF"/>
    <stop offset="52%" stop-color="#E6EDF3"/>
    <stop offset="100%" stop-color="#A7C6E8"/>
  </linearGradient>
  <linearGradient id="ruleG" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#2388FF"/>
    <stop offset="55%" stop-color="#00C2FF" stop-opacity=".5"/>
    <stop offset="100%" stop-color="#00C2FF" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="panelG" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#151D26" stop-opacity=".92"/>
    <stop offset="100%" stop-color="#111820" stop-opacity=".72"/>
  </linearGradient>
  <linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#00C2FF" stop-opacity="0"/>
    <stop offset="50%" stop-color="#00C2FF" stop-opacity=".05"/>
    <stop offset="100%" stop-color="#00C2FF" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="divG" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#2388FF" stop-opacity="0"/>
    <stop offset="18%" stop-color="#233343" stop-opacity=".9"/>
    <stop offset="82%" stop-color="#233343" stop-opacity=".9"/>
    <stop offset="100%" stop-color="#2388FF" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="spineG" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#2388FF" stop-opacity=".75"/>
    <stop offset="100%" stop-color="#2388FF" stop-opacity=".12"/>
  </linearGradient>

  <!-- Figur: weiche Kanten, damit sie im Panel sitzt statt darauf zu kleben -->
  <linearGradient id="fadeVg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#000"/>
    <stop offset="7%" stop-color="#BBB"/>
    <stop offset="16%" stop-color="#FFF"/>
    <stop offset="76%" stop-color="#FFF"/>
    <stop offset="94%" stop-color="#3A3A3A"/>
    <stop offset="100%" stop-color="#000"/>
  </linearGradient>
  <linearGradient id="fadeHg" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#000"/>
    <stop offset="9%" stop-color="#DDD"/>
    <stop offset="22%" stop-color="#FFF"/>
    <stop offset="82%" stop-color="#FFF"/>
    <stop offset="96%" stop-color="#B0B0B0"/>
    <stop offset="100%" stop-color="#4A4A4A"/>
  </linearGradient>
  <mask id="fadeV"><rect x="856" y="96" width="400" height="596" fill="url(#fadeVg)"/></mask>
  <mask id="fadeH"><rect x="856" y="96" width="400" height="596" fill="url(#fadeHg)"/></mask>

  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
    <path d="M32 0H0V32" fill="none" stroke="#16212C" stroke-width="1" stroke-opacity=".5"/>
  </pattern>
  <pattern id="gridFine" width="8" height="8" patternUnits="userSpaceOnUse">
    <path d="M8 0H0V8" fill="none" stroke="#111A23" stroke-width=".5" stroke-opacity=".55"/>
  </pattern>

  <filter id="glowXS" x="-140%" y="-140%" width="380%" height="380%">
    <feGaussianBlur stdDeviation="1.5" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
    <feDropShadow dx="0" dy="2" stdDeviation="6" flood-color="#000" flood-opacity=".5"/>
  </filter>

  <clipPath id="typeClip">
    <rect x="64" y="70" width="0" height="24">
      <animate attributeName="width" calcMode="discrete" dur="1.45s" fill="freeze"
        values="0;10;20;30;40;50;60;70;80;90;100;110;120;130;140;150;160;170;180;190;200;220;280"/>
    </rect>
  </clipPath>
  <clipPath id="frameClip"><rect x="0" y="0" width="1280" height="720" rx="14"/></clipPath>
</defs>

<g clip-path="url(#frameClip)">
  <rect width="1280" height="720" fill="url(#bg)"/>
  <rect width="1280" height="720" fill="url(#gridFine)"/>
  <rect width="1280" height="720" fill="url(#grid)"/>
  <rect width="1280" height="720" fill="url(#glowL)"/>
  <rect class="scanline" x="0" y="0" width="1280" height="140" fill="url(#scanG)"/>

  <!-- Blueprint-Ticks -->
  <g stroke="#1C2A38" stroke-width="1" opacity=".75">
    <path d="M64 26 v7 M320 26 v7 M576 26 v7 M832 26 v7 M1088 26 v7"/>
    <path d="M32 34 H1248" stroke-opacity=".55"/>
  </g>
  <g class="mono" font-size="9" fill="#41525F" letter-spacing="1.4">
    <text x="64" y="22">00</text><text x="320" y="22">20</text><text x="576" y="22">40</text>
    <text x="832" y="22">60</text><text x="1088" y="22">80</text>
  </g>
  <text class="mono" x="1216" y="22" text-anchor="end" font-size="9" fill="#41525F" letter-spacing="1.4">NODE.MAP / v2</text>

  <rect class="anim t-div" x="547" y="58" width="1" height="612" fill="url(#divG)"/>
  <rect class="anim t-div" x="843" y="58" width="1" height="612" fill="url(#divG)"/>

  <!-- ══════════ ZONE 1 · IDENTITAET ══════════ -->
  <g clip-path="url(#typeClip)">
    <text class="mono" x="64" y="88" font-size="15" letter-spacing=".4">
      <tspan fill="#22C55E">alex@infra</tspan><tspan fill="#3D4C5A">:</tspan><tspan fill="#2388FF">~</tspan><tspan fill="#3D4C5A">$</tspan><tspan fill="#AAB4BE" dx="6">./whoami</tspan><tspan class="caret" fill="#00C2FF" dx="2">&#9608;</tspan>
    </text>
  </g>

  <text class="sans anim t-name1" x="64" y="170" font-size="52" font-weight="700" fill="url(#nameG)" letter-spacing="1">ALEXANDER</text>
  <text class="sans anim t-name2" x="64" y="222" font-size="52" font-weight="700" fill="url(#nameG)" letter-spacing="1">SCHNEIDER</text>

  <rect class="anim t-rule" x="64" y="244" width="300" height="2" rx="1" fill="url(#ruleG)"/>

  <text class="mono anim t-sub" x="64" y="280" font-size="14" fill="#7D8996" letter-spacing="5.4">SYSTEM INTEGRATION</text>
  <text class="mono anim t-tech" x="64" y="308" font-size="11.5" letter-spacing="2.2">
    <tspan fill="#2388FF">LINUX</tspan><tspan fill="#3D4C5A"> • </tspan><tspan fill="#2388FF">NETWORKING</tspan><tspan fill="#3D4C5A"> • </tspan><tspan fill="#2388FF">DEVOPS</tspan><tspan fill="#3D4C5A"> • </tspan><tspan fill="#2388FF">SECURITY</tspan>
  </text>

  <g class="anim t-role">
    <rect x="64" y="340" width="440" height="52" rx="7" fill="url(#panelG)" stroke="#1E2A36" stroke-width="1"/>
    <rect x="64" y="340" width="3" height="52" rx="1.5" fill="#2388FF"/>
    <text class="mono" x="84" y="360" font-size="9.5" fill="#4E5E6C" letter-spacing="2.4">ACTIVE ROLE</text>
    <g class="mono" font-size="16" fill="#00C2FF" letter-spacing=".5">
      <text class="role r1" x="84" y="380">Infrastructure Engineer</text>
      <text class="role r2" x="84" y="380">Linux Administrator</text>
      <text class="role r3" x="84" y="380">DevOps Engineer</text>
      <text class="role r4" x="84" y="380">Security Enthusiast</text>
      <text class="role r5" x="84" y="380">Automation Builder</text>
      <text class="role r6" x="84" y="380">Self-Hosting Nerd</text>
    </g>
    <circle class="led" cx="486" cy="366" r="3" fill="#00C2FF" filter="url(#glowXS)"/>
  </g>

  <text class="sans anim t-claim" x="64" y="444" font-size="18" font-weight="600" letter-spacing="4.2">
    <tspan fill="#E6EDF3">BUILD</tspan><tspan fill="#2388FF">.</tspan><tspan fill="#E6EDF3" dx="8">HARDEN</tspan><tspan fill="#2388FF">.</tspan><tspan fill="#E6EDF3" dx="8">AUTOMATE</tspan><tspan fill="#2388FF">.</tspan>
  </text>

  <g class="mono" font-size="11.5" letter-spacing="1.7">
    <g class="anim t-st1">
      <circle class="led" cx="70" cy="500" r="3.4" fill="#22C55E" filter="url(#glowXS)"/>
      <text x="88" y="504" fill="#AAB4BE">SYSTEM ONLINE</text>
      <text x="504" y="504" fill="#4E5E6C" text-anchor="end">NOMINAL</text>
      <path d="M88 512 H504" stroke="#18232E" stroke-width="1"/>
    </g>
    <g class="anim t-st2">
      <circle class="led" cx="70" cy="532" r="3.4" fill="#2388FF" filter="url(#glowXS)" style="animation-delay:.7s"/>
      <text x="88" y="536" fill="#AAB4BE">AUTOMATION ENABLED</text>
      <text x="504" y="536" fill="#4E5E6C" text-anchor="end">RUNNING</text>
      <path d="M88 544 H504" stroke="#18232E" stroke-width="1"/>
    </g>
    <g class="anim t-st3">
      <circle class="led" cx="70" cy="564" r="3.4" fill="#F59E0B" filter="url(#glowXS)" style="animation-delay:1.4s"/>
      <text x="88" y="568" fill="#AAB4BE">COFFEE DEPENDENCY</text>
      <text x="504" y="568" fill="#F59E0B" text-anchor="end">CRITICAL</text>
    </g>
  </g>

  <text class="mono anim t-meta" x="64" y="648" font-size="10.5" fill="#3D4C5A" letter-spacing="1.9">LEIPZIG, DE &#160;·&#160; alex-schneider.dev &#160;·&#160; github.com/arn0ld87</text>

  <!-- ══════════ ZONE 2 · INFRASTRUKTUR-STACK ══════════ -->
  <g class="anim t-stack">
    <text class="mono" x="580" y="70" font-size="9.5" fill="#41525F" letter-spacing="2.4">STACK / EDGE → MESH</text>
    <path d="M580 80 H812" stroke="#18232E" stroke-width="1"/>

    <!-- Spine -->
    <rect x="596" y="118" width="1.5" height="424" fill="url(#spineG)"/>

    <!-- Datenpakete auf der Spine -->
    <g filter="url(#glowXS)">
      <circle cx="596.75" r="2.6" fill="#00C2FF">
        <animate attributeName="cy" values="118;542" dur="7s" begin="1.6s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0;.95;.95;0" dur="7s" begin="1.6s" repeatCount="indefinite"/>
      </circle>
      <circle cx="596.75" r="2.2" fill="#2388FF">
        <animate attributeName="cy" values="118;542" dur="9.5s" begin="4.4s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0;.8;.8;0" dur="9.5s" begin="4.4s" repeatCount="indefinite"/>
      </circle>
    </g>

    <!-- Stufen -->
    <g class="mono">
      <g>
        <circle class="sl1" cx="596.75" cy="126" r="4.5" fill="#0F1B26" stroke="#2388FF" stroke-width="1.4"/>
        <path d="M604 126 H620" stroke="#233343" stroke-width="1"/>
        <text x="628" y="121" font-size="8.5" fill="#4E5E6C" letter-spacing="2.2">EDGE</text>
        <text x="628" y="135" font-size="11" fill="#E6EDF3" letter-spacing=".6">Cloudflare</text>
      </g>
      <g>
        <circle class="sl2" cx="596.75" cy="230" r="4.5" fill="#0F1B26" stroke="#2388FF" stroke-width="1.4"/>
        <path d="M604 230 H620" stroke="#233343" stroke-width="1"/>
        <text x="628" y="225" font-size="8.5" fill="#4E5E6C" letter-spacing="2.2">FILTER</text>
        <text x="628" y="239" font-size="11" fill="#E6EDF3" letter-spacing=".6">Firewall</text>
        <text x="812" y="239" font-size="8" fill="#2E3D4C" letter-spacing="1.2" text-anchor="end">deny all</text>
      </g>
      <g>
        <circle class="sl3" cx="596.75" cy="334" r="4.5" fill="#0F1B26" stroke="#22C55E" stroke-width="1.4"/>
        <path d="M604 334 H620" stroke="#233343" stroke-width="1"/>
        <text x="628" y="329" font-size="8.5" fill="#4E5E6C" letter-spacing="2.2">COMPUTE</text>
        <text x="628" y="343" font-size="11" fill="#E6EDF3" letter-spacing=".6">Host</text>
        <text x="812" y="343" font-size="8" fill="#2E3D4C" letter-spacing="1.2" text-anchor="end">+ VPS</text>
      </g>
      <g>
        <circle class="sl4" cx="596.75" cy="438" r="4.5" fill="#0F1B26" stroke="#2388FF" stroke-width="1.4"/>
        <path d="M604 438 H620" stroke="#233343" stroke-width="1"/>
        <text x="628" y="433" font-size="8.5" fill="#4E5E6C" letter-spacing="2.2">RUNTIME</text>
        <text x="628" y="447" font-size="11" fill="#E6EDF3" letter-spacing=".6">Docker · LXC · VM</text>
      </g>
      <g>
        <circle class="sl5" cx="596.75" cy="542" r="4.5" fill="#0F1B26" stroke="#22C55E" stroke-width="1.4"/>
        <path d="M604 542 H620" stroke="#233343" stroke-width="1"/>
        <text x="628" y="537" font-size="8.5" fill="#4E5E6C" letter-spacing="2.2">MESH</text>
        <text x="628" y="551" font-size="11" fill="#E6EDF3" letter-spacing=".6">Tailscale</text>
      </g>
    </g>

    <!-- Kleine Rack-Andeutung am Fuss des Stacks -->
    <g transform="translate(580,588)">
      <rect x="0" y="0" width="232" height="60" rx="5" fill="#0D131A" stroke="#1E2A36"/>
      <g>
        <rect x="8" y="8" width="216" height="12" rx="2" fill="#131C25" stroke="#1F2C39" stroke-width=".8"/>
        <circle class="sl1" cx="18" cy="14" r="2" fill="#22C55E"/>
        <rect x="30" y="11" width="72" height="5" rx="1.5" fill="#22303E"/>
        <rect x="8" y="24" width="216" height="12" rx="2" fill="#131C25" stroke="#1F2C39" stroke-width=".8"/>
        <circle class="sl3" cx="18" cy="30" r="2" fill="#2388FF"/>
        <rect x="30" y="27" width="104" height="5" rx="1.5" fill="#22303E"/>
        <rect x="8" y="40" width="216" height="12" rx="2" fill="#131C25" stroke="#1F2C39" stroke-width=".8"/>
        <circle class="sl5" cx="18" cy="46" r="2" fill="#F59E0B"/>
        <rect x="30" y="43" width="56" height="5" rx="1.5" fill="#22303E"/>
      </g>
    </g>
  </g>

  <!-- ══════════ ZONE 3 · OPERATOR ══════════ -->
  <!-- Glow hinter der Person, damit sie aus der Flaeche kommt statt darauf zu liegen -->
  <ellipse class="halo" cx="1056" cy="360" rx="215" ry="290" fill="url(#figHalo)"/>

  <g class="figReveal">
    <g mask="url(#fadeV)">
      <g mask="url(#fadeH)">
        <image x="856" y="96" width="400" height="596"
               preserveAspectRatio="xMidYMid slice"
               href="__FIGURE__"/>
      </g>
    </g>
  </g>

  <!-- Scanline, die den Reveal begleitet und danach verschwindet -->
  <g opacity="0">
    <rect x="856" y="96" width="400" height="2" fill="#00C2FF" filter="url(#glowXS)">
      <animate attributeName="y" values="692;96" dur="1.7s" begin=".75s" fill="freeze"
               calcMode="spline" keyTimes="0;1" keySplines=".25 .7 .2 1"/>
    </rect>
    <animate attributeName="opacity" values="0;.85;.85;0" keyTimes="0;.06;.9;1" dur="1.9s" begin=".7s" fill="freeze"/>
  </g>

  <!-- HUD um die Figur -->
  <g class="anim t-hud" fill="none" stroke="#2388FF" stroke-width="1.4" stroke-opacity=".55">
    <path d="M872 128 V108 H900"/>
    <path d="M1240 108 H1212"/>
    <path d="M872 656 V676 H900"/>
    <path d="M1240 676 H1212"/>
  </g>
  <g class="anim t-hud">
    <text class="mono" x="872" y="100" font-size="9" fill="#41525F" letter-spacing="2.4">OPERATOR</text>
    <circle class="led" cx="1236" cy="96" r="3" fill="#22C55E" filter="url(#glowXS)"/>
    <text class="mono" x="1224" y="100" font-size="9" fill="#41525F" letter-spacing="2.2" text-anchor="end">ON SITE</text>
  </g>

  <g class="anim t-cap">
    <text class="mono" x="1240" y="626" font-size="13" fill="#E6EDF3" letter-spacing=".8" text-anchor="end">Infrastructure Engineer</text>
    <text class="mono" x="1240" y="646" font-size="9.5" fill="#4E5E6C" letter-spacing="2.2" text-anchor="end">LINUX / DEVOPS / NETWORK</text>
  </g>

  <rect width="1280" height="720" fill="url(#vign)" pointer-events="none"/>
  <rect x=".75" y=".75" width="1278.5" height="718.5" rx="14" fill="none" stroke="#1B2733" stroke-width="1.5"/>
</g>
</svg>
'''

# ─────────────────────────────────────────────────────────────────────────────
# ENGINEER ID
# ─────────────────────────────────────────────────────────────────────────────
ID_CARD = '''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 420 640" width="420" height="640" role="img" aria-label="Engineer ID: Alexander Schneider — Infrastructure Access, Clearance Linux, Network, Automation, Status Online">
<title>Engineer ID — Alexander Schneider</title>
<desc>Ausweiskarte an einem anthrazitfarbenen Lanyard mit Stahlclip. Portraet von Alexander Schneider in runder Fassung mit hexagonalem Rahmen, darunter Name, Rolle, Zugangsstufe und Status online.</desc>

<defs>
  <style><![CDATA[
    .mono{font-family:ui-monospace,"SFMono-Regular","JetBrains Mono","IBM Plex Mono",Menlo,Consolas,"Liberation Mono",monospace}
    .sans{font-family:Inter,"Inter var",system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}

    @keyframes shine{0%{transform:translate(-260px,0)}55%,100%{transform:translate(300px,0)}}
    @keyframes ledOn{0%,100%{opacity:.4}50%{opacity:1}}
    @keyframes edgeRun{0%{stroke-dashoffset:1272}100%{stroke-dashoffset:0}}
    @keyframes fadeIn{from{opacity:0}to{opacity:1}}
    @keyframes ringSpin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
    @keyframes hudScan{0%{transform:translate(0,0)}100%{transform:translate(0,112px)}}
    @keyframes qrFlick{0%,88%,100%{opacity:.55}92%{opacity:.9}}

    .sheen{animation:shine 7s cubic-bezier(.4,0,.2,1) 3.4s infinite}
    .statusLed{animation:ledOn 2.8s ease-in-out 3s infinite}
    .edge{stroke-dasharray:300 972;animation:edgeRun 7s linear 2.8s infinite}
    .late{opacity:0;animation:fadeIn .6s ease 2.2s forwards}
    .qr{animation:qrFlick 5.5s linear 3.5s infinite}
    .ring{transform-box:fill-box;transform-origin:center;animation:ringSpin 34s linear infinite}
    .pscan{animation:hudScan 4.6s cubic-bezier(.4,0,.5,1) 2.6s infinite}

    @media (prefers-reduced-motion:reduce){
      .sheen,.statusLed,.edge,.qr,.ring,.pscan{animation:none!important}
      .late{opacity:1;animation:none!important}
      .edge{stroke-dasharray:none}
    }
  ]]></style>

  <linearGradient id="steel" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#8E9AA6"/><stop offset="28%" stop-color="#D3DBE3"/>
    <stop offset="52%" stop-color="#6E7A87"/><stop offset="76%" stop-color="#B6C0CA"/>
    <stop offset="100%" stop-color="#5C6874"/>
  </linearGradient>
  <linearGradient id="strap" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#141A21"/><stop offset="35%" stop-color="#232C36"/>
    <stop offset="65%" stop-color="#1B222A"/><stop offset="100%" stop-color="#10151B"/>
  </linearGradient>
  <linearGradient id="carbon" x1="0" y1="0" x2=".7" y2="1">
    <stop offset="0%" stop-color="#1A222B"/><stop offset="45%" stop-color="#141B23"/>
    <stop offset="100%" stop-color="#0D131A"/>
  </linearGradient>
  <linearGradient id="headBand" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#0E1A28"/><stop offset="55%" stop-color="#12233A"/>
    <stop offset="100%" stop-color="#0C1622"/>
  </linearGradient>
  <linearGradient id="edgeG" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#00C2FF"/><stop offset="50%" stop-color="#2388FF"/>
    <stop offset="100%" stop-color="#00C2FF"/>
  </linearGradient>
  <linearGradient id="sheenG" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
    <stop offset="45%" stop-color="#BFE4FF" stop-opacity=".085"/>
    <stop offset="55%" stop-color="#FFFFFF" stop-opacity=".045"/>
    <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="pscanG" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#00C2FF" stop-opacity="0"/>
    <stop offset="50%" stop-color="#00C2FF" stop-opacity=".5"/>
    <stop offset="100%" stop-color="#00C2FF" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="portraitVig" cx="50%" cy="42%" r="62%">
    <stop offset="62%" stop-color="#000" stop-opacity="0"/>
    <stop offset="100%" stop-color="#040709" stop-opacity=".72"/>
  </radialGradient>

  <pattern id="weave" width="6" height="6" patternUnits="userSpaceOnUse">
    <path d="M0 3 H6" stroke="#0A0E13" stroke-width="1" stroke-opacity=".55"/>
    <path d="M3 0 V6" stroke="#2A343F" stroke-width=".6" stroke-opacity=".3"/>
  </pattern>
  <pattern id="carbonTex" width="5" height="5" patternUnits="userSpaceOnUse">
    <path d="M0 0 L5 5 M5 0 L0 5" stroke="#212B36" stroke-width=".45" stroke-opacity=".38"/>
  </pattern>

  <filter id="cardShadow" x="-40%" y="-20%" width="180%" height="160%">
    <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#000" flood-opacity=".62"/>
  </filter>
  <filter id="blueGlow" x="-40%" y="-25%" width="180%" height="160%">
    <feGaussianBlur stdDeviation="7" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="ledGlow" x="-300%" y="-300%" width="700%" height="700%">
    <feGaussianBlur stdDeviation="2" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>

  <path id="strapMid" d="M209 74 C200 119 178 155 157 190" fill="none"/>
  <clipPath id="cardClip"><rect x="100" y="200" width="220" height="410" rx="14"/></clipPath>
  <clipPath id="portraitClip"><circle cx="210" cy="322" r="54"/></clipPath>
  <clipPath id="pscanClip"><circle cx="210" cy="322" r="54"/></clipPath>
</defs>

<g id="rig">
  <animateTransform attributeName="transform" type="translate" additive="replace"
      from="0 -720" to="0 0" dur=".8s" begin="0s" fill="freeze"
      calcMode="spline" keyTimes="0;1" keySplines=".16 .84 .3 1"/>

  <g>
    <animateTransform attributeName="transform" type="rotate" additive="replace"
      dur="4.4s" begin=".52s" fill="freeze" calcMode="spline"
      values="0 210 40; -8.6 210 40; 6.5 210 40; -4.6 210 40; 3.2 210 40; -2.1 210 40; 1.3 210 40; -0.7 210 40; 0.3 210 40; 0 210 40"
      keyTimes="0;.11;.23;.35;.47;.59;.70;.81;.91;1"
      keySplines=".42 0 .58 1;.42 0 .58 1;.42 0 .58 1;.42 0 .58 1;.42 0 .58 1;.42 0 .58 1;.42 0 .58 1;.42 0 .58 1;.42 0 .58 1"/>
    <animateTransform attributeName="transform" type="rotate" additive="sum"
      dur="11s" begin="4.9s" repeatCount="indefinite" calcMode="spline"
      values="0 210 40; 1.4 210 40; 0 210 40; -1.4 210 40; 0 210 40"
      keyTimes="0;.25;.5;.75;1"
      keySplines=".42 0 .58 1;.42 0 .58 1;.42 0 .58 1;.42 0 .58 1"/>

    <!-- Stahlclip -->
    <g>
      <rect x="196" y="22" width="28" height="10" rx="4" fill="url(#steel)" opacity=".9"/>
      <rect x="199" y="30" width="22" height="34" rx="8" fill="url(#steel)"/>
      <rect x="203.5" y="36" width="13" height="20" rx="6" fill="#0B1015"/>
      <path d="M199 46 h22" stroke="#0B1015" stroke-opacity=".35" stroke-width="1"/>
      <rect x="192" y="62" width="36" height="12" rx="3" fill="url(#steel)"/>
      <rect x="195" y="65" width="30" height="2" rx="1" fill="#F2F6FA" opacity=".35"/>
      <rect x="192" y="70" width="36" height="4" rx="1.5" fill="#0F141A" opacity=".55"/>
    </g>

    <!-- Lanyard -->
    <g>
      <path d="M202 73 C193 118 169 154 147 187 L170 197 C192 162 212 124 217 75 Z" fill="url(#strap)"/>
      <path d="M202 73 C193 118 169 154 147 187 L170 197 C192 162 212 124 217 75 Z" fill="url(#weave)" opacity=".5"/>
      <path d="M218 73 C227 118 251 154 273 187 L250 197 C228 162 208 124 203 75 Z" fill="url(#strap)"/>
      <path d="M218 73 C227 118 251 154 273 187 L250 197 C228 162 208 124 203 75 Z" fill="url(#weave)" opacity=".5"/>
      <path d="M203 75 C194 119 170 155 149 187" fill="none" stroke="#3B4753" stroke-width=".8" stroke-opacity=".5"/>
      <path d="M217 75 C226 119 250 155 271 187" fill="none" stroke="#3B4753" stroke-width=".8" stroke-opacity=".5"/>
      <text class="mono late" font-size="6.4" fill="#525F6D" letter-spacing="1.4">
        <textPath href="#strapMid" xlink:href="#strapMid" startOffset="9%">ALEX // SYSTEMS</textPath>
      </text>
      <rect x="142" y="184" width="34" height="12" rx="5" fill="url(#steel)" opacity=".85"/>
      <rect x="244" y="184" width="34" height="12" rx="5" fill="url(#steel)" opacity=".85"/>
      <circle cx="159" cy="190" r="2.6" fill="#0B1015"/>
      <circle cx="261" cy="190" r="2.6" fill="#0B1015"/>
    </g>

    <!-- Karte -->
    <g filter="url(#cardShadow)">
      <rect x="100" y="200" width="220" height="410" rx="14" fill="url(#carbon)"/>
    </g>

    <g clip-path="url(#cardClip)">
      <rect x="100" y="200" width="220" height="410" fill="url(#carbonTex)"/>

      <!-- Kopfband -->
      <rect x="100" y="200" width="220" height="50" fill="url(#headBand)"/>
      <path d="M100 250 H320" stroke="#2388FF" stroke-width="1" stroke-opacity=".45"/>
      <g transform="translate(116,216)">
        <rect width="18" height="18" rx="4" fill="none" stroke="#2388FF" stroke-width="1.3"/>
        <path d="M4.5 9 h9 M9 4.5 v9" stroke="#00C2FF" stroke-width="1.3" stroke-linecap="round"/>
      </g>
      <text class="mono" x="142" y="223" font-size="8" fill="#5B6C7C" letter-spacing="1.9">CREDENTIAL</text>
      <text class="mono" x="142" y="236" font-size="9.5" fill="#00C2FF" letter-spacing="1.75">INFRASTRUCTURE ACCESS</text>
      <text class="mono" x="306" y="223" font-size="7" fill="#3D4C5A" letter-spacing="1.2" text-anchor="end">REV 03</text>

      <!-- ── Portraet ── -->
      <circle cx="210" cy="322" r="60" fill="#0C141C" stroke="#1C2A38"/>
      <g clip-path="url(#portraitClip)">
        <image x="156" y="268" width="108" height="108" preserveAspectRatio="xMidYMid slice"
               href="__PORTRAIT__"/>
        <circle cx="210" cy="322" r="54" fill="url(#portraitVig)"/>
      </g>
      <!-- HUD-Scan ueber dem Portraet -->
      <g clip-path="url(#pscanClip)">
        <rect class="pscan" x="156" y="256" width="108" height="9" fill="url(#pscanG)"/>
      </g>
      <!-- Fassung: Kreis, laufender Ring, dezenter Hexagon-Rahmen -->
      <circle cx="210" cy="322" r="54" fill="none" stroke="#00C2FF" stroke-width="1.3" stroke-opacity=".6"/>
      <circle class="ring" cx="210" cy="322" r="59" fill="none" stroke="#2388FF" stroke-width=".9"
              stroke-opacity=".5" stroke-dasharray="24 11 3 11"/>
      <path d="M210 256 L267 289 L267 355 L210 388 L153 355 L153 289 Z"
            fill="none" stroke="#233A50" stroke-width="1.1"/>
      <g fill="#2388FF" opacity=".85">
        <circle cx="153" cy="322" r="2"/><circle cx="267" cy="322" r="2"/>
        <circle cx="210" cy="256" r="2"/><circle cx="210" cy="388" r="2"/>
      </g>

      <!-- Name -->
      <text class="mono" x="210" y="404" font-size="7.5" fill="#4E5E6C" letter-spacing="1.9" text-anchor="middle">HOLDER</text>
      <text class="sans" x="210" y="424" font-size="17" font-weight="700" fill="#E6EDF3" letter-spacing=".6" text-anchor="middle">ALEXANDER</text>
      <text class="sans" x="210" y="443" font-size="17" font-weight="700" fill="#E6EDF3" letter-spacing=".6" text-anchor="middle">SCHNEIDER</text>
      <text class="mono" x="210" y="460" font-size="8.5" fill="#7D8996" letter-spacing="2.1" text-anchor="middle">SYSTEM INTEGRATION</text>

      <path d="M118 476 H302" stroke="#1E2A36" stroke-width="1"/>

      <!-- Clearance -->
      <text class="mono" x="118" y="493" font-size="7.5" fill="#4E5E6C" letter-spacing="1.9">CLEARANCE</text>
      <g class="mono" font-size="8.5" letter-spacing="1.1">
        <rect x="118" y="500" width="52" height="17" rx="3.5" fill="#101C28" stroke="#28455F"/>
        <text x="144" y="512" fill="#AAB4BE" text-anchor="middle">LINUX</text>
        <rect x="176" y="500" width="62" height="17" rx="3.5" fill="#101C28" stroke="#28455F"/>
        <text x="207" y="512" fill="#AAB4BE" text-anchor="middle">NETWORK</text>
        <rect x="244" y="500" width="58" height="17" rx="3.5" fill="#101C28" stroke="#28455F"/>
        <text x="273" y="512" fill="#AAB4BE" text-anchor="middle">AUTOMAT.</text>
      </g>

      <!-- Status -->
      <text class="mono" x="118" y="537" font-size="7.5" fill="#4E5E6C" letter-spacing="1.9">STATUS</text>
      <circle class="statusLed" cx="122" cy="551" r="3.4" fill="#22C55E" filter="url(#ledGlow)"/>
      <text class="mono" x="134" y="555" font-size="11" fill="#22C55E" letter-spacing="2.4">ONLINE</text>

      <!-- Ident + dekoratives Modulmuster -->
      <g class="mono" font-size="7.5" letter-spacing=".55">
        <text x="196" y="537" fill="#4E5E6C" letter-spacing="1.9">IDENT</text>
        <text x="196" y="549" fill="#8B98A5">alex-schneider.dev</text>
        <text x="196" y="560" fill="#8B98A5">github.com/arn0ld87</text>
        <text x="196" y="571" fill="#6C7B8A">LEIPZIG / DE</text>
      </g>
      <g class="qr" opacity=".55">
        <rect x="118" y="565" width="12" height="12" rx="1" fill="none" stroke="#7D8996" stroke-width="2"/>
        <rect x="121.5" y="568.5" width="5" height="5" fill="#7D8996"/>
        <rect x="152" y="565" width="12" height="12" rx="1" fill="none" stroke="#7D8996" stroke-width="2"/>
        <rect x="155.5" y="568.5" width="5" height="5" fill="#7D8996"/>
        <g fill="#00C2FF" opacity=".8">
          <rect x="136" y="565" width="4" height="4"/><rect x="142" y="571" width="4" height="4"/>
          <rect x="136" y="577" width="4" height="4"/><rect x="168" y="567" width="4" height="4"/>
          <rect x="174" y="573" width="4" height="4"/><rect x="168" y="579" width="4" height="4"/>
        </g>
      </g>

      <!-- Fusszeile -->
      <rect x="100" y="594" width="220" height="16" fill="#0B1219"/>
      <text class="mono" x="118" y="605" font-size="7" fill="#3D4C5A" letter-spacing="1.6">BUILD &#183; HARDEN &#183; AUTOMATE</text>
      <text class="mono" x="302" y="605" font-size="7" fill="#3D4C5A" letter-spacing="1.6" text-anchor="end">FI-S</text>

      <g class="sheen">
        <rect x="60" y="196" width="90" height="418" fill="url(#sheenG)" transform="skewX(-14)"/>
      </g>
    </g>

    <rect x="100" y="200" width="220" height="410" rx="14" fill="none" stroke="#243441" stroke-width="1.5"/>
    <rect class="edge" x="100" y="200" width="220" height="410" rx="14" fill="none"
          stroke="url(#edgeG)" stroke-width="1.5" stroke-opacity=".9" filter="url(#blueGlow)"/>
  </g>
</g>
</svg>
'''


# ─────────────────────────────────────────────────────────────────────────────
# BANNER (Light) - gleiche Komposition, schlichter. Die Figur sitzt in einem
# dunklen Panel, weil das Foto selbst dunkel ist und auf hellem Grund sonst
# wie ein ausgeschnittener Fleck wirken wuerde.
# ─────────────────────────────────────────────────────────────────────────────
BANNER_LIGHT = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720" role="img" aria-label="Alexander Schneider — System Integration. Linux, Networking, DevOps, Security.">
<title>Alexander Schneider — System Integration</title>
<desc>Helles Infrastruktur-Panel: links Terminal-Prompt, Name und wechselnde Rollen, in der Mitte ein Infrastruktur-Stack von Edge bis Mesh, rechts Alexander Schneider als Infrastructure Engineer.</desc>

<defs>
  <style><![CDATA[
    .mono{font-family:ui-monospace,"SFMono-Regular","JetBrains Mono","IBM Plex Mono",Menlo,Consolas,"Liberation Mono",monospace}
    .sans{font-family:Inter,"Inter var",system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
    @keyframes riseS{from{opacity:0;transform:translate(0,6px)}to{opacity:1;transform:translate(0,0)}}
    @keyframes fade{from{opacity:0}to{opacity:1}}
    @keyframes roleIn{
      0%{opacity:0;transform:translate(0,8px)}
      2.2%{opacity:1;transform:translate(0,0)}
      13.8%{opacity:1;transform:translate(0,0)}
      16.6%{opacity:0;transform:translate(0,-8px)}
      100%{opacity:0;transform:translate(0,-8px)}
    }
    .anim{opacity:0}
    .a1{animation:riseS .6s ease .25s forwards}
    .a2{animation:fade .6s ease .45s forwards}
    .a3{animation:riseS .6s ease .60s forwards}
    .a4{animation:riseS .6s ease .75s forwards}
    .a5{animation:fade .6s ease .90s forwards}
    .a6{animation:riseS .6s ease 1.05s forwards}
    .a7{animation:fade .6s ease 1.20s forwards}
    .a8{animation:fade .7s ease .35s forwards}
    .a9{animation:fade .9s ease .55s forwards}
    .role{opacity:0;animation:roleIn 18s ease-in-out infinite}
    .r1{animation-delay:1.1s}.r2{animation-delay:4.1s}.r3{animation-delay:7.1s}
    .r4{animation-delay:10.1s}.r5{animation-delay:13.1s}.r6{animation-delay:16.1s}
    @media (prefers-reduced-motion:reduce){
      .anim{opacity:1!important;animation:none!important;transform:none!important}
      .role{opacity:0!important;animation:none!important;transform:none!important}
      .r1{opacity:1!important}
    }
  ]]></style>

  <linearGradient id="bgL" x1="0" y1="0" x2=".6" y2="1">
    <stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#EEF2F6"/>
  </linearGradient>
  <linearGradient id="ruleL" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#0B63C8"/><stop offset="100%" stop-color="#0B63C8" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="divL" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#C9D4DF" stop-opacity="0"/><stop offset="20%" stop-color="#C9D4DF"/>
    <stop offset="80%" stop-color="#C9D4DF"/><stop offset="100%" stop-color="#C9D4DF" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="spineL" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#0B63C8" stop-opacity=".7"/><stop offset="100%" stop-color="#0B63C8" stop-opacity=".12"/>
  </linearGradient>
  <linearGradient id="panelL" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#101A24"/><stop offset="100%" stop-color="#0A0F15"/>
  </linearGradient>
  <linearGradient id="fadeVgL" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#000"/><stop offset="8%" stop-color="#CCC"/>
    <stop offset="18%" stop-color="#FFF"/><stop offset="80%" stop-color="#FFF"/>
    <stop offset="96%" stop-color="#333"/><stop offset="100%" stop-color="#000"/>
  </linearGradient>
  <mask id="fadeVL"><rect x="872" y="112" width="368" height="520" fill="url(#fadeVgL)"/></mask>
  <pattern id="gridL" width="32" height="32" patternUnits="userSpaceOnUse">
    <path d="M32 0H0V32" fill="none" stroke="#DCE4EC" stroke-width="1"/>
  </pattern>
  <clipPath id="fcL"><rect x="0" y="0" width="1280" height="720" rx="14"/></clipPath>
  <clipPath id="figPanelL"><rect x="864" y="104" width="384" height="536" rx="12"/></clipPath>
</defs>

<g clip-path="url(#fcL)">
  <rect width="1280" height="720" fill="url(#bgL)"/>
  <rect width="1280" height="720" fill="url(#gridL)"/>

  <g stroke="#CBD5E1" stroke-width="1"><path d="M64 26 v7 M320 26 v7 M576 26 v7 M832 26 v7 M1088 26 v7 M32 34 H1248"/></g>
  <g class="mono" font-size="9" fill="#94A3B0" letter-spacing="1.4">
    <text x="64" y="22">00</text><text x="320" y="22">20</text><text x="576" y="22">40</text>
    <text x="832" y="22">60</text><text x="1088" y="22">80</text>
  </g>
  <text class="mono" x="1216" y="22" text-anchor="end" font-size="9" fill="#94A3B0" letter-spacing="1.4">NODE.MAP / v2</text>

  <rect x="547" y="58" width="1" height="612" fill="url(#divL)"/>

  <!-- Identitaet -->
  <text class="mono anim a1" x="64" y="88" font-size="15" letter-spacing=".4">
    <tspan fill="#15803D">alex@infra</tspan><tspan fill="#94A3B0">:</tspan><tspan fill="#0B63C8">~</tspan><tspan fill="#94A3B0">$</tspan><tspan fill="#334155" dx="6">./whoami</tspan>
  </text>
  <text class="sans anim a1" x="64" y="170" font-size="52" font-weight="700" fill="#0F1B26" letter-spacing="1">ALEXANDER</text>
  <text class="sans anim a1" x="64" y="222" font-size="52" font-weight="700" fill="#0F1B26" letter-spacing="1">SCHNEIDER</text>
  <rect class="anim a2" x="64" y="244" width="300" height="2" rx="1" fill="url(#ruleL)"/>
  <text class="mono anim a3" x="64" y="280" font-size="14" fill="#5A6B7B" letter-spacing="5.4">SYSTEM INTEGRATION</text>
  <text class="mono anim a4" x="64" y="308" font-size="11.5" letter-spacing="2.2">
    <tspan fill="#0B63C8">LINUX</tspan><tspan fill="#A3B1BF"> • </tspan><tspan fill="#0B63C8">NETWORKING</tspan><tspan fill="#A3B1BF"> • </tspan><tspan fill="#0B63C8">DEVOPS</tspan><tspan fill="#A3B1BF"> • </tspan><tspan fill="#0B63C8">SECURITY</tspan>
  </text>

  <g class="anim a5">
    <rect x="64" y="340" width="440" height="52" rx="7" fill="#FFFFFF" stroke="#D7E0E9"/>
    <rect x="64" y="340" width="3" height="52" rx="1.5" fill="#0B63C8"/>
    <text class="mono" x="84" y="360" font-size="9.5" fill="#8B98A5" letter-spacing="2.4">ACTIVE ROLE</text>
    <g class="mono" font-size="16" fill="#0B63C8" letter-spacing=".5">
      <text class="role r1" x="84" y="380">Infrastructure Engineer</text>
      <text class="role r2" x="84" y="380">Linux Administrator</text>
      <text class="role r3" x="84" y="380">DevOps Engineer</text>
      <text class="role r4" x="84" y="380">Security Enthusiast</text>
      <text class="role r5" x="84" y="380">Automation Builder</text>
      <text class="role r6" x="84" y="380">Self-Hosting Nerd</text>
    </g>
  </g>

  <text class="sans anim a6" x="64" y="444" font-size="18" font-weight="600" letter-spacing="4.2">
    <tspan fill="#0F1B26">BUILD</tspan><tspan fill="#0B63C8">.</tspan><tspan fill="#0F1B26" dx="8">HARDEN</tspan><tspan fill="#0B63C8">.</tspan><tspan fill="#0F1B26" dx="8">AUTOMATE</tspan><tspan fill="#0B63C8">.</tspan>
  </text>

  <g class="mono anim a7" font-size="11.5" letter-spacing="1.7">
    <circle cx="70" cy="500" r="3.4" fill="#15803D"/>
    <text x="88" y="504" fill="#334155">SYSTEM ONLINE</text>
    <text x="504" y="504" fill="#8B98A5" text-anchor="end">NOMINAL</text>
    <path d="M88 512 H504" stroke="#DCE4EC"/>
    <circle cx="70" cy="532" r="3.4" fill="#0B63C8"/>
    <text x="88" y="536" fill="#334155">AUTOMATION ENABLED</text>
    <text x="504" y="536" fill="#8B98A5" text-anchor="end">RUNNING</text>
    <path d="M88 544 H504" stroke="#DCE4EC"/>
    <circle cx="70" cy="564" r="3.4" fill="#B45309"/>
    <text x="88" y="568" fill="#334155">COFFEE DEPENDENCY</text>
    <text x="504" y="568" fill="#B45309" text-anchor="end">CRITICAL</text>
  </g>
  <text class="mono anim a7" x="64" y="648" font-size="10.5" fill="#94A3B0" letter-spacing="1.9">LEIPZIG, DE &#160;·&#160; alex-schneider.dev &#160;·&#160; github.com/arn0ld87</text>

  <!-- Stack -->
  <g class="anim a8">
    <text class="mono" x="580" y="70" font-size="9.5" fill="#94A3B0" letter-spacing="2.4">STACK / EDGE → MESH</text>
    <path d="M580 80 H812" stroke="#DCE4EC"/>
    <rect x="596" y="118" width="1.5" height="424" fill="url(#spineL)"/>
    <g class="mono">
      <g><circle cx="596.75" cy="126" r="4.5" fill="#FFF" stroke="#0B63C8" stroke-width="1.4"/>
         <path d="M604 126 H620" stroke="#CBD5E1"/>
         <text x="628" y="121" font-size="8.5" fill="#94A3B0" letter-spacing="2.2">EDGE</text>
         <text x="628" y="135" font-size="11" fill="#0F1B26" letter-spacing=".6">Cloudflare</text></g>
      <g><circle cx="596.75" cy="230" r="4.5" fill="#FFF" stroke="#0B63C8" stroke-width="1.4"/>
         <path d="M604 230 H620" stroke="#CBD5E1"/>
         <text x="628" y="225" font-size="8.5" fill="#94A3B0" letter-spacing="2.2">FILTER</text>
         <text x="628" y="239" font-size="11" fill="#0F1B26" letter-spacing=".6">Firewall</text></g>
      <g><circle cx="596.75" cy="334" r="4.5" fill="#FFF" stroke="#15803D" stroke-width="1.4"/>
         <path d="M604 334 H620" stroke="#CBD5E1"/>
         <text x="628" y="329" font-size="8.5" fill="#94A3B0" letter-spacing="2.2">COMPUTE</text>
         <text x="628" y="343" font-size="11" fill="#0F1B26" letter-spacing=".6">Host</text>
         <text x="812" y="343" font-size="8" fill="#A3B1BF" letter-spacing="1.2" text-anchor="end">+ VPS</text></g>
      <g><circle cx="596.75" cy="438" r="4.5" fill="#FFF" stroke="#0B63C8" stroke-width="1.4"/>
         <path d="M604 438 H620" stroke="#CBD5E1"/>
         <text x="628" y="433" font-size="8.5" fill="#94A3B0" letter-spacing="2.2">RUNTIME</text>
         <text x="628" y="447" font-size="11" fill="#0F1B26" letter-spacing=".6">Docker · LXC · VM</text></g>
      <g><circle cx="596.75" cy="542" r="4.5" fill="#FFF" stroke="#15803D" stroke-width="1.4"/>
         <path d="M604 542 H620" stroke="#CBD5E1"/>
         <text x="628" y="537" font-size="8.5" fill="#94A3B0" letter-spacing="2.2">MESH</text>
         <text x="628" y="551" font-size="11" fill="#0F1B26" letter-spacing=".6">Tailscale</text></g>
    </g>
    <g transform="translate(580,588)">
      <rect x="0" y="0" width="232" height="60" rx="5" fill="#F4F7FA" stroke="#D7E0E9"/>
      <g fill="#FFFFFF" stroke="#E2E9F0" stroke-width=".8">
        <rect x="8" y="8" width="216" height="12" rx="2"/><rect x="8" y="24" width="216" height="12" rx="2"/>
        <rect x="8" y="40" width="216" height="12" rx="2"/>
      </g>
      <circle cx="18" cy="14" r="2" fill="#15803D"/><circle cx="18" cy="30" r="2" fill="#0B63C8"/><circle cx="18" cy="46" r="2" fill="#B45309"/>
      <g fill="#DCE4EC"><rect x="30" y="11" width="72" height="5" rx="1.5"/><rect x="30" y="27" width="104" height="5" rx="1.5"/><rect x="30" y="43" width="56" height="5" rx="1.5"/></g>
    </g>
  </g>

  <!-- Operator im dunklen Panel -->
  <g class="anim a9">
    <rect x="864" y="104" width="384" height="536" rx="12" fill="url(#panelL)"/>
    <g clip-path="url(#figPanelL)">
      <g mask="url(#fadeVL)">
        <image x="872" y="112" width="368" height="520" preserveAspectRatio="xMidYMid slice"
               href="__FIGURE__"/>
      </g>
    </g>
    <rect x="864" y="104" width="384" height="536" rx="12" fill="none" stroke="#0B63C8" stroke-opacity=".35" stroke-width="1.5"/>
    <text class="mono" x="884" y="132" font-size="9" fill="#5B6C7C" letter-spacing="2.4">OPERATOR</text>
    <text class="mono" x="1228" y="604" font-size="13" fill="#E6EDF3" letter-spacing=".8" text-anchor="end">Infrastructure Engineer</text>
    <text class="mono" x="1228" y="622" font-size="9.5" fill="#7D8996" letter-spacing="2.2" text-anchor="end">LINUX / DEVOPS / NETWORK</text>
  </g>

  <rect x=".75" y=".75" width="1278.5" height="718.5" rx="14" fill="none" stroke="#D7E0E9" stroke-width="1.5"/>
</g>
</svg>
'''


def main() -> int:
    if not shutil.which("magick"):
        sys.exit("ImageMagick (magick) wird zum Zuschneiden benoetigt.")
    tmp = HERE / "_tmp_build"
    tmp.mkdir(exist_ok=True)
    try:
        print("Bilder aufbereiten:")
        uris = {k: encode(k, v, tmp) for k, v in SOURCES.items()}

        out = {
            "alex-banner.svg": BANNER.replace("__FIGURE__", uris["figure"]),
            "alex-engineer-id.svg": ID_CARD.replace("__PORTRAIT__", uris["portrait"]),
            "alex-banner-light.svg": BANNER_LIGHT.replace("__FIGURE__", uris["figure"]),
        }
        print("\nSVGs schreiben:")
        for name, content in out.items():
            p = HERE / name
            _ = p.write_text(content, encoding="utf-8")
            print(f"  {name:<24} {p.stat().st_size/1024:7.1f} KB")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
