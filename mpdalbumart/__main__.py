#!/usr/bin/env python3

from __future__ import annotations

import time
import urllib.parse
import urllib.request
from os import path, replace, symlink

import requests
from mpd import MPDClient


def is_album_new(last_song: dict, current_song: dict) -> bool:
    if not last_song["album"] == current_song["album"]:
        return True
    if not last_song["albumartist"] == current_song["albumartist"]:
        return True
    return False


def make_file_name(song: dict, userPath: str = None) -> str:
    album = song["album"]
    artist = song["albumartist"]
    return f"{userPath}{artist}/{album}.jpg"


def is_art_cached(fname: str) -> bool:
    return path.isfile(fname)


def get_itunes_data(album: str, artist: str) -> dict:
    search_term = urllib.parse.quote(artist + " " + album)
    base = "https://itunes.apple.com/search"
    params = f"?term={search_term}&country=us&entity=album&limit=25"
    url = f"{base}{params}"
    return requests.get(url).json()["results"]


def download_album_art(song: dict, filepath: str) -> None:
    url = get_album_art_url(song)
    urllib.request.urlretrieve(url, filepath)


def format_album_art_url(url: str) -> str:
    return url.replace("100x100bb", "10000x10000-900")


def get_album_art_url(song: dict) -> None:
    album = song["album"]
    artist = song["albumartist"]
    data = get_itunes_data(album, artist)

    # Looks for exact match of artist + album name
    for entry in data:
        if artist != entry["artistName"]:
            continue
        if album != entry["collectionName"]:
            continue
        return format_album_art_url(entry["artworkUrl100"])

    # Failing an exact match, look for partial match for album name
    for entry in data:
        if artist != entry["artistName"]:
            continue
        if album not in entry["collectionName"]:
            continue
        return format_album_art_url(entry["artworkUrl100"])

    # Failing partial match and only 1 result, its likely correct
    if len(data) == 1:
        if artist == data[0]["artistName"]:
            return data[0]["artworkUrl100"]


def mpd_wait_for_new_album(client: MPDClient, last_song: dict) -> bool:
    status = client.status()
    song = client.currentsong()

    try:
        in_suitable_state = status["state"] == "play"
        new_album = is_album_new(last_song, song)

        if in_suitable_state and new_album:
            return True

        while not in_suitable_state or not new_album:
            client.idle("player")
            status = client.status()
            song = client.currentsong()

            in_suitable_state = status["state"] == "play"
            new_album = is_album_new(last_song, song)

        # Check if these keys are accessible, if not exeception is thrown
        if song["album"]:
            pass
        if song["albumartist"]:
            pass

        return True
    except Exception:
        pass

    return False


def mpd_connect(host: str = "127.0.0.1", port: int = 6600) -> MPDClient:
    client = MPDClient()
    client.timeout = 10
    client.idletimeout = None
    client.connect(host, port)
    return client


def mpd_reconnect(TIMEOUT: int = 10) -> MPDClient:
    try:
        time.sleep(TIMEOUT)
        client = mpd_connect()
    except KeyboardInterrupt:
        # logger.info("Keyboard Interrupt detected - Exiting!")
        pass
    except Exception:
        # logger.debug("Could not connect to MPD!")
        pass

    return client


def update_linked_art(filePath: str, cachePath: str = None):
    symlink(filePath, f"{cachePath}/.tmp_art")
    replace(f"{cachePath}.tmp_art", f"{cachePath}albumart")


def mpd_update_album_art(client: MPDClient, userPath: str = None) -> None:
    PATH = path.expanduser("~") + "/Music/.art/"
    CACHEPATH = path.expanduser("~") + "/.cache/"
    song = {
        "album": "",
        "albumartist": "",
    }

    while mpd_wait_for_new_album(client, song):
        song = client.currentsong()
        fname = make_file_name(song, PATH)
        art_cached = is_art_cached(fname)
        if not art_cached:
            download_album_art(song, fname)

        update_linked_art(fname, CACHEPATH)


def cli_run():
    client = None
    try:
        client = mpd_connect()
    except Exception:
        pass

    while True:
        if not client:
            client = mpd_reconnect()
        try:
            mpd_update_album_art(client)
            # User is in no-daemon mode and wants to exit
        except KeyboardInterrupt:  # User exit
            # logger.info("Keyboard Interrupt detected - Exiting!")
            break
        except ConnectionError:  # MPD connection loss (retry)
            # logger.error("Received an MPD Connection error!: {}".format(e))
            client = None
        # except Exception:
        #     print("Huh")
        #     # logger.exception("Something went very wrong!")
        #     break

    try:
        client.close()
        client.disconnect()
    except Exception:
        # logger.warn("Could not gracefully disconnect from Mpd...")
        pass

    # logger.info("Shutting down...")
    exit(0)


# for idx, flag in enumerate(sys.argv):
#      if flag == "-h" or flag == "--help":
#          break;

if __name__ == "__main__":
    cli_run()
