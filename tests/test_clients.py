import unittest
from flask import Flask
from flask_testing import TestCase
from app import create_app
from app.models import get_db
import json

class ClientstestCase(TestCase):
    def create_app(self):
        return create_app('testing')

    def setUp(self):
        self.db = get_db()
        self.db.execute('CREATE TABLE IF NOT EXISTS clients (dni TEXT PRIMARY KEY, name TEXT, email TEXT, capital FLOAT)')
        self.db.execute('CREATE TABLE IF NOT EXISTS simulaciones (id INTEGER PRIMARY KEY AUTOINCREMENT, dni TEXT, tae FLOAT, plazo INTEGER, cuota FLOAT, importe_total FLOAT, created_at TEXT, updated_at TEXT)')
        self.db.commit()

    def tearDown(self):
        self.db.execute('DROP TABLE IF EXISTS clients')
        self.db.execute('DROP TABLE IF EXISTS simulaciones')
        self.db.commit()

    def test_create_client(self):
        response = self.client.post('/api/clients/', data=json.dumps({
            'name': 'user test',
            'dni': '98174769M',
            'email': 'user.test@example.com',
            'capital': 100000
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Client created successfully', response.json['message'])

    def test_get_clients(self):
        self.db.execute('INSERT INTO clients (dni, name, email, capital) VALUES (?, ?, ?, ?)', ('98174769M', 'user test', 'user.test@example.com', 100000))
        self.db.commit()
        response = self.client.get('/api/clients/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['dni'], '98174769M')

    def test_update_client(self):
        self.db.execute('INSERT INTO clients (dni, name, email, capital) VALUES (?, ?, ?, ?)', ('98174769M', 'user test', 'user.test@example.com', 100000))
        self.db.commit()
        response = self.client.put('/api/clients/98174769M', data=json.dumps({
            'name': 'user test change',
            'email': 'change.test@example.com',
            'capital': 150000
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['nombre'], 'user test change')

    def test_simulate_loan(self):
        self.db.execute('INSERT INTO clients (dni, name, email, capital) VALUES (?, ?, ?, ?)', ('98174769M', 'user test', 'user.test@example.com', 100000))
        self.db.commit()
        response = self.client.post('/api/clients/98174769M/simulation/', data=json.dumps({
            'tae': 3.75,
            'plazo': 15
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        client_data = response.json[0]
        self.assertIn('simulaciones', client_data)
        self.assertGreater(len(client_data['simulaciones']), 0)
        simulation_data = client_data['simulaciones'][0]
        self.assertIn('cuota', simulation_data)
        self.assertIn('importe_total', simulation_data)

if __name__ == '__main__':
    unittest.main()