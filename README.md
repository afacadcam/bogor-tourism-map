# 🗺️ Bogor Tourism Map (GIS Pariwisata Bogor)

[![Django](https://img.shields.io/badge/Django-5.2.6-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-PostGIS-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgis.net/)
[![Leaflet](https://img.shields.io/badge/Leaflet-1.9.4-199900?style=for-the-badge&logo=leaflet&logoColor=white)](https://leafletjs.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

**Bogor Tourism Map** adalah aplikasi web berbasis **Sistem Informasi Geografis (GIS)** yang dirancang untuk memetakan, mengelola, serta menganalisis persebaran destinasi wisata di wilayah Bogor, Jawa Barat. Dibangun menggunakan **Django (GeoDjango)** dengan database spasial **PostgreSQL/PostGIS** serta visualisasi peta interaktif **Leaflet.js**, aplikasi ini menyajikan fitur pencarian lokasi terdekat (spatial query), import/export data massal, dan dashboard visual analitik kunjungan.

---

## 📌 Fitur Unggulan

### 1. Peta Interaktif & Spasial (Leaflet.js + PostGIS)

### 2. Manajemen Destinasi Wisata (CRUD & Import/Export)

### 3. Dashboard Analitik & Statistik Kunjungan

### 4. Production-Ready & Sub-path Support

* **Sub-path / Subdirectory Deployment**: Dukungan deploy di sub-path (misalnya `https://domain.com/python`) melalui variabel lingkungan `SUB_PATH` tanpa merusak *routing* asset static dan media.
* **Dual Server Interface**: Siap dijalankan via **WSGI** (Gunicorn) maupun **ASGI** (Uvicorn).
* **Optimasi Aset**: Integrasi **WhiteNoise** untuk *serving* static file performa tinggi.
* **Pengujian Kinerja**: Script pengujian beban endpoint bawaan (`performance_test.py`).

---

## Arsitektur & Tech Stack

| Komponen              | Teknologi                               | Keterangan                               |
|:--------------------- |:--------------------------------------- |:---------------------------------------- |
| **Backend Framework** | Django 5.2.6 (GeoDjango)                | Core framework MVC/MVT                   |
| **Spatial Database**  | PostgreSQL + PostGIS                    | Database relasional spasial (SRID 4326)  |
| **Database Driver**   | Psycopg 3 (`psycopg`, `psycopg-binary`) | Konektor PostgreSQL modern               |
| **Frontend Mapping**  | Leaflet.js 1.9.4 & OpenStreetMap        | Rendering peta interaktif                |
| **UI Components**     | Bootstrap 5.3.3 & Font Awesome 6.5.0    | Desain responsif dan modern              |
| **Charts & Graphs**   | Chart.js                                | Visualisasi dashboard analitik           |
| **Data Processing**   | Pandas, OpenPyXL, Xlrd                  | Pemrosesan file CSV & Excel              |
| **Web Server**        | Gunicorn / Uvicorn + WhiteNoise         | Deployment WSGI/ASGI & static management |

---

## Prasyarat Sistem (Prerequisites)

Sebelum instalasi, pastikan sistem telah terpasang:

1. **Python 3.10+** dan `pip`
2. **PostgreSQL** (versi 14+) beserta ekstensi **PostGIS**
3. **Pustaka Spasial Geospasial (GDAL & GEOS)**  
   *Di Ubuntu/Debian:*

   ```bash
   sudo apt update
   sudo apt install -y binutils libproj-dev gdal-bin libgdal-dev python3-gdal postgis postgresql-postgis
   ```

   *Di Arch:*

   ```bash
   sudo pacman -Syu
   sudo pacman -S --needed gdal geos proj postgis postgresql python-gdal
   ```

---

## Panduan Instalasi Lokal

### 1. Clone Repositori

```bash
git clone https://github.com/afacadcam/app-python-map-gis.git
cd app-python-map-gis
```

### 2. Buat & Aktifkan Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Pasang Dependensi

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Konfigurasi Database PostGIS

Buka terminal PostgreSQL (`psql`) dan buat database dengan ekstensi PostGIS:

```sql
CREATE DATABASE bogor_tourism_db;
\c bogor_tourism_db;
CREATE EXTENSION postgis;
\q
```

### 5. Konfigurasi Environment Variables (`.env`)

Salin file template `.env.example` ke `.env`:

```bash
cp .env.example .env
```

Sesuaikan parameter database dan secret key pada file `.env`:

```env
SECRET_KEY=kunci-rahasia-django-anda
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
SUB_PATH=

DB_NAME=bogor_tourism_db
DB_USER=postgres
DB_PASSWORD=password_db_anda
DB_HOST=localhost
DB_PORT=5432
```

### 6. Migrasi Database & Load Data Awal Kategori

Jalankan migrasi tabel spasial dan muat data kategori pariwisata:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata categories.json
```

### 7. Buat Akun Administrator & Kumpulkan Static Files

```bash
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 8. Jalankan Server Pengembangan

```bash
python manage.py runserver
```

Buka browser dan akses aplikasi di: **`http://127.0.0.1:8000/`**

---

## Dokumentasi Endpoint API

| Endpoint                                | Metode | Parameter                                | Deskripsi                                                                               |
|:--------------------------------------- |:------:|:---------------------------------------- |:--------------------------------------------------------------------------------------- |
| `/api/places/`                          | `GET`  | `category` *(opsional)*                  | Mengembalikan seluruh tempat wisata dalam format standar **GeoJSON FeatureCollection**. |
| `/api/nearby/`                          | `GET`  | `lat`, `lng`, `radius` *(km, default 5)* | Pencarian tempat wisata terdekat berbasis kalkulasi spasial jarak PostGIS.              |
| `/analytics/api/category-distribution/` | `GET`  | -                                        | Data agregasi jumlah tempat wisata per kategori untuk Chart.js.                         |
| `/analytics/api/monthly-visits/`        | `GET`  | -                                        | Data tren kunjungan per bulan selama 12 bulan terakhir.                                 |
| `/analytics/api/top-places/`            | `GET`  | -                                        | Daftar 5 destinasi dengan kunjungan terbanyak.                                          |
| `/analytics/api/rating-distribution/`   | `GET`  | -                                        | Sebaran klasifikasi rating tempat wisata.                                               |
| `/analytics/api/visitor-analytics/`     | `GET`  | -                                        | Statistik rekapitulasi analitik pengunjung.                                             |

---

## 🧪 Pengujian Kinerja (Performance Test)

Repositori ini menyertakan skrip pengujian beban untuk mengevaluasi latensi dan keandalan endpoint:

```bash
python performance_test.py
```

*Catatan: Pastikan mengubah variabel `base_url` di dalam file `performance_test.py` sesuai alamat server yang sedang diuji.*
