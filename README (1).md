# تِريلوكس بوت - بوت الأخبار الذكي 🤖📰

بوت تليجرام متقدم للأخبار باللغة العربية مع ميزات الذكاء الاصطناعي وإدارة المستخدمين

## 🌟 الميزات الرئيسية

### 📰 إدارة الأخبار
- **مصادر متنوعة**: 60+ مصدر أخبار عربي موثوق
- **فئات متعددة**: عام، اقتصاد، سياسة، رياضة، تقنية، صحة، عالم
- **تحديث مستمر**: جلب الأخبار في الوقت الفعلي
- **ذاكرة تخزين مؤقت**: تحسين الأداء وسرعة الاستجابة

### 🤖 الذكاء الاصطناعي
- **تلخيص ذكي**: تلخيص المقالات باستخدام الذكاء الاصطناعي
- **تحليل المحتوى**: فهم وتحليل النصوص العربية
- **اقتراحات ذكية**: توصيات مخصصة للمستخدمين

### 👥 إدارة المستخدمين
- **تسجيل المستخدمين**: إدارة شاملة لبيانات المستخدمين
- **تفضيلات شخصية**: إعدادات مخصصة لكل مستخدم
- **إحصائيات مفصلة**: تتبع استخدام البوت

### ⭐ المفضلة والمراجعيات
- **حفظ المقالات**: إمكانية حفظ المقالات المفضلة
- **قوائم مخصصة**: تنظيم المقالات حسب الفئات
- **سهولة الوصول**: الوصول السريع للمقالات المحفوظة

### 🔔 الإشعارات والجدولة
- **أخبار يومية**: إرسال الأخبار تلقائياً في الوقت المحدد
- **إعدادات مرنة**: تخصيص وقت الإشعارات
- **اختيار المصادر**: تحديد المصادر المفضلة

### 📊 الإحصائيات والتحليلات
- **إحصائيات المستخدمين**: متابعة تفاعل المستخدمين
- **تحليل الأداء**: مراقبة أداء البوت
- **تقارير مفصلة**: تقارير الاستخدام والأداء

## 🏗️ هيكل المشروع

```
trelox-bot/
├── main.py                 # نقطة البداية للتطبيق
├── bot.py                  # المنطق الرئيسي للبوت
├── config.py               # إدارة الإعدادات
├── database.py             # إدارة قاعدة البيانات
├── rss_sources.json        # مصادر الأخبار
├── requirements.txt        # متطلبات Python
├── Procfile               # إعدادات النشر
├── .env                   # متغيرات البيئة
├── .env.example           # نموذج متغيرات البيئة
├── .gitignore             # حماية الملفات الحساسة
└── README.md              # هذه الوثائق
```

## 🚀 التثبيت والإعداد

### متطلبات النظام

- Python 3.8 أو أحدث
- pip أو uv لإدارة الحزم
- SQLite (مدمج مع Python) أو قاعدة بيانات أخرى

### التثبيت المحلي

1. **استنساخ المستودع**
   ```bash
   git clone https://github.com/username/trelox-bot.git
   cd trelox-bot
   ```

2. **إنشاء بيئة افتراضية**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # أو
   venv\Scripts\activate     # Windows
   ```

3. **تثبيت المتطلبات**
   ```bash
   pip install -r requirements.txt
   ```

4. **إعداد متغيرات البيئة**
   ```bash
   cp .env.example .env
   # ثم تحرير .env وإضافة معلوماتك
   ```

5. **تشغيل البوت**
   ```bash
   python main.py
   ```

## ⚙️ الإعدادات

### متغيرات البيئة المطلوبة

```env
# توكن البوت (مطلوب)
BOT_TOKEN=your_bot_token_here

# مفتاح API للذكاء الاصطناعي (اختياري)
AI_API_KEY=your_ai_api_key_here

# إعدادات قاعدة البيانات
DATABASE_URL=sqlite:///trelox_bot.db
```

### إعدادات اختيارية

```env
# إعدادات الأداء
MAX_NEWS_ITEMS=10
RSS_TIMEOUT=10
MAX_CONCURRENT_FETCHES=5

