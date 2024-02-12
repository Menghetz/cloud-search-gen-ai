import logging
from drivers import main
import asyncio

logging.basicConfig(level=logging.ERROR) 

if __name__ == '__main__':
    asyncio.run(main())