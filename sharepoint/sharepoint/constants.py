from asyncio import Semaphore

BASE_URL = "https://sharepoint.com"
API_LIMIT = Semaphore(10)
