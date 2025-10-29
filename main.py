#!/usr/bin/env python3
"""
Main entry point for Trelox Bot
Entry point for deployment compatibility
"""

import asyncio
from bot import TreloxBot

async def main():
    """Main function to run the bot"""
    bot = TreloxBot()
    await bot.run()

if __name__ == "__main__":
    # Run the bot
    asyncio.run(main())
