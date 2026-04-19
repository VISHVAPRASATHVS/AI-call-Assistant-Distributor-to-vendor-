import time


class EscalationAgent:
    """Agent 5: Evaluates whether a query needs escalation and determines P1/P2/P3 priority."""

    NAME = "EscalationAgent"

    P1_KEYWORDS = ['urgent', 'critical', 'emergency', 'asap', 'immediately', 'escalate',
                   'serious', 'major', 'unacceptable', 'losing', 'cannot operate', 'system down']
    P2_KEYWORDS = ['important', 'soon', 'quickly', 'priority', 'blocking', 'cannot', 'unable',
                   'broken', 'fail', 'no reply', 'unanswered', 'overdue', '5 days', '3 days']

    def evaluate(self, query_text: str, sentiment: dict, classification: dict) -> dict:
        t0 = time.time()
        tl = query_text.lower()
        p1_hits = [kw for kw in self.P1_KEYWORDS if kw in tl]
        p2_hits = [kw for kw in self.P2_KEYWORDS if kw in tl]
        score = sentiment.get('score', 0.5)
        neg_count = sentiment.get('negative_count', 0)

        should_escalate = False
        priority = 'P3'
        reason = 'Standard query — no escalation needed'

        if p1_hits or (neg_count >= 5 and score < 0.25):
            should_escalate = True
            priority = 'P1'
            reason = f"CRITICAL: {', '.join(p1_hits) or 'Extremely negative sentiment detected'}"
        elif p2_hits or (neg_count >= 3 and score < 0.35):
            should_escalate = True
            priority = 'P2'
            reason = f"HIGH: {', '.join(p2_hits[:3]) or 'High negative sentiment'}"
        elif classification.get('category') in ('support', 'logistics') and score < 0.4:
            should_escalate = True
            priority = 'P2'
            reason = f"Operationally critical category ({classification['category']}) with negative tone"

        return {
            'should_escalate': should_escalate,
            'priority': priority,
            'reason': reason,
            'p1_hits': p1_hits,
            'p2_hits': p2_hits,
            'duration_ms': round((time.time() - t0) * 1000, 1),
        }
