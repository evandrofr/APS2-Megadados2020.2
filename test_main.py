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

def test_get_invalid_task():
    uuid_ = uuid.uuid4()
    
    response = client.get(f'/task/{uuid_}')
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_delete_invalid_task():
    uuid_ = uuid.uuid4()
    
    response = client.delete(f'/task/{uuid_}')
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_read_all_tasks():
    responsePost1 = client.post('/task', json={"description": "description1", "completed": False})
    assert responsePost1.status_code == 200

    responsePost2 = client.post('/task', json={"description": "description2", "completed": True})
    assert responsePost2.status_code == 200

    responsePost3 = client.post('/task', json={"description": "description3", "completed": False})
    assert responsePost3.status_code == 200

    responseGet = client.get('/task')
    assert responseGet.status_code == 200
    assert responseGet.json() == {
        responsePost1.json(): {
            "description": "description1",
            "completed": False,
        },
        responsePost2.json(): {
            "description": "description2",
            "completed": True,
        },
        responsePost3.json(): {
            "description": "description3",
            "completed": False,
        },
    }
    responseDelete1 = client.delete(f"/task/{responsePost1.json()}")
    assert responseDelete1.status_code == 200
    assert responseDelete1.json() == None
    responseDelete2 = client.delete(f"/task/{responsePost2.json()}")
    assert responseDelete2.status_code == 200
    assert responseDelete2.json() == None
    responseDelete3 = client.delete(f"/task/{responsePost3.json()}")
    assert responseDelete3.status_code == 200
    assert responseDelete3.json() == None

def test_patch_invalid_task():
    uuid_ = uuid.uuid4()
    response = client.patch(f"/task/{uuid_}", json={"description": "description", "completed": False })
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_patch_valid_task():
    responsePost = client.post(
        "/task", json={"description": "description1", "completed": False }
    )
    assert responsePost.status_code == 200

    responsePatch = client.patch(
        f"/task/{responsePost.json()}",
        json={"description": "description2", "completed": True },
    )
    assert responsePatch.status_code == 200
    assert responsePatch.json() == None

    responseGet = client.get(f"/task/{responsePost.json()}")
    assert responseGet.status_code == 200
    assert responseGet.json() == {
        "description": "description2",
        "completed": True,
    }

    responseDelete = client.delete(f"/task/{responsePost.json()}")
    assert responseDelete.status_code == 200
    assert responseDelete.json() == None


def test_put_valid_task():

    responsePost = client.post("/task", json={"description": "description1", "completed": True })
    assert responsePost.status_code == 200

    responsePut = client.put(f"/task/{responsePost.json()}",json={"description": "description2", "completed": False },)
    assert responsePut.status_code == 200
    assert responsePut.json() == None

    responseGet = client.get(f"/task/{responsePost.json()}")
    assert responseGet.status_code == 200
    assert responseGet.json() == { "description": "description2", "completed": False }

    responseDelete = client.delete(f"/task/{responsePost.json()}")
    assert responseDelete.status_code == 200
    assert responseDelete.json() == None

