import json
import pandas as pd
from prediccion_vocacional import ArbolDecision, cargar_arbol_decision, cargar_programas_educativos, LabelEncoder

def main():
    # Cargar el árbol de decisión y los programas educativos
    arbol_json = cargar_arbol_decision()
    programas_df = cargar_programas_educativos()
    
    # Crear el modelo de árbol de decisión
    arbol = ArbolDecision(arbol_json)
    
    # Crear encoders para cada característica
    encoders = {}
    for caracteristica in ["TIPO DE INSTITUTO", "NIVEL DE FORMACION", "CAMPO AMPLIO", 
                         "CAMPO ESPECIFICO", "CAMPO DETALLADO"]:
        if caracteristica in programas_df.columns:
            encoder = LabelEncoder()
            encoder.fit(programas_df[caracteristica].unique())
            encoders[caracteristica] = encoder
    
    # Ejemplo de características para probar el modelo
    ejemplos = [
        {
            "TIPO DE INSTITUTO": "publica",
            "NIVEL DE FORMACION": "universitario",
            "CAMPO AMPLIO": "ingenieria, industria y construccion",
            "CAMPO ESPECIFICO": "ingenieria y profesiones afines",
            "CAMPO DETALLADO": "electronica y automatizacion",
            "Estrato": 2
        },
        {
            "TIPO DE INSTITUTO": "privada",
            "NIVEL DE FORMACION": "tecnologico",
            "CAMPO AMPLIO": "administracion de empresas y derecho",
            "CAMPO ESPECIFICO": "educacion comercial y administracion",
            "CAMPO DETALLADO": "gestion y administracion",
            "Estrato": 3
        },
        {
            "TIPO DE INSTITUTO": "publica",
            "NIVEL DE FORMACION": "universitario",
            "CAMPO AMPLIO": "educacion",
            "CAMPO ESPECIFICO": "educacion",
            "CAMPO DETALLADO": "ciencias de la educacion",
            "Estrato": 1
        }
    ]
    
    # Convertir características a valores numéricos
    ejemplos_numericos = []
    for ejemplo in ejemplos:
        ejemplo_numerico = {}
        for caracteristica, valor in ejemplo.items():
            if caracteristica in encoders:
                # Convertir a valor numérico usando el encoder
                try:
                    ejemplo_numerico[caracteristica] = encoders[caracteristica].transform([valor])[0]
                except:
                    # Si el valor no está en el encoder, usar un valor por defecto
                    ejemplo_numerico[caracteristica] = 0
            elif caracteristica == "Estrato":
                # Para el estrato, usar el valor directamente
                ejemplo_numerico[caracteristica] = int(valor)
            else:
                ejemplo_numerico[caracteristica] = 0
        ejemplos_numericos.append(ejemplo_numerico)
    
    # Realizar predicciones para cada ejemplo
    print("\n===== PRUEBA DEL MODELO DE PREDICCIÓN VOCACIONAL =====\n")
    for i, (ejemplo, ejemplo_numerico) in enumerate(zip(ejemplos, ejemplos_numericos)):
        print(f"\nEjemplo {i+1}:")
        print("Características:")
        for caracteristica, valor in ejemplo.items():
            print(f"  - {caracteristica}: {valor}")
        
        # Realizar la predicción
        programa_predicho, muestras = arbol.predecir(ejemplo_numerico)
        
        # Calcular la confianza
        confianza = min(muestras / 30 * 100, 100)  # Normalizar a un máximo de 100%
        
        print("\nResultado:")
        print(f"  - Programa educativo recomendado: {programa_predicho}")
        print(f"  - Confianza: {confianza:.2f}%")
        print("\n" + "-"*50)

if __name__ == "__main__":
    main()