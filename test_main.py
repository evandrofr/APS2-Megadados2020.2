from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)

def test_read_main_returns_not_found():
 response = client.get('/')
 assert response.status_code == 404
 assert response.json() == {'detail': 'Not Found'}

def test_read_tasks_return_empty_json():
    response = client.get('/task')
    assert response.status_code == 200
    assert response.json() == {}

# def test_create_task_and_delete_it():
#     responsePost = client.post('/task', json={"description": "description", "completed": False})
#     assert responsePost.status_code == 200

#     responseDelete = client.delete(f'/task/{responsePost.json()}')
#     assert responseDelete.json() == None

def test_create_task_get_and_delete_it():
    responsePost = client.post('/task', json={"description": "description", "completed": False})
    assert responsePost.status_code == 200

    responseGet = client.get(f'/task/{responsePost.json()}')
    assert responseGet.json() == {"description": "description", "completed": False}

    responseDelete = client.delete(f'/task/{responsePost.json()}')
    assert responseDelete.json() == None

def test_get_invalue_task():
    uuid_ = uuid.uuid4()
    
    response = client.get(f'/task/{uuid_}')
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_delete_invalue_task():
    uuid_ = uuid.uuid4()
    
    response = client.delete(f'/task/{uuid_}')
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
