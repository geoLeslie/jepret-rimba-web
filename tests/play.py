import sys, asyncio
from playwright.async_api import async_playwright

URL = 'file://' + str(__import__('pathlib').Path(__file__).resolve().parent.parent / 'index.html') + ''
OUT = str(__import__('pathlib').Path(__file__).resolve().parent / 'shots')

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
        pg = await b.new_page(viewport={'width': 960, 'height': 540})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        await pg.goto(URL)
        await pg.wait_for_timeout(600)
        await pg.screenshot(path=f'{OUT}/01_menu.png')
        # Cara main
        await pg.mouse.click(350, 375); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'{OUT}/02_howto.png')
        await pg.mouse.click(685, 440); await pg.wait_for_timeout(200)
        await pg.mouse.click(150, 375); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'{OUT}/03_missions.png')
        await pg.mouse.click(144, 280); await pg.wait_for_timeout(300)
        # wrong region first: Papua
        await pg.mouse.move(850, 260); await pg.wait_for_timeout(200)
        await pg.screenshot(path=f'{OUT}/04_map.png')
        await pg.mouse.click(850, 260); await pg.wait_for_timeout(300)
        print('region', await pg.evaluate('__G.region'), await pg.evaluate('__G.regionCorrect'))
        await pg.mouse.move(430, 186); await pg.wait_for_timeout(200)
        await pg.screenshot(path=f'{OUT}/05_region.png')
        await pg.mouse.click(430, 186); await pg.mouse.click(430, 186); await pg.wait_for_timeout(1500)
        print('screen', await pg.evaluate('__G.screen'))
        await pg.mouse.move(480, 300)
        await pg.screenshot(path=f'{OUT}/06_session_pedada.png')
        for i in range(3):
            await pg.mouse.click(300 + i * 150, 230); await pg.wait_for_timeout(400)
        await pg.screenshot(path=f'{OUT}/07_session_shots.png')
        await pg.evaluate('__SS().t = 31')
        await pg.wait_for_timeout(1500)
        await pg.screenshot(path=f'{OUT}/08_event.png')
        await pg.evaluate('__SS().t = 39.9')
        await pg.wait_for_timeout(600)
        print('screen', await pg.evaluate('__G.screen'), 'offer', await pg.evaluate('__G.offerSwitch'))
        await pg.screenshot(path=f'{OUT}/09_summary_wrong.png')
        # switch region
        await pg.mouse.click(645, 511); await pg.wait_for_timeout(300)
        print('after switch', await pg.evaluate('__G.screen'), await pg.evaluate('__G.day'))
        await pg.mouse.click(420, 200); await pg.wait_for_timeout(300)
        print('region', await pg.evaluate('__G.region'), await pg.evaluate('__G.regionCorrect'))
        # Force target appearance at river: set appearedEver false and day 4 guarantee
        await pg.evaluate('__G.day = 4')
        await pg.mouse.click(150, 246); await pg.mouse.click(150, 246); await pg.wait_for_timeout(500)
        tgt = await pg.evaluate('__SS().tgtAt')
        print('tgtAt', tgt)
        await pg.evaluate(f'__SS().t = {max(0, tgt - 0.1)}')
        # follow bekantan and shoot during leap
        shot = False
        for i in range(120):
            info = await pg.evaluate("(()=>{const s=__SS(); if(!s) return null; const b=s.ents.find(e=>e.kind==='target'); if(!b) return {none:true, t:s.t}; const c=b.c(); return {x:c.x,y:c.y,m:b.moment(),ph:b.phase}})()")
            if info and not info.get('none'):
                await pg.mouse.move(info['x'], info['y'])
                if info['m'] and not shot and info['ph'] in ('leap', 'eat1', 'eat2'):
                    await pg.mouse.click(info['x'], info['y']); shot = True
                    await pg.wait_for_timeout(120)
                    await pg.screenshot(path=f'{OUT}/10_target_shot.png')
            await pg.wait_for_timeout(80)
            if shot and i > 5: break
        await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'{OUT}/11_after_target.png')
        print('targetFound', await pg.evaluate('__G.targetFound'), await pg.evaluate('__G.bestTarget && __G.bestTarget.q'))
        await pg.evaluate('__SS().t = 39.9'); await pg.wait_for_timeout(500)
        await pg.screenshot(path=f'{OUT}/12_summary.png')
        await pg.mouse.click(530, 511); await pg.wait_for_timeout(400)
        print('screen', await pg.evaluate('__G.screen'))
        await pg.screenshot(path=f'{OUT}/13_archive.png')
        # mangrove fog scene sample
        await pg.evaluate("__G.screen='region'")
        await pg.wait_for_timeout(200)
        await pg.mouse.click(384, 392); await pg.mouse.click(384, 392); await pg.wait_for_timeout(1200)
        await pg.mouse.move(480, 280)
        await pg.screenshot(path=f'{OUT}/14_mangrove.png')
        await pg.evaluate('__SS().t = 39.9'); await pg.wait_for_timeout(400)
        await pg.evaluate("__G.screen='region'")
        await pg.mouse.click(596, 446); await pg.mouse.click(596, 446); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=f'{OUT}/15_estuary.png')
        print('ERRORS', errs)
        await b.close()

asyncio.run(main())
