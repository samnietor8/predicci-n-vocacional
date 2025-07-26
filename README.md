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

## Opciones de Despliegue

Existen varias plataformas sencillas donde puedes desplegar esta aplicación de forma gratuita:

### 1. Render (Configuración actual)

Render es una plataforma de nube unificada que facilita el despliegue de aplicaciones web.

1. Crea una cuenta en [Render](https://render.com/)
2. Conecta tu repositorio de GitHub
3. Crea un nuevo servicio web
4. Configura los siguientes campos:
   - **Root Directory**: / (o dejar en blanco)
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn wsgi:app`
   - **Environment Variables**:
     - `PYTHON_VERSION`: 3.9.18
     - `FLASK_APP`: app.py
     - `FLASK_ENV`: production

### 2. GitHub Pages

GitHub Pages es una opción excelente para desplegar la interfaz frontend de la aplicación de forma estática.

1. Asegúrate de tener un repositorio en GitHub
2. Ve a Settings > Pages en tu repositorio
3. Selecciona la rama principal (main o master) como fuente
4. Configura la carpeta /docs o /root según tu estructura
5. GitHub generará automáticamente una URL para tu aplicación (username.github.io/repository)
6. Para aplicaciones dinámicas, puedes configurar la API para que se ejecute en otro servicio

### 3. Railway

Railway es una plataforma que facilita el despliegue de aplicaciones con un flujo de trabajo sencillo.

1. Crea una cuenta en [Railway](https://railway.app/)
2. Conecta tu repositorio de GitHub
3. Railway detectará automáticamente la configuración en `railway.json`
4. Haz clic en "Deploy" y tu aplicación estará en línea en minutos

### 4. Replit

Replit es una plataforma de desarrollo colaborativo en línea que facilita la ejecución de código.

1. Crea una cuenta en [Replit](https://replit.com/)
2. Crea un nuevo repl e importa tu repositorio de GitHub
3. Replit detectará automáticamente la configuración en `.replit`
4. Haz clic en "Run" y tu aplicación estará disponible inmediatamente

### 5. Fly.io

Fly.io es una plataforma para ejecutar aplicaciones y bases de datos cerca de los usuarios.

1. Crea una cuenta en [Fly.io](https://fly.io/)
2. Instala la CLI de Fly: `curl -L https://fly.io/install.sh | sh`
3. Inicia sesión: `fly auth login`
4. Despliega la aplicación: `fly launch`

### 6. Deta Space

Deta Space es una plataforma para construir y desplegar aplicaciones en la nube con un enfoque en la simplicidad.

1. Crea una cuenta en [Deta Space](https://deta.space/)
2. Instala la CLI de Deta: `curl -fsSL https://get.deta.dev/space-cli.sh | sh`
3. Inicia sesión: `space login`
4. Despliega la aplicación: `space push`

### Ejecución local

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