
# systemctl 로 변경
#source /app/fastapi/venv310/bin/activate

#cd /app/fastapi

#uvicorn app.main:app --reload --host=10.1.90.155 --port=8385 --> service.log &

#gunicorn -k uvicorn.workers.UvicornWorker --access-logfile ./gunicorn-access.log app.main:app --bind 10.1.90.155:8384 --workers 2 --daemon
