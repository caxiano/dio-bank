set -e

flask --app src.app db upgrade
run gunicorn src.wsgi:app