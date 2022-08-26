from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from tkinter.ttk import Progressbar
from PIL import ImageTk, Image  ## install pil
import pygame
from os import listdir
import os
from mutagen.mp3 import MP3
import time
import threading
import mysql.connector
import random

"""
Project by R##$
Important note

When opening folders wait for complete loading message.
Do not seek while paused
"""

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS music_player")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="music_player"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS song_list(song_id INT AUTO_INCREMENT PRIMARY KEY,song_name VARCHAR(255),song_path CHAR(255), song_lenght INT(10))")

mycursor.execute("CREATE TABLE IF NOT EXISTS play_list(playlist_id INT AUTO_INCREMENT PRIMARY KEY,playlist_name VARCHAR(255))")

mycursor.execute("CREATE TABLE IF NOT EXISTS paths(table_name CHAR(255),path CHAR(255))")

class Seek(ttk.Scale):
    # (Seek)a type of Scale where the left click is hijacked to work like a right click
    def __init__(self, master=None, **kwargs):
        ttk.Scale.__init__(self, master, **kwargs)
        self.bind('<Button-1>', self.set_value)

    def set_value(self, event):
        global seeker, play_bool
        self.event_generate('<Button-3>', x=event.x, y=event.y)
        seeker = round(seek_bar.get())
        pygame.mixer.music.play(0, seeker)
        return 'break'


class volume(Scale):
    # a type of Scale where the left click is hijacked to work like a right click
    def __init__(self, master=None, **kwargs):
        Scale.__init__(self, master, **kwargs)
        self.bind('<Button-1>', self.set_value)

    def set_value(self, event):
        global vol
        self.event_generate('<Button-3>', x=event.x, y=event.y)
        v = float(round(seek_bar.get())) * 0.01
        pygame.mixer.music.set_volume(v)
        if v > 0:
            vol_min.configure(image=mute_photo)
            vol = True
        return 'break'


