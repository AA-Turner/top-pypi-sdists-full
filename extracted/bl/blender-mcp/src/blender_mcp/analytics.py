import sqlite3
import hashlib
import platform
import getpass
import os
from datetime import datetime, date
import logging
from pathlib import Path

logger = logging.getLogger("BlenderMCPAnalytics")

class Analytics:
    def __init__(self):
        # Create analytics directory in user's home
        self.analytics_dir = Path.home() / ".blendermcp"
        self.analytics_dir.mkdir(exist_ok=True)
        self.db_path = self.analytics_dir / "usage.db"
        self.init_database()
        
    def init_database(self):
        """Initialize the SQLite database for tracking usage"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS daily_usage (
                        date TEXT PRIMARY KEY,
                        unique_users INTEGER DEFAULT 0,
                        total_sessions INTEGER DEFAULT 0
                    )
                ''')
                
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS user_sessions (
                        user_id TEXT,
                        date TEXT,
                        timestamp TEXT,
                        PRIMARY KEY (user_id, date)
                    )
                ''')
                
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to initialize analytics database: {e}")
    
    def get_anonymous_user_id(self):
        """Generate an anonymous but consistent user ID"""
        try:
            # Create a hash from username + machine info for consistency
            username = getpass.getuser()
            machine = platform.node()
            system = platform.system()
            
            # Create a hash that's consistent but anonymous
            user_string = f"{username}_{machine}_{system}"
            user_id = hashlib.sha256(user_string.encode()).hexdigest()[:16]
            return user_id
        except Exception:
            # Fallback to a random-ish but semi-consistent ID
            return hashlib.sha256(str(os.getpid()).encode()).hexdigest()[:16]
    
    def track_usage(self):
        """Track that a user used the system today"""
        try:
            user_id = self.get_anonymous_user_id()
            today = date.today().isoformat()
            now = datetime.now().isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                # Insert or ignore user session for today
                conn.execute('''
                    INSERT OR IGNORE INTO user_sessions (user_id, date, timestamp)
                    VALUES (?, ?, ?)
                ''', (user_id, today, now))
                
                # Update daily usage stats
                conn.execute('''
                    INSERT OR REPLACE INTO daily_usage (date, unique_users, total_sessions)
                    VALUES (?, 
                        (SELECT COUNT(DISTINCT user_id) FROM user_sessions WHERE date = ?),
                        (SELECT COUNT(*) FROM user_sessions WHERE date = ?)
                    )
                ''', (today, today, today))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Failed to track usage: {e}")
    
    def get_daily_stats(self, days=7):
        """Get daily active user stats for the last N days"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT date, unique_users, total_sessions
                    FROM daily_usage
                    ORDER BY date DESC
                    LIMIT ?
                ''', (days,))
                
                results = cursor.fetchall()
                return [{"date": row[0], "unique_users": row[1], "total_sessions": row[2]} 
                       for row in results]
        except Exception as e:
            logger.error(f"Failed to get daily stats: {e}")
            return []
    
    def get_total_users(self):
        """Get total number of unique users ever"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('SELECT COUNT(DISTINCT user_id) FROM user_sessions')
                return cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Failed to get total users: {e}")
            return 0

# Global analytics instance
_analytics = Analytics()

def track_usage():
    """Simple function to track usage"""
    _analytics.track_usage()

def get_usage_stats(days=7):
    """Get usage statistics"""
    return _analytics.get_daily_stats(days)

def get_total_users():
    """Get total unique users"""
    return _analytics.get_total_users() 