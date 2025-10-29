# دليل النشر الشامل لتِريلوكس بوت 🚀

دليل مفصل لنشر بوت الأخبار الذكي على منصات مختلفة

## 📋 قائمة المراجعة قبل النشر

### ✅ التحقق من المتطلبات

- [ ] **BOT_TOKEN** مُحدَّث في ملف `.env`
- [ ] **AI_API_KEY** مُحدد (اختياري)
- [ ] جميع الملفات المطلوبة موجودة
- [ ] متغيرات البيئة مُحدَّثة
- [ ] نسخة احتياطية من البيانات (إن وجدت)

### ✅ فحص الكود

- [ ] لا توجد أخطاء في الكود
- [ ] جميع المسارات صحيحة
- [ ] متغيرات البيئة محمية
- [ ] إعدادات قاعدة البيانات صحيحة

### ✅ اختبار محلي

- [ ] البوت يعمل محلياً بدون أخطاء
- [ ] أمر `/start` يعمل
- [ ] جلب الأخبار يعمل
- [ ] حفظ المفضلة يعمل

---

## 🌐 نشر على Render (الأسهل)

### الخطوة 1: تحضير المستودع

1. **رفع الملفات إلى GitHub**
   ```bash
   git add .
   git commit -m "Initial commit: Trelox Bot"
   git branch -M main
   git remote add origin https://github.com/USERNAME/trelox-bot.git
   git push -u origin main
   ```

2. **تحديث ملف .env**
   ```env
   BOT_TOKEN=8250505483:AAGzegCCd-6QQuXwsvvH_POlcmsnnomoNHU
   AI_API_KEY=your_ai_api_key_here
   ```

### الخطوة 2: إنشاء مشروع على Render

