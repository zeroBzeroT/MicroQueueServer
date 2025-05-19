# MicroQueueServer

[![discord](https://img.shields.io/discord/895546064260718622?logo=discord)](https://discord.0b0t.org)
[![reddit](https://img.shields.io/reddit/subreddit-subscribers/0b0t)](https://old.reddit.com/r/0b0t/)

Simple minecraft server based on a stonewall to provide a "parking space" for the player until a space becomes available on the main server.
---
# Usage
To install run
```powershell
pip install requirements.txt
```

Then to run the program run
```powershell
python queueserver.py
```

Availble arguments:
* --max / -m | Maximum amount of players (usage: python queueserver.py -m 10)
* --host / -a | Adress to listen on (usage: python queueserver.py -a 0.0.0.0)
* --port / -p | Port to listen on (usage: python queueserver.py -p 12345)
