import sqlite3
import os
import json
import threading
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'ai_call_assistant.db')


class DatabaseManager:
    _lock = threading.Lock()

    def __init__(self):
        os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)
        self._init_db()

    def _get_conn(self):
        conn = sqlite3.connect(os.path.abspath(DB_PATH), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._lock:
            conn = self._get_conn()
            conn.executescript('''
                CREATE TABLE IF NOT EXISTS queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    distributor_name TEXT NOT NULL,
                    query_text TEXT NOT NULL,
                    query_type TEXT DEFAULT 'unknown',
                    timestamp TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    processing_time_ms INTEGER DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS solutions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_id INTEGER NOT NULL,
                    solution_text TEXT NOT NULL,
                    agent_name TEXT NOT NULL,
                    confidence REAL DEFAULT 0.0,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (query_id) REFERENCES queries(id)
                );
                CREATE TABLE IF NOT EXISTS action_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_id INTEGER NOT NULL,
                    task TEXT NOT NULL,
                    owner TEXT NOT NULL,
                    deadline TEXT NOT NULL,
                    priority TEXT DEFAULT 'Medium',
                    status TEXT DEFAULT 'Open',
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (query_id) REFERENCES queries(id)
                );
                CREATE TABLE IF NOT EXISTS sentiment_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_id INTEGER NOT NULL,
                    overall_sentiment TEXT NOT NULL,
                    sentiment_score REAL NOT NULL,
                    positive_phrases TEXT,
                    negative_phrases TEXT,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (query_id) REFERENCES queries(id)
                );
                CREATE TABLE IF NOT EXISTS escalations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_id INTEGER NOT NULL,
                    priority TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    status TEXT DEFAULT 'Open',
                    assigned_to TEXT DEFAULT 'Support Manager',
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (query_id) REFERENCES queries(id)
                );
                CREATE TABLE IF NOT EXISTS notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    distributor_name TEXT NOT NULL,
                    message TEXT NOT NULL,
                    notification_type TEXT DEFAULT 'info',
                    timestamp TEXT NOT NULL,
                    is_read INTEGER DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS agent_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT NOT NULL,
                    action TEXT NOT NULL,
                    input_summary TEXT,
                    output_summary TEXT,
                    duration_ms INTEGER DEFAULT 0,
                    timestamp TEXT NOT NULL
                );
            ''')
            conn.commit()
            conn.close()

    def add_query(self, distributor_name, query_text, query_type='unknown'):
        with self._lock:
            conn = self._get_conn()
            cur = conn.execute(
                'INSERT INTO queries (distributor_name, query_text, query_type, timestamp, status) VALUES (?,?,?,?,?)',
                (distributor_name, query_text, query_type, datetime.now().isoformat(), 'pending')
            )
            qid = cur.lastrowid
            conn.commit()
            conn.close()
            return qid

    def update_query_status(self, query_id, status, processing_time_ms=0, query_type='unknown'):
        with self._lock:
            conn = self._get_conn()
            conn.execute(
                'UPDATE queries SET status=?, processing_time_ms=?, query_type=? WHERE id=?',
                (status, processing_time_ms, query_type, query_id)
            )
            conn.commit()
            conn.close()

    def save_solution(self, query_id, solution_text, agent_name, confidence):
        with self._lock:
            conn = self._get_conn()
            conn.execute(
                'INSERT INTO solutions (query_id, solution_text, agent_name, confidence, timestamp) VALUES (?,?,?,?,?)',
                (query_id, solution_text, agent_name, confidence, datetime.now().isoformat())
            )
            conn.commit()
            conn.close()

    def save_action_item(self, query_id, task, owner, deadline, priority='Medium'):
        with self._lock:
            conn = self._get_conn()
            conn.execute(
                'INSERT INTO action_items (query_id, task, owner, deadline, priority, status, timestamp) VALUES (?,?,?,?,?,?,?)',
                (query_id, task, owner, deadline, priority, 'Open', datetime.now().isoformat())
            )
            conn.commit()
            conn.close()

    def save_sentiment(self, query_id, result):
        with self._lock:
            conn = self._get_conn()
            conn.execute(
                'INSERT INTO sentiment_log (query_id, overall_sentiment, sentiment_score, positive_phrases, negative_phrases, timestamp) VALUES (?,?,?,?,?,?)',
                (query_id, result['overall'], result['score'],
                 json.dumps(result.get('positive_phrases', [])),
                 json.dumps(result.get('negative_phrases', [])),
                 datetime.now().isoformat())
            )
            conn.commit()
            conn.close()

    def save_escalation(self, query_id, priority, reason):
        with self._lock:
            conn = self._get_conn()
            conn.execute(
                'INSERT INTO escalations (query_id, priority, reason, status, assigned_to, timestamp) VALUES (?,?,?,?,?,?)',
                (query_id, priority, reason, 'Open', 'Support Manager', datetime.now().isoformat())
            )
            conn.commit()
            conn.close()

    def save_notification(self, distributor_name, message, notification_type='info'):
        with self._lock:
            conn = self._get_conn()
            conn.execute(
                'INSERT INTO notifications (distributor_name, message, notification_type, timestamp) VALUES (?,?,?,?)',
                (distributor_name, message, notification_type, datetime.now().isoformat())
            )
            conn.commit()
            conn.close()

    def log_agent_action(self, agent_name, action, input_summary, output_summary, duration_ms=0):
        with self._lock:
            conn = self._get_conn()
            conn.execute(
                'INSERT INTO agent_logs (agent_name, action, input_summary, output_summary, duration_ms, timestamp) VALUES (?,?,?,?,?,?)',
                (agent_name, action, str(input_summary)[:500], str(output_summary)[:500], duration_ms, datetime.now().isoformat())
            )
            conn.commit()
            conn.close()

    def get_all_queries(self, limit=200):
        conn = self._get_conn()
        rows = conn.execute('SELECT * FROM queries ORDER BY timestamp DESC LIMIT ?', (limit,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_pending_queries(self, limit=10):
        conn = self._get_conn()
        rows = conn.execute("SELECT * FROM queries WHERE status='pending' ORDER BY timestamp ASC LIMIT ?", (limit,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_query_solutions(self, query_id):
        conn = self._get_conn()
        rows = conn.execute('SELECT * FROM solutions WHERE query_id=? ORDER BY confidence DESC', (query_id,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_query_actions(self, query_id):
        conn = self._get_conn()
        rows = conn.execute('SELECT * FROM action_items WHERE query_id=?', (query_id,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_query_sentiment(self, query_id):
        conn = self._get_conn()
        row = conn.execute('SELECT * FROM sentiment_log WHERE query_id=?', (query_id,)).fetchone()
        conn.close()
        return dict(row) if row else {}

    def get_all_escalations(self):
        conn = self._get_conn()
        rows = conn.execute(
            'SELECT e.*, q.distributor_name, q.query_text FROM escalations e JOIN queries q ON e.query_id=q.id ORDER BY e.timestamp DESC'
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_notifications(self, distributor_name=None):
        conn = self._get_conn()
        if distributor_name:
            rows = conn.execute('SELECT * FROM notifications WHERE distributor_name=? ORDER BY timestamp DESC LIMIT 50', (distributor_name,)).fetchall()
        else:
            rows = conn.execute('SELECT * FROM notifications ORDER BY timestamp DESC LIMIT 100').fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_agent_logs(self, limit=100):
        conn = self._get_conn()
        rows = conn.execute('SELECT * FROM agent_logs ORDER BY timestamp DESC LIMIT ?', (limit,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_analytics(self):
        conn = self._get_conn()
        total = conn.execute('SELECT COUNT(*) FROM queries').fetchone()[0]
        completed = conn.execute("SELECT COUNT(*) FROM queries WHERE status='completed'").fetchone()[0]
        pending = conn.execute("SELECT COUNT(*) FROM queries WHERE status='pending'").fetchone()[0]
        by_type = conn.execute('SELECT query_type, COUNT(*) as count FROM queries GROUP BY query_type').fetchall()
        by_distributor = conn.execute('SELECT distributor_name, COUNT(*) as count FROM queries GROUP BY distributor_name ORDER BY count DESC LIMIT 10').fetchall()
        sentiment_dist = conn.execute('SELECT overall_sentiment, COUNT(*) as count FROM sentiment_log GROUP BY overall_sentiment').fetchall()
        total_escalations = conn.execute('SELECT COUNT(*) FROM escalations').fetchone()[0]
        open_escalations = conn.execute("SELECT COUNT(*) FROM escalations WHERE status='Open'").fetchone()[0]
        avg_time = conn.execute("SELECT AVG(processing_time_ms) FROM queries WHERE status='completed'").fetchone()[0] or 0
        trend = conn.execute("SELECT DATE(timestamp) as date, COUNT(*) as count FROM queries GROUP BY DATE(timestamp) ORDER BY date DESC LIMIT 14").fetchall()
        conn.close()
        return {
            'total': total, 'completed': completed, 'pending': pending,
            'resolution_rate': round((completed / total * 100) if total > 0 else 0, 1),
            'by_type': [dict(r) for r in by_type],
            'by_distributor': [dict(r) for r in by_distributor],
            'sentiment_dist': [dict(r) for r in sentiment_dist],
            'total_escalations': total_escalations,
            'open_escalations': open_escalations,
            'avg_processing_time_ms': round(avg_time, 1),
            'trend': [dict(r) for r in trend]
        }

    def get_distributor_summary(self):
        conn = self._get_conn()
        rows = conn.execute('''
            SELECT q.distributor_name,
                   COUNT(q.id) as total_queries,
                   SUM(CASE WHEN q.status='completed' THEN 1 ELSE 0 END) as resolved,
                   SUM(CASE WHEN q.status='pending' THEN 1 ELSE 0 END) as pending,
                   AVG(COALESCE(sl.sentiment_score,0.5)) as avg_sentiment
            FROM queries q
            LEFT JOIN sentiment_log sl ON q.id = sl.query_id
            GROUP BY q.distributor_name
            ORDER BY total_queries DESC
        ''').fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def query_count(self):
        conn = self._get_conn()
        n = conn.execute('SELECT COUNT(*) FROM queries').fetchone()[0]
        conn.close()
        return n


db = DatabaseManager()