class musicplayer:
    def __init__(self):
        pygame.mixer.init()

    def pause(self):
        global play_bool, play_state
        if play_bool:
            if not play_state:
                play_state = True
                play_bool = False
                pygame.mixer.music.play()
            elif play_state:
                play_bool = False
                pygame.mixer.music.unpause()
            play_button.configure(image=pause_photo)
        elif not play_bool:
            play_bool = True
            pygame.mixer.music.pause()
            play_button.configure(image=play_photo)

    def rewind(self):
        global song_no, play_state, play_bool, selected, current_playlist_name, shuffled, length_dict, last_played
        song_no -= 1
        if shuffle_list == {}:
            x = song_no
        else:
            x = shuffle_list[song_no]
        if current_playlist_name == "All Songs":
            p = playlist.search("song_list", x)
        else:
            p = playlist.search(current_playlist_name, x)
        playlist_title.configure(text=p[1])
        if current_playlist_name == selected.get():
            song_listbox.itemconfig(song_listbox.get(0, "end").index(last_played[1]), bg=main_background_color)
            song_listbox.itemconfig(song_listbox.get(0, "end").index(p[1]), bg="green")
        pygame.mixer.music.load(os.path.join(p[2], p[1]))
        seek_bar_init(p[3])
        pygame.mixer.music.play()
        thread.counter(p[3])
        if play_bool:
            play_state = True
            play_bool = False
            play_button.configure(image=pause_photo)
        last_played = p
        stat_check()

    def next(self):
        global song_no, play_bool, play_state, shuffled, current_playlist_name, length_dict, last_played
        song_no += 1
        if shuffle_list == {}:
            x = song_no
        else:
            x = shuffle_list[song_no]
        if current_playlist_name == "All Songs":
            p = playlist.search("song_list", x)
        else:
            p = playlist.search(current_playlist_name, x)
        playlist_title.configure(text=p[1])
        if current_playlist_name == selected.get():
            song_listbox.itemconfig(song_listbox.get(0, "end").index(last_played[1]), bg=main_background_color)
            song_listbox.itemconfig(song_listbox.get(0, "end").index(p[1]), bg="green")
        pygame.mixer.music.load(os.path.join(p[2], p[1]))
        seek_bar_init(p[3])
        pygame.mixer.music.play()
        thread.counter(p[3])
        if play_bool:
            play_state = True
            play_bool = False
            play_button.configure(image=pause_photo)
        last_played = p
        stat_check()

    def autoplay(self):
        # weird error
        global autoplay_bool, play_bool, song_no, play_state, t1, current_playlist_name, length_dict, seeker, last_played
        if not pygame.mixer.music.get_busy() and play_state:
            if autoplay_bool:
                pos = pygame.mixer.music.get_pos()
                if int(pos) == -1:
                    song_no += 1
                    if current_playlist_name == "All Songs":
                        p = length_dict["song_list"]
                    else:
                        p = length_dict[current_playlist_name]
                    if song_no <= p:
                        if shuffle_list == {}:
                            x = song_no
                        else:
                            x = shuffle_list[song_no]
                        if current_playlist_name == "All Songs":
                            p = playlist.search("song_list", x)
                        else:
                            p = playlist.search(current_playlist_name, x)
                        pygame.mixer.music.load(os.path.join(p[2], p[1]))
                        playlist_title.configure(text=p[1])
                        if current_playlist_name == selected.get():
                            song_listbox.itemconfig(song_listbox.get(0, "end").index(last_played[1]),
                                                    bg=main_background_color)
                            song_listbox.itemconfig(song_listbox.get(0, "end").index(p[1]), bg="green")
                        seek_bar_init(p[3])
                        thread.counter(p[3])
                        pygame.mixer.music.play()
                        last_played = p
                        stat_check()
            else:
                seeker = 0
                seek_bar.set(seeker)
                min_label.configure(text=str(00).zfill(2) + ":" + str(00).zfill(2))
                min_label.configure(text=str(00).zfill(2) + ":" + str(00).zfill(2))
                play_bool = True
                play_state = False
                seek_bar.configure(state=DISABLED)
                pygame.mixer.music.pause()
                play_button.configure(image=play_photo)
                seek_bar.configure(state=DISABLED)
        top.after(1, self.autoplay)

    def shuffle(self):
        global shuffle_list, shuffled, shuffle_count, song_no
        shuffle_count += 1
        if shuffle_count == 1:
            if shuffled:
                pass
            elif not shuffled:
                length = song_listbox.size()
                l = []
                u = 0
                for x in range(1, length + 1):
                    l.append(x)
                    random.shuffle(l)
                for x in range(len(l)):
                    u += 1
                    shuffle_list[u] = l[x]
                song_no = 0
                shuffled = True
            shuffle_Button.configure(image=shuffle_active)

        elif shuffle_count >= 2:
            shuffle_list = {}
            song_no = 0
            shuffle_count = 0
            shuffled = False
            shuffle_Button.configure(image=shuffle_inactive)

    def vol(self, val):
        v = float(val) * 0.01
        pygame.mixer.music.set_volume(v)

    def min(self):
        global vol
        if vol:
            pygame.mixer.music.set_volume(0)
            vol_slider.set(0)
            vol_min.configure(image=max_photo)
            vol = False
        else:
            pygame.mixer.music.set_volume(0.5)
            vol_slider.set(50)
            vol_min.configure(image=mute_photo)
            vol = True


class thread_control:

    def __init__(self):
        self._running = True

    def start(self):
        self._running = True

    def terminate(self):
        self._running = False

    def convert(self, seconds):
        l = []
        hours = seconds // 3600
        seconds %= 3600
        mins = seconds // 60
        seconds %= 60
        l.append(hours)
        l.append(mins)
        l.append(seconds)
        return l

    def run(self, n):
        global seeker
        total = n
        n = round(n)
        while self._running and n > 0:
            if not play_bool:
                max_time_list = self.convert(seeker)
                min_time_list = self.convert(n)
                min_label.configure(text=str(max_time_list[1]).zfill(2) + ":" + str(max_time_list[2]).zfill(2))
                max_label.configure(text=str(min_time_list[1]).zfill(2) + ":" + str(min_time_list[2]).zfill(2))
                seek_bar.set(seeker)
                time.sleep(1)
                n -= 1
                seeker += 1
                n = total - round(float(seeker))
            else:
                time.sleep(0.1)

    def counter(self, music_len):
        global t1
        if threading.active_count() >= 2:
            thread.terminate()
            t1.join()
            thread.start()
            t1 = threading.Thread(target=self.run, args=(music_len,))
            t1.daemon = True
            t1.start()
        else:
            t1 = threading.Thread(target=self.run, args=(music_len,))
            t1.daemon = True
            t1.start()