# إعدادات الإشعارات
ENABLE_SCHEDULED_NEWS=true
DAILY_NEWS_HOUR=9
DAILY_NEWS_MINUTE=0

# إعدادات التفاعل
MAX_REQUESTS_PER_MINUTE=30
MAX_REQUESTS_PER_HOUR=100
```

## 🌐 النشر

### نشر على Render

1. **إنشاء حساب على [Render](https://render.com)**
2. **ربط مستودع GitHub**
3. **إنشاء Web Service جديد**
4. **إعداد متغيرات البيئة**
   ```
   BOT_TOKEN=your_bot_token
   AI_API_KEY=your_ai_api_key
   ```
5. **النشر**

### نشر على Railway

1. **إنشاء حساب على [Railway](https://railway.app)**
2. **ربط مستودع GitHub**
3. **إنشاء مشروع جديد**
4. **إضافة متغيرات البيئة**
5. **النشر التلقائي**

### نشر على Heroku

1. **تثبيت Heroku CLI**
2. **تسجيل الدخول**
   ```bash
   heroku login
   ```
3. **إنشاء تطبيق**
   ```bash
   heroku create your-bot-name
   ```
4. **إضافة متغيرات البيئة**
   ```bash
   heroku config:set BOT_TOKEN=your_bot_token
   ```
5. **النشر**
   ```bash
   git push heroku main
   ```

## 📚 واجهة برمجة التطبيقات

### الأوامر المتاحة

| الأمر | الوصف | مثال |
|-------|--------|--------|
| `/start` | بدء استخدام البوت | `/start` |
| `/news` | عرض الأخبار | `/news` |
| `/sources` | قائمة مصادر الأخبار | `/sources` |
| `/favorites` | المقالات المفضلة | `/favorites` |
| `/preferences` | الإعدادات | `/preferences` |
| `/help` | المساعدة | `/help` |
| `/stats` | إحصائيات الاستخدام | `/stats` |

### الوظائف الرئيسية

#### جلب الأخبار
```python
# جلب آخر الأخبار
news_items = await bot.fetch_news_from_all_sources(limit=10)

# جلب الأخبار حسب الفئة
news_items = await bot.fetch_news_by_category("اقتصاد", limit=5)
```

#### إدارة المفضلة
```python
# إضافة إلى المفضلة
await db.add_to_favorites(user_id, title, url, summary)

# الحصول على المفضلة
favorites = await db.get_user_favorites(user_id, limit=20)
```

#### الإعدادات
```python
# الحصول على إعدادات المستخدم
prefs = await db.get_user_preferences(user_id)

# تحديث الإعدادات
await db.update_user_preferences(user_id, {"notifications_enabled": True})
```

## 🔧 التطوير والمساهمة

### إعداد بيئة التطوير

1. **تثبيت أدوات التطوير**
   ```bash
   pip install -r requirements.txt
   pip install black flake8 mypy pytest
   ```

2. **تشغيل الاختبارات**
   ```bash
   pytest
   ```

3. **فحص جودة الكود**
   ```bash
   black .
   flake8 .
   mypy bot.py database.py config.py
   ```

### هيكل قاعدة البيانات

#### جدول المستخدمين (`users`)
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    language_code TEXT DEFAULT 'ar',
    is_premium BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### جدول التفضيلات (`user_preferences`)
```sql
CREATE TABLE user_preferences (
    user_id INTEGER PRIMARY KEY,
    notifications_enabled BOOLEAN DEFAULT TRUE,
    ai_summaries_enabled BOOLEAN DEFAULT TRUE,
    preferred_sources TEXT DEFAULT '[]',
    preferred_categories TEXT DEFAULT '[]',
    daily_news_time TEXT DEFAULT '09:00',
    language TEXT DEFAULT 'ar',
    theme TEXT DEFAULT 'default'
);
```

#### جدول المفضلة (`favorites`)
```sql
CREATE TABLE favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    summary TEXT,
    source TEXT,
    published_date TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 📊 المراقبة والصيانة

