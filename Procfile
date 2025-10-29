# Trelox Bot - Procfile for Deployment
# This file tells deployment platforms how to run the bot

# Primary deployment configuration
worker: python main.py

# Alternative configurations for different platforms

# For Heroku
# worker: python -m bot

# For Railway
# web: python main.py

# For Fly.io
# app: python main.py

# For DigitalOcean App Platform
# worker: python3 main.py

# Development configuration (uncomment for local development)
# debug: python -m bot --debug

# Testing configuration
# test: python -m pytest

# Linting configuration
# lint: python -m flake8 bot.py database.py config.py main.py

# Type checking
# type-check: python -m mypy bot.py database.py config.py main.py

# Security check
# security: python -m bandit -r . -f json

# Documentation generation
# docs: python -m sphinx -b html docs/ docs/_build/html

# Database backup
# backup: python -c "from database import db; import asyncio; asyncio.run(db.backup_database())"

# Database migration
# migrate: python -c "from database import db; db.init_database()"

# Cache cleanup
# cleanup: python -c "from database import db; import asyncio; asyncio.run(db.cleanup_expired_cache())"

# Statistics generation
# stats: python -c "from database import db; import asyncio; print(asyncio.run(db.get_database_stats()))"

# RSS source validation
# validate-sources: python -c "import json; data=json.load(open('rss_sources.json')); print(f'Found {sum(len(cats) for cats in data.values())} countries with {sum(len(sources) for country in data.values() for sources in country.values() if isinstance(sources, list))} total sources')"

# Environment validation
# validate-env: python -c "from config import validate_config; import sys; sys.exit(0 if validate_config() else 1)"
