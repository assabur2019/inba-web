# Manual de actualización del sitio inba.cl

Sitio del Internado Nacional Barros Arana. Este documento es para quien publique cambios cuando el administrador habitual no esté.

El sitio que ve el público está en el hosting del dominio. Un push a GitHub no actualiza https://inba.cl/.

## Qué es cada cosa

| Pieza | Dónde está | Para qué sirve |
|---|---|---|
| Código y contenidos | Repositorio Git `assabur2019/inba-web`, carpeta del proyecto | Origen de las páginas |
| Sitio público | https://inba.cl/ en el servidor `192.141.168.52` | Lo que ve la gente |
| Panel del hosting | https://alpha-052.xhost.cl:2083/ | Subir archivos. La cuenta del sitio es `gxkdmjyuzp`. La carpeta web es `/home/gxkdmjyuzp/public_html` |
| GitHub Pages | https://assabur2019.github.io/inba-web/ | Copia antigua. No es el sitio oficial |

La clave del panel no está en este repositorio. Pídala a quien administraba la cuenta.

No use la dirección `cwp.inba.cl`: el certificado del panel no coincide con ese nombre y el navegador bloquea la entrada. Use `https://alpha-052.xhost.cl:2083/`.

## Qué no hay que cambiar

No modifique el DNS del correo. El correo de inba.cl está en Google. No toque estos registros:

- MX
- SPF (`v=spf1 include:_spf.google.com`)
- DKIM (`google._domainkey`)
- DMARC (`_dmarc`)

Tampoco cambie el registro A de `inba.cl`. Ya apunta al servidor correcto.

## Programas necesarios

- Git
- Hugo **0.164.0 extended** (la misma versión con la que se construye el sitio)
- Node.js (solo para el buscador Pagefind)

En Windows, el proyecto usado hasta ahora está en `c:\wamp64\www\2026-nuevo`.

## Dónde se edita el contenido

| Qué quiere publicar | Dónde |
|---|---|
| Noticia | Carpeta nueva en `content/noticias/nombre-corto/index.md`, con sus fotos y videos dentro de esa misma carpeta |
| Comunicado | `content/comunicados/nombre.md` |
| Videos de la portada (los tres recuadros) | `data/home_videos.yaml` |
| Página de todos los videos | No se edita a mano. Lista sola los `.mp4` que estén dentro de las noticias, más los de YouTube declarados en `data/home_videos.yaml` |
| Textos fijos (quiénes somos, estamentos, etc.) | `content/` en la carpeta de esa sección |
| Imágenes sueltas que no pertenecen a una noticia | `static/images/` |

Una noticia lleva al inicio del `index.md` un bloque como este:

```yaml
---
title: "Título"
date: 2026-09-30
image: "hero.jpg"
excerpt: "Una frase para la portada y el listado."
---
```

`image` es el archivo que está en la misma carpeta de la noticia. La fecha determina el orden: la más nueva sale primero.

Para copiar el formato, abra una noticia reciente y duplique su estructura.

## 1. Revisar en el computador antes de publicar

En la carpeta del proyecto:

```text
hugo server -D --port 8090 --bind 127.0.0.1
```

Abra http://localhost:8090/ y revise la página que cambió. Detenga el servidor antes de generar la versión final.

## 2. Generar el sitio para inba.cl

Tiene que construirse con la dirección del dominio. Si se construye para GitHub, los enlaces quedan en `/inba-web/` y el sitio se ve roto en inba.cl.

PowerShell, en la carpeta del proyecto:

```text
$env:HUGO_RELATIVEURLS = "false"
hugo --gc --minify --baseURL "https://inba.cl/" --destination "deploy\site-inba"
npx -y pagefind --site "deploy\site-inba"
```

Compruebe el archivo `deploy\site-inba\index.html`. La línea canónica debe decir `https://inba.cl/`. No debe aparecer `github.io` ni `/inba-web/`.

