import unittest
from app import create_app, db  # Import create_app function

class TestItemEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()  # Use create_app function to create the app instance
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_item(self):
        response = self.client.post('/items', json={'name': 'Test Item', 'category_id': 1})
        self.assertEqual(response.status_code, 201)

    def test_update_item(self):
        from app.models import Item  # Import Item inside the test method
        item = Item(name='Test Item', category_id=1)
        with self.app.app_context():
            db.session.add(item)
            db.session.commit()
        
        response = self.client.put('/items/1', json={'name': 'Updated Item'})
        self.assertEqual(response.status_code, 200)

    def test_delete_item(self):
        from app.models import Item  # Import Item inside the test method
        item = Item(name='Test Item', category_id=1)
        with self.app.app_context():
            db.session.add(item)
            db.session.commit()
        
        response = self.client.delete('/items/1')
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(Item.query.get(1))

    def test_get_all_items(self):
        from app.models import Item  # Import Item inside the test method
        with self.app.app_context():
            db.session.add(Item(name='Item 1', category_id=1))
            db.session.add(Item(name='Item 2', category_id=1))
            db.session.commit()
        
        response = self.client.get('/items')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

if __name__ == '__main__':
    unittest.main()
