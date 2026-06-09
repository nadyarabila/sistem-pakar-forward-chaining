# Sistem Pakar Diagnosis Penyakit Kulit

Sistem pakar berbasis Python dan Streamlit yang digunakan untuk melakukan diagnosis awal penyakit kulit menggunakan metode **Forward Chaining**. Sistem bekerja dengan mencocokkan gejala yang dipilih pengguna terhadap basis aturan (rule base) untuk menghasilkan kemungkinan diagnosis penyakit.

---

## Fitur Utama

* Diagnosa penyakit kulit menggunakan metode Forward Chaining
* Pemilihan area tubuh sebelum diagnosis
* Filtering gejala berdasarkan area tubuh
* Trace proses inferensi (Forward Chaining)
* Menampilkan rule yang terpenuhi
* Menampilkan deskripsi penyakit
* Menampilkan penyebab penyakit
* Menampilkan saran penanganan awal
* Antarmuka interaktif berbasis Streamlit

---

## Penyakit yang Didukung

* Dermatitis (Eksim)
* Psoriasis
* Tinea (Kurap / Ringworm)
* Skabies (Kudis)
* Acne Vulgaris (Jerawat)
* Urtikaria (Biduran)

---

## Teknologi yang Digunakan

* Python
* Streamlit
* Forward Chaining
* Rule-Based Expert System

---

## Cara Menjalankan Project

1. Clone repository ini
2. Install dependency:

```bash
pip install streamlit
```

3. Jalankan aplikasi:

```bash
streamlit run app.py
```

4. Buka browser pada alamat yang diberikan oleh Streamlit

---

## Notes

Project ini dikembangkan sebagai implementasi Sistem Pakar untuk diagnosis awal penyakit kulit menggunakan pendekatan rule-based dan metode Forward Chaining. Sistem dirancang untuk membantu pengguna mengenali kemungkinan penyakit berdasarkan gejala yang dialami.

---

## Author

**Nadya Rabila**

---

## Disclaimer

Sistem ini hanya digunakan untuk tujuan edukasi dan diagnosis awal. Hasil yang diberikan bukan pengganti konsultasi dengan dokter atau tenaga medis profesional.
