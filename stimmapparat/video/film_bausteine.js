/* Regie für das Baustein-Video. Wird vom Renderer in bausteine.html eingefügt; window.__TIMELINE muss gesetzt sein.
   Alle Einblendungen werden aus der Videozeit t berechnet, damit jedes Bild reproduzierbar ist. */
(() => {
  'use strict';
  const API = window.Bausteine, TL = window.__TIMELINE;
  const $ = s => document.querySelector(s);
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v)), ease = x => { x = clamp(x, 0, 1); return x * x * (3 - 2 * x); };
  const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
  const MS = t => 1e8 + t * 1000; // Seitenzeit in ms zur Videozeit t

  document.body.classList.add('film');
  const st0 = el('div'); st0.id = 'fstage'; document.body.appendChild(st0); st0.appendChild($('#stage'));
  const step = el('div', 'fl'); step.id = 'fStep'; step.innerHTML = '<span class="n"></span><small></small><b></b>'; st0.appendChild(step);
  const parts = el('div', 'fl'); parts.id = 'fParts'; parts.innerHTML = '<h3>Bauteile</h3><ul></ul>'; st0.appendChild(parts);
  const sub = el('div', 'fl'); sub.id = 'fSub'; sub.innerHTML = '<span></span>'; st0.appendChild(sub);
  const prog = el('div', 'fl'); prog.id = 'fProg'; st0.appendChild(prog);
  const cover = el('div', 'fl'); cover.id = 'fCover'; st0.appendChild(cover);
  cover.innerHTML = `<div class="in"><div class="badges"><span class="badge y">10+</span><span class="badge">4 Bauschritte</span></div><h1>${TL.title}</h1><p>${TL.subtitle}</p><div class="done">Fertig!</div></div>`;
  const done = cover.querySelector('.done');
  const fade = el('div', 'fl'); fade.id = 'fFade'; st0.appendChild(fade);
  const segs = TL.scenes.map(s => { const d = el('div', 's', `<em>${s.label}</em><div class="b"><i></i></div>`); d.style.setProperty('--w', (s.end - s.start).toFixed(2)); prog.appendChild(d); return d; });

  const SHOTS = {
    overview: { t: [1, -12, 0], r: 98, th: .35, ph: 1.35, shift: 0 },
    cover: { t: [1, -12, 0], r: 98, th: .35, ph: 1.35, shift: -15 },
    atmung: { t: [0, -20, 0], r: 60, th: .3, ph: 1.36, shift: 9 },
    kehlkopfSeite: { t: [0, -8.4, 0], r: 17, th: .45, ph: 1.15, shift: 2.6 },
    kehlkopf: { t: [0, -8.4, 0], r: 11, th: .35, ph: .38, shift: 1.7 },
    ansatz: { t: [3, -1, 0], r: 34, th: .3, ph: 1.35, shift: 5.5 },
    mund: { t: [4.5, 2, 0], r: 20, th: .32, ph: 1.3, shift: 3.2 },
    mundNase: { t: [4.5, 3.2, 0], r: 22, th: .3, ph: 1.3, shift: 3.4 }
  };
  function shot(name, instant) {
    const s = SHOTS[name]; if (!s) return; const rt = [Math.cos(s.th), 0, -Math.sin(s.th)];
    API.camGoal({ t: [s.t[0] + rt[0] * s.shift, s.t[1], s.t[2] + rt[2] * s.shift], r: s.r, th: s.th, ph: s.ph }, instant);
  }
  const st = { i: 0, headT: -9, intro: false, introT: -9, outro: false, partT: [], shown: -1 };
  const DUR = { platte: 1.4, wand: 1.8, atmung: 3.2, kehlkopf: 2.2, ansatz: 2.4, artik: 2.4 };

  const H = {
    reset(v, t) {
      API.setStep(v.step, true); API.setMode('speech'); API.setVowel(v.vowel || 'a'); API.setCons(v.cons || null);
      const F = API.film; F.hold = !!v.hold; F.voice = v.vforce ?? null; F.abd = v.glottis ?? null; F.orbit = v.orbit || 0;
      shot(v.intro ? 'cover' : v.shot, true);
      if (v.unbuilt) API.buildGroups(v.unbuilt, 1e12);
      if (v.build) { let t0 = MS(t + .5) / 1000; v.build.forEach(g => { API.buildGroups([g], t0, DUR[g] || 2); t0 += (DUR[g] || 2) + .2; }); }
      step.querySelector('.n').textContent = v.num || ''; step.querySelector('small').textContent = v.role || ''; step.querySelector('b').textContent = v.label || '';
      parts.querySelector('ul').innerHTML = (v.parts || []).map(p => `<li><span class="q">${p[0]}</span><span class="sw" style="background:${p[1]}"></span>${p[2]}</li>`).join('');
      st.partT = []; st.shown = -1; st.headT = t; st.intro = !!v.intro; st.introT = t; st.outro = !!v.outro; st.hasParts = !!(v.parts && v.parts.length);
    },
    shot(v) { shot(v, false); },
    part(v, t) { for (let i = st.shown + 1; i <= v; i++) st.partT[i] = t; st.shown = Math.max(st.shown, v); },
    glottis(v) { API.film.abd = v; }, vforce(v) { API.film.voice = v; }, hold(v) { API.film.hold = v; },
    vowel(v) { API.setVowel(v); }, cons(v) { API.setCons(v); }, syl(v) { API.playSyl(v); },
    outro(v, t) { st.outro = true; }
  };
  function applyUntil(t, seeking) {
    const C = TL.cues;
    while (st.i < C.length && C[st.i].t <= t) { const c = C[st.i++]; if (seeking && c.a === 'syl' && t - c.t > .9) continue; H[c.a] && H[c.a](c.v, c.t); }
  }
  function update(t) {
    applyUntil(t, false);
    let f = clamp(1 - t / .8, 0, 1);
    TL.scenes.forEach((s, i) => { if (i) f = Math.max(f, clamp(1 - Math.abs(t - s.start) / .4, 0, 1)); });
    f = Math.max(f, clamp((t - (TL.duration - .6)) / .6, 0, 1));
    fade.style.opacity = f.toFixed(3);
    const hk = st.intro ? 0 : ease((t - st.headT - .3) / .5);
    step.style.opacity = hk; step.style.transform = `translateY(${(1 - hk) * -12}px)`;
    const pk = st.intro || !st.hasParts ? 0 : ease((t - st.headT - .6) / .5);
    parts.style.opacity = pk; parts.style.transform = `translateX(${(1 - pk) * 20}px)`;
    parts.querySelectorAll('li').forEach((li, i) => { const k = i <= st.shown ? ease((t - st.partT[i]) / .4) : 0; li.style.opacity = (.2 + .8 * k).toFixed(3); li.style.transform = `scale(${(.92 + .08 * k).toFixed(3)})`; });
    cover.style.opacity = st.intro ? ease((t - st.introT) / .6) : 0;
    done.style.display = st.outro ? '' : 'none';
    const s = TL.subs.find(x => t >= x.start && t < x.end), span = sub.querySelector('span'), txt = s ? s.text : '';
    if (span.textContent !== txt) span.textContent = txt; span.style.visibility = txt ? 'visible' : 'hidden';
    TL.scenes.forEach((sc, i) => { segs[i].querySelector('i').style.width = (clamp((t - sc.start) / (sc.end - sc.start), 0, 1) * 100).toFixed(2) + '%'; segs[i].classList.toggle('on', t >= sc.start && t < sc.end); });
  }
  window.__film = {
    seek(t) { st.i = 0; applyUntil(t, true); update(t); },
    update,
    render(t) { API.renderAt(MS(t)); }
  };
})();
