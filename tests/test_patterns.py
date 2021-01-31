import unittest
from skorovarka.process import replace_token

class TestPatterns(unittest.TestCase):

    def setUp(self):
        self.inputs = [
            "dfasdf asdf|||1:blah blah||| asjdfaisdj |||2:blah jssa|||asdggasdf",
            "dfasdf asdf${1:blah blah} asjdfaisdj ${2:blah jssa}asdggasdf"
        ]
        self.repls = [
            "dfasdf asdfREPL asjdfaisdj REPLasdggasdf",
            "dfasdf asdfREPL asjdfaisdj REPLasdggasdf"
        ]
        return super().setUpClass()
    
    def test_patterns(self):
        for idx, i in enumerate(self.inputs):
            self.assertEqual(
                replace_token(
                    i, 
                    idx,
                    lambda x, y: "REPL",
                    dict(),
                    []
                ),
                self.repls[idx]
            )

if __name__ == "__main__":
    unittest.main()