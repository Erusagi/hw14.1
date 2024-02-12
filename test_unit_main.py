import unittest
from unittest.mock import MagicMock, patch
from main import create_contact, update_user_avatar

class TestMainFunctions(unittest.TestCase):

    def test_create_contact(self):
        contact_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "123456789",
            "birthday": "1990-01-01",
            "additional_info": "Additional information"
        }
        db_mock = MagicMock()
        current_user_mock = MagicMock()

        created_contact = create_contact(contact_data, db_mock, current_user_mock)

        self.assertIsNotNone(created_contact)
        self.assertEqual(created_contact.first_name, contact_data["first_name"])

    def test_update_user_avatar(self):
        avatar_file_mock = MagicMock()
        current_user_mock = MagicMock()

        result = update_user_avatar(avatar_file_mock, current_user_mock)

        self.assertEqual(result, "Avatar updated successfully")

if __name__ == '__main__':
    unittest.main()