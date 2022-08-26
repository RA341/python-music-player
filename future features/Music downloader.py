"""
from pprint import pprint
from tkinter import ttk
from PIL import ImageTk, Image
import pygame
import threading
from mutagen.mp3 import MP3
import mysql.connector
import pprint

"""
from tkinter import *
from tkinter.ttk import *
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import shutil



def yt_downloader(music_link):
    options = Options()
    options.add_argument('--headless')
    music_link = music_link.replace("https://www.youtube.com/watch?v=", '')
    print("Connecting")
    webpage = r"https://www.y2mate.com/en/youtube-mp3/" + music_link
    driver = webdriver.Firefox(options=options)
    try:
        driver.get(webpage)
        print("Connection Successful")
        print("Setting quality")
        quality = driver.find_element_by_id("format_label")
        driver.execute_script("arguments[0].innerHTML = 'MP3 320 kbps'", quality)
        time.sleep(1)
        print("Generating link")
        submit = driver.find_element_by_id("process_mp3")
        submit.click()
        print("Waiting for link to be generated")
        time.sleep(2)
        print("Downloading")
        result = driver.find_element_by_class_name("modal-content").find_element_by_class_name(
            "modal-body").find_element_by_id("process-result").find_element_by_class_name("btn")
        result.click()
        time.sleep(1)
        print("done")

    except:
        print("connection error")

    # driver.quit()


def manage_list():
    play_window = Toplevel(master)
    play_window.geometry("200x100")
    play_window.resizable(False, False)
    play_window.title("Play list Manager")
    info = Label(play_window, text="Ready")
    info.pack()

    label_button = Label(master, text="Paste link")
    label_button.pack()

    player_entry = Entry(play_window)
    player_entry.pack(pady=10)

    ok_button = Button(play_window, text="DOWNLOAD", command=lambda: yt_downloader(player_entry.get()))
    ok_button.pack()


master = Tk()
master.geometry("300x200")
master.resizable(False, False)

b = Button(master, command=manage_list)
b.pack()
try:
    music_link = "https://www.youtube.com/watch?v=3s9E7lEJz2A"
    options = Options()
    options.add_argument('--headless')
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)  # custom location
    profile.set_preference('browser.download.dir', "F:\Audio")
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'audio/mpeg3')  # type of file to download
    music_link = music_link.replace("https://www.youtube.com/watch?v=", '')
    print("Connecting")
    webpage = r"https://www.y2mate.com/en/youtube-mp3/" + music_link
    driver = webdriver.Firefox(firefox_profile=profile, options=options)
    driver.get(webpage)
    print("Connection Successful")
    print("Setting quality")
    quality = driver.find_element_by_id("format_label")
    driver.execute_script("arguments[0].innerHTML = 'MP3 320 kbps'", quality)
    time.sleep(1)
    print("Generating link")
    submit = driver.find_element_by_id("process_mp3")
    submit.click()
    print("Waiting for link to be generated")
    time.sleep(2)
    print("Downloading")
    result = driver.find_element_by_class_name("modal-content").find_element_by_class_name("modal-body").find_element_by_id(
        "process-result").find_element_by_class_name("btn")
    result.click()
    time.sleep(1)
    print("done")
    driver.quit()
except:
    print("error")


