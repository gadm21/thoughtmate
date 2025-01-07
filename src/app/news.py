
from pygooglenews import GoogleNews
import openai
from openai import OpenAI
import os 
import matplotlib.pyplot as plt
import requests

from PIL import Image
from io import BytesIO
from IPython.display import display


def generate_txt(prompt) :
  client = OpenAI()
  completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": prompt}
    ]
  )

  return completion.choices[0].message.content



def display_image(images, size= (10, 5)):
    # Check if images is a list of image paths or a single image path
    if isinstance(images, list):
        # Initialize a plot with 1 row and as many columns as there are images
        fig, axs = plt.subplots(1, len(images), figsize = size)
        for i, img_path in enumerate(images):
            # Open the image
            if isinstance(img_path, str) : 
              img = Image.open(img_path)
            else : 
              img = img_path 

            # Display the image
            if len(images) > 1:
                axs[i].imshow(img)
                axs[i].axis('off')  # Turn off axis numbers and ticks
            else:
                axs.imshow(img)
                axs.axis('off')
    else:
        # Open the image
        if isinstance(images, str) : 
          img = Image.open(images)
        else : 
          img = images 

        # Display the image
        plt.figure(figsize=size)
        plt.imshow(img)
        plt.axis('off')  # Turn off axis numbers and ticks
    
    # Show the plot
    plt.show()

def generate_image(prompt, style = 'vivid', save = True) :
    client = OpenAI()
    res = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        style = style,
        quality = 'hd',
        size="1024x1024"
    )
    url = res.data[0].url

    data = requests.get(url).content

    if save :
        # Opening a new file named img with extension .png
        # This file would store the data of the image file
        with open(f'newsimages/{prompt[-10:]}.png','wb') as f : 

            # Storing the image data inside the data variable to the file
            f.write(data)

    image = Image.open(BytesIO(data))
    return image


def generate_image_from_news(title) : 
    txt_prompt = """
  Please take the following news headline and rephrase it to be politically correct and neutral, avoiding any sensitive or controversial language. The rephrased headline should be clear, concise, and suitable for use in public merchandise. Here is the headline:
  """ + title 
    prompt = generate_txt(txt_prompt) 
    image_prompt = """
  Based on the following politically correct and neutral news headline, create a visually appealing and artistic design that would look great on a t-shirt. The design should capture the essence of the headline in a creative and engaging way. Here is the headline:
  """ + prompt
    image = generate_image(image_prompt, save = True)
    return image 


def get_titles(keyword = None, country = 'USA') :
    gn = GoogleNews(country = country)
    
    if keyword : 
        items = gn.search(keyword)['entries']
    else : 
        items = gn.top_news()['entries']
    stories = []
    for item in items :

        story = {
            'title' : item.title,
            'link': item.link
        }
        stories.append(story)
    return stories



os.environ['OPENAI_API_KEY'] = ''
openai.api_key = os.environ["OPENAI_API_KEY"]
project_id = ''
organization_id = ''

client = OpenAI(
  organization=organization_id,
  project= project_id,
)

topn = get_titles()

for i in range(5) : 
  title = topn[i]['title']
  image = generate_image_from_news(title)
  display_image(image)