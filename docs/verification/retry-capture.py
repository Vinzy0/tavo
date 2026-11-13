from pathlib import Path
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch(channel='chrome',headless=True);page=b.new_page(viewport={'width':1440,'height':1000});log=[]
 page.on('response',lambda r: log.append(f'{r.status} {r.url.split("?")[0]}'))
 page.goto('https://sapture.pages.dev/sign-in',wait_until='networkidle');page.screenshot(path='../sapture/docs/screenshots/login.png',full_page=True);print('sapture',page.locator('body').inner_text()[:350]);Path('../sapture/docs/screenshots/network.txt').write_text('\n'.join(log),encoding='utf-8')
 for path,name in [('/','public'),('/login','login')]:
  page.goto('https://tavo-web-6d8p.onrender.com'+path,wait_until='networkidle',timeout=120000);page.screenshot(path=f'docs/screenshots/{name}.png',full_page=True);print('tavo',name,page.locator('body').inner_text()[:350])
 b.close()
