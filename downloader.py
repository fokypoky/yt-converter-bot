from pytube import YouTube
import os
import moviepy.editor as mp
import telebot
from telebot import types
import asyncio

api_token = 'your token'
bot = telebot.TeleBot(api_token)

users_collection = {}

def downloadYouTube(videourl, output_path, file_name):
    yt = YouTube(videourl)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    yt.download(output_path=output_path, filename=file_name)

def convert_to_mp3(input_file_path, output_file_path):
    video = mp.VideoFileClip(input_file_path)
    audio = video.audio
    audio.write_audiofile(output_file_path)
    audio.close()
    video.close()

@bot.message_handler(commands=['start'])
def on_start_command(message: types.Message) -> None:
    hello_message = 'Hi! This bot allows you to download videos from YouTube in mp3 format. To get started send a link to the video'
    bot.send_message(message.chat.id, hello_message)

@bot.message_handler(content_types=['text'])
def on_text_received(message: types.Message):
    try:
        mp4_file_name = f'{message.chat.id}.mp4'
        mp3_file_name = f'{message.chat.id}.mp3'

        print(mp3_file_name)

        users_collection[message.chat.id] = [mp4_file_name, mp3_file_name]
        bot.send_message(message.chat.id, 'Started processing. Please wait...')
        
        downloadYouTube(message.text, '.', mp4_file_name)
        convert_to_mp3(mp4_file_name, mp3_file_name)
        
        audio = open(mp3_file_name, 'rb')
        bot.send_audio(message.chat.id, audio)
        audio.close()
    except:
        bot.send_message(message.chat.id, 'Sorry, something went wrong... Try again')
    finally:
        if os.path.exists(mp4_file_name):
            os.remove(mp4_file_name)
        
        if os.path.exists(mp3_file_name):
            os.remove(mp3_file_name)
        
        users_collection.pop(message.chat.id)

bot.polling()