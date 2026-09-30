const target = [[1,1,1,1,1,1,1,0,1,1,1,0,1,0,0,0,0,1,1,1,1,0,0,1,0,0,1,1,1,1,1,1,1],[1,0,0,0,0,0,1,0,1,1,1,0,0,0,0,0,1,1,0,1,0,1,0,0,1,0,1,0,0,0,0,0,1],[1,0,1,1,1,0,1,0,1,0,1,1,0,1,0,1,1,0,0,0,0,1,0,1,1,0,1,0,1,1,1,0,1],[1,0,1,1,1,0,1,0,1,1,0,1,0,0,1,1,1,1,1,0,1,0,0,1,1,0,1,0,1,1,1,0,1],[1,0,1,1,1,0,1,0,0,0,0,0,0,1,1,0,1,0,1,1,0,1,0,1,0,0,1,0,1,1,1,0,1],[1,0,0,0,0,0,1,0,1,0,0,1,1,1,1,1,0,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0,1],[1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0],[1,1,0,0,1,1,1,0,0,0,0,1,0,1,1,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,1,1,1],[1,1,0,0,0,1,0,1,0,1,1,0,1,0,0,0,0,1,0,0,0,1,1,1,0,0,0,1,0,0,1,0,0],[1,1,1,1,1,0,1,0,1,0,0,1,1,1,1,1,0,0,1,0,0,0,0,1,1,1,0,0,1,0,1,1,0],[0,0,1,1,1,0,0,1,1,0,1,1,0,1,0,1,1,0,0,0,0,1,0,0,1,0,0,0,1,1,0,0,0],[1,1,1,1,0,1,1,1,1,0,1,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,0,1,1],[1,1,1,1,0,0,0,1,1,0,0,0,0,1,1,0,1,0,1,1,0,0,1,1,0,0,0,1,0,0,0,0,0],[0,1,1,1,1,1,1,0,1,1,1,0,0,0,0,0,1,1,0,0,1,0,0,1,1,1,0,0,0,1,1,1,0],[0,0,0,1,0,0,0,1,0,0,0,0,1,0,1,0,0,1,1,1,1,1,1,0,1,1,0,0,0,1,0,0,0],[0,1,0,0,0,1,1,0,0,0,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,0,1,0,1,0,0,0,1],[0,0,1,0,1,0,0,1,1,1,1,0,1,0,0,0,0,1,0,0,0,1,1,1,1,1,0,1,0,1,0,0,0],[1,0,0,0,0,0,1,1,0,0,1,1,1,1,1,1,0,0,1,0,1,1,0,1,1,0,0,0,1,0,1,1,0],[0,1,0,0,0,1,0,1,0,1,1,1,0,1,0,1,1,0,0,1,1,1,0,1,1,0,1,1,0,1,0,0,0],[1,0,1,0,1,1,1,1,0,0,0,0,1,1,0,0,0,0,0,1,0,1,1,1,1,0,1,1,1,0,0,0,1],[1,0,1,0,0,1,0,1,1,1,0,0,0,1,1,0,1,0,1,1,0,0,0,1,0,1,0,1,0,1,0,0,0],[0,0,1,1,1,0,1,0,1,1,1,0,0,0,0,0,1,1,0,0,1,1,0,1,1,1,0,1,0,0,1,1,0],[0,0,0,0,0,0,0,0,0,1,1,0,1,0,1,0,0,1,1,0,0,1,1,0,1,1,0,0,0,0,0,0,0],[1,1,0,0,1,0,1,1,1,0,1,1,0,1,1,1,1,0,1,0,0,0,1,1,1,1,1,1,1,1,0,1,0],[0,0,0,0,0,0,0,0,1,1,1,0,1,0,0,0,0,1,0,0,1,0,1,0,1,0,0,0,1,1,1,1,0],[1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,0,0,1,0,1,1,1,0,1,0,1,0,1,0,1,1,0],[1,0,0,0,0,0,1,0,1,0,0,1,0,1,0,1,1,0,0,1,1,1,0,0,1,0,0,0,1,0,0,1,1],[1,0,1,1,1,0,1,0,1,0,1,0,1,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,1,1,0,1,0],[1,0,1,1,1,0,1,0,0,1,1,0,0,1,1,0,1,0,1,0,0,0,1,1,0,1,1,0,1,1,1,1,0],[1,0,1,1,1,0,1,0,0,0,1,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,1,1,1,0,1,0,0],[1,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,0,1,1,0,1,1,0,1,1,1,1,0,0,0,0,0,0],[1,1,1,1,1,1,1,0,1,0,0,1,0,1,1,1,1,0,1,1,0,1,0,1,1,1,0,1,0,1,0,0,1]];
const zones = [["f","f","f","f","f","f","f","f","m","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","f","f","f","f","f","f","f","f"],["f","f","f","f","f","f","f","f","m","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","f","f","f","f","f","f","f","f"],["f","f","f","f","f","f","f","f","m","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","f","f","f","f","f","f","f","f"],["f","f","f","f","f","f","f","f","m","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","f","f","f","f","f","f","f","f"],["f","f","f","f","f","f","f","f","m","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","f","f","f","f","f","f","f","f"],["f","f","f","f","f","f","f","f","m","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","f","f","f","f","f","f","f","f"],["f","f","f","f","f","f","f","f","t","t","t","t","t","t","t","t","t","t","t","t","t","t","t","t","t","f","f","f","f","f","f","f","f"],["f","f","f","f","f","f","f","f","m","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","f","f","f","f","f","f","f","f"],["m","m","m","m","m","m","t","m","m","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","m","m","m","m","m","m","m","m"],["d","d","d","d","d","d","t","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["d","d","d","d","d","d","t","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["d","d","d","d","d","d","t","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["d","d","d","d","d","d","t","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["d","d","d","d","d","d","t","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["d","d","d","d","d","d","t","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["d","d","d","d","d","d","t","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["d","d","d","d","d","d","t","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["d","d","d","d","d","d","t","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["d","d","d","d","d","d","t","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["d","d","d","d","d","d","t","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["d","d","d","d","d","d","t","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["d","d","d","d","d","d","t","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["d","d","d","d","d","d","t","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["d","d","d","d","d","d","t","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["d","d","d","d","d","d","t","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["f","f","f","f","f","f","f","f","m","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["f","f","f","f","f","f","f","f","m","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["f","f","f","f","f","f","f","f","m","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["f","f","f","f","f","f","f","f","m","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["f","f","f","f","f","f","f","f","m","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["f","f","f","f","f","f","f","f","m","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["f","f","f","f","f","f","f","f","m","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],["f","f","f","f","f","f","f","f","m","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"]];

let N = target.length, T = N / 3;
const COLORS = { f:"#e03131", t:"#f08c00", m:"#7048e8", d:"#1c1e26" };
const LIGHT  = { f:"#ffe3e3", t:"#fff0d6", m:"#ece5ff", d:"#ffffff" };
let pieces = [], selected = null, dragFrom = null, lastHint = null;
const $ = id => document.getElementById(id), board = $("board");

const sub = (m, id) => {
  const ox = (id % 3) * T, oy = Math.floor(id / 3) * T;
  return Array.from({ length: T }, (_, y) => Array.from({ length: T }, (_, x) => m[oy + y][ox + x]));
};
const rot1 = m => m.map((row, y) => row.map((_, x) => m[T - 1 - x][y]));
const rot = (m, r) => { for (let i = 0; i < r; i++) m = rot1(m); return m; };

function assemble() {
  const out = Array.from({ length: N }, () => Array(N).fill(0));
  pieces.forEach((p, pos) => {
    const m = rot(sub(target, p.id), p.rot), ox = (pos % 3) * T, oy = Math.floor(pos / 3) * T;
    m.forEach((row, y) => row.forEach((v, x) => { out[oy + y][ox + x] = v; }));
  });
  return out;
}
const isSolved = () => assemble().every((row, y) => row.every((v, x) => v === target[y][x]));
const isCorrect = (p, pos) => p.id === pos && p.rot === 0;
const countOk = () => pieces.filter((p, pos) => isCorrect(p, pos)).length;
const easy = () => $("easyChk").checked;

function drawTile(canvas, p) {
  const bits = rot(sub(target, p.id), p.rot), zn = rot(sub(zones, p.id), p.rot), s = 30, ctx = canvas.getContext("2d");
  canvas.width = canvas.height = T * s;
  const colored = $("zonesChk").checked;
  for (let y = 0; y < T; y++) for (let x = 0; x < T; x++) {
    const z = zn[y][x];
    ctx.fillStyle = bits[y][x] ? (colored ? COLORS[z] : "#111") : (colored ? LIGHT[z] : "#fff");
    ctx.fillRect(x * s, y * s, s, s);
  }
}
function drawPreview() {
  const q = 4, size = N + 2 * q, c = $("preview"), ctx = c.getContext("2d");
  c.width = c.height = size; ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, size, size); ctx.fillStyle = "#000";
  assemble().forEach((row, y) => row.forEach((v, x) => { if (v) ctx.fillRect(x + q, y + q, 1, 1); }));
}
function render() {
  board.innerHTML = "";
  board.classList.toggle("easy", easy());
  pieces.forEach((p, pos) => {
    const d = document.createElement("div");
    d.className = "tile" + (selected === pos ? " sel" : "") + (easy() && isCorrect(p, pos) ? " ok" : "") + (lastHint === pos ? " hint" : "");
    d.draggable = true;
    d.setAttribute("role", "button");
    d.setAttribute("aria-label", "Tuile " + (pos + 1) + " sur 9");
    const cv = document.createElement("canvas"); drawTile(cv, p);
    const b = document.createElement("button"); b.type = "button"; b.textContent = "↻"; b.title = "Tourner d'un quart de tour"; b.setAttribute("aria-label", "Tourner la tuile");
    b.onclick = e => { e.stopPropagation(); p.rot = (p.rot + 1) % 4; update(); };
    d.append(cv, b);
    d.onclick = () => {
      if (selected === null) selected = pos;
      else { if (selected !== pos) swap(selected, pos); selected = null; }
      update();
    };
    d.ondragstart = e => { dragFrom = pos; e.dataTransfer.effectAllowed = "move"; e.dataTransfer.setData("text/plain", pos); };
    d.ondragover = e => { e.preventDefault(); d.classList.add("over"); };
    d.ondragleave = () => d.classList.remove("over");
    d.ondrop = e => { e.preventDefault(); if (dragFrom !== null && dragFrom !== pos) swap(dragFrom, pos); dragFrom = null; selected = null; update(); };
    board.append(d);
  });
}
function swap(a, b) { [pieces[a], pieces[b]] = [pieces[b], pieces[a]]; }

function update() {
  render(); drawPreview();
  const st = $("status");
  if (isSolved()) {
    st.className = "win";
    st.textContent = "Bravo ! Le QR code est reconstitué. Il est maintenant lisible : vous pouvez le scanner avec votre téléphone.";
  } else if (selected !== null) {
    st.className = "";
    st.textContent = "Tuile choisie. Touchez maintenant la tuile avec laquelle l'échanger.";
  } else {
    st.className = "";
    const n = countOk();
    st.textContent = n + " tuile" + (n > 1 ? "s" : "") + " sur 9 bien placée" + (n > 1 ? "s" : "") + (easy() ? "." : " (au bon endroit et dans le bon sens).") + " Le QR code ne peut pas encore être lu.";
  }
}
function shuffle() {
  do {
    const ids = [0, 1, 2, 3, 4, 5, 6, 7, 8];
    for (let i = ids.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [ids[i], ids[j]] = [ids[j], ids[i]]; }
    pieces = ids.map(id => ({ id, rot: easy() ? 0 : Math.floor(Math.random() * 4) }));
  } while (isSolved());
  selected = null; lastHint = null; update();
}
function hint() {
  for (let pos = 0; pos < 9; pos++) {
    if (isCorrect(pieces[pos], pos)) continue;
    const j = pieces.findIndex(p => p.id === pos);
    swap(pos, j); pieces[pos].rot = 0;
    selected = null; lastHint = pos; update();
    setTimeout(() => { lastHint = null; render(); }, 1600);
    return;
  }
}
$("newBtn").onclick = shuffle;
$("hintBtn").onclick = hint;
$("solveBtn").onclick = () => { pieces = [0, 1, 2, 3, 4, 5, 6, 7, 8].map(id => ({ id, rot: 0 })); selected = null; lastHint = null; update(); };
$("zonesChk").onchange = update;
$("easyChk").onchange = shuffle;
shuffle();