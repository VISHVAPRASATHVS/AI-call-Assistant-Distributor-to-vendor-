import re
import time


class SentimentAgent:
    """Agent 2: Analyzes emotional tone of calls — rule-based with negation & intensifier awareness."""

    NAME = "SentimentAgent"

    POSITIVE = [
        'great', 'good', 'excellent', 'amazing', 'fantastic', 'wonderful', 'happy', 'thank',
        'appreciate', 'pleased', 'satisfied', 'excited', 'looking forward', 'success', 'love',
        'perfect', 'helpful', 'impressive', 'best', 'growth', 'opportunity', 'committed',
        'partnership', 'trust', 'confident', 'productive', 'efficient', 'resolved', 'improved',
        'positive', 'smooth', 'support', 'proud', 'glad', 'delighted', 'thrilled', 'awesome',
    ]
    NEGATIVE = [
        'bad', 'terrible', 'awful', 'horrible', 'hate', 'angry', 'frustrated', 'problem',
        'issue', 'bug', 'broken', 'fail', 'failure', 'disappointed', 'slow', 'delay', 'unclear',
        'confused', 'concern', 'worry', 'difficult', 'complicated', 'stuck', 'blocked', 'wrong',
        'incorrect', 'missing', 'lack', 'unable', 'cannot', 'trouble', 'challenge', 'complaint',
        'unacceptable', 'poor', 'worse', 'losing', 'lost', 'critical', 'urgent', 'serious',
        'no reply', 'unanswered', 'ignored', 'neglected', 'overdue', 'unprofessional',
    ]
    INTENSIFIERS = {'very', 'extremely', 'really', 'absolutely', 'completely', 'totally', 'so'}
    NEGATORS = {"not", "no", "never", "don't", "doesn't", "isn't", "aren't", "wasn't", "won't"}

    def analyze(self, text: str) -> dict:
        t0 = time.time()
        tl = text.lower()
        words = re.findall(r"\b[\w']+\b", tl)
        pos, neg = 0, 0
        pos_phrases, neg_phrases = [], []

        for i, word in enumerate(words):
            negated = i > 0 and words[i - 1] in self.NEGATORS
            weight = 2 if i > 0 and words[i - 1] in self.INTENSIFIERS else 1

            if any(pw == word or (len(pw) > 4 and pw in tl) for pw in self.POSITIVE):
                if negated:
                    neg += weight
                else:
                    pos += weight
                    ctx = tl[max(0, tl.find(word) - 15): tl.find(word) + len(word) + 20].strip()
                    if ctx and ctx not in pos_phrases:
                        pos_phrases.append(ctx)

            if any(nw == word or (len(nw) > 4 and nw in tl) for nw in self.NEGATIVE):
                if negated:
                    pos += weight
                else:
                    neg += weight
                    ctx = tl[max(0, tl.find(word) - 15): tl.find(word) + len(word) + 20].strip()
                    if ctx and ctx not in neg_phrases:
                        neg_phrases.append(ctx)

        total = pos + neg
        score = (pos / total) if total > 0 else 0.5
        overall = 'Positive' if score >= 0.65 else ('Negative' if score <= 0.35 else 'Neutral')

        return {
            'overall': overall,
            'score': round(score, 3),
            'positive_count': pos,
            'negative_count': neg,
            'positive_phrases': pos_phrases[:3],
            'negative_phrases': neg_phrases[:3],
            'duration_ms': round((time.time() - t0) * 1000, 1),
        }
