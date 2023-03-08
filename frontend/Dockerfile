 FROM python:3.10-slim-buster
 RUN apt-get update
 RUN apt-get install nano
 
 RUN mkdir app
 WORKDIR app
 COPY ./requirements.txt /app/requirements.txt
 RUN pip3 install -r requirements.txt
  
 COPY . /app
  
CMD [ "python3", "app.py" ]
#  CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:80", "app:server"]