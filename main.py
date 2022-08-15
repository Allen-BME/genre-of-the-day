import random
import urllib.request
from datetime import date
import os

import spotipy
from instagrapi import Client

if __name__ == "__main__":

    # --- get secret names and passwords
    GENRE_ACCT_NAME = os.environ['GENRE_ACCT_NAME']
    GENRE_ACCT_PASSWORD = os.environ['GENRE_ACCT_PASSWORD']
    SPOTIFY_ID = os.environ['SPOTIFY_ID']
    SPOTIFY_SECRET = os.environ['SPOTIFY_SECRET']


    # --- get random genre
    print("getting random genre...")
    with open("GENRES.txt", "r", encoding="UTF-8") as fp:
        lines = fp.readlines()

        genre_list = []
        for line in lines:
            genre_list.append(line.strip())

    genre_choice = random.choice(genre_list)
    print(f"got {genre_choice}!")
    genre_query = f"genre:\"{genre_choice}\""
    genre_tag = genre_choice.replace(" ", "").lower()


    # --- search spotify
    print("searching spotify...")
    auth_manager = spotipy.SpotifyClientCredentials(
        client_id=SPOTIFY_ID,
        client_secret=SPOTIFY_SECRET,
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    results = sp.search(q=genre_query, limit=1, )

    song = None
    for a in results['tracks']["items"]:
        image = a["album"]["images"][1]["url"]
        song = {
            "name": a["name"],
            "artista":a["artists"][0]["name"],
            "uri":a["uri"],
            "cover":image,
            'preview_url':a["preview_url"]
        }
    

    # --- if spotify had info
    if song != None:
        print("found info! posting info!")
        img_name = f"./cover-art/{date.today()}-cover.png"
        urllib.request.urlretrieve(
            song["cover"],
            img_name
        )

        caption = f" | Today's genre is \"{genre_choice}\"! If you need a suggestion, \"{song['name']}\" by {song['artista']} is a good choice. \n#music #{genre_tag}"


    # if spotify had no info
    else:
        print("didn't found info :( posting sad")
        img_name = "sad.jpg"
        caption = f" | Today's genre is \"{genre_choice}\", but it's too underground! I couldn't find a suggestion today, sorry... \n#music #{genre_choice}"


    # upload to instagram
    print("uploading to insta...")

    cl = Client()
    cl.login(GENRE_ACCT_NAME, GENRE_ACCT_PASSWORD)

    cl.photo_upload(
        path=img_name,
        caption = caption,
    )


    # update genres
    print("updating genre list...")
    with open("GENRES.txt", "w", encoding="UTF-8") as fp:
        for item in genre_list:
            if item != genre_choice:
                fp.write(item)
                fp.write("\n")


    # update log
    print("updating log...")
    with open("LOG.txt", "a", encoding="UTF-8") as log:
        log.write(f"{date.today()} - {genre_choice}\n")
