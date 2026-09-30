#!/usr/bin/env python3
"""Génère le site (racine du dépôt) + les flyers (dossier flyers/).
Usage : python build.py https://TON-PSEUDO.github.io/qr-atelier
"""
import sys, os, html
import qrcode
from PIL import Image, ImageDraw, ImageFont

BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://TON-PSEUDO.github.io/qr-atelier").rstrip("/")
OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(f"{OUT}/flyers", exist_ok=True)

# ---------- Scénarios ----------
S = [
 dict(slug="menu", safe=True, titre="Menu du restaurant",
  indices=["Le QR est imprimé dans le même bloc que le menu, aucun sticker ni décalage.",
           "Le contexte est logique : un menu se consulte, on ne vous demande rien.",
           "Aucune urgence, aucune demande de paiement ou de mot de passe."]),
 dict(slug="parking", safe=False, titre="Paiement de parking",
  indices=["Le QR est un sticker collé par-dessus un autre : bords visibles, léger décalage, l'ancien code dépasse.",
           "Les faux QR sur horodateurs sont une arnaque classique : ils redirigent vers un faux site de paiement.",
           "Le nom de la page (parking) annonce un paiement : on ne paie jamais via un QR collé sur une borne.",
           "Bon réflexe : utiliser l'application officielle de la ville ou l'horodateur lui-même."]),
 dict(slug="colis", safe=False, titre="Colis en attente",
  indices=["Message de pression : « sous 24 h », « retourné à l'expéditeur ».",
           "Vous n'attendiez pas de colis, et le transporteur n'est même pas nommé précisément.",
           "Frais minuscules (1,99 €) : le but est de récupérer vos données bancaires.",
           "Bon réflexe : suivre son colis depuis le site ou l'appli du transporteur, tapé à la main."]),
 dict(slug="wifi", safe=True, titre="Wi-Fi de la médiathèque",
  indices=["Affiche officielle, plastifiée, à l'accueil, cohérente avec le lieu.",
           "Le QR sert à se connecter au réseau, sans formulaire ni identifiants à saisir.",
           "En cas de doute, on peut demander à l'accueil de confirmer."]),
 dict(slug="concours", safe=False, titre="Concours « gagnez un iPhone »",
  indices=["Trop beau pour être vrai : un smartphone dernier cri pour un simple scan.",
           "Compte à rebours et « plus que 3 lots » : fausse urgence.",
           "Aucun organisateur identifiable, pas de règlement, pas de mentions légales.",
           "Bon réflexe : ne jamais donner ses données personnelles pour un gain surprise."]),
 dict(slug="salon", safe=True, titre="Programme du salon",
  indices=["Organisateur clairement identifié, adresse du site officiel imprimée en toutes lettres.",
           "Le QR est un complément : l'information existe aussi sans le scanner.",
           "Rien n'est demandé en échange."]),
]

PRATIQUES = [
 "Lire l'URL affichée par l'appareil photo <strong>avant</strong> d'ouvrir le lien.",
 "Ne jamais saisir identifiants, code SMS ou carte bancaire après un scan.",
 "Se méfier des QR en espace public : vérifier qu'ils ne sont pas collés par-dessus un autre.",
 "Se méfier de l'urgence, de la menace et des gains inattendus.",
 "En cas de doute : passer par le site ou l'appli officielle, tapé à la main.",
 "Signaler un QR suspect au gestionnaire du lieu.",
]

# ---------- Site ----------
CAROUSEL_CSS = """
.carousel{position:relative;display:flex;align-items:center;justify-content:center;gap:6px}
.carousel img{width:100%;max-width:340px;border-radius:10px;border:1px solid var(--line);cursor:zoom-in;display:block}
.nav{flex:none;width:44px;height:44px;border-radius:50%;border:0;background:#2b5cff;color:#fff;font-size:28px;line-height:1;cursor:pointer}
.nav:active{transform:scale(.94)}
.counter{text-align:center;margin:.6em 0 0;font-weight:600}
.thumbs{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;margin-top:10px}
.thumbs img{width:48px;border-radius:5px;border:2px solid transparent;cursor:pointer;opacity:.6}
.thumbs img.active{border-color:#2b5cff;opacity:1}
.lightbox{position:fixed;inset:0;background:rgba(0,0,0,.88);display:flex;align-items:center;justify-content:center;gap:6px;padding:12px;z-index:10}
.lightbox[hidden]{display:none}
.lightbox img{max-width:calc(100% - 100px);max-height:100%;object-fit:contain;border-radius:8px;cursor:zoom-out}
.lightbox .close{position:absolute;top:10px;right:10px;width:40px;height:40px;border-radius:50%;border:0;background:#fff;color:#000;font-size:20px;cursor:pointer}
"""

