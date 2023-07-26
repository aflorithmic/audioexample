import audiostack

audiostack.api_base = "https://v2.api.audio"
audiostack.api_key = "APIKEY" # fill up

script = """
<as:section name="intro" soundsegment="intro">
Make some custom templates with audiostack S.D.K.!. Now that I've introduced the topic lets move on to another section!</as:section>
 <as:section name="main" soundsegment="main">
On this test we show you how to use custom music to generate templates.
You can add several segments an associate them to script sections. 
Lets skip to the outro!
 </as:section>
 <as:section name="outro" soundsegment="outro">
 And so we are now in the outro and its time to say Goood bye good bye
 </as:section>
"""


# CREATING CUSTOM TEMPLATE

# 1. Create an empty template

try:
    template = audiostack.Production.Sound.Template.create(templateName="sound_templates_demo") 
except Exception as e:
    response = audiostack.Production.Sound.Template.delete(templateName="sound_templates_demo")
    raise ValueError("template already existed so we cleared it for you, just re-run the demo")

# 2. Paths to our template segments / This segments can be 
segments =[
    {
        "name": "intro",
        "path": "demo_segments/br_intro.wav"
    },
    {
        "name": "main",
        "path": "demo_segments/br_main.wav"
    },
    {
        "name": "outro",
        "path": "demo_segments/br_outro.wav"
    }
]

# # 3. Upload each segment of our template to audiostack media storage and assign it to the template previously created
for segment in segments:

    # add to media storage
    response = audiostack.Content.Media.create(segment["path"])                
    media_id =response.data.get('mediaId')    

    # assign to our template
    response = audiostack.Production.Sound.Segment.create(             
        templateName="sound_templates_demo", soundSegmentName=segment["name"], mediaId=media_id
    ) 

# 4. Template created! Now lets make use of it:
script = audiostack.Content.Script.create(scriptText=script, scriptName="demo", projectName="demo")        
speech = audiostack.Speech.TTS.create(
        scriptItem=script,
        voice="wren",
        speed=1,
)
mix = audiostack.Production.Mix.create(
    speechId=speech.speechId,
    soundTemplate="sound_templates_demo",
    masteringPreset="balanced",
)
encoded = audiostack.Delivery.Encoder.encode_mix(
    productionItem=mix,
    preset='wav',
    loudnessPreset = 'spotify'
)
encoded.download(fileName=f"demo_sound_templates")
print("Downloaded -> ", encoded.data)

# AUTOMATIC TAGGING PARAMETERS AND LISTING

# Once our template is created our automatic tagging engine will trigger and analyze the template.
# List some of the parameters of the auto-tagger:

response = audiostack.Production.Sound.Parameter.get()
parameters = response.data.get("parameters")
for k, v in parameters.items():
    print(f"\n* Parameter: {k}\n{v}")

# Use this parameters filter available templates. Lets try using mood:
response = audiostack.Production.Sound.Template.list(instruments="synth")
templates = response.data.get("templates")
print(f"{len(templates)} matching templates found!! Try them out!")
for i, tmplt in enumerate(templates):
    print(f"{i} - {tmplt.get('alias')}")


# Lets delete our demo template
response = audiostack.Production.Sound.Template.delete(templateName="sound_templates_demo")






