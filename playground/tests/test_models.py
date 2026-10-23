import unittest

from splitter import Group


class GroupTest(unittest.TestCase):
    def test_add_member(self):
        group = Group("offsite")
        alice = group.add_member("alice")
        self.assertEqual(group.get_member("alice"), alice)

    def test_duplicate_member_rejected(self):
        group = Group("offsite")
        group.add_member("alice")
        with self.assertRaises(ValueError):
            group.add_member("alice")


if __name__ == "__main__":
    unittest.main()
