import unittest
from codeblog.models import User,Comment

class User_Model_Test(unittest.TestCase):
    def setUp(self):
        self.new_user = User(password = '12321')
    
    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password
    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('12321'))

class Comments_Model_Test(unittest.TestCase):
    def setUp(self):
           self.new_comment = Comment(id=1, user_id = 1, comment = 'testc',blog_id = '5',date_posted='2022-04-17')
    def test_comment_variables(self):
       self.assertEquals(self.new_comment.comment,'testc')
       self.assertEquals(self.new_comment.date_posted,'2022-04-17')
       self.assertEquals(self.new_comment.user_id, 1)
    def test_save_comment(self):
        self.assertTrue(len(Comment.query.all())>0)
        
