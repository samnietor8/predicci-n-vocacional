#!/usr/bin/env bash
# Script de construcción para Render

set -o errexit

echo "Actualizando pip y setuptools..."
pip install --upgrade pip
pip install setuptools==67.8.0 wheel>=0.38.4

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Verificando archivos de datos..."
ls -la

echo "Construcción completada."