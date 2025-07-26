from setuptools import setup, find_packages

setup(
    name="prediccion_vocacional",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas",
        "numpy",
        "flask",
        "gunicorn",
        "Werkzeug",
        "python-dotenv",
    ],
)