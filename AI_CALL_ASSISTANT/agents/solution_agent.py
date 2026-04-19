import json
import os
import time

KB_PATH = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'solutions.json')


class SolutionAgent:
    """Agent 3: Matches queries to solutions in the knowledge base via keyword scoring."""

    NAME = "SolutionAgent"

    def __init__(self):
        with open(KB_PATH, 'r') as f:
            self.kb = json.load(f)

    def match(self, query_text: str, classification: dict, distributor_name: str = '') -> list:
        t0 = time.time()
        tl = query_text.lower()
        category = classification.get('category', 'general')
        candidates = self.kb.get(category, []) + self.kb.get('general', [])

        scored = []
        for sol in candidates:
            kw_score = sum(1 for kw in sol.get('keywords', []) if kw.lower() in tl)
            base_conf = classification.get('confidence', 0.5)
            confidence = min((kw_score * 0.3 + base_conf * 0.7), 1.0)
            if confidence > 0.1:
                scored.append({
                    'solution': sol['solution'],
                    'description': sol.get('description', ''),
                    'agent': self.NAME,
                    'confidence': round(confidence, 3),
                    'resources': sol.get('resources', []),
                    'estimated_time': sol.get('estimated_time', '24 hours'),
                    'duration_ms': round((time.time() - t0) * 1000, 1),
                })

        scored.sort(key=lambda x: x['confidence'], reverse=True)

        if not scored:
            scored = [{
                'solution': 'Assign Dedicated Account Manager for personalized resolution',
                'description': 'A senior account manager will contact you within 4 business hours.',
                'agent': self.NAME,
                'confidence': 0.65,
                'resources': ['Account Management Team'],
                'estimated_time': '4 hours',
                'duration_ms': 0,
            }]

        return scored[:3]
