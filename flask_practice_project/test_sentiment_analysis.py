import unittest
from SentimentAnalysis.sentiment_analysis import sentiment_analyzer

class TestSentimentAnalysis(unittest.TestCase):
    def test_sentiment_analyzer(self):
        positive_result = sentiment_analyzer("great news")
        self.assertEqual(positive_result['label'], 'SENT_POSITIVE')

        neutral_result = sentiment_analyzer("nothing special happened")
        self.assertEqual(neutral_result['label'], 'SENT_NEUTRAL')

        negative_result = sentiment_analyzer("bad news")
        self.assertEqual(negative_result['label'], 'SENT_NEGATIVE')


if __name__ == "__main__":
    unittest.main()