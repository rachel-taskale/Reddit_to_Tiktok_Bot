# import pandas as pd
import praw
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *
import textwrap
from moviepy.editor import *
from string import ascii_letters



class Scraper:
    def __init__(self):
        pass

    def __init__(self, url):
        self.set_up_reddit()
        self.manual_submission(url)

        pass


    def set_up_reddit(self):
        # cred = load_creds('.env')
        # client_id = cred["CLIENT_ID"]
        # client_secret=cred["CLIENT_SECRET"]
        user_agent = "Scraper 1.0 by /u/Candid-Cantaloupe-24"
        self.reddit = praw.Reddit(
            client_id = "",
            client_secret="",
            user_agent = user_agent,
            check_for_async=False
        )
        # reddit_submissions = []
        

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


    # Make a separate file for just the title page + audio
    def convert_title(self, text, sub_id):
        url = './audio/'+ sub_id +'_title.mp3'
        title = gTTS(text=text , lang='en')
        title.save(url)

    # generate the description audio and store references to audio files and their text
    def convert_description(self, text, sub_id):
        url = './audio/'
        size, i= len(text), 0
        m = []
        part = 0
        while i < size:
            sentence = ''
            counter = 0
            while i < size and counter < 15:
                sentence += ' '+ text[i]
                counter+=1
                i+=1
            ten_sec_bit = gTTS(text=sentence , lang='en')
            ten_sec_bit.save(url+sub_id +'_'+str(part)+'.mp3')
            m.append([sentence, url+sub_id +'_'+str(part)+'.mp3'])
            part+=1
        return m



    # Generate subclip
    def generate_clip(self, text, audio_url, sub_id):
        width = 800
        height = 512
        img = Image.new('RGB', (width, height))
        font = ImageFont.truetype(font='SourceCodePro-Bold.ttf', size=24)
        
        
        imgDraw = ImageDraw.Draw(img)
        avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
        max_char_count = int(width * .618 / avg_char_width)
        lines = textwrap.fill(text=text, width=max_char_count)
        
        imgDraw.text(xy=(width/2, height / 2), text=lines, font=font, fill='#FFFFFF', anchor='mm')
       
        img.show()
        
        
        # audio_file = AudioFileClip(audio_url)
        # clip = ImageClip(img).set_duration(audio_file.duration)
        # clip.set_audio(audio_file)
        # return clip
        
        pass
        

    def generate_video(self, title, sub_id, description_text_ref):
        idx = 0
        movie = self.generate_clip(title,'./audio/' +sub_id+'_title.mp3', sub_id)
        for i in range(len(description_text_ref)):
            self.generate_clip(description_text_ref[i][0], description_text_ref[i][1], sub_id)
            # movie = concatenate_videoclips([movie, generate_clip(description_text_ref[i][0], description_text_ref[i][1], sub_id)])
        
        movie.ipython_display(width = 800)
        return movie




    def manual_submission(self, url):
        sub = self.reddit.submission(url=url)
        title =sub.title.replace('fuck', 'duck').replace('dick', 'd').replace('aita', 'am I the a-hole')
        description = sub.selftext.replace('fuck', 'duck').replace('dick', 'd').split(' ')
        # self.reddit_submissions.append([title, sub.id])
        self.convert_title(title, sub.id)
        description_text_map = self.convert_description(description, sub.id)  
        # print(description_text_map) 
        self.generate_video(title, sub.id, description_text_map)
    

new_scrape = Scraper('https://www.reddit.com/r/AmItheAsshole/comments/wafrdc/aita_for_saying_that_it_is_fucking_weird_that_my/')