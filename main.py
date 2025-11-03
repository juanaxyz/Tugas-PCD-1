from PIL import Image
import math
import matplotlib.pyplot as plt

latest_image = None


def save_gambar():
    if latest_image is not None:
        latest_image.save("./output/hasil.jpg")
        print("Gambar berhasil disimpan sebagai 'hasil.jpg'")
    else:
        print("Tidak ada gambar hasil yang bisa disimpan.")


def translasi(image_input: Image):
    """
    Fungsi untuk melakukan translasi gambar
    Args :
    s_x (int) : nilai translasi dalam sumbu x
    s_y (int) : nilai translasi dalam sumbu y
    Returns : Image
    """

    s_x = int(input("Masukkan translasi X: "))
    s_y = int(input("Masukkan translasi Y: "))
    img = Image.open(image_input)
    px = img.load()

    if image_type == "RGB":
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

    return temp_canvas


def perbesaran(image_input: Image):
    sx = int(input("Masukkan skala X: "))
    sy = int(input("Masukkan skala Y: "))
    img = Image.open(image_input)
    px = img.load()
    # perbesaran
    s_x, s_y = sx, sy
    new_w, new_h = img.width * s_x, img.height * s_y
    if image_type == "RGB":
        canvas = Image.new("RGB", [new_w, new_h], (0, 0, 0))
    else:
        canvas = Image.new("L", [new_w, new_h], 255)
    px_baru = canvas.load()

    for x in range(new_w):
        for y in range(new_h):
            src_x = int(x / s_x)
            src_y = int(y / s_y)
            px_baru[x, y] = px[src_x, src_y]

    return canvas


def pencerminan_x(image_input: Image) -> Image:
    img = Image.open(image_input)
    px = img.load()
    center = (img.width - 1) / 2
    canvas = Image.new(
        image_type,
        (img.width, img.height),
        (255, 255, 255) if image_type == "RGB" else 255,
    )
    px_new = canvas.load()

    for x in range(img.width):
        for y in range(img.height):
            xb = int(round(2 * center - x))
            xb = int(2 * center - x)
            px_new[x, y] = px[xb, y]

    # canvas.show()  # image pencerminan
    return canvas


def pencerminan_y(image_input: Image) -> Image:
    img = Image.open(image_input)
    px = img.load()
    center = (img.height - 1) / 2
    canvas = Image.new(
        image_type,
        (img.width, img.height),
        (255, 255, 255) if image_type == "RGB" else 255,
    )
    px_new = canvas.load()

    for x in range(img.width):
        for y in range(img.height):
            yb = int(2 * center - y)
            px_new[x, y] = px[x, yb]

    # canvas.show()  # image pencerminan
    return canvas


def pencerminan_kombinasi(image_input: Image) -> Image:
    img = Image.open(image_input)
    px = img.load()
    canvas = Image.new(
        image_type,
        (img.width, img.height),
        (255, 255, 255) if image_type == "RGB" else 255,
    )
    px_new = canvas.load()

    for x in range(img.width):
        for y in range(img.height):
            xb = img.width - 1 - x
            yb = img.height - 1 - y
            px_new[x, y] = px[xb, yb]

    # canvas.show()  # image pencerminan
    return canvas


