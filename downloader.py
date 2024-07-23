import requests
import numpy as np
from osudbParser import readHeader, readBeatmap
import re

def getMostPlayed(playerID : int, client_id : int, client_secret : str, count : int = 100) -> None:
    API_URL = 'https://osu.ppy.sh/api/v2'
    TOKEN_URL = 'https://osu.ppy.sh/oauth/token'
    def get_token():
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials',
            'scope': 'public'
        }
        
        response = requests.post(TOKEN_URL, data=data)
        return response.json().get('access_token')

    token = get_token()
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    params = {
        'mode': 'osu',
        'offset': 0,
        'limit': 100,
    }

    idArray = np.empty(count, np.uint32)
    session = requests.session()

    for i in range(0, count, 100):
        params['offset'] = i
        params['limit'] = i+100
        if count - i < 100:
            params['limit'] = i+count-i

        response = session.get(f'{API_URL}/users/{playerID}/beatmapsets/most_played', params=params, headers=headers).json()

        for counter, resp in enumerate(response):
            mapID = resp.get('beatmap_id')
            idArray[counter+i] = mapID

    datatype = np.dtype([("hash", np.dtype("<S32")), (("id"), (np.uint32))])
    beatmap = np.empty(count, dtype=datatype)
    mapC = 0
    i = 0
    arraySize = idArray.size // 50
    if arraySize == 0:
        arraySize = 50
    while i < arraySize:

        mapCounter = i * 50 + 50
        
        params['ids[]'] = idArray[i*50:mapCounter]
        
        response = session.get(f'{API_URL}/beatmaps', params=params, headers=headers)
        
        response = response.json()

        for j in response.get("beatmaps"):
            beatmap[mapC]['id'] = j.get('beatmapset_id')
            beatmap[mapC]['hash'] = j.get('checksum')
            mapC += 1

        i += 1


    np.save("beatmaps.npy", beatmap)


def downloadBeatmapSet(setID: int, session: requests.session, forbidden : dict[int, int], downloadPath : str) -> None:
    response = session.get(f"https://catboy.best/d/{setID}")
    content_disposition = response.headers['Content-Disposition']
    filename = re.findall('filename="(.+)"', content_disposition)

    if len(filename) != 0:
        filename = filename[0].replace("%20", " ")
    else:
        filename = str(setID)

    with open(f"{downloadPath}/{filename}", "wb") as f:
        f.write(response.content)


def parseHashFromOsuDB(file) -> np.ndarray:
    header = readHeader(file)
    size = header[5]
    hashs = np.empty(size, np.dtype("<S32"))
    for i in range(size):
        beatmap = readBeatmap(file)
        if beatmap[7]:
            hashs[i] = beatmap[7][1]
    return hashs


def parseHashId(file = "beatmaps.npy") -> np.ndarray:

    data = np.load(file)

    return data


def downloadMaps(osudbFile, downloadPath : str) -> None:

    with open(osudbFile, "rb") as osudbFile:
        hashs = parseHashFromOsuDB(osudbFile)

    ids = parseHashId()

    forbidden = str.maketrans("<>:\"/\\|?*", "_________")
    session = requests.session()
    downloadedIDs = []
    for hash, id in ids:
        if np.where(hash == hashs)[0].size or id in downloadedIDs:
            continue
        
        downloadBeatmapSet(id, session, forbidden, downloadPath)
        downloadedIDs.append(id)


if __name__ == "__main__":

    getMostPlayed(id, client_id, client_secret, count)
    downloadMaps(osudbPath, downloadPath)


