#!/usr/bin/env bash
# Script de construcción para Render

set -o errexit

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Verificando archivos de datos..."
ls -la

echo "Construcción completada."