# osu-most-played-downloader
A quickly thrown-together tool for downloading a user's most played maps on osu.


To use this simply change the placeholder arguments in the function calls to your own.

So instead of this:
```python
if __name__ == "__main__":

    getMostPlayed(id, count, client_id, client_secret)
    downloadMaps(osudbPath, downloadPath)
```

It should look something like this:
```python
if __name__ == "__main__":

    getMostPlayed(2, 100, your client id, "your client secret")
    downloadMaps("C:\\Users\\[your user]\\AppData\\Local\\osu!\\osu!.db", "C:\\Users\\[your user]\\AppData\\Local\\osu!\\Songs\\")
```
