from VkMusicDownloader.api import VkAudio

au = VkAudio('VK_ADMIN TOKEN')


async def one() -> list[str]:
    audios = await au.get_audioId(owner_id = 2128351, count = 5) # Getting the first five audios of the user https://vk.com/2128351 (count = 0 if you want to get the all audios)
    return audios # returns list ['ownerId_audioId=title']
    

async def two() -> list[str]:
    urls = await au.get_urlById(['2128351_334257529']) # Getting url of https://vk.com/audio2128351_334257529
    return urls # returns ['https://cs1-64v4.vkuseraudio.net/s/v1/acmp/GddE0dAeHu8Cw81RkIlve_0MYs31F-f8f0dRghEEAOA5AOb1L8FXopyOXRu5TZNdoca6PlD3Nv9u5JTfhMHG6g7bpsYzr_89NFVg3BGYckydmu13H_xcWEYyVHMWSfbOU6mrZbdA9UFrP2gsQsk49Q5b6_2IaBV1RbxFGFYQAhqzixZ1Cg.mp3']


async def three() -> bytearray:
    download = au.byte_download('https://cs1-64v4.vkuseraudio.net/s/v1/acmp/GddE0dAeHu8Cw81RkIlve...mp3') # Downloading audio from the link
    return download # returns a bytes-like object
