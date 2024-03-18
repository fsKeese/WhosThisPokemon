import os
import requests
import numpy as np
import io
from io import BytesIO
from PIL import Image
from playsound import playsound

import streamlit as st
from utils import *



if "pokemon_id" not in st.session_state:
    st.session_state.pokemon_id = 1


st.write("""
         Is this Ditto?
         """)



# if st.button("Next"):
#     pokemon_id = np.random.randint(0, 1025) ## ALLLLL POKEEEE
#     img = grab_poke(url="https://pokeapi.co/api/v2/pokemon/", poke_number=pokemon_id)
#     img, solution = turn_black_resize(img)
#     result = create_whos_poke(img)
#     st.image(result)

# if st.button("Result"):
#     result_sol = create_whos_poke(solution)
#     st.image(result_sol)

if st.button("Next"):
    #st.audio("sounds\whoisthat.wav")
    poke_id = np.random.randint(0, 1020)
    st.session_state.pokemon_id = poke_id
    poke = Pokemon(url="https://pokeapi.co/api/v2/pokemon/", background_path="whos_that_poke.png", id=st.session_state.pokemon_id)
    st.image(poke.get_question())
    playsound("sounds\whoisthat.wav")

if st.button("Result"):
    poke = Pokemon(url="https://pokeapi.co/api/v2/pokemon/", background_path="whos_that_poke.png", id=st.session_state.pokemon_id)

    st.image(poke.get_solution())
    playsound("sounds\its.wav")
