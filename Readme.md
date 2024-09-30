# API de Clasificación de Imágenes - FastAPI

Esta API permite realizar predicciones de clasificación de imágenes utilizando un modelo de Machine Learning. El usuario puede enviar una imagen codificada en **base64** junto con el nombre del modelo que desea utilizar, y la API devolverá la predicción correspondiente.

## Descripción

El servicio expone un único endpoint de predicción, donde los usuarios pueden enviar imágenes en formato **base64** y recibir una predicción basada en el modelo de Machine Learning especificado. La API está desarrollada en **FastAPI** y containerizada con **Docker**.

## Requisitos

- **Python 3.10** o superior.
- **FastAPI**.
- **Docker** y **Docker Compose**.
- Modelo de clasificación en formato `pickle` (`clf.pickle`).

## Endpoints

### `POST /predict/`

Este es el endpoint que recibe las imágenes y devuelve las predicciones.

- **Método HTTP**: `POST`
- **Descripción**: Procesa una imagen en formato base64 y la predice utilizando el modelo especificado.

#### Parámetros

El cuerpo de la solicitud debe ser un **JSON** con los siguientes campos:

- **`request_id`**: Un identificador único para la solicitud. 
- **`model`**: El nombre del modelo a utilizar para la predicción (por ejemplo, `clf.pickle`).
- **`image`**: La imagen codificada en **base64**.

#### Ejemplo de solicitud:

```json
{
  "request_id": "123",
  "model": "clf.pickle",
  "image": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwc..."
}
```



## Respuesta

La respuesta será un JSON con los siguientes campos:

- **request_id**: El mismo identificador proporcionado en la solicitud, para que el cliente pueda hacer seguimiento de la solicitud.
- **prediction**: El resultado de la predicción realizada por el modelo.

#### Ejemplo de respuesta exitosa:
```json
{
  "request_id": "123e4567-e89b-12d3-a456-426614174000",
  "prediction": 8
}
```
#### Ejemplo de respuesta con error:
Si ocurre algún error en el proceso, se devolverá una respuesta con un código de error y un mensaje explicativo. Por ejemplo, si el modelo especificado no existe:
```json 
{
  "detail": "Invalid model name"
}
```

### Ejecutar server FastAPI sin Docker

```sh
uvicorn fastapi_image_predictor:app --reload
```


## Implementación

### 1. Clonar el repositorio

```sh
git clone https://github.com/kmilo89/ML-Engineer-Test
cd ML-Engineer-Test
```

### 2. Ejecutar el servicio con Docker Compose

Utiliza Docker Compose para levantar el servicio en segundo plano.

```sh
docker-compose up -d
```

### 3. Probar la API

Una vez que el servicio esté corriendo, puedes probar el endpoint usando curl o Postman.

#### Ejemplo de uso con curl:
```sh
curl -X POST "http://127.0.0.1:8000/predict/" -H "Content-Type: application/json" -d '{"request_id": "123", "model": "clf.pickle", "image": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAAIAAgBAREA/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oACAEBAAA/AOYitTJ8BgJYkn8tZJ4maMLFEpnC5EhXJnBVh5YYZR884Ar/2Q=="}'
```

#### Ejemplo de uso con python:

Primero que todo se debe crear y activar entorno virtual con sus dependencias.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Ejecutar archivo python en el entorno virtual.

```python
import requests
import json

url = "http://localhost:8000/predict/"
data = {
    "request_id": "123",
    "model": "clf.pickle",
    "image": "//9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAAIAAgBAREA/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oACAEBAAA/AOYitTJ8BgJYkn8tZJ4maMLFEpnC5EhXJnBVh5YYZR884Ar/2Q=="
}

headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(data), headers=headers)

print(response.json())
```

## Errores comunes

- **400 Bad Request**: Si falta algún campo en la solicitud, la imagen no está correctamente codificada o si el modelo solicitado no está disponible en el servidor.

- **500 Internal Server Error**: Si ocurre un error inesperado durante la predicción o el procesamiento de la imagen.


## Estimación de latencia de al API.

Una forma sencilla de verificar la latencia es usar la función time con curlÑ

```sh
time curl -X POST "http://127.0.0.1:8000/predict/" -H "Content-Type: application/json" -d '{"request_id": "123", "model": "clf.pickle", "image": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAAIAAgBAREA/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oACAEBAAA/AOYitTJ8BgJYkn8tZJ4maMLFEpnC5EhXJnBVh5YYZR884Ar/2Q=="}'
```
La respuesta obtenida es:
```
real    0m0.016s
user    0m0.009s
sys     0m0.005s
```
Donde se observa una latencia de 16ms para completar la predicción. 


# Manejo de Drift y Re-entrenamiento

## Descripción:
Escenario en el cual un modelo de machine learning en producción empieza a perder precisión debido a cambios en los datos de entrada (data drift). La meta es diseñar una estrategia para  detectar y abordar este problema.

Uno de los enfoques que implementaría es el monitoreo constante de la precisión del modelo. De modo que si la precisión disminuye notablemente este sería un indicador clave para detectar el data drift. Otro metodo muy utilizado es la comparación en la distribución de características de los datos en producción con la de los datos de entrenamiento. Si está distribución es muy diferente puede ser un indicio de que se presenta data drift.