def rotate(image_input: Image) -> Image:
    """
    Fungsi untuk melakukan rotasi gambar (Rotation) di sekitar pusat gambar.
    Menggunakan interpolasi bilinear untuk hasil lebih halus.
    Args:
    degree (int): Sudut rotasi dalam derajat (misalnya 90, 180, 270).
    Returns: Image
    """
    img = Image.open(image_input)
    px = img.load()
    degree = int(input("Masukkan sudut rotasi (derajat): "))
    theta = math.radians(degree)

    # Ukuran dan pusat gambar asli
    w_orig, h_orig = img.size
    cx_orig, cy_orig = w_orig / 2, h_orig / 2

    # Menghitung ukuran kanvas baru
    wb = int(abs(w_orig * math.cos(theta)) + abs(h_orig * math.sin(theta)))
    hb = int(abs(w_orig * math.sin(theta)) + abs(h_orig * math.cos(theta)))

    # Pusat kanvas baru
    cx_new, cy_new = wb / 2, hb / 2

    print(f"INFO: Rotasi {degree}° -> Ukuran kanvas baru: {wb}x{hb}")
    canvas = Image.new(
        image_type,
        (wb, hb),
        (255, 255, 255) if image_type == "RGB" else 255,
    )
    px_new = canvas.load()

    # Untuk setiap pixel pada kanvas baru, cari posisi sumber pada gambar asli
    for y_new in range(hb):
        for x_new in range(wb):
            # Translate ke pusat kanvas baru
            x_shift = x_new - cx_new
            y_shift = y_new - cy_new

            # Inverse rotasi (dari kanvas baru ke gambar asli)
            x_orig = (
                (x_shift * math.cos(-theta)) - (y_shift * math.sin(-theta)) + cx_orig
            )
            y_orig = (
                (x_shift * math.sin(-theta)) + (y_shift * math.cos(-theta)) + cy_orig
            )

            if 0 <= x_orig < w_orig - 1 and 0 <= y_orig < h_orig - 1:
                # Interpolasi bilinear
                x0, y0 = int(math.floor(x_orig)), int(math.floor(y_orig))
                x1, y1 = x0 + 1, y0 + 1
                dx, dy = x_orig - x0, y_orig - y0

                def get_pixel(xx, yy):
                    if 0 <= xx < w_orig and 0 <= yy < h_orig:
                        return px[xx, yy]
                    return (255, 255, 255) if image_type == "RGB" else 255

                if image_type == "RGB":
                    p00 = get_pixel(x0, y0)
                    p10 = get_pixel(x1, y0)
                    p01 = get_pixel(x0, y1)
                    p11 = get_pixel(x1, y1)
                    r = (
                        p00[0] * (1 - dx) * (1 - dy)
                        + p10[0] * dx * (1 - dy)
                        + p01[0] * (1 - dx) * dy
                        + p11[0] * dx * dy
                    )
                    g = (
                        p00[1] * (1 - dx) * (1 - dy)
                        + p10[1] * dx * (1 - dy)
                        + p01[1] * (1 - dx) * dy
                        + p11[1] * dx * dy
                    )
                    b = (
                        p00[2] * (1 - dx) * (1 - dy)
                        + p10[2] * dx * (1 - dy)
                        + p01[2] * (1 - dx) * dy
                        + p11[2] * dx * dy
                    )
                    px_new[x_new, y_new] = (int(r), int(g), int(b))
                else:
                    p00 = get_pixel(x0, y0)
                    p10 = get_pixel(x1, y0)
                    p01 = get_pixel(x0, y1)
                    p11 = get_pixel(x1, y1)
                    gray = (
                        p00 * (1 - dx) * (1 - dy)
                        + p10 * dx * (1 - dy)
                        + p01 * (1 - dx) * dy
                        + p11 * dx * dy
                    )
                    px_new[x_new, y_new] = int(gray)
            # Jika di luar gambar asli, biarkan warna background
            # else: sudah otomatis background

    return canvas


def crop(image_input: Image) -> Image:
    img = Image.open(image_input)
    px = img.load()
    xL = int(input("Masukkan x Left (kiri): "))
    xR = int(input("Masukkan x Right (kanan): "))
    yT = int(input("Masukkan y Top (atas): "))
    yB = int(input("Masukkan y Bottom (bawah): "))
    wb = xR - xL
    hb = yB - yT

    canvas = Image.new(
        image_type, (wb, hb), (255, 255, 255) if image_type == "RGB" else 255
    )
    px_new = canvas.load()

    for x in range(wb):
        for y in range(hb):
            px_new[x, y] = px[x + xL, y + yT]

    return canvas


def transformasi_affine(image_path: Image):
    img = Image.open(image_path)
    canvas = Image.new("RGB", (img.width, img.height), (255, 255, 255))
    px = img.load()
    px_new = canvas.load()

    print("transformasi affine")
    rot = input("Rotasi (derajat, bisa kosong): ") or "0"
    sx = input("Skala X (default 1): ") or "1"
    sy = input("Skala Y (default 1): ") or "1"
    shx = input("Shear X (default 0): ") or "0"
    shy = input("Shear Y (default 0): ") or "0"
    tx = input("Translasi X (default 0): ") or "0"
    ty = input("Translasi Y (default 0): ") or "0"

    # Konversi ke float
    rot, sx, sy, shx, shy, tx, ty = map(float, [rot, sx, sy, shx, shy, tx, ty])

    # Hitung komponen matriks affine
    rad = math.radians(rot)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    # Matriks rotasi + skala + shear digabung
    a = sx * cos_a + shy * sin_a
    b = shx * cos_a - sy * sin_a
    d = sx * sin_a - shy * cos_a
    e = shx * sin_a + sy * cos_a
    f = ty

    matrix = (a, b, tx, d, e, f)

    print("Matriks Affine:", matrix)

    for x in range(img.width):
        for y in range(img.height):
            # Hitung posisi baru dengan matriks affine
            xb = int(a * x + b * y + tx)
            yb = int(d * x + e * y + f)

            # Pastikan koordinat sumber dan tujuan berada dalam batas kanvas
            if (
                0 <= xb < img.width
                and 0 <= yb < img.height
                and 0 <= x < img.width
                and 0 <= y < img.height
            ):
                px_new[xb, yb] = px[x, y]
    return canvas
    # # Terapkan transformasi
    # result = img.transform(img.size, Image.AFFINE, matrix)
    # result.show()


