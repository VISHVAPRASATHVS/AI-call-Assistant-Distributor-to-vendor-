from datetime import datetime, timedelta
import time


class ActionAgent:
    """Agent 4: Auto-generates follow-up action items with owners, deadlines, and priority."""

    NAME = "ActionAgent"

    TEMPLATES = {
        'pricing': [
            {'task': 'Send updated Pricing Tier Documentation (PDF + Video)',  'owner': 'Partner Manager',       'days': 1, 'priority': 'High'},
            {'task': 'Schedule 1:1 Pricing Strategy Call with Finance Team',   'owner': 'Sales Director',        'days': 2, 'priority': 'Medium'},
            {'task': 'Grant access to Real-Time Partner Pricing Portal',        'owner': 'IT Operations',         'days': 1, 'priority': 'High'},
        ],
        'onboarding': [
            {'task': 'Deliver complete Sales Rep Onboarding Kit (digital)',     'owner': 'Vendor AE',             'days': 1, 'priority': 'High'},
            {'task': 'Register distributor team for next Bootcamp session',     'owner': 'Training Team',         'days': 3, 'priority': 'High'},
            {'task': 'Assign dedicated Partner Success Manager',                'owner': 'Partner Success',        'days': 1, 'priority': 'Medium'},
        ],
        'technical': [
            {'task': 'Share full Technical Documentation & API Reference',      'owner': 'Solutions Engineer',    'days': 1, 'priority': 'High'},
            {'task': 'Provision sandbox/test environment for integration',      'owner': 'DevOps Team',           'days': 2, 'priority': 'High'},
            {'task': 'Schedule live Technical Troubleshooting Session',         'owner': 'Solutions Engineer',    'days': 3, 'priority': 'Medium'},
        ],
        'support': [
            {'task': 'Open Priority-1 Support Ticket and assign engineer',     'owner': 'Support Manager',       'days': 0, 'priority': 'Critical'},
            {'task': 'Initiate live screen-share troubleshooting session',     'owner': 'Support Engineer',      'days': 0, 'priority': 'Critical'},
            {'task': 'Provide 24/7 emergency hotline access',                  'owner': 'Operations Director',   'days': 0, 'priority': 'Critical'},
        ],
        'logistics': [
            {'task': 'Expedite shipment to priority fulfillment queue',        'owner': 'Logistics Manager',     'days': 1, 'priority': 'High'},
            {'task': 'Send real-time inventory status report',                 'owner': 'Supply Chain Team',     'days': 1, 'priority': 'High'},
            {'task': 'Assign dedicated Logistics Coordinator for account',     'owner': 'Operations Team',       'days': 2, 'priority': 'Medium'},
        ],
        'compliance': [
            {'task': 'Share full Compliance & Certification Bundle',           'owner': 'Legal Team',            'days': 1, 'priority': 'High'},
            {'task': 'Schedule Compliance Review meeting with legal officers',  'owner': 'Compliance Officer',   'days': 3, 'priority': 'High'},
            {'task': 'Send GDPR/ISO compliance statement',                     'owner': 'Legal Team',            'days': 2, 'priority': 'Medium'},
        ],
        'enablement': [
            {'task': 'Send complete Partner Enablement Kit (slides + videos)', 'owner': 'Enablement Manager',   'days': 1, 'priority': 'High'},
            {'task': 'Enrol team in 3-Month Partner Enablement Program',       'owner': 'Partner Success',       'days': 3, 'priority': 'Medium'},
            {'task': 'Invite to next Product Webinar & Demo Day',              'owner': 'Marketing Team',        'days': 5, 'priority': 'Low'},
        ],
        'partnership': [
            {'task': 'Schedule Quarterly Business Review (QBR)',               'owner': 'Account Manager',       'days': 5, 'priority': 'High'},
            {'task': 'Share Market Growth Opportunity Analysis Report',         'owner': 'Business Development',  'days': 4, 'priority': 'Medium'},
            {'task': 'Define Q4 partnership targets and KPIs',                 'owner': 'Partner Manager',       'days': 3, 'priority': 'High'},
        ],
        'general': [
            {'task': 'Assign Dedicated Account Manager for follow-up',         'owner': 'Account Management',    'days': 1, 'priority': 'Medium'},
            {'task': 'Log case in CRM and initiate SLA tracking',              'owner': 'Operations Team',       'days': 1, 'priority': 'Medium'},
            {'task': 'Schedule check-in call within 48 hours',                 'owner': 'Account Manager',       'days': 2, 'priority': 'Low'},
        ],
    }

    def generate(self, query_text: str, classification: dict, solutions: list) -> list:
        t0 = time.time()
        category = classification.get('category', 'general')
        templates = self.TEMPLATES.get(category, self.TEMPLATES['general'])
        actions = []
        for tmpl in templates[:3]:
            deadline = (datetime.now() + timedelta(days=tmpl['days'])).strftime('%b %d, %Y')
            actions.append({
                'task': tmpl['task'],
                'owner': tmpl['owner'],
                'deadline': deadline,
                'priority': tmpl['priority'],
                'status': 'Open',
                'duration_ms': round((time.time() - t0) * 1000, 1),
            })
        return actions
