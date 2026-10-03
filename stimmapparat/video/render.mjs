// Rendert Einzelbilder des Erklärvideos aus dem 3D-Modell (Playwright + Chromium; jedes Bild wird mit fester Zeit berechnet).
// Aufruf: node render.mjs [--page index.html] [--film film] [--out out] [--from 0] [--to N] [--fps 25] [--three PFAD] [--fonts PFAD] [--frames out/frames] [--at 12.5,80]
import { createRequire } from 'module';
import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath, pathToFileURL } from 'url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(path.join(execSync('npm root -g').toString().trim(), 'playwright')); }

const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const FPS = +arg('fps', 25);
const OUT = path.resolve(arg('out', path.join(HERE, 'out')));
const TL = JSON.parse(fs.readFileSync(path.join(OUT, 'timeline.json'), 'utf8'));
const FRAMES = path.resolve(arg('frames', path.join(OUT, 'frames')));
const total = Math.ceil(TL.duration * FPS);
const from = +arg('from', 0), to = Math.min(+arg('to', total), total);
const at = arg('at', null);
const THREE = arg('three', null), FONTS = arg('fonts', null);
const PAGE = arg('page', 'index.html'), FILM = arg('film', 'film');
fs.mkdirSync(FRAMES, { recursive: true });

const browser = await pw.chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--autoplay-policy=no-user-gesture-required'] });
const ctx = await browser.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1.5 });
const page = await ctx.newPage();
const cdp = await ctx.newCDPSession(page);
await cdp.send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 720, deviceScaleFactor: 1.5, mobile: false });
page.on('pageerror', e => console.error('Seitenfehler:', e.message));
if (THREE) await page.route('**/three.min.js', r => r.fulfill({ path: THREE, contentType: 'application/javascript' }));
if (FONTS) { await page.route('**/fonts.googleapis.com/**', r => r.abort()); await page.route('**/fonts.gstatic.com/**', r => r.abort()); }
await page.goto(pathToFileURL(path.join(HERE, '..', PAGE)).href);
await page.waitForTimeout(500);
console.log('devicePixelRatio', await page.evaluate(() => devicePixelRatio));
if (FONTS) {
  for (const f of ['bricolage-grotesque/500.css', 'bricolage-grotesque/700.css', 'atkinson-hyperlegible/400.css', 'atkinson-hyperlegible/700.css', 'jetbrains-mono/400.css', 'jetbrains-mono/500.css', 'noto-sans/500.css', 'archivo/400.css', 'archivo/600.css', 'archivo/800.css', 'archivo/900.css', 'ibm-plex-mono/500.css'])
    if (fs.existsSync(path.join(FONTS, f))) await page.addStyleTag({ url: pathToFileURL(path.join(FONTS, f)).href });
}
await page.addStyleTag({ path: path.join(HERE, FILM + '.css') });
await page.evaluate(tl => { window.__TIMELINE = tl; }, TL);
await page.addScriptTag({ path: path.join(HERE, FILM + '.js') });
await page.evaluate(() => document.fonts.ready);

async function frame(t, file) {
  await page.evaluate(x => { window.__film.update(x); if (window.__film.render) window.__film.render(x); else window.Stimmapparat.renderAt(1e8 + x * 1000); }, t);
  if (file) { const r = await cdp.send('Page.captureScreenshot', { format: 'jpeg', quality: 92, }); fs.writeFileSync(file, Buffer.from(r.data, 'base64')); }
}

if (at) {
  // Einzelbilder zur Kontrolle
  for (const ts of at.split(',').map(Number)) {
    await page.evaluate(x => window.__film.seek(x), Math.max(0, ts - 2));
    for (let t = Math.max(0, ts - 2); t < ts; t += 1 / FPS) await frame(t, null);
    await frame(ts, path.join(FRAMES, `check_${ts.toFixed(1)}.jpg`));
  }
} else {
  const pre = Math.max(0, from / FPS - 2);
  await page.evaluate(x => window.__film.seek(x), pre);
  for (let t = pre; t < from / FPS - 1e-6; t += 1 / FPS) await frame(t, null);
  const t0 = Date.now();
  for (let f = from; f < to; f++) {
    await frame(f / FPS, path.join(FRAMES, String(f).padStart(5, '0') + '.jpg'));
    if ((f - from) % 250 === 249) console.log(`Bilder ${from}–${to}: ${f + 1 - from} fertig, ${((Date.now() - t0) / (f + 1 - from)).toFixed(0)} ms/Bild`);
  }
}
await browser.close();
