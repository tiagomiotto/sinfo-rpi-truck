from motorClass import Motor
import unittest2


class TestMotor(unittest2.TestCase):

    def setUp(self):
        self.motor = Motor("test")
        self.motor.setup()


if __name__ == '__main__':
    unittest2.main()