La carpeta `deploy\site-inba` es solo el paquete para subir. No se edita a mano. Lo que se edita es `content/`, `data/`, `layouts/` y `static/`.

## 3. Armar el zip

El panel anuncia un máximo de 500 MB, pero el servidor rechaza archivos grandes con el error **413 Request Entity Too Large**. Cada zip debe pesar **menos de 40 MB**.

Cambio chico (una noticia, un texto, una foto): comprima solo lo que cambió, conservando las carpetas. Ejemplos:

- Noticia nueva: la carpeta `noticias/nombre-de-la-noticia/` y también `noticias/index.html` e `index.html` de la raíz del paquete, porque el listado y la portada cambiaron.
- Solo un texto de una página existente: el `index.html` de esa página.

Cambio grande: parta todo `deploy\site-inba` en varios zip de menos de 40 MB (`parte-01.zip`, `parte-02.zip`, …). Al descomprimirlos uno tras otro en el mismo lugar, el sitio queda completo.

Al descomprimir, un archivo con el mismo nombre reemplaza al anterior. Si en el repositorio se borró una página, hay que borrarla también a mano en `public_html`. El zip no elimina archivos viejos.

## 4. Subir y publicar

1. Entre a https://alpha-052.xhost.cl:2083/ con el usuario del sitio.
2. **File Manager**.
3. Abra `public_html`.
4. **Upload** y suba el zip (o los zip, de a uno o en grupo, cada uno bajo 40 MB).
5. En cada zip use descomprimir. El destino tiene que ser `/home/gxkdmjyuzp/public_html/`, no una carpeta nueva.

## 5. Sacar los zip del sitio

Dentro de `public_html` el botón de borrar no funciona: el panel responde `Access denied. Invalid path`.

1. Mueva cada `parte-*.zip` desde `public_html` a `/home/gxkdmjyuzp/tmp/`.
2. Entre a `tmp` y bórralos ahí.

No los deje en `public_html`. Cualquiera que conozca el nombre podría descargarlos en `https://inba.cl/parte-01.zip`.

**File System Lock** (menú **File Management**) debe decir **Unlocked**. Si dice **Locked**, pulse **Unlock** antes de subir. Con el candado activo no se puede cambiar ningún archivo.

## 6. Comprobar en el dominio

Abra estas direcciones en una ventana de incógnito:

- https://inba.cl/ muestra el sitio y no salta a github.io.
- https://www.inba.cl/ muestra lo mismo.
- La noticia o página que acaba de cambiar abre y se ven sus fotos.
- Si tocó videos: https://inba.cl/videos/
- Si tocó el buscador: busque una palabra de la página nueva.

Si inba.cl redirige a `assabur2019.github.io`, en `public_html` volvió el redirect viejo. Tiene que estar el `index.html` generado en el paso 2, y el `.htaccess` no debe contener `github.io`.

## Git y GitHub

Guarde los cambios de contenido en Git para que el próximo administrador parta del mismo material. Eso no publica el sitio.

El flujo de GitHub Actions («Publicar sitio Hugo en GitHub Pages») sigue construyendo la copia de GitHub Pages. Esa copia no es inba.cl. No hace falta tocarla para una actualización normal.

## Si algo falla

| Lo que pasa | Qué hacer |
|---|---|
| El zip dice que es muy grande o aparece 413 | Pártelo en archivos de menos de 40 MB y súbalos de nuevo |
| El basurero no borra el zip | Muévalo a `/home/gxkdmjyuzp/tmp/` y bórralo ahí |
| La página abre sin estilos | El sitio se construyó con la dirección de GitHub. Repita el paso 2 y suba de nuevo `index.html`, `css/` y `js/` |
| Una foto de noticia no aparece | El archivo no está en la carpeta de esa noticia, o el nombre en `image:` no coincide |
| El correo de @inba.cl falla después de un cambio | Revise que nadie haya editado MX, SPF, DKIM o DMARC. Esos registros no forman parte de una actualización del sitio |
