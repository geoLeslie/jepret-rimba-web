import asyncio
from playwright.async_api import async_playwright

URL = 'file://' + str(__import__('pathlib').Path(__file__).resolve().parent.parent / 'index.html') + ''
OUT = str(__import__('pathlib').Path(__file__).resolve().parent / 'shots')

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 960, 'height': 540})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        await pg.mouse.click(150, 375); await pg.wait_for_timeout(200)
        await pg.mouse.click(144, 280); await pg.wait_for_timeout(200)
        await pg.screenshot(path=f'{OUT}/20_map.png')
        await pg.mouse.click(420, 200); await pg.wait_for_timeout(200)
        await pg.mouse.click(384, 392); await pg.wait_for_timeout(200)
        await pg.screenshot(path=f'{OUT}/21_region.png')
        await pg.evaluate('__G.day = 4')
        await pg.mouse.click(150, 246); await pg.mouse.click(150, 246); await pg.wait_for_timeout(400)
        tgt = await pg.evaluate('__SS().tgtAt')
        await pg.evaluate(f'__SS().t = {max(0, tgt - 0.1)}')
        shot = 0
        for i in range(160):
            info = await pg.evaluate("(()=>{const s=__SS(); const b=s.ents.find(e=>e.kind==='target'); if(!b) return null; const c=b.c(); return {x:c.x,y:c.y,m:b.moment(),ph:b.phase,aim:b.aimT}})()")
            if info:
                await pg.mouse.move(info['x'], info['y'])
                if info['m'] and shot < 2:
                    await pg.mouse.click(info['x'], info['y']); shot += 1
                    await pg.wait_for_timeout(60)
                    await pg.screenshot(path=f'{OUT}/22_target_{shot}.png')
                    await pg.wait_for_timeout(500)
            elif shot: break
            await pg.wait_for_timeout(60)
        print('targetFound', await pg.evaluate('__G.targetFound'), await pg.evaluate('__G.bestTarget && __G.bestTarget.q'))
        # shoot something else for variety
        await pg.evaluate('__SS().t = 39.9'); await pg.wait_for_timeout(400)
        await pg.screenshot(path=f'{OUT}/23_summary.png')
        await pg.mouse.click(630, 511); await pg.wait_for_timeout(300)
        print('screen', await pg.evaluate('__G.screen'))
        await pg.screenshot(path=f'{OUT}/24_archive.png')
        print('ERRORS', errs)
        await b.close()

asyncio.run(main())
