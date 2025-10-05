from PIL import Image
import math

# Load gambar
img = Image.open("./images/baymax(1).jpg")
px = img.load()


def cek_tipe_gambar():
    print(px[0, 0])
    try:
        r, g, b = px[0, 0]
        print(r, g, b)
        return "RGB"
    except TypeError:
        return "L"


mode = cek_tipe_gambar()
if mode == "RGB":
    canvas = Image.new("RGB", (img.width, img.height), (255, 255, 255))
else:
    canvas = Image.new("L", (img.width, img.height), 255)


def tampilkan_gambar_asli():
    img.show(title="Gambar Asli")
    return img


def save_gambar():
    if latest_image is not None:
        latest_image.save("./output/hasil.jpg")
        print("Gambar berhasil disimpan sebagai 'hasil.jpg'")
    else:
        print("Tidak ada gambar hasil yang bisa disimpan.")


def translasi(s_x: int, s_y: int) -> Image:
    """
    Fungsi untuk melakukan translasi gambar
    Args :
    s_x (int) : nilai translasi dalam sumbu x
    s_y (int) : nilai translasi dalam sumbu y
    Returns : Image
    """
    if mode == "RGB":
        temp_canvas = Image.new("RGB", (img.width, img.height), (255, 255, 255))
    else:
        temp_canvas = Image.new("L", (img.width, img.height), 255)
    px_new = temp_canvas.load()

    # Pindahkan pixel sesuai rumus translasi
    for y in range(img.height):
        for x in range(img.width):
            new_x, new_y = x + s_x, y + s_y
            if 0 <= new_x < img.width and 0 <= new_y < img.height:
                px_new[new_x, new_y] = px[x, y]

    temp_canvas.show()  ## Tampilkan hasil
    return temp_canvas


def perbesaran(sx: int, sy: int) -> Image:
    # perbesaran
    s_x, s_y = sx, sy
    new_w, new_h = img.width * s_x, img.height * s_y
    if mode == "RGB":
        canvas = Image.new("RGB", [new_w, new_h], (0, 0, 0))
    else:
        canvas = Image.new("L", [new_w, new_h], 255)
    px_baru = canvas.load()

    for x in range(new_w):
        for y in range(new_h):
            src_x = int(x / s_x)
            src_y = int(y / s_y)
            px_baru[x, y] = px[src_x, src_y]

    canvas.show()  # show image perbesaran
    return canvas


def pencerminan_x() -> Image:
    center = (img.width - 1) / 2
    px_new = canvas.load()

    for x in range(img.width):
        for y in range(img.height):
            xb = 2 * center - x
            px_new[x, y] = px[xb, y]

    canvas.show()  # image pencerminan
    return canvas


def pencerminan_y() -> Image:
    center = (img.height - 1) / 2
    px_new = canvas.load()

    for x in range(img.width):
        for y in range(img.height):
            yb = 2 * center - y
            px_new[x, y] = px[x, yb]

    canvas.show()  # image pencerminan
    return canvas


def pencerminan_kombinasi() -> Image:
    px_new = canvas.load()

    for x in range(img.width):
        for y in range(img.height):
            xb = img.width - 1 - x
            yb = img.height - 1 - y
            px_new[x, y] = px[xb, yb]

    canvas.show()  # image pencerminan
    return canvas


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
    canvas_crop = Image.new("RGB", [wb, hb], (255, 255, 255))
    px_new = canvas_crop.load()

    for x in range(wb):
        for y in range(hb):
            px_new[x, y] = px[x + xL, y + yT]

    canvas_crop.show()
    return canvas_crop


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


def hitung_nilai_gray(r: int, g: int, b: int) -> int:
    return int(0.299 * r + 0.587 * g + 0.114 * b)
    # return int((r + g + b ) // 3)


def rgb_to_grayscale():
    canvas = Image.new("L", (img.width, img.height))
    px_new = canvas.load()

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = px[x, y]
            gray = hitung_nilai_gray(r, g, b)
            px_new[x, y] = gray

    # canvas.show()
    return canvas


def grayscale_to_biner():
    canvas_biner = Image.new("1", (img.width, img.height))
    px_new = canvas_biner.load()

    T = 128  # threesold

    for x in range(img.width):
        for y in range(img.height):
            r, g, b = px[x, y]
            gray = hitung_nilai_gray(r, g, b)
            if gray >= T:
                px_new[x, y] = 255  # putih
            else:
                px_new[x, y] = 0  # hitam
    canvas_biner.show()
    return canvas_biner


def double_thresholding(T1: int, T2: int):
    canvas_biner = Image.new("1", (img.width, img.height))
    px_new = canvas_biner.load()

    for x in range(img.width):
        for y in range(img.height):
            # print(px[x,y])
            r, g, b = px[x, y]
            gray = hitung_nilai_gray(r, g, b)
            if T1 <= gray <= T2:
                # px_new[x, y] = 0  # black
                px_new[x, y] = 255
            else:
                # px_new[x, y] = 255  # white
                px_new[x, y] = 0
    canvas_biner.show()
    return canvas_biner


def RGB_to_mbit(m: int):
    canvas_mbit = Image.new("L", (img.width, img.height))
    px_new = canvas_mbit.load()

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = px[x, y]
            gray = hitung_nilai_gray(r, g, b)
            p_baru = (2 ** (8 - m + 1)) * int(gray / 2 ** (8 - m + 1))
            px_new[x, y] = p_baru

    canvas_mbit.show()
    return canvas_mbit


