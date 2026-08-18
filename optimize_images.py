from pathlib import Path
from PIL import Image
import os

ROOT = Path(__file__).resolve().parent / "static" / "images"

if not ROOT.exists():
    raise SystemExit(f"No existe la carpeta de imágenes: {ROOT}")

processed = 0
saved = 0
before_total = 0
after_total = 0

for path in sorted(ROOT.rglob('*')):
    if not path.is_file():
        continue
    if path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
        continue

    before = path.stat().st_size
    before_total += before

    try:
        with Image.open(path) as img:
            if path.suffix.lower() in {".jpg", ".jpeg"}:
                rgb = img.convert("RGB")
                temp = path.with_suffix(path.suffix.lower() + ".tmp")
                rgb.save(temp, format="JPEG", quality=75, optimize=True, progressive=True)
            else:
                temp = path.with_suffix(path.suffix.lower() + ".tmp")
                img.save(temp, format="PNG", optimize=True, compress_level=9)

        temp_size = temp.stat().st_size
        if temp_size < before:
            os.replace(temp, path)
            after_total += temp_size
            saved += before - temp_size
            processed += 1
        else:
            temp.unlink(missing_ok=True)
            after_total += before
    except Exception:
        try:
            if path.with_suffix(path.suffix.lower() + ".tmp").exists():
                path.with_suffix(path.suffix.lower() + ".tmp").unlink(missing_ok=True)
        except Exception:
            pass
        after_total += before

print(f"images_optimized={processed}")
print(f"bytes_before={before_total}")
print(f"bytes_after={after_total}")
print(f"bytes_saved={saved}")
