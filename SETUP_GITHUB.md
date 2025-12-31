# Panduan Push ke GitHub

Ikuti langkah-langkah berikut untuk push project ke GitHub:

## 1. Inisialisasi Git Repository

```bash
cd "/Users/fachrainazis02/Project Documentation/KRSBI 2023/KAMERA KRSBI 2023"
git init
```

## 2. Tambahkan File ke Git

```bash
git add robot_vision.py
git add config.py
git add requirements.txt
git add README.md
git add .gitignore
git add SETUP_GITHUB.md
```

Atau tambahkan semua file sekaligus (kecuali yang di .gitignore):
```bash
git add .
```

## 3. Buat Commit Pertama

```bash
git commit -m "Initial commit: KRSBI Robot Vision System"
```

## 4. Buat Repository di GitHub

1. Buka [https://github.com](https://github.com)
2. Login ke akun GitHub Anda
3. Klik tombol "+" di pojok kanan atas, pilih "New repository"
4. Isi detail repository:
   - Repository name: `krsbi-robot-vision` (atau nama lain)
   - Description: "Robot Vision System untuk KRSBI 2023"
   - Pilih "Public" 
   - **JANGAN** centang "Initialize this repository with a README"
5. Klik "Create repository"

## 5. Hubungkan Local Repository ke GitHub

Ganti `username` dengan username GitHub Anda:

```bash
git remote add origin https://github.com/username/krsbi-robot-vision.git
```

Atau gunakan SSH (jika sudah setup SSH key):
```bash
git remote add origin git@github.com:username/krsbi-robot-vision.git
```

## 6. Push ke GitHub

```bash
git branch -M main
git push -u origin main
```

Jika diminta login:
- Username: username GitHub Anda
- Password: gunakan **Personal Access Token**, bukan password biasa

### Cara Membuat Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token → pilih scope "repo"
3. Copy token dan gunakan sebagai password

## 7. Verifikasi

Buka repository di GitHub dan pastikan semua file sudah ter-upload.

## Update Project di Masa Depan

Setelah melakukan perubahan:

```bash
git add .
git commit -m "Deskripsi perubahan"
git push
```

## Tips

1. **File Sensitif**: Pastikan tidak ada data sensitif (password, API key) dalam kode
2. **Commit Message**: Gunakan pesan commit yang jelas dan deskriptif
3. **Branch**: Untuk development, buat branch baru:
   ```bash
   git checkout -b development
   ```
4. **Pull Request**: Untuk kolaborasi, gunakan pull request
5. **.gitignore**: File yang sudah ada di `.gitignore` tidak akan ter-push

## Troubleshooting

### Error: "repository not found"
- Periksa URL repository sudah benar
- Pastikan repository sudah dibuat di GitHub

### Error: "permission denied"
- Periksa Personal Access Token
- Atau setup SSH key

### Error: "failed to push some refs"
- Pull dulu: `git pull origin main --allow-unrelated-histories`
- Lalu push lagi: `git push origin main`

## Kontak

Jika ada masalah, buka issue di repository GitHub.
