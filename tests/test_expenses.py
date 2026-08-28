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

    email = f"{uuid.uuid4()}@gmail.com"

    # Register user
    register_response = client.post(
        "/auth/register",
        json={
            "username": "testuser123",
            "email": email,
            "password": "test123"
        }
    )

    assert register_response.status_code == 200

    # Login
    response = client.post(
        "/auth/login",
        data={
            "username": email,
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


#5 Report
# 5. Test expense summary

def test_expense_summary(client):

    email = f"{uuid.uuid4()}@gmail.com"

    # Register user
    register_response = client.post(
        "/auth/register",
        json={
            "username": "summaryuser",
            "email": email,
            "password": "test123"
        }
    )

    assert register_response.status_code == 200

    # Login to get JWT
    login_response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "test123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Call summary API using JWT
    response = client.get(
        "/reports/summary",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "user_id" in data
    assert "total_expense" in data
    assert "expense_count" in data