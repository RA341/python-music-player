from tkinter import *
from PIL import ImageTk, Image
import pygame
from os import listdir
import random
import time

class musicplayer():

    def pause(self):
        global play_bool, loops, play_state
        if play_bool:
            if not play_state:
                play_state = True
                play_bool = False
                pygame.mixer.music.play(loops)
            elif play_state:
                play_bool = False
                pygame.mixer.music.unpause()
            play_button.configure(image=pause_photo)
        elif not play_bool:
            play_bool = True
            play_button.configure(image=play_photo)
            pygame.mixer.music.pause()

    def rewind(self):
        global song_no, count, play_state, play_bool
        count += 1
        if count == 1:
            pygame.mixer.music.rewind()
        elif count == 2:
            if song_no == 0:
                song_no = len(music_list) - 1
            else:
                song_no -= 1
            title_Label.configure(text=music_list[song_no])
            pygame.mixer.music.load(r"songs/"+music_list[song_no])
            pygame.mixer.music.play(loops)
            play_button.configure(image=pause_photo)
            if play_bool:
                play_state = True
                play_bool = False
        else:
            pygame.mixer.music.rewind()
            count = 1
        stat_check()

    def next(self):
        global song_no, play_bool, play_state
        song_no += 1
        if song_no > len(music_list) - 1:
            song_no = 0
        stat_check()
        title_Label.configure(text=music_list[song_no])
        pygame.mixer.music.load(r"songs/"+music_list[song_no])
        pygame.mixer.music.play(loops)
        play_button.configure(image=pause_photo)
        if play_bool:
            play_state = True
            play_bool = False


def next_song():
    global song_no
    player.next()


def prev_song():
    global song_no
    player.rewind()


def pausesong():
    global play_bool, loops
    player.pause()


def music_init():
    pygame.mixer.init()
    pygame.mixer.music.load(r"songs/"+music_list[0])
    title_Label.configure(text=music_list[0])

def vol():
    global vol_bool
    if vol_bool:
        pygame.mixer.music.set_volume(0)
        vol_bool = False
    elif not vol_bool:
        pygame.mixer.music.set_volume(1)
        vol_bool = True

def stat_check():
    global song_no
    if song_no == 0:
        prev_Button2.configure(state=DISABLED)
    else:
        prev_Button2.configure(state=NORMAL)

def autoplay():
    global play_bool, song_no, play_state
    pos = pygame.mixer.music.get_pos()
    if not pygame.mixer.music.get_busy() and play_state:
        if int(pos) == -1:
            if song_no <= len(music_list) - 1:
                song_no += 1
            elif song_no == len(music_list) - 1:
                song_no = 0
                pygame.mixer.pause()
                play_button.configure(image=play_photo)
            pygame.mixer.music.load(r"songs/"+music_list[song_no])
            pygame.mixer.music.play()
            title_Label.configure(text=music_list[song_no])
            stat_check()

    top.after(1, autoplay)

def listgen(path):
    l = []
    for file in listdir(path):
        if file.endswith(".mp3"):
            l.append(file)
    return l

def image_rezizer(path, height, width):
    image = Image.open(path)
    image = image.resize((height, width))
    image = ImageTk.PhotoImage(image)
    return image


top = Tk()

# global var

prev_photo = image_rezizer(r"photos\fast-forward-media-control-button.png", 53, 56)
next_photo = image_rezizer(r"photos\fast-forward-media-control-button2.png", 53, 56)
play_photo = image_rezizer(r"photos\play-rounded-button.png", 49, 49)
pause_photo = image_rezizer(r"photos\pause.png", 49, 49)

player = musicplayer()
music_list = listgen("songs")
random.shuffle(music_list)

play_bool = True
play_state = False
loops = 0
seek = 0
song_no = 0
count = 0
auto = True
vol_bool = True


top.geometry("909x639+979+13")
top.minsize(148, 1)
top.maxsize(1924, 1030)
top.resizable(1, 1)
top.title("New Toplevel")
top.configure(background="#d9d9d9")

title_Frame = Frame(top)
title_Frame.place(relx=0.012, rely=0.031, relheight=0.117, relwidth=0.966)
title_Frame.configure(relief='groove')
title_Frame.configure(borderwidth="2")
title_Frame.configure(relief="groove")
title_Frame.configure(background="#d9d9d9")

media_Frame = Frame(top)
media_Frame.place(relx=0.012, rely=0.782, relheight=0.177, relwidth=0.966)
media_Frame.configure(relief='groove')
media_Frame.configure(borderwidth="2")
media_Frame.configure(relief="groove")
media_Frame.configure(background="#d9d9d9")

