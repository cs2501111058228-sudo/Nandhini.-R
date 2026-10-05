import os
os.environ["USE_AI"]="false"
os.environ["DATABASE_URL"]="sqlite:///./test_pocketsmart.db"
from fastapi.testclient import TestClient
from app.main import app

def test_health():
    with TestClient(app) as client:
        assert client.get('/health').json()['status'] == 'ok'

def test_register_login_and_home():
    with TestClient(app) as client:
        email='test@example.com'
        r=client.post('/register',json={'name':'Test User','email':email,'password':'secret123'})
        assert r.status_code in (200,409)
        r=client.post('/login',json={'email':email,'password':'secret123'})
        assert r.status_code == 200
        r=client.post('/generate-home',json={'budget':50000,'rooms':['Living Room'],'style':'modern','quantities':{'lights':2},'priorities':['price']})
        assert r.status_code == 200
        data=r.json(); assert data['planner']=='home'; assert data['source']=='fallback'
