import os
import aiohttp
import asyncio
from dotenv import load_dotenv

load_dotenv()

NAVER_PLACE_API_URL = "https://openapi.naver.com/v1/search/local.json"
NAVER_CLIENT_ID = os.environ.get("naver_client_id")
NAVER_CLIENT_SECRET = os.environ.get("naver_client_secret")

def clean_text(text: str) -> str:
    return text.replace("<b>", "").replace("</b>", "").strip()

async def search_naver_places(query: str, display: int = 20):
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    
    params = {
        "query": query,
        "display": display,
        "start": 1,
        "sort": "comment"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(NAVER_PLACE_API_URL, headers=headers, params=params, ssl=False) as response:
        #async with session.get(NAVER_PLACE_API_URL, headers=headers, params=params) as response:
            if response.status != 200:
                raise Exception(f"Naver API error: {response.status}")
            data = await response.json()

    items = data.get("items", [])
    if not items:
        print("검색 결과가 없습니다.")
        return

    print(f"\n🔍 '{query}'에 대한 검색 결과 (상위 {display}개):\n")
    for idx, item in enumerate(items, 1):
        title = clean_text(item.get("title", ""))
        address = item.get("address", "")
        category = item.get("category", "")
        link = item.get("link", "")
        description = clean_text(item.get("description", ""))

        print(f"{idx}. {title}")
        print(f"   📍 주소: {address}")
        print(f"   🏷️ 카테고리: {category}")
        print(f"   🔗 링크: {link}")
        print(f"   📝 설명: {description}")
        print()

if __name__ == "__main__":
    query = input("검색어를 입력하세요: ")
    asyncio.run(search_naver_places(query))