class playlist_cotrols:

    def search(self, playlist, name):
        if type(name) == str:
            mycursor.execute("SELECT * FROM " + playlist + " WHERE song_name = %s", (name,))
        elif type(name) == int:
            mycursor.execute("SELECT * FROM " + playlist + " WHERE song_id = %s", (name,))
        myresult = mycursor.fetchone()
        mydb.commit()
        return myresult

    def insert_song(self, playlist_name, name, path, music_lenght):
        sql = "INSERT INTO " + playlist_name + " (song_name,song_path,song_lenght) VALUES (%s,%s,%s)"
        val = (name, path, music_lenght)
        mycursor.execute(sql, val)
        mydb.commit()

    def delete_song(self, playlist, song):
        mycursor.execute("DELETE FROM " + playlist + " WHERE song_name = %s", (song,))
        mycursor.execute("ALTER TABLE " + playlist + " DROP song_id")
        mycursor.execute("ALTER TABLE " + playlist + " AUTO_INCREMENT = 1")
        mycursor.execute(
            "ALTER TABLE " + playlist + " ADD song_id int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST")
        mydb.commit()

    def search_playlist(self, playlist, name):
        mycursor.execute("SELECT * FROM " + playlist + " WHERE playlist_name = %s", (name,))
        myresult = mycursor.fetchone()
        return myresult

    def create_play_list(self, name):
        sql = "INSERT INTO play_list (playlist_name) VALUES (%s)"
        val = (name,)
        mycursor.execute(sql, val)
        mycursor.execute(
            "CREATE TABLE " + name + " (song_id INT AUTO_INCREMENT PRIMARY KEY,song_name VARCHAR(255),song_path CHAR(255),song_lenght INT(10))")
        mydb.commit()

    def delete_table(self, name):
        if name != "":
            if name != "All Songs":
                mycursor.execute("DELETE FROM play_list WHERE playlist_name = %s", (name,))
                mycursor.execute("ALTER TABLE play_list DROP playlist_id")
                mycursor.execute("ALTER TABLE play_list AUTO_INCREMENT = 1")
                mycursor.execute(
                    "ALTER TABLE play_list ADD playlist_id int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST")
                mycursor.execute("DROP TABLE " + name)
        else:
            messagebox.showerror("Error", "No Playlist Selected")
        mydb.commit()

    def mass_del(self, playlist1):
        mycursor.execute("SELECT * FROM play_list")
        result = mycursor.fetchall()
        mycursor.execute("SELECT * FROM " + playlist1)
        myresult = mycursor.fetchall()
        for x in myresult:
            mycursor.execute("delete from song_list where song_name = %s", (x[1],))
            for y in result:
                mycursor.execute("delete from " + y[1] + " where song_name = %s", (x[1],))
        mycursor.execute("ALTER TABLE song_list DROP song_id")
        mycursor.execute("ALTER TABLE song_list AUTO_INCREMENT = 1")
        mycursor.execute("ALTER TABLE song_list ADD song_id int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST")
        mycursor.execute("drop table " + playlist1)
        mycursor.execute("delete from paths where table_name = %s", (playlist1,))
        mycursor.execute("delete from play_list where playlist_name = %s", (playlist1,))
        mycursor.execute("ALTER TABLE play_list DROP playlist_id")
        mycursor.execute("ALTER TABLE play_list AUTO_INCREMENT = 1")
        mycursor.execute("ALTER TABLE play_list ADD playlist_id int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST")
        mydb.commit()

    def table_length(self):
        length_dict_f = {}
        mycursor.execute("SHOW TABLES")
        result = mycursor.fetchall()
        for x in result:
            if x[0] != "paths":
                if x[0] != "play_list":
                    mycursor.execute("SELECT * FROM " + str(x[0]))
                    myresult = mycursor.fetchall()
                    length_dict_f[x[0]] = len(list(myresult))
        return length_dict_f


