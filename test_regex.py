import unittest
import re

with open('arxivbot.py', 'r') as f:
    mod = f.readlines()
    regex_expr = mod[6].split("'")[1]


class TestRegexExpressionOneMatch(unittest.TestCase):
    def setUp(self):
        self.r = re.compile(regex_expr)
        self.match = "https://arxiv.org/abs/1109.3195"
    def test_single_url(self):
        text = "https://arxiv.org/abs/1109.3195"
        self.assertEqual(self.r.search(text).group(), self.match)
    def test_single_url_period(self):
        text = "https://arxiv.org/abs/1109.3195."
        self.assertEqual(self.r.search(text).group(), self.match)
    def test_single_url_inside_text(self):
        text = "Hey! Check this paper: https://arxiv.org/abs/1109.3195. What do you think?"
        self.assertEqual(self.r.search(text).group(), self.match)
    def test_single_url_multiple_lines(self):
        text = "\nhttps://arxiv.org/abs/1109.3195\n\n"
        self.assertEqual(self.r.search(text).group(), self.match)
    def test_single_url_parenthesis(self):
        text = "This paper (https://arxiv.org/abs/1109.3195) looks interesting."
        self.assertEqual(self.r.search(text).group(), self.match)

class TestRegexExpressionOldURLs(unittest.TestCase):
    def setUp(self):
        self.r = re.compile(regex_expr)
    def test_quant_ph(self):
        text = "https://arxiv.org/abs/quant-ph/0512258"
        self.assertEqual(self.r.search(text).group(), text)
    def test_hep_ex(self):
        text = "https://arxiv.org/abs/hep-ex/0102001"
        self.assertEqual(self.r.search(text).group(), text)
    def test_math_ph(self):
        text = "https://arxiv.org/abs/math-ph/9810001"
        self.assertEqual(self.r.search(text).group(), text)
    def test_cs(self):
        text = "https://arxiv.org/abs/cs/9902001"
        self.assertEqual(self.r.search(text).group(), text)

class TestRegexExpressionMultipleMatches(unittest.TestCase):
    def setUp(self):
        self.r = re.compile(regex_expr)
        self.matches = ["https://arxiv.org/abs/quant-ph/0512258", "https://arxiv.org/abs/quant-ph/9806051",
                        "https://arxiv.org/abs/0810.4372", "https://arxiv.org/abs/quant-ph/9810080"]
    def test_multiple_matches_simple(self):
        text = "https://arxiv.org/abs/quant-ph/0512258 https://arxiv.org/abs/quant-ph/9806051 "\
             + "https://arxiv.org/abs/0810.4372 https://arxiv.org/abs/quant-ph/9810080"
        self.assertEqual(self.r.findall(text), self.matches)
    def test_multiple_matches_no_spaces(self):
        text = "https://arxiv.org/abs/quant-ph/0512258https://arxiv.org/abs/quant-ph/9806051"\
             + "https://arxiv.org/abs/0810.4372https://arxiv.org/abs/quant-ph/9810080"
        self.assertEqual(self.r.findall(text), self.matches)
    def test_multiple_matches_paragraph(self):
        text = """https://arxiv.org/abs/quant-ph/0512258. Also, did you read this (https://arxiv.org/abs/quant-ph/9806051)?
        And what about this other one: https://arxiv.org/abs/0810.4372
        https://arxiv.org/abs/quant-ph/9810080"""
        self.assertEqual(self.r.findall(text), self.matches)


if __name__ == '__main__':
    unittest.main()
