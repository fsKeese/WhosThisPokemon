import os
import requests
import numpy as np
import io
from io import BytesIO
from PIL import Image
from playsound import playsound
from pydub import AudioSegment



import streamlit as st
from utils import *



#################### Session State variables: ####################

if "pokemon_id" not in st.session_state:
    st.session_state.pokemon_id = None
if "pokemon_name" not in st.session_state:
    st.session_state.pokemon_name = None
if "next" not in st.session_state:
    st.session_state.next = False
if "result" not in st.session_state:
    st.session_state.result = False
if "pokemon" not in st.session_state:
    st.session_state.pokemon = None




st.title("""
         Who is that Pokemon?
         """)

## two columns layout
left_column, right_column, outer_right_column = st.columns((3,1,1))

wild = st.checkbox('Go Wild')

if left_column.button("Next"):
    poke_id = np.random.randint(0, 1020)
    st.session_state.pokemon_id = poke_id
    st.session_state.pokemon = Pokemon(url="https://pokeapi.co/api/v2/pokemon/", background_path="whos_that_poke.png", id=st.session_state.pokemon_id)
    poke = st.session_state.pokemon  
    st.session_state.pokemon_name = str(poke.name).capitalize()
    
    st.session_state.next = True
    st.session_state.result = False
    
    if not wild:
        st.session_state.image = poke.get_question()
    else:
        st.session_state.image, st.session_state.pokechamp_names = poke.get_pokechamp()
    # st.session_state.image = poke.get_question()
    left_column.image(st.session_state.image, use_column_width=True)
    playsound("sounds\whoisthat.wav")

if left_column.button("Result"):
    poke = st.session_state.pokemon
    #poke = Pokemon(url="https://pokeapi.co/api/v2/pokemon/", background_path="whos_that_poke.png", id=st.session_state.pokemon_id)

    st.session_state.result = True
    st.session_state.image = poke.get_solution()
    
    left_column.image(st.session_state.image, caption=st.session_state.pokemon_name)
    playsound("sounds\its.wav")
    playsound("sounds\clefairy.wav")



if right_column.button("Hint"):
    #if st.session_state.next & st.session_state.result:
    poke = st.session_state.pokemon
    left_column.image(st.session_state.image, use_column_width=True)
    right_column.write(f"The Pokémon weighs: {poke.get_weight()}kg")
    
        # poke = Pokemon(url="https://pokeapi.co/api/v2/pokemon/", background_path="whos_that_poke.png", id=st.session_state.pokemon_id)
        # mp3_cry = poke.cry_wav()
        # playsound(str(mp3_cry))
        # remove_oggs()
        
if outer_right_column.button("Hint 2"):
    #if st.session_state.next & st.session_state.result:
    poke = st.session_state.pokemon
    left_column.image(st.session_state.image, use_column_width=True)
    right_column.write(f"The Pokémon weighs: {poke.get_weight()}kg")
    outer_right_column.write(f"The Pokémon(s) types are:")
    outer_right_column.write(f"1st type: {poke.type}")
    outer_right_column.write(f"2nd type: {poke.get_second_type()}")
        
        # poke = Pokemon(url="https://pokeapi.co/api/v2/pokemon/", background_path="whos_that_poke.png", id=st.session_state.pokemon_id)
        # mp3_cry = poke.cry_wav()
        # playsound(str(mp3_cry))
        # remove_oggs()
        
    # if st.session_state.next &  st.session_state.result == False:
    #     poke = st.session_state.pokemon
    #     left_column.image(st.session_state.next_image, use_column_width=True)
    #     right_column.write(f"The Pokémon weighs: {poke.get_weight()}kg")
    #     # poke = Pokemon(url="https://pokeapi.co/api/v2/pokemon/", background_path="whos_that_poke.png", id=st.session_state.pokemon_id)
    #     # mp3_cry = poke.cry_wav()
    #     # playsound(str(mp3_cry))
    #     # remove_oggs()