class song_manager:
    def listgen(self, path):
        global length_dict
        playlist.create_play_list(os.path.basename(path))
        for file in listdir(path):
            if file.endswith(".mp3"):
                if str(playlist.search(os.path.basename(path), file)) != "None":
                    pass
                else:
                    music_lenght = MP3(os.path.join(path, file)).info.length
                    playlist.insert_song(os.path.basename(path), file, path, music_lenght)
                    if str(playlist.search("song_list", file)) == "None":
                        playlist.insert_song("song_list", file, path, music_lenght)
                    else:
                        pass
        length_dict = playlist.table_length()
        mydb.commit()

    def get_key(self, val):
        global selected
        if val != "":
            if selected.get() == "All Songs":
                o = playlist.search("song_list", val)[0]
            else:
                o = playlist.search(selected.get(), val)[0]
        return o

    def direc(self):
        global options, add_options, check_list, length_dict
        directory = askdirectory()
        if len(directory) != 0:
            mycursor.execute("CREATE TABLE IF NOT EXISTS paths(table_name CHAR(255),path CHAR(255))")
            mycursor.execute("SELECT * FROM paths WHERE table_name = %s", (os.path.basename(directory),))
            myresult = mycursor.fetchone()
            p = os.path.basename(directory)
            if str(myresult) == "None":
                sql = "INSERT INTO paths (table_name,path) VALUES (%s,%s)"
                val = (p, directory)
                mycursor.execute(sql, val)
                mydb.commit()
                manager.listgen(directory)
                options.append(p)
                add_options.append(p)
                check_list.append(p)
                playlist_drop()
                adds()
                mycursor.execute("SELECT * FROM " + p)
                myresult = mycursor.fetchall()
                length_dict[len(length_dict) + 1] = len(list(myresult))
                messagebox.showinfo("All Done", "Songs Successfully added ")
            else:
                messagebox.showerror("File error",
                                     "You have already inserted the folder,check folder location and try again\nOr a folder with the same name has already been loaded ,change folder name and try again.")

    def refresh_direc(self):
        mycursor.execute("SELECT * FROM paths")
        myresult = mycursor.fetchall()
        for x in myresult:  # getting main directories
            direc_list = []
            database_list = []
            mycursor.execute("SELECT * FROM " + x[0])  # getting song from database
            result = mycursor.fetchall()
            for t in result:
                database_list.append(t[1])
            for file in listdir(x[1]):  # getting files in directory
                if file.endswith(".mp3"):
                    direc_list.append(file)
                    p = playlist.search(os.path.basename(x[1]), file)
                    if str(p) != "None":
                        pass
                    else:
                        music_length = MP3(os.path.join(x[1], file)).info.length
                        playlist.insert_song(os.path.basename(x[1]), file, x[1], music_length)
                        if str(playlist.search("song_list", file)) == "None":
                            playlist.insert_song("song_list", file, x[1], music_length)
                        else:
                            pass
            for i in database_list:
                if i in direc_list:
                    pass
                elif i not in direc_list:
                    playlist.delete_song("song_list", i)
                    playlist.delete_song(x[0], i)

    def add_func(self, val):
        global selected
        p = selected.get()
        s = song_listbox.get(ANCHOR)
        if p == "All Songs":
            p = "song_list"
        mycursor.execute("SELECT * FROM play_list")
        result = mycursor.fetchall()
        if s != "":
            if s not in result:
                o = playlist.search(val, s)
                if str(o) == "None":
                    q = playlist.search(p, s)
                    if str(q) == "None":
                        pass
                    else:
                        playlist.insert_song(val, s, q[2], q[3])
                else:
                    messagebox.showerror("Name Error", "Song already in Playlist")

    def del_func(self):
        global check_list
        val = selected.get()
        s = song_listbox.get(ANCHOR)
        if len(s) != 0:
            if val != "All Songs":
                if val in check_list:
                    messagebox.showerror("error", "Cannot delete songs from " + "'" + val + "'" + " playlist")
                else:
                    playlist.delete_song(val, s)
                    listboxinit(val)
            else:
                messagebox.showerror("error", "Cannot delete songs from All Songs playlist")
        else:
            messagebox.showerror("Error", "No song selected")


