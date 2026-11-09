from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock
from main import app

def test_translation_and_validation():
    # Sem lifespan: não baixa pesos nem chama serviços externos.
    app.state.translate = Mock(return_value="Bonjour")
    app.state.translate.invoke = Mock(return_value="Guten Tag")
    app.state.chain = Mock()
    app.state.chain.ainvoke = AsyncMock(return_value="Bonjour")
    client = TestClient(app)
    response = client.post("/translate", json={"text": "Hello"})
    assert response.status_code == 200
    assert response.json()["translation"] == "Bonjour"
    assert response.json()["target_language"] == "fr"
    assert response.json()["source_language"] == "en"
    assert client.post("/translate", json={"text":"   "}).status_code == 422
    assert client.post("/translate", json={}).status_code == 422
