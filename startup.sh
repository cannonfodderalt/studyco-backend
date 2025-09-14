cd /home/site/wwwroot

python3 -m venv antenv
source antenv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate --noinput

gunicorn studyco.wsgi:application --bind 0.0.0.0:8000
