
from PIL import Image
import base64
import io
import os
import requests
from datetime import datetime
from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app

import app.globals as globals

supported_products = ['t-shirt', 'candle']
printify_key = ''

base_url = "https://api.printify.com/v1"
product_url = "https://api.printify.com/v1/catalog/blueprints/{}/print_providers/{}/variants.json"
shop_url = "{}/shops/{}/products.json"


shop_id = 16063870
#[{'id': 15747140, 'title': 'rock and balloon', 'sales_channel': 'shopify'}, {'id': 16063870, 'title': 'My Etsy Store', 'sales_channel': 'etsy'}]


products = {
    't-shirt' : {
        'colors' : ['White', 'Black', 'Red', 'Blue', 'Green'],
        'sizes' : ['S', 'M', 'L', 'XL', '2XL'], 
        'design_sizes' : [(3761, 3319), (4431, 3909), (5100, 4500), (5100, 4500), (5100, 4500), (750, 750)],  # S (front, back), M (front, back) L (front, back), neck
        'positions': ['front', 'neck'], 
        'prices' : [2399, 2499, 2799, 2899, 2999],
        'print_provider_id': 29, 
        'blueprint_id': 12, 
        'variants': [
{'id': 18052, 'title': 'Aqua / S', 'options': {'color': 'Aqua', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18053, 'title': 'Aqua / M', 'options': {'color': 'Aqua', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18054, 'title': 'Aqua / L', 'options': {'color': 'Aqua', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18055, 'title': 'Aqua / XL', 'options': {'color': 'Aqua', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18056, 'title': 'Aqua / 2XL', 'options': {'color': 'Aqua', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18057, 'title': 'Aqua / 3XL', 'options': {'color': 'Aqua', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18060, 'title': 'Army / S', 'options': {'color': 'Army', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18061, 'title': 'Army / M', 'options': {'color': 'Army', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18062, 'title': 'Army / L', 'options': {'color': 'Army', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18063, 'title': 'Army / XL', 'options': {'color': 'Army', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18064, 'title': 'Army / 2XL', 'options': {'color': 'Army', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18065, 'title': 'Army / 3XL', 'options': {'color': 'Army', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18068, 'title': 'Asphalt / S', 'options': {'color': 'Asphalt', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18069, 'title': 'Asphalt / M', 'options': {'color': 'Asphalt', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18070, 'title': 'Asphalt / L', 'options': {'color': 'Asphalt', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18071, 'title': 'Asphalt / XL', 'options': {'color': 'Asphalt', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18072, 'title': 'Asphalt / 2XL', 'options': {'color': 'Asphalt', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18073, 'title': 'Asphalt / 3XL', 'options': {'color': 'Asphalt', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18076, 'title': 'Athletic Heather / S', 'options': {'color': 'Athletic Heather', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18077, 'title': 'Athletic Heather / M', 'options': {'color': 'Athletic Heather', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18078, 'title': 'Athletic Heather / L', 'options': {'color': 'Athletic Heather', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18079, 'title': 'Athletic Heather / XL', 'options': {'color': 'Athletic Heather', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18080, 'title': 'Athletic Heather / 2XL', 'options': {'color': 'Athletic Heather', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18081, 'title': 'Athletic Heather / 3XL', 'options': {'color': 'Athletic Heather', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18084, 'title': 'Baby Blue / S', 'options': {'color': 'Baby Blue', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18085, 'title': 'Baby Blue / M', 'options': {'color': 'Baby Blue', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18086, 'title': 'Baby Blue / L', 'options': {'color': 'Baby Blue', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18087, 'title': 'Baby Blue / XL', 'options': {'color': 'Baby Blue', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18088, 'title': 'Baby Blue / 2XL', 'options': {'color': 'Baby Blue', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18089, 'title': 'Baby Blue / 3XL', 'options': {'color': 'Baby Blue', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18092, 'title': 'Berry / S', 'options': {'color': 'Berry', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18093, 'title': 'Berry / M', 'options': {'color': 'Berry', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18094, 'title': 'Berry / L', 'options': {'color': 'Berry', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18095, 'title': 'Berry / XL', 'options': {'color': 'Berry', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18096, 'title': 'Berry / 2XL', 'options': {'color': 'Berry', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18097, 'title': 'Berry / 3XL', 'options': {'color': 'Berry', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18100, 'title': 'Black / S', 'options': {'color': 'Black', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18101, 'title': 'Black / M', 'options': {'color': 'Black', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18102, 'title': 'Black / L', 'options': {'color': 'Black', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18103, 'title': 'Black / XL', 'options': {'color': 'Black', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18104, 'title': 'Black / 2XL', 'options': {'color': 'Black', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18105, 'title': 'Black / 3XL', 'options': {'color': 'Black', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18124, 'title': 'Cardinal / S', 'options': {'color': 'Cardinal', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18125, 'title': 'Cardinal / M', 'options': {'color': 'Cardinal', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18126, 'title': 'Cardinal / L', 'options': {'color': 'Cardinal', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18127, 'title': 'Cardinal / XL', 'options': {'color': 'Cardinal', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18128, 'title': 'Cardinal / 2XL', 'options': {'color': 'Cardinal', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18129, 'title': 'Cardinal / 3XL', 'options': {'color': 'Cardinal', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18140, 'title': 'Dark Grey / S', 'options': {'color': 'Dark Grey', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18141, 'title': 'Dark Grey / M', 'options': {'color': 'Dark Grey', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18142, 'title': 'Dark Grey / L', 'options': {'color': 'Dark Grey', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18143, 'title': 'Dark Grey / XL', 'options': {'color': 'Dark Grey', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18144, 'title': 'Dark Grey / 2XL', 'options': {'color': 'Dark Grey', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18145, 'title': 'Dark Grey / 3XL', 'options': {'color': 'Dark Grey', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18148, 'title': 'Dark Grey Heather / S', 'options': {'color': 'Dark Grey Heather', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18149, 'title': 'Dark Grey Heather / M', 'options': {'color': 'Dark Grey Heather', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18150, 'title': 'Dark Grey Heather / L', 'options': {'color': 'Dark Grey Heather', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18151, 'title': 'Dark Grey Heather / XL', 'options': {'color': 'Dark Grey Heather', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18152, 'title': 'Dark Grey Heather / 2XL', 'options': {'color': 'Dark Grey Heather', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18153, 'title': 'Dark Grey Heather / 3XL', 'options': {'color': 'Dark Grey Heather', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18156, 'title': 'Deep Heather / S', 'options': {'color': 'Deep Heather', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18157, 'title': 'Deep Heather / M', 'options': {'color': 'Deep Heather', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18158, 'title': 'Deep Heather / L', 'options': {'color': 'Deep Heather', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18159, 'title': 'Deep Heather / XL', 'options': {'color': 'Deep Heather', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18160, 'title': 'Deep Heather / 2XL', 'options': {'color': 'Deep Heather', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18161, 'title': 'Deep Heather / 3XL', 'options': {'color': 'Deep Heather', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18180, 'title': 'Forest / S', 'options': {'color': 'Forest', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18181, 'title': 'Forest / M', 'options': {'color': 'Forest', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18182, 'title': 'Forest / L', 'options': {'color': 'Forest', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18183, 'title': 'Forest / XL', 'options': {'color': 'Forest', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18184, 'title': 'Forest / 2XL', 'options': {'color': 'Forest', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18185, 'title': 'Forest / 3XL', 'options': {'color': 'Forest', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18188, 'title': 'Gold / S', 'options': {'color': 'Gold', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18189, 'title': 'Gold / M', 'options': {'color': 'Gold', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18190, 'title': 'Gold / L', 'options': {'color': 'Gold', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18191, 'title': 'Gold / XL', 'options': {'color': 'Gold', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18192, 'title': 'Gold / 2XL', 'options': {'color': 'Gold', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18193, 'title': 'Gold / 3XL', 'options': {'color': 'Gold', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18236, 'title': 'Heather Green / S', 'options': {'color': 'Heather Green', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18237, 'title': 'Heather Green / M', 'options': {'color': 'Heather Green', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18238, 'title': 'Heather Green / L', 'options': {'color': 'Heather Green', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18239, 'title': 'Heather Green / XL', 'options': {'color': 'Heather Green', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18240, 'title': 'Heather Green / 2XL', 'options': {'color': 'Heather Green', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18241, 'title': 'Heather Green / 3XL', 'options': {'color': 'Heather Green', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18244, 'title': 'Heather Kelly / S', 'options': {'color': 'Heather Kelly', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18245, 'title': 'Heather Kelly / M', 'options': {'color': 'Heather Kelly', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18246, 'title': 'Heather Kelly / L', 'options': {'color': 'Heather Kelly', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18247, 'title': 'Heather Kelly / XL', 'options': {'color': 'Heather Kelly', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18248, 'title': 'Heather Kelly / 2XL', 'options': {'color': 'Heather Kelly', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18249, 'title': 'Heather Kelly / 3XL', 'options': {'color': 'Heather Kelly', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18260, 'title': 'Heather Mint / S', 'options': {'color': 'Heather Mint', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18261, 'title': 'Heather Mint / M', 'options': {'color': 'Heather Mint', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18262, 'title': 'Heather Mint / L', 'options': {'color': 'Heather Mint', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18263, 'title': 'Heather Mint / XL', 'options': {'color': 'Heather Mint', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18264, 'title': 'Heather Mint / 2XL', 'options': {'color': 'Heather Mint', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18265, 'title': 'Heather Mint / 3XL', 'options': {'color': 'Heather Mint', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18268, 'title': 'Heather Navy / S', 'options': {'color': 'Heather Navy', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18269, 'title': 'Heather Navy / M', 'options': {'color': 'Heather Navy', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18270, 'title': 'Heather Navy / L', 'options': {'color': 'Heather Navy', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18271, 'title': 'Heather Navy / XL', 'options': {'color': 'Heather Navy', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18272, 'title': 'Heather Navy / 2XL', 'options': {'color': 'Heather Navy', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18273, 'title': 'Heather Navy / 3XL', 'options': {'color': 'Heather Navy', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18292, 'title': 'Heather Red / S', 'options': {'color': 'Heather Red', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18293, 'title': 'Heather Red / M', 'options': {'color': 'Heather Red', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18294, 'title': 'Heather Red / L', 'options': {'color': 'Heather Red', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18295, 'title': 'Heather Red / XL', 'options': {'color': 'Heather Red', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18296, 'title': 'Heather Red / 2XL', 'options': {'color': 'Heather Red', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18297, 'title': 'Heather Red / 3XL', 'options': {'color': 'Heather Red', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18316, 'title': 'Heather Team Purple / S', 'options': {'color': 'Heather Team Purple', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18317, 'title': 'Heather Team Purple / M', 'options': {'color': 'Heather Team Purple', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18318, 'title': 'Heather Team Purple / L', 'options': {'color': 'Heather Team Purple', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18319, 'title': 'Heather Team Purple / XL', 'options': {'color': 'Heather Team Purple', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18320, 'title': 'Heather Team Purple / 2XL', 'options': {'color': 'Heather Team Purple', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18321, 'title': 'Heather Team Purple / 3XL', 'options': {'color': 'Heather Team Purple', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18324, 'title': 'Heather True Royal / S', 'options': {'color': 'Heather True Royal', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18325, 'title': 'Heather True Royal / M', 'options': {'color': 'Heather True Royal', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18326, 'title': 'Heather True Royal / L', 'options': {'color': 'Heather True Royal', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18327, 'title': 'Heather True Royal / XL', 'options': {'color': 'Heather True Royal', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18328, 'title': 'Heather True Royal / 2XL', 'options': {'color': 'Heather True Royal', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18329, 'title': 'Heather True Royal / 3XL', 'options': {'color': 'Heather True Royal', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18340, 'title': 'Kelly / S', 'options': {'color': 'Kelly', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18341, 'title': 'Kelly / M', 'options': {'color': 'Kelly', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18342, 'title': 'Kelly / L', 'options': {'color': 'Kelly', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18343, 'title': 'Kelly / XL', 'options': {'color': 'Kelly', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18344, 'title': 'Kelly / 2XL', 'options': {'color': 'Kelly', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18345, 'title': 'Kelly / 3XL', 'options': {'color': 'Kelly', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18348, 'title': 'Leaf / S', 'options': {'color': 'Leaf', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18349, 'title': 'Leaf / M', 'options': {'color': 'Leaf', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18350, 'title': 'Leaf / L', 'options': {'color': 'Leaf', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18351, 'title': 'Leaf / XL', 'options': {'color': 'Leaf', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18352, 'title': 'Leaf / 2XL', 'options': {'color': 'Leaf', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18353, 'title': 'Leaf / 3XL', 'options': {'color': 'Leaf', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18356, 'title': 'Light Blue / S', 'options': {'color': 'Light Blue', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18357, 'title': 'Light Blue / M', 'options': {'color': 'Light Blue', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18358, 'title': 'Light Blue / L', 'options': {'color': 'Light Blue', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18359, 'title': 'Light Blue / XL', 'options': {'color': 'Light Blue', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18360, 'title': 'Light Blue / 2XL', 'options': {'color': 'Light Blue', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18361, 'title': 'Light Blue / 3XL', 'options': {'color': 'Light Blue', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18372, 'title': 'Maroon / S', 'options': {'color': 'Maroon', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18373, 'title': 'Maroon / M', 'options': {'color': 'Maroon', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18374, 'title': 'Maroon / L', 'options': {'color': 'Maroon', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18375, 'title': 'Maroon / XL', 'options': {'color': 'Maroon', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18376, 'title': 'Maroon / 2XL', 'options': {'color': 'Maroon', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18377, 'title': 'Maroon / 3XL', 'options': {'color': 'Maroon', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18388, 'title': 'Natural / S', 'options': {'color': 'Natural', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18389, 'title': 'Natural / M', 'options': {'color': 'Natural', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18390, 'title': 'Natural / L', 'options': {'color': 'Natural', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18391, 'title': 'Natural / XL', 'options': {'color': 'Natural', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18392, 'title': 'Natural / 2XL', 'options': {'color': 'Natural', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18393, 'title': 'Natural / 3XL', 'options': {'color': 'Natural', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18396, 'title': 'Navy / S', 'options': {'color': 'Navy', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18397, 'title': 'Navy / M', 'options': {'color': 'Navy', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18398, 'title': 'Navy / L', 'options': {'color': 'Navy', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18399, 'title': 'Navy / XL', 'options': {'color': 'Navy', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18400, 'title': 'Navy / 2XL', 'options': {'color': 'Navy', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18401, 'title': 'Navy / 3XL', 'options': {'color': 'Navy', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18412, 'title': 'Olive / S', 'options': {'color': 'Olive', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18413, 'title': 'Olive / M', 'options': {'color': 'Olive', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18414, 'title': 'Olive / L', 'options': {'color': 'Olive', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18415, 'title': 'Olive / XL', 'options': {'color': 'Olive', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18416, 'title': 'Olive / 2XL', 'options': {'color': 'Olive', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18417, 'title': 'Olive / 3XL', 'options': {'color': 'Olive', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18420, 'title': 'Orange / S', 'options': {'color': 'Orange', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18421, 'title': 'Orange / M', 'options': {'color': 'Orange', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18422, 'title': 'Orange / L', 'options': {'color': 'Orange', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18423, 'title': 'Orange / XL', 'options': {'color': 'Orange', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18424, 'title': 'Orange / 2XL', 'options': {'color': 'Orange', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18425, 'title': 'Orange / 3XL', 'options': {'color': 'Orange', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18436, 'title': 'Pink / S', 'options': {'color': 'Pink', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18437, 'title': 'Pink / M', 'options': {'color': 'Pink', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18438, 'title': 'Pink / L', 'options': {'color': 'Pink', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18439, 'title': 'Pink / XL', 'options': {'color': 'Pink', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18440, 'title': 'Pink / 2XL', 'options': {'color': 'Pink', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18441, 'title': 'Pink / 3XL', 'options': {'color': 'Pink', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18444, 'title': 'Red / S', 'options': {'color': 'Red', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18445, 'title': 'Red / M', 'options': {'color': 'Red', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18446, 'title': 'Red / L', 'options': {'color': 'Red', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18447, 'title': 'Red / XL', 'options': {'color': 'Red', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18448, 'title': 'Red / 2XL', 'options': {'color': 'Red', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18449, 'title': 'Red / 3XL', 'options': {'color': 'Red', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18452, 'title': 'Silver / S', 'options': {'color': 'Silver', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18453, 'title': 'Silver / M', 'options': {'color': 'Silver', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18454, 'title': 'Silver / L', 'options': {'color': 'Silver', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18455, 'title': 'Silver / XL', 'options': {'color': 'Silver', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18456, 'title': 'Silver / 2XL', 'options': {'color': 'Silver', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18457, 'title': 'Silver / 3XL', 'options': {'color': 'Silver', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18460, 'title': 'Soft Cream / S', 'options': {'color': 'Soft Cream', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18461, 'title': 'Soft Cream / M', 'options': {'color': 'Soft Cream', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18462, 'title': 'Soft Cream / L', 'options': {'color': 'Soft Cream', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18463, 'title': 'Soft Cream / XL', 'options': {'color': 'Soft Cream', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18464, 'title': 'Soft Cream / 2XL', 'options': {'color': 'Soft Cream', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18465, 'title': 'Soft Cream / 3XL', 'options': {'color': 'Soft Cream', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18468, 'title': 'Soft Pink / S', 'options': {'color': 'Soft Pink', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18469, 'title': 'Soft Pink / M', 'options': {'color': 'Soft Pink', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18470, 'title': 'Soft Pink / L', 'options': {'color': 'Soft Pink', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18471, 'title': 'Soft Pink / XL', 'options': {'color': 'Soft Pink', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18472, 'title': 'Soft Pink / 2XL', 'options': {'color': 'Soft Pink', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18473, 'title': 'Soft Pink / 3XL', 'options': {'color': 'Soft Pink', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18476, 'title': 'Solid Black Blend / S', 'options': {'color': 'Solid Black Blend', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18477, 'title': 'Solid Black Blend / M', 'options': {'color': 'Solid Black Blend', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18478, 'title': 'Solid Black Blend / L', 'options': {'color': 'Solid Black Blend', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18479, 'title': 'Solid Black Blend / XL', 'options': {'color': 'Solid Black Blend', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18480, 'title': 'Solid Black Blend / 2XL', 'options': {'color': 'Solid Black Blend', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18481, 'title': 'Solid Black Blend / 3XL', 'options': {'color': 'Solid Black Blend', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18492, 'title': 'Steel Blue / S', 'options': {'color': 'Steel Blue', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18493, 'title': 'Steel Blue / M', 'options': {'color': 'Steel Blue', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18494, 'title': 'Steel Blue / L', 'options': {'color': 'Steel Blue', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18495, 'title': 'Steel Blue / XL', 'options': {'color': 'Steel Blue', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18496, 'title': 'Steel Blue / 2XL', 'options': {'color': 'Steel Blue', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18497, 'title': 'Steel Blue / 3XL', 'options': {'color': 'Steel Blue', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18508, 'title': 'Team Purple / S', 'options': {'color': 'Team Purple', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18509, 'title': 'Team Purple / M', 'options': {'color': 'Team Purple', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18510, 'title': 'Team Purple / L', 'options': {'color': 'Team Purple', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18511, 'title': 'Team Purple / XL', 'options': {'color': 'Team Purple', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18512, 'title': 'Team Purple / 2XL', 'options': {'color': 'Team Purple', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18513, 'title': 'Team Purple / 3XL', 'options': {'color': 'Team Purple', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18516, 'title': 'True Royal / S', 'options': {'color': 'True Royal', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18517, 'title': 'True Royal / M', 'options': {'color': 'True Royal', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18518, 'title': 'True Royal / L', 'options': {'color': 'True Royal', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18519, 'title': 'True Royal / XL', 'options': {'color': 'True Royal', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18520, 'title': 'True Royal / 2XL', 'options': {'color': 'True Royal', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18521, 'title': 'True Royal / 3XL', 'options': {'color': 'True Royal', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18524, 'title': 'Turquoise / S', 'options': {'color': 'Turquoise', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18525, 'title': 'Turquoise / M', 'options': {'color': 'Turquoise', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18526, 'title': 'Turquoise / L', 'options': {'color': 'Turquoise', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18527, 'title': 'Turquoise / XL', 'options': {'color': 'Turquoise', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18528, 'title': 'Turquoise / 2XL', 'options': {'color': 'Turquoise', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18529, 'title': 'Turquoise / 3XL', 'options': {'color': 'Turquoise', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18540, 'title': 'White / S', 'options': {'color': 'White', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18541, 'title': 'White / M', 'options': {'color': 'White', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18542, 'title': 'White / L', 'options': {'color': 'White', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18543, 'title': 'White / XL', 'options': {'color': 'White', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18544, 'title': 'White / 2XL', 'options': {'color': 'White', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18545, 'title': 'White / 3XL', 'options': {'color': 'White', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18548, 'title': 'Yellow / S', 'options': {'color': 'Yellow', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18549, 'title': 'Yellow / M', 'options': {'color': 'Yellow', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18550, 'title': 'Yellow / L', 'options': {'color': 'Yellow', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18551, 'title': 'Yellow / XL', 'options': {'color': 'Yellow', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18552, 'title': 'Yellow / 2XL', 'options': {'color': 'Yellow', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 18553, 'title': 'Yellow / 3XL', 'options': {'color': 'Yellow', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38602, 'title': 'Ash / S', 'options': {'color': 'Ash', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38605, 'title': 'Ash / M', 'options': {'color': 'Ash', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38608, 'title': 'Ash / L', 'options': {'color': 'Ash', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38611, 'title': 'Ash / XL', 'options': {'color': 'Ash', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38614, 'title': 'Ash / 2XL', 'options': {'color': 'Ash', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38617, 'title': 'Ash / 3XL', 'options': {'color': 'Ash', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38656, 'title': 'Heather Peach / S', 'options': {'color': 'Heather Peach', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38659, 'title': 'Heather Peach / M', 'options': {'color': 'Heather Peach', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38662, 'title': 'Heather Peach / L', 'options': {'color': 'Heather Peach', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38665, 'title': 'Heather Peach / XL', 'options': {'color': 'Heather Peach', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38668, 'title': 'Heather Peach / 2XL', 'options': {'color': 'Heather Peach', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38671, 'title': 'Heather Peach / 3XL', 'options': {'color': 'Heather Peach', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38710, 'title': 'Heather Aqua / S', 'options': {'color': 'Heather Aqua', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38713, 'title': 'Heather Aqua / M', 'options': {'color': 'Heather Aqua', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38716, 'title': 'Heather Aqua / L', 'options': {'color': 'Heather Aqua', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38719, 'title': 'Heather Aqua / XL', 'options': {'color': 'Heather Aqua', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38722, 'title': 'Heather Aqua / 2XL', 'options': {'color': 'Heather Aqua', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38725, 'title': 'Heather Aqua / 3XL', 'options': {'color': 'Heather Aqua', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38728, 'title': 'Heather Clay / S', 'options': {'color': 'Heather Clay', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38731, 'title': 'Heather Clay / M', 'options': {'color': 'Heather Clay', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38734, 'title': 'Heather Clay / L', 'options': {'color': 'Heather Clay', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38737, 'title': 'Heather Clay / XL', 'options': {'color': 'Heather Clay', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38740, 'title': 'Heather Clay / 2XL', 'options': {'color': 'Heather Clay', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38743, 'title': 'Heather Clay / 3XL', 'options': {'color': 'Heather Clay', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38746, 'title': 'Heather Columbia Blue / S', 'options': {'color': 'Heather Columbia Blue', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38749, 'title': 'Heather Columbia Blue / M', 'options': {'color': 'Heather Columbia Blue', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38752, 'title': 'Heather Columbia Blue / L', 'options': {'color': 'Heather Columbia Blue', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38755, 'title': 'Heather Columbia Blue / XL', 'options': {'color': 'Heather Columbia Blue', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38758, 'title': 'Heather Columbia Blue / 2XL', 'options': {'color': 'Heather Columbia Blue', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38761, 'title': 'Heather Columbia Blue / 3XL', 'options': {'color': 'Heather Columbia Blue', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38764, 'title': 'Heather Ice Blue / S', 'options': {'color': 'Heather Ice Blue', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38767, 'title': 'Heather Ice Blue / M', 'options': {'color': 'Heather Ice Blue', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38770, 'title': 'Heather Ice Blue / L', 'options': {'color': 'Heather Ice Blue', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38773, 'title': 'Heather Ice Blue / XL', 'options': {'color': 'Heather Ice Blue', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38776, 'title': 'Heather Ice Blue / 2XL', 'options': {'color': 'Heather Ice Blue', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38779, 'title': 'Heather Ice Blue / 3XL', 'options': {'color': 'Heather Ice Blue', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38782, 'title': 'Black Heather / S', 'options': {'color': 'Black Heather', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38785, 'title': 'Black Heather / M', 'options': {'color': 'Black Heather', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38788, 'title': 'Black Heather / L', 'options': {'color': 'Black Heather', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38791, 'title': 'Black Heather / XL', 'options': {'color': 'Black Heather', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38794, 'title': 'Black Heather / 2XL', 'options': {'color': 'Black Heather', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 38797, 'title': 'Black Heather / 3XL', 'options': {'color': 'Black Heather', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 39556, 'title': 'Heather Olive / S', 'options': {'color': 'Heather Olive', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 39559, 'title': 'Heather Olive / M', 'options': {'color': 'Heather Olive', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 39562, 'title': 'Heather Olive / L', 'options': {'color': 'Heather Olive', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 39565, 'title': 'Heather Olive / XL', 'options': {'color': 'Heather Olive', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 39568, 'title': 'Heather Olive / 2XL', 'options': {'color': 'Heather Olive', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 39571, 'title': 'Heather Olive / 3XL', 'options': {'color': 'Heather Olive', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 39577, 'title': 'Brown / S', 'options': {'color': 'Brown', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 39580, 'title': 'Brown / M', 'options': {'color': 'Brown', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 39583, 'title': 'Brown / L', 'options': {'color': 'Brown', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 39586, 'title': 'Brown / XL', 'options': {'color': 'Brown', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 39589, 'title': 'Brown / 2XL', 'options': {'color': 'Brown', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 39592, 'title': 'Brown / 3XL', 'options': {'color': 'Brown', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 61821, 'title': 'Heather Mauve / S', 'options': {'color': 'Heather Mauve', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 61822, 'title': 'Heather Mauve / M', 'options': {'color': 'Heather Mauve', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 61823, 'title': 'Heather Mauve / L', 'options': {'color': 'Heather Mauve', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 61824, 'title': 'Heather Mauve / XL', 'options': {'color': 'Heather Mauve', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 61825, 'title': 'Heather Mauve / 2XL', 'options': {'color': 'Heather Mauve', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 61826, 'title': 'Heather Mauve / 3XL', 'options': {'color': 'Heather Mauve', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 64317, 'title': 'Military Green / S', 'options': {'color': 'Military Green', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 64318, 'title': 'Military Green / M', 'options': {'color': 'Military Green', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 64319, 'title': 'Military Green / L', 'options': {'color': 'Military Green', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 64320, 'title': 'Military Green / XL', 'options': {'color': 'Military Green', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 64321, 'title': 'Military Green / 2XL', 'options': {'color': 'Military Green', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 64322, 'title': 'Military Green / 3XL', 'options': {'color': 'Military Green', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 66337, 'title': 'Charity Pink / S', 'options': {'color': 'Charity Pink', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 66338, 'title': 'Charity Pink / M', 'options': {'color': 'Charity Pink', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 66339, 'title': 'Charity Pink / L', 'options': {'color': 'Charity Pink', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 66340, 'title': 'Charity Pink / XL', 'options': {'color': 'Charity Pink', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 66341, 'title': 'Charity Pink / 2XL', 'options': {'color': 'Charity Pink', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 66342, 'title': 'Charity Pink / 3XL', 'options': {'color': 'Charity Pink', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 80473, 'title': 'Autumn / S', 'options': {'color': 'Autumn', 'size': 'S'}, 'placeholders': [{'position': 'back', 'height': 3761, 'width': 3319}, {'position': 'front', 'height': 3761, 'width': 3319}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 80474, 'title': 'Autumn / M', 'options': {'color': 'Autumn', 'size': 'M'}, 'placeholders': [{'position': 'back', 'height': 4431, 'width': 3909}, {'position': 'front', 'height': 4431, 'width': 3909}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 80475, 'title': 'Autumn / L', 'options': {'color': 'Autumn', 'size': 'L'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 80476, 'title': 'Autumn / XL', 'options': {'color': 'Autumn', 'size': 'XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 80477, 'title': 'Autumn / 2XL', 'options': {'color': 'Autumn', 'size': '2XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]},
{'id': 80478, 'title': 'Autumn / 3XL', 'options': {'color': 'Autumn', 'size': '3XL'}, 'placeholders': [{'position': 'back', 'height': 5100, 'width': 4500}, {'position': 'front', 'height': 5100, 'width': 4500}, {'position': 'neck', 'height': 750, 'width': 750}]}
        ]


    },
    'candle' : {
        'colors' : ['Amber', 'Clear'],
        'sizes' : ['4oz', '9oz'],  
        'design_sizes' : [(624, 546), (863, 706)], # 4oz, 9oz
        'template_images': ['candle_4oz.png', 'candle_9oz.png'], 
        'positions' : ['front', 'back', 'neck'],
        'scents' : ['Lavender', 'Cashmere Musk', 'Cinnamon Chai', 'Fraser Fir', 'Mango Coconut', 'Unscented', 'vanilla Bean', 'Beachwood', 'Midnight Blackberry'],
        'prices' : [1999, 2599], 
        'blueprint_id' : 1488,
        'print_provider_id' : 70,
        'variants': [
            {'id': 107587, 'title': '4oz / Clear / Beachwood', 'options': {'size': '4oz', 'color': 'Clear', 'scent': 'Beachwood'}, 'placeholders': [{'position': 'front', 'height': 546, 'width': 624}]},
{'id': 107588, 'title': '4oz / Clear / Cashmere Musk', 'options': {'size': '4oz', 'color': 'Clear', 'scent': 'Cashmere Musk'}, 'placeholders': [{'position': 'front', 'height': 546, 'width': 624}]},
{'id': 107589, 'title': '4oz / Clear / Cinnamon Chai', 'options': {'size': '4oz', 'color': 'Clear', 'scent': 'Cinnamon Chai'}, 'placeholders': [{'position': 'front', 'height': 546, 'width': 624}]},
{'id': 107590, 'title': '4oz / Clear / Fraser Fir', 'options': {'size': '4oz', 'color': 'Clear', 'scent': 'Fraser Fir'}, 'placeholders': [{'position': 'front', 'height': 546, 'width': 624}]},
{'id': 107591, 'title': '4oz / Clear / Lavender', 'options': {'size': '4oz', 'color': 'Clear', 'scent': 'Lavender'}, 'placeholders': [{'position': 'front', 'height': 546, 'width': 624}]},
{'id': 107592, 'title': '4oz / Clear / Midnight Blackberry', 'options': {'size': '4oz', 'color': 'Clear', 'scent': 'Midnight Blackberry'}, 'placeholders': [{'position': 'front', 'height': 546, 'width': 624}]},
{'id': 107593, 'title': '4oz / Clear / Mango Coconut', 'options': {'size': '4oz', 'color': 'Clear', 'scent': 'Mango Coconut'}, 'placeholders': [{'position': 'front', 'height': 546, 'width': 624}]},
{'id': 107594, 'title': '4oz / Clear / Unscented', 'options': {'size': '4oz', 'color': 'Clear', 'scent': 'Unscented'}, 'placeholders': [{'position': 'front', 'height': 546, 'width': 624}]},
{'id': 107595, 'title': '4oz / Clear / Vanilla Bean', 'options': {'size': '4oz', 'color': 'Clear', 'scent': 'Vanilla Bean'}, 'placeholders': [{'position': 'front', 'height': 546, 'width': 624}]},
{'id': 107596, 'title': '9oz / Clear / Beachwood', 'options': {'size': '9oz', 'color': 'Clear', 'scent': 'Beachwood'}, 'placeholders': [{'position': 'front', 'height': 706, 'width': 863}]},
{'id': 107597, 'title': '9oz / Clear / Cashmere Musk', 'options': {'size': '9oz', 'color': 'Clear', 'scent': 'Cashmere Musk'}, 'placeholders': [{'position': 'front', 'height': 706, 'width': 863}]},
{'id': 107598, 'title': '9oz / Clear / Cinnamon Chai', 'options': {'size': '9oz', 'color': 'Clear', 'scent': 'Cinnamon Chai'}, 'placeholders': [{'position': 'front', 'height': 706, 'width': 863}]},
{'id': 107599, 'title': '9oz / Clear / Fraser Fir', 'options': {'size': '9oz', 'color': 'Clear', 'scent': 'Fraser Fir'}, 'placeholders': [{'position': 'front', 'height': 706, 'width': 863}]},
{'id': 107600, 'title': '9oz / Clear / Lavender', 'options': {'size': '9oz', 'color': 'Clear', 'scent': 'Lavender'}, 'placeholders': [{'position': 'front', 'height': 706, 'width': 863}]},
{'id': 107601, 'title': '9oz / Clear / Midnight Blackberry', 'options': {'size': '9oz', 'color': 'Clear', 'scent': 'Midnight Blackberry'}, 'placeholders': [{'position': 'front', 'height': 706, 'width': 863}]},
{'id': 107602, 'title': '9oz / Clear / Mango Coconut', 'options': {'size': '9oz', 'color': 'Clear', 'scent': 'Mango Coconut'}, 'placeholders': [{'position': 'front', 'height': 706, 'width': 863}]},
{'id': 107603, 'title': '9oz / Clear / Unscented', 'options': {'size': '9oz', 'color': 'Clear', 'scent': 'Unscented'}, 'placeholders': [{'position': 'front', 'height': 706, 'width': 863}]},
{'id': 107604, 'title': '9oz / Clear / Vanilla Bean', 'options': {'size': '9oz', 'color': 'Clear', 'scent': 'Vanilla Bean'}, 'placeholders': [{'position': 'front', 'height': 706, 'width': 863}]},
{'id': 107605, 'title': '4oz / Amber / Beachwood', 'options': {'size': '4oz', 'color': 'Amber', 'scent': 'Beachwood'}, 'placeholders': [{'position': 'front', 'height': 546, 'width': 624}]},
{'id': 107606, 'title': '4oz / Amber / Cashmere Musk', 'options': {'size': '4oz', 'color': 'Amber', 'scent': 'Cashmere Musk'}, 'placeholders': [{'position': 'front', 'height': 546, 'width': 624}]},
{'id': 107607, 'title': '4oz / Amber / Cinnamon Chai', 'options': {'size': '4oz', 'color': 'Amber', 'scent': 'Cinnamon Chai'}, 'placeholders': [{'position': 'front', 'height': 546, 'width': 624}]},
{'id': 107608, 'title': '4oz / Amber / Fraser Fir', 'options': {'size': '4oz', 'color': 'Amber', 'scent': 'Fraser Fir'}, 'placeholders': [{'position': 'front', 'height': 546, 'width': 624}]},
{'id': 107609, 'title': '4oz / Amber / Lavender', 'options': {'size': '4oz', 'color': 'Amber', 'scent': 'Lavender'}, 'placeholders': [{'position': 'front', 'height': 546, 'width': 624}]},
{'id': 107610, 'title': '4oz / Amber / Midnight Blackberry', 'options': {'size': '4oz', 'color': 'Amber', 'scent': 'Midnight Blackberry'}, 'placeholders': [{'position': 'front', 'height': 546, 'width': 624}]},
{'id': 107611, 'title': '4oz / Amber / Mango Coconut', 'options': {'size': '4oz', 'color': 'Amber', 'scent': 'Mango Coconut'}, 'placeholders': [{'position': 'front', 'height': 546, 'width': 624}]},
{'id': 107612, 'title': '4oz / Amber / Unscented', 'options': {'size': '4oz', 'color': 'Amber', 'scent': 'Unscented'}, 'placeholders': [{'position': 'front', 'height': 546, 'width': 624}]},
{'id': 107613, 'title': '4oz / Amber / Vanilla Bean', 'options': {'size': '4oz', 'color': 'Amber', 'scent': 'Vanilla Bean'}, 'placeholders': [{'position': 'front', 'height': 546, 'width': 624}]},
{'id': 107614, 'title': '9oz / Amber / Beachwood', 'options': {'size': '9oz', 'color': 'Amber', 'scent': 'Beachwood'}, 'placeholders': [{'position': 'front', 'height': 706, 'width': 863}]},
{'id': 107615, 'title': '9oz / Amber / Cashmere Musk', 'options': {'size': '9oz', 'color': 'Amber', 'scent': 'Cashmere Musk'}, 'placeholders': [{'position': 'front', 'height': 706, 'width': 863}]},
{'id': 107616, 'title': '9oz / Amber / Cinnamon Chai', 'options': {'size': '9oz', 'color': 'Amber', 'scent': 'Cinnamon Chai'}, 'placeholders': [{'position': 'front', 'height': 706, 'width': 863}]},
{'id': 107617, 'title': '9oz / Amber / Fraser Fir', 'options': {'size': '9oz', 'color': 'Amber', 'scent': 'Fraser Fir'}, 'placeholders': [{'position': 'front', 'height': 706, 'width': 863}]},
{'id': 107618, 'title': '9oz / Amber / Lavender', 'options': {'size': '9oz', 'color': 'Amber', 'scent': 'Lavender'}, 'placeholders': [{'position': 'front', 'height': 706, 'width': 863}]},
{'id': 107619, 'title': '9oz / Amber / Midnight Blackberry', 'options': {'size': '9oz', 'color': 'Amber', 'scent': 'Midnight Blackberry'}, 'placeholders': [{'position': 'front', 'height': 706, 'width': 863}]},
{'id': 107620, 'title': '9oz / Amber / Mango Coconut', 'options': {'size': '9oz', 'color': 'Amber', 'scent': 'Mango Coconut'}, 'placeholders': [{'position': 'front', 'height': 706, 'width': 863}]},
{'id': 107621, 'title': '9oz / Amber / Unscented', 'options': {'size': '9oz', 'color': 'Amber', 'scent': 'Unscented'}, 'placeholders': [{'position': 'front', 'height': 706, 'width': 863}]},
{'id': 107622, 'title': '9oz / Amber / Vanilla Bean', 'options': {'size': '9oz', 'color': 'Amber', 'scent': 'Vanilla Bean'}, 'placeholders': [{'position': 'front', 'height': 706, 'width': 863}]}
        ]
        
    }
}


def resize_image(image, new_width, new_height):
    return image.resize((new_width, new_height), Image.LANCZOS)



def create_candle_design_image(main_image, template_image, output_path, background_size=(624, 546), output_format='JPEG'):
    """
    Creates a white background image, places the middle image on top, and then places the top image on both.

    Parameters:
    main_image (str): Path to the middle image.
    template_image (str): Path to the top image.
    output_path (str): Path to save the resulting image.
    background_size (tuple): Size of the background image (width, height).
    output_format (str): Format to save the resulting image (default is 'JPEG').

    Returns:
    Image: The resulting image object.
    """
    # Create a white background image
    bottom = Image.new("RGBA", background_size, (255, 255, 255, 255))

    # Open the middle and top images
    print("main image to be printed on candle:", main_image) 
    main_image = Image.open(main_image).convert("RGBA")
    main_image_size = (background_size[1] - 20, background_size[1] - 20)
    main_image = resize_image(main_image, new_width = main_image_size[0], new_height = main_image_size[1])
    
    
    top = Image.open(template_image).convert("RGBA")
    template_name = template_image.split('/')[-1].split('.')[0]
    

    # Paste the top image on the combined image at position (0, 0)
    bottom.paste(top, (0, 0), top)
    
    # Paste the middle image on the background image at position (10, 10)
    bottom.paste(main_image, (10, 10), main_image)


    # Convert to 'RGB' mode if output format is JPEG
    if output_format.upper() == 'JPEG':
        bottom = bottom.convert('RGB')

    # Save the resulting image
    output_path = output_path.split('.')[0] + '_' + template_name + '.png'
    bottom.save(output_path, format=output_format)

    return bottom

def upload_image_printify(image, printify_key):
    base_url = "https://api.printify.com/v1"
    upload_url = f"{base_url}/uploads/images.json"
    headers = {
        "Authorization": f"Bearer {printify_key}",
        "Content-Type": "application/json"
    }

    if isinstance(image, str):
        # Read and encode the image file in base64
        with open(image, "rb") as img_file:
            img_b64 = base64.b64encode(img_file.read()).decode('utf-8')
        file_name = os.path.basename(image)
    else:
        # Convert the PIL Image to bytes
        img_byte_arr = io.BytesIO()
        if image.mode == 'RGBA':
            image = image.convert('RGB')  # Convert RGBA to RGB
        image.save(img_byte_arr, format='JPEG')  # Adjust format as needed (e.g., PNG)
        img_byte_arr.seek(0)  # Move to the start of the byte array
        img_b64 = base64.b64encode(img_byte_arr.read()).decode('utf-8')
        file_name = "image.jpg"  # Assign a generic file name or create a naming convention

    # Prepare the JSON data for the POST request
    data = {
        "file_name": file_name,
        "contents": img_b64
    }

    # Upload the image to the Printify media library
    response = requests.post(upload_url, headers=headers, json=data)
    # Ensure the response is successful and contains the necessary data
    if response.status_code == 200:
        image_id = response.json().get("id")
        return image_id
    else:
        print("Failed to upload image:", response.json())
        return None



def prepare_and_upload_product_images(product_name, image_path) : 

    image_name = os.path.basename(image_path).split('.')[0]
    product_name = product_name.lower()
    product = products[product_name]
    current_date = datetime.now().strftime("%m_%d")
    image_ids = [] 
    print(f"uploading images for {product_name}")
    if product_name == 'candle' :
        for i, s in enumerate(product['sizes']) :
            template_image = [img for img in product['template_images'] if s in img][0]
            template_image_path = os.path.join(current_app.static_folder, 'images', 'templates', template_image)
            output_image_folder = os.path.join(current_app.static_folder, 'images', 'designs', current_date)
            if not os.path.exists(output_image_folder):
                os.makedirs(output_image_folder)
            output_image_path = os.path.join(output_image_folder, f'{image_name}.png')
            design_image = create_candle_design_image(image_path, template_image_path, output_path = output_image_path, background_size=product['design_sizes'][i])
            image_id =upload_image_printify(design_image, printify_key)
            image_ids.append(image_id)
    elif product_name == 't-shirt': 
        for i, s in enumerate(product['sizes']) : 
            print(f"uploading image for the size:{s}")
            image = Image.open(image_path).convert("RGBA")
            main_image_size = product['design_sizes'][i]
            image = resize_image(image, new_width = main_image_size[0], new_height = main_image_size[1])            
            image_id = upload_image_printify(image, printify_key)
            image_ids.append(image_id) 
        neck_image_path = os.path.join(current_app.static_folder, 'images', 'templates', 'neck.png')
        neck_image = Image.open(neck_image_path).convert("RGBA")
        neck_image_size = product['design_sizes'][-1]
        neck_image = resize_image(neck_image, new_width = neck_image_size[0], new_height = neck_image_size[1])
        neck_image_id = upload_image_printify(neck_image, printify_key)
        image_ids.append(neck_image_id)
    else : 
        print(f"Product {product_name} not supported")

    print(f"Image ids uploaded: {len(image_ids)}")
    return image_ids 




def submit_product(product_name, title, description, colors, image_path) : 

    if globals.lastPrintTime is None : 
        globals.lastPrintTime = datetime.now()

    
    if product_name.lower() not in supported_products : 
        print(f"Product {product_name} not supported")
        return False, 'Could not process print request'
    else : 
        print(f"Processing print request for {product_name}")

        product = products[product_name.lower()]
        image_ids = prepare_and_upload_product_images(product_name, image_path)

        print(f"Image ids uploaded: {len(image_ids)}")
        print_areas = []
        target_products = {s:[] for s in product['sizes']}

        product_variants = product['variants']
        for variant in product_variants :
            s = variant['options']['size']
            c = variant['options']['color']
            if c.lower() in colors and s in product['sizes'] :
                print(f"Adding variant {variant['title']} to target products")
                target_products[s].append(variant)

        print(f"Target products: {target_products}")
        prices = product['prices']
        target_variants = []
        for k, variants in target_products.items() :
            variant_ids = []
            print("variants:", len(variants))
            for variant in variants :
                idx = product['sizes'].index(variant['options']['size'])
                print("Index:", idx)
                v = {
                    "id": variant['id'],
                    "is_enabled": True,
                    "price": prices[idx]
                }
                target_variants.append(v)
                variant_ids.append(variant['id'])
            if len(variant_ids) == 0 :
                print(f"No variants found for size {k}")
                continue
            else : 
                print(f" variants found for size {k}: {len(variant_ids)}")
            print_area = {
                'variant_ids': variant_ids,

                "placeholders": [
                {
                    "position": "neck",
                    "images": [
                        {
                            "id": image_ids[-1],  # neck small size image id
                            "x": 0.5,
                            "y": 0.5,
                            "scale": 1.0,
                            "angle": 0
                        }
                    ]
                },
                {
                    "position": "front",
                    "images": [
                        {
                            "id": image_ids[idx],  # Front small size image id
                            "x": 0.5,
                            "y": 0.5,
                            "scale": 1.0,
                            "angle": 0
                        }
                    ]
                }

            ]

            }
            print_areas.append(print_area)

            print("print areas:", len(print_areas))
        data = {
            "title": title,
            "description": description, 
            "blueprint_id": product['blueprint_id'],  # Example blueprint ID
            "print_provider_id": product['print_provider_id'],
            "variants": target_variants,
            "print_areas": print_areas
        }

        headers = {
        "Authorization": f"Bearer {printify_key}",
        "Content-Type": "application/json"
        }
        response = requests.post(shop_url.format(base_url, shop_id), headers=headers, json=data)
        if response.status_code >= 200 and response.status_code < 300:
            print(f"Product created successfully!")
            return True, 'Print request submitted successfully'
        else:
            print(f"Failed to create product. Server responded with: {response.text}")
            return False, 'Print request submitted successfully'






