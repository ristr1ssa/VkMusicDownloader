import aiohttp
import io


class VkAudio:
    API_V = 5.130
    
    def __init__(self, token):
        """
        token: [str] VkAdmin token (get via https://vkhost.github.io/)
        """
        
        self.token = token

    
    async def get_audioId(self, owner_id: int, count: int = 0) -> list[str]:
        """
        owner_id: int = owner_id
        count: int = count of ids you want to get.

        returns: list['ownerId_audioId=title']
        """
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.vk.com/method/audio.get?owner_id={owner_id}&count={count}&access_token={self.token}&v={self.API_V}') as resp_id:
                resp_id = await resp_id.json()
                resp_id = resp_id['response']['items']
                ans = [f"{resp_id[elem]['owner_id']}_{resp_id[elem]['id']}={resp_id[elem]['title']}" for elem in range(len(resp_id))]

            return ans
    
    async def get_urlById(self, ids_list: list[str]) -> list[str]:
        """
        ids_list: list[str] = list with audio ids (get via VkAudio.get_audioId() method)

        returns: list['links']
        """
       
        ans = []
        async with aiohttp.ClientSession() as session:
            for id in ids_list:
                async with session.get(f'https://api.vk.com/method/audio.getById?audios={id}&access_token={self.token}&v={self.API_V}') as resp_link:
                    resp_link = await resp_link.json()
                    ans.append(resp_link['response'][0]['url'])
            return ans
        
    async def byte_download(self, link: str) -> str:
        """
        link: list[str] = audio link

        returns: IO.Bytesio object     
        """
        
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                ans = await resp.content.read()
                ans = io.BytesIO(ans)
            return ans

    async def get_title(self, id: int) -> list[str]:
        """
        id: str = ownerId_audioId

        returns: str[title]
        """
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.vk.com/method/audio.getById?audios={id}&access_token={self.token}&v={self.API_V}') as title:
                title = await title.json()
                title = title['response'][0]['title']

            return title
