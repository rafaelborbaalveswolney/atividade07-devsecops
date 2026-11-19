import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class APITests(unittest.TestCase):
    def test_health(self):
        r = client.get("/health")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {"status": "ok"})
        self.assertEqual(r.headers["x-content-type-options"], "nosniff")

    def test_echo(self):
        self.assertEqual(client.post("/echo", json={"texto": "oi"}).json(), {"resposta": "oi"})

    def test_echo_invalido(self):
        self.assertEqual(client.post("/echo", json={"texto": ""}).status_code, 422)


if __name__ == "__main__":
    unittest.main()