def ripple(image_input: Image) -> Image:
    """
    Efek ripple sesuai rumus:
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
    img = Image.open(image_input)
    px = img.load()
    canvas = Image.new(
        image_type,
        (img.width, img.height),
        (255, 255, 255) if image_type == "RGB" else 255,
    )
    px_new = canvas.load()

    ax = int(input("Masukkan amplitudo X (ax): "))
    ay = int(input("Masukkan amplitudo Y (ay): "))
    Tx = int(input("Masukkan periode X (Tx): "))
    Ty = int(input("Masukkan periode Y (Ty): "))

    for y_ in range(img.height):
        for x_ in range(img.width):
            # Hitung posisi sumber dengan rumus ripple
            x = x_ + int(ax * math.sin(2 * math.pi * y_ / Tx))
            y = y_ + int(ay * math.sin(2 * math.pi * x_ / Ty))

            if 0 <= x < img.width and 0 <= y < img.height:
                px_new[x_, y_] = px[x, y]

    # canvas.show(title="Efek Ripple Manual")
    return canvas


# operasi enhancement


def hitung_nilai_gray(r: int, g: int, b: int) -> int:
    return int(0.299 * r + 0.587 * g + 0.114 * b)
    # return int((r + g + b ) // 3)


def rgb_to_grayscale(image_input: Image) -> Image:
    img = Image.open(image_input)
    px = img.load()
    canvas = Image.new("L", (img.width, img.height))
    px_new = canvas.load()

    for y in range(img.height):
        for x in range(img.width):
            if image_type == "RGB":
                # if isinstance(px[x, y], tuple):
                r, g, b = px[x, y]
                gray = hitung_nilai_gray(r, g, b)
            else:
                gray = px[x, y]
            px_new[x, y] = gray

    # canvas.show()
    return canvas


def grayscale_to_biner(image_input: Image) -> Image:
    if image_type == "RGB":
        print("INFO: Gambar RGB otomatis dikonversi ke Grayscale dulu.")
        img = rgb_to_grayscale(image_input)
    else:
        img = Image.open(image_input)
    px = img.load()
    canvas_biner = Image.new("1", (img.width, img.height))
    px_new = canvas_biner.load()

    T = 128  # threshold

    for x in range(img.width):
        for y in range(img.height):
            pixel = px[x, y]
            gray = pixel
            if gray >= T:
                px_new[x, y] = 255  # putih
            else:
                px_new[x, y] = 0  # hitam
    # canvas_biner.show()
    return canvas_biner


def double_thresholding(image_input: Image) -> Image:
    if image_type == "RGB":
        print("INFO: Gambar RGB otomatis dikonversi ke Grayscale dulu.")
        img = rgb_to_grayscale(image_input)
    else:
        img = Image.open(image_input)
    px = img.load()
    canvas = Image.new("1", (img.width, img.height))
    px_new = canvas.load()

    T1 = int(input("Masukkan nilai threshold 1 (T1): "))
    T2 = int(input("Masukkan nilai threshold 2 (T2): "))

    for x in range(img.width):
        for y in range(img.height):
            pixel = px[x, y]
            gray = pixel
            if T1 <= gray <= T2:
                # px_new[x, y] = 0  # black
                px_new[x, y] = 255
            else:
                # px_new[x, y] = 255  # white
                px_new[x, y] = 0
    # canvas.show()
    return canvas


def RGB_to_mbit(image_input: Image) -> Image:
    img = Image.open(image_input)
    px = img.load()
    canvas = Image.new("L", (img.width, img.height))
    px_new = canvas.load()

    m = int(input("Masukkan nilai m (1-8): "))
    for y in range(img.height):
        for x in range(img.width):
            pixel = px[x, y]

            # if isinstance(pixel, tuple):
            if image_type == "RGB":
                r, g, b = pixel
                gray = hitung_nilai_gray(r, g, b)
            else:
                gray = pixel
            p_baru = (2 ** (8 - m + 1)) * int(gray / 2 ** (8 - m + 1))
            px_new[x, y] = p_baru

    # canvas.show()
    return canvas


def change_brigthness(image_input: Image) -> Image:
    img = Image.open(image_input)
    px = img.load()
    canvas = Image.new("RGB", (img.width, img.height))
    px_new = canvas.load()

    c = int(input("Masukkan nilai c (positif/negatif): "))

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
    # canvas.show()
    return canvas


def change_kontras(imageinput: Image) -> Image:
    img = Image.open(imageinput)
    px = img.load()
    canvas = Image.new("RGB", (img.width, img.height))
    px_new = canvas.load()

    faktor = float(
        input("Masukkan nilai faktor (>1 untuk perbesar, <1 untuk perkecil): ")
    )
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
    # canvas.show()
    return canvas


def negasi(image_input: Image) -> Image:
    img = Image.open(image_input)
    px = img.load()
    canvas = Image.new(
        image_type,
        (img.width, img.height),
        (255, 255, 255) if image_type == "RGB" else 255,
    )
    px_new = canvas.load()
    for x in range(img.width):
        for y in range(img.height):
            if image_type == "RGB":
                r, g, b = px[x, y]
                r_baru = 255 - r
                g_baru = 255 - g
                b_baru = 255 - b
                px_new[x, y] = (r_baru, g_baru, b_baru)
            else:
                gray = px[x, y]
                gray_baru = 255 - gray
                px_new[x, y] = gray_baru
    # canvas.show()
    return canvas


def histogram_RGB(image_input: Image):
    if image_type != "RGB":
        print("INFO: Gambar bukan RGB, histogram RGB tidak bisa dibuat.")
        return

    img = Image.open(image_input)
    px = img.load()
    hist_r = [0] * 256
    hist_g = [0] * 256
    hist_b = [0] * 256

    # Loop semua pixel
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = px[x, y]
            hist_r[r] += 1
            hist_g[g] += 1
            hist_b[b] += 1
    # Plot hasil
    plt.figure(figsize=(10, 4))

    plt.subplot(131)
    plt.bar(range(256), hist_r, color="red")
    plt.title("Red Channel")

    plt.subplot(132)
    plt.bar(range(256), hist_g, color="green")
    plt.title("Green Channel")

    plt.subplot(133)
    plt.bar(range(256), hist_b, color="blue")
    plt.title("Blue Channel")

    plt.tight_layout()
    plt.show()


def histogram_gray(image_input: Image):
    if image_type == "RGB":
        print("INFO: Gambar RGB, otomatis dikonversi ke grayscale dulu.")
        img = rgb_to_grayscale(image_input)
        # px = img.load()
    else:
        img = Image.open(image_input)

    px = img.load()
    hist_gray = [0] * 256

    for x in range(img.width):
        for y in range(img.height):
            # print(px[x, y])
            hist_gray[px[x, y]] += 1

    plt.figure(figsize=(6, 4))
    plt.subplot(111)
    plt.bar(range(256), hist_gray, color="gray")
    plt.title("Histogram Grayscale")

    plt.tight_layout()
    plt.show()

    return hist_gray


def histogram_equalization(image_input: Image) -> Image:
    """
    Melakukan ekualisasi histogram pada gambar grayscale.
    Jika gambar RGB, otomatis dikonversi ke grayscale dulu.
    """
    img = Image.open(image_input)
    # Konversi ke grayscale jika perlu
    if image_type == "RGB":
        gray_img = rgb_to_grayscale(image_input)
        px_gray = gray_img.load()
    else:
        gray_img = img.copy()
        px_gray = gray_img.load()

    # px_gray = gray_img.load()
    w, h = gray_img.size
    total_pixels = w * h
    k = 8  # gambar 8-bit (0–255)

    # 1. Hitung histogram
    hist = [0] * 256
    for y in range(h):
        for x in range(w):
            hist[px_gray[x, y]] += 1

    # 2. Hitung CDF
    cdf = [0] * 256
    cdf[0] = hist[0]
    for i in range(1, 256):
        cdf[i] = cdf[i - 1] + hist[i]

    # 3. Mapping pakai rumus
    mapping = [0] * 256
    for i in range(256):
        mapping[i] = round(cdf[i] * (2**k - 1) / total_pixels)

    # 4. Buat gambar baru dengan intensitas hasil equalization
    new_img = Image.new("L", (w, h))
    new_pixels = new_img.load()
    for y in range(h):
        for x in range(w):
            new_pixels[x, y] = mapping[px_gray[x, y]]

    # ✅ Hitung histogram BARU untuk perbandingan
    hist_new = [0] * 256
    for y in range(h):
        for x in range(w):
            hist_new[new_pixels[x, y]] += 1

    # Plot perbandingan histogram
    plt.figure(figsize=(12, 4))

    plt.subplot(121)
    plt.bar(range(256), hist, color="gray", alpha=0.7)
    plt.title("Histogram Sebelum Equalization")
    plt.xlabel("Intensitas")
    plt.ylabel("Frekuensi")

    plt.subplot(122)
    plt.bar(range(256), hist_new, color="blue", alpha=0.7)
    plt.title("Histogram Setelah Equalization")
    plt.xlabel("Intensitas")
    plt.ylabel("Frekuensi")

    plt.tight_layout()
    plt.show()

    return new_img


if __name__ == "__main__":
    image_path = "./images/baymax.jpg"
    # print resolusi gambar
    # print(f"width original : {img.width}")
    # print(f"height original : {img.height}")

    image_type = (
        "RGB" if isinstance(Image.open(image_path).getpixel((0, 0)), tuple) else "L"
    )
    print(f"INFO: Tipe gambar terdeteksi sebagai {image_type}")

    while True:
        print("\nMenu Operasi Citra:")
        print("1. Translasi")
        print("2. Perbesaran")
        print("3. Pencerminan X")
        print("4. Pencerminan Y")
        print("5. Pencerminan Kombinasi")
        print("6. Rotasi")
        print("7. Crop")
        print("8. Affine Transformasi")
        print("9. Ripple")
        print("10. RGB ke Grayscale")
        print("11. Grayscale ke Biner")
        print("12. Double Thresholding")
        print("13. RGB ke m-bit")
        print("14. Ubah Brightness")
        print("15. Ubah Kontras")
        print("16. Negasi")
        print("17. Histogram RGB")
        print("18. Histogram Grayscale")
        print("19. Ekualisasi Histogram")
        print("98. Save Gambar Terbaru")
        print("99. Tampilkan Gambar Asli")
        print("0. Keluar")
        pilihan = input("Pilih Operasi : ")
        match pilihan:
            case "1":
                latest_image = translasi(image_path)
                latest_image.show()

            case "2":
                latest_image = perbesaran(image_path)
                latest_image.show()
            case "3":
                latest_image = pencerminan_x(image_path)
                latest_image.show()
            case "4":
                latest_image = pencerminan_y(image_path)
                latest_image.show()
            case "5":
                latest_image = pencerminan_kombinasi(image_path)
                latest_image.show()
            case "6":
                latest_image = rotate(image_path)
                latest_image.show()
            case "7":
                latest_image = crop(image_path)
                latest_image.show()
            case "8":
                latest_image = transformasi_affine(image_path)
                latest_image.show()
            case "9":
                latest_image = ripple(image_path)
                latest_image.show()
            case "10":
                latest_image = rgb_to_grayscale(image_path)
                latest_image.show()
            case "11":
                latest_image = grayscale_to_biner(image_path)
                latest_image.show()
            case "12":
                latest_image = double_thresholding(image_path)
                latest_image.show()
            case "13":
                latest_image = RGB_to_mbit(image_path)
                latest_image.show()
            case "14":
                latest_image = change_brigthness(image_path)
                latest_image.show()
            case "15":
                latest_image = change_kontras(image_path)
                latest_image.show()
            case "16":
                latest_image = negasi(image_path)
                latest_image.show()
            case "17":
                histogram_RGB(image_path)
            case "18":
                histogram_gray(image_path)
            case "19":
                latest_image = histogram_equalization(image_path)
                latest_image.show()
            case "98":
                save_gambar()
            case "99":
                img = Image.open(image_path)
                img.show()
            case "0":
                print("Keluar dari program.")
                break
            case _:
                print("Pilihan tidak valid.")