main_Frame = Frame(top)
main_Frame.place(relx=0.011, rely=0.172, relheight=0.476
                 , relwidth=0.966)
main_Frame.configure(relief='groove')
main_Frame.configure(borderwidth="2")
main_Frame.configure(relief="groove")
main_Frame.configure(background="#d9d9d9")

seek_frame = Frame(top)
seek_frame.place(relx=0.012, rely=0.689, relheight=0.07, relwidth=0.966)
seek_frame.configure(relief='groove')
seek_frame.configure(borderwidth="2")
seek_frame.configure(relief="groove")
seek_frame.configure(background="#d9d9d9")

title_Label = Label(title_Frame)
title_Label.place(relx=0.211, rely=0.133, height=46, width=504)
title_Label.configure(background="#d9d9d9")
title_Label.configure(disabledforeground="#a3a3a3")
title_Label.configure(foreground="#000000")
title_Label.configure(text="TITLE")

music_init()

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
next_Button2.configure(command=lambda: next_song())
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
play_button.configure(command=lambda: pausesong())
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
prev_Button2.configure(command=lambda: prev_song())
prev_Button2.configure(image=next_photo)

shuffle_Button = Button(media_Frame)
shuffle_Button.place(relx=0.124, rely=0.354, height=43, width=36)
shuffle_Button.configure(activebackground="#ececec")
shuffle_Button.configure(activeforeground="#000000")
shuffle_Button.configure(background="#d9d9d9")
shuffle_Button.configure(disabledforeground="#a3a3a3")
shuffle_Button.configure(foreground="#000000")
shuffle_Button.configure(highlightbackground="#d9d9d9")
shuffle_Button.configure(highlightcolor="black")
shuffle_Button.configure(pady="0")
shuffle_Button.configure(text="LOOP")

add_Button = Button(media_Frame)
add_Button.place(relx=0.831, rely=0.354, height=43, width=36)
add_Button.configure(activebackground="#ececec")
add_Button.configure(activeforeground="#000000")
add_Button.configure(background="#d9d9d9")
add_Button.configure(disabledforeground="#a3a3a3")
add_Button.configure(foreground="#000000")
add_Button.configure(highlightbackground="#d9d9d9")
add_Button.configure(highlightcolor="black")
add_Button.configure(pady="0")
add_Button.configure(command=lambda: vol())
add_Button.configure(text="ADD")

photo_Label = Label(main_Frame)
photo_Label.place(relx=0.298, rely=0.066, height=256, width=353)
photo_Label.configure(background="#d9d9d9")
photo_Label.configure(disabledforeground="#a3a3a3")
photo_Label.configure(foreground="#000000")
photo_Label.configure(text="PHOTO")

prev_Button = Button(main_Frame)
prev_Button.place(relx=0.013, rely=0.066, height=263, width=56)
prev_Button.configure(activebackground="#ececec")
prev_Button.configure(activeforeground="#000000")
prev_Button.configure(background="#d9d9d9")
prev_Button.configure(disabledforeground="#a3a3a3")
prev_Button.configure(foreground="#000000")
prev_Button.configure(highlightbackground="#d9d9d9")
prev_Button.configure(highlightcolor="black")
prev_Button.configure(command=lambda: prev_song())
prev_Button.configure(text="PREV")

next_Button = Button(main_Frame)
next_Button.place(relx=1.925, rely=0.164, height=263, width=56)
next_Button.configure(activebackground="#ececec")
next_Button.configure(activeforeground="#000000")
next_Button.configure(background="#d9d9d9")
next_Button.configure(disabledforeground="#a3a3a3")
next_Button.configure(foreground="#000000")
next_Button.configure(highlightbackground="#d9d9d9")
next_Button.configure(highlightcolor="black")
next_Button.configure(pady="0")
next_Button.configure(command=lambda: next_song())
next_Button.configure(text="NEXT")

Button1 = Button(main_Frame)
Button1.place(relx=0.923, rely=0.066, height=263, width=56)
Button1.configure(activebackground="#ececec")
Button1.configure(activeforeground="#000000")
Button1.configure(background="#d9d9d9")
Button1.configure(disabledforeground="#a3a3a3")
Button1.configure(foreground="#000000")
Button1.configure(highlightbackground="#d9d9d9")
Button1.configure(highlightcolor="black")
Button1.configure(pady="0")
Button1.configure(text="NEXT")

# menubar = Menu(top, font="TkMenuFont", bg="#d9d9d9", fg="#d9d9d9")
# top.configure(menu=menubar)

stat_check()
autoplay()

top.mainloop()
