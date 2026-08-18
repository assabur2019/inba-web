import requests
import os
import json
from urllib.parse import urlparse
from pathlib import Path

# Mapeo entre títulos del sitio viejo y archivos del sitio nuevo
mapping = {
    "¡Gran debut de nuestra Selección de Fútbol!": "content/noticias/debut-seleccion-futbol.md",
    "Noche de cine en el INBA: una comunidad que se encuentra": "content/noticias/noche-de-cine.md",
    "🏃‍♂️✨ INBA celebra la vida sana: energía, deporte y comunidad en el Día de la Actividad Física": "content/noticias/dia-actividad-fisica.md",
    "✨ ¡Nace INBA Comunica! Conéctate con nuestra comunidad": "content/noticias/nace-inba-comunica.md",
    "✨ ¡El recreo se llenó de música": "content/noticias/recreo-musica-encadenados.md",
    "✨ ¡Inspiradora Charla Magistral de Ciencias": "content/noticias/charla-magistral-ciencias.md",
    "Campeonato Futsal juegos deportivos escolares 2025": "content/noticias/campeones-balonmano/index.md"
}

# Cargar datos de galerías
with open('gallery_data.json', 'r', encoding='utf-8') as f:
    gallery_data = json.load(f)

print("=== DESCARGANDO IMÁGENES DE GALERÍAS ===\n")

# Crear directorio para imágenes si no existe
os.makedirs('static/images/noticias', exist_ok=True)

# Para cada galería
gallery_mapping = {}

for title, content_file in mapping.items():
    if title in gallery_data:
        gallery_info = gallery_data[title]
        print(f"\nProcesando: {title}")
        print(f"  Archivo: {content_file}")
        print(f"  Total de imágenes: {len(gallery_info['imagenes'])}")
        
        # Crear directorio específico para esta noticia
        content_name = Path(content_file).stem
        if content_name == 'index':
            content_name = Path(content_file).parent.name
        
        gallery_dir = f"static/images/noticias/{content_name}"
        os.makedirs(gallery_dir, exist_ok=True)
        
        gallery_array = []
        
        # Descargar cada imagen
        for i, img_url in enumerate(gallery_info['imagenes'], 1):
            try:
                # Obtener nombre de archivo original
                filename = img_url.split('/')[-1]
                filepath = f"{gallery_dir}/{filename}"
                
                # Descargar si no existe
                if not os.path.exists(filepath):
                    img_data = requests.get(img_url, timeout=10)
                    if img_data.status_code == 200:
                        with open(filepath, 'wb') as f:
                            f.write(img_data.content)
                        print(f"  ✓ Descargado: {filename}")
                    else:
                        print(f"  ✗ Error {img_data.status_code}: {filename}")
                else:
                    print(f"  ~ Existe: {filename}")
                
                # Crear entrada de galería
                image_path = f"images/noticias/{content_name}/{filename}"
                gallery_array.append({
                    'image': image_path,
                    'label': f"Imagen {i}"
                })
                
            except Exception as e:
                print(f"  ✗ Error descargando {filename}: {e}")
        
        gallery_mapping[content_file] = gallery_array

# Guardar mapeo
with open('gallery_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(gallery_mapping, f, ensure_ascii=False, indent=2)

print("\n\nDatos de galería guardados en gallery_mapping.json")
print(f"Total de noticias con galerías: {len(gallery_mapping)}")
