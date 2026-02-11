import sqlite3
import json
from datetime import datetime
import os

class Database:
    """SQLite database for storing user data and preferences"""
    
    def __init__(self, db_path='data/styleai.db'):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Recommendations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                skin_tone TEXT,
                undertone TEXT,
                recommendations TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Wardrobe table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wardrobe (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                item_type TEXT,
                color TEXT,
                style TEXT,
                image_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                recommendation_id INTEGER,
                liked BOOLEAN,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_recommendation(self, user_id, recommendations):
        """Save AI recommendations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO recommendations (user_id, recommendations)
            VALUES (?, ?)
        ''', (user_id, json.dumps(recommendations)))
        
        conn.commit()
        rec_id = cursor.lastrowid
        conn.close()
        
        return rec_id
    
    def add_wardrobe_item(self, user_id, item):
        """Add item to virtual wardrobe"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO wardrobe (user_id, item_type, color, style, image_url)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, item.get('type'), item.get('color'), 
              item.get('style'), item.get('image_url')))
        
        conn.commit()
        conn.close()
    
    def get_wardrobe(self, user_id):
        """Get user's wardrobe items"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, item_type, color, style, image_url, created_at
            FROM wardrobe
            WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        items = []
        for row in rows:
            items.append({
                'id': row[0],
                'type': row[1],
                'color': row[2],
                'style': row[3],
                'image_url': row[4],
                'created_at': row[5]
            })
        
        return items
    
    def save_feedback(self, user_id, feedback):
        """Save user feedback"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO feedback (user_id, recommendation_id, liked, comment)
            VALUES (?, ?, ?, ?)
        ''', (user_id, feedback.get('recommendation_id'), 
              feedback.get('liked'), feedback.get('comment')))
        
        conn.commit()
        conn.close()
    
    def get_user_preferences(self, user_id):
        """Analyze user preferences from feedback"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT liked, comment FROM feedback
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 20
        ''', (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        liked_count = sum(1 for row in rows if row[0])
        total_count = len(rows)
        
        return {
            'liked_percentage': (liked_count / total_count * 100) if total_count > 0 else 0,
            'total_feedback': total_count
        }