CAROUSEL_JS = """
(function () {
  var files = %s;
  var i = 0;
  var img = document.getElementById('c-img'), count = document.getElementById('c-count');
  var thumbs = document.getElementById('c-thumbs');
  var box = document.getElementById('lightbox'), limg = document.getElementById('l-img');

  files.forEach(function (f, k) {
    var t = document.createElement('img');
    t.src = 'flyers/' + f; t.alt = 'Flyer ' + (k + 1);
    t.addEventListener('click', function () { go(k); });
    thumbs.appendChild(t);
  });

  function go(n) {
    i = (n + files.length) %% files.length;
    img.src = limg.src = 'flyers/' + files[i];
    img.alt = limg.alt = 'Flyer ' + (i + 1);
    count.textContent = 'Flyer ' + (i + 1) + ' / ' + files.length;
    Array.prototype.forEach.call(thumbs.children, function (t, k) { t.classList.toggle('active', k === i); });
  }
  function open() { box.hidden = false; }
  function close() { box.hidden = true; }

  document.querySelectorAll('.prev').forEach(function (b) { b.addEventListener('click', function () { go(i - 1); }); });
  document.querySelectorAll('.next').forEach(function (b) { b.addEventListener('click', function () { go(i + 1); }); });
  img.addEventListener('click', open);
  limg.addEventListener('click', close);
  box.querySelector('.close').addEventListener('click', close);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') go(i - 1);
    if (e.key === 'ArrowRight') go(i + 1);
    if (e.key === 'Escape') close();
  });
  var x0 = null;
  [img, limg].forEach(function (el) {
    el.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    el.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 40) go(i + (dx < 0 ? 1 : -1));
      x0 = null;
    });
  });
  go(0);
})();
"""
FILES = [f"flyer{n}_{s['slug']}.png" for n, s in enumerate(S, 1)]
CAROUSEL_JS = CAROUSEL_JS % __import__("json").dumps(FILES)

CSS = """
:root{--bg:#f5f6fa;--fg:#1c2233;--card:#fff;--ok:#0f8a4f;--ko:#c62828;--muted:#5b6478;--line:#dfe3ee}
@media(prefers-color-scheme:dark){:root{--bg:#12151f;--fg:#eef0f7;--card:#1c2030;--muted:#a3abc0;--line:#2c3247}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:640px;margin:0 auto;padding:20px 16px 48px}
h1{font-size:1.7rem;line-height:1.2;margin:.2em 0 .5em}
h2{font-size:1.15rem;margin:1.4em 0 .5em}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin:16px 0}
.warn{border-left:6px solid #f5a300}
.banner{border-radius:14px;padding:26px 18px;text-align:center;color:#fff;margin:8px 0 16px}
.banner.ko{background:var(--ko)}.banner.ok{background:var(--ok)}
.banner h1{margin:0;font-size:2rem}.banner p{margin:.5em 0 0}
ul,ol{padding-left:1.2em}li{margin:.35em 0}
.btn{display:inline-block;background:#2b5cff;color:#fff;text-decoration:none;padding:12px 18px;border-radius:10px;font-weight:600}
.muted{color:var(--muted);font-size:.92rem}
h2.first{margin-top:0}
table{width:100%;border-collapse:collapse}td,th{padding:8px;border-bottom:1px solid var(--line);text-align:left}
"""

HEAD = """<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>{t}</title>
<link rel="stylesheet" href="style.css"><link rel="stylesheet" href="carousel.css"></head><body><main>"""

