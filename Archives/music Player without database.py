from tkinter import *
from PIL import ImageTk, Image
import pygame
from os import listdir
import os
import random
from mutagen.mp3 import MP3
import time
import threading


class musicplayer:

    def pause(self):
        global play_bool, loops, play_state
        if play_bool:
            if not play_state:
                pygame.mixer.music.play(loops)
                play_state = True
                play_bool = False

            elif play_state:
                pygame.mixer.music.unpause()
                play_bool = False

            play_button.configure(image=pause_photo)
        elif not play_bool:
            pygame.mixer.music.pause()
            play_bool = True
            play_button.configure(image=play_photo)


    def rewind(self):
        global song_no, count, play_state, play_bool
        count += 1
        if count == 2:
            if song_no == 0:
                song_no = len(music_list) - 1
            else:
                song_no -= 1
            title_Label.configure(text=music_list[song_no])
            Label1.configure(text=music_list[song_no])
            play_button.configure(image=pause_photo)
            music_len = MP3(r"songs/" + music_list[song_no]).info.length
            pygame.mixer.music.load(r"songs/" + music_list[song_no])
            song_list.selection_clear(song_list.get(0, "end").index(music_list[song_no - 1]))
            song_list.selection_set(song_list.get(0, "end").index(music_list[song_no]))
            if play_bool:
                play_state = True
                play_bool = False
            thread.counter(music_len)
            pygame.mixer.music.play(loops)
        else:
            if count > 2:
                count = 1
            pygame.mixer.music.rewind()
        stat_check()

    def next(self):
        global song_no, play_bool, play_state
        song_list.selection_clear(song_list.get(0, "end").index(music_list[song_no]))
        song_no += 1
        if song_no > len(music_list) - 1:
            song_no = 0
        music_len = MP3(r"songs/" + music_list[song_no]).info.length
        title_Label.configure(text=music_list[song_no])
        Label1.configure(text=music_list[song_no])
        pygame.mixer.music.load(r"songs/" + music_list[song_no])
        play_button.configure(image=pause_photo)
        # song_list.selection_clear(song_list.get(0, "end").index(music_list[song_no-1]))
        song_list.selection_set(song_list.get(0, "end").index(music_list[song_no]))
        if play_bool:
            play_state = True
            play_bool = False
        stat_check()
        thread.counter(music_len)
        pygame.mixer.music.play(loops)

    def autoplay(self):
        global play_bool, song_no, play_state, t1
        if not pygame.mixer.music.get_busy() and play_state:
            song_list.selection_clear(song_list.get(0, "end").index(music_list[song_no]))
            pos = pygame.mixer.music.get_pos()
            if int(pos) == -1:
                if song_no <= len(music_list) - 1:
                    song_no += 1
                elif song_no == len(music_list) - 1:
                    song_no = 0
                    pygame.mixer.pause()
                    play_bool = True
                    play_button.configure(image=play_photo)
                music_len = MP3(r"songs/" + music_list[song_no]).info.length
                title_Label.configure(text=music_list[song_no])
                Label1.configure(text=music_list[song_no])
                song_list.selection_set(song_list.get(0, "end").index(music_list[song_no]))
                thread.counter(music_len)
                pygame.mixer.music.load(r"songs/" + music_list[song_no])
                pygame.mixer.music.play()
                stat_check()

        top.after(1, self.autoplay)

    def vol(self, val):
        v = float(val) * 0.01
        pygame.mixer.music.set_volume(v)

    def min(self):
        pygame.mixer.music.set_volume(0)
        vol_slider.set(0)

    def max(self):
        pygame.mixer.music.set_volume(1.0)
        vol_slider.set(100)


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
        max_sec = 0
        n = round(n)
        while self._running and n > 0:
            if not play_bool:
                max_time_list = self.convert(max_sec)
                min_time_list = self.convert(n)
                min_label.configure(text=str(max_time_list[1]).zfill(2) + ":" + str(max_time_list[2]).zfill(2))
                max_label.configure(text=str(min_time_list[1]).zfill(2) + ":" + str(min_time_list[2]).zfill(2))
                time.sleep(1)
                n -= 1
                max_sec += 1

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


def music_init():
    global music_len, music_list
    pygame.mixer.init()
    music_list = manager.listgen("songs")
    pygame.mixer.music.load(r"songs/" + music_list[song_no])
    title_Label.configure(text=music_list[song_no])
    pygame.mixer.music.set_volume(0.5)
    vol_slider.set(0.5 / 0.01)


