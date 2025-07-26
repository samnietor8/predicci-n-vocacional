# Sistema de Predicción Vocacional

Este sistema utiliza un árbol de decisión para recomendar programas educativos basados en diferentes características del usuario como el tipo de instituto, nivel de formación, campo de estudio y estrato socioeconómico.

## Acceso en línea

La aplicación está disponible en línea en: [https://prediccion-vocacional.onrender.com](https://prediccion-vocacional.onrender.com)

## Descripción

El Sistema de Predicción Vocacional es una herramienta que ayuda a los estudiantes a encontrar el programa educativo más adecuado según sus preferencias y características. Utiliza un modelo de árbol de decisión previamente entrenado para hacer recomendaciones personalizadas.

Ahora disponible en dos versiones:
- **Aplicación de escritorio**: Interfaz gráfica con tkinter
- **Aplicación web**: Interfaz moderna accesible desde cualquier dispositivo

## Características

- Interfaz intuitiva para ingresar las preferencias del usuario
- Predicción basada en un árbol de decisión pre-entrenado
- Muestra el programa educativo recomendado junto con un nivel de confianza
- Utiliza datos reales de programas educativos
- Versión web con diseño responsivo accesible desde cualquier dispositivo
- Interfaz moderna y amigable con animaciones y elementos visuales mejorados

## Requisitos

### Para la versión de escritorio
- Python 3.6 o superior
- Bibliotecas: pandas, numpy, tkinter

### Para la versión web
- Python 3.6 o superior
- Bibliotecas: pandas, numpy, Flask, gunicorn, Werkzeug
- Navegador web moderno

## Instalación

### Instalación local

1. Asegúrate de tener Python 3.9 o superior instalado en tu sistema
2. Clona este repositorio o descarga los archivos
3. Instala las bibliotecas necesarias:

```
pip install -r requirements.txt
```

4. Ejecuta la aplicación:

```
python app.py
```

5. Abre tu navegador y visita `http://localhost:5000`

## Opciones de Despliegue

### Despliegue en Render

La aplicación está configurada para ser desplegada en Render.com utilizando el archivo `render.yaml` y el script `build.sh`.

1. Crea una cuenta en [Render](https://render.com)
2. Conecta tu repositorio de GitHub o GitLab
3. Crea un nuevo Web Service con las siguientes configuraciones:
   - **Environment**: Python
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn wsgi:app`
   - **Python Version**: 3.9 (especificado en runtime.txt)

### Despliegue en Vercel

1. Crear una cuenta en [Vercel](https://vercel.com)
2. Instalar Vercel CLI:
   ```
   npm install -g vercel
   ```
3. Iniciar sesión en Vercel:
   ```
   vercel login
   ```
4. Desplegar la aplicación:
   ```
   vercel
   ```
5. Para desplegar a producción:
   ```
   vercel --prod
   ```

## Uso

### Versión web

1. Accede a la aplicación a través de la URL de despliegue o localmente
2. Selecciona tus preferencias en el formulario web
3. Haz clic en el botón "Predecir" para obtener la recomendación
4. El sistema mostrará el programa educativo recomendado junto con un nivel de confianza

## Estructura de archivos

- `app.py`: Servidor Flask que implementa la API y sirve la aplicación web
- `wsgi.py`: Punto de entrada para servidores WSGI
- `arbol_decision.json`: Archivo JSON que contiene el árbol de decisión pre-entrenado
- `programas_educativos.csv`: Base de datos de programas educativos disponibles
- `requirements.txt`: Lista de dependencias del proyecto
- `Procfile`: Archivo de configuración para despliegue en servicios como Heroku
- `vercel.json`: Configuración para despliegue en Vercel
- `render.yaml`: Configuración para despliegue en Render
- `build.sh`: Script de construcción para el despliegue
- `templates/`: Carpeta con las plantillas HTML
  - `index.html`: Página principal de la aplicación web
- `static/`: Carpeta con archivos estáticos
  - `css/styles.css`: Estilos CSS para la interfaz web
  - `js/script.js`: Código JavaScript para la interactividad

## Cómo funciona

El sistema utiliza un árbol de decisión que ha sido previamente entrenado con datos de programas educativos y preferencias de estudiantes. El árbol toma decisiones basadas en las características seleccionadas por el usuario, siguiendo un camino desde la raíz hasta una hoja que representa el programa educativo recomendado.

La confianza de la predicción se calcula en función de la cantidad de muestras de entrenamiento que respaldan esa recomendación.

## Solución de problemas

Si encuentras un error al desplegar la aplicación:

1. Verifica los logs en el dashboard del servicio de hosting
2. Asegúrate de que todos los archivos de datos estén correctamente subidos
3. Verifica que las versiones de las dependencias en requirements.txt sean compatibles
4. Comprueba que la versión de Python especificada en runtime.txt esté disponible en el servicio de hosting