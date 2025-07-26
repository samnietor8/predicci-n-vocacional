# Sistema de Predicción Vocacional

Este sistema utiliza un árbol de decisión para recomendar programas educativos basados en diferentes características del usuario como el tipo de instituto, nivel de formación, campo de estudio y estrato socioeconómico.

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

1. Asegúrate de tener Python instalado en tu sistema
2. Instala las bibliotecas necesarias:

```
pip install -r requirements.txt
```

## Uso

### Versión de escritorio

1. Ejecuta el script `prediccion_vocacional.py`:

```
python prediccion_vocacional.py
```

2. En la interfaz gráfica, selecciona tus preferencias para cada característica
3. Haz clic en el botón "Predecir" para obtener la recomendación
4. El sistema mostrará el programa educativo recomendado junto con un nivel de confianza

### Versión web

1. Ejecuta el servidor Flask:

```
python app.py
```

2. Abre tu navegador y visita `http://localhost:5000`
3. Selecciona tus preferencias en el formulario web
4. Haz clic en el botón "Predecir" para obtener la recomendación
5. El sistema mostrará el programa educativo recomendado junto con un nivel de confianza

### Despliegue en la nube

Para hacer la aplicación accesible desde cualquier dispositivo a través de internet:

1. Crea una cuenta en un servicio de hosting como [Heroku](https://www.heroku.com/), [PythonAnywhere](https://www.pythonanywhere.com/) o [Render](https://render.com/)
2. Sigue las instrucciones del proveedor para desplegar una aplicación Flask
3. Sube los archivos del proyecto al servicio de hosting
4. Configura las variables de entorno necesarias
5. Despliega la aplicación y comparte la URL generada

## Estructura de archivos

### Archivos comunes
- `arbol_decision.json`: Archivo JSON que contiene el árbol de decisión pre-entrenado
- `programas_educativos.csv`: Base de datos de programas educativos disponibles
- `requirements.txt`: Lista de dependencias del proyecto

### Versión de escritorio
- `prediccion_vocacional.py`: Script principal que implementa la interfaz gráfica y el modelo
- `test_prediccion.py`: Script para probar el modelo sin la interfaz gráfica

### Versión web
- `app.py`: Servidor Flask que implementa la API y sirve la aplicación web
- `Procfile`: Archivo de configuración para despliegue en servicios como Heroku
- `templates/`: Carpeta con las plantillas HTML
  - `index.html`: Página principal de la aplicación web
- `static/`: Carpeta con archivos estáticos
  - `css/styles.css`: Estilos CSS para la interfaz web
  - `js/script.js`: Código JavaScript para la interactividad

## Cómo funciona

El sistema utiliza un árbol de decisión que ha sido previamente entrenado con datos de programas educativos y preferencias de estudiantes. El árbol toma decisiones basadas en las características seleccionadas por el usuario, siguiendo un camino desde la raíz hasta una hoja que representa el programa educativo recomendado.

La confianza de la predicción se calcula en función de la cantidad de muestras de entrenamiento que respaldan esa recomendación.

## Limitaciones

- El modelo solo puede recomendar programas educativos que estén incluidos en los datos de entrenamiento
- La precisión de las recomendaciones depende de la calidad y cantidad de los datos de entrenamiento
- El modelo no tiene en cuenta factores personales como habilidades específicas, intereses o aptitudes del estudiante