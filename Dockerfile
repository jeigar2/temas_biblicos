# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requisitos e instala las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instala las dependencias de producción
#COPY requirements-prod.txt .
#RUN pip install --no-cache-dir -r requirements-prod.txt

# Instala Gunicorn (para producción)
RUN pip install --no-cache-dir gunicorn

# Copia todos los archivos de la aplicación
COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# Expone el puerto en el que la aplicación Flask correrá
EXPOSE 5000
# Comando para ejecutar la aplicación con Flask
#CMD ["python", "src/app.py"]    
# Comando para ejecutar la aplicación con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:app"]