#!/usr/bin/env python3
"""
Configuration management for Trelox Bot
Centralized configuration with environment variables
"""

import os
from typing import List, Optional
from dataclasses import dataclass, field

@dataclass
class Config:
    """Configuration class for Trelox Bot"""
    
    # Bot Configuration
    BOT_TOKEN: str = field(default_factory=lambda: os.getenv("BOT_TOKEN", ""))
    
    # AI Configuration
    AI_API_KEY: Optional[str] = field(default_factory=lambda: os.getenv("AI_API_KEY"))
    
    # Database Configuration
    DATABASE_URL: str = field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///trelox_bot.db"))
    
    # Performance Settings
    MAX_NEWS_ITEMS: int = int(os.getenv("MAX_NEWS_ITEMS", "10"))
    RSS_TIMEOUT: int = int(os.getenv("RSS_TIMEOUT", "10"))
    MAX_CONCURRENT_FETCHES: int = int(os.getenv("MAX_CONCURRENT_FETCHES", "5"))
    
    # Cache Settings
    ENABLE_CACHE: bool = os.getenv("ENABLE_CACHE", "true").lower() == "true"
    CACHE_DURATION: int = int(os.getenv("CACHE_DURATION", "300"))  # 5 minutes
    
    # Scheduled News
    ENABLE_SCHEDULED_NEWS: bool = os.getenv("ENABLE_SCHEDULED_NEWS", "true").lower() == "true"
    DAILY_NEWS_HOUR: int = int(os.getenv("DAILY_NEWS_HOUR", "9"))
    DAILY_NEWS_MINUTE: int = int(os.getenv("DAILY_NEWS_MINUTE", "0"))
    
    # User Preferences
    DEFAULT_NOTIFICATIONS: bool = os.getenv("DEFAULT_NOTIFICATIONS", "true").lower() == "true"
    DEFAULT_AI_SUMMARIES: bool = os.getenv("DEFAULT_AI_SUMMARIES", "true").lower() == "true"
    DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "ar")
    
    # Rate Limiting
    ENABLE_RATE_LIMITING: bool = os.getenv("ENABLE_RATE_LIMITING", "true").lower() == "true"
    MAX_REQUESTS_PER_MINUTE: int = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "30"))
    MAX_REQUESTS_PER_HOUR: int = int(os.getenv("MAX_REQUESTS_PER_HOUR", "100"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE")
    ENABLE_FILE_LOGGING: bool = os.getenv("ENABLE_FILE_LOGGING", "false").lower() == "true"
    
    # Security
    ALLOWED_USERS: List[int] = field(default_factory=lambda: [])
    ADMIN_USER_IDS: List[int] = field(default_factory=lambda: [])
    ENABLE_USER_REGISTRATION: bool = os.getenv("ENABLE_USER_REGISTRATION", "true").lower() == "true"
    
    # Features
    ENABLE_AI_SUMMARIES: bool = True  # Always available if AI_API_KEY is set
    ENABLE_FAVORITES: bool = os.getenv("ENABLE_FAVORITES", "true").lower() == "true"
    ENABLE_USER_STATS: bool = os.getenv("ENABLE_USER_STATS", "true").lower() == "true"
    ENABLE_NOTIFICATIONS: bool = os.getenv("ENABLE_NOTIFICATIONS", "true").lower() == "true"
    
    # RSS Settings
    RSS_USER_AGENT: str = os.getenv("RSS_USER_AGENT", "TreloxBot/1.0 (News Bot)")
    RSS_MAX_ITEMS_PER_SOURCE: int = int(os.getenv("RSS_MAX_ITEMS_PER_SOURCE", "10"))
    
    # Message Formatting
    MAX_MESSAGE_LENGTH: int = 4096  # Telegram's message limit
    TRUNCATED_SUMMARY_LENGTH: int = int(os.getenv("TRUNCATED_SUMMARY_LENGTH", "150"))
    
    # Database Settings
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "5"))
    DATABASE_TIMEOUT: int = int(os.getenv("DATABASE_TIMEOUT", "30"))
    
    # Backup Settings
    ENABLE_BACKUP: bool = os.getenv("ENABLE_BACKUP", "false").lower() == "true"
    BACKUP_INTERVAL_HOURS: int = int(os.getenv("BACKUP_INTERVAL_HOURS", "24"))
    BACKUP_RETENTION_DAYS: int = int(os.getenv("BACKUP_RETENTION_DAYS", "7"))
    
    # API Limits
    TELEGRAM_API_TIMEOUT: int = int(os.getenv("TELEGRAM_API_TIMEOUT", "30"))
    EXTERNAL_API_TIMEOUT: int = int(os.getenv("EXTERNAL_API_TIMEOUT", "10"))
    
    # Development Settings
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "false").lower() == "true"
    DEVELOPMENT_MODE: bool = os.getenv("DEVELOPMENT_MODE", "false").lower() == "true"
    
    def __post_init__(self):
        """Validate configuration after initialization"""
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN environment variable is required")
        
        # Validate time settings
        if not (0 <= self.DAILY_NEWS_HOUR <= 23):
            raise ValueError("DAILY_NEWS_HOUR must be between 0 and 23")
        
        if not (0 <= self.DAILY_NEWS_MINUTE <= 59):
            raise ValueError("DAILY_NEWS_MINUTE must be between 0 and 59")
            
        # Validate numeric settings
        if self.MAX_NEWS_ITEMS <= 0:
            raise ValueError("MAX_NEWS_ITEMS must be positive")
            
        if self.RSS_TIMEOUT <= 0:
            raise ValueError("RSS_TIMEOUT must be positive")
            
        if self.MAX_CONCURRENT_FETCHES <= 0:
            raise ValueError("MAX_CONCURRENT_FETCHES must be positive")
    
    def get_rss_config(self) -> dict:
        """Get RSS-specific configuration"""
        return {
            'timeout': self.RSS_TIMEOUT,
            'user_agent': self.RSS_USER_AGENT,
            'max_items': self.RSS_MAX_ITEMS_PER_SOURCE,
            'enable_cache': self.ENABLE_CACHE,
            'cache_duration': self.CACHE_DURATION
        }
    
    def get_database_config(self) -> dict:
        """Get database-specific configuration"""
        return {
            'database_url': self.DATABASE_URL,
            'pool_size': self.DATABASE_POOL_SIZE,
            'timeout': self.DATABASE_TIMEOUT,
            'enable_backup': self.ENABLE_BACKUP,
            'backup_interval_hours': self.BACKUP_INTERVAL_HOURS,
            'backup_retention_days': self.BACKUP_RETENTION_DAYS
        }
    
    def get_bot_config(self) -> dict:
        """Get bot-specific configuration"""
        return {
            'token': self.BOT_TOKEN,
            'ai_api_key': self.AI_API_KEY,
            'max_news_items': self.MAX_NEWS_ITEMS,
            'enable_scheduled_news': self.ENABLE_SCHEDULED_NEWS,
            'daily_news_hour': self.DAILY_NEWS_HOUR,
            'daily_news_minute': self.DAILY_NEWS_MINUTE,
            'enable_rate_limiting': self.ENABLE_RATE_LIMITING,
            'max_requests_per_minute': self.MAX_REQUESTS_PER_MINUTE,
            'max_requests_per_hour': self.MAX_REQUESTS_PER_HOUR,
            'enable_ai_summaries': self.ENABLE_AI_SUMMARIES,
            'enable_favorites': self.ENABLE_FAVORITES,
            'enable_user_stats': self.ENABLE_USER_STATS,
            'enable_notifications': self.ENABLE_NOTIFICATIONS,
            'debug_mode': self.DEBUG_MODE,
            'development_mode': self.DEVELOPMENT_MODE
        }
    
    def get_message_config(self) -> dict:
        """Get message formatting configuration"""
        return {
            'max_message_length': self.MAX_MESSAGE_LENGTH,
            'truncated_summary_length': self.TRUNCATED_SUMMARY_LENGTH,
            'default_language': self.DEFAULT_LANGUAGE
        }
    
    def get_logging_config(self) -> dict:
        """Get logging configuration"""
        return {
            'level': self.LOG_LEVEL,
            'file': self.LOG_FILE,
            'enable_file_logging': self.ENABLE_FILE_LOGGING
        }
    
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.DEBUG_MODE or self.DEVELOPMENT_MODE
    
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return not self.is_development()
    
    def get_environment_info(self) -> dict:
        """Get environment information for debugging"""
        return {
            'debug_mode': self.DEBUG_MODE,
            'development_mode': self.DEVELOPMENT_MODE,
            'is_development': self.is_development(),
            'is_production': self.is_production(),
            'log_level': self.LOG_LEVEL,
            'has_ai_key': bool(self.AI_API_KEY),
            'has_database_url': bool(self.DATABASE_URL)
        }

