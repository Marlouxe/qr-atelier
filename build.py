#!/usr/bin/env python3
"""Génère le site (racine du dépôt) + les flyers (dossier flyers/).
Usage : python build.py https://TON-PSEUDO.github.io/qr-atelier
Dépendances : pip install qrcode pillow
"""
import sys, os, html
import qrcode
from PIL import Image, ImageDraw, ImageFont

BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://marlouxe.github.io/qr-atelier").rstrip("/")
OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(f"{OUT}/flyers", exist_ok=True)

# ---------------------------------------------------------------- Scénarios
S = [
 dict(slug="menu", safe=True, titre="Menu du restaurant",
  suite="Vous seriez simplement arrivé sur la carte du restaurant.",
  indices=["Le QR est imprimé dans le même bloc que le menu, sans sticker ni décalage.",
           "Le contexte est logique : un menu se consulte, on ne vous demande rien.",
           "Aucune urgence, aucune demande de paiement ni de mot de passe."]),
 dict(slug="parking", safe=False, titre="Paiement de parking",
  suite="Vous auriez atterri sur un faux site de paiement, prêt à recueillir votre numéro de carte.",
  indices=["Le QR est un sticker collé par-dessus un autre : bords visibles, léger décalage, l'ancien code dépasse.",
           "Les faux QR sur horodateurs sont une arnaque classique : ils redirigent vers un faux site de paiement.",
           "Le contexte annonce un paiement : on ne paie pas via un QR collé sur une borne.",
           "Bon réflexe : utiliser l'application officielle de la ville ou l'horodateur lui-même."]),
 dict(slug="colis", safe=False, titre="Colis en attente",
  suite="Vous auriez été invité à saisir votre adresse, puis votre carte bancaire pour « régler 1,99 € ».",
  indices=["Message de pression : « sous 24 h », « retourné à l'expéditeur ».",
           "Vous n'attendiez pas de colis, et le transporteur n'est même pas nommé.",
           "Frais minuscules (1,99 €) : le but est de récupérer vos données bancaires.",
           "Bon réflexe : suivre son colis depuis le site ou l'appli du transporteur, adresse tapée à la main."]),
 dict(slug="wifi", safe=True, titre="Wi-Fi de la médiathèque",
  suite="Vous vous seriez simplement connecté au réseau de la médiathèque.",
  indices=["Affiche officielle, à l'accueil, cohérente avec le lieu où l'on se trouve.",
           "Le QR sert à se connecter au réseau, sans formulaire ni identifiants à saisir.",
           "En cas de doute, on peut demander à l'accueil de confirmer."]),
 dict(slug="concours", safe=False, titre="Concours « gagnez un iPhone »",
  suite="Vous auriez été invité à laisser nom, e-mail, téléphone, puis peut-être des frais de « livraison ».",
  indices=["Trop beau pour être vrai : un smartphone dernier cri pour un simple scan.",
           "Compte à rebours et « plus que 3 lots » : fausse urgence.",
           "Aucun organisateur identifiable, pas de règlement, pas de mentions légales.",
           "Bon réflexe : ne jamais donner ses données personnelles pour un gain surprise."]),
 dict(slug="salon", safe=True, titre="Programme du salon",
  suite="Vous auriez consulté le programme du salon.",
  indices=["Organisateur clairement identifié, adresse du site officiel imprimée en toutes lettres.",
           "Le QR est un complément : l'information existe aussi sans le scanner.",
           "Rien n'est demandé en échange."]),
]

