import os
from redditScraper import Scraper
import openai
# improt Scraper

openai.api_key = ""


def gpt_3(story):
    # response = openai.Completion.create(
    #     model="text-davinci-002",
    #     prompt=story,
    #     temperature=0.7,
    #     max_tokens=1000,
    #     top_p=1,
    #     frequency_penalty=0,
    #     presence_penalty=0
    # )
    response ={
        "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": None,
      "text": "My husband cheated on me with my sister and got her pregnant. He then decided to leave me for her. I found out about the affair and the pregnancy when my sister came to me in tears, confessing everything. I was devastated.\n\nI confronted my husband and he admitted that he had been seeing my sister behind my back for months. He said that he was in love with her and was going to leave me for her. I was heartbroken.\n\nI had no idea what to do. I considered leaving him, but I didn't want to ruin my sister's life. I decided to stay with him and try to make things work.\n\nA few months later, my sister came to me and told me that she was going to keep the baby. She said that she wanted to raise it with my husband. I was shocked.\n\nI confronted my husband again and he told me that he was in love with my sister and that he was going to leave me for her. I was devastated.\n\nI had no idea what to do. I considered leaving him, but I didn't want to ruin my sister's life. I decided to stay with him and try to make things work.\n\nA few months later, my sister came to me and told me that she was going to keep the baby. She said that she wanted to raise it with my husband. I was shocked.\n\nI confronted my husband again and he told me that he was in love with my sister and that he was going to leave me for her. I was devastated.\n\nI had no idea what to do. I considered leaving him, but I didn't want to ruin my sister's life. I decided to stay with him and try to make things work.\n\nA few months later, my sister gave birth to a beautiful baby girl. My husband and I were both there for her, supporting her through everything.\n\nA few weeks after the birth, my husband came to me and told me that he was leaving me for my sister. I was heartbroken, but I knew that I couldn't stop him.\n\nI wished them both the best and I decided to move on with my life.\n\nA few months later, I received a call from my sister. She was in tears and she told me that she was sorry for everything that had happened. She said that she didn't want to raise the baby with my husband, she wanted me to do it.\n\nI was shocked. I didn't know what to say. I told her that I would raise the baby as my own and that I would always love her.\n\nA few weeks later, my husband came to me and told me that he was sorry for everything that had happened. He said that he wanted to try and work things out with me.\n\nI was surprised, but I agreed. We started to work on our relationship and things were slowly getting better.\n\nA few months later, my sister came to me and told me that she was moving away. She said that she wanted to start fresh and that she needed to get away from my husband.\n\nI was sad to see her go, but I knew that it was for the best.\n\nA few years later, my husband and I are still together and we have a beautiful baby girl. We are happy and we have forgiven each other for what happened."
    }
  ],
  "created": 1666646541,
  "id": "cmpl-64zBlHek4ZomJPXqpMYotqr7Z6Lil",
  "model": "text-davinci-002",
  "object": "text_completion",
  "usage": {
    "completion_tokens": 701,
    "prompt_tokens": 61,
    "total_tokens": 762
  }
}
    return response


if __name__ == "__main__":
    story = input("Enter a story\n")
    res = gpt_3(story)
    # print(res)
    # print('res: ', res['choices'][0]['text'])
    x = Scraper(res['choices'][0]['text'].replace('\n',' ').split(' '), False, "some generated title")
    # app.run()