Por otra parte, una de las estrategias que se pueden utilizar para el manejo del data drift es el re-entrenamiento utilizando datos nuevos. La idea es que la estrategia incluya un proceso de recolección de nuevos datos y un proceso de re-entrenamiento que se ejecute sin interrumpir el servicio que se encuentra en producción.


## Pipeline Automatizado:

Propuesta para un pipeline automatizado:
- ***Recolectar nuevos datos relevantes para el re-entrenamiento***.

    - Establecer una fuente de datos nuevos y actualizados usando fuentes como los datos de producción, bases de datos, APIs o diversos sistemas que puedan enriquecer esta fuente de datos.
    - Al recolectar los datos es importante realizar una etapa de normalización.

    Los posibles desafíos en esta etapa pueden estar enfocados en el aumento significativo de datos a lo largo del tiempo. También se puede ver afectado por datos de mala calidad.

    Para resolver estos desafíos, se deben tener en cuenta procesos de muestreo en los datos, limpieza continua de la información después de ser procesada y procesos de validación de calidad de los datos.

- ***Re-entrenar el modelo de manera eficiente***.
    - El objetivo principal de esta etapa es que se realice el reentrenamiento del modelo a partir de los datos nuevos recolectados y se valide para asegurar que es mejor que la versión anterior.
    - Establecer un umbral para el almacenamiento de datos, de modo que cuando existan suficientes muestras o en el momento en que se detecte el data drift, se pueda lanzar el proceso de reentrenamiento.
    - Utilizar métricas para la validación del modelo, como la precisión, el recall, el índice F1 score, las tasas de falsos positivos y negativos, entre otras. Alguna métrica que permita comparar y validar el modelo actual con respecto al anterior.

    Algunos de los posibles desafíos en esta etapa pueden ser que los nuevos datos no generen un modelo con un mejor desempeño. También puede suceder que el entrenamiento sea complejo y costoso.

    Para atacar esto, se propone almacenar las diferentes versiones que vayan surgiendo de los reentrenamientos y llevar un seguimiento de las métricas de cada uno de estos modelos. Adicionalmente, para procesos de entrenamiento que pueden llegar a ser complejos, se sugiere considerar sistemas de entrenamiento distribuido implementando servicios en la nube.

- **Desplegar la nueva versión del modelo sin interrumpir el servicio actual**
    - Existen algunos servicios o aplicaciones que pueden ser muy críticos en producción, por lo que detenerlos para lanzar una nueva versión acarrea diversos problemas.
    - Una de las estrategias que destaca para enfrentar este reto es **Blue-Green Deployment**. La idea es que se mantenga en producción la versión actual (blue) mientras se despliega la nueva versión (green). Una parte de los datos de producción se redirige a la nueva versión para validar su desempeño y respuesta. 
    - En el momento en que se detecte un buen funcionamiento, se redirige todo el tráfico y se detiene la versión anterior, todo esto sin interrumpir el servicio.
    
    En esta etapa se pueden presentar desafíos relacionados con una degradación en el desempeño, tiempos de latencia altos, errores de ejecución, entre otros.

    La idea es que se deben plantear estrategias para revertir a la versión anterior sin afectar el servicio a los usuarios de la aplicación.

### Estrategia de ejecución.

Ejecutar cada etapa como servicio separado, utilizar conetendores para encapsular las tareas.

- Un contenedor para el servicio de recolección de datos y la validación del data drift que se ejecute periódicamente.

- Definir si el re-entrenamiento estará extrictamente ligado a la detección del data drift o si se realizara re-entrenamiento constante dependiendo de un umbral de cantidad de nuevos datos. Encapsular este proceso en un contenedor que se encargue del proceso de re-entrenamiento, de validar los resultados y almacenar los modelos.

- Establecer un servicio de validación de los modelos que se encargue de comparar las diferentes versiones del modelo a partir de las metricas de rendimiento.

- Un servicio que despligue el modelo utilizando una plataforma de orquestación como kubernetes.



## Pruebas unitarias

Pruebas unitarias para asegurar el correcto funcionamiento de los endpoints de la API y la validación de entradas.

- **test_predict_success()**: Esta prueba verifica que el endpoint /predict/ funcione correctamente cuando se le proporcionan todos los datos válidos.

- **test_missing_model_field()**: Esta prueba valida el comportamiento de la API cuando falta el campo obligatorio model en la solicitud.

- **test_nonexistent_model()**: Esta prueba asegura que la API maneje correctamente el caso en que se proporciona un nombre de modelo que no existe.

### Ejecución de las pruebas

Para ejecutar las pruebas unitarias, utiliza el siguiente comando en la terminal dentro del entorno virtual:
```sh
pytest
```


## GCP

La API ha sido desplegada en Google Cloud Run y está disponible públicamente en la siguiente URL:

Service URL: https://predictor-app-447383300663.us-central1.run.app

### Endpoints Disponibles

POST /predict/
Este es el endpoint principal para realizar predicciones basadas en imágenes codificadas en base64.

URL: https://predictor-app-447383300663.us-central1.run.app/predict

#### Ejemplo de solicitud
```sh 
curl -X POST "https://predictor-app-447383300663.us-central1.run.app/predict/" -H "Co:tent-Type: application/json" -d '{"request_id": "123", "model": "clf.pickle", "image": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAAIAAgBAREA/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oACAEBAAA/AOYitTJ8BgJYkn8tZJ4maMLFEpnC5EhXJnBVh5YYZR884Ar/2Q=="}'
```