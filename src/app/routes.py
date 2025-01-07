from app import db, bcrypt
from flask import g, Blueprint, render_template, url_for, flash, redirect, request, current_app
from app.forms import RegistrationForm, LoginForm
from app.models import User, Image
from flask_login import login_user, current_user, logout_user, login_required
from flask import jsonify

import os
import shutil
import requests
import os
import stripe
from werkzeug.utils import secure_filename
from PIL import Image as PILImage
import secrets
from math import ceil
from datetime import datetime
import random 
import time 

from image_utils import generate_txt, edit_image, generate_image, generate_gallery_images_and_descriptions, save_picture, generate_description
from image_utils import prompt_template, artists, background_details, themes, events, activities
from image_utils import prompt_template2, background_details2, themes2, events2, activities2
from print_utils import submit_product
from do_it import post_on_facebook
import app.globals as globals

main = Blueprint('main', __name__)




@main.route('/get_product_info', methods=['POST'])
def get_product_info():
    data = request.get_json()
    image_name = data['image']
    image_number = image_name.split('_')[0]
    design_name = os.path.splitext(image_name)[0]
    current_date = datetime.now().strftime("%m_%d")

    print("design_name:", design_name) 
    print("current_date:", current_date)

    try:
        with open(f'{current_app.static_folder}/images/display/{current_date}/{image_number}.txt', 'r') as file:
            lines = file.readlines()
            title = lines[0].strip()
            description = " ".join(line.strip() for line in lines[1:])
            # tags_prompt = f"put the following tags in comma separated format: {description.split('jtagsj')[1]}"
            # tags = generate_txt(tags_prompt) 
            # print("title:", title) 
            # print("description:", description) 
            print("successeded  ")
            return jsonify({'success': True, 'title': title, 'description': description})
    except Exception as e:
        print("failed")
        return jsonify({'success': False, 'error': str(e)})


@main.route('/love_image', methods=['POST'])
@login_required
def love_image():
    data = request.get_json()
    image_name = data['image']
    
    # Here you should implement the logic to update the "loved" counter
    # For demonstration purposes, we'll assume it's successful
    success = True
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Could not update loved counter'}), 500


@main.route('/print_image', methods=['POST'])
@login_required
def print_image():
    title = request.form.get('title')
    description = request.form.get('description')
    product = request.form.get('product')
    colors = request.form.getlist('colors')

    image_name = request.form.get('imagePath')
    current_date = datetime.now().strftime("%m_%d")
    image_path = os.path.join(current_app.static_folder, 'images', 'display', current_date, image_name)
    
    
    success, msg = submit_product(product, title, description, colors, image_path) 
    
    
    if success:
        post_on_facebook(post = f"Check out this amazing design! {title}", file_paths = [image_path])
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'error': msg}), 500


@main.route("/")
@main.route("/home")
def home():
    current_date = datetime.now().strftime("%m_%d")

    page = request.args.get('page', 1, type=int)
    per_page = 12
    if current_user.is_authenticated:
        image_folder = os.path.join(current_app.static_folder, 'images', 'display', current_date)
        if not os.path.exists(image_folder):
            os.makedirs(image_folder) 
        images = [image for image in os.listdir(image_folder) if image.endswith('.png')]
        total_images = len(images)
        if total_images < 10 :
            if not globals.IamCreatingImagesNow: 
                globals.IamCreatingImagesNow = True
                generate_gallery_images_and_descriptions(image_folder, 10) 
                globals.IamCreatingImagesNow = False
            else : 
                print("Images are being created now. Please wait for a few seconds and refresh the page")
            

        total_pages = ceil(total_images / per_page)
        paginated_images = images[(page - 1) * per_page:page * per_page]
        pagination = {
            'total_pages': total_pages,
            'current_page': page
        }
        return render_template('home.html', images=paginated_images, pagination=pagination, title='Home', current_date=current_date)
    else:
        return render_template('home.html', title = 'Home')
    