def stat_check():
    global song_no
    if song_no == 0:
        prev_Button2.configure(state=DISABLED)
    else:
        prev_Button2.configure(state=NORMAL)


def image_rezizer(path, height, width):
    image = Image.open(path)
    image = image.resize((height, width))
    image = ImageTk.PhotoImage(image)
    return image


class song_manager:
    def listgen(self, path):
        song_dict = {}
        song_no = 0
        for file in listdir(path):
            song_no += 1
            if file.endswith(".mp3"):
                song_dict[song_no] = file
        return song_dict

    def get_key(self, val):
        for key, value in music_list.items():
            if val == value:
                return key


def double_click(event):
    global song_no, music_list, play_bool, play_state
    song = song_list.selection_get()
    song_no = manager.get_key(song)
    pygame.mixer.music.load(os.path.join(r"songs", song))
    music_len = MP3(r"songs/" + song).info.length
    title_Label.configure(text=song)
    Label1.configure(text=song)
    play_button.configure(image=pause_photo)
    Label1.configure(text=song)
    if play_bool:
        play_state = True
        play_bool = False
    stat_check()
    thread.counter(music_len)
    pygame.mixer.music.play()


def listboxinit():
    global music_list
    for item in music_list.values():
        song_list.insert('end', item)


def view_change():
    global view_bool
    if view_bool:
        playlist_view_frame.lift(song_view_frame)
        view_bool = False
    elif not view_bool:
        song_view_frame.lift(playlist_view_frame)
        view_bool = True


top = Tk()

##########################################################################
# Pics

prev_photo = image_rezizer(r"photos\fast-forward-media-control-button.png", 53, 56)
next_photo = image_rezizer(r"photos\fast-forward-media-control-button2.png", 53, 56)
play_photo = image_rezizer(r"photos\play-rounded-button.png", 49, 49)
pause_photo = image_rezizer(r"photos\pause.png", 49, 49)
mute_photo = image_rezizer(r"photos\mute.png", 20, 20)
max_photo = image_rezizer(r"photos\volume-interface-symbol.png", 20, 20)
music_view = image_rezizer(r"photos\musical-note.png", 25, 25)
list_view = image_rezizer(r"photos\list.png", 25, 25)

##########################################################################
# VARIABLES
thread = thread_control()
play_bool = True
play_state = False
loops = 0
seek = 0
song_no = 1
count = 0
music_len = 0.0
t1 = threading.Thread(target=thread.run, args=(music_len,))
t1.daemon = True
view_bool = True
music_list = {}
sleep = 0

##########################################################################
# CLASS/SONGLIST INIT

player = musicplayer()
manager = song_manager()

###########################################################################
# TKINTER WINDOW
top.geometry("909x639+979+13")
top.minsize(148, 1)
top.maxsize(1924, 1030)
top.resizable(1, 1)
top.title("New Toplevel")
top.configure(background="#d9d9d9")

############################################################################
# FRAMES

main_Frame = Frame(top)
main_Frame.place(relx=0.011, rely=0.010, relheight=0.690, relwidth=0.966)
main_Frame.configure(relief="groove")
main_Frame.configure(borderwidth="2")
main_Frame.configure(background="#d9d9d9")

playlist_view_frame = Frame(main_Frame)
playlist_view_frame.place(relx=0.000, rely=0.000, relheight=1.0, relwidth=1.0)
playlist_view_frame.configure(relief="groove")
playlist_view_frame.configure(borderwidth="2")
playlist_view_frame.configure(background="#d9d9d9")

song_view_frame = Frame(main_Frame)
song_view_frame.place(relx=0.000, rely=0.000, relheight=1.0, relwidth=1.0)
song_view_frame.configure(relief="groove")
song_view_frame.configure(borderwidth="2")
song_view_frame.configure(background="#d9d9d9")

playlist_frame = Frame(playlist_view_frame)
playlist_frame.place(relx=0.009, rely=0.018, relheight=0.946, relwidth=0.887)
playlist_frame.configure(relief='groove')
playlist_frame.configure(borderwidth="2")
playlist_frame.configure(relief="groove")
playlist_frame.configure(background="#d9d9d9")
playlist_frame.configure(highlightbackground="#d9d9d9")
playlist_frame.configure(highlightcolor="black")

title_Frame = Frame(song_view_frame)
title_Frame.place(relx=0.012, rely=0.031, relheight=0.117, relwidth=0.966)
title_Frame.configure(relief='groove')
title_Frame.configure(borderwidth="2")
title_Frame.configure(relief="groove")
title_Frame.configure(background="#d9d9d9")

