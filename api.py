import aiohttp
import asyncio
import io


class VkAudio:
    API_V = 5.13

    async def validate_token(self, token) -> bool:
        method = "users.get"
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://api.vk.com/method/{method}?access_token={token}&v={self.API_V}") as api_resp:

                api_resp = await api_resp.json()

            if 'error' in api_resp:
                return False
            return True

    def __init__(self, token):
        """
        token: [str] VkAdmin token (get via https://vkhost.github.io/)
        """

        loop = asyncio.new_event_loop()
        loop = asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(
            self.validate_token(
                token
            )
        )

        if result:
            self.token = token
        else:
            raise BaseException("CHECK TOKEN")

    async def __make_request(self, method: str, params: str):
        """
        Making request, openning one session

        returns: request.json()
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://api.vk.com/method/{method}?access_token={self.token[0]}&v={self.API_V}&{params}") as api_resp:

                api_resp = await api_resp.json()

            return api_resp

    async def get_audioId(self, owner_id: int, count: int = 0) -> list[str]:
        """
        owner_id: int = owner_id
        count: int = count of ids you want to get.

        returns: list['ownerId_audioId=title']
        """

        params = f"owner_id={owner_id}&count={count}"
        api_resp = await VkAudio.__make_request(self, method='audio.get', params=params)
        api_resp = api_resp['response']['items']
        ans = [f"{api_resp[elem]['owner_id']}_{api_resp[elem]['id']}={api_resp[elem]['title']}" for elem in range(
            len(api_resp))]

        return ans

    async def get_urlById(self, ids_list: list[str]) -> list[str]:
        """
        ids_list: list[str] = list with audio ids (get via VkAudio.get_audioId() method)

        returns: list['links']
        """

        ans = []
        for id in ids_list:
            params = f"audios={id}"
            resp_link = await VkAudio.__make_request(self, method='audio.getById', params=params)

            ans.append(
                resp_link['response'][0]['url']
            )

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

        params = f"audios={id}"
        api_resp = await VkAudio.__make_request(self, method="audio.getById", params=params)
        title = api_resp['response'][0]['title']

        return title
