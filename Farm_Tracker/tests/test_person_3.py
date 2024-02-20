# test_person_3.py

import unittest
from app import app, db
from models import Item, Category

class TestItemEndpoints(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_item(self):
        response = self.app.post('/items', json={'name': 'Test Item', 'category_id': 1})
        self.assertEqual(response.status_code, 201)

    def test_update_item(self):
        item = Item(name='Test Item', category_id=1)
        with app.app_context():
            db.session.add(item)
            db.session.commit()
        
        response = self.app.put('/items/1', json={'name': 'Updated Item'})
        self.assertEqual(response.status_code, 200)

    def test_delete_item(self):
        item = Item(name='Test Item', category_id=1)
        with app.app_context():
            db.session.add(item)
            db.session.commit()
        
        response = self.app.delete('/items/1')
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(Item.query.get(1))

    def test_get_all_items(self):
        with app.app_context():
            db.session.add(Item(name='Item 1', category_id=1))
            db.session.add(Item(name='Item 2', category_id=1))
            db.session.commit()
        
        response = self.app.get('/items')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

if __name__ == '__main__':
    unittest.main()
