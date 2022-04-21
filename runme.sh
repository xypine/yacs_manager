python3 -m pip install -r requirements.txt
python3 -m gunicorn -w 4 -b 0.0.0.0:5000 server:app