def test_create_task(client, auth_headers):
    r = client.post("/tasks", json={"title":"Buy milk"}, headers=auth_headers)
    assert r.status_code == 201
    assert r.json()["title"] == "Buy milk"

def test_list_tasks(client, auth_headers):
    client.post("/tasks", json={"title":"Task 1"}, headers=auth_headers)
    r = client.get("/tasks", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["total"] == 1

def test_filter_completed(client, auth_headers):
    tid = client.post("/tasks", json={"title":"T"}, headers=auth_headers).json()["id"]
    client.put(f"/tasks/{tid}", json={"completed": True}, headers=auth_headers)
    r = client.get("/tasks?completed=true", headers=auth_headers)
    assert r.json()["total"] == 1
    r2 = client.get("/tasks?completed=false", headers=auth_headers)
    assert r2.json()["total"] == 0

def test_complete_task(client, auth_headers):
    task_id = client.post("/tasks", json={"title":"T"}, headers=auth_headers).json()["id"]
    r = client.put(f"/tasks/{task_id}", json={"completed": True}, headers=auth_headers)
    assert r.json()["completed"] is True

def test_delete_task(client, auth_headers):
    task_id = client.post("/tasks", json={"title":"T"}, headers=auth_headers).json()["id"]
    r = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert r.status_code == 204

def test_cannot_access_other_users_task(client, auth_headers):
    task_id = client.post("/tasks", json={"title":"Private"}, headers=auth_headers).json()["id"]
    client.post("/auth/register", json={"username":"bob","email":"bob@b.com","password":"pass123"})
    token = client.post("/auth/login", json={"username":"bob","password":"pass123"}).json()["access_token"]
    r = client.get(f"/tasks/{task_id}", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 404

def test_pagination(client, auth_headers):
    for i in range(5):
        client.post("/tasks", json={"title": f"Task {i}"}, headers=auth_headers)
    r = client.get("/tasks?page=1&page_size=3", headers=auth_headers)
    assert len(r.json()["tasks"]) == 3
    assert r.json()["total"] == 5
