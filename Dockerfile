FROM python:3.10
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["gunicorn", "proyectoDjango.wsgi:application", "--bind", "0.0.0.0:8000"]
