# Usa una imagen base de Python
FROM python:3.10

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala las dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Añade el directorio actual al PYTHONPATH
ENV PYTHONPATH="/app"

# Expone el puerto 8000
EXPOSE 8000

# Comando para arrancar Gunicorn
CMD ["gunicorn", "proyectoDjango.wsgi:application", "--bind", "0.0.0.0:8000"]
