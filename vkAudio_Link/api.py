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

    
    async def get_audioId(self, owner_id: int, count: int = 0) -> list[str]:
        """
        owner_id: int = owner_id
        count: int = count of ids you want to get.

        returns: ['ownerId_audioId=title']
        """
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.vk.com/method/audio.get?owner_id={owner_id}&count={count}&access_token={self.token}&v=5.130') as resp_id:
                resp_id = await resp_id.json()
                resp_id = resp_id['response']['items']
                ans = [f"{resp_id[elem]['owner_id']}_{resp_id[elem]['id']}={resp_id[elem]['title']}" for elem in range(len(resp_id))]
                
                await session.close()
                await asyncio.sleep(0.1)
                return ans
    
    async def get_urlById(self, ids_list: list[str]) -> list[str]:
        """
        ids_list: list[str] = list with audio ids (can get by VkAudio.get_audioId() method)

        returns: list with links
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
        """
        link: list[str]

        returns: audio in bytes      
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                ans = await resp.content.read()
                ans = io.BytesIO(ans)
                await session.close()
                return ans

    async def get_title(self, id: int) -> list[str]:
        """
        id: str = ownerId_audioId

        returns: title of the audio
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.vk.com/method/audio.getById?audios={id}&access_token={self.token}&v=5.130') as title:
                title = await title.json()
                title = title['response'][0]['title']

        await session.close()
        await asyncio.sleep(0.1)
        return title