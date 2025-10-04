from PIL import Image
import math

# Load gambar
img = Image.open("./images/baymax(1).jpg")

px = img.load()
print(px)

def translasi(s_x: int, s_y: int) -> Image:
    """
    Fungsi untuk melakukan translasi gambar
    Args :
    s_x (int), s_y (int): nilai translasi dalam sumbu x dan y
    Returns : Image
    """
    canvas_Translasi = Image.new("RGB", (img.width, img.height), (255, 255, 255))
    px_new = canvas_Translasi.load()

    # Pindahkan pixel sesuai rumus translasi
    for y in range(img.height):
        for x in range(img.width):
            new_x, new_y = x + s_x, y + s_y
            if 0 <= new_x < img.width and 0 <= new_y < img.height:
                px_new[x + s_x, y + s_y] = px[x, y]

    canvas_Translasi.show()  ## Tampilkan hasil


def perbesaran(x: int) -> Image:
    # perbesaran
    s_x, s_y = x, x
    new_w, new_h = img.width * s_x, img.height * s_y
    canvas_perbesaran = Image.new("RGB", [new_w, new_h], (0, 0, 0))
    px_baru = canvas_perbesaran.load()

    for x in range(new_w):
        for y in range(new_h):
            src_x = int(x / s_x)
            src_y = int(y / s_y)
            px_baru[x, y] = px[src_x, src_y]

    canvas_perbesaran.show()  # show image perbesaran


def pencerminan_x() -> Image:
    center = (img.width - 1) / 2
    canvas = Image.new("RGB", [img.width, img.height], (0, 0, 0))
    px_new = canvas.load()

    for x in range(img.width):
        for y in range(img.height):
            xb = 2 * center - x
            px_new[x, y] = px[xb, y]

    canvas.show()  # image pencerminan


def pencerminan_y() -> Image:
    center = (img.height - 1) / 2
    canvas = Image.new("RGB", [img.width, img.height], (0, 0, 0))
    px_new = canvas.load()

    for x in range(img.width):
        for y in range(img.height):
            yb = 2 * center - y
            px_new[x, y] = px[x, yb]

    canvas.show()  # image pencerminan


def pencerminan_kombinasi() -> Image:
    canvas = Image.new("RGB", [img.width, img.height], (0, 0, 0))
    px_new = canvas.load()

    for x in range(img.width):
        for y in range(img.height):
            xb = img.width - 1 - x
            yb = img.height - 1 - y
            px_new[x, y] = px[xb, yb]

    canvas.show()  # image pencerminan


def rotate(degree: int) -> Image:
    """
    Fungsi untuk melakukan rotasi gambar (Rotation) di sekitar pusat gambar.
    Args:
    degree (int): Sudut rotasi dalam derajat (misalnya 90, 180, 270).
    Returns: Image
    """
    theta = math.radians(degree)

    # Ukuran dan pusat gambar asli
    w_orig, h_orig = img.size
    cx_orig, cy_orig = w_orig / 2, h_orig / 2

    # Menghitung ukuran bounding box (kanvas baru) yang diperlukan
    # agar seluruh gambar yang diputar termuat
    wb = int(abs(w_orig * math.cos(theta)) + abs(h_orig * math.sin(theta)))
    hb = int(abs(w_orig * math.sin(theta)) + abs(h_orig * math.cos(theta)))

    # Pusat kanvas baru
    cx_new, cy_new = wb / 2, hb / 2

    print(f"INFO: Rotasi {degree}° -> Ukuran kanvas baru: {wb}x{hb}")
    canvas = Image.new("RGB", (wb, hb), (255, 255, 255))
    px_new = canvas.load()

    # Rotasi dilakukan dengan langkah-langkah:
    # 1. Geser pusat gambar asli ke (0, 0)
    # 2. Terapkan rumus rotasi
    # 3. Geser kembali ke pusat kanvas baru

    for y in range(h_orig):
        for x in range(w_orig):
            # 1. Translate ke origin (0, 0)
            x_shift = x - cx_orig
            y_shift = y - cy_orig

            # 2. Rotasi
            x_rot = (x_shift * math.cos(theta)) - (y_shift * math.sin(theta))
            y_rot = (x_shift * math.sin(theta)) + (y_shift * math.cos(theta))

            # 3. Translate kembali ke pusat kanvas baru untuk mendapatkan koordinat (xb, yb)
            xb = round(x_rot + cx_new)
            yb = round(y_rot + cy_new)

            # Pastikan koordinat tujuan berada dalam batas kanvas baru
            if 0 <= xb < wb and 0 <= yb < hb:
                px_new[xb, yb] = px[x, y]

    canvas.show(title=f"Rotasi {degree}°")
    return canvas