def manage_list():
    global text_color, main_background_color

    def click2():
        global options, add_options, selected, selected2
        s = str(player_entry.get())
        if len(s) > 0:
            if str(playlist.search_playlist("play_list", s)) == "None":
                playlist.create_play_list(s)
                options.append(s)
                add_options.append(s)
                playlist_drop()
                adds()
                menu_drop()
                label_button.configure(text="Playlist added")
                player_entry.delete(0, 'end')
            else:
                messagebox.showerror("Error", "Playlist name already exits")
        else:
            messagebox.showerror("Error", "No name entered")

    def click3(g):
        global options, add_options, selected, selected2, check_list
        if g == "All Songs":
            messagebox.showerror("Error", "All songs cannot be deleted")
        elif g in check_list:
            question = messagebox.askquestion("Warning",
                                              "This playlist is where songs of folder " + "'" + g + "'" + " are saved.\nThis will remove songs which are part of folder " + "'" + g + "'" + " from all playlists\nAre you sure ?")
            if question == "yes":
                playlist.mass_del(g)
                options.remove(g)
                add_options.remove(g)
                playlist_drop()
                adds()
                menu_drop()
                selected.set(options[0])
                label_button.configure(text="Playlist Deleted")

            else:
                pass
        else:
            playlist.delete_table(g)
            options.remove(g)
            add_options.remove(g)
            playlist_drop()
            adds()
            menu_drop()
            selected.set(options[0])
            listboxinit(selected.get())
            label_button.configure(text="Playlist Deleted")

    play_window = Toplevel(top, background=main_background_color)
    play_window.geometry("300x200")
    play_window.resizable(False, False)
    play_window.title("Play list Manager")

    label_button = Label(play_window, text="New Playlist", background=main_background_color, foreground=text_color)
    label_button.pack()

    player_entry = Entry(play_window, background=main_background_color, foreground=text_color)
    player_entry.pack(pady=10)

    padd_button = Button(play_window, text="Add Playlist", command=click2, background=main_background_color,
                         foreground=text_color)
    padd_button.pack()

    def menu_drop():
        menu = OptionMenu(play_window, selected, *options)
        menu.configure(background=main_background_color, foreground=text_color,
                       highlightbackground=main_background_color)
        menu.place(x=95, y=95, height=30, width=110)

    menu_drop()

    ok_button = Button(play_window, text="Delete Playlist", command=lambda: click3(selected.get()),
                       background=main_background_color, foreground=text_color)
    ok_button.place(x=105, y=130, height=25, width=92)


def double_click(event):
    global song_no, selected, play_bool, play_state, current_playlist_name, last_played, shuffle_count, shuffle_list, length_dict, shuffled
    song = song_listbox.selection_get()
    song_no = manager.get_key(song)
    if current_playlist_name != selected.get():
        if shuffle_list != {}:
            shuffle_list = {}
            shuffle_count = 0
            shuffled = False
            shuffle_Button.configure(image=shuffle_inactive)
    if selected.get() == "All Songs":
        p = playlist.search("song_list", song_no)
    else:
        p = playlist.search(selected.get(), song_no)
    pygame.mixer.music.load(os.path.join(p[2], p[1]))
    seek_bar_init(p[3])
    thread.counter(p[3])
    playlist_title.configure(text=song)
    if last_played != "":
        if current_playlist_name == selected.get():
            song_listbox.itemconfig(song_listbox.get(0, "end").index(last_played[1]), bg=main_background_color)
        song_listbox.itemconfig(song_listbox.get(0, "end").index(p[1]), bg="green")
    pygame.mixer.music.play()
    if play_bool:
        play_state = True
        play_bool = False
        play_button.configure(image=pause_photo)
    if next_Button2["state"] == DISABLED:
        play_button.configure(state=NORMAL)
        next_Button2.configure(state=NORMAL)
        prev_Button2.configure(state=NORMAL)
        shuffle_Button.configure(state=NORMAL)
        seek_bar.configure(state=NORMAL)
    current_playlist_name = selected.get()
    last_played = p
    stat_check()


