def test_register(client):
    r = client.post("/auth/register", json={"username":"alice","email":"alice@example.com","password":"pass123"})
    assert r.status_code == 201
    assert r.json()["username"] == "alice"

def test_register_duplicate(client, registered_user):
    r = client.post("/auth/register", json={"username":"testuser","email":"x@x.com","password":"pass123"})
    assert r.status_code == 400

def test_login(client, registered_user):
    r = client.post("/auth/login", json=registered_user)
    assert r.status_code == 200
    assert "access_token" in r.json()

def test_login_wrong_password(client, registered_user):
    r = client.post("/auth/login", json={"username":"testuser","password":"wrong"})
    assert r.status_code == 401