# ---------------------------------------------------------------- Site
CSS = """\
:root{
  --bg:#f6f6f3;--surface:#fff;--fg:#1b1c1e;--muted:#64676e;--line:#e2e1dc;
  --accent:#2f4fb3;--accent-fg:#fff;--ok:#2b7a4b;--ko:#b03a30;--warn:#a86a00;
  color-scheme:light dark;
}
@media(prefers-color-scheme:dark){:root{
  --bg:#131416;--surface:#1a1b1e;--fg:#e9e9e6;--muted:#9a9da5;--line:#2a2b2f;
  --accent:#8ba3ee;--accent-fg:#101218;--ok:#6cc08f;--ko:#e58a80;--warn:#e0b060;
}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);
  font:16.5px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",sans-serif}
main{max-width:660px;margin:0 auto;padding:28px 18px 56px}
h1{font-size:1.65rem;line-height:1.25;font-weight:650;letter-spacing:-.01em;margin:0 0 .35em}
h2{font-size:1.05rem;font-weight:650;margin:0 0 .6em}
p{margin:.6em 0}
a{color:var(--accent)}
.lead{color:var(--muted);margin:0 0 1.4em}
.card{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:18px 20px;margin:14px 0}
.card>:first-child{margin-top:0}.card>:last-child{margin-bottom:0}
.note{border-left:3px solid var(--warn)}
ol,ul{padding-left:1.25em;margin:.5em 0}
li{margin:.4em 0}
li::marker{color:var(--muted)}
.muted{color:var(--muted);font-size:.92rem}
.verdict{border:1px solid var(--line);border-left-width:4px;border-radius:8px;background:var(--surface);padding:18px 20px;margin:0 0 14px}
.verdict.ok{border-left-color:var(--ok)}.verdict.ko{border-left-color:var(--ko)}
.verdict .tag{font-size:.78rem;font-weight:650;letter-spacing:.08em;text-transform:uppercase;margin:0 0 .3em}
.verdict.ok .tag{color:var(--ok)}.verdict.ko .tag{color:var(--ko)}
.verdict h1{margin:0 0 .3em}
.verdict p{margin:.3em 0;color:var(--muted)}
.btn{display:inline-block;background:var(--accent);color:var(--accent-fg);text-decoration:none;
  padding:10px 18px;border-radius:6px;font-weight:600;font-size:.95rem}
.btn:hover{opacity:.9}
.split{display:grid;gap:12px}
@media(min-width:620px){.split{grid-template-columns:1fr 1fr}}
.split .card{margin:0}
.split h2.bad{color:var(--ko)}.split h2.good{color:var(--ok)}
"""

CAROUSEL_CSS = """\
.carousel{display:flex;align-items:center;justify-content:center;gap:8px}
.carousel img{flex:0 1 auto;width:100%;max-width:440px;height:auto;border:1px solid var(--line);
  border-radius:4px;cursor:zoom-in;display:block;background:#fff}
.nav{flex:none;width:40px;height:40px;border-radius:50%;border:1px solid var(--line);
  background:var(--surface);color:var(--fg);font-size:22px;line-height:1;cursor:pointer;padding:0}
.nav:hover{border-color:var(--muted)}
.nav:active{transform:scale(.94)}
.counter{text-align:center;margin:.8em 0 0;font-weight:600;font-size:.95rem}
.thumbs{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;margin-top:10px}
.thumbs img{width:44px;height:auto;border:2px solid transparent;border-radius:3px;cursor:pointer;opacity:.55}
.thumbs img.active{border-color:var(--accent);opacity:1}
.lightbox{position:fixed;inset:0;background:rgba(0,0,0,.9);display:flex;align-items:center;
  justify-content:center;gap:6px;padding:12px;z-index:10}
.lightbox[hidden]{display:none}
.lightbox img{max-width:calc(100% - 100px);max-height:100%;object-fit:contain;border-radius:4px;cursor:zoom-out;background:#fff}
.lightbox .nav{background:#222;color:#fff;border-color:#444}
.lightbox .close{position:absolute;top:10px;right:10px;width:38px;height:38px;border-radius:50%;
  border:0;background:#fff;color:#000;font-size:18px;cursor:pointer}
"""

HEAD = """<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta name="robots" content="noindex"><title>{t}</title>
<link rel="stylesheet" href="style.css"><link rel="stylesheet" href="carousel.css"></head><body><main>"""

