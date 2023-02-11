# osu! most played downloader
A quickly thrown-together tool for downloading a user's most played maps on osu.


### Getting started

Simply install the required modules using `pip install -r requirements.txt` from the project folder.

### Usage

To use this simply change the placeholder arguments in `downloader.py` to your own and run the file.

`id` should be changed to the users id.<br />
`count` should be changed to the amount of beatmaps you want to download.<br />
`client_id` and `client_secret` should be changed to the corresponding data from the osu! api.<br />
`osudbPath` should be changed to the path to your `osu!.db` file.<br />
`donwloadPath` should be chnaged to the path you want your maps to be downloaded to.<br />

So instead of this:
```python
if __name__ == "__main__":

    getMostPlayed(id, client_id, client_secret, count)
    downloadMaps(osudbPath, downloadPath)
```

It should look something like this:
```python
if __name__ == "__main__":

    getMostPlayed(2, your client id, "your client secret", 100)
    downloadMaps("C:\\Users\\[your user]\\AppData\\Local\\osu!\\osu!.db", "C:\\Users\\[your user]\\AppData\\Local\\osu!\\Songs\\")
```

## Getting api data

To get a `client_id` and `client_secret`, you must create an OAuth-Application on your profile. To do this simply navigate to your profile settings on the osu! website, scroll all the way down and click the `new OAuth-Application` button. Then simply enter a name and register the application. Now you can press the edit button and see both your secret and id. 
