import os
import requests
import numpy as np
import io
from io import BytesIO
from PIL import Image

import streamlit as st

pokemon = 250


pokemon_json = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}").json()
pokemon_image_url = pokemon_json["sprites"]["other"]["official-artwork"]["front_default"]
image_io = requests.get(pokemon_image_url).content
image = Image.open(io.BytesIO(image_io))


st.write("""
         Is this Ditto?
         """)
st.write(image)