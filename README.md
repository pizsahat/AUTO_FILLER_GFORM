# AUTO_FILLER_GFORM

Sebuah tool untuk mengisi Google Form secara otomatis dengan berbagai mode pengisian data.

## Prerequisites

Sebelum menjalankan aplikasi, pastikan Anda telah menginstall dependencies berikut:

### 1. Install Selenium
```bash
pip install selenium
```

### 2. Install Faker
```bash
pip install faker
```

## Cara Penggunaan

### 1. Persiapan
- Pastikan Anda memiliki URL Google Form yang ingin diisi
- Masukkan URL Google Form ke dalam kode sesuai dengan file yang akan digunakan

### 2. Menjalankan Script

Terdapat 3 jenis script yang dapat digunakan:

#### A. Random Penuh (`index.py`)
Script ini akan mengisi form dengan data yang benar-benar random.

```bash
python index.py
```

**Karakteristik:**
- Data dibuat secara acak menggunakan library Faker
- Tidak ada kontrol terhadap kuantitas atau jenis data
- Sepenuhnya otomatis dan random

#### B. Random dengan Set Kuantitas (`randomset.py`)
Script ini memungkinkan Anda mengatur kuantitas data per pertanyaan.

```bash
python randomset.py
```

**Karakteristik:**
- Data random namun dapat dikontrol kuantitasnya
- Anda dapat menentukan berapa banyak data untuk setiap field
- Lebih fleksibel dalam pengaturan

#### C. Data Statis (`statis.py`)
Script ini menggunakan data yang telah ditentukan sebelumnya.

```bash
python statis.py
```

**Karakteristik:**
- Menggunakan data yang sudah ditetapkan
- Konsisten dan dapat diprediksi
- Cocok untuk testing dengan data spesifik

## Konfigurasi

1. **URL Google Form**: Pastikan untuk mengganti URL Google Form di dalam kode dengan URL form yang ingin Anda isi
2. **WebDriver**: Pastikan ChromeDriver atau webdriver lainnya sudah terinstall dan dapat diakses
3. **Delay**: Sesuaikan delay/waktu tunggu jika diperlukan untuk menghindari deteksi bot

## Struktur Project

```
project/
│
├── index.py          # Script random penuh
├── randomset.py      # Script random dengan set kuantitas
├── statis.py         # Script data statis
└── README.md         # Dokumentasi ini
```

## Catatan Penting

⚠️ **Disclaimer**: Tool ini dibuat untuk tujuan edukasi dan testing. Pastikan Anda memiliki izin untuk mengisi form yang ditargetkan dan tidak melanggar terms of service dari Google Forms.

## Troubleshooting

### Error Common:
1. **WebDriver not found**: Pastikan ChromeDriver sudah terinstall
2. **Form tidak terdeteksi**: Periksa selector element di Google Form
3. **Rate limiting**: Tambahkan delay yang lebih lama antar request

### Tips:
- Gunakan mode headless browser untuk performa lebih baik
- Monitor penggunaan untuk menghindari rate limiting
- Test dengan jumlah data kecil terlebih dahulu

## Kontribusi

Jika Anda ingin berkontribusi atau melaporkan bug, silakan buat issue atau pull request.

---