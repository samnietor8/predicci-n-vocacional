import json
import pandas as pd
import numpy as np
import os
import logging
from flask import Flask, render_template, request, jsonify

# Clase para simular LabelEncoder de sklearn
class LabelEncoder:
    def __init__(self):
        self.classes_ = []
        self.mapping_ = {}
    
    def fit(self, y):
        self.classes_ = sorted(set(y))
        self.mapping_ = {val: i for i, val in enumerate(self.classes_)}
        return self
    
    def transform(self, y):
        return [self.mapping_.get(item, -1) for item in y]

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

# Cargar el árbol de decisión desde el archivo JSON
def cargar_arbol_decision():
    try:
        # Obtener la ruta absoluta del archivo
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_archivo = os.path.join(ruta_base, 'arbol_decision.json')
        logging.info(f"Intentando cargar árbol de decisión desde: {ruta_archivo}")
        
        with open(ruta_archivo, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error al cargar el árbol de decisión: {str(e)}")
        raise

# Cargar los datos de programas educativos
def cargar_programas_educativos():
    try:
        # Obtener la ruta absoluta del archivo
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_archivo = os.path.join(ruta_base, 'programas_educativos.csv')
        logging.info(f"Intentando cargar programas educativos desde: {ruta_archivo}")
        
        return pd.read_csv(ruta_archivo, sep=';')
    except Exception as e:
        logging.error(f"Error al cargar los programas educativos: {str(e)}")
        raise

# Clase para implementar el árbol de decisión manualmente
class ArbolDecision:
    def __init__(self, modelo_json):
        self.modelo = modelo_json
    
    def predecir(self, caracteristicas):
        nodo_actual = self.modelo
        
        # Recorrer el árbol hasta llegar a una hoja (clase)
        while 'class' not in nodo_actual:
            nombre_caracteristica = nodo_actual['name']
            umbral = nodo_actual['threshold']
            
            # Si la característica no está en el diccionario, usar un valor por defecto
            if nombre_caracteristica not in caracteristicas:
                valor = 0
            else:
                valor = caracteristicas[nombre_caracteristica]
            
            # Decidir si ir a la izquierda o derecha
            if valor <= umbral:
                nodo_actual = nodo_actual['left']
            else:
                nodo_actual = nodo_actual['right']
        
        # Devolver la clase (programa educativo) y la cantidad de muestras
        return nodo_actual['class'], nodo_actual['samples']

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configurar manejo de errores
@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Error del servidor: {error}')
    return jsonify(error="Error interno del servidor. Por favor, contacta al administrador."), 500

@app.errorhandler(404)
def not_found(error):
    app.logger.error(f'Página no encontrada: {error}')
    return jsonify(error="Página no encontrada"), 404

# Cargar datos al iniciar la aplicación
try:
    app.logger.info("Iniciando carga de datos...")
    arbol_json = cargar_arbol_decision()
    programas_df = cargar_programas_educativos()
    arbol = ArbolDecision(arbol_json)
    app.logger.info("Datos cargados correctamente")
except Exception as e:
    app.logger.error(f"Error al cargar los datos iniciales: {str(e)}")

# Obtener valores únicos para cada característica
def obtener_valores_unicos():
    # Obtener valores únicos para cada característica del árbol
    valores_unicos = {}
    valores_numericos = {}
    
    # Características principales del árbol
    caracteristicas = [
        "TIPO DE INSTITUTO", "NIVEL DE FORMACION", "CAMPO AMPLIO", 
        "CAMPO ESPECIFICO", "CAMPO DETALLADO", "Estrato"
    ]
    
    for caracteristica in caracteristicas:
        if caracteristica in programas_df.columns:
            valores = programas_df[caracteristica].unique()
            valores_unicos[caracteristica] = sorted(valores.tolist())
            
            # Crear mapeo de valores a números
            encoder = LabelEncoder()
            encoder.fit(valores)
            valores_numericos[caracteristica] = {
                valor: i for i, valor in enumerate(encoder.classes_)
            }
        elif caracteristica == "Estrato":
            # Para el estrato, usar valores del 1 al 6
            valores_unicos[caracteristica] = [str(i) for i in range(1, 7)]
            valores_numericos[caracteristica] = {
                str(i): i for i in range(1, 7)
            }
    
    return valores_unicos, valores_numericos

# Obtener los valores únicos y numéricos
valores_unicos, valores_numericos = obtener_valores_unicos()

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html', valores_unicos=valores_unicos)

# Ruta para realizar la predicción
@app.route('/predecir', methods=['POST'])
def predecir():
    try:
        # Obtener datos del formulario
        datos = request.json
        app.logger.info(f"Datos recibidos: {datos}")
        
        # Convertir a valores numéricos
        caracteristicas = {}
        for caracteristica, valor in datos.items():
            if caracteristica in valores_numericos and valor in valores_numericos[caracteristica]:
                caracteristicas[caracteristica] = valores_numericos[caracteristica][valor]
        
        app.logger.info(f"Características procesadas: {caracteristicas}")
        
        # Realizar la predicción
        programa_predicho, muestras = arbol.predecir(caracteristicas)
        
        # Calcular la confianza basada en la cantidad de muestras
        confianza = min(muestras / 30 * 100, 100)  # Normalizar a un máximo de 100%
        
        # Devolver resultados
        return jsonify({
            'programa': programa_predicho,
            'confianza': round(confianza, 2)
        })
    except Exception as e:
        app.logger.error(f"Error en la predicción: {str(e)}")
        return jsonify(error=f"Error al procesar la predicción: {str(e)}"), 500

# Ejecutar la aplicación
if __name__ == "__main__":
    # En desarrollo local
    app.run(debug=True)
else:
    # En producción (Render)
    # Asegurarse de que los archivos de datos estén disponibles
    try:
        app.logger.info("Verificando archivos en producción...")
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        app.logger.info(f"Directorio base: {ruta_base}")
        app.logger.info(f"Contenido del directorio: {os.listdir(ruta_base)}")
    except Exception as e:
        app.logger.error(f"Error al verificar archivos: {str(e)}")