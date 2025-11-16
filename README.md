# WatchTower

## Tracks and Alerts the clients about the devices up time.

## Docker

docker build -t watchtower:1.0 . --debug

docker tag watchtower:1.0 jayantrane/watchtower:1.0

docker push jayantrane/watchtower:1.0

docker run --name running  --env-file .env watchtower:1.0 

curl -s -X POST "https://api.telegram.org/<token>/sendMessage" -d chat_id=<id> -d text="Hello, from the bot"