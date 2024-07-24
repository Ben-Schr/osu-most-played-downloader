# osu! most played downloader
A quickly thrown-together tool for downloading a user's most played maps on osu.


### Getting started

Simply install the required modules using `pip install -r requirements.txt` from the project folder.<br />

### Usage

To use this simply change the placeholder arguments in `config.json` to your own and run the `downloader.py` file.<br />

Note: To run this file you will have to have installed python.

#### Program arguments

The program can take some arguments from the command line, the most important ones are -c/--use-cache and -n/--max-number.
These specify if the program should use cached data from a previous run to speed up the current run and the maximum amount of maps to download.

Note: The --use-cache option should only be used, if you didn't download a lot of maps that overlap the target user's most played maps since the creation of the cache file.

### Config

`user_id` should be changed to the users id.<br />
`client_id` and `client_secret` should be changed to the corresponding data from the osu! api.<br />
`db_path` should be changed to the path to your `osu!.db` file.<br />
`download_path` should be changed to the path you want your maps to be downloaded to.<br />

### Getting api credentials

To get a `client_id` and `client_secret`, you must create an OAuth-Application on your profile. To do this simply navigate to your profile settings on the osu! website, scroll all the way down and click the `new OAuth-Application` button. Then simply enter a name and register the application. Now you can press the edit button and see both your secret and id. 
