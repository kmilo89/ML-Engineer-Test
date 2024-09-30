# test_api.py
from fastapi.testclient import TestClient
from fastapi_image_predictor import app  

client = TestClient(app)

# Prueba básica: la API debe responder con un código 200
def test_predict_success():
    data = {
        "request_id": "123",
        "model": "clf.pickle",
        "image": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAAIAAgBAREA/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oACAEBAAA/AOYitTJ8BgJYkn8tZJ4maMLFEpnC5EhXJnBVh5YYZR884Ar/2Q=="
    }
    response = client.post("/predict/", json=data)
    assert response.status_code == 200
    assert "prediction" in response.json()  # Asegura que 'prediction' está en la respuesta

# Prueba de validación: debe responder con error 400 si falta el campo 'model'
def test_missing_model_field():
    data = {
        "request_id": "123",
        "image": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAAIAAgBAREA/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oACAEBAAA/AOYitTJ8BgJYkn8tZJ4maMLFEpnC5EhXJnBVh5YYZR884Ar/2Q=="
    }
    response = client.post("/predict/", json=data)
    assert response.status_code == 400  # Verifica que el código de estado sea 400
    assert response.json() == {"detail": "Model name is required"}

# Prueba de manejo de excepciones: el modelo no existe
def test_nonexistent_model():
    data = {
        "request_id": "123",
        "model": "model.pickle",
        "image": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAAIAAgBAREA/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oACAEBAAA/AOYitTJ8BgJYkn8tZJ4maMLFEpnC5EhXJnBVh5YYZR884Ar/2Q=="
    }
    response = client.post("/predict/", json=data)
    assert response.status_code == 400  # Verifica que el código de estado sea 400
    assert response.json() == {"detail": "Invalid model name"}