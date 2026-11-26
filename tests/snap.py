import asyncio, sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 960, 'height': 540}); errs=[]
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file://' + str(__import__('pathlib').Path(__file__).resolve().parent.parent / 'index.html') + ''); await pg.wait_for_timeout(900)
        await pg.screenshot(path='shots/s_menu.png')
        await pg.mouse.click(150,375); await pg.wait_for_timeout(200); await pg.mouse.click(144,280); await pg.wait_for_timeout(200)
        await pg.mouse.click(420,200); await pg.wait_for_timeout(200)
        for name,(x,y) in {'river':(150,246),'pedada':(430,186),'estuary':(596,446),'mangrove':(384,392)}.items():
            await pg.evaluate("__G.screen='region'"); await pg.wait_for_timeout(150)
            await pg.mouse.click(x,y); await pg.mouse.click(x,y); await pg.wait_for_timeout(1800)
            await pg.mouse.move(480,500); await pg.wait_for_timeout(300)
            await pg.screenshot(path=f'shots/s_{name}.png')
            await pg.evaluate('__SS().t=34'); await pg.wait_for_timeout(1200)
            await pg.screenshot(path=f'shots/s_{name}_ev.png')
            await pg.evaluate('__SS().t=39.95'); await pg.wait_for_timeout(300)
        print('ERR',errs); await b.close()
asyncio.run(main())
