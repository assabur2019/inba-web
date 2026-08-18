import requests
from bs4 import BeautifulSoup
import json

print('=== EXPLORANDO GALERÍAS EN SITIO VIEJO ===\n')

r = requests.get('http://localhost/2026b/', timeout=10)
soup = BeautifulSoup(r.text, 'html.parser')

print('TODAS LAS PÁGINAS CON "galeria":')
encontrados = set()
for link in soup.find_all('a', href=True):
    href = link.get('href', '')
    text = link.get_text(strip=True)
    if 'galeria' in href.lower():
        if href not in encontrados:
            encontrados.add(href)
            print(f'  {text or "[sin texto]"}: {href}')

print(f'\nTotal de galerías encontradas: {len(encontrados)}')

# Ahora revisar cada galería
print('\n\n=== CONTENIDO DE CADA GALERÍA ===\n')

for galeria_url in list(encontrados)[:5]:  # Limitar a las primeras 5
    print(f'\n{"-"*60}')
    print(f'URL: {galeria_url}')
    print('-'*60)
    try:
        r2 = requests.get(galeria_url, timeout=10)
        soup2 = BeautifulSoup(r2.text, 'html.parser')
        
        # Título
        title = soup2.find('h1')
        if title:
            print(f'Título: {title.get_text(strip=True)}')
        
        # Descripción - primeros párrafos
        parrafos = soup2.find_all('p')
        for p in parrafos[:2]:
            t = p.get_text(strip=True)
            if t and len(t) > 20:
                print(f'Desc: {t[:150]}...')
        
        # Imágenes
        imgs = []
        for img in soup2.find_all('img', src=True):
            src = img.get('src', '')
            if src and ('/wp-content/uploads' in src or '/uploads/' in src):
                imgs.append(src)
        
        # Únicos
        unique_imgs = list(set(imgs))
        print(f'Imágenes: {len(unique_imgs)}')
        for i, img in enumerate(unique_imgs[:8], 1):
            # Mostrar solo el nombre del archivo
            filename = img.split('/')[-1]
            print(f'  {i}. .../{filename}')
            
    except Exception as e:
        print(f'Error: {e}')

print('\n\nScript completado.')
