import os
import shutil
from datetime import datetime

# Ganti ini sesuai lokasi xampp kamu
xampp_path = r"C:\xampp\mysql"
data_path = os.path.join(xampp_path, "data")
backup_path = os.path.join(xampp_path, "backup")
today = datetime.now().strftime("%Y%m%d")
renamed_path = os.path.join(xampp_path, f"data_{today}")

excluded_folders = {'mysql', 'test', 'phpmyadmin', 'performance_schema'}

def copy_folder(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s_item = os.path.join(src, item)
        d_item = os.path.join(dst, item)
        if os.path.isdir(s_item):
            shutil.copytree(s_item, d_item, dirs_exist_ok=True)
        else:
            shutil.copy2(s_item, d_item)

# Step 1: Rename data → data_YYYYMMDD
if not os.path.exists(data_path):
    print("❌ Folder 'data' tidak ditemukan.")
    exit(1)

try:
    # Jika target rename sudah ada, tambahkan counter sampai mendapat nama unik
    def unique_path(path):
        if not os.path.exists(path):
            return path
        base = path
        counter = 1
        while True:
            candidate = f"{base}_{counter}"
            if not os.path.exists(candidate):
                return candidate
            counter += 1

    final_renamed_path = unique_path(renamed_path)
    os.rename(data_path, final_renamed_path)
    # update renamed_path agar langkah berikutnya memakai nama yang benar
    renamed_path = final_renamed_path
    # tampilkan nama folder yang dipakai (bisa berbeda jika counter dipakai)
    print(f"✅ Folder 'data' berhasil di-rename menjadi '{os.path.basename(renamed_path)}'")
except Exception as e:
    print(f"❌ Gagal rename folder: {e}")
    exit(1)

# Step 2: Copy backup → data
try:
    shutil.copytree(backup_path, data_path)
    print("✅ Folder 'backup' berhasil dicopy ke 'data'")
except Exception as e:
    print(f"❌ Gagal menyalin backup: {e}")
    exit(1)

# Step 3: Salin folder & file ibdata1 dari data_YYYYMMDD ke data baru
for item in os.listdir(renamed_path):
    src_item = os.path.join(renamed_path, item)
    dst_item = os.path.join(data_path, item)

    if os.path.isdir(src_item) and item not in excluded_folders:
        try:
            shutil.copytree(src_item, dst_item, dirs_exist_ok=True)
            print(f"📁 Folder '{item}' disalin")
        except Exception as e:
            print(f"⚠️  Gagal salin folder '{item}': {e}")
    elif os.path.isfile(src_item) and item == 'ibdata1':
        try:
            shutil.copy2(src_item, dst_item)
            print("📄 File 'ibdata1' berhasil disalin")
        except Exception as e:
            print(f"⚠️  Gagal salin ibdata1: {e}")

print("\n🎉 Selesai. Silakan coba jalankan ulang MySQL dari XAMPP.")
