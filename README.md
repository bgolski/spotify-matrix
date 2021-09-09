# Spotipi

## Overview
A personal project utilizing the Spotify API and a Raspberry Pi to display the song information of the currently playing song on the user's Spotify account. 

## Setup
- First, follow the instructions in [this repository](https://github.com/hzeller/rpi-rgb-led-matrix) to set up the wiring and the configuration for your RGB matrix. 
- Next, set up a [Spotify Developer Account](https://developer.spotify.com/) and create a new application. Take note of your Client ID, Client Secret, and Redirect URIs as they will need to be entered later. 
- Finally, run the following script to finish setup: 

    ```sudo bash setup/setup.sh```

    Enter the information for your Spotify Developer account when prompted to do so. 

## To Run
- Enter the python directory

    ```cd python```

- Run the main Python script using the command below, replacing {YOUR-SPOTIFY-ACCOUNT} with your username: 
    
    ```sudo python3 main.py {YOUR-SPOTIFY-ACCOUNT}```

