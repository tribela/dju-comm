dev: PYTHONUNBUFFERED=1 DEBUG=on ./manage.py runserver
web: uwsgi --master --die-on-term --http :${PORT:-5000} --module dju_community.wsgi
worker: python ./manage.py process_tasks
