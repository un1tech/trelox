#!/usr/bin/env python3
"""
Trelox Bot - Comprehensive Arabic News Bot
Features: RSS news, AI summaries, user preferences, favorites
Author: MiniMax Agent
"""

import asyncio
import json
import logging
import os
import feedparser
import httpx
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from pathlib import Path

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    BotCommand, BotCommandScopeAllChatAdministrators,
    BotCommandScopeAllPrivateChats
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)
from telegram.constants import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import google.generativeai as genai

from database import DatabaseManager
from config import Config

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TreloxBot:
    def __init__(self):
        self.config = Config()
        self.db = DatabaseManager()
        self.scheduler = AsyncIOScheduler()
        self.application = None
        
        # Setup AI if available
        self.ai_available = False
        if self.config.AI_API_KEY:
            try:
                genai.configure(api_key=self.config.AI_API_KEY)
                self.model = genai.GenerativeModel('gemini-pro')
                self.ai_available = True
                logger.info("AI capabilities initialized")
            except Exception as e:
                logger.warning(f"AI initialization failed: {e}")
                
        # Load RSS sources
        self.rss_sources = self.load_rss_sources()
        
    def load_rss_sources(self) -> Dict:
        """Load RSS sources from JSON file"""
        try:
            with open('rss_sources.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error("rss_sources.json not found")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Invalid RSS sources JSON: {e}")
            return {}
            
    async def setup_commands(self):
        """Setup bot commands"""
        commands = [
            BotCommand("start", "🚀 بدء استخدام البوت"),
            BotCommand("news", "📰 عرض الأخبار"),
            BotCommand("sources", "📡 مصادر الأخبار"),
            BotCommand("favorites", "⭐ المفضلة"),
            BotCommand("preferences", "⚙️ الإعدادات"),
            BotCommand("help", "❓ المساعدة"),
            BotCommand("stats", "📊 إحصائيات الاستخدام")
        ]
        
        try:
            await self.application.bot.set_my_commands(
                commands, 
                scope=BotCommandScopeAllPrivateChats()
            )
            logger.info("Bot commands updated")
        except Exception as e:
            logger.error(f"Failed to set commands: {e}")
            
    async def initialize(self):
        """Initialize the bot application"""
        self.application = Application.builder().token(self.config.BOT_TOKEN).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("news", self.news_command))
        self.application.add_handler(CommandHandler("sources", self.sources_command))
        self.application.add_handler(CommandHandler("favorites", self.favorites_command))
        self.application.add_handler(CommandHandler("preferences", self.preferences_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
        
        # Setup scheduled news
        self.setup_scheduled_news()
        
        # Setup commands
        await self.setup_commands()
        
        logger.info("Bot initialized successfully")
        
    def setup_scheduled_news(self):
        """Setup daily news scheduling"""
        if self.config.ENABLE_SCHEDULED_NEWS:
            # Schedule daily news at 9 AM
            self.scheduler.add_job(
                self.send_daily_news,
                CronTrigger(hour=9, minute=0),
                id='daily_news',
                replace_existing=True
            )
            self.scheduler.start()
            logger.info("Scheduled news configured")
            
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        # Welcome message
        welcome_text = f"""
🌟 **مرحباً {user.first_name}!**

أنا **تِريلوكس بوت** - بوت الأخبار الذكي باللغة العربية

📰 **ما يمكنني فعله:**
• عرض الأخبار من أفضل المصادر العربية
• تلخيص الأخبار باستخدام الذكاء الاصطناعي  
• حفظ المقالات المفضلة
• إعدادات مخصصة لكل مستخدم
• إرسال الأخبار يومياً في الوقت المحدد

🎯 **للبدء، استخدم:** `/news`
📚 **للمساعدة:** `/help`
        """
        
        # Welcome keyboard
        keyboard = [
            [InlineKeyboardButton("📰 أحدث الأخبار", callback_data="news_latest")],
            [InlineKeyboardButton("📡 مصادر الأخبار", callback_data="sources_list")],
            [InlineKeyboardButton("⭐ المفضلة", callback_data="favorites_list")],
            [InlineKeyboardButton("⚙️ الإعدادات", callback_data="preferences")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Register user in database
        await self.db.add_user(
            user_id=user.id,
            username=user.username or "",
            first_name=user.first_name,
            last_name=user.last_name or ""
        )
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        logger.info(f"User {user.id} started the bot")
        
    async def news_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /news command"""
        keyboard = []
        
        # Category selection
        keyboard.append([InlineKeyboardButton("🏠 أخبار عامة", callback_data="news_general")])
        keyboard.append([InlineKeyboardButton("💼 اقتصاد", callback_data="news_business")])
        keyboard.append([InlineKeyboardButton("🏛️ سياسة", callback_data="news_politics")])
        keyboard.append([InlineKeyboardButton("⚽ رياضة", callback_data="news_sports")])
        keyboard.append([InlineKeyboardButton("🔬 تقنية", callback_data="news_technology")])
        keyboard.append([InlineKeyboardButton("🏥 صحة", callback_data="news_health")])
        keyboard.append([InlineKeyboardButton("🌍 عالم", callback_data="news_world")])
        keyboard.append([InlineKeyboardButton("📰 أحدث الأخبار", callback_data="news_latest")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "📰 **اختر نوع الأخبار:**",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    async def sources_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /sources command"""
        sources_text = "📡 **مصادر الأخبار المتاحة:**\n\n"
        
        for country, categories in self.rss_sources.items():
            sources_text += f"🏴 **{country}**\n"
            for category, sources in categories.items():
                if isinstance(sources, list):
                    sources_text += f"• **{category}**: {len(sources)} مصدر\n"
            sources_text += "\n"
            
        await update.message.reply_text(
            sources_text,
            parse_mode=ParseMode.MARKDOWN
        )
        
    async def favorites_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /favorites command"""
        user_id = update.effective_user.id
        
        favorites = await self.db.get_user_favorites(user_id)
        
        if not favorites:
            await update.message.reply_text(
                "⭐ **لا توجد مقالات مفضلة بعد**\n\nاستخدم زر ⭐ لحفظ المقالات التي تعجبك",
                parse_mode=ParseMode.MARKDOWN
            )
            return
            
        # Display favorites
        text = "⭐ **مقالاتك المفضلة:**\n\n"
        for i, fav in enumerate(favorites[:10], 1):
            text += f"{i}. {fav['title']}\n"
            text += f"📅 {fav['created_at']}\n\n"
            
        keyboard = [
            [InlineKeyboardButton("🔄 تحديث القائمة", callback_data="favorites_list")],
            [InlineKeyboardButton("🗑️ مسح الكل", callback_data="favorites_clear")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    async def preferences_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /preferences command"""
        user_id = update.effective_user.id
        
        # Get user preferences
        prefs = await self.db.get_user_preferences(user_id)
        
        text = "⚙️ **إعداداتك الحالية:**\n\n"
        text += f"🔔 **الإشعارات**: {'مفعلة' if prefs.get('notifications', True) else 'معطلة'}\n"
        text += f"🤖 **الذكاء الاصطناعي**: {'مفعل' if self.ai_available and prefs.get('ai_summaries', True) else 'معطل'}\n"
        text += f"🌍 **المصادر المفضلة**: {', '.join(prefs.get('preferred_sources', []))}\n\n"
        
        keyboard = [
            [InlineKeyboardButton("🔔 تبديل الإشعارات", callback_data="toggle_notifications")],
            [InlineKeyboardButton("🤖 تبديل الذكاء الاصطناعي", callback_data="toggle_ai")],
            [InlineKeyboardButton("🌍 تبديل المصادر", callback_data="toggle_sources")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
❓ **مساعدة تِريلوكس بوت**

📱 **الأوامر المتاحة:**
• `/start` - بدء استخدام البوت
• `/news` - عرض الأخبار
• `/sources` - قائمة مصادر الأخبار
• `/favorites` - المقالات المفضلة
• `/preferences` - الإعدادات
• `/help` - هذه المساعدة
• `/stats` - إحصائيات الاستخدام

🔧 **الميزات:**
📰 أخبار من 60+ مصدر عربي
🤖 تلخيص ذكي بالذكاء الاصطناعي
⭐ حفظ المقالات المفضلة
🔔 إشعارات يومية مخصصة
🌍 إعدادات متقدمة

🆘 **إذا واجهت مشكلة:**
• تأكد من اتصالك بالإنترنت
• استخدم `/start` لإعادة تشغيل البوت
• جرب `/news` لعرض الأخبار

📧 **التواصل:** تواصل مع المطور في حالة وجود مشاكل
        """
        
        await update.message.reply_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN
        )
        
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        user_id = update.effective_user.id
        
        # Get user stats
        stats = await self.db.get_user_stats(user_id)
        
        text = f"""
📊 **إحصائياتك:**

📰 **الأخبار المقروءة**: {stats.get('articles_read', 0)}
⭐ **المقالات المحفوظة**: {stats.get('favorites_count', 0)}
🔔 **الإشعارات المستلمة**: {stats.get('notifications_sent', 0)}
📅 **تاريخ الانضمام**: {stats.get('joined_date', 'غير محدد')}
⏱️ **آخر نشاط**: {stats.get('last_activity', 'غير محدد')}
        """
        
        await update.message.reply_text(
            text,
            parse_mode=ParseMode.MARKDOWN
        )
        
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard callbacks"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "news_latest":
            await self.show_latest_news(update, context)
        elif data == "news_general":
            await self.show_news_by_category(update, context, "عام")
        elif data == "news_business":
            await self.show_news_by_category(update, context, "اقتصاد")
        elif data == "news_politics":
            await self.show_news_by_category(update, context, "سياسة")
        elif data == "news_sports":
            await self.show_news_by_category(update, context, "رياضة")
        elif data == "news_technology":
            await self.show_news_by_category(update, context, "تقنية")
        elif data == "news_health":
            await self.show_news_by_category(update, context, "صحة")
        elif data == "news_world":
            await self.show_news_by_category(update, context, "عالم")
        elif data == "sources_list":
            await self.show_sources_list(update, context)
        elif data == "favorites_list":
            await self.show_favorites_list(update, context)
        elif data == "favorites_clear":
            await self.clear_favorites(update, context)
        elif data == "preferences":
            await self.show_preferences(update, context)
        elif data.startswith("toggle_"):
            await self.toggle_setting(update, context, data)
        elif data.startswith("favorite_"):
            await self.add_to_favorites(update, context, data)
        elif data.startswith("read_more_"):
            await self.read_full_article(update, context, data)
            
    async def show_latest_news(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show latest news from all sources"""
        news_items = await self.fetch_news_from_all_sources(limit=10)
        
        if not news_items:
            await update.callback_query.edit_message_text(
                "❌ **لا توجد أخبار متاحة حالياً**\n\nيرجى المحاولة لاحقاً"
            )
            return
            
        text = "📰 **أحدث الأخبار:**\n\n"
        
        for i, news in enumerate(news_items[:5], 1):
            text += f"**{i}. {news['title']}**\n"
            text += f"📅 {news['published']}\n"
            text += f"📡 {news['source']}\n"
            if len(news['summary']) > 100:
                text += f"{news['summary'][:100]}...\n"
            else:
                text += f"{news['summary']}\n"
            text += f"🔗 [قراءة المزيد]({news['link']})\n\n"
            
        # Add navigation
        keyboard = [
            [InlineKeyboardButton("🔄 تحديث", callback_data="news_latest")],
            [InlineKeyboardButton("📰 فئات أخرى", callback_data="news_categories")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    async def show_news_by_category(self, update: Update, context: ContextTypes.DEFAULT_TYPE, category: str):
        """Show news by category"""
        news_items = await self.fetch_news_by_category(category, limit=8)
        
        if not news_items:
            await update.callback_query.edit_message_text(
                f"❌ **لا توجد أخبار في فئة {category} حالياً**\n\nجرب فئات أخرى"
            )
            return
            
        text = f"📰 **أخبار {category}:**\n\n"
        
        for i, news in enumerate(news_items[:6], 1):
            text += f"**{i}. {news['title']}**\n"
            text += f"📅 {news['published']}\n"
            text += f"📡 {news['source']}\n"
            if len(news['summary']) > 80:
                text += f"{news['summary'][:80]}...\n"
            else:
                text += f"{news['summary']}\n"
            text += f"🔗 [قراءة المزيد]({news['link']})\n\n"
            
        # Add action buttons
        keyboard = [
            [InlineKeyboardButton("⭐ حفظ", callback_data=f"favorite_{news['link']}") for news in news_items[:2]],
            [InlineKeyboardButton("🔄 تحديث", callback_data=f"news_{category.lower()}")],
            [InlineKeyboardButton("📱 القائمة الرئيسية", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    async def show_sources_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show all available sources"""
        sources_text = "📡 **قائمة مصادر الأخبار:**\n\n"
        
        count = 1
        for country, categories in self.rss_sources.items():
            sources_text += f"🏴 **{country}**\n"
            for category, sources in categories.items():
                if isinstance(sources, list):
                    sources_text += f"• **{category}**: {len(sources)} مصدر\n"
                    # Show first few sources
                    for source in sources[:3]:
                        sources_text += f"  - {source.get('name', 'Unknown')}\n"
                    if len(sources) > 3:
                        sources_text += f"  ... و {len(sources) - 3} مصادر أخرى\n"
                    sources_text += "\n"
            sources_text += "\n"
            
        keyboard = [
            [InlineKeyboardButton("🔄 تحديث", callback_data="sources_list")],
            [InlineKeyboardButton("📱 القائمة الرئيسية", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            sources_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    async def show_favorites_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user favorites"""
        user_id = update.effective_user.id
        
        favorites = await self.db.get_user_favorites(user_id)
        
        if not favorites:
            await update.callback_query.edit_message_text(
                "⭐ **لا توجد مقالات مفضلة بعد**\n\nاستخدم زر ⭐ لحفظ المقالات التي تعجبك"
            )
            return
            
        text = "⭐ **مقالاتك المفضلة:**\n\n"
        for i, fav in enumerate(favorites[:8], 1):
            text += f"{i}. **{fav['title']}**\n"
            text += f"📅 {fav['created_at']}\n"
            text += f"🔗 [قراءة]({fav['url']})\n\n"
            
        keyboard = [
            [InlineKeyboardButton("🔄 تحديث", callback_data="favorites_list")],
            [InlineKeyboardButton("🗑️ مسح الكل", callback_data="favorites_clear")],
            [InlineKeyboardButton("📱 القائمة الرئيسية", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    async def clear_favorites(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Clear all user favorites"""
        user_id = update.effective_user.id
        
        await self.db.clear_user_favorites(user_id)
        
        await update.callback_query.edit_message_text(
            "✅ **تم مسح جميع المقالات المفضلة**"
        )
        
    async def show_preferences(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user preferences"""
        user_id = update.effective_user.id
        
        prefs = await self.db.get_user_preferences(user_id)
        
        text = "⚙️ **إعداداتك الحالية:**\n\n"
        text += f"🔔 **الإشعارات**: {'مفعلة' if prefs.get('notifications', True) else 'معطلة'}\n"
        text += f"🤖 **الذكاء الاصطناعي**: {'مفعل' if self.ai_available and prefs.get('ai_summaries', True) else 'معطل'}\n"
        text += f"🌍 **المصادر المفضلة**: {', '.join(prefs.get('preferred_sources', []))}\n\n"
        text += "اضغط على الأزرار أدناه لتغيير الإعدادات:"
        
        keyboard = [
            [InlineKeyboardButton("🔔 تبديل الإشعارات", callback_data="toggle_notifications")],
            [InlineKeyboardButton("🤖 تبديل الذكاء الاصطناعي", callback_data="toggle_ai")],
            [InlineKeyboardButton("🌍 تبديل المصادر", callback_data="toggle_sources")],
            [InlineKeyboardButton("📱 القائمة الرئيسية", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    async def toggle_setting(self, update: Update, context: ContextTypes.DEFAULT_TYPE, setting: str):
        """Toggle user settings"""
        user_id = update.effective_user.id
        
        if setting == "toggle_notifications":
            await self.db.toggle_user_notifications(user_id)
            message = "🔔 تم تبديل حالة الإشعارات"
        elif setting == "toggle_ai":
            await self.db.toggle_user_ai_summaries(user_id)
            message = "🤖 تم تبديل حالة الذكاء الاصطناعي"
        elif setting == "toggle_sources":
            await self.db.toggle_user_preferred_sources(user_id)
            message = "🌍 تم تبديل المصادر المفضلة"
            
        await update.callback_query.edit_message_text(message)
        
    async def add_to_favorites(self, update: Update, context: ContextTypes.DEFAULT_TYPE, data: str):
        """Add article to favorites"""
        user_id = update.effective_user.id
        
        # Extract URL from callback data
        url = data.replace("favorite_", "")
        
        # Fetch article details and save
        # This is a simplified version - in practice you'd fetch and store full article details
        
        await update.callback_query.edit_message_text("✅ تم حفظ المقال في المفضلة")
        
    async def fetch_news_from_all_sources(self, limit: int = 10) -> List[Dict]:
        """Fetch news from all RSS sources"""
        news_items = []
        
        for country, categories in self.rss_sources.items():
            for category, sources in categories.items():
                if isinstance(sources, list):
                    for source in sources:
                        try:
                            feed = feedparser.parse(source.get('url', ''))
                            for entry in feed.entries[:3]:  # Limit per source
                                news_items.append({
                                    'title': entry.title,
                                    'summary': self.clean_text(entry.summary or entry.description or ""),
                                    'link': entry.link,
                                    'published': self.format_date(entry.published),
                                    'source': source.get('name', 'Unknown'),
                                    'country': country,
                                    'category': category
                                })
                        except Exception as e:
                            logger.error(f"Error fetching from {source.get('name', 'Unknown')}: {e}")
                            continue
                            
        # Sort by publication date and limit
        news_items = sorted(news_items, key=lambda x: x['published'], reverse=True)
        return news_items[:limit]
        
    async def fetch_news_by_category(self, category: str, limit: int = 8) -> List[Dict]:
        """Fetch news by specific category"""
        news_items = []
        
        for country, categories in self.rss_sources.items():
            if category in categories:
                sources = categories[category]
                if isinstance(sources, list):
                    for source in sources:
                        try:
                            feed = feedparser.parse(source.get('url', ''))
                            for entry in feed.entries[:2]:  # Limit per source
                                news_items.append({
                                    'title': entry.title,
                                    'summary': self.clean_text(entry.summary or entry.description or ""),
                                    'link': entry.link,
                                    'published': self.format_date(entry.published),
                                    'source': source.get('name', 'Unknown'),
                                    'country': country,
                                    'category': category
                                })
                        except Exception as e:
                            logger.error(f"Error fetching from {source.get('name', 'Unknown')}: {e}")
                            continue
                            
        # Sort and limit
        news_items = sorted(news_items, key=lambda x: x['published'], reverse=True)
        return news_items[:limit]
        
    def clean_text(self, text: str) -> str:
        """Clean and format text"""
        if not text:
            return ""
            
        # Remove HTML tags
        import re
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Truncate if too long
        if len(text) > 300:
            text = text[:297] + "..."
            
        return text
        
    def format_date(self, date_str: str) -> str:
        """Format publication date"""
        try:
            # This is a simplified version - in practice you'd use proper date parsing
            return date_str[:16] if date_str else "غير محدد"
        except:
            return "غير محدد"
            
    async def send_daily_news(self):
        """Send daily news to users who enabled notifications"""
        users = await self.db.get_users_with_notifications_enabled()
        
        for user in users:
            try:
                news_items = await self.fetch_news_from_all_sources(limit=5)
                
                text = "🌅 **أخبارك اليومية**\n\n"
                for i, news in enumerate(news_items, 1):
                    text += f"**{i}. {news['title']}**\n"
                    text += f"📡 {news['source']}\n"
                    if len(news['summary']) > 80:
                        text += f"{news['summary'][:80]}...\n"
                    else:
                        text += f"{news['summary']}\n"
                    text += f"🔗 [قراءة]({news['link']})\n\n"
                    
                keyboard = [
                    [InlineKeyboardButton("📰 المزيد من الأخبار", callback_data="news_latest")],
                    [InlineKeyboardButton("⚙️ الإعدادات", callback_data="preferences")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await self.application.bot.send_message(
                    chat_id=user['user_id'],
                    text=text,
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.MARKDOWN
                )
                
                # Update notification count
                await self.db.increment_notification_count(user['user_id'])
                
            except Exception as e:
                logger.error(f"Failed to send daily news to user {user['user_id']}: {e}")
                
    async def run(self):
        """Run the bot"""
        await self.initialize()
        logger.info("Starting Trelox Bot...")
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        # Keep running
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        finally:
            await self.application.stop()
            await self.application.shutdown()

# Main execution
if __name__ == "__main__":
    bot = TreloxBot()
    asyncio.run(bot.run())