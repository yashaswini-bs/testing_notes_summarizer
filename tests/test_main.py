from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check_endpoint():
    """Verify the API is online and responding."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_analyze_empty_notes():
    """Verify the API rejects empty payloads."""
    response = client.post("/api/analyze", json={"notes": ""})
    assert response.status_code == 400
    assert "detail" in response.json()

def test_analyze_non_testing_text():
    """Verify the AI guardrail catches casual text (False Positive Prevention)."""
    payload = {
        "notes": "To make a perfect omelette, whisk three eggs with a splash of milk. Cook on a buttered skillet on medium heat."
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # The AI should flag this as NOT testing notes
    assert data["is_testing_notes"] == False
    assert "rejection_reason" in data

def test_analyze_valid_testing_notes():
    """Verify the API correctly structures valid exploratory testing notes."""
    payload = {
        "notes": "Tested the mobile checkout flow on iOS. Added an item to the cart, but when I tapped 'Pay with Apple Pay', the app crashed immediately to the home screen."
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Validate the Pydantic schema structure
    assert data["is_testing_notes"] == True
    assert "coverage_summary" in data
    assert isinstance(data["bugs"], list)
    assert isinstance(data["open_questions"], list)
    assert isinstance(data["suggested_next_focus"], list)