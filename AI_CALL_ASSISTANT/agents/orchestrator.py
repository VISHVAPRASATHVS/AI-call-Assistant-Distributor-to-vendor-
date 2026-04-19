import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.classifier_agent import ClassifierAgent
from agents.sentiment_agent import SentimentAgent
from agents.solution_agent import SolutionAgent
from agents.action_agent import ActionAgent
from agents.escalation_agent import EscalationAgent
from agents.notifier_agent import NotifierAgent
from database.db_manager import db


class OrchestratorAgent:
    """
    Master Agent 7: Coordinates the full 6-agent pipeline autonomously.
    Processes queries end-to-end with zero human interaction required.
    """

    NAME = "OrchestratorAgent"
    PIPELINE = [
        'ClassifierAgent → categorize query',
        'SentimentAgent → measure emotional tone',
        'SolutionAgent → match KB solutions',
        'ActionAgent → generate follow-up tasks',
        'EscalationAgent → determine priority',
        'NotifierAgent → push distributor notification',
    ]

    def __init__(self):
        self.classifier = ClassifierAgent()
        self.sentiment = SentimentAgent()
        self.solution = SolutionAgent()
        self.action = ActionAgent()
        self.escalation = EscalationAgent()
        self.notifier = NotifierAgent()

    def process_query(self, query_id: int, query_text: str, distributor_name: str) -> dict:
        """Full autonomous 6-agent pipeline. Returns complete result dict."""
        pipeline_start = time.time()
        result = {'query_id': query_id, 'success': False}

        try:
            # ── Agent 1: Classify ─────────────────────────────
            t0 = time.time()
            classification = self.classifier.classify(query_text)
            db.log_agent_action('ClassifierAgent', 'classify',
                                query_text[:120], str(classification),
                                int((time.time() - t0) * 1000))
            result['classification'] = classification

            # ── Agent 2: Sentiment ────────────────────────────
            t0 = time.time()
            sentiment = self.sentiment.analyze(query_text)
            db.log_agent_action('SentimentAgent', 'analyze',
                                query_text[:120], str(sentiment),
                                int((time.time() - t0) * 1000))
            db.save_sentiment(query_id, sentiment)
            result['sentiment'] = sentiment

            # ── Agent 3: Solutions ────────────────────────────
            t0 = time.time()
            solutions = self.solution.match(query_text, classification, distributor_name)
            db.log_agent_action('SolutionAgent', 'match',
                                query_text[:120], str([s['solution'] for s in solutions]),
                                int((time.time() - t0) * 1000))
            for sol in solutions:
                db.save_solution(query_id, sol['solution'], sol['agent'], sol['confidence'])
            result['solutions'] = solutions

            # ── Agent 4: Action Items ─────────────────────────
            t0 = time.time()
            actions = self.action.generate(query_text, classification, solutions)
            db.log_agent_action('ActionAgent', 'generate',
                                query_text[:120], str([a['task'] for a in actions]),
                                int((time.time() - t0) * 1000))
            for a in actions:
                db.save_action_item(query_id, a['task'], a['owner'], a['deadline'], a['priority'])
            result['actions'] = actions

            # ── Agent 5: Escalation ───────────────────────────
            t0 = time.time()
            escl = self.escalation.evaluate(query_text, sentiment, classification)
            db.log_agent_action('EscalationAgent', 'evaluate',
                                query_text[:120], str(escl),
                                int((time.time() - t0) * 1000))
            if escl['should_escalate']:
                db.save_escalation(query_id, escl['priority'], escl['reason'])
                notif_type = 'critical' if escl['priority'] == 'P1' else 'warning'
            else:
                notif_type = 'success'
            result['escalation'] = escl

            # ── Agent 6: Notify ───────────────────────────────
            t0 = time.time()
            notification = self.notifier.notify(distributor_name, query_id, solutions, actions)
            db.log_agent_action('NotifierAgent', 'notify',
                                distributor_name, notification['message'][:120],
                                int((time.time() - t0) * 1000))
            db.save_notification(distributor_name, notification['message'], notif_type)
            result['notification'] = notification

            # ── Finalise ──────────────────────────────────────
            total_ms = int((time.time() - pipeline_start) * 1000)
            db.update_query_status(query_id, 'completed', total_ms, classification['category'])
            result['total_ms'] = total_ms
            result['success'] = True

        except Exception as e:
            db.update_query_status(query_id, 'failed')
            db.log_agent_action('OrchestratorAgent', 'pipeline_error', str(query_id), str(e))
            result['error'] = str(e)

        return result

    def process_pending(self, limit: int = 5) -> int:
        """Autonomously drain the pending queue. Returns count processed."""
        pending = db.get_pending_queries(limit=limit)
        for q in pending:
            self.process_query(q['id'], q['query_text'], q['distributor_name'])
        return len(pending)
