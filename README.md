# 1. Clone repo
git clone <url-repo-kamu>
cd <nama-folder-project>

# 2. Buat virtual environment
python -m venv venv

# 3. Aktifkan venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4. Install dependencies dari requirements.txt
pip install -r requirements.txt

# 5. Apply migrations (jika pakai Django)
python manage.py migrate

# 6. (opsional) buat superuser
python manage.py createsuperuser

# 7. Jalankan server
python manage.py runserver
python mqtt_subscriber.py
python pengendali_service.py
