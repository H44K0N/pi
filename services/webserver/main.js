'use strict';

document.querySelector('.jump-link').addEventListener('click', function (e) {
  e.preventDefault();
  var inner = document.querySelector('.edu-inner');
  var sec = document.getElementById('education');
  sec.style.height = 'auto';
  sec.style.overflow = 'visible';
  inner.classList.remove('edu-collapsed');
  inner.style.padding = '60px 0 80px';
  document.getElementById('education').classList.add('edu-revealed');
  setTimeout(function () {
    document.getElementById('education').scrollIntoView({ behavior: 'smooth' });
  }, 10);
});

document.querySelectorAll('.curriculum-toggle').forEach(function (el) {
  el.addEventListener('click', function () {
    el.closest('.curriculum').classList.toggle('open');
  });
});

document.querySelectorAll('.tl-expand').forEach(function (el) {
  el.addEventListener('click', function () {
    var tl = el.closest('.timeline');
    tl.classList.toggle('tl-open');
    el.textContent = tl.classList.contains('tl-open') ? 'Show less' : 'Show more';
  });
});
