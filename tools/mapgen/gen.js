// Rasterize Natural Earth (public domain) country polygons to a 320x180 grid around Indonesia.
const topo = require('topojson-client');
const world = require('world-atlas/countries-10m.json');
const fc = topo.feature(world, world.objects.countries);
const GW = 320, GH = 180, LON0 = 93.5, LAT0 = 11, D = 0.15;
const grid = new Uint8Array(GW * GH);
const REG = { sumatra: 2, jawa: 3, kalimantan: 4, sulawesi: 5, nusa: 6, maluku: 7, papua: 8 };
function inRing(x, y, ring) { let c = false; for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) { const [xi, yi] = ring[i], [xj, yj] = ring[j]; if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) c = !c; } return c; }
function inPoly(x, y, poly) { if (!inRing(x, y, poly[0])) return false; for (let k = 1; k < poly.length; k++) if (inRing(x, y, poly[k])) return false; return true; }
function regionOf(poly) {
  let sx = 0, sy = 0, n = 0; for (const [x, y] of poly[0]) { sx += x; sy += y; n++; } const c = sx / n, l = sy / n;
  if ((c >= 130 && l > -2.5) || c >= 135 || (c >= 132 && l > -4.2 && l <= -2.5)) return REG.papua;
  if (l < -7.9 && c >= 114.4 && c < 127.5) return REG.nusa;
  if ((c >= 118.8 && c <= 125.3 && l > -6.8 && l < 2.2) || (c >= 119 && c <= 122.5 && l > -7.7 && l < 2.2) || (c >= 124 && c < 127 && l >= 2.2)) return REG.sulawesi;
  if (c >= 125.3) return REG.maluku;
  if (c < 107.3 || (c < 108.4 && l < -2.3 && l > -3.6) || (c < 108.6 && l > 2.5)) return REG.sumatra;
  if (l < -5.3 && c < 116.2) return REG.jawa;
  if (l > -4.9 && c < 119.5) return REG.kalimantan;
  return REG.jawa;
}
for (const f of fc.features) {
  if (!f.geometry) continue;
  const polys = f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates;
  const isIDN = String(f.id) === '360';
  for (const poly of polys) {
    let minx = 1e9, maxx = -1e9, miny = 1e9, maxy = -1e9;
    for (const [x, y] of poly[0]) { minx = Math.min(minx, x); maxx = Math.max(maxx, x); miny = Math.min(miny, y); maxy = Math.max(maxy, y); }
    if (maxx < LON0 || minx > LON0 + GW * D || maxy < LAT0 - GH * D || miny > LAT0) continue;
    const v = isIDN ? regionOf(poly) : 1;
    const cx0 = Math.max(0, Math.floor((minx - LON0) / D)), cx1 = Math.min(GW - 1, Math.ceil((maxx - LON0) / D));
    const cy0 = Math.max(0, Math.floor((LAT0 - maxy) / D)), cy1 = Math.min(GH - 1, Math.ceil((LAT0 - miny) / D));
    let hit = 0;
    for (let cy = cy0; cy <= cy1; cy++) for (let cx = cx0; cx <= cx1; cx++) {
      const lon = LON0 + (cx + .5) * D, lat = LAT0 - (cy + .5) * D;
      if (inPoly(lon, lat, poly)) { if (v > 1 || grid[cy * GW + cx] === 0) grid[cy * GW + cx] = v; hit++; }
    }
    if (!hit && isIDN && (maxx - minx) > 0.04) { // keep small islands visible as one pixel
      let sx = 0, sy = 0, n = 0; for (const [x, y] of poly[0]) { sx += x; sy += y; n++; }
      const cx = Math.floor((sx / n - LON0) / D), cy = Math.floor((LAT0 - sy / n) / D);
      if (cx >= 0 && cx < GW && cy >= 0 && cy < GH && grid[cy * GW + cx] === 0) grid[cy * GW + cx] = v;
    }
  }
}
// RLE
let out = ''; let prev = grid[0], cnt = 1;
for (let i = 1; i <= grid.length; i++) { const v = i < grid.length ? grid[i] : -1; if (v === prev && cnt < 1295) cnt++; else { out += prev + cnt.toString(36).padStart(2, '0'); prev = v; cnt = 1; } }
const cent = {};
for (const k in REG) { let sx = 0, sy = 0, n = 0; for (let i = 0; i < grid.length; i++) if (grid[i] === REG[k]) { sx += i % GW; sy += Math.floor(i / GW); n++; } cent[k] = { x: +(sx / n).toFixed(1), y: +(sy / n).toFixed(1), n }; }
require('fs').writeFileSync('map.json', JSON.stringify({ rle: out, cent }));
console.log('rle length', out.length, JSON.stringify(cent));
// preview
let txt = ''; for (let y = 0; y < GH; y += 3) { for (let x = 0; x < GW; x += 2) txt += ' .SJKCNMP'[grid[y * GW + x]]; txt += '\n'; }
require('fs').writeFileSync('preview.txt', txt);
