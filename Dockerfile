FROM python:3.10

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todo el contenido del proyecto
COPY . .

# Entra a la carpeta donde están manage.py y settings.py
WORKDIR /app/proyectoDjango

# Instala dependencias
RUN pip install --upgrade pip
RUN pip install -r ../requirements.txt

# Recolecta archivos estáticos (opcional pero recomendado)
RUN python manage.py collectstatic --noinput

# Expone el puerto para Render
EXPOSE 8000

# Lanza Gunicorn apuntando al módulo correcto
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn proyectoDjango.wsgi:application --bind 0.0.0.0:10000"]
