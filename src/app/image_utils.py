import random
from openai import OpenAI
import requests
import time
from PIL import Image
from io import BytesIO
from IPython.display import display
import numpy as np
from datetime import datetime
import os
import io
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image as PILImage
import secrets 
from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app

# Template for the prompt
# prompt_template = """
#     Create an imaginative scene featuring Frostwing the Snowman, a huge, plain snowman composed of two snowballs for his body and one snowball for his head, with no legs, adorned with vibrant, colorful butterfly wings. 
#     The rest of the scene should be in the distinctive style of {artist}, with a black and white background that contrasts strikingly with Frostwing's radiant wings.
#     The background should be rich with {background_details}, providing a vivid backdrop that enhances the {theme} theme of the artwork. 
#     This artwork should also reflect the spirit of {event}.
# """
prompt_template = """
    Create an abstract artwork featuring a huge, plain snowman composed of two snowballs for his body and one snowball for his head, and no legs, 
    adorned with colorful and decorated butterfly wings. 
    The scene in the distinctive style of {}, contrasting strikingly with wings.
    The background  {}. the theme is {}. 
    This artwork should also reflect the spirit of the event: {}. The event should be clearly reflected with this scene in the background: {}.
"""




artists = [
    "Leonardo da Vinci",
    "Vincent van Gogh",
    "Pablo Picasso",
    "Claude Monet",
    "Michelangelo",
    "Rembrandt van Rijn",
    "Salvador Dalí",
    "Henri Matisse",
    "Georgia O'Keeffe",
    "Frida Kahlo",
    "Jackson Pollock",
    "Andy Warhol",
    "Gustav Klimt",
    "Edvard Munch",
    "Paul Cézanne",
    "Johannes Vermeer",
    "Édouard Manet",
    "Auguste Rodin",
    "Diego Rivera",
    "Edgar Degas"
]
themes = [
    "thanks giving",
    "christmas", 
    "halloween", 
    "birthday"
]

background_details = [
    "around fire pit",
    "in the office",
    "in the classroom",
    "in the club",
    "in home",
    "plain"
    ]

events = [
    "friendship",
    "mom",
    "parents",
    "brother",
    "sister"
    ]

activities = [
    "playing",
    "hugging",
    "greeting",
    "Serving",
    "Cycling"
]


prompt_template2 = """
Create an abstract artwork inspired by {}.
 The artwork should feature a scene of {}. {}.
   The background should include {}. This piece is set during {}.
"""

themes2 = [
    "Woman in Formula 1 Racing",
    "Woman in NASCAR",
    "Woman Driving Classic Cars",
    "Woman Driving Family Cars",
    "Woman on Road Trips",
    "Woman in Rally Racing",
    "Woman in Off-Road Adventures",
    "Woman Driving Convertibles",
    "Woman Driving Electric Cars",
    "Woman in Luxury Cars",
    "Woman in Vintage Car Shows",
    "Woman in Urban Driving",
    "Woman on Scenic Drives",
    "Woman in Drag Racing",
    "Woman in Carpooling Scenes",
    "Woman in Taxi Driver Roles",
    "Woman in Emergency Vehicles",
    "Woman in Autonomous Cars",
    "Woman Driving to Work",
    "Woman in Car Maintenance"
]


background_details2 = [
    "Race track",
    "City street",
    "Countryside",
    "Highway",
    "Garage",
    "Urban ",
    "Coastal road",
    "Suburban neighborhood",
    "Desert ",
    "Mountain road",
    "Traffic light",
    "Car show",
    "Pit stop",
    "Parking lot",
    "Roadside diner",
    "Gas station",
    "Car wash",
    "School zone",
    "Office building",
    "Forest road"
]


events2 = [
    "Grand Prix",
    "NASCAR Championship",
    "Classic Car Rally",
    "Family Road Trip",
    "Cross-Country Drive",
    "Off-Road Race",
    "Convertible Cruise",
    "Electric Car Parade",
    "Luxury Car Exhibition",
    "Vintage Car Show",
    "Urban Driving Challenge",
    "Scenic Route Tour",
    "Drag Racing Event",
    "Carpool Challenge",
    "Taxi Driver Marathon",
    "Emergency Vehicle Rally",
    "Autonomous Car Demo",
    "Daily Commute Race",
    "Car Maintenance Workshop",
    "Women in Motorsport Conference"
]


