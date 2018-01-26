#!/bin/bash
echo "You may need an internet connection to set up your google cloud account"
cd ~/
curl https://sdk.cloud.google.com | bash
./google-cloud-sdk/install.sh
gcloud init
gcloud components install beta
echo "For installing python packages you have enter root password"
sudo pip3 install --upgrade google-cloud-vision
sudo pip3 install --upgrade google-cloud-speech
sudo pip3 install --upgrade google-cloud-translate
sudo pip3 install --upgrade google_speech
