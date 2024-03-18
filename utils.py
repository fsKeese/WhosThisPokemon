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
    return poke, img.resize((350,350), Image.Resampling.NEAREST) ## return original as well


def create_whos_poke(img):
    background = Image.open("whos_that_poke.png")
    height, width, channel = np.asarray(background).shape
    who = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    who.paste(background)
    resized_height, resized_width = img.size
    anker = (405- int(resized_height/2), int(394-(resized_width/2)))
    who.paste(img, anker)
    return who


class Pokemon:
    def __init__(self, url="https://pokeapi.co/api/v2/pokemon/", background_path="whos_that_poke.png", id=9):
        self.id = id
        self.pokemon_json = requests.get(url+str(self.id)).json()
        self.background_path = background_path
        
        self.sprite = self.pokemon_json["sprites"]["front_default"]
    
    def load_pokemon_image(self):
        image_io = requests.get(self.sprite).content
        img = Image.open(io.BytesIO(image_io)).convert("RGB")
        return img
        
    def turn_black(self):
        img = self.load_pokemon_image()
        
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
    
    def turn_boarder_white(self):
        original_img = self.load_pokemon_image()
        
        gray_image = original_img.convert("L") ## turn image gray
        gray_image_numpy = np.copy(np.asarray(gray_image)) ## copy to prevent only read rights
        height, width = np.where(gray_image_numpy ==0) 
        
        np_image = np.copy(np.asarray(original_img))
        np_image[height, width, :] = 255
        #np_image = np_image[np.min(height): np.max(height), np.min(width):np.max(width)] ## crop
        
        poke = Image.fromarray(np_image)
        poke = poke.resize((350,350), Image.Resampling.NEAREST) ## resize image to fit into backgroung
        return poke
    
    
    def get_question(self):
        img = self.turn_black()
        background = Image.open(self.background_path)
        height, width, channel = np.asarray(background).shape
        who = Image.new("RGBA", (width, height), (255, 255, 255, 255))
        who.paste(background)
        resized_height, resized_width = img.size
        anker = (405- int(resized_height/2), int(394-(resized_width/2)))
        who.paste(img, anker)
        return who
    
    def get_solution(self):
        img = self.turn_boarder_white()
        
        background = Image.open(self.background_path)
        height, width, channel = np.asarray(background).shape
        who = Image.new("RGBA", (width, height), (255, 255, 255, 255))
        who.paste(background)
        resized_height, resized_width = img.size
        anker = (405- int(resized_height/2), int(394-(resized_width/2)))
        who.paste(img, anker)   
        return who     
        
        