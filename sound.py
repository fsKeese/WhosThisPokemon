import os
import requests
import io
from io import BytesIO
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pathlib import Path

audio_path = Path(r"C:\Users\Keese\Documents\GitHub\WhosThisPokemon\sounds")
pokemon_json = requests.get("https://pokeapi.co/api/v2/pokemon/9").json()

r = requests.get(pokemon_json["cries"]["legacy"])
cry_url = pokemon_json["cries"]["legacy"]
cry_content = requests.get(cry_url)
with open(f"sounds\{str(9)}.ogg", "wb") as o:
    o.write(cry_content.content)
sound = AudioSegment.from_ogg(audio_path / (str(9)+".ogg"))
sound.export(audio_path / (str(9)+".wav"), format="wav")