import requests
from bs4 import BeautifulSoup
import re
import json

# Revisar URLs sin el parámetro fgr_gallery
urls = [
    'http://localhost/2026b/2026/06/07/124-anos-de-historia-y-mistica-inbana/',
    'http://localhost/2026b/2026/04/07/uniforme-escolar-inba/',
    'http://localhost/2026b/2026/05/19/el-recreo-se-lleno-de-musica/',
]

for url in urls:
    print(f'\n{"="*70}')
    print(f'ANALIZANDO: {url}')
    print("="*70)
    
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Título
        title = soup.find('h1')
        if title:
            title_text = title.get_text(strip=True)
            print(f'Título: {title_text}')
        
        # Buscar el shortcode de galería en el HTML crudo
        html = r.text
        
        # Buscar [gallery ...] shortcodes
        gallery_matches = re.findall(r'\[gallery[^\]]*\]', html)
        print(f'\nShortcodes encontrados: {len(gallery_matches)}')
        for match in gallery_matches[:3]:
            print(f'  {match}')
        
        # Extraer IDs de attachment
        attachment_ids = re.findall(r'ids="([^"]*)"', html)
        if attachment_ids:
            print(f'\nIDs de attachments: {attachment_ids}')
        
        # Buscar imágenes
        print(f'\nIMÁGENES EN EL ARTÍCULO:')
        imgs = []
        for img in soup.find_all('img', src=True):
            src = img.get('src')
            if src and '/wp-content/uploads' in src:
                imgs.append(src)
        
        # Eliminar duplicados
        unique_imgs = []
        seen = set()
        for img in imgs:
            if img not in seen:
                seen.add(img)
                unique_imgs.append(img)
        
        for i, img in enumerate(unique_imgs[:20], 1):
            filename = img.split('/')[-1]
            print(f'  {i}. {filename}')
        
        if len(unique_imgs) > 20:
            print(f'  ... y {len(unique_imgs) - 20} más')
            
    except Exception as e:
        print(f'Error: {e}')

print('\n\nScript completado.')
