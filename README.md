# Proyecto Finanzas

Este repositorio contiene un proyecto de análisis de datos para el trabajo práctico de finanzas.

## Estructura del proyecto

- `main.py` - Script principal de ejecución.
- `requirements.txt` - Lista de librerías necesarias.
- `data/` - Carpeta con los datos del proyecto.
- `src/` - Código fuente del proyecto.
- `TPfundamentosDatos Entregable.ipynb` - Notebook de entrega.

## Instrucciones de instalación 

1. Descarga o clona el proyecto en tu equipo.
2. Asegúrate de que todas las carpetas y archivos del proyecto estén en la misma carpeta raíz del proyecto.
3. Abre una terminal en la carpeta raíz del proyecto, donde se encuentra `requirements.txt`.

## Crear el ambiente virtual

En Windows PowerShell:

```powershell o CMD
python -m venv .env-finanzas
```

Esto creará una carpeta `.env-finanzas` dentro de la carpeta del proyecto.

## Activar el ambiente virtual

En PowerShell:

```powershell
.\.env-finanzas\Scripts\Activate.ps1
```

En CMD:

```cmd
.env-finanzas\Scripts\activate
```

## Instalar dependencias

Con el ambiente virtual activado, ejecuta:

```powershell o CMD
pip install -r requirements.txt
```

## Ejecutar el proyecto

Una vez instalado todo, puedes ejecutar el script principal:

```powershell o CMD
python main.py
```

> Nota: Si tu proyecto depende del notebook u otros scripts, asegúrate de usar el entorno virtual activado y de que los archivos estén en la carpeta raíz del proyecto. Antes del path deberia aparecer el nombre del ambiente entre parentesis indicando que se encuentra activo.

## Requisitos

El archivo `requirements.txt` contiene las siguientes librerías:

- contourpy==1.3.2
- cycler==0.12.1
- fonttools==4.63.0
- joblib==1.5.3
- kiwisolver==1.5.0
- matplotlib==3.10.9
- numpy==2.2.6
- packaging==26.2
- pandas==2.3.3
- pillow==12.2.0
- pyparsing==3.3.2
- python-dateutil==2.9.0.post0
- pytz==2026.2
- scikit-learn==1.7.2
- scipy==1.15.3
- seaborn==0.13.2
- six==1.17.0
- threadpoolctl==3.6.0
- tzdata==2026.2