def crop(xL: int, xR: int, yT: int, yB: int):
    wb = xR - xL
    hb = yB - yT
    canvas = Image.new("RGB", [wb, hb], (255, 255, 255))
    px_new = canvas.load()

    for x in range(wb):
        for y in range(hb):
            px_new[x, y] = px[x + xL, y + yT]

    canvas.show()


def affine(matrix, translasi=(0, 0)) -> Image:
    """
    Transformasi affine , hasil akan dicrop ke ukuran asli gambar.
    matrix = [[a, b], [c, d]]
    translate = (e, f)
    """

    a, b = matrix[0]
    c, d = matrix[1]
    e, f = translasi

    print(matrix[0])
    cx, cy = img.width / 2, img.height / 2

    canvas = Image.new("RGB", (img.width, img.height), (255, 255, 255))
    px_new = canvas.load()

    for x in range(img.width):
        for y in range(img.height):
            x_shift = x - cx
            y_shift = y - cy
            # Transformasi affine
            xb = round(a * x_shift + b * y_shift + e) + cx
            yb = round(c * x_shift + d * y_shift + f) + cy

            # Pastikan koordinat tujuan berada dalam batas kanvas
            if 0 <= xb < img.width and 0 <= yb < img.height:
                px_new[xb, yb] = px[x, y]
    canvas.show()
    return canvas


def hitung_matrix_rotation(degree: int):
    theta = math.radians(degree)
    return [[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]]


def ripple(ax: int = 10, ay: int = 10, Tx: int = 50, Ty: int = 50) -> Image:
    """
    Efek ripple manual sesuai rumus:
    x = x' + ax * sin(2πy'/Tx)
    y = y' + ay * sin(2πx'/Ty)

    Args:
        ax (int): Besar efek gelombang pada sumbu x (amplitudo).
        ay (int): Besar efek gelombang pada sumbu y (amplitudo).
        Tx (int): Periode gelombang pada sumbu x.
        Ty (int): Periode gelombang pada sumbu y.

    Returns:
        Image: Gambar hasil transformasi ripple.
    """
    canvas = Image.new("RGB", (img.width, img.height), (255, 255, 255))
    px_new = canvas.load()

    for y_ in range(img.height):
        for x_ in range(img.width):
            # Hitung posisi sumber dengan rumus ripple
            x = x_ + int(ax * math.sin(2 * math.pi * y_ / Tx))
            y = y_ + int(ay * math.sin(2 * math.pi * x_ / Ty))

            if 0 <= x < img.width and 0 <= y < img.height:
                px_new[x_, y_] = px[x, y]

    canvas.show(title="Efek Ripple Manual")
    return canvas


# operasi enhancement


def rgb_to_grayscale():
    canvas = Image.new("L", (img.width, img.height))
    px_new = canvas.load()

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = px[x, y]
            # gray = (r + g + b ) // 3
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            px_new[x, y] = gray

    # canvas.show()
    return canvas


