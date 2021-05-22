# import config
import openai
import ipywidgets as widgets
from IPython.display import display
import gtts
import multiprocessing
from playsound import playsound
import os
with open("config.txt",'r') as f:
    key=f.readlines()

openai.api_key = key[1]

class text2s:
    def __init__(self,text):
        self.text=text
        self.p = multiprocessing.Process(target=playsound, args=("hello.mp3",))
    def get_audio(self):
        # make request to google to get synthesis
        tts = gtts.gTTS(self.text)
        # save the audio file
        tts.save("hello.mp3")
        self.p = multiprocessing.Process(target=playsound, args=("hello.mp3",))
    def play_audio(self):
        self.p.start()
    def stop_audio(self):
        self.p.terminate()
    

def getResponse():


    myEntry = f"""Topic:{Topic.value}."""
    #Custom text input
    myPrompt = f"""Generates a poem on a given Topic. 

    Topic:Friendship.
    The friendship we have is so rare to find.
    We hate to see each other in a bind.
    We have made each other laugh so hard we've cried.
    We feel each other's pain if we are hurt inside.
    We always can find the right words to say
    To help us get through any dreadful day.
    We have told our darkest secrets with feeling no shame,
    We will tell each other the truth, even if we are to blame.
    Thinking of you not being here makes me feel so sad.
    We will have to look back on our crazy memories to make us glad.
    The miles between us can't keep us apart,
    Because we will keep each other close at heart.


    Topic:Love
    Love is in your heart,
    Love is in your mind.
    Love doesn't discriminate,
    Love is always blind.
    Love's the greatest power,
    And yet it is so small.
    Love's a gift from God
    To be shared amongst us all.
    Love is universal,
    It encompasses the globe.
    No matter where you are,
    Love has a language all its own.


    Topic:lover.
    Sometimes I wonder what my world would be like
    If I didn't have someone like you in my life.
    I come back to reality only to see
    That I wouldn't be myself without you and me.
    I am looking forward to the future, hoping you'll be with me,
    Growing old together and being happy as can be.


    {myEntry}
    """

    #parameters
    myTokens = 250 # max length
    myEngine = "davinci"
    myTemp = 0.87 # creativity
    myTop_p = 1 
    myN=1
    myStream = None
    myLogProbs = None
    myStop = "\n\n"

    response = openai.Completion.create(
      engine=myEngine,
      prompt=myPrompt,
      max_tokens=myTokens,
      temperature=myTemp,
      top_p=myTop_p,
      n=myN,
      stream = myStream,
      logprobs=myLogProbs,
      stop = myStop
    )

    response=f"{myEntry}\n{response.choices[0].text}"
    historyText.value=response
    try:
        tts=text2s(response)
        tts.get_audio()
        tts.play_audio()
    except Exception as e:
        print(f"-->{e}")
    with open('gpt3Poem.txt', 'a') as f:
        f.writelines("\n\n"+response)

def submitButton(btn_object):
    try:
        os.remove("./hello.mp3")
    except Exception as e:
        print(e)
    getResponse()


layout = widgets.Layout(width='auto', height='auto')
Topic = widgets.Text(value="", disabled=False,description='Topic')

historyText = widgets.Textarea(
value="",
placeholder="No history yet.",
description='gpt3 output',
disabled=True,
layout=layout
)

submit = widgets.Button(
    description='Send',
    disabled=False,
    button_style='success', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Send message',
    icon='meh-blank' # (FontAwesome names without the `fa-` prefix)
)

submit.on_click(submitButton)

display(Topic,historyText,submit)