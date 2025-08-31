python version : 3.10.6
# 1. Clone repo
git clone https://github.com/rabbanisidiq14/gudang.git <br/>
cd gudang

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
python manage.py runserver <br/>
python mqtt_subscriber.py <br/>
python pengendali_service.py