def option_list():
    options = []
    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        if x[0] != "play_list":
            if x[0] == "song_list":
                options.append("All Songs")
            else:
                options.append(x[0])
    return options


def drop_func(val):
    global selected, check_list
    if val == "All Songs":
        listboxinit("song_list")
        del_button.configure(state=DISABLED)

    elif val in check_list:
        listboxinit(val)
        del_button.configure(state=DISABLED)

    else:
        listboxinit(val)
        if del_button['state'] == DISABLED:
            del_button.configure(state=NORMAL)
    manager.refresh_direc()


def listboxinit(name):
    song_listbox.delete(0, 'end')
    if name == "All Songs":
        mycursor.execute("SELECT * FROM " + "song_list")
    else:
        mycursor.execute("SELECT * FROM " + str(name))
    myresult = mycursor.fetchall()
    for x in myresult:
        song_listbox.insert('end', x[1])


def stat_check():
    global song_no, current_playlist_name, length_dict, autoplay_bool
    if current_playlist_name != "":
        if current_playlist_name == "All Songs":
            if song_no == length_dict["song_list"]:
                next_Button2.configure(state=DISABLED)
                autoplay_bool = False
            else:
                next_Button2.configure(state=NORMAL)
                autoplay_bool = True
        else:
            if song_no == length_dict[current_playlist_name]:
                next_Button2.configure(state=DISABLED)
                autoplay_bool = False
            else:
                next_Button2.configure(state=NORMAL)
                autoplay_bool = True
        if song_no == 1:
            prev_Button2.configure(state=DISABLED)
        else:
            prev_Button2.configure(state=NORMAL)


def seek_bar_init(music_len):
    global seeker
    seeker = 0
    seek_bar.set(0)
    seek_bar.configure(to=music_len)


def image_rezizer(path, height, width):
    image = Image.open(path)
    image = image.resize((height, width))
    image = ImageTk.PhotoImage(image)
    return image


def save_file(name, path, time, seek, song_number, playlist):
    f = open("tests/Save_data.txt", "w")
    f.write(str(name) + "\n" + str(path) + "\n" + str(time) + "\n" + str(seek) + "\n" + str(song_number) + "\n" + playlist)
    f.close()


def retrive_file():
    name = ""
    seek = 0
    path = 0
    time = 0
    song_number = 0
    playlist = 0
    f = open("tests/Save_data.txt", "r")
    Content = f.read()
    CoList = Content.split("\n")
    c = 0
    for i in CoList:
        c += 1
        if c == 1:
            name = i
        if c == 2:
            path = i
        if c == 3:
            time = i
            time = int(time)
        if c == 4:
            seek = i
            seek = int(seek)
        if c == 5:
            song_number = int(i)
        if c == 6:
            playlist = i

    f.close()
    return name, path, time, seek, song_number, playlist


def music_init():
    global autoplay_bool, seeker, play_bool, play_state, last_played, song_no, current_playlist_name
    t = retrive_file()
    last_played = t
    if t[1] != '':
        pygame.mixer.music.load(os.path.join(t[1], t[0]))
        playlist_title.configure(text=t[0])
        seeker = t[3]
        seek_bar.configure(to=t[2])
        song_no = t[4]
        current_playlist_name = t[5]
        play_state = True
        play_bool = False
        autoplay_bool = False
        thread.counter(t[2])
        play_bool = True
        pygame.mixer.music.set_volume(0)
        pygame.mixer.music.play(0, seeker)
        pygame.mixer.music.pause()
        play_button.configure(image=play_photo)
    else:
        play_button.configure(state=DISABLED)
        seek_bar.configure(state=DISABLED)
    #next_Button2.configure(state=DISABLED)
    #prev_Button2.configure(state=DISABLED)
    #shuffle_Button.configure(state=DISABLED)
    pygame.mixer.music.set_volume(0.5)
    vol_slider.set(50)


