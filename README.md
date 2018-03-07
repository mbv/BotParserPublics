# BotParserPublics

The script receives data from the wall of users / communities / public from VK and sends them to the channel in a Telegram.

Text from the source post is added to the top of the picture.

## Requirements

* Python 3.5

## Installation
    cd project_folder
    virtualenv bpp
    
    source bpp/bin/activate
    pip install -r requirements.txt
    
Need to add the launch of `run.sh` in cron

## Configuration
    cp config.yaml.example config.yaml


config.yaml:
    
    access_token: <user or application access token that has access to the wall >
    last_date: 0
    wall_id: <wall id, if it is user wall use "user_id", if it is public wall use "-public_id" >
    telegram_token: <Bot token, you can get it from @BotFather >
    telegram_chat_id: '@<Channel for sending posts, bot must be admin>'


Filled example(config.yaml):

    access_token: abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0
    last_date: 0
    owner_id: -12345678
    telegram_chat_id: '@mychannel'
    telegram_token: 123456789:AABBCCDDEEFF00112233445566778899AA0
