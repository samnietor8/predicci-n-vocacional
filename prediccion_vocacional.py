import json
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox

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

# Clase para la interfaz gráfica
class AplicacionPrediccionVocacional:
    def __init__(self, root):
        self.root = root
        self.root.title("Predicción Vocacional")
        self.root.geometry("800x600")
        
        # Cargar datos
        self.arbol_json = cargar_arbol_decision()
        self.programas_df = cargar_programas_educativos()
        self.arbol = ArbolDecision(self.arbol_json)
        
        # Obtener valores únicos para cada característica
        self.obtener_valores_unicos()
        
        # Crear la interfaz
        self.crear_interfaz()
    
    def obtener_valores_unicos(self):
        # Obtener valores únicos para cada característica del árbol
        self.valores_unicos = {}
        self.valores_numericos = {}
        
        # Características principales del árbol
        caracteristicas = [
            "TIPO DE INSTITUTO", "NIVEL DE FORMACION", "CAMPO AMPLIO", 
            "CAMPO ESPECIFICO", "CAMPO DETALLADO", "Estrato"
        ]
        
        for caracteristica in caracteristicas:
            if caracteristica in self.programas_df.columns:
                valores = self.programas_df[caracteristica].unique()
                self.valores_unicos[caracteristica] = sorted(valores)
                
                # Crear mapeo de valores a números
                encoder = LabelEncoder()
                encoder.fit(valores)
                self.valores_numericos[caracteristica] = {
                    valor: i for i, valor in enumerate(encoder.classes_)
                }
            elif caracteristica == "Estrato":
                # Para el estrato, usar valores del 1 al 6
                self.valores_unicos[caracteristica] = [str(i) for i in range(1, 7)]
                self.valores_numericos[caracteristica] = {
                    str(i): i for i in range(1, 7)
                }
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text="Sistema de Predicción Vocacional", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Frame para los controles
        controles_frame = ttk.Frame(main_frame)
        controles_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Variables para almacenar las selecciones
        self.selecciones = {}
        self.comboboxes = {}
        
        # Crear controles para cada característica
        row = 0
        for caracteristica in ["TIPO DE INSTITUTO", "NIVEL DE FORMACION", "CAMPO AMPLIO", 
                              "CAMPO ESPECIFICO", "CAMPO DETALLADO", "Estrato"]:
            if caracteristica in self.valores_unicos:
                # Etiqueta
                ttk.Label(controles_frame, text=f"{caracteristica}:").grid(row=row, column=0, sticky=tk.W, pady=5, padx=5)
                
                # Variable para almacenar la selección
                self.selecciones[caracteristica] = tk.StringVar()
                
                # Combobox
                combobox = ttk.Combobox(controles_frame, textvariable=self.selecciones[caracteristica], 
                                       values=self.valores_unicos[caracteristica], state="readonly", width=50)
                combobox.grid(row=row, column=1, sticky=tk.W, pady=5, padx=5)
                
                # Almacenar el combobox
                self.comboboxes[caracteristica] = combobox
                
                row += 1
        
        # Botón para predecir
        ttk.Button(main_frame, text="Predecir", command=self.predecir).pack(pady=20)
        
        # Frame para mostrar resultados
        self.resultados_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        self.resultados_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Etiqueta para mostrar la predicción
        self.prediccion_label = ttk.Label(self.resultados_frame, text="", font=("Arial", 12))
        self.prediccion_label.pack(pady=10)
        
        # Etiqueta para mostrar la confianza
        self.confianza_label = ttk.Label(self.resultados_frame, text="", font=("Arial", 10))
        self.confianza_label.pack(pady=5)
    
    def predecir(self):
        # Obtener las características seleccionadas
        caracteristicas = {}
        
        # Verificar que todas las características necesarias estén seleccionadas
        for caracteristica, var in self.selecciones.items():
            valor = var.get()
            if not valor:
                messagebox.showwarning("Datos incompletos", f"Por favor, seleccione un valor para {caracteristica}")
                return
            
            # Convertir a valor numérico
            caracteristicas[caracteristica] = self.valores_numericos[caracteristica][valor]
        
        # Realizar la predicción
        programa_predicho, muestras = self.arbol.predecir(caracteristicas)
        
        # Calcular la confianza basada en la cantidad de muestras
        confianza = min(muestras / 30 * 100, 100)  # Normalizar a un máximo de 100%
        
        # Mostrar resultados
        self.prediccion_label.config(text=f"Programa educativo recomendado: {programa_predicho}")
        self.confianza_label.config(text=f"Confianza: {confianza:.2f}%")

# Función principal
def main():
    root = tk.Tk()
    app = AplicacionPrediccionVocacional(root)
    root.mainloop()

if __name__ == "__main__":
    main()