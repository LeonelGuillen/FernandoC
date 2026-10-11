(() => {
  // Menú móvil
  const burger = document.querySelector('.burger');
  const menu = document.getElementById('menu');
  if (burger && menu) {
    burger.addEventListener('click', () => {
      const open = menu.classList.toggle('open');
      burger.setAttribute('aria-expanded', open);
    });
    menu.addEventListener('click', e => { if (e.target.tagName === 'A') { menu.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); } });
  }

  // Animación de aparición
  const els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -60px 0px' });
    els.forEach(el => io.observe(el));
  } else els.forEach(el => el.classList.add('in'));

  // Contadores animados en las cifras
  const counters = document.querySelectorAll('[data-count]');
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const yearNow = new Date().getFullYear();
  const run = el => {
    let to = +el.dataset.count;
    if (el.dataset.since) to = yearNow - +el.dataset.since;   // años transcurridos, se actualiza solo cada año
    const from = +(el.dataset.from || 0), suf = el.dataset.suffix || '';
    if (reduce) { el.textContent = to + suf; return; }
    const dur = 1600, t0 = performance.now();
    const step = t => {
      const p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(from + (to - from) * e) + (p === 1 ? suf : '');
      if (p < 1) requestAnimationFrame(step); else el.classList.add('done');
    };
    el.textContent = from; requestAnimationFrame(step);
  };
  if (counters.length) {
    if ('IntersectionObserver' in window) {
      const co = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { run(en.target); co.unobserve(en.target); } }), { threshold: .6 });
      counters.forEach(c => co.observe(c));
    } else counters.forEach(run);
  }

  // Filtros + búsqueda (publicaciones / participaciones)
  const list = document.querySelector('[data-filter-list]');
  if (list) {
    const items = [...list.querySelectorAll('[data-type]')];
    const heads = [...list.querySelectorAll('[data-year-head]')];
    const chips = [...document.querySelectorAll('.chip[data-f]')];
    const q = document.getElementById('q');
    const count = document.getElementById('count');
    const empty = document.getElementById('empty');
    let f = 'all';
    const norm = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
    const apply = () => {
      const term = norm(q ? q.value.trim() : '');
      let n = 0;
      items.forEach(it => {
        const okF = f === 'all' || it.dataset.type.split(' ').includes(f);
        const okQ = !term || norm(it.textContent).includes(term);
        const show = okF && okQ;
        it.hidden = !show; if (show) n++;
      });
      heads.forEach(h => {
        const y = h.dataset.yearHead;
        h.hidden = !items.some(it => it.dataset.year === y && !it.hidden);
      });
      if (count) count.textContent = n + (n === 1 ? ' resultado' : ' resultados');
      if (empty) empty.hidden = n !== 0;
    };
    chips.forEach(c => c.addEventListener('click', () => {
      chips.forEach(x => x.setAttribute('aria-pressed', 'false'));
      c.setAttribute('aria-pressed', 'true'); f = c.dataset.f; apply();
    }));
    if (q) q.addEventListener('input', apply);
    apply();
  }

  // Formulario de contacto (Cloudflare Pages Function /api/contact)
  const form = document.getElementById('contact-form');
  if (form) {
    const st = document.getElementById('form-status');
    form.addEventListener('submit', async e => {
      e.preventDefault();
      const btn = form.querySelector('button[type=submit]');
      btn.disabled = true; btn.textContent = 'Enviando…';
      st.className = 'form-status';
      try {
        const r = await fetch('/api/contact', { method: 'POST', body: new FormData(form) });
        const j = await r.json().catch(() => ({}));
        if (!r.ok || !j.ok) throw new Error(j.error || 'No fue posible enviar el mensaje.');
        st.className = 'form-status ok';
        st.textContent = 'Gracias. Su mensaje fue enviado correctamente.';
        form.reset();
      } catch (err) {
        st.className = 'form-status err';
        st.textContent = err.message;
      } finally { btn.disabled = false; btn.textContent = 'Enviar mensaje'; }
    });
  }

  // Videos: cargar YouTube solo al hacer clic (privacidad y velocidad)
  document.querySelectorAll('[data-yt]').forEach(b => b.addEventListener('click', () => {
    const f = document.createElement('iframe');
    f.className = 'vframe'; f.title = b.getAttribute('aria-label');
    f.src = 'https://www.youtube-nocookie.com/embed/' + b.dataset.yt + '?autoplay=1&rel=0';
    f.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture'; f.allowFullscreen = true;
    b.replaceWith(f);
  }));
  document.querySelectorAll('[data-print]').forEach(b => b.addEventListener('click', () => window.print()));
  const y = document.getElementById('yr'); if (y) y.textContent = new Date().getFullYear();
})();