# Default configuration instance
config = Config()

# Validation function
def validate_config() -> bool:
    """Validate that all required configuration is present"""
    try:
        # Test config creation
        _ = Config()
        
        # Check required fields
        if not config.BOT_TOKEN:
            print("❌ BOT_TOKEN is required")
            return False
            
        # Test RSS config
        rss_config = config.get_rss_config()
        if not isinstance(rss_config['timeout'], int) or rss_config['timeout'] <= 0:
            print("❌ Invalid RSS timeout configuration")
            return False
            
        # Test database config
        db_config = config.get_database_config()
        if not db_config['database_url']:
            print("❌ Database URL not configured")
            return False
            
        print("✅ Configuration validation passed")
        return True
        
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Testing configuration...")
    validate_config()
    
    print("\n📋 Current Configuration:")
    print(f"Bot Token: {'✅ Set' if config.BOT_TOKEN else '❌ Missing'}")
    print(f"AI API Key: {'✅ Set' if config.AI_API_KEY else '❌ Missing'}")
    print(f"Database URL: {config.DATABASE_URL}")
    print(f"Debug Mode: {config.DEBUG_MODE}")
    print(f"Max News Items: {config.MAX_NEWS_ITEMS}")
    print(f"Enable AI Summaries: {config.ENABLE_AI_SUMMARIES and bool(config.AI_API_KEY)}")
    print(f"Enable Scheduled News: {config.ENABLE_SCHEDULED_NEWS}")
    print(f"Development Mode: {config.is_development()}")
    print(f"Production Mode: {config.is_production()}")