def page(s):
    ok = s["safe"]
    ban = ('<div class="banner ok"><h1>✅ Ce QR code était safe</h1><p>Aucun piège ici. Mais pourquoi pouvait-on lui faire confiance ?</p></div>'
           if ok else
           '<div class="banner ko"><h1>⚠️ Vous êtes hacké !</h1><p>Simulation pédagogique : rien n\'a été volé, mais ç\'aurait pu.</p></div>')
    lis = "".join(f"<li>{html.escape(i)}</li>" for i in s["indices"])
    titre_ind = "Ce qui rassurait" if ok else "Ce qui aurait dû vous alerter"
    prat = "".join(f"<li>{p}</li>" for p in PRATIQUES)
    return (HEAD.format(t=s["titre"]) + ban +
      f'<div class="card"><h2 class="first">🤔 Prenez 30 secondes</h2><p>Regardez de nouveau le flyer « {html.escape(s["titre"])} ». Qu\'est-ce qui pouvait vous mettre la puce à l\'oreille ?</p></div>'
      f'<details class="card"><summary><strong>{titre_ind}</strong> (touchez pour voir)</summary><ul>{lis}</ul></details>'
      f'<div class="card"><h2 class="first">🛡️ Les bonnes pratiques</h2><ul>{prat}</ul></div>'
      '<p><a class="btn" href="index.html">← Retour à l\'atelier</a></p></main></body></html>')

INDEX = HEAD.format(t="Atelier QR codes") + """
<h1>📱 Atelier : saurez-vous repérer le QR code piégé ?</h1>
<div class="card warn"><strong>⚠️ Attention</strong>
<p>Cette activité utilise <strong>votre téléphone</strong>. Rien de dangereux : toutes les pages sont fabriquées pour l'atelier, et aucune donnée n'est collectée.</p></div>
<div class="card"><h2 class="first">La consigne</h2>
<ol>
<li>Récupérez les <strong>6 flyers</strong> disposés dans la salle.</li>
<li>Scannez chaque QR code avec l'appareil photo de votre téléphone.</li>
<li><strong>Avant d'ouvrir le lien</strong>, observez le flyer et l'adresse affichée, puis notez : ✅ sûr ou ❌ douteux.</li>
<li>Ouvrez ensuite le lien : la page vous dit si vous aviez raison.</li>
<li>Sur chaque page, cherchez ce qui aurait pu vous alerter.</li>
</ol></div>
<div class="card"><h2 class="first">Les flyers</h2>
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
<div class="card"><h2 class="first">Votre feuille de route</h2>
<table><tr><th>Flyer</th><th>Mon avis</th></tr>
""" + "".join(f"<tr><td>Flyer {i+1}</td><td>☐ ✅ &nbsp; ☐ ❌</td></tr>" for i in range(6)) + """
</table></div>
<p class="muted">Animateur : <a href="corrige.html">corrigé</a> (ne pas ouvrir avant la fin !)</p>
</main><script src="carousel.js"></script></body></html>"""

CORRIGE = HEAD.format(t="Corrigé") + "<h1>Corrigé (animateur)</h1><div class='card'><table><tr><th>Flyer</th><th>Thème</th><th>Verdict</th></tr>" + "".join(
    f"<tr><td>{i+1}</td><td><a href='{s['slug']}.html'>{html.escape(s['titre'])}</a></td><td>{'✅ safe' if s['safe'] else '❌ piégé'}</td></tr>"
    for i, s in enumerate(S)) + "</table></div><p><a class='btn' href='index.html'>← Accueil</a></p></main></body></html>"

open(f"{OUT}/style.css", "w").write(CSS)
open(f"{OUT}/carousel.css", "w").write(CAROUSEL_CSS)
open(f"{OUT}/carousel.js", "w").write(CAROUSEL_JS)
open(f"{OUT}/index.html", "w").write(INDEX)
open(f"{OUT}/corrige.html", "w").write(CORRIGE)
for s in S:
    open(f"{OUT}/{s['slug']}.html", "w").write(page(s))