#################################################################################
# Colours bg-"#021c4b" text-"#9AECDB"
main_background_color = "#6f75a3"
text_color = "#9AECDB"

#################################################################################
# TKINTER WINDOW
top = Tk()
top.title("")
top.geometry("909x639")
top.resizable(False, False)
top.configure(background=main_background_color)

#################################################################################
# Media
prev_photo = image_rezizer(r"photos\fast-forward-media-control-button.png", 53, 56)
next_photo = image_rezizer(r"photos\fast-forward-media-control-button2.png", 53, 56)
play_photo = image_rezizer(r"photos\play-rounded-button.png", 49, 49)
pause_photo = image_rezizer(r"photos\pause.png", 49, 49)
mute_photo = image_rezizer(r"photos\mute.png", 22, 22)
max_photo = image_rezizer(r"photos\volume-interface-symbol.png", 22, 22)
add = image_rezizer(r"photos\add.png", 45, 45)
shuffle_inactive = image_rezizer(r"photos\shuffle inactive.png", 25, 25)
shuffle_active = image_rezizer(r"photos\shuffle active.png", 25, 25)
delete = image_rezizer(r"photos\Delete.png", 45, 45)

##########################################################################
# CLASS INIT

player = musicplayer()
manager = song_manager()
playlist = playlist_cotrols()
thread = thread_control()
file_thread = thread_control()
##########################################################################
# VARIABLES

# song controls
play_bool = True
play_state = False
song_no = 1
count = 0
shuffled = False
shuffle_list = {}
shuffle_count = 0
seeker = 0
vol = True
autoplay_bool = True

# Playlist variables
length_dict = playlist.table_length()
current_playlist_name = ""
last_played = ""

# Song time/length
music_len = 0.0
t1 = threading.Thread(target=thread.run, args=(music_len,))
t1.daemon = True

# Option menu
mycursor.execute("SELECT * FROM paths")
myresult = mycursor.fetchall()
check_list = []
for x in myresult:
    check_list.append(x[0])
options = option_list()
add_options = option_list()

# Removing unnecessary options
for x in options:
    if x == "paths":
        options.remove(x)
for x in add_options:
    if x == "paths":
        add_options.remove(x)
for x in add_options:
    if x == "All Songs":
        add_options.remove(x)
# Options menu variable
selected = StringVar()
selected2 = StringVar()

############################################################################
# FRAMES

main_Frame = Frame(top, background=main_background_color)
main_Frame.place(relx=0.011, rely=0.010, relheight=0.690, relwidth=0.966)

##########################################################################
# SEEK BAR
seek_frame = Frame(top, background=main_background_color, relief="groove", borderwidth="2")
seek_frame.place(relx=0.012, rely=0.720, relheight=0.07, relwidth=0.966)

# seek bar Color
seek_style = ttk.Style()
seek_style.configure('Horizontal.TScale', background=main_background_color)

seek_bar = Seek(seek_frame, from_=0, to=0, style="Horizontal.TScale")
seek_bar.place(relx=0.045, rely=0.25, relheight=0.5, relwidth=0.910)

min_label = Label(seek_frame, background=main_background_color, foreground=text_color)
min_label.place(x=1.0, y=6.8, height=25, width=35)

max_label = Label(seek_frame, background=main_background_color, foreground=text_color)
max_label.place(relx=0.958, rely=0.150, height=25, width=35)

###################################################################################
# MEDIA CONTROLS

# MEDIA CONTROL FRAME
media_control_frame = Frame(top, relief="groove", borderwidth="2", background=main_background_color)
media_control_frame.place(relx=0.012, rely=0.782, relheight=0.177, relwidth=0.966)

next_Button2 = Button(media_control_frame, command=lambda: player.next(), image=prev_photo,
                      background=main_background_color)
next_Button2.place(relx=0.646, rely=0.265, height=53, width=56)

