"""Раскладывает исходники из input/ в images/ под имена из main.html и index.html.
У картинок с белым фоном (title, sign, wallet, yellow-sign) белый фон от краёв делается прозрачным."""
from collections import deque
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "input"
DST = ROOT / "images"

# исходник (время в имени) -> имя в images/
MAP = {
    "02.45.16": "bag.jpg",
    "02.45.19": "carpet.jpg",
    "02.45.21": "hosts.jpg",
    "02.45.24": "icon-rutube.jpg",
    "02.45.26": "icon-telegram.jpg",
    "02.45.28": "icon-tiktok.jpg",
    "02.45.31": "icon-vk.jpg",
    "02.45.33": "label-social.jpg",
    "02.45.36": "label-about.jpg",
    "02.45.38": "label-when.jpg",
    "02.45.42": "paper-when.jpg",
    "02.45.44": "letters.jpg",
    "02.45.46": "paper-call.jpg",
    "02.45.48": "paper-social.jpg",
    "02.45.51": "paper-about.jpg",
    "02.45.53": "phone.jpg",
    "02.45.55": "pravda.jpg",
    "02.45.58": "sign.png",
    "02.46.00": "title.png",
    "02.46.03": "wallet.png",
    "02.46.06": "wood.jpg",
    "02.46.08": "yellow-sign.png",
}


def white_to_transparent(img, tol=28):
    img = img.convert("RGBA")
    w, h = img.size
    px = img.load()
    seen = bytearray(w * h)
    q = deque()
    for x in range(w):
        q.append((x, 0)); q.append((x, h - 1))
    for y in range(h):
        q.append((0, y)); q.append((w - 1, y))
    while q:
        x, y = q.popleft()
        if not (0 <= x < w and 0 <= y < h) or seen[y * w + x]:
            continue
        seen[y * w + x] = 1
        r, g, b, _ = px[x, y]
        if min(r, g, b) < 255 - tol:
            continue
        px[x, y] = (255, 255, 255, 0)
        q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return img


for key, name in MAP.items():
    img = Image.open(SRC / f"2026-10-30 {key}.jpg")
    if name.endswith(".png"):
        white_to_transparent(img, 1 if name == "title.png" else 28).save(DST / name)
    else:
        img.convert("RGB").save(DST / name, quality=92)
    print(name)
