import unittest, os
from skorovarka.process import process_directory

class TestDirectoryProcessor(unittest.TestCase):

    def setUp(self):
        self.input = os.path.join(os.path.dirname(__file__), 'template_test')
        self.output = os.path.join(os.path.dirname(__file__), 'to_remove')

    def test_dir_processor(self):
        process_directory(
            self.input,
            self.output,
            lambda x, y: "REPL"
        )
        self.assertTrue(
            os.path.exists(os.path.join(self.output, 'subdir', 'subdir.txt')) and \
                os.path.exists(os.path.join(self.output, 'lol.txt'))
        )

    def tearDown(self):
        for root, _, files in os.walk(self.output):
            for file in files:
                os.remove(os.path.join(root,file))
        for root, dirs, _ in os.walk(self.output):
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(self.output)

if __name__ == "__main__":
    unittest.main()
