/* Regie für das Erklärvideo: setzt Zeitleisten-Anweisungen auf das 3D-Modell um.
   Wird vom Renderer in index.html eingefügt; window.__TIMELINE muss vorher gesetzt sein.
   Alle Einblendungen werden aus der Videozeit t berechnet, damit jedes Bild reproduzierbar ist. */
(() => {
  'use strict';
  const API = window.Stimmapparat, TL = window.__TIMELINE;
  const $ = s => document.querySelector(s);
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const ease = x => { x = clamp(x, 0, 1); return x * x * (3 - 2 * x); };
  const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };

  document.documentElement.dataset.theme = 'dark';
  document.body.classList.add('film');
  const stage = el('div'); stage.id = 'filmStage'; document.body.appendChild(stage);
  stage.appendChild($('#view'));
  stage.appendChild(el('div', 'f-layer f-vignette'));

  const head = el('div', 'f-layer'); head.id = 'fHead'; head.innerHTML = '<div class="eb"><b></b><span></span></div><h1></h1>'; stage.appendChild(head);
  const card = el('div', 'f-layer'); card.id = 'fCard'; card.innerHTML = '<h3></h3><div class="slot"></div><ul></ul>'; stage.appendChild(card);
  const sub = el('div', 'f-layer'); sub.id = 'fSub'; sub.innerHTML = '<span></span>'; stage.appendChild(sub);
  const prog = el('div', 'f-layer'); prog.id = 'fProg'; stage.appendChild(prog);
  const intro = el('div', 'f-layer'); intro.id = 'fIntro'; stage.appendChild(intro);
  const fade = el('div', 'f-layer'); fade.id = 'fFade'; stage.appendChild(fade);

  const COL = { atmung: '#78B4F5', kehlkopf: '#F07CA2', schwingung: '#F07CA2', resonanz: '#EBB052', artikulation: '#57CDA7' };
  const CHAIN = [
    ['Atmung', 'liefert die Energie', '#78B4F5'],
    ['Stimmlippen', 'erzeugen den Ton', '#F07CA2'],
    ['Ansatzrohr', 'formt den Klang', '#EBB052'],
    ['Artikulation', 'formt die Laute', '#57CDA7']
  ];
  intro.innerHTML = `<div class="in"><div class="kick">Erklärvideo · Stimmphysiologie</div><h1>${TL.title}</h1><p>${TL.subtitle}</p>
    <ol>${CHAIN.map((c, i) => `<li style="--sc:${c[2]}"><b>${i + 1}</b><span><strong>${c[0]}</strong><small>${c[1]}</small></span></li>`).join('')}</ol>
    <div class="sum">Zusammen ergibt das: <span style="color:#F07CA2">Stimme und Sprache</span>.</div></div>`;
  const chainLis = [...intro.querySelectorAll('li')], chainSum = intro.querySelector('.sum'), chainOl = intro.querySelector('ol');

  /* Fortschrittsleiste */
  const segs = TL.scenes.map(s => {
    const d = el('div', 'fseg'); d.style.setProperty('--w', (s.end - s.start).toFixed(2));
    d.innerHTML = `<em>${s.label}</em><div class="bar"><i></i></div>`; d.style.setProperty('--sc', COL[s.chapter] || '#D8E4E2'); prog.appendChild(d); return d;
  });

  /* Diagramme aus dem Seitenpanel */
  const FIG = {
    breath: { title: 'Lungenvolumen und Druck unter den Stimmlippen', nodes: () => [$('#cvBreath').closest('figure')] },
    glottis: { title: 'Blick von oben · Luftstrom durch die Glottis', nodes: () => [$('#cvGlottis').closest('figure')] },
    spec: { title: 'Quelle × Filter = Klang', nodes: () => [$('#cvSpec').closest('figure')], legend: '<span>━</span> Filterkurve des Ansatzrohrs · grau: Obertöne der Quelle · <span>●</span> Ergebnis am Mund' },
    vowel: { title: 'Vokalviereck: F1 und F2', nodes: () => [$('#cvVowel').closest('figure')] },
    cons: { title: 'Konsonanten: Stelle und Art', nodes: () => [$('.chart-wrap'), $('#selBox')] }
  };
  const home = new Map();
  Object.values(FIG).forEach(f => f.nodes().forEach(n => home.set(n, { parent: n.parentNode, next: n.nextSibling })));

  const st = { i: 0, card: null, cardT: -9, bullets: [], shown: -1, bulletT: [], color: '#D8E4E2', intro: false, introT: -9, chain: -1, chainT: [], outro: false, outroT: -9, press: null, headT: -9 };

  const SHOTS = {
    intro: { c: [0, -13, 0], r: 76, th: .45, ph: 1.42, shift: -12 },
    overview: { c: [0, -13, 0], r: 74, th: .5, ph: 1.42, shift: 10 },
    torso: { c: [-1, -21, 0], r: 50, th: .6, ph: 1.38, shift: 8.5 },
    neck: { c: [0, -11, 0], r: 24, th: .75, ph: 1.42, shift: 4.5 },
    larynxSide: { c: [.2, -7.8, 0], r: 10.5, th: .95, ph: 1.3, shift: 2 },
    larynxTop: { c: [.1, -8, 0], r: 9.5, th: -1.4, ph: .26, shift: 1.7 },
    larynxClose: { c: [.1, -8, 0], r: 6.8, th: -1.45, ph: .2, shift: 1.2 },
    tract: { c: [2.8, -1.8, 0], r: 36, th: .3, ph: 1.45, shift: 6.5 },
    tractClose: { c: [3.6, .6, 0], r: 22, th: .35, ph: 1.4, shift: 4.2 },
    mouth: { c: [5, 1.8, 0], r: 19, th: .55, ph: 1.28, shift: 3.8 },
    mouthNose: { c: [4.6, 3, 0], r: 20, th: .45, ph: 1.3, shift: 3.8 }
  };
  function shot(name, instant) {
    const s = SHOTS[name]; if (!s) return;
    API.film.particles = !/^larynx(Top|Close)/.test(name);
    const rt = [Math.cos(s.th), 0, -Math.sin(s.th)];
    API.camGoal({ t: [s.c[0] + rt[0] * s.shift, s.c[1], s.c[2] + rt[2] * s.shift], r: s.r, th: s.th, ph: s.ph }, instant);
  }
  function setCard(key, t) {
    const slot = card.querySelector('.slot');
    [...slot.children].forEach(n => { const h = home.get(n); if (h) h.parent.insertBefore(n, h.next); });
    slot.innerHTML = '';
    st.card = key; st.cardT = t;
    if (!key) return;
    const f = FIG[key]; card.querySelector('h3').textContent = f.title;
    f.nodes().forEach(n => slot.appendChild(n));
    if (f.legend) slot.appendChild(el('div', 'legend', f.legend));
  }
  function setBullets(list) {
    st.bullets = list || []; st.shown = -1; st.bulletT = [];
    card.querySelector('ul').innerHTML = st.bullets.map(b => `<li>${b}</li>`).join('');
  }

  const H = {
    reset(v, t) {
      API.setStage(v.stage, true);
      API.setMode(v.mode || 'speech'); API.setVoice(v.voice || 'f'); API.setVowel(v.vowel || 'a'); API.setCons(v.cons || null);
      const F = API.film; F.hi = null; F.abd = v.glottis ?? null; F.voice = v.vforce ?? null; F.hold = !!v.hold; F.orbit = v.orbit || 0;
      API.setLabels(v.labels !== false); API.setWave(v.wave ?? 0); API.setSlow(v.slow || 90); API.setPress(7); st.press = null;
      shot(v.intro ? 'intro' : v.shot, true);
      st.color = v.color || '#D8E4E2'; stage.style.setProperty('--fc', st.color);
      head.querySelector('.eb b').textContent = v.num || ''; head.querySelector('.eb b').style.display = v.num ? '' : 'none';
      head.querySelector('.eb span').textContent = v.num ? `Kapitel ${v.num} · ${v.role}` : '';
      head.querySelector('h1').textContent = v.intro ? '' : v.label; st.headT = t;
      setCard(v.card || null, t); setBullets(v.bullets);
      st.intro = !!v.intro; st.introT = t; st.chain = -1; st.chainT = []; st.outro = false;
    },
    shot(v) { shot(v, false); },
    hi(v) { API.film.hi = v; },
    mode(v) { API.setMode(v); },
    voice(v) { API.setVoice(v); },
    vowel(v) { API.setVowel(v); },
    cons(v) { API.setCons(v); },
    syl(v) { const c = API.CONS.find(x => x.ipa === v); if (c) API.playSyllable(c); },
    glottis(v) { API.film.abd = v; },
    vforce(v) { API.film.voice = v; },
    wave(v) { API.setWave(v); },
    card(v, t) { setCard(v, t); },
    bullet(v, t) { for (let i = st.shown + 1; i <= v; i++) st.bulletT[i] = t; st.shown = Math.max(st.shown, v); },
    pressTo(v, t) { st.press = { from: API.S.press, to: v[0], t0: t, d: v[1] }; },
    chain(v, t) { for (let i = st.chain + 1; i <= v; i++) st.chainT[i] = t; st.chain = Math.max(st.chain, v); },
    outro(v, t) { st.outro = true; st.outroT = t; }
  };

  function applyUntil(t, seeking) {
    const C = TL.cues;
    while (st.i < C.length && C[st.i].t <= t) {
      const c = C[st.i++];
      if (seeking && c.a === 'syl' && t - c.t > .9) continue;
      H[c.a] && H[c.a](c.v, c.t);
    }
  }

  function update(t) {
    applyUntil(t, false);
    if (st.press) { const k = ease((t - st.press.t0) / st.press.d); API.setPress(Math.round((st.press.from + (st.press.to - st.press.from) * k) * 2) / 2); if (k >= 1) st.press = null; }

    /* Überblendung zwischen Szenen */
    let f = clamp(1 - t / .8, 0, 1);
    TL.scenes.forEach((s, i) => { if (i) f = Math.max(f, clamp(1 - Math.abs(t - s.start) / .45, 0, 1)); });
    f = Math.max(f, clamp((t - (TL.duration - .6)) / .6, 0, 1));
    fade.style.opacity = f.toFixed(3);

    /* Kopf, Karte, Stichpunkte */
    const hk = ease((t - st.headT - .3) / .5);
    head.style.opacity = st.intro ? 0 : hk; head.style.transform = `translateY(${(1 - hk) * 10}px)`;
    const ck = st.card && !st.intro ? ease((t - st.cardT - .15) / .45) : 0;
    card.style.opacity = ck; card.style.transform = `translateX(${(1 - ck) * 24}px)`; card.hidden = !st.card || st.intro;
    card.querySelectorAll('li').forEach((li, i) => {
      const k = i <= st.shown ? ease((t - st.bulletT[i]) / .45) : 0;
      li.style.opacity = (.18 + .82 * k).toFixed(3); li.style.transform = `translateX(${(1 - k) * 8}px)`;
    });

    /* Titelkarte */
    intro.style.opacity = st.intro ? ease((t - st.introT) / .6) : 0;
    chainOl.style.opacity = st.chain >= 0 ? ease((t - st.chainT[0]) / .5) : 0;
    chainLis.forEach((li, i) => {
      const k = st.chain >= i + 1 ? ease((t - st.chainT[i + 1]) / .4) : 0;
      li.classList.toggle('lit', k > .5); li.style.opacity = (.35 + .65 * k).toFixed(3);
    });
    chainSum.style.opacity = st.chain >= 5 ? ease((t - st.chainT[5]) / .6) : 0;

    /* Untertitel */
    const s = TL.subs.find(x => t >= x.start && t < x.end);
    const span = sub.querySelector('span'); const txt = s ? s.text : '';
    if (span.textContent !== txt) span.textContent = txt;
    span.style.visibility = txt ? 'visible' : 'hidden';
    sub.classList.toggle('withCard', !!st.card && !st.intro);

    /* Fortschritt */
    TL.scenes.forEach((sc, i) => {
      const k = clamp((t - sc.start) / (sc.end - sc.start), 0, 1);
      segs[i].querySelector('i').style.width = (k * 100).toFixed(2) + '%';
      segs[i].classList.toggle('on', t >= sc.start && t < sc.end);
    });
    prog.style.opacity = st.intro ? .5 : 1;
  }

  window.__film = {
    seek(t) { st.i = 0; applyUntil(t, true); update(t); },
    update
  };
})();
