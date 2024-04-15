import os
import sys
import random
from pathlib import Path
import requests
import io
from io import BytesIO
import numpy as np
from pydub import AudioSegment
from PIL import Image
import matplotlib.pyplot as plt
from gtts import gTTS 
from patchify import patchify, unpatchify


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


def remove_oggs(path=r"C:\Users\Keese\Documents\GitHub\WhosThisPokemon\sounds\temp"):
    for file in path:
        if file.endswith(".ogg") or file.endswith(".wav"):
            os.remove(os.path.join(path, file))

class Pokemon:
    def __init__(self, url="https://pokeapi.co/api/v2/pokemon/", background_path="whos_that_poke.png", audio_path=r"sounds\temp", id=9):
        self.id = id
        self.pokemon_json = requests.get(url+str(self.id)).json()
        self.background_path = background_path
        self.pokemon_audio = Path(audio_path)
        
        self.name = self.pokemon_json["forms"][0]["name"]
        self.sprite = self.pokemon_json["sprites"]["front_default"]
        self.weight = self.pokemon_json["weight"]
        self.type = self.pokemon_json["types"][0]["type"]["name"]
    
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
    
    def get_cry_url(self):
        cry_url = self.pokemon_json["cries"]["legacy"]
        return cry_url
    
    def get_weight(self):
        return self.weight/10
    
    def get_second_type(self):
        if len(self.pokemon_json["types"]) >1:
            second_type = self.pokemon_json["types"][1]["type"]["name"]
        else:
            second_type = None
        return second_type          
    
    def download_cry(self):
        temp_audio = self.pokemon_audio / "temp"
        cry_url = self.get_cry_url()
        cry_content = requests.get(cry_url)
        with open(temp_audio / (str(self.id)+".ogg"), "wb") as o:
            o.write(cry_content.content)
        return temp_audio / (str(self.id)+".ogg")
    
    def cry_wav(self):
        temp_audio = self.pokemon_audio / "temp"
        cry_path = self.download_cry()
        sound = AudioSegment.from_ogg(cry_path)
        sound.export(temp_audio / (str(self.id) +".wav"), format="wav")
        return temp_audio / (str(self.id) +".wav")
    
    def get_pokename_mp3(self):
        language = 'en'
        mp3 = gTTS(text=str(self.name).capitalize, lang=language, slow=False)
        mp3_path = os.path.join(self.pokemon_audio, str(self.name) +".mp3")
        #mp3.save(mp3_path)
        mp3.save("sounds/temp/test.mp3")
        return mp3_path
    
    def get_pokechamp(self):
        temp = requests.get("https://ddragon.leagueoflegends.com/cdn/14.7.1/data/en_US/champion.json").json()
        champ_name = random.choice(list(temp["data"].keys())) # chose random league champ from all champs
        league_json = requests.get(f"https://ddragon.leagueoflegends.com/cdn/14.7.1/data/en_US/champion/{str(champ_name)}.json").json()
        skin = random.choice(league_json["data"][str(champ_name)]["skins"])["num"]
        
        
        league_json_img = requests.get(f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{str(champ_name)+'_'+str(skin)}.jpg").content
        
        pokemon_json = requests.get(f"https://pokeapi.co/api/v2/pokemon/{str(self.id)}").json()
        pokemon_json_img = requests.get(pokemon_json["sprites"]["other"]["official-artwork"]["front_default"]).content
        pokemon_image = Image.open(io.BytesIO(pokemon_json_img)).convert("RGB")
        
        champion_image = Image.open(io.BytesIO(league_json_img)).convert("RGB")
        poke_resized = pokemon_image.resize(champion_image.size, Image.Resampling.NEAREST)

        pokechmap_img = Image.fromarray(np.asarray(poke_resized) + np.asarray(champion_image))
        return pokechmap_img, (champ_name, self.name)
    
    def get_pokechamp_remastered(self):
        pokemon_json = requests.get(f"https://pokeapi.co/api/v2/pokemon/{str(self.id)}").json()
        pokemon_json_img = requests.get(pokemon_json["sprites"]["other"]["official-artwork"]["front_default"]).content
        pokemon_image = Image.open(io.BytesIO(pokemon_json_img)).convert("RGB")
        
        temp = requests.get("https://ddragon.leagueoflegends.com/cdn/14.7.1/data/en_US/champion.json").json()
        champ_name = random.choice(list(temp["data"].keys())) # chose random league champ from all champs
        league_json = requests.get(f"https://ddragon.leagueoflegends.com/cdn/14.7.1/data/en_US/champion/{str(champ_name)}.json").json()
        skin = random.choice(league_json["data"][str(champ_name)]["skins"])["num"]
        
        
        league_json_img = requests.get(f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{str(champ_name)+'_'+str(skin)}.jpg").content
        
        
        champion_image = Image.open(io.BytesIO(league_json_img)).convert("RGB")
        
        champ_image_resized = champion_image.resize((500,500), Image.Resampling.NEAREST)
        poke_resized = pokemon_image.resize((500, 500), Image.Resampling.NEAREST)

        patches_poke = patchify(np.asarray(poke_resized), (50,50,3), 50)
        patches_champ = patchify(np.asarray(champ_image_resized), (50,50,3), 50)


        patches = [patches_poke, patches_champ]
        new_image = np.zeros((500,500,3), np.uint8)
        for i in range(0,10):
            i_list = list(l for l in range(0,10))
            j_list = list(l for l in range(0,10))
            for j in range(0,10):
                x = random.choice(i_list)
                y = random.choice(j_list)
                p = random.choice(patches)
                new_image[i*50:(i+1)*50, j*50:(j+1)*50,:] = p[x][y][0]
                
                i_list.remove(x)
                j_list.remove(y)
        
        dst = Image.new('RGB', (poke_resized.width + champ_image_resized.width, poke_resized.height))
        dst.paste(poke_resized, (0, 0))
        dst.paste(champ_image_resized, (poke_resized.width, 0))
        
        return Image.fromarray(new_image), (champ_name, self.name), dst
        