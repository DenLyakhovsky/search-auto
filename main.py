import logging
import asyncio
from bot.app import main

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