### مراقبة الأداء

```python
# الحصول على إحصائيات قاعدة البيانات
stats = await db.get_database_stats()

# تنظيف الذاكرة المؤقتة
await db.cleanup_expired_cache()

# إنشاء نسخة احتياطية
backup_path = await db.backup_database()
```

### سجل الأحداث

```python
import logging

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
```

## 🛠️ استكشاف الأخطاء

### مشاكل شائعة

#### البوت لا يستجيب
- تحقق من صحة `BOT_TOKEN`
- تأكد من تشغيل البوت
- فحص سجلات الأخطاء

#### خطأ في قاعدة البيانات
```bash
# إعادة إنشاء قاعدة البيانات
python -c "from database import db; db.init_database()"
```

#### مشكلة في مصادر RSS
- فحص اتصال الإنترنت
- التحقق من صحة روابط RSS
- مراجعة إعدادات `RSS_TIMEOUT`

### سجل الأخطاء

```
2024-01-15 10:30:15 - INFO - Bot started successfully
2024-01-15 10:30:20 - INFO - User 123456789 started the bot
2024-01-15 10:35:10 - ERROR - Failed to fetch from RSS source: Connection timeout
2024-01-15 10:35:11 - INFO - Cache cleanup completed
```

## 🔒 الأمان

### حماية البيانات

- **تشفير كلمات المرور**: استخدام رموز آمنة
- **التحقق من صحة المدخلات**: فحص البيانات الواردة
- **حماية API**: استخدام مفاتيح محدودة الصلاحيات

### حماية المستودع

```bash
# عدم رفع الملفات الحساسة
echo ".env" >> .gitignore
echo "*.db" >> .gitignore
echo "*.log" >> .gitignore
```

## 📈 إحصائيات المشروع

- **الأسطر**: 2000+ سطر كود
- **الملفات**: 10 ملفات أساسية
- **مصادر الأخبار**: 60+ مصدر عربي
- **الدعم**: 10+ دولة عربية
- **الفئات**: 6 فئات رئيسية

## 🤝 المساهمة

نرحب بالمساهمات! يرجى اتباع هذه الخطوات:

1. **Fork المستودع**
2. **إنشاء فرع جديد**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit التغييرات**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push للفرع**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **إنشاء Pull Request**

### معايير المساهمة

- **التوثيق**: تحديث الوثائق عند الحاجة
- **الاختبارات**: إضافة اختبارات للميزات الجديدة
- **التنسيق**: استخدام `black` لتنسيق الكود
- **الفحص**: تشغيل `flake8` و `mypy`

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.

## 📞 الدعم والتواصل

- **GitHub Issues**: [إنشاء مشكلة](https://github.com/username/trelox-bot/issues)
- **البريد الإلكتروني**: your-email@example.com
- **تليجرام**: [@yourusername](https://t.me/yourusername)

## 🙏 الشكر والتقدير

- **Telegram Bot API**: API للبوتات
- **python-telegram-bot**: مكتبة Python للبوتات
- **feedparser**: مكتبة تحليل RSS
- **Google AI**: خدمات الذكاء الاصطناعي

## 📝 ملاحظات الإصدار

### الإصدار 2.0.0
- ✨ إضافة ميزات الذكاء الاصطناعي
- 🗄️ تحسين إدارة قاعدة البيانات
- 📱 واجهة مستخدم محسنة
- 🔧 إعدادات متقدمة
- 🐛 إصلاح الأخطاء

### الإصدار 1.0.0
- 🚀 الإصدار الأولي
- 📰 إدارة الأخبار الأساسية
- 👥 إدارة المستخدمين
- ⭐ نظام المفضلة

---

**تم التطوير بواسطة MiniMax Agent** 🤖

*بوت الأخبار الذكي - إبق على اطلاع مع أحدث الأخبار العربية* 📰✨