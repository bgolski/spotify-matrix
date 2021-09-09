#!/bin/bash

echo "Beginning install..."

echo "Setting Spotify Secrets..."

echo "Enter Spotify Client ID: "
read SPOTIPY_CLIENT_ID
echo "Enter Spotify Client Secret: "
read SPOTIPY_CLIENT_SECRET
echo "Enter Spotify Redirect URI: "
read SPOTIPY_REDIRECT_URI

echo "Environment=\"SPOTIPY_CLIENT_ID=${SPOTIPY_CLIENT_ID}\"" >> "../environment/$SPOTIPY_CLIENT_ID"
echo "Environment=\"SPOTIPY_CLIENT_SECRET=${SPOTIPY_CLIENT_SECRET}\"" >> "../environment/$SPOTIPY_CLIENT_SECRET"
echo "Environment=\"SPOTIPY_REDIRECT_URI=${SPOTIPY_REDIRECT_URI}\"" >> "../environment/$SPOTIPY_REDIRECT_URI"

echo "Installing Python requirements..."
pip3 install -r requirements.txt

echo "Setup complete!"

exit 0