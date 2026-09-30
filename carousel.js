
(function () {
  var base = 'flyers/';
  var files = ["flyer1_menu.png", "flyer2_parking.png", "flyer3_colis.png", "flyer4_wifi.png", "flyer5_concours.png", "flyer6_salon.png"];
  var i = 0;
  var img = document.getElementById('c-img'), count = document.getElementById('c-count');
  var thumbs = document.getElementById('c-thumbs');
  var box = document.getElementById('lightbox'), limg = document.getElementById('l-img');

  files.forEach(function (f, k) {
    var t = document.createElement('img');
    t.src = base + f; t.alt = 'Flyer ' + (k + 1);
    t.addEventListener('click', function () { go(k); });
    thumbs.appendChild(t);
  });

  function go(n) {
    i = (n + files.length) % files.length;
    img.src = limg.src = base + files[i];
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
