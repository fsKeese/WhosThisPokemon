import os
import requests
import numpy as np
import io
from io import BytesIO
from PIL import Image

import streamlit as st
from utils import *

st.write("""
         Is this Ditto?
         """)



if st.button("Next"):
    pokemon_id = np.random.randint(0, 1025) ## ALLLLL POKEEEE
    img = grab_poke(url="https://pokeapi.co/api/v2/pokemon/", poke_number=pokemon_id)
    img = turn_black_resize(img)
    result = create_whos_poke(img)
    st.image(result)


