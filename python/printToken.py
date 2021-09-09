import spotipy as spotipy
import spotipy.util as util


scope = 'user-read-currently-playing'

user_name = input("Enter spotify username: ")

token = spotipy.util.prompt_for_user_token(
    user_name, scope, redirect_uri='http:/127.0.0.1/callback:8080')

print(token)