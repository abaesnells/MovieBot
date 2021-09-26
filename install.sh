#!/bin/bash

echo "Installing MovieBot dependencies..."

sudo apt-get update
sudo apt-get upgrade

sudo apt -y install python3-pip python3-cffi
sudo pip3 install discord.py[voice]
sudo pip3 python-dotenv


echo "Creating Movie Catalog Files" 
sudo touch movies.txt
sudo touch watched.txt


echo "Setting up MovieBot service..."
cd install
sudo cp moviebot.service /etc/systemd/system
sudo chmod 755 /etc/systemd/system/moviebot.service
sudo chown root:root /etc/systemd/system/moviebot.service
sudo systemctl enable moviebot.service
sudo systemctl restart vwebserver
cd -


echo "Completed MovieBot Installation!"