# ---------- Flyers ----------
W, H = 600, 850
def F(sz, bold=False):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if bold else ''}.ttf", sz)

def qr_img(data, size):
    q = qrcode.QRCode(border=2, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(data); q.make(fit=True)
    return q.make_image(fill_color="black", back_color="white").convert("RGB").resize((size, size), Image.NEAREST)

def center(d, y, txt, font, fill):
    w = d.textlength(txt, font=font)
    d.text(((W - w) / 2, y), txt, font=font, fill=fill)

def wrap(d, txt, font, maxw):
    out, line = [], ""
    for w in txt.split():
        t = (line + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: line = t
        else: out.append(line); line = w
    out.append(line); return out

def flyer(i, s):
    url = f"{BASE}/{s['slug']}.html"
    bg, head, sub, foot, extra = {
     "menu":   ("#fbf3e4", "Chez Marcel", "Brasserie · Menu du jour", "Scannez pour consulter notre carte", None),
     "parking":("#e8edf3", "STATIONNEMENT", "Zone 3 · Payez ici", "Régularisez avant verbalisation", None),
     "colis":  ("#fff6e0", "COLIS EN ATTENTE", "Livraison impossible : adresse incomplète", "Réglez 1,99 € sous 24 h ou votre colis sera retourné", None),
     "wifi":   ("#e6f3f1", "Médiathèque municipale", "Wi-Fi gratuit pour les usagers", "Scannez pour vous connecter au réseau", None),
     "concours":("#ffe9f2", "🎁 GAGNEZ UN iPHONE 15 !", "Tirage immédiat · Plus que 3 lots !", "Scannez maintenant, offre valable 10 minutes", None),
     "salon":  ("#eaeefc", "Salon Numérique 2026", "12 & 13 octobre · Halle des Congrès", "Programme complet : salon-numerique.example", None),
    }[s["slug"]]
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im)
    accent = "#c62828" if s["slug"] in ("colis", "concours") else "#1c2a4a"
    d.rectangle([0, 0, W, 120], fill=accent)
    hf = F(38 if len(head) < 20 else 32, True)
    center(d, 38, head, hf, "white")
    y = 150
    for ln in wrap(d, sub, F(26), W - 80):
        center(d, y, ln, F(26), "#222"); y += 36
    qs = 330; qx, qy = (W - qs) // 2, 300

    if s["slug"] == "parking":
        # vrai QR d'origine dessous, sticker décalé et tourné par-dessus
        base = qr_img("https://stationnement-ville.example/pay", qs)
        im.paste(base, (qx, qy))
        st = qr_img(url, qs - 30)
        pad = Image.new("RGB", (qs - 10, qs - 10), "#fdfdfd")
        pad.paste(st, (5, 5))
        pad = ImageOps_border(pad)
        pad = pad.convert("RGBA").rotate(3.5, expand=True, resample=Image.BICUBIC)
        sh = Image.new("RGBA", pad.size, (0, 0, 0, 0))
        im.paste(Image.new("RGB", pad.size, "#777"), (qx + 20, qy + 16), pad.split()[3].point(lambda a: a // 3))
        im.paste(pad, (qx + 14, qy + 8), pad)
    else:
        box = Image.new("RGB", (qs + 30, qs + 30), "white")
        box.paste(qr_img(url, qs), (15, 15))
        im.paste(box, (qx - 15, qy - 15))

    y = qy + qs + 40
    for ln in wrap(d, foot, F(23, True), W - 80):
        center(d, y, ln, F(23, True), accent); y += 32
    d.text((14, H - 30), f"Flyer {i}", font=F(16), fill="#888")
    return im

def ImageOps_border(img):
    d = ImageDraw.Draw(img); d.rectangle([0, 0, img.width - 1, img.height - 1], outline="#bbb", width=2); return img

imgs = []
for i, s in enumerate(S, 1):
    im = flyer(i, s); im.save(f"{OUT}/flyers/flyer{i}_{s['slug']}.png"); imgs.append(im)
imgs[0].save(f"{OUT}/flyers/tous_les_flyers.pdf", save_all=True, append_images=imgs[1:], resolution=100)
print("OK ->", BASE)
