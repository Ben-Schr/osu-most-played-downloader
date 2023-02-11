import requests
import numpy as np
from osdbParser import readHeader, readBeatmap

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
        response = session.get(f'{API_URL}/users/{playerID}/beatmapsets/most_played', params=params, headers=headers).json()

        for counter, resp in enumerate(response):
            mapID = resp.get('beatmap_id')
            idArray[counter+i] = mapID

    datatype = np.dtype([("hash", np.dtype("<S32")), (("id"), (np.uint32))])
    beatmap = np.empty(count, dtype=datatype)
    mapC = 0
    i = 0
    while i < idArray.size // 50:

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


def downloadBeatmapSet(setID: int, session: requests.session, forbidden : dict[int, int | None]) -> None:
    mapFile = session.get(f"https://api.chimu.moe/v1/download/{setID}").content
    mapName = session.get(f"https://api.chimu.moe/v1/set/{setID}").json()

    mapName = f'{mapName.get("SetId")} {mapName.get("Artist")} - {mapName.get("Title")}'.translate(forbidden)

    with open(f"Songs/{mapName}.osz", "wb") as f:
        f.write(mapFile)


def parseHashFromOsuDB(file) -> np.ndarray:
    header = readHeader(file)
    print(header)
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


def downloadMaps(osudbFile) -> None:

    with open(osudbFile, "rb") as osudbFile:
        hashs = parseHashFromOsuDB(osudbFile)

    ids = parseHashId()

    forbidden = str.maketrans("<>:\"/\\|?*", "_________")
    session = requests.session()
    c = 0
    downloadedIDs = []
    for hash, id in ids:
        if np.where(hash == hashs)[0].size or id in downloadedIDs:
            print(f"know {hash} {id}")
            c += 1
            print(c)
            continue

        downloadBeatmapSet(id, session, forbidden)
        downloadedIDs.append(id)


if __name__ == "__main__":

    getMostPlayed(id, count, client_id, client_secret)
    downloadMaps(path)


