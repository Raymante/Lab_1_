from PIL import Image
import os, sys

INPUT = "img.png"
OUTPUT_PBM = "img_marked.pbm"
EXPECTED_WIDTH = 960
EXPECTED_HEIGHT = 1280

POINTS = [
    ((64, 64, 255), "upper_left"),
    ((255, 255, 64), "upper_right"),
    ((255, 64, 255), "lower_left"),
]

POINT_SIZE = 3

THRESHOLD = 128

def draw_point(pixels, width, height, x_center, y_center, color, size=1):
    half = size // 2
    for yy in range(y_center - half, y_center - half + size):
        for xx in range(x_center - half, x_center - half + size):
            if 0 <= xx < width and 0 <= yy < height:
                pixels[xx, yy] = color

def rgb_to_luminance(r,g,b):
    return 0.299*r + 0.587*g + 0.114*b

def main():
    if not os.path.exists(INPUT):
        print(f"Ошибка: файл '{INPUT}' не найден в текущей папке: {os.getcwd()}")
        sys.exit(1)

    img = Image.open(INPUT).convert("RGB")
    w, h = img.size
    if (w, h) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        print(f"Внимание: ожидаемый размер {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}, но файл имеет {w}x{h}. Продолжаю работать с реальным размером.")

    pixels = img.load()

    coords = {
        "upper_left": (0, 0),
        "upper_right": (w - 1, 0),
        "lower_left": (0, h - 1),
        "lower_right": (w - 1, h - 1),
        "center": (w // 2, h // 2),
    }

    for color, pos_name in POINTS:
        x, y = coords.get(pos_name, (None, None))
        if x is None:
            continue
        draw_point(pixels, w, h, x, y, color, size=POINT_SIZE)

    bw = [[0]*w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            r,g,b = pixels[x,y]
            lum = rgb_to_luminance(r,g,b)
            bit = 0 if lum > THRESHOLD else 1
            bw[y][x] = bit

    with open(OUTPUT_PBM, "w", encoding="ascii") as f:
        f.write("P1\n")
        f.write(f"#lab1_variant10_to_pbm.py\n")
        f.write(f"{w} {h}\n")
        for y in range(h):
            row = " ".join(str(bw[y][x]) for x in range(w))
            f.write(row + "\n")

    print(f"Готово: сохранён {OUTPUT_PBM}")

if __name__ == "__main__":
    main()