def change_brigthness(c: int):
    px_new = canvas.load()

    for y in range(img.height):
        for x in range(img.width):
            if len(px[x, y]) == 3:
                r, g, b = px[x, y]
                r_baru = r + c
                g_baru = g + c
                b_baru = b + c
                px_new[x, y] = (r_baru, g_baru, b_baru)
            else:
                gray = px[x, y]
                gray_baru = gray + c
                px_new[x, y] = gray_baru
    canvas.show()
    return canvas


def change_kontras(faktor: float):
    px_new = canvas.load()

    for y in range(img.height):
        for x in range(img.width):
            # cek gambar rgb atau grayscale
            if type(px[x, y]) is tuple:
                r, g, b = px[x, y]
                r_baru = int(faktor * (r - 128) + 128)
                g_baru = int(faktor * (g - 128) + 128)
                b_baru = int(faktor * (b - 128) + 128)
                px_new[x, y] = (r_baru, g_baru, b_baru)
            else:
                gray = px[x, y]
                gray_baru = int(faktor * (gray - 128) + 128)
                px_new[x, y] = gray_baru
    canvas.show()
    return canvas


def negasi():
    px_new = canvas.load()
    for x in range(img.width):
        for y in range(img.height):
            if type(px[x, y]) is tuple:
                r, g, b = px[x, y]
                r_baru = 255 - r
                g_baru = 255 - g
                b_baru = 255 - b
                px_new[x, y] = (r_baru, g_baru, b_baru)
            else:
                gray = px[x, y]
                gray_baru = 255 - gray
                px_new[x, y] = gray_baru
    canvas.show()
    return canvas


latest_image = None

if __name__ == "__main__":
    # print resolusi gambar
    print(f"width original : {img.width}")
    print(f"height original : {img.height}")

    while True:
        print("\nMenu Operasi Citra:")
        print("1. Translasi")
        print("2. Perbesaran")
        print("3. Pencerminan X")
        print("4. Pencerminan Y")
        print("5. Pencerminan Kombinasi")
        print("6. Rotasi")
        print("7. Crop")
        print("8. Affine Transformasi (Rotasi)")
        print("9. Ripple")
        print("10. RGB ke Grayscale")
        print("11. Grayscale ke Biner")
        print("12. Double Thresholding")
        print("13. RGB ke m-bit")
        print("14. Ubah Brightness")
        print("15. Ubah Kontras")
        print("16. Negasi")
        print("98. Save Gambar Terbaru")
        print("99. Tampilkan Gambar Asli")
        print("0. Keluar")
        pilihan = input("Pilih Operasi : ")
        match pilihan:
            case "1":
                sx = int(input("Masukkan translasi X: "))
                sy = int(input("Masukkan translasi Y: "))
                latest_image = translasi(sx, sy)
            case "2":
                sx = int(input("Masukkan faktor perbesaran X: "))
                sy = int(input("Masukkan faktor perbesaran Y: "))
                latest_image = perbesaran(sx, sy)
            case "3":
                latest_image = pencerminan_x()
            case "4":
                latest_image = pencerminan_y()
            case "5":
                latest_image = pencerminan_kombinasi()
            case "6":
                deg = int(input("Masukkan derajat rotasi: "))
                latest_image = rotate(deg)
            case "7":
                xL = int(input("x Left: "))
                xR = int(input("x Right: "))
                yT = int(input("y Top: "))
                yB = int(input("y Bottom: "))
                latest_image = crop(xL, xR, yT, yB)
            case "8":
                print("Affine Transformasi:")
                print("1. Rotasi (masukkan derajat)")
                print("2. Scaling (sx, sy)")
                print("3. Shear (kx, ky)")

                sub = input("Pilih jenis transformasi: ")

                if sub == "1":  # rotasi
                    deg = float(input("Masukkan derajat rotasi: "))
                    matrix = hitung_matrix_rotation(deg)
                    e, f = 0, 0

                elif sub == "2":  # scaling
                    sx = float(input("Masukkan faktor skala X: "))
                    sy = float(input("Masukkan faktor skala Y: "))
                    matrix = [[sx, 0], [0, sy]]
                    e, f = 0, 0

                elif sub == "3":  # shear
                    kx = float(input("Masukkan faktor shear X: "))
                    ky = float(input("Masukkan faktor shear Y: "))
                    matrix = [[1, kx], [ky, 1]]
                    e, f = 0, 0

                else:  # custom
                    print("tidak valid")

                latest_image = affine(matrix, translasi=(e, f))

            case "9":
                ax = int(input("ax: "))
                ay = int(input("ay: "))
                Tx = int(input("Tx: "))
                Ty = int(input("Ty: "))
                latest_image = ripple(ax, ay, Tx, Ty)
            case "10":
                latest_image = rgb_to_grayscale()
                latest_image.show()
            case "11":
                latest_image = grayscale_to_biner()
            case "12":
                T1 = int(input("Threshold bawah: "))
                T2 = int(input("Threshold atas: "))
                latest_image = double_thresholding(T1, T2)
            case "13":
                m = int(input("Masukkan nilai m (1-8): "))
                latest_image = RGB_to_mbit(m)
            case "14":
                c = int(input("Masukkan perubahan brightness: "))
                latest_image = change_brigthness(c)
            case "15":
                f = float(input("Masukkan faktor kontras: "))
                latest_image = change_kontras(f)
            case "16":
                latest_image = negasi()
            case "98":
                save_gambar()
            case "99":
                tampilkan_gambar_asli()
            case "0":
                print("Keluar.")
                break
            case _:
                print("Pilihan tidak valid.")