1. **تسجيل الدخول**: [render.com](https://render.com)
2. **إنشاء Web Service جديد**
   - Connect to GitHub
   - اختيار المستودع
   - Root Directory: (اتركه فارغاً)
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`

### الخطوة 3: إعداد متغيرات البيئة

في لوحة تحكم Render:
```
Environment: Environment Variables
Add Variables:
- BOT_TOKEN = 8250505483:AAGzegCCd-6QQuXwsvvH_POlcmsnnomoNHU
- AI_API_KEY = your_ai_api_key (اختياري)
- ENVIRONMENT = production
```

### الخطوة 4: النشر والمراقبة

1. **النشر**: سيتم تلقائياً
2. **المراقبة**: Check logs for any errors
3. **الاختبار**: `/start` command على البوت

### ✅ مزايا Render
- ✅ سهل الاستخدام
- ✅ نشر تلقائي
- ✅ مجاني للبداية
- ✅ لوحة تحكم بسيطة

---

## 🚂 نشر على Railway

### الخطوة 1: تحضير المشروع

1. **تحديث Procfile** (إذا لم يكن موجود):
   ```
   worker: python main.py
   ```

2. **ضبط package.json** (إن لم يكن موجود):
   ```json
   {
     "name": "trelox-bot",
     "version": "1.0.0",
     "main": "main.py",
     "scripts": {
       "start": "python main.py"
     }
   }
   ```

### الخطوة 2: إنشاء مشروع على Railway

1. **تسجيل الدخول**: [railway.app](https://railway.app)
2. **إنشاء مشروع جديد**
   - Deploy from GitHub repo
   - اختر المستودع

### الخطوة 3: إعداد متغيرات البيئة

```
Variables:
- BOT_TOKEN = 8250505483:AAGzegCCd-6QQuXwsvvH_POlcmsnnomoNHU
- AI_API_KEY = your_ai_api_key
- RAILWAY_ENVIRONMENT = production
```

### الخطوة 4: النشر

1. **Deploy**: سيتم تلقائياً
2. **Logs**: مراقبة السجلات
3. **Domain**: الحصول على URL البوت

### ✅ مزايا Railway
- ✅ سرعة في النشر
- ✅ شبكةRailway
- ✅ اتصالات آمنة
- ✅ تدرج سهل

---

## 🦾 نشر على Heroku

### الخطوة 1: تثبيت Heroku CLI

**Windows:**
```bash
# تحميل من الموقع الرسمي
https://devcenter.heroku.com/articles/heroku-cli
```

**macOS:**
```bash
brew install heroku/brew/heroku
```

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

### الخطوة 2: إعداد Heroku

1. **تسجيل الدخول:**
   ```bash
   heroku login
   ```

2. **إنشاء تطبيق:**
   ```bash
   heroku create your-trelox-bot-name
   ```

3. **إضافة Buildpack لـ Python:**
   ```bash
   heroku buildpacks:set heroku/python
   ```

### الخطوة 3: إعداد متغيرات البيئة

```bash
heroku config:set BOT_TOKEN=8250505483:AAGzegCCd-6QQuXwsvvH_POlcmsnnomoNHU
heroku config:set AI_API_KEY=your_ai_api_key
heroku config:set ENVIRONMENT=production
```

### الخطوة 4: النشر

```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### الخطوة 5: تشغيل البوت

```bash
heroku ps:scale worker=1
```

### ✅ مزايا Heroku
- ✅ منصة متقدمة
- ✅ دعم ممتاز
- ✅ عدد كبير من Add-ons
- ✅ نشر موثوق

---

## 🌊 نشر على Fly.io

### الخطوة 1: تثبيت Fly CLI

**macOS:**
```bash
brew install flyctl
```

**Windows/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

### الخطوة 2: إعداد Fly

1. **تسجيل الدخول:**
   ```bash
   fly auth login
   ```

2. **إنشاء تطبيق:**
   ```bash
   fly apps create trelox-bot
   ```

### الخطوة 3: إنشاء fly.toml

```toml
app = "trelox-bot"
primary_region = "ams"

[build]
  builder = "paketobuildpacks/builder:jammy-base"

[[services]]
  internal_port = 8080
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443

[env]
  PORT = "8080"

[processes]
  worker = "python main.py"
```

### الخطوة 4: النشر

```bash
fly deploy
```

---

## ☁️ نشر على DigitalOcean

### الخطوة 1: تحضير App Spec

**appspec.yaml:**
```yaml
name: trelox-bot
services:
- name: worker
  source_dir: /
  github:
    repo: your-username/trelox-bot
    branch: main
    deploy_on_push: true
  run_command: python main.py
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: BOT_TOKEN
    value: 8250505483:AAGzegCCd-6QQuXwsvvH_POlcmsnnomoNHU
    type: SECRET
  - key: AI_API_KEY
    value: your_ai_api_key
    type: SECRET
```

### الخطوة 2: نشر

1. **رفع App Spec** إلى DigitalOcean
2. **تفعيل النشر التلقائي**
3. **مراقبة التطبيق**

---

## 🐳 نشر بـ Docker

### إنشاء Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "main.py"]
```

### بناء وتشغيل

```bash
# بناء الصورة
docker build -t trelox-bot .

# تشغيل الحاوية
docker run -d \
  --name trelox-bot \
  -e BOT_TOKEN=8250505483:AAGzegCCd-6QQuXwsvvH_POlcmsnnomoNHU \
  -e AI_API_KEY=your_ai_api_key \
  trelox-bot
```

### Docker Compose

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  bot:
    build: .
    environment:
      - BOT_TOKEN=8250505483:AAGzegCCd-6QQuXwsvvH_POlcmsnnomoNHU
      - AI_API_KEY=your_ai_api_key
      - ENVIRONMENT=production
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

---

## 🖥️ نشر على VPS (Linux)

### الخطوة 1: إعداد الخادم

```bash
# تحديث النظام
sudo apt update && sudo apt upgrade -y

# تثبيت Python و pip
sudo apt install python3 python3-pip python3-venv git -y

# إنشاء مستخدم للبوت
sudo adduser trelox-bot
sudo usermod -aG sudo trelox-bot
```

### الخطوة 2: تحضير التطبيق

```bash
# الانتقال لمجلد المستخدم
cd /home/trelox-bot

# استنساخ المستودع
git clone https://github.com/your-username/trelox-bot.git
cd trelox-bot

# إنشاء بيئة افتراضية
python3 -m venv venv
source venv/bin/activate

# تثبيت المتطلبات
pip install -r requirements.txt
```

### الخطوة 3: إعداد متغيرات البيئة

```bash
# إنشاء ملف .env
cat > .env << EOF
BOT_TOKEN=8250505483:AAGzegCCd-6QQuXwsvvH_POlcmsnnomoNHU
AI_API_KEY=your_ai_api_key
ENVIRONMENT=production
DATABASE_URL=sqlite:///home/trelox-bot/trelox_bot.db
EOF
```

### الخطوة 4: إنشاء خدمة systemd

**/etc/systemd/system/trelox-bot.service:**
```ini
[Unit]
Description=Trelox Bot
After=network.target

[Service]
Type=simple
User=trelox-bot
WorkingDirectory=/home/trelox-bot
Environment=PATH=/home/trelox-bot/venv/bin
ExecStart=/home/trelox-bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# تفعيل الخدمة
sudo systemctl daemon-reload
sudo systemctl enable trelox-bot
sudo systemctl start trelox-bot

# مراقبة الحالة
sudo systemctl status trelox-bot
sudo journalctl -u trelox-bot -f
```

---

## 🔧 اختبار البوت

### 1. اختبار محلي

```bash
python main.py
```

### 2. اختبار الاستجابات

في تليجرام، إرسال:
- `/start` - يجب أن تستجيب بالترحيب
- `/news` - يجب أن تظهر قائمة الأخبار
- `/help` - يجب أن تظهر المساعدة

### 3. فحص السجلات

```bash
# عرض السجلات
tail -f trelox_bot.log

# أو في Docker
docker logs trelox-bot

# أو في systemd
journalctl -u trelox-bot -f
```

---

## 🛠️ مراقبة وإدارة

### مراقبة الأداء

```bash
# فحص استخدام الموارد
top
htop
ps aux | grep python

# فحص اتصال قاعدة البيانات
sqlite3 trelox_bot.db "SELECT COUNT(*) FROM users;"

# فحص حجم قاعدة البيانات
ls -lh trelox_bot.db
```

### النسخ الاحتياطية

```bash
# نسخة احتياطية لقاعدة البيانات
cp trelox_bot.db "backup_$(date +%Y%m%d_%H%M%S).db"

# نسخة احتياطية تلقائية
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp trelox_bot.db "/backups/trelox_bot_$DATE.db"
find /backups -name "trelox_bot_*.db" -mtime +7 -delete
```

### التحديث

```bash
# تحديث الكود
git pull origin main
pip install -r requirements.txt

# إعادة تشغيل البوت
sudo systemctl restart trelox-bot

# أو في Docker
docker pull your-username/trelox-bot:latest
docker-compose up -d --force-recreate
```

---

## 🐛 حل المشاكل الشائعة

### مشكلة: البوت لا يستجيب

```bash
# فحص حالة البوت
sudo systemctl status trelox-bot

# فحص السجلات
sudo journalctl -u trelox-bot --since "1 hour ago"

# فحص الاتصال
curl -X GET "https://api.telegram.org/bot<BOT_TOKEN>/getMe"
```

### مشكلة: خطأ في قاعدة البيانات

```bash
# فحص وجود الملف
ls -la trelox_bot.db

# إعادة إنشاء قاعدة البيانات
python -c "from database import db; db.init_database()"

# فحص الصلاحيات
sudo chown trelox-bot:trelox-bot trelox_bot.db
chmod 644 trelox_bot.db
```

### مشكلة: RSS لا يعمل

```bash
# فحص اتصال الإنترنت
ping google.com

# اختبار RSS مباشر
curl -I "https://www.alarabiya.net/rss.xml"

# فحص إعدادات DNS
nslookup alarabiya.net
```

### مشكلة: ذاكرة مُفرطة

```bash
# مراقبة استخدام الذاكرة
free -h
ps aux --sort=-%mem | head

# تحسين إعدادات قاعدة البيانات
# إضافة فهارس في database.py
```

---

## 📈 تحسين الأداء

### تحسين قاعدة البيانات

```sql
-- إضافة فهارس
CREATE INDEX idx_users_last_activity ON users (last_activity);
CREATE INDEX idx_favorites_user_id ON favorites (user_id);
CREATE INDEX idx_news_cache_expires ON news_cache (expires_at);
```

### تحسين الذاكرة المؤقتة

```python
# في config.py
CACHE_DURATION = 300  # 5 دقائق
ENABLE_CACHE = True
MAX_NEWS_ITEMS = 10
```

### تحسين الاتصالات

```python
# في config.py
RSS_TIMEOUT = 10
MAX_CONCURRENT_FETCHES = 5
TELEGRAM_API_TIMEOUT = 30
```

---

## 🔒 الأمان

### حماية متغيرات البيئة

```bash
# ضبط صلاحيات الملفات
chmod 600 .env
chmod 644 .env.example

# فحص الملفات الحساسة
find . -name "*.env" -type f
find . -name "*.key" -type f
find . -name "*.pem" -type f
```

### جدار الحماية

```bash
# إعداد UFW
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### تحديث النظام

```bash
# تحديث دوري
sudo apt update && sudo apt upgrade -y

# تحديث Python packages
pip list --outdated
pip install --upgrade package_name
```

---

## 📊 مراقبة متقدمة

### إعداد Prometheus (اختياري)

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'trelox-bot'
    static_configs:
      - targets: ['localhost:8080']
```

### إعداد Grafana (اختياري)

```python
# إضافة metrics في bot.py
from prometheus_client import Counter, Histogram, Gauge

# عدد الرسائل المعالجة
messages_processed = Counter('bot_messages_total', 'Total messages processed')

# وقت الاستجابة
response_time = Histogram('bot_response_time_seconds', 'Response time')

# المستخدمين النشطين
active_users = Gauge('bot_active_users', 'Active users count')
```

---

## 📝 قائمة مراجعة النشر

### قبل النشر
- [ ] BOT_TOKEN صحيح
- [ ] AI_API_KEY محدد (اختياري)
- [ ] جميع الملفات موجودة
- [ ] الكود خالي من الأخطاء
- [ ] اختبار محلي ناجح
- [ ] قاعدة البيانات مُعدة

### أثناء النشر
- [ ] متغيرات البيئة مُحددة
- [ ] العملية بدأت بنجاح
- [ ] لا توجد أخطاء في السجلات
- [ ] البوت يستجيب للأوامر

### بعد النشر
- [ ] اختبار `/start`
- [ ] اختبار `/news`
- [ ] اختبار `/help`
- [ ] فحص قاعدة البيانات
- [ ] إعداد النسخ الاحتياطية
- [ ] إعداد المراقبة

---

## 🎯 نصائح للنجاح

### التدرج في التطوير
1. **ابدأ بـ Render** (الأسهل)
2. **اختبر في بيئة محلية أولاً**
3. **استخدم متغيرات البيئة دائماً**
4. **راجع السجلات بانتظام**

### أفضل الممارسات
- **استخدم Git** لإدارة الإصدارات
- **اجعل السجلات شاملة ومفيدة**
- **راقب استخدام الموارد**
- **اعد نسخ احتياطية منتظمة**
- **اختبر الميزات الجديدة بعناية**

### التحسين المستمر
- **راقب أداء البوت**
- **استخدم آراء المستخدمين**
- **حدث المصادر بانتظام**
- **حسن إعدادات قاعدة البيانات**

---

**🎉 تهانينا! بوت تِريلوكس أصبح جاهزاً للإطلاق!** 🚀

لأي مساعدة أو استفسار، لا تتردد في فتح Issue في GitHub أو التواصل معنا.