listbox_frame = Frame(playlist_view_frame)
listbox_frame.place(relx=0.01, rely=0.21, relheight=0.748, relwidth=0.735)
listbox_frame.configure(relief='groove')
listbox_frame.configure(borderwidth="2")
listbox_frame.configure(relief="groove")
listbox_frame.configure(background="#d9d9d9")

##########################################################################
# SEEK BAR

seek_frame = Frame(top)
seek_frame.place(relx=0.012, rely=0.720, relheight=0.07, relwidth=0.966)
seek_frame.configure(relief='groove')
seek_frame.configure(borderwidth="2")
seek_frame.configure(relief="groove")
seek_frame.configure(background="#d9d9d9")

min_label = Label(seek_frame)
min_label.place(x=0.70, y=6.8, height=25, width=35)

max_label = Label(seek_frame)
max_label.place(relx=0.958, rely=0.150, height=25, width=35)

###################################################################################
# MEDIA CONTROL FRAME

media_Frame = Frame(top)
media_Frame.place(relx=0.012, rely=0.782, relheight=0.177, relwidth=0.966)
media_Frame.configure(relief='groove')
media_Frame.configure(borderwidth="2")
media_Frame.configure(relief="groove")
media_Frame.configure(background="#d9d9d9")
###################################################################################
# SONG VIEW

title_Label = Label(title_Frame)
title_Label.place(relx=0.211, rely=0.100, height=40, width=504)
title_Label.configure(background="#d9d9d9")
title_Label.configure(disabledforeground="#a3a3a3")
title_Label.configure(foreground="#000000")
title_Label.configure(text="TITLE")
###################################################################################
# MEDIA CONTROLS

vol_slider = Scale(media_Frame, from_=0, to=100, orient=HORIZONTAL)
vol_slider.place(relx=0.831, rely=0.354)
vol_slider.configure(sliderlength=15)
vol_slider.configure(activebackground="#ececec")
vol_slider.configure(background="#d9d9d9")
vol_slider.configure(foreground="#000000")
vol_slider.configure(highlightbackground="#d9d9d9")
vol_slider.configure(highlightcolor="black")
vol_slider.configure(showvalue=0)
vol_slider.configure(command=player.vol)

vol_min = Button(media_Frame)
vol_min.place(relx=0.795, rely=0.354, height=25, width=25)
vol_min.configure(image=mute_photo)
vol_min.configure(command=player.min)

vol_max = Button(media_Frame)
vol_max.place(relx=0.958, rely=0.354, height=25, width=25)
vol_max.configure(image=max_photo)
vol_max.configure(command=player.max)

next_Button2 = Button(media_Frame)
next_Button2.place(relx=0.646, rely=0.265, height=53, width=56)
next_Button2.configure(activebackground="#ececec")
next_Button2.configure(activeforeground="#000000")
next_Button2.configure(background="#d9d9d9")
next_Button2.configure(disabledforeground="#a3a3a3")
next_Button2.configure(foreground="#000000")
next_Button2.configure(highlightbackground="#d9d9d9")
next_Button2.configure(highlightcolor="black")
next_Button2.configure(pady="0")
next_Button2.configure(image=prev_photo)
next_Button2.configure(command=lambda: player.next())
next_Button2.configure(text="NEXT")

play_button = Button(media_Frame)
play_button.place(relx=0.465, rely=0.265, height=53, width=56)
play_button.configure(activebackground="#ececec")
play_button.configure(activeforeground="#000000")
play_button.configure(background="#d9d9d9")
play_button.configure(disabledforeground="#a3a3a3")
play_button.configure(foreground="#000000")
play_button.configure(highlightbackground="#d9d9d9")
play_button.configure(highlightcolor="black")
play_button.configure(pady="0")
play_button.configure(command=lambda: player.pause())
play_button.configure(image=play_photo)

prev_Button2 = Button(media_Frame)
prev_Button2.place(relx=0.286, rely=0.265, height=53, width=56)
prev_Button2.configure(activebackground="#ececec")
prev_Button2.configure(activeforeground="#000000")
prev_Button2.configure(background="#d9d9d9")
prev_Button2.configure(disabledforeground="#a3a3a3")
prev_Button2.configure(foreground="#000000")
prev_Button2.configure(highlightbackground="#d9d9d9")
prev_Button2.configure(highlightcolor="black")
prev_Button2.configure(pady="0")
prev_Button2.configure(command=lambda: player.rewind())
prev_Button2.configure(image=next_photo)

####################################################################################
# PLAYLIST/SONG VIEW

options = []

