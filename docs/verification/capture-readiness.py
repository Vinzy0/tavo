from pathlib import Path
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch(channel='chrome',headless=True)
 page=b.new_page(viewport={'width':1440,'height':1000})
 for name,url in [('tavo','https://tavo-web-6d8p.onrender.com'),('sapture','https://sapture.pages.dev/')]:
  folder=Path('C:/Users/vinzp/Documents/readiness-work')/name/'docs/screenshots';folder.mkdir(parents=True,exist_ok=True)
  try:
   page.goto(url,wait_until='domcontentloaded',timeout=120000)
   page.wait_for_timeout(60000 if name=='tavo' else 5000)
   page.screenshot(path=str(folder/'public.png'),full_page=True)
   print(name,page.url,page.title())
   if name=='tavo': page.goto(url+'/login',wait_until='networkidle',timeout=120000)
   else: page.goto(url+'/sign-in',wait_until='networkidle',timeout=60000)
   page.screenshot(path=str(folder/'login.png'),full_page=True)
   print(name,'second',page.url)
  except Exception as e: print(name,type(e).__name__,str(e)[:180])
 b.close()