@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.username.data, form.picture.data)
        else:
            picture_file = os.path.join(current_app.static_folder, 'users', 'default_profile_image.jpg')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, image_file=picture_file)
        db.session.add(user)
        db.session.commit()

        
        print('your account has been created') 
        flash('Your account has been created!', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', title='Register', form=form)


@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route("/profile")
@login_required
def profile():
    return render_template('profile.html', title='Profile')

@main.route("/history")
@login_required
def history():
    images = Image.query.filter_by(author=current_user).order_by(Image.date_posted.desc()).all()
    return render_template('history.html', title='History', images=images)

@main.route("/privacy_policy")
def privacy_policy():
    return render_template('privacy_policy.html', title='Privacy Policy')

@main.route("/contact_us")
def contact_us():
    return render_template('contact_us.html', title='Contact Us')

@main.route("/buy_credits", methods=['POST'])
@login_required
def buy_credits():
    stripe.api_key = current_app.config['STRIPE_API_KEY']
    try:
        charge = stripe.Charge.create(
            amount=1000,
            currency='usd',
            description='Buy Credits',
            source=request.form['stripeToken']
        )
        current_user.credits += 10
        db.session.commit()
        flash('Credits purchased successfully!', 'success')
    except stripe.error.StripeError:
        flash('Something went wrong. Please try again.', 'danger')
    return redirect(url_for('main.profile'))

@main.route("/studio", methods=['GET', 'POST'])
@login_required
def studio():
    current_date = datetime.now().strftime("%m_%d")
    gallery_images = os.listdir(os.path.join(current_app.root_path, 'static', 'images', 'display', current_date))
    return render_template('studio.html', title='Studio', gallery_images=gallery_images)

@main.route("/studio_blend", methods=['POST'])
@login_required
def studio_blend():
    image1 = request.files['image1']
    image2 = request.files['image2']

    if image1 and image2:
        filename1 = secure_filename(image1.filename)
        filename2 = secure_filename(image2.filename)
        image_path1 = os.path.join(current_app.root_path, 'static/uploads', filename1)
        image_path2 = os.path.join(current_app.root_path, 'static/uploads', filename2)
        image1.save(image_path1)
        image2.save(image_path2)

        blended_image = blend_images(image_path1, image_path2)
        blended_image_filename = f"blended_{filename1}_{filename2}.jpg"
        blended_image_path = os.path.join(current_app.root_path, 'static/blended', blended_image_filename)
        blended_image.save(blended_image_path)

        gallery_images = os.listdir(os.path.join(current_app.root_path, 'static/gallery'))
        return render_template('studio.html', title='Studio', gallery_images=gallery_images, blended_image=blended_image_filename)

    flash('Please upload both images.', 'danger')
    return redirect(url_for('main.studio'))

@main.route("/studio_upload_and_blend", methods=['POST'])
@login_required
def studio_upload_and_blend():
    gallery_image = request.form['gallery_image']
    upload_image = request.files['upload_image']

    if gallery_image and upload_image:
        filename1 = gallery_image
        filename2 = secure_filename(upload_image.filename)
        image_path1 = os.path.join(current_app.root_path, 'static/gallery', filename1)
        image_path2 = os.path.join(current_app.root_path, 'static/uploads', filename2)
        upload_image.save(image_path2)

        blended_image = blend_images(image_path1, image_path2)
        blended_image_filename = f"blended_{filename1}_{filename2}.jpg"
        blended_image_path = os.path.join(current_app.root_path, 'static/blended', blended_image_filename)
        blended_image.save(blended_image_path)

        gallery_images = os.listdir(os.path.join(current_app.root_path, 'static/gallery'))
        return render_template('studio.html', title='Studio', gallery_images=gallery_images, blended_image=blended_image_filename)

    flash('Please select a gallery image and upload an image.', 'danger')
    return redirect(url_for('main.studio'))

def blend_images(image_path1, image_path2):
    image1 = PILImage.open(image_path1)
    image2 = PILImage.open(image_path2)

    # Resize images to the same size
    image1 = image1.resize((500, 500))  # You can adjust the size as needed
    image2 = image2.resize((500, 500))  # Ensure both images are the same size

    blended_image = PILImage.blend(image1, image2, alpha=0.5)
    return blended_image

@main.route('/replace_image', methods=['POST'])
@login_required
def replace_image():
    data = request.get_json()

    current_date = datetime.now().strftime("%m_%d")
    image_name = data['image']
    image_number = image_name.split('_')[0]
    image_folder = os.path.join(current_app.static_folder, 'images', 'display', current_date)
    image_path = os.path.join(image_folder, image_name) 
    
    if os.path.exists(image_path):
        artist = random.choice(artists)
        idx = random.randint(0, len(background_details2) - 1)
        background_detail = background_details2[idx]
        theme = themes2[idx]
        event = events2[idx]
        activity = activities2[idx]
        prompt = prompt_template2.format(artist, background_detail, theme, event, activity)

        new_image_name = image_number + '_' + artist + '_' + event + '.png'
        new_image_path = os.path.join(image_folder, new_image_name)
        generate_image(prompt = prompt, save = new_image_path) 
        print(f"Generated image: {new_image_path}")
        

        description = generate_description(artist, event) 
        with open(os.path.join(image_folder, image_number +'.txt'), 'w') as f :
            f.write(description)

        # delete the old image
        os.remove(image_path)

        return jsonify({'success': True, 'new_image_url': new_image_path})
    else:
        print(f"Image {image_path} not found")
        return jsonify({'success': False, 'error': 'Image not found'}), 404