Label1 = Label(playlist_frame)
Label1.place(relx=0.234, rely=0.038, height=46, width=508)
Label1.configure(activebackground="#f9f9f9")
Label1.configure(activeforeground="black")
Label1.configure(background="#d9d9d9")
Label1.configure(disabledforeground="#a3a3a3")
Label1.configure(foreground="#000000")
Label1.configure(highlightbackground="#d9d9d9")
Label1.configure(highlightcolor="black")

selected = StringVar()
# selected.set(options[0])
"""
playlist_dropdown = OptionMenu(playlist_view_frame, selected, *options)
playlist_dropdown.place(relx=0.02, rely=0.115, height=33, width=166)
playlist_dropdown.configure(activebackground="#ececec")
playlist_dropdown.configure(activeforeground="#000000")
playlist_dropdown.configure(background="#d9d9d9")
playlist_dropdown.configure(disabledforeground="#a3a3a3")
playlist_dropdown.configure(foreground="#000000")
playlist_dropdown.configure(highlightbackground="#d9d9d9")
playlist_dropdown.configure(highlightcolor="black")
playlist_dropdown.configure(pady="0")
playlist_dropdown.configure(text='''Button''')
"""

b2 = Button(playlist_view_frame, image=music_view, width=25, height=25, command=view_change)
b3 = Button(song_view_frame, image=list_view, width=25, height=25, command=view_change)
b2.place(x=820, y=385)
b3.place(x=820, y=385)

scrollbar = Scrollbar(listbox_frame)
scrollbar.pack(side='right', fill='y')

song_list = Listbox(listbox_frame)
song_list.place(relx=0.001, rely=0.003, relheight=0.995, relwidth=0.973)
song_list.configure(background="white")
song_list.configure(disabledforeground="#a3a3a3")
song_list.configure(font="TkFixedFont")
song_list.configure(foreground="#000000")
song_list.configure(yscrollcommand=scrollbar.set)

scrollbar.config(command=song_list.yview)
song_list.bind('<Double-1>', double_click)

####################################################################################
# PLAYLIST MODIFIERS/CONTROLS

add_button = Button(playlist_frame)
add_button.place(relx=0.865, rely=0.229, height=55, width=55)
add_button.configure(activebackground="#ececec")
add_button.configure(activeforeground="#000000")
add_button.configure(background="#d9d9d9")
add_button.configure(disabledforeground="#a3a3a3")
add_button.configure(foreground="#000000")
add_button.configure(highlightbackground="#d9d9d9")
add_button.configure(highlightcolor="black")
add_button.configure(pady="0")
add_button.configure(text='''Button''')

some_button = Button(playlist_frame)
some_button.place(relx=0.865, rely=0.401, height=55, width=55)
some_button.configure(activebackground="#ececec")
some_button.configure(activeforeground="#000000")
some_button.configure(background="#d9d9d9")
some_button.configure(disabledforeground="#a3a3a3")
some_button.configure(foreground="#000000")
some_button.configure(highlightbackground="#d9d9d9")
some_button.configure(highlightcolor="black")
some_button.configure(pady="0")
some_button.configure(text='''Button''')

some_butoon_2 = Button(playlist_frame)
some_butoon_2.place(relx=0.865, rely=0.573, height=55, width=55)
some_butoon_2.configure(activebackground="#ececec")
some_butoon_2.configure(activeforeground="#000000")
some_butoon_2.configure(background="#d9d9d9")
some_butoon_2.configure(disabledforeground="#a3a3a3")
some_butoon_2.configure(foreground="#000000")
some_butoon_2.configure(highlightbackground="#d9d9d9")
some_butoon_2.configure(highlightcolor="black")
some_butoon_2.configure(pady="0")
some_butoon_2.configure(text='''Button''')

some_button_3 = Button(playlist_frame)
some_button_3.place(relx=0.865, rely=0.744, height=55, width=55)
some_button_3.configure(activebackground="#ececec")
some_button_3.configure(activeforeground="#000000")
some_button_3.configure(background="#d9d9d9")
some_button_3.configure(disabledforeground="#a3a3a3")
some_button_3.configure(foreground="#000000")
some_button_3.configure(highlightbackground="#d9d9d9")
some_button_3.configure(highlightcolor="black")
some_button_3.configure(pady="0")
some_button_3.configure(text='''Button''')

####################################################################################
# INITS
music_init()
listboxinit()
t1.start()
thread.counter(music_len)
stat_check()
player.autoplay()

###################################################################################
# END
top.update_idletasks()
top.mainloop()