def grayscale_to_biner():
    canvas = Image.new("1", (img.width, img.height))
    px_new = canvas.load()

    for x in range(img.width):
        for y in range(img.height):
            r, g, b = px[x, y]
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            T = 128
            if gray >= T:
                px_new[x, y] = 255  # putih
            else:
                px_new[x, y] = 0  # hitam
    canvas.show()
    return canvas


def double_thresholding(T1: int, T2: int):
    canvas = Image.new("1", (img.width, img.height))
    px_new = canvas.load()

    for x in range(img.width):
        for y in range(img.height):
            # print(px[x,y])
            r, g, b = px[x, y]
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            if T1 <= gray <= T2:
                # px_new[x, y] = 0  # black
                px_new[x, y] = 255
            else:
                # px_new[x, y] = 255  # white
                px_new[x, y] = 0
    canvas.show()
    return canvas


def RGB_to_mbit(m: int):
    canvas = Image.new("L", (img.width, img.height))
    px_new = canvas.load()

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = px[x, y]
            # gray = (r + g + b ) // 3
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            p_baru = (2**(8-m+1)) * int(gray/2**(8-m+1))
            px_new[x, y] = p_baru

    canvas.show()
    return canvas

def  change_brigthness(c: int):
    canvas = Image.new("RGB", (img.width, img.height))
    px_new = canvas.load()

    for y in range(img.height):
        for x in range(img.width):
            if len(px[x,y]) == 3:
                r, g, b = px[x, y]
                r_baru = r + c
                g_baru = g + c
                b_baru =  b + c
                px_new[x, y] = (r_baru, g_baru, b_baru)
            else : 
                gray = px[x,y]
                gray_baru = gray + c
                px_new[x,y] = gray_baru
    canvas.show()
    return canvas

def change_kontras(faktor : float):
    if type(px[0,0]) is tuple:
        canvas = Image.new("RGB", (img.width, img.height))
        px_new = canvas.load()
    else :
        canvas = Image.new("L", (img.width, img.height))
        px_new = canvas.load()

    for y in range(img.height):
        for x in range(img.width):
            # print(type(px[x,y]))
            if type(px[x,y]) is tuple:
                
                r, g, b = px[x, y]
                r_baru = int(faktor * (r-128) + 128)
                g_baru = int(faktor * (g-128) + 128)
                b_baru = int(faktor * (b-128) + 128)
                px_new[x, y] = (r_baru, g_baru, b_baru)
            else : 
                gray = px[x,y]
                gray_baru = int(faktor * (gray-128) + 128)
                px_new[x,y] = gray_baru
    canvas.show()
    return canvas

def negasi():
    if type(px[0,0]) is tuple:
        canvas = Image.new("RGB", (img.width, img.height))
        px_new = canvas.load()
    else :
        canvas = Image.new("L", (img.width, img.height))
        px_new = canvas.load()
    
    for x in range(img.width):
        for y in range(img.height):
            if type(px[x,y]) is tuple:
                r, g, b = px[x, y]
                r_baru = 255 - r
                g_baru = 255 - g
                b_baru = 255 - b
                px_new[x, y] = (r_baru, g_baru, b_baru)
            else : 
                gray = px[x,y]
                gray_baru = 255 - gray
                px_new[x,y] = gray_baru
    canvas.show()

if __name__ == "__main__":
    # print resolusi gambar
    print(f"width original : {img.width}")
    print(f"height original : {img.height}")

    gray = rgb_to_grayscale()
    px = gray.load()
    # gray.show()
    # img.show()
    # rotasi matrix dengan T affine
    # affine(hitung_matrix_rotation(180), translasi=(0, 0))
    # ripple_manual(5,5,200,100)
    # ripple(100,20, 200,100)
    # crop(100,400,100,400)
    # pencerminan_kombinasi()
    # double_thresholding(100, 300)
    # RGB_to_mbit(3)
    # change_brigthness(100)
    # rgb_to_grayscale()
    # grayscale_to_biner()
    # change_kontras(1.5)
    negasi()