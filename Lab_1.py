from PIL import Image
import sys
import os

INPUT = "img.png"
OUTPUT = "img_marked.png"
EXPECTED_WIDTH = 960
EXPECTED_HEIGHT = 1280

POINTS = [
    ((64, 64, 255), "upper_left"),
    ((255, 255, 64), "upper_right"),
    ((255, 64, 255), "lower_left"),
]

POINT_SIZE = 3

def clamp(v, a, b):
    return max(a, min(b, v))

def draw_point(pixels, width, height, x_center, y_center, color, size=1):
    half = size // 2
    for yy in range(y_center - half, y_center - half + size):
        for xx in range(x_center - half, x_center - half + size):
            if 0 <= xx < width and 0 <= yy < height:
                pixels[xx, yy] = color

def main():
    if not os.path.exists(INPUT):
        print(f"Ошибка: файл '{INPUT}' не найден в текущей папке: {os.getcwd()}")
        sys.exit(1)

    img = Image.open(INPUT).convert("RGB")
    w, h = img.size
    if (w, h) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        print(f"Внимание: ожидаемый размер {EXPECTED_WIDTH}x{EXPECTED_HEIGHT},"
              f" а файл имеет {w}x{h}. Скрипт всё равно выполнится.")
    pixels = img.load()

    # координаты углов
    coords = {
        "upper_left": (0, 0),
        "upper_right": (w - 1, 0),
        "lower_left": (0, h - 1),
        "lower_right": (w - 1, h - 1),
        "center": (w // 2, h // 2),
    }

    for color, pos_name in POINTS:
        if pos_name not in coords:
            print(f"Неправильная позиция: {pos_name}")
            continue
        x, y = coords[pos_name]
        draw_point(pixels, w, h, x, y, color, size=POINT_SIZE)

    img.save(OUTPUT)
    print(f"Сохранено: {OUTPUT}")

if __name__ == "__main__":
    main()
