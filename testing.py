import unittest
from app import app, db
from models import User, db

class TestUserModel(unittest.TestCase):
    def test_user_creation(self):
        user = User(username='testuser')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(User.query.count(), 1)

if __name__ == '__main__':
    unittest.main()
