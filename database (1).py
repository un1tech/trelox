#!/usr/bin/env python3
"""
Database management for Trelox Bot
SQLite database with comprehensive user management
"""

import asyncio
import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
from pathlib import Path
import aiosqlite

from config import Config

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Database manager for Trelox Bot"""
    
    def __init__(self):
        self.config = Config()
        self.db_path = "trelox_bot.db"
        self.init_database()
        
    def init_database(self):
        """Initialize database and create tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        language_code TEXT DEFAULT 'ar',
                        is_premium BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # User preferences table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_preferences (
                        user_id INTEGER PRIMARY KEY,
                        notifications_enabled BOOLEAN DEFAULT TRUE,
                        ai_summaries_enabled BOOLEAN DEFAULT TRUE,
                        preferred_sources TEXT DEFAULT '[]',
                        preferred_categories TEXT DEFAULT '[]',
                        daily_news_time TEXT DEFAULT '09:00',
                        language TEXT DEFAULT 'ar',
                        theme TEXT DEFAULT 'default',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    )
                """)
                
                # Favorites table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS favorites (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        title TEXT NOT NULL,
                        url TEXT NOT NULL,
                        summary TEXT,
                        source TEXT,
                        published_date TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (user_id),
                        UNIQUE(user_id, url)
                    )
                """)
                
                # Usage statistics table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS usage_stats (
                        user_id INTEGER PRIMARY KEY,
                        articles_read INTEGER DEFAULT 0,
                        favorites_count INTEGER DEFAULT 0,
                        notifications_sent INTEGER DEFAULT 0,
                        commands_used INTEGER DEFAULT 0,
                        last_news_request TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    )
                """)
                
                # News cache table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS news_cache (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        url TEXT UNIQUE NOT NULL,
                        title TEXT NOT NULL,
                        summary TEXT,
                        content TEXT,
                        source TEXT,
                        published_date TEXT,
                        category TEXT,
                        cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        expires_at TIMESTAMP
                    )
                """)
                
                # RSS sources tracking table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS rss_sources (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        url TEXT NOT NULL UNIQUE,
                        country TEXT,
                        category TEXT,
                        is_active BOOLEAN DEFAULT TRUE,
                        last_fetched TIMESTAMP,
                        success_count INTEGER DEFAULT 0,
                        error_count INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # User sessions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        session_data TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        expires_at TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    )
                """)
                
                # Create indexes for better performance
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_last_activity ON users (last_activity)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_favorites_user_id ON favorites (user_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_usage_stats_user_id ON usage_stats (user_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_news_cache_url ON news_cache (url)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_news_cache_expires ON news_cache (expires_at)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_rss_sources_active ON rss_sources (is_active)")
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    async def add_user(self, user_id: int, username: str = "", first_name: str = "", last_name: str = "", language_code: str = "ar"):
        """Add a new user to the database"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT OR REPLACE INTO users 
                    (user_id, username, first_name, last_name, language_code, last_activity)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, username, first_name, last_name, language_code, datetime.now()))
                
                # Initialize user preferences
                await db.execute("""
                    INSERT OR IGNORE INTO user_preferences (user_id)
                    VALUES (?)
                """, (user_id,))
                
                # Initialize usage stats
                await db.execute("""
                    INSERT OR IGNORE INTO usage_stats (user_id)
                    VALUES (?)
                """, (user_id,))
                
                await db.commit()
                logger.info(f"User {user_id} added/updated successfully")
                
        except Exception as e:
            logger.error(f"Failed to add user {user_id}: {e}")
            raise
    
    async def update_user_activity(self, user_id: int):
        """Update user's last activity timestamp"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    UPDATE users SET last_activity = ? WHERE user_id = ?
                """, (datetime.now(), user_id))
                await db.commit()
                
        except Exception as e:
            logger.error(f"Failed to update user activity for {user_id}: {e}")
    
    async def get_user_preferences(self, user_id: int) -> Dict[str, Any]:
        """Get user preferences"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute("""
                    SELECT * FROM user_preferences WHERE user_id = ?
                """, (user_id,))
                row = await cursor.fetchone()
                
                if row:
                    result = dict(row)
                    # Parse JSON fields
                    result['preferred_sources'] = json.loads(result['preferred_sources'] or '[]')
                    result['preferred_categories'] = json.loads(result['preferred_categories'] or '[]')
                    return result
                else:
                    # Return default preferences
                    return {
                        'user_id': user_id,
                        'notifications_enabled': True,
                        'ai_summaries_enabled': True,
                        'preferred_sources': [],
                        'preferred_categories': [],
                        'daily_news_time': '09:00',
                        'language': 'ar',
                        'theme': 'default'
                    }
                    
        except Exception as e:
            logger.error(f"Failed to get user preferences for {user_id}: {e}")
            return {}
    
    async def update_user_preferences(self, user_id: int, preferences: Dict[str, Any]):
        """Update user preferences"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Get current preferences to merge
                current = await self.get_user_preferences(user_id)
                current.update(preferences)
                
                await db.execute("""
                    INSERT OR REPLACE INTO user_preferences 
                    (user_id, notifications_enabled, ai_summaries_enabled, preferred_sources, 
                     preferred_categories, daily_news_time, language, theme, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    current.get('notifications_enabled', True),
                    current.get('ai_summaries_enabled', True),
                    json.dumps(current.get('preferred_sources', [])),
                    json.dumps(current.get('preferred_categories', [])),
                    current.get('daily_news_time', '09:00'),
                    current.get('language', 'ar'),
                    current.get('theme', 'default'),
                    datetime.now()
                ))
                await db.commit()
                logger.info(f"Updated preferences for user {user_id}")
                
        except Exception as e:
            logger.error(f"Failed to update user preferences for {user_id}: {e}")
            raise
    
    async def toggle_user_notifications(self, user_id: int):
        """Toggle user notifications preference"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute("""
                    SELECT notifications_enabled FROM user_preferences WHERE user_id = ?
                """, (user_id,))
                row = await cursor.fetchone()
                
                if row:
                    new_state = not row[0]
                    await db.execute("""
                        UPDATE user_preferences SET notifications_enabled = ?, updated_at = ? WHERE user_id = ?
                    """, (new_state, datetime.now(), user_id))
                    await db.commit()
                    return new_state
                    
        except Exception as e:
            logger.error(f"Failed to toggle notifications for user {user_id}: {e}")
            return False
    
    async def toggle_user_ai_summaries(self, user_id: int):
        """Toggle user AI summaries preference"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute("""
                    SELECT ai_summaries_enabled FROM user_preferences WHERE user_id = ?
                """, (user_id,))
                row = await cursor.fetchone()
                
                if row:
                    new_state = not row[0]
                    await db.execute("""
                        UPDATE user_preferences SET ai_summaries_enabled = ?, updated_at = ? WHERE user_id = ?
                    """, (new_state, datetime.now(), user_id))
                    await db.commit()
                    return new_state
                    
        except Exception as e:
            logger.error(f"Failed to toggle AI summaries for user {user_id}: {e}")
            return False
    
    async def toggle_user_preferred_sources(self, user_id: int):
        """Toggle user preferred sources"""
        try:
            current_prefs = await self.get_user_preferences(user_id)
            sources = current_prefs.get('preferred_sources', [])
            
            # For simplicity, toggle between all sources and empty
            if sources:
                new_sources = []
                message = "تم مسح المصادر المفضلة"
            else:
                new_sources = ['البداية', 'العربية', 'الجزيرة']  # Default sources
                message = "تم تحديد المصادر المفضلة"
            
            await self.update_user_preferences(user_id, {'preferred_sources': new_sources})
            return message
            
        except Exception as e:
            logger.error(f"Failed to toggle preferred sources for user {user_id}: {e}")
            return "حدث خطأ في تحديث المصادر"
    
    async def add_to_favorites(self, user_id: int, title: str, url: str, summary: str = "", source: str = "", published_date: str = ""):
        """Add article to user favorites"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT OR IGNORE INTO favorites 
                    (user_id, title, url, summary, source, published_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, title, url, summary, source, published_date))
                await db.commit()
                
                # Update favorites count in usage stats
                await db.execute("""
                    UPDATE usage_stats SET favorites_count = (
                        SELECT COUNT(*) FROM favorites WHERE user_id = ?
                    ), updated_at = ? WHERE user_id = ?
                """, (user_id, datetime.now(), user_id))
                await db.commit()
                
                logger.info(f"Added to favorites: {title[:50]}...")
                
        except Exception as e:
            logger.error(f"Failed to add to favorites for user {user_id}: {e}")
            raise
    
    async def remove_from_favorites(self, user_id: int, url: str):
        """Remove article from user favorites"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    DELETE FROM favorites WHERE user_id = ? AND url = ?
                """, (user_id, url))
                await db.commit()
                
                # Update favorites count
                await db.execute("""
                    UPDATE usage_stats SET favorites_count = (
                        SELECT COUNT(*) FROM favorites WHERE user_id = ?
                    ), updated_at = ? WHERE user_id = ?
                """, (user_id, datetime.now(), user_id))
                await db.commit()
                
        except Exception as e:
            logger.error(f"Failed to remove from favorites for user {user_id}: {e}")
            raise
    
    async def get_user_favorites(self, user_id: int, limit: int = 20) -> List[Dict[str, Any]]:
        """Get user favorites"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute("""
                    SELECT * FROM favorites 
                    WHERE user_id = ? 
                    ORDER BY created_at DESC 
                    LIMIT ?
                """, (user_id, limit))
                rows = await cursor.fetchall()
                
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Failed to get favorites for user {user_id}: {e}")
            return []
    
    async def clear_user_favorites(self, user_id: int):
        """Clear all user favorites"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("DELETE FROM favorites WHERE user_id = ?", (user_id,))
                await db.execute("""
                    UPDATE usage_stats SET favorites_count = 0, updated_at = ? WHERE user_id = ?
                """, (datetime.now(), user_id))
                await db.commit()
                logger.info(f"Cleared favorites for user {user_id}")
                
        except Exception as e:
            logger.error(f"Failed to clear favorites for user {user_id}: {e}")
            raise
    
    async def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Get user statistics"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute("""
                    SELECT u.*, us.* FROM users u
                    LEFT JOIN usage_stats us ON u.user_id = us.user_id
                    WHERE u.user_id = ?
                """, (user_id,))
                row = await cursor.fetchone()
                
                if row:
                    result = dict(row)
                    # Format dates
                    result['joined_date'] = result.get('created_at', '').split(' ')[0] if result.get('created_at') else 'غير محدد'
                    result['last_activity'] = result.get('last_activity', '').split(' ')[0] if result.get('last_activity') else 'غير محدد'
                    return result
                else:
                    return {
                        'user_id': user_id,
                        'articles_read': 0,
                        'favorites_count': 0,
                        'notifications_sent': 0,
                        'commands_used': 0,
                        'joined_date': 'غير محدد',
                        'last_activity': 'غير محدد'
                    }
                    
        except Exception as e:
            logger.error(f"Failed to get stats for user {user_id}: {e}")
            return {}
    
    async def increment_articles_read(self, user_id: int):
        """Increment articles read count"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    UPDATE usage_stats 
                    SET articles_read = articles_read + 1, 
                        last_news_request = ?, 
                        updated_at = ? 
                    WHERE user_id = ?
                """, (datetime.now(), datetime.now(), user_id))
                await db.commit()
                
        except Exception as e:
            logger.error(f"Failed to increment articles read for user {user_id}: {e}")
    
    async def increment_notification_count(self, user_id: int):
        """Increment notifications sent count"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    UPDATE usage_stats 
                    SET notifications_sent = notifications_sent + 1, 
                        updated_at = ? 
                    WHERE user_id = ?
                """, (datetime.now(), user_id))
                await db.commit()
                
        except Exception as e:
            logger.error(f"Failed to increment notification count for user {user_id}: {e}")
    
    async def get_users_with_notifications_enabled(self) -> List[Dict[str, Any]]:
        """Get all users who have notifications enabled"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute("""
                    SELECT u.user_id, u.username, u.first_name 
                    FROM users u
                    JOIN user_preferences up ON u.user_id = up.user_id
                    WHERE up.notifications_enabled = TRUE
                    AND u.last_activity > datetime('now', '-30 days')
                """)
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Failed to get users with notifications: {e}")
            return []
    
    async def cache_news_article(self, title: str, url: str, summary: str = "", content: str = "", 
                                source: str = "", published_date: str = "", category: str = ""):
        """Cache news article for performance"""
        try:
            if not self.config.ENABLE_CACHE:
                return
                
            expires_at = datetime.now() + timedelta(seconds=self.config.CACHE_DURATION)
            
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT OR REPLACE INTO news_cache 
                    (url, title, summary, content, source, published_date, category, expires_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (url, title, summary, content, source, published_date, category, expires_at))
                await db.commit()
                
        except Exception as e:
            logger.error(f"Failed to cache news article: {e}")
    
    async def get_cached_article(self, url: str) -> Optional[Dict[str, Any]]:
        """Get cached article if available and not expired"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute("""
                    SELECT * FROM news_cache 
                    WHERE url = ? AND expires_at > datetime('now')
                """, (url,))
                row = await cursor.fetchone()
                
                return dict(row) if row else None
                
        except Exception as e:
            logger.error(f"Failed to get cached article: {e}")
            return None
    
    async def cleanup_expired_cache(self):
        """Clean up expired cache entries"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("DELETE FROM news_cache WHERE expires_at <= datetime('now')")
                await db.commit()
                logger.info("Cleaned up expired cache entries")
                
        except Exception as e:
            logger.error(f"Failed to cleanup expired cache: {e}")
    
    async def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                stats = {}
                
                # Count users
                cursor = await db.execute("SELECT COUNT(*) FROM users")
                stats['total_users'] = cursor.fetchone()[0]
                
                # Count favorites
                cursor = await db.execute("SELECT COUNT(*) FROM favorites")
                stats['total_favorites'] = cursor.fetchone()[0]
                
                # Count cached articles
                cursor = await db.execute("SELECT COUNT(*) FROM news_cache")
                stats['cached_articles'] = cursor.fetchone()[0]
                
                # Active users (last 7 days)
                cursor = await db.execute("""
                    SELECT COUNT(*) FROM users 
                    WHERE last_activity > datetime('now', '-7 days')
                """)
                stats['active_users_week'] = cursor.fetchone()[0]
                
                # Active users (last 30 days)
                cursor = await db.execute("""
                    SELECT COUNT(*) FROM users 
                    WHERE last_activity > datetime('now', '-30 days')
                """)
                stats['active_users_month'] = cursor.fetchone()[0]
                
                return stats
                
        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
            return {}
    
    async def backup_database(self, backup_path: str = None):
        """Create database backup"""
        try:
            if not backup_path:
                backup_path = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                
            async with aiosqlite.connect(self.db_path) as source_db:
                async with aiosqlite.connect(backup_path) as backup_db:
                    await source_db.backup(backup_db)
                    
            logger.info(f"Database backed up to {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Failed to backup database: {e}")
            raise

# Global database instance
db = DatabaseManager()

# Initialize database on import
db.init_database()