def page(s):
    ok = s["safe"]
    tag = "Verdict : sûr" if ok else "Verdict : piégé"
    titre = "Ce QR code était sûr" if ok else "Ce QR code était piégé"
    sub = ("Aucun piège ici. Voyons pourquoi on pouvait lui faire confiance." if ok else
           "Simulation pédagogique : rien n'a été collecté ni volé. Dans la réalité : "
           + s["suite"][0].lower() + s["suite"][1:])
    titre_ind = "Ce qui rassurait" if ok else "Ce qui aurait dû vous alerter"
    lis = "".join(f"<li>{html.escape(i)}</li>" for i in s["indices"])
    return (HEAD.format(t=html.escape(s["titre"])) +
      f'<div class="verdict {"ok" if ok else "ko"}"><p class="tag">{tag}</p><h1>{titre}</h1><p>{html.escape(sub)}</p></div>'
      f'<div class="card"><h2>Flyer : {html.escape(s["titre"])}</h2>'
      f'<p>Reprenez le flyer et comparez avec votre premier avis. Aviez-vous vu ces éléments ?</p></div>'
      f'<div class="card"><h2>{titre_ind}</h2><ul>{lis}</ul></div>'
      '<p><a class="btn" href="index.html">Retour aux flyers</a></p></main></body></html>')

INDEX = HEAD.format(t="Atelier QR codes") + """
<h1>Atelier QR codes</h1>
<p class="lead">Saurez-vous repérer les QR codes piégés ?</p>

<div class="card note"><h2>Avant de commencer</h2>
<p>Cette activité utilise votre téléphone. Rien de dangereux : toutes les pages sont fabriquées pour l'atelier et aucune donnée n'est collectée.</p></div>

<div class="card"><h2>La consigne</h2>
<ol>
<li>Lisez les flyers ci-dessous, un par un, comme si vous les croisiez dans la rue ou dans un commerce.</li>
<li>Pour chacun, faites-vous votre propre avis : est-ce que vous scanneriez ce QR code, oui ou non ?</li>
<li>Scannez ensuite les QR codes avec l'appareil photo de votre téléphone (depuis un autre écran ou une impression, pas depuis l'écran de ce même téléphone).</li>
<li>Lisez l'adresse qui s'affiche, ouvrez le lien : la page vous dira si vous aviez raison ou non de le scanner.</li>
</ol></div>

<div class="card"><h2>Les flyers</h2>
<p class="muted">Touchez un flyer pour l'agrandir, utilisez les flèches pour passer de l'un à l'autre.</p>
<div class="carousel" id="carousel">
<button class="nav prev" aria-label="Flyer précédent">‹</button>
<img id="c-img" src="flyers/flyer1_menu.png" alt="Flyer 1">
<button class="nav next" aria-label="Flyer suivant">›</button>
</div>
<p class="counter" id="c-count">Flyer 1 / 6</p>
<div class="thumbs" id="c-thumbs"></div>
</div>
<div class="lightbox" id="lightbox" hidden>
<button class="nav prev" aria-label="Précédent">‹</button>
<img id="l-img" src="" alt="">
<button class="nav next" aria-label="Suivant">›</button>
<button class="close" aria-label="Fermer">✕</button>
</div>

<h2 style="margin-top:1.8em">Scanner ou pas : quelques repères</h2>
<div class="split">
<div class="card"><h2 class="bad">Mieux vaut s'abstenir</h2>
<p>Un QR code n'est qu'un lien déguisé : les mêmes réflexes s'appliquent que pour un lien reçu par SMS. Mieux vaut ne pas scanner dès qu'on vous met la pression (« sous 24 h », « plus que 3 lots », « dernières places »), dès qu'on vous demande de payer (stationnement, frais de livraison, amende), de saisir un mot de passe, un code reçu par SMS ou un numéro de carte, ou lorsque le gain paraît trop beau. Même prudence avec un colis que vous n'attendiez pas, ou un QR collé dans l'espace public, surtout si des bords dépassent ou si un autre code apparaît dessous.</p></div>
<div class="card"><h2 class="good">Plutôt raisonnable</h2>
<p>Scanner est en revanche sans grand risque quand le QR n'est qu'un confort : consulter un menu ou un programme, rejoindre le Wi-Fi du lieu où vous vous trouvez, avec un organisateur clairement identifié et rien à donner en échange. Dans tous les cas, lisez l'adresse affichée avant d'ouvrir le lien, et pour tout ce qui touche à l'argent ou à un compte, passez plutôt par l'application ou le site officiel, adresse tapée à la main.</p></div>
</div>
</main><script src="carousel.js"></script></body></html>"""

