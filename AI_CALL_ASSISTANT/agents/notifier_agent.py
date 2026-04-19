from datetime import datetime
import time


class NotifierAgent:
    """Agent 6: Generates rich, structured notifications for distributors after query resolution."""

    NAME = "NotifierAgent"

    def notify(self, distributor_name: str, query_id: int, solutions: list, actions: list) -> dict:
        t0 = time.time()
        top_sol = solutions[0]['solution'] if solutions else 'Personalized support is being arranged'
        top_act = actions[0] if actions else {'task': 'Follow-up call scheduled', 'deadline': 'within 24h', 'owner': 'Account Manager'}

        msg = (
            f"✅ [Query #{query_id}] Auto-resolved by AI Agent Pipeline | "
            f"Solution: {top_sol} | "
            f"Next Action: '{top_act['task']}' by {top_act['owner']} ({top_act['deadline']}) | "
            f"Processed: {datetime.now().strftime('%d %b %Y %H:%M')} IST"
        )
        return {
            'message': msg,
            'distributor': distributor_name,
            'query_id': query_id,
            'top_solution': top_sol,
            'top_action': top_act,
            'timestamp': datetime.now().isoformat(),
            'duration_ms': round((time.time() - t0) * 1000, 1),
        }