activities2 = [
    "Racing at high speed",
    "Navigating through traffic",
    "Enjoying a leisurely drive",
    "Driving kids to school",
    "Going on a road trip",
    "Competing in a rally",
    "Driving on rough terrains",
    "Cruising with the top down",
    "Charging an electric car",
    "Showing off a luxury car",
    "Participating in a vintage car parade",
    "Driving through city lights",
    "Taking a scenic route",
    "Competing in a drag race",
    "Carpooling with friends",
    "Driving a taxi",
    "Responding to emergencies",
    "Testing autonomous driving",
    "Driving to the office",
    "Tuning up a car"
]


def generate_description(artist, event) : 
    
    title = f"{event} Inspired Candle by {artist}. Natural Scented Coconut Apricot Candle Gift for Him. Unique Candle Gift for Her. "
    
    description = f""" 
        🎨 Inspired by {artist}'s works & the spirit of {event}.\n
        🎁✨ Surprise mom, a special friend, or loved one with our magical Scented Coconut Apricot Candle! ✨🎁\n
        🌟 **INFO**:\n
        - 🌿 Materials: Coconut apricot wax, cotton wick\n
        - 🥇 Lid: Gold\n
        - 🏺 Vessel: Amber & clear\n
        - ⏳ Burn time: Up to 20 hours (4oz), up to 50 hours (9oz)\n
        - 🚫 All scents: Natural color\n
        - ✅ ASTM safety standards\n
        - 🇺🇸 Assembled in the USA\n
        🕯️ **CARE TIPS**:\n
        - 🔥 First burn: Melt to edges\n
        - ✂️ Trim wick: 1/4" before each burn\n
        - ⏱️ Burn: 2-3 hours max\n
        - 🚫 Never leave unattended, avoid drafts & flammable items\n
        🌍 **FEATURES**:\n
        - 🌱 Eco-friendly & non-toxic\n
        - 🏡 Hand-poured in the USA\n
        - 🚫 No lead, plastics, parabens, synthetic dyes, or phthalates\n
        🕒 **BURN TIME**:\n
        - Up to 20 hours of aromatic bliss\n
        🌸 **SCENTS**:\n
        - 🍇 **Midnight Blackberry**: Lime, orange, blackberry, raspberry, champagne, sugar, praline, pine\n
        - 🌿 **Lavender**: Citrus, bergamot, camphor, eucalyptus, cedar\n
        - 🌲 **Fraser Fir**: Cypress, lemon peel, evergreen, cedar, fir, amber, moss\n
        - ☕ **Cinnamon Chai**: Orange peel, black tea, nutmeg, peppercorn, vanilla, clove, cinnamon\n
        - 🌼 **Cashmere Musk**: Bergamot, saffron, violets, lily of the valley, dark musk, vetiver\n
        - 🌊 **Beachwood**: Sea salt, orange peel, grass, eucalyptus, sage, teakwood, patchouli\n
        - 🥭 **Mango Coconut**: Orange, pineapple, peach, mango, sugar, coconut milk\n
        - 🔅 **Unscented**: Fragrance-free illumination\n
        - 🍰 **Vanilla Bean**: Buttercream, sugary cake, vanilla, bourbon\n
        📏 **SIZE**:\n
        *IMPERIAL*\n
        - 4oz: Diameter 2.30", Height 2.50"\n
        - 9oz: Diameter 2.80", Height 3.50"\n
        *METRIC*\n
        - 4oz: Diameter 5.84cm, Height 6.35cm\n
        - 9oz: Diameter 7.11cm, Height 8.89cm\n
        🕯️✨ Enjoy a magical, eco-friendly candle experience! ✨🕯️
        """

    
    
    tags_prompt = f"Create a python list of 13 comma-separated 20-letters-max letters-only tags for an Etsy product whose title is: {title} and description is: {description}.\
      tags has to be human readable with trendy relevant keywords. Do not include quotes. Do not make the tags too general, instead make them too specific to the product. put a space between every two words."
    tags = generate_txt(tags_prompt)
    
    return title + "\n" + description + "\njtagsj\n" + tags


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


