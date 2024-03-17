import os
import requests
import io
from io import BytesIO
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def grab_poke(url="https://pokeapi.co/api/v2/pokemon/" , poke_number=1):
    pokemon_json = requests.get(url+str(poke_number)).json()
    pokemon_image_url = pokemon_json["sprites"]["front_default"]
    image_io = requests.get(pokemon_image_url).content
    image = Image.open(io.BytesIO(image_io))
    return image


def turn_black_resize(img):
    gray_image = img.convert("L") ## turn image gray
    gray_image_numpy = np.copy(np.asarray(gray_image)) ## copy to prevent only read rights
    height, width = np.where(gray_image_numpy ==0) 
    gray_image_numpy[height, width] = 255
    
    poke = Image.fromarray(gray_image_numpy)
    poke = poke.resize((350,350), Image.Resampling.NEAREST) ## resize image to fit into backgroung
    
    poke_numpy = np.copy(np.asarray(poke)) 
    height, width = np.where(poke_numpy <255)
    poke_numpy[height, width] = 0 ## turn Pokemon black
    poke_numpy = poke_numpy[np.min(height): np.max(height), np.min(width):np.max(width)] ## crop
    poke = Image.fromarray(poke_numpy)
    return poke


def create_whos_poke(img):
    background = Image.open("whos_that_poke.png")
    height, width, channel = np.asarray(background).shape
    who = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    who.paste(background)
    resized_height, resized_width = img.size
    anker = (405- int(resized_height/2), int(394-(resized_width/2)))
    who.paste(img, anker)
    return who