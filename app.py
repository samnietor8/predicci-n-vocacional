import json
import pandas as pd
import numpy as np
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

# Cargar el árbol de decisión desde el archivo JSON
def cargar_arbol_decision():
    with open('arbol_decision.json', 'r', encoding='utf-8') as file:
        return json.load(file)

# Cargar los datos de programas educativos
def cargar_programas_educativos():
    return pd.read_csv('programas_educativos.csv', sep=';')

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

# Cargar datos al iniciar la aplicación
arbol_json = cargar_arbol_decision()
programas_df = cargar_programas_educativos()
arbol = ArbolDecision(arbol_json)

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
    # Obtener datos del formulario
    datos = request.json
    
    # Convertir a valores numéricos
    caracteristicas = {}
    for caracteristica, valor in datos.items():
        if caracteristica in valores_numericos and valor in valores_numericos[caracteristica]:
            caracteristicas[caracteristica] = valores_numericos[caracteristica][valor]
    
    # Realizar la predicción
    programa_predicho, muestras = arbol.predecir(caracteristicas)
    
    # Calcular la confianza basada en la cantidad de muestras
    confianza = min(muestras / 30 * 100, 100)  # Normalizar a un máximo de 100%
    
    # Devolver resultados
    return jsonify({
        'programa': programa_predicho,
        'confianza': round(confianza, 2)
    })

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)