open(f"{OUT}/style.css", "w").write(CSS)
open(f"{OUT}/carousel.css", "w").write(CAROUSEL_CSS)
open(f"{OUT}/index.html", "w").write(INDEX)
for s in S:
    open(f"{OUT}/{s['slug']}.html", "w").write(page(s))
if os.path.exists(f"{OUT}/corrige.html"):
    os.remove(f"{OUT}/corrige.html")

# ---------------------------------------------------------------- Flyers
W, H = 1240, 1754   # A4 portrait à 150 dpi
GF = "/usr/share/fonts/truetype/google-fonts/Poppins-"
LB = "/usr/share/fonts/truetype/liberation/Liberation"
def P(sz, w="Regular"): return ImageFont.truetype(f"{GF}{w}.ttf", sz)
def SE(sz, st="Regular"): return ImageFont.truetype(f"{LB}Serif-{st}.ttf", sz)
def MO(sz, st="Regular"): return ImageFont.truetype(f"{LB}Mono-{st}.ttf", sz)

def qr_img(data, target):
    q = qrcode.QRCode(border=2, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(data); q.make(fit=True)
    n = q.modules_count + 4
    q.box_size = max(1, target // n)
    return q.make_image(fill_color="black", back_color="white").convert("RGB")

def T(d, x, y, s, f, fill, anchor="la"):
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)

def wrap(d, s, f, maxw):
    out, line = [], ""
    for w in s.split():
        t = (line + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: line = t
        else: out.append(line); line = w
    if line: out.append(line)
    return out

def para(d, x, y, s, f, fill, maxw, lh, anchor="la"):
    for ln in wrap(d, s, f, maxw):
        T(d, x, y, ln, f, fill, anchor); y += lh
    return y

def RR(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)

def qr_card(im, d, cx, top, size, url, pad=30, border="#1b1b1b", radius=18):
    q = qr_img(url, size)
    bw = q.width + 2 * pad
    x0 = cx - bw // 2
    RR(d, [x0, top, x0 + bw, top + bw], radius, fill="white", outline=border, width=4)
    im.paste(q, (x0 + pad, top + pad))
    return top + bw

def dotted(d, x0, x1, y, fill):
    for x in range(x0, x1, 14): d.ellipse([x, y, x + 4, y + 4], fill=fill)

def sticker_over(im, d, cx, top, size, url_real, url_fake):
    base = qr_img(url_fake, size)
    bw = base.width + 40
    x0 = cx - bw // 2
    RR(d, [x0, top, x0 + bw, top + bw], 6, fill="white", outline="#9aa", width=2)
    im.paste(base, (x0 + 20, top + 20))
    st = qr_img(url_real, size - 70)
    pad = Image.new("RGB", (size - 40, size - 40), "#fdfdfb")
    pad.paste(st, ((pad.width - st.width) // 2, (pad.height - st.height) // 2))
    pd = ImageDraw.Draw(pad); pd.rectangle([0, 0, pad.width - 1, pad.height - 1], outline="#b8b8b8", width=3)
    pad = pad.convert("RGBA").rotate(3.5, expand=True, resample=Image.BICUBIC)
    im.paste(Image.new("RGB", pad.size, "#6a6a6a"), (x0 + 42, top + 40), pad.split()[3].point(lambda a: a // 3))
    im.paste(pad, (x0 + 34, top + 30), pad)
    return top + bw

def footer(d, i):
    T(d, 40, H - 44, f"Flyer {i}", P(22), "#8a8a8a")

def flyer_menu(i, url):
    bg, ink, gold = "#f6efe0", "#3b2b14", "#8a6a2f"
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im)
    d.rectangle([40, 40, W - 40, H - 40], outline=gold, width=4)
    d.rectangle([58, 58, W - 58, H - 58], outline=gold, width=1)
    T(d, W // 2, 150, "BRASSERIE LYONNAISE · DEPUIS 1974", P(26, "Medium"), gold, "ma")
    T(d, W // 2, 205, "Chez Marcel", SE(170, "Bold"), ink, "ma")
    d.line([W // 2 - 220, 430, W // 2 - 20, 430], fill=gold, width=3)
    d.line([W // 2 + 20, 430, W // 2 + 220, 430], fill=gold, width=3)
    d.ellipse([W // 2 - 8, 422, W // 2 + 8, 438], fill=gold)
    T(d, W // 2, 470, "Menu du jour", SE(74, "Italic"), ink, "ma")
    rows = [("Entrée", "Salade de lentilles, lardons et œuf mollet"),
            ("Plat", "Quenelle de brochet, sauce Nantua"),
            ("Plat", "Andouillette AAAAA, gratin dauphinois"),
            ("Dessert", "Tarte aux pralines roses")]
    y = 570
    for lab, dish in rows:
        T(d, 150, y, lab.upper(), P(24, "Medium"), gold)
        T(d, 150, y + 34, dish, SE(44), ink); y += 105
    d.line([150, y + 6, W - 150, y + 6], fill=gold, width=2)
    T(d, W // 2, y + 40, "Plat + entrée ou dessert 19,50 €   ·   Formule complète 24 €", SE(38, "Bold"), ink, "ma")
    top = y + 100
    bottom = qr_card(im, d, 330, top, 280, url, pad=24, border=gold)
    T(d, 560, top + 30, "Notre carte complète", SE(56, "Bold"), ink)
    yy = para(d, 560, top + 110, "Vins au verre, suggestions du chef et liste des allergènes.", SE(38), ink, 540, 50)
    T(d, 560, yy + 20, "Scannez pour consulter", SE(38, "Italic"), gold)
    d.line([150, H - 250, W - 150, H - 250], fill=gold, width=1)
    T(d, W // 2, H - 220, "12 rue des Tables · 69002 Lyon · 04 78 00 00 00", SE(34), ink, "ma")
    T(d, W // 2, H - 170, "Ouvert du mardi au samedi · 12h–14h30 / 19h–22h30", SE(34), ink, "ma")
    footer(d, i); return im

def flyer_parking(i, url):
    im = Image.new("RGB", (W, H), "#dde4ec"); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 300], fill="#1d3f8f")
    RR(d, [70, 60, 250, 240], 26, fill="white")
    T(d, 160, 150, "P", P(130, "Bold"), "#1d3f8f", "mm")
    T(d, 300, 85, "STATIONNEMENT", P(72, "Bold"), "white")
    T(d, 300, 175, "Zone 3 · Centre-ville", P(42), "#cbd8f5")
    T(d, 80, 350, "Payez ici", P(110, "Bold"), "#14264f")
    RR(d, [80, 500, W - 80, 830], 20, fill="white", outline="#b9c4d4", width=3)
    T(d, 130, 530, "TARIFS · Lundi au samedi, 9h–19h", P(28, "Medium"), "#5a6a85")
    tar = [("30 minutes", "0,80 €"), ("1 heure", "1,60 €"), ("2 heures", "3,50 €"), ("4 heures (maximum)", "9,00 €")]
    yy = 595
    for a, b in tar:
        T(d, 130, yy, a, P(38), "#1b2438"); T(d, W - 130, yy, b, P(38, "Bold"), "#1b2438", "ra")
        dotted(d, 130 + int(d.textlength(a, font=P(38))) + 20, W - 130 - int(d.textlength(b, font=P(38, "Bold"))) - 20, yy + 30, "#9fb0c8")
        yy += 56
    T(d, W // 2, 870, "Paiement sans contact · sans ticket", P(36, "Medium"), "#14264f", "ma")
    bot = sticker_over(im, d, W // 2, 950, 470, url, "https://stationnement-ville.example/pay")
    T(d, W // 2, bot + 40, "Scannez pour régler votre stationnement", P(38, "Bold"), "#1d3f8f", "ma")
    d.rectangle([0, H - 190, W, H], fill="#f2c400")
    T(d, W // 2, H - 150, "Régularisez avant verbalisation", P(50, "Bold"), "#1b1b1b", "ma")
    T(d, W // 2, H - 88, "Forfait post-stationnement : 35 €", P(34), "#1b1b1b", "ma")
    footer(d, i); return im

def flyer_colis(i, url):
    im = Image.new("RGB", (W, H), "#fff4d6"); d = ImageDraw.Draw(im)
    red, ink = "#c0291f", "#2a1a10"
    d.rectangle([0, 0, W, 260], fill=red)
    T(d, W // 2, 90, "AVIS DE PASSAGE", P(88, "Bold"), "white", "mm")
    T(d, W // 2, 190, "Livraison non aboutie · Ne pas jeter", P(38, "Medium"), "#ffd9d4", "mm")
    T(d, W // 2, 340, "COLIS EN ATTENTE", P(84, "Bold"), red, "mm")
    d.line([120, 405, W - 120, 405], fill=red, width=5)
    RR(d, [110, 450, W - 110, 850], 16, fill="white", outline="#e0c990", width=3)
    rows = [("N° de suivi", "FR 7429 1180 4"), ("Statut", "Livraison impossible"),
            ("Motif", "Adresse incomplète"), ("Frais de réexpédition", "1,99 €"), ("Délai restant", "24 heures")]
    yy = 485
    for a, b in rows:
        T(d, 160, yy, a, P(32), "#7a6a50"); T(d, W - 160, yy, b, P(34, "Bold"), ink, "ra")
        yy += 70
        if a != rows[-1][0]: d.line([160, yy - 16, W - 160, yy - 16], fill="#efe3c2", width=2)
    RR(d, [110, 900, W - 110, 1090], 16, fill=red)
    yy = para(d, W // 2, 930, "Réglez 1,99 € sous 24 h", P(56, "Bold"), "white", W - 260, 70, "ma")
    T(d, W // 2, 1010, "ou votre colis sera retourné à l'expéditeur", P(38), "#ffe3df", "ma")
    bot = qr_card(im, d, W // 2, 1150, 330, url, pad=26, border=red)
    T(d, W // 2, bot + 40, "Scannez pour mettre à jour votre adresse", P(38, "Bold"), ink, "ma")
    T(d, W // 2, bot + 100, "et régler les frais de réexpédition", P(34), "#6b5a40", "ma")
    T(d, W // 2, H - 90, "Service de livraison · Ne pas répondre à ce message", P(26), "#8a7a5a", "ma")
    footer(d, i); return im

def wifi_icon(d, cx, cy, r, col, w):
    for k in (1, 2, 3):
        rr = r * k // 3
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 225, 315, fill=col, width=w)
    d.ellipse([cx - w, cy - w, cx + w, cy + w], fill=col)

def flyer_wifi(i, url):
    im = Image.new("RGB", (W, H), "#e5f1ef"); d = ImageDraw.Draw(im)
    teal, ink = "#0f5f5a", "#10302e"
    d.rectangle([0, 0, W, 330], fill=teal)
    T(d, 90, 90, "MÉDIATHÈQUE MUNICIPALE", P(34, "Medium"), "#a6d8d3")
    T(d, 90, 150, "Wi-Fi gratuit", P(110, "Bold"), "white")
    wifi_icon(d, W - 230, 290, 190, "white", 16)
    T(d, W // 2, 420, "Connectez-vous en un scan", P(60, "Bold"), ink, "ma")
    bot = qr_card(im, d, W // 2, 530, 420, url, pad=30, border=teal)
    T(d, W // 2, bot + 36, "Scannez pour vous connecter au réseau", P(38, "Medium"), teal, "ma")
    y0 = bot + 130
    RR(d, [90, y0, W - 90, y0 + 380], 18, fill="white", outline="#bcd9d5", width=3)
    T(d, 140, y0 + 30, "Réseau", P(28), "#5a7a76"); T(d, W - 140, y0 + 26, "Mediatheque-Public", MO(38, "Bold"), ink, "ra")
    d.line([140, y0 + 100, W - 140, y0 + 100], fill="#e0eeec", width=2)
    T(d, 140, y0 + 125, "Durée", P(28), "#5a7a76"); T(d, W - 140, y0 + 121, "2 h par session, renouvelable", P(34, "Medium"), ink, "ra")
    d.line([140, y0 + 195, W - 140, y0 + 195], fill="#e0eeec", width=2)
    T(d, 140, y0 + 220, "Horaires", P(28), "#5a7a76")
    T(d, W - 140, y0 + 216, "Mar–Ven 10h–18h · Sam 10h–17h", P(34, "Medium"), ink, "ra")
    d.line([140, y0 + 290, W - 140, y0 + 290], fill="#e0eeec", width=2)
    T(d, 140, y0 + 315, "Besoin d'aide ?", P(28), "#5a7a76"); T(d, W - 140, y0 + 311, "Demandez à l'accueil", P(34, "Medium"), ink, "ra")
    T(d, W // 2, H - 130, "Merci de respecter le calme des espaces de lecture", P(30), "#4a6a66", "ma")
    footer(d, i); return im

def burst(d, cx, cy, r1, r2, n, fill):
    import math
    pts = []
    for k in range(n * 2):
        r = r1 if k % 2 == 0 else r2
        a = math.pi * k / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)

def flyer_concours(i, url):
    im = Image.new("RGB", (W, H), "#ffe3ef"); d = ImageDraw.Draw(im)
    plum, pink = "#5a1246", "#e0246f"
    d.rectangle([0, 0, W, 190], fill=plum)
    T(d, W // 2, 95, "JEU CONCOURS · TIRAGE IMMÉDIAT", P(46, "Bold"), "#ffd23f", "mm")
    T(d, 80, 250, "GAGNEZ", P(158, "Bold"), pink)
    T(d, 80, 440, "UN iPHONE 15 !", P(96, "Bold"), plum)
    # téléphone stylisé
    RR(d, [850, 250, 1120, 690], 40, fill="#1b1b1b")
    RR(d, [866, 268, 1104, 672], 28, fill="#ffb3d1")
    RR(d, [930, 282, 1040, 304], 11, fill="#1b1b1b")
    RR(d, [880, 300, 950, 370], 16, fill="#e0246f")
    d.ellipse([895, 315, 935, 355], fill="#1b1b1b"); d.ellipse([905, 325, 925, 345], fill="#3a3a5a")
    burst(d, 1050, 850, 130, 100, 14, "#ffd23f")
    T(d, 1050, 830, "PLUS QUE", P(28, "Bold"), plum, "mm"); T(d, 1050, 875, "3 LOTS !", P(40, "Bold"), plum, "mm")
    T(d, 80, 600, "Aucun achat nécessaire", P(42), plum)
    T(d, 80, 660, "Scannez, jouez, repartez gagnant.", P(40, "Bold"), plum)
    # compte à rebours
    T(d, 80, 790, "Offre valable encore", P(36, "Medium"), plum)
    x = 80
    for t, lab in (("00", "heures"), ("09", "minutes"), ("59", "secondes")):
        RR(d, [x, 850, x + 190, 1010], 16, fill=plum)
        T(d, x + 95, 915, t, P(90, "Bold"), "white", "mm"); T(d, x + 95, 990, lab, P(24), "#e7b6d3", "mm")
        x += 215
    T(d, 80, 1030, "", P(10), plum)
    bot = qr_card(im, d, W // 2, 1080, 380, url, pad=26, border=pink)
    RR(d, [100, bot + 40, W - 100, bot + 150], 20, fill=pink)
    T(d, W // 2, bot + 95, "SCANNEZ MAINTENANT", P(60, "Bold"), "white", "mm")
    T(d, W // 2, H - 90, "Offre valable 10 minutes · Un seul tirage par personne", P(28), "#7a3a62", "ma")
    footer(d, i); return im

def flyer_salon(i, url):
    im = Image.new("RGB", (W, H), "#edf0fb"); d = ImageDraw.Draw(im)
    navy, ink, acc = "#1c2a4a", "#151d33", "#3b5bdb"
    d.rectangle([0, 0, W, 400], fill=navy)
    T(d, 90, 80, "ÉDITION 2026 · ENTRÉE LIBRE", P(30, "Medium"), "#9fb2e8")
    T(d, 90, 140, "Salon Numérique", P(112, "Bold"), "white")
    T(d, 90, 275, "12 & 13 octobre · Halle des Congrès", P(46), "#d5defa")
    T(d, 90, 490, "Au programme", P(58, "Bold"), ink)
    prog = [("9h30", "Ouverture et visite des stands"),
            ("10h30", "Conférence : l'IA dans la vie de tous les jours"),
            ("14h00", "Atelier : protéger ses données personnelles"),
            ("16h00", "Table ronde : le numérique et les territoires")]
    y = 590
    for h, t in prog:
        RR(d, [90, y, 290, y + 84], 12, fill=acc)
        T(d, 190, y + 42, h, P(44, "Bold"), "white", "mm")
        T(d, 320, y + 42, t, P(36), ink, "lm"); y += 110
    d.line([90, y + 10, W - 90, y + 10], fill="#c6cff0", width=2)
    y += 60
    bot = qr_card(im, d, 330, y, 300, url, pad=24, border=navy)
    T(d, 560, y + 25, "Programme complet", P(48, "Bold"), ink)
    yy = para(d, 560, y + 100, "Horaires détaillés, plan de la halle et inscriptions.", P(34), "#33405f", 580, 46)
    T(d, 560, yy + 20, "Site officiel", P(26), "#5a6a95")
    T(d, 560, yy + 55, "salon-numerique.example", MO(38, "Bold"), acc)
    T(d, 90, bot + 60, "Le programme est aussi disponible à l'accueil de la Halle.", P(32), "#33405f")
    d.rectangle([0, H - 190, W, H], fill=navy)
    T(d, 90, H - 150, "Organisé par l'Association Numérique & Territoires", P(34, "Medium"), "white")
    T(d, 90, H - 95, "Halle des Congrès · Accès tram et parking public à proximité", P(28), "#9fb2e8")
    footer(d, i); return im

MAKERS = dict(menu=flyer_menu, parking=flyer_parking, colis=flyer_colis,
              wifi=flyer_wifi, concours=flyer_concours, salon=flyer_salon)

imgs = []
for i, s in enumerate(S, 1):
    im = MAKERS[s["slug"]](i, f"{BASE}/{s['slug']}.html")
    im.save(f"{OUT}/flyers/flyer{i}_{s['slug']}.png", optimize=True)
    imgs.append(im)
imgs[0].save(f"{OUT}/flyers/tous_les_flyers.pdf", save_all=True, append_images=imgs[1:], resolution=150)
print("OK ->", BASE)