import time


class ClassifierAgent:
    """Agent 1: Classifies incoming queries into business categories using keyword scoring."""

    NAME = "ClassifierAgent"

    CATEGORIES = {
        'pricing':     ['price', 'pricing', 'cost', 'rate', 'tier', 'discount', 'margin', 'fee',
                        'charge', 'expensive', 'budget', 'quote', 'invoice', 'billing'],
        'onboarding':  ['onboard', 'onboarding', 'new rep', 'training', 'orientation', 'setup',
                        'getting started', 'new hire', 'joining', 'bootcamp', 'ramp', 'induction'],
        'technical':   ['technical', 'bug', 'error', 'documentation', 'docs', 'api', 'integration',
                        'system', 'software', 'product spec', 'specification', 'manual', 'crash',
                        'glitch', 'fix', '503', '404', 'code'],
        'support':     ['support', 'help', 'assist', 'problem', 'trouble', 'response time', 'ticket',
                        'resolve', 'broken', 'unresponsive', 'no reply', 'unanswered', 'complaint'],
        'logistics':   ['delivery', 'shipping', 'shipment', 'stock', 'inventory', 'supply', 'order',
                        'dispatch', 'warehouse', 'logistics', 'fulfillment', 'lead time', 'delay'],
        'compliance':  ['compliance', 'regulation', 'legal', 'policy', 'audit', 'certification',
                        'license', 'law', 'gdpr', 'standard', 'iso', 'certification'],
        'partnership': ['partner', 'partnership', 'relationship', 'collaboration', 'growth',
                        'opportunity', 'expand', 'target', 'goal', 'q4', 'quarter', 'revenue'],
        'enablement':  ['enablement', 'material', 'collateral', 'marketing', 'sales kit', 'brochure',
                        'demo', 'presentation', 'webinar', 'workshop', 'video', 'content'],
    }

    def classify(self, text: str) -> dict:
        t0 = time.time()
        tl = text.lower()
        scores = {cat: sum(1 for kw in kws if kw in tl) for cat, kws in self.CATEGORIES.items()}
        scores = {k: v for k, v in scores.items() if v > 0}

        if not scores:
            category, confidence = 'general', 0.3
        else:
            category = max(scores, key=scores.get)
            total = sum(scores.values())
            confidence = min(scores[category] / max(total, 1), 1.0)

        return {
            'category': category,
            'confidence': round(confidence, 3),
            'all_scores': scores,
            'duration_ms': round((time.time() - t0) * 1000, 1),
        }
