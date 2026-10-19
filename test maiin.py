
import unittest

from main import (
    EmailNotification,
    SMSNotification,
    WhatsAppNotification,
    NotificationStatus,
    NotificationService,
)


class TestNotificationSystem(unittest.TestCase):

    def setUp(self):
        self.service = NotificationService()

    def test_1_create_email_notification(self):
        notification = self.service.add_notification(
            "email", "zoha@example.com", "Hello"
        )
        self.assertIsInstance(notification, EmailNotification)

    def test_2_create_sms_notification(self):
        notification = self.service.add_notification(
            "sms", "+923001234567", "Hello"
        )
        self.assertIsInstance(notification, SMSNotification)

    def test_3_create_whatsapp_notification(self):
        notification = self.service.add_notification(
            "whatsapp", "+923001234567", "Hello"
        )
        self.assertIsInstance(notification, WhatsAppNotification)

    def test_4_reject_invalid_channel(self):
        with self.assertRaises(ValueError):
            self.service.add_notification(
                "telegram", "zoha@example.com", "Hello"
            )

    def test_5_reject_empty_message(self):
        with self.assertRaises(ValueError):
            self.service.add_notification(
                "email", "zoha@example.com", "   "
            )

    def test_6_send_valid_email(self):
        notification = self.service.add_notification(
            "email", "zoha@example.com", "Hello"
        )
        result = self.service.send_notification(notification.notification_id)
        self.assertTrue(result)
        self.assertEqual(notification.status, NotificationStatus.SENT)

    def test_7_invalid_recipient_fails(self):
        notification = self.service.add_notification(
            "email", "invalid-email", "Hello"
        )
        result = self.service.send_notification(notification.notification_id)
        self.assertFalse(result)
        self.assertEqual(notification.status, NotificationStatus.FAILED)

    def test_8_retry_failed_notification(self):
        notification = self.service.add_notification(
            "email", "zoha@example.com", "Hello", fail_attempts=1
        )
        self.assertFalse(
            self.service.send_notification(notification.notification_id)
        )
        self.assertTrue(
            self.service.retry_notification(notification.notification_id)
        )
        self.assertEqual(notification.status, NotificationStatus.SENT)

    def test_9_reject_retry_when_not_failed(self):
        notification = self.service.add_notification(
            "email", "zoha@example.com", "Hello"
        )
        self.service.send_notification(notification.notification_id)
        with self.assertRaises(ValueError):
            self.service.retry_notification(notification.notification_id)

    def test_10_notification_history(self):
        notification = self.service.add_notification(
            "email", "zoha@example.com", "Hello"
        )
        self.service.send_notification(notification.notification_id)
        history = self.service.get_history(notification.notification_id)
        self.assertGreaterEqual(len(history), 2)
        self.assertIn("sent successfully", history[-1])

    def test_11_notification_ids_are_unique(self):
        first = self.service.add_notification(
            "email", "a@example.com", "First"
        )
        second = self.service.add_notification(
            "email", "b@example.com", "Second"
        )
        self.assertNotEqual(first.notification_id, second.notification_id)


if __name__ == "__main__":
    unittest.main()
