from pydoc import resolve
import aiohttp
import asyncio
import io

class VkAudio:
    def __init__(self, token):
        """
        token: [str] VkAdmin token (get via https://vkhost.github.io/)
        """
        self.token = token

    
    async def get_audioId(self, owner_id: int, count: int = 1) -> list[str]:
        """
        owner_id: int = owner_id
        count: int = count of ids you want to get.

        returns ['ownerId_audioId']
        """
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.vk.com/method/audio.get?owner_id={owner_id}&count={count}&access_token={self.token}&v=5.130') as resp_id:
                resp_id = await resp_id.json()
                resp_id = resp_id['response']['items']
                ans = [f"{resp_id[elem]['owner_id']}_{resp_id[elem]['id']}" for elem in range(len(resp_id))]
                
                await session.close()
                await asyncio.sleep(0.1)
                return ans
    
    async def get_urlById(self, ids_list: list[str]) -> list[str]:
        """
        ids_list: list[str] = list with audio ids (can get by VkAudio.get_audioId() method)

        returns list with links
        """
        ans = []
        async with aiohttp.ClientSession() as session:
            for id in ids_list:
                async with session.get(f'https://api.vk.com/method/audio.getById?audios={id}&access_token={self.token}&v=5.130') as resp_link:
                    resp_link = await resp_link.json()
                    ans.append(resp_link['response'][0]['url'])
            
            await session.close()
            await asyncio.sleep(0.1)
            return ans
        
    async def byte_download(self, link: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as resp:
                    await session.close()
                    await asyncio.sleep(0.1)
                    
                    ans = resp.content
                    ans = ans.read_nowait(n = -1)
                    ans = io.BytesIO(ans)
                    return ans

        