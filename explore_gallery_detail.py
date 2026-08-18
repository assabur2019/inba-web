import requests
from bs4 import BeautifulSoup

# Revisar una noticia con galería
url = 'http://localhost/2026b/2026/06/07/124-anos-de-historia-y-mistica-inbana/?fgr_gallery=1'
print('ANALIZANDO NOTICIA CON GALERÍA:')
print(f'URL: {url}\n')

r = requests.get(url, timeout=10)
soup = BeautifulSoup(r.text, 'html.parser')

# Título
title = soup.find('h1')
if title:
    print(f'Título: {title.get_text(strip=True)}\n')

# Buscar todas las imágenes
print('IMÁGENES EN LA NOTICIA:')
imgs = []
for img in soup.find_all('img', src=True):
    src = img.get('src')
    alt = img.get('alt', '')
    if src and '/wp-content/uploads' in src:
        imgs.append({'src': src, 'alt': alt})

for i, img in enumerate(imgs[:30], 1):
    filename = img['src'].split('/')[-1]
    alt_text = img['alt'][:50] if img['alt'] else '[sin alt]'
    print(f'{i}. {filename}')
    print(f'   Alt: {alt_text}')

print(f'\nTotal de imágenes: {len(imgs)}')

# Buscar también galerías de FooGallery
print('\n\n=== BUSCANDO SHORTCODES DE GALERÍA ===')
html = r.text
if 'foogallery' in html.lower():
    print('Encontrado: FooGallery')
if 'gallery' in html:
    print('Encontrado: [gallery] shortcode')
if 'flexslider' in html.lower():
    print('Encontrado: FlexSlider')
    
# Buscar divs con clase gallery
print('\n=== DIVS CON CLASE GALLERY ===')
for div in soup.find_all('div', class_='gallery'):
    print(f'Encontrado div.gallery')
    for img in div.find_all('img'):
        src = img.get('src')
        if src:
            filename = src.split('/')[-1]
            print(f'  - {filename}')
