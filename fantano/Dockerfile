FROM python:3-onbuild

WORKDIR /var/fantano
COPY . .
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:5000"]
