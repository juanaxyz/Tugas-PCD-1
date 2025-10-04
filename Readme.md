# Image Processing with Python (PCD Tugas 1)

Proyek ini berisi berbagai fungsi pengolahan citra digital menggunakan Python dan library [Pillow](https://python-pillow.org/).  
Fitur meliputi transformasi geometris, efek ripple, konversi warna, thresholding, bit depth reduction, brightness/contrast adjustment, dan negasi.

## Requirement

- Python 3.x
- Pillow (lihat `requirement.txt`)

Install dependensi:
```
pip install -r requirement.txt
```

## Fitur Utama

### 1. Transformasi Geometri
- **Translasi**: Menggeser gambar pada sumbu x dan y.
- **Perbesaran**: Memperbesar gambar dengan faktor skala.
- **Pencerminan**: Mirror pada sumbu x, y, atau kombinasi.
- **Rotasi**: Memutar gambar dengan sudut tertentu.
- **Crop**: Memotong bagian gambar.
- **Affine Transform**: Transformasi affine umum (rotasi, skala, shear, dsb).

### 2. Efek Ripple
- **Ripple**: Efek gelombang pada gambar sesuai rumus:
  ```
  x = x' + ax * sin(2πy'/Tx)
  y = y' + ay * sin(2πx'/Ty)
  ```

### 3. Enhancement & Konversi Warna
- **RGB ke Grayscale**: Konversi gambar berwarna ke grayscale.
- **Grayscale ke Biner**: Thresholding sederhana.
- **Double Thresholding**: Thresholding dengan dua ambang.
- **Bit Depth Reduction**: Mengurangi kedalaman bit citra grayscale.
- **Brightness Adjustment**: Mengubah kecerahan gambar.
- **Contrast Adjustment**: Mengubah kontras gambar.
- **Negasi**: Membalik warna gambar (negatif).

## Cara Penggunaan

1. Letakkan gambar pada folder `images/` (default: `baymax(1).jpg`).
2. Jalankan file utama:
   ```
   python main.py
   ```
3. Aktifkan fungsi yang diinginkan dengan meng-uncomment baris pada bagian:
   ```python
   if __name__ == "__main__":
       # Contoh:
       # gray = rgb_to_grayscale()
       # grayscale_to_biner()
       # ripple(10, 10, 50, 50)
       # change_brigthness(50)
       # change_kontras(1.5)
       # negasi()
   ```

## Struktur File

- `main.py` : Kode utama dan semua fungsi pengolahan citra.
- `requirement.txt` : Daftar dependensi Python.

## Catatan

- Gambar default yang digunakan adalah `./images/baymax(1).jpg`. Ubah path jika ingin menggunakan gambar lain.
- Beberapa fungsi membutuhkan gambar dalam mode tertentu (misal grayscale). Pastikan urutan pemanggilan fungsi sesuai kebutuhan.

---

**Tugas Praktikum Pengolahan Citra Digital**  
Fakultas/Prodi: [Isi sesuai kebutuhan]