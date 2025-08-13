set -e

pip run flask --app src.app db upgrade
pip run gunicorn src.wsgi:app