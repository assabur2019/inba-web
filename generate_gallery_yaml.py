import json
import re

# Cargar mapeo de galerías
with open('gallery_mapping.json', 'r', encoding='utf-8') as f:
    gallery_mapping = json.load(f)

# Para cada archivo, generar el front matter actualizado
for filepath, gallery_images in gallery_mapping.items():
    print(f"\n{'='*70}")
    print(f"ARCHIVO: {filepath}")
    print(f"{'='*70}")
    print(f"Total de imágenes: {len(gallery_images)}\n")
    
    # Generar YAML para la galería
    yaml_gallery = "gallery:\n"
    for img in gallery_images:
        yaml_gallery += f'  - image: "{img["image"]}"\n'
        yaml_gallery += f'    label: "{img["label"]}"\n'
    
    print(yaml_gallery)

# Crear un archivo con el template para actualizar manualmente
print("\n" + "="*70)
print("TEMPLATE PARA ACTUALIZAR FRONT MATTER")
print("="*70)

for filepath, gallery_images in gallery_mapping.items():
    print(f"\n\n# {filepath}")
    print(f"Reemplazar la sección 'gallery:' con:\n")
    
    yaml_gallery = "gallery:\n"
    for img in gallery_images:
        yaml_gallery += f'  - image: "{img["image"]}"\n'
        yaml_gallery += f'    label: "{img["label"]}"\n'
    
    print(yaml_gallery)

# Guardar el template completo en un archivo
with open('gallery_updates.txt', 'w', encoding='utf-8') as f:
    for filepath, gallery_images in gallery_mapping.items():
        f.write(f"\n# {filepath}\n")
        f.write(f"# Total de imágenes: {len(gallery_images)}\n\n")
        f.write("gallery:\n")
        for img in gallery_images:
            f.write(f'  - image: "{img["image"]}"\n')
            f.write(f'    label: "{img["label"]}"\n')
        f.write("\n")

print("\n\nTemplate guardado en gallery_updates.txt")
