import unittest
from skorovarka.process import try_get_lines

class TestProcess(unittest.TestCase):

    def test_try_get_lines(self):

        inputs = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        def case1(self):
            pre, curr, post = try_get_lines(
                inputs,
                3,
                4,
                4
            )

            self.assertListEqual(pre, [0, 1, 2])
            self.assertEqual(curr, 3)
            self.assertListEqual(post, [4, 5, 6, 7])

        def case2(self):
            pre, curr, post = try_get_lines(
                inputs,
                6,
                4,
                4
            )

            self.assertListEqual(pre, [2, 3, 4, 5])
            self.assertEqual(curr, 6)
            self.assertListEqual(post, [7, 8, 9])

        def case3(self):
            pre, curr, post = try_get_lines(
                inputs,
                6,
                2,
                2
            )

            self.assertListEqual(pre, [4, 5])
            self.assertEqual(curr, 6)
            self.assertListEqual(post, [7, 8])
        
        case1(self)
        case2(self)
        case3(self)
        


if __name__ == "__main__":
    unittest.main()