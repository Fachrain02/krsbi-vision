# KRSBI Robot Vision System

Sistem vision untuk robot sepak bola KRSBI menggunakan OpenCV dan deteksi warna HSV.

## Fitur

- **Deteksi Bola**: Mendeteksi bola berdasarkan warna orange menggunakan HSV color space
- **Deteksi Robot**: Mendeteksi robot teman berdasarkan marker warna
- **Komunikasi Serial**: Mengirim data posisi ke Arduino via serial
- **Base Station Communication**: Menerima perintah dari base station via socket
- **Real-time Tuning**: Trackbar untuk kalibrasi nilai HSV secara real-time

## Requirements

- Python 3.7+
- OpenCV (cv2)
- NumPy
- PySerial

## Instalasi

1. Clone repository ini:
```bash
git clone https://github.com/Fachrain02/krsbi-vision.git
cd krsbi-vision
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Konfigurasi:
   - Edit `config.py` atau langsung edit variabel di `robot_vision.py`
   - Sesuaikan `SERIAL_PORT` dengan port Arduino Anda
   - Sesuaikan `CAMERA_INDEX` jika menggunakan kamera eksternal

## Cara Penggunaan

### Mode Normal (dengan Arduino dan Socket)

```bash
python robot_vision.py
```

### Kalibrasi Warna

1. Jalankan program
2. Gunakan trackbar pada window "BOLA" untuk kalibrasi deteksi bola:
   - L_H, U_H: Range Hue (warna)
   - L_S, U_S: Range Saturation (intensitas warna)
   - L_V, U_V: Range Value (kecerahan)
3. Gunakan trackbar pada window "ROBOT" untuk kalibrasi deteksi robot
4. Nilai yang sudah dikalibrasi bisa disimpan sebagai default

### Kontrol

- **'q'**: Keluar dari program

## Struktur Project

```
.
├── robot_vision.py      # Program utama sistem vision robot
├── README.md            # Dokumentasi project
└── .gitignore           # Git ignore file
```

## Cara Kerja

### Deteksi Objek

1. **Capture Frame**: Mengambil frame dari kamera
2. **Color Conversion**: Konversi BGR ke HSV
3. **Thresholding**: Filter berdasarkan range warna HSV
4. **Morphological Operations**: Menghilangkan noise
5. **Contour Detection**: Menemukan objek
6. **Position Calculation**: Menghitung posisi dan mengirim ke Arduino

### Komunikasi Serial

Program mengirim data ke Arduino dengan format:
- `X[code]`: Posisi X bola (201-225)
- `Y[code]`: Posisi Y bola (201-216)
- `W[code]`: Posisi X robot teman (201-225)
- `Z[code]`: Command dari base station (4-9)

### Base Station Commands

- `go3000,4100,0`: Kick Off posisi 1
- `go7400,3000,0`: Kick Off posisi 2
- `go9000,0,135`: Corner A
- `go9000,6000,225`: Corner B
- `j`: Jalan
- `k`: Stop

## Troubleshooting

### Kamera tidak terdeteksi
- Pastikan kamera terhubung dengan benar
- Coba ubah `CAMERA_INDEX` menjadi 1 atau 2

### Serial connection failed
- Periksa port COM di Device Manager (Windows) atau `/dev/ttyUSB*` (Linux)
- Pastikan Arduino terhubung dan driver terinstall
- Program tetap berjalan dalam demo mode jika serial tidak tersedia

### Socket binding error
- Pastikan port tidak digunakan aplikasi lain
- Ubah `port` di konfigurasi jika diperlukan

## Konfigurasi Default HSV

### Bola (Orange)
- Hue: 0-35
- Saturation: 199-255
- Value: 220-255

### Robot (Magenta)
- Hue: 163-189
- Saturation: 213-255
- Value: 80-255

## Kontribusi

Silakan buat pull request atau issue untuk perbaikan dan penambahan fitur.

## Lisensi

MIT License

## Author

Fachrain Azis

## Catatan

Program ini dikembangkan untuk kompetisi KRSBI 2023. Sesuaikan parameter dan konfigurasi dengan kebutuhan robot Anda.