play_button = Button(media_control_frame, image=play_photo, command=lambda: player.pause(),
                     background=main_background_color)
play_button.place(relx=0.465, rely=0.265, height=53, width=56)

prev_Button2 = Button(media_control_frame, image=next_photo, command=lambda: player.rewind(),
                      background=main_background_color)
prev_Button2.place(relx=0.286, rely=0.265, height=53, width=56)

shuffle_Button = Button(media_control_frame, command=player.shuffle, image=shuffle_inactive,
                        background=main_background_color)
shuffle_Button.place(relx=0.160, rely=0.354, height=30, width=30)

vol_slider = volume(media_control_frame, from_=0, to=100, orient=HORIZONTAL, command=player.vol, showvalue=0,
                    sliderlength=10, troughcolor="#876fa3", background=main_background_color,
                    highlightbackground=main_background_color)
vol_slider.place(relx=0.831, rely=0.354)

vol_min = Button(media_control_frame, command=player.min, image=mute_photo, background=main_background_color)
vol_min.place(relx=0.795, rely=0.350, height=28, width=28)

####################################################################################
# PLAYLIST

listbox_frame = Frame(main_Frame, background=main_background_color)
listbox_frame.place(relx=0.01, rely=0.21, relheight=0.748, relwidth=0.735)

scrollbar_Y = Scrollbar(listbox_frame, background=main_background_color)

song_listbox = Listbox(listbox_frame, yscrollcommand=scrollbar_Y.set, background=main_background_color,
                       foreground=text_color)
song_listbox.place(relx=0.001, rely=0.003, relheight=0.995, relwidth=0.973)
song_listbox.configure(font="TkFixedFont")
song_listbox.bind('<Double-1>', double_click)

scrollbar_Y.config(command=song_listbox.yview)
scrollbar_Y.pack(side='right', fill='y')


def playlist_drop():
    playlist_dropdown = OptionMenu(main_Frame, selected, *options, command=drop_func)
    playlist_dropdown.place(relx=0.02, rely=0.115, height=33, width=166)
    playlist_dropdown.configure(background=main_background_color, foreground=text_color,
                                highlightbackground=main_background_color)
    selected.set(options[0])


playlist_drop()

listboxinit(selected.get())

manage_playlist = Button(main_Frame, command=manage_list, text="Manage Playlists", background=main_background_color,
                         foreground=text_color)
manage_playlist.place(relx=0.25, rely=0.115, height=33, width=100)


####################################################################################
# PLAYLIST MODIFIERS/CONTROLS

def adds():
    if not add_options:
        add_button = OptionMenu(main_Frame, selected2, add_options, command=manager.add_func)
    else:
        add_button = OptionMenu(main_Frame, selected2, *add_options, command=manager.add_func)
    add_button.config(indicatoron=False, image=add, background=main_background_color,
                      highlightbackground=main_background_color)
    add_button.place(relx=0.775, rely=0.229, height=55, width=55)


adds()

del_button = Button(main_Frame, command=manager.del_func, image=delete, background=main_background_color,
                    highlightbackground=main_background_color)
del_button.place(relx=0.775, rely=0.401, height=55, width=55)

playlist_title = Label(main_Frame, background=main_background_color, foreground=text_color)
playlist_title.place(relx=0.234, rely=0.0008, height=46, width=508)

####################################################################################
# Menubar
progress = Progressbar(top, orient=HORIZONTAL, length=100, mode='determinate')

menubar = Menu(top)

file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file)
file.add_command(label='Open Folder', command=manager.direc)
file.add_separator()
file.add_command(label='Exit', command=top.destroy)

top.config(menu=menubar)

####################################################################################
# INITS
music_init()
player.autoplay()

###################################################################################
# END
top.update_idletasks()
top.mainloop()

if last_played != "":
    if str(last_played[0])[0].isnumeric():
        save_file(last_played[1], last_played[2], last_played[3], seeker,song_no, current_playlist_name)
    elif str(last_played[0])[0].isalnum():
        save_file(last_played[0], last_played[1], last_played[2], seeker, song_no, current_playlist_name)
