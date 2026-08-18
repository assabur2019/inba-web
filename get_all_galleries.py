import requests
from bs4 import BeautifulSoup
import json

# Primero, obtener lista de todas las noticias del sitio
print("OBTENIENDO LISTA DE NOTICIAS...\n")

r = requests.get('http://localhost/2026b/', timeout=10)
soup = BeautifulSoup(r.text, 'html.parser')

# Encontrar todos los enlaces que parecen ser noticias
noticias_urls = set()
for link in soup.find_all('a', href=True):
    href = link.get('href', '')
    if '/2026/' in href or '/2025/' in href:
        # Filtrar URLs de noticias
        if '/wp-content' not in href and '/wp-json' not in href and '.jpg' not in href and '.png' not in href:
            noticias_urls.add(href)

# Filtrar para obtener solo las que parecen ser posts
posts = [url for url in noticias_urls if any(x in url for x in ['/2026/', '/2025/', 'http'])]

print(f"Noticias encontradas: {len(posts)}\n")

# Analizar cada noticia
galeria_data = {}

for url in sorted(posts)[:15]:  # Limitamos a 15 para no tardar demasiado
    if 'galeria' not in url.lower():  # Excluir páginas de galería
        try:
            r = requests.get(url, timeout=10)
            soup = requests.get(url).text
            if 'No se encontró' not in r.text and r.status_code == 200:
                soup_obj = BeautifulSoup(r.text, 'html.parser')
                
                title = soup_obj.find('h1')
                title_text = title.get_text(strip=True) if title else 'Sin título'
                
                # Extraer imágenes
                imgs = []
                for img in soup_obj.find_all('img', src=True):
                    src = img.get('src', '')
                    if '/wp-content/uploads' in src:
                        imgs.append(src)
                
                # Únicos
                unique_imgs = list(set(imgs))
                
                if len(unique_imgs) > 3:  # Solo guardar si tiene más de 3 imágenes
                    galeria_data[title_text] = {
                        'url': url,
                        'imagenes': unique_imgs,
                        'count': len(unique_imgs)
                    }
                    print(f"{title_text}")
                    print(f"  URL: {url}")
                    print(f"  Imágenes: {len(unique_imgs)}")
                    for img in unique_imgs[:5]:
                        print(f"    - {img.split('/')[-1]}")
                    if len(unique_imgs) > 5:
                        print(f"    ... y {len(unique_imgs) - 5} más")
                    print()
        except Exception as e:
            pass

# Guardar en JSON
with open('gallery_data.json', 'w', encoding='utf-8') as f:
    json.dump(galeria_data, f, ensure_ascii=False, indent=2)

print(f"\nDatos guardados en gallery_data.json")
print(f"Total de artículos con galerías: {len(galeria_data)}")
