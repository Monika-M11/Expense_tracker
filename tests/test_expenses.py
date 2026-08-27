import uuid




# 1. Test root endpoint

def test_root(client):

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Expense Tracker API is running"
    }


# 2. Test user registration

def test_register(client):
    email = f"{uuid.uuid4()}@gmail.com"
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser123",
            "email": email,
            "password": "test123"
    }
)
    assert response.status_code == 200

  


# 3. Test login

def test_login(client):
    response = client.post(
    "/auth/login",
    data={
        "username": "testuser123@gmail.com",
        "password": "test123"
    }
)

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


# 4. Test unauthorized expense access

def test_get_expenses_without_token(client):

    response = client.get("/expenses")

    assert response.status_code == 401