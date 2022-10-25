#!/usr/bin/env python3
from os import lseek
from random import random
import praw
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import textwrap
from moviepy.editor import *
from string import ascii_letters
from flask import Flask, request
app= Flask(__name__)





class Scraper:
    def __init__(self, sub, isReddit, title):
        if isReddit:
            self.set_up_reddit()
            self.manual_submission(sub)
            self.relative_path = ''
        else:
            print(sub)
            print(title)
            self.gpt_3_choice(sub, title)
    


    # load env creds
    def load_creds(self, env_file):
        f = open(env_file)
        lines = f.readlines()
        env_vars = {}
        for line in lines:
            var = line.split("=")
            final = [elt.strip() for elt in var]
            env_vars[final[0]] = final[1]
        f.close()
        return env_vars


    # Use praw to get access to reddit
    def set_up_reddit(self):
        cred = self.load_creds('.env')
        # client_id = cred["CLIENT_ID"]
        client_id = ''
        # client_secret=cred["CLIENT_SECRET"]
        client_secret = ''
        user_agent = "Scraper 1.0 by /u/Candid-Cantaloupe-24"
        self.reddit = praw.Reddit(
            client_id =  client_id,
            client_secret=client_secret,
            user_agent = user_agent,
            check_for_async=False
        )
        



    # Make a separate file for just the title page + audio
    def convert_title(self, text, sub_id):
        url = './assets/audio/'+ sub_id +'_title.mp3'
        title = gTTS(text=text , lang='en')
        title.save(url)


    # Generate the description audio and store references to audio files and their text
    def convert_description(self, text, sub_id):
        url = './assets/audio/'
        size, i= len(text), 0
        print(size)
        m = []
        part = 0
        while i < size:
            sentence = ''
            counter = 0
            while i < size and counter < 20:
                sentence += ' '+ text[i]
                counter+=1
                i+=1
            ten_sec_bit = gTTS(text=sentence , lang='en')
            ten_sec_bit.save(url+sub_id +'_'+str(part)+'.mp3')
            m.append([sentence, url+sub_id +'_'+str(part)+'.mp3'])
            part+=1
        return m



    # Generate subclip
    def generate_clip(self, text, audio_url, sub_id, num):
        # Static variables to fit tiktok size window
        print(text)
        width = 800
        height = 512
        # Create new image to write text
        img = Image.new('RGB', (width, height))
        font = ImageFont.truetype(font='./assets/SourceCodePro-Bold.ttf', size=24)
        imgDraw = ImageDraw.Draw(img)
        avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
        max_char_count = int(width * .618 / avg_char_width)
        lines = textwrap.fill(text=text, width=max_char_count)
        imgDraw.text(xy=(width/2, height / 2), text=lines, font=font, fill='#FFFFFF', anchor='mm')
        img.save('./assets/images/'+sub_id+'_'+str(num)+'.png')
        audio_clip = AudioFileClip('./assets/audio/'+sub_id+'_'+str(num)+'.mp3')
        duration = audio_clip.duration
        clip = ImageClip('./assets/images/'+sub_id+'_'+str(num)+'.png').set_duration(duration)
        return clip, audio_clip
        


    def generate_video(self, title, sub_id, description_text_ref):
        try: 
            # generate title clip
            video, audio_seg = self.generate_clip(title,'./assets/audio/' +sub_id+'_title.mp3', sub_id, 'title')
            clips = [video]
            audio = [audio_seg]
            # generate description clips and add to array
            for i in range(len(description_text_ref)):
                print('in loop: ', description_text_ref[i][0])
                video_clip, audio_clip = self.generate_clip(description_text_ref[i][0], description_text_ref[i][1], sub_id, i)
                clips.append(video_clip)
                audio.append(audio_clip)
            # concat all the video clips together
            concat_video_clip = concatenate_videoclips(clips, method="compose")
            # concat all the audio clips together
            concat_audio = concatenate_audioclips(audio)
            concat_video_clip.audio = concat_audio
            # Write to mp4 file
            concat_video_clip.write_videofile('./assets/videos/'+sub_id+'_final.mp4', fps=24)
            self.relative_path= '/assets/videos/' + sub_id + '_final.mp4'
            return './assets/videos/'+sub_id+'_final.mp4', 
        except Exception as e:
            raise Exception('Could not make video :(')



    def manual_submission(self, url):
        sub = self.reddit.submission(url=url)
        title =sub.title.replace('fuck', 'duck').replace('dick', 'd').replace('aita', 'am I the a-hole')
        print(title)
        description = sub.selftext.replace('fuck', 'duck').replace('dick', 'd').split(' ')
        self.convert_title(title, sub.id)
        description_text_map = self.convert_description(description, sub.id)  
        video_url = self.generate_video(title, sub.id, description_text_map)
        return video_url


    def get_url(self):
        print(self.relative_path)
        return self.relative_path


    def gpt_3_choice(self, story, title):
        num=0
        title_desc = self.convert_title(title, 'gpt3')
        story_des = self.convert_description(story, 'gpt3')
        print(story_des)
        video_url = self.generate_video(title_desc, 'gpt3', story_des )
        return video_url



if __name__ == "__main__":
    url = input("Enter a reddit post\n")
    x = Scraper(url, True, None)