def generate_gallery_images_and_descriptions(image_folder, num_images = 20) : 

    print("Generating images")
    trials = 10 
    images = 0 
    i = 0

    while images < num_images and trials > 0 : 
        try : 
                
            artist = random.choice(artists)
            idx = random.randint(0, len(artists) - 1)
            background_detail = background_details[idx]
            theme = themes[idx]
            event = events[idx]
            activity = activities[idx]
            prompt = prompt_template.format(artist, background_detail, theme, event, activity)
            
            image_number = str(i).zfill(3)
            for image_name in os.listdir(image_folder) :
                if not image_name.endswith('.png') :
                    continue 
                if image_name.startswith(image_number) :
                    i += 1
                    image_number = str(i).zfill(3)
                    continue 
                
            image_path = os.path.join(image_folder, image_number + '_' + artist + '_' + event + '.png')
            generate_image(prompt = prompt, save = image_path) 
            print(f"Generated image: {image_path}")
            # sleep for 2 second
            time.sleep(5)

            description = generate_description(artist, event) 
            with open(os.path.join(image_folder, image_number +'.txt'), 'w') as f :
                f.write(description)

        except Exception as e  : 
            print(e)
            trials -= 1

        images += 1
        i += 1


def generate_image(prompt, style = 'vivid', save = True) :
    client = OpenAI()
    res = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    n=1,
    style = style, # can be 'vivid' or 'natural'
    quality = 'hd',
    size="1024x1024"
    )
    url = res.data[0].url

    data = requests.get(url).content

    if save :
        # Opening a new file named img with extension .png
        # This file would store the data of the image file
        # imagename = str(time.localtime().tm_min) + "_" + str(time.localtime().tm_sec)
        f = open(f'{save}','wb')

        # Storing the image data inside the data variable to the file
        f.write(data)
        f.close()
    else :
        image = Image.open(BytesIO(data))
        display(image)


def save_picture(username, form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = 'profile_image' + f_ext
    picture_folder = os.path.join(current_app.root_path, 'static', 'users', username, 'images')
    picture_path = os.path.join(picture_folder, picture_fn)


    try : 
        os.makedirs(picture_folder)
    except Exception as e:
        print(e)

    output_size = (125, 125)
    i = PILImage.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def edit_image(image, prompt, save = True) : 

    print("Editing image")
    print("image:", image) 
    print("dst:", save) 
    if isinstance(image, str) : 
        image = open(image, "rb")
    else :
        image = image

    client = OpenAI()
    mask_array = np.ones((1024, 1024), dtype=np.uint8) * 255  # Assuming mask is white

    # Convert the NumPy array to an image and save to a buffer
    mask_image = Image.fromarray(mask_array)
    mask_buffer = io.BytesIO()
    mask_image.save(mask_buffer, format="PNG")
    mask_buffer.seek(0)
    res = client.images.edit(
    image= image, 
    mask= mask_buffer,
    prompt= prompt, 
    n=1,
    size="1024x1024"
    )

    url = res.data[0].url

    data = requests.get(url).content


    if save :
        # Opening a new file named img with extension .png
        # This file would store the data of the image file
        
        f = open(f'{save}','wb')

        # Storing the image data inside the data variable to the file
        f.write(data)
        f.close()
    else :
        image = Image.open(BytesIO(data))
        display(image)



# def check_and_generate_images(base_folder):
#     current_date = datetime.now().strftime("%b_%d")
#     current_folder_path = os.path.join(base_folder, current_date)
    
#     # Check if the folder for the current date exists
#     if not os.path.exists(current_folder_path):
#         # Create the folder
#         os.makedirs(current_folder_path)
#         print(f"Created folder: {current_folder_path}")
        
#         # Generate 9 images
#         for i in range(1, 10):
#             prompt = random.choice(prompts)
#             generate_image(prompt = prompt, save = current_folder_path)
#             print(f"Generated image: {image_path}")
#     else:
#         print(f"Folder {current_folder_path} already exists. No new images generated.")



if __name__ == "__main__":
    generate_gallery_images_and_descriptions("newsimages")