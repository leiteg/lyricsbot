Lyrics Twitter Bot
================================================================================

A bot that posts one verse at a time to twitter.

How to use
--------------------------------------------------------------------------------

This bot uses `pipenv` for environment and dependency management. Install it
through your operating system package manager or follow the instructions
provided [here][1].

Clone the repository in the desired location and run `pipenv install` inside it
to create the virtual environment and install dependencies.

```bash
git clone https://github.com/leiteg/lyricsbot
cd lyricsbot
pipenv install
```

Now, create a file called `lyrics.txt` and put the lyrics you want the bot to
post here. Do **not** leave blank lines.

```
# lyrics.txt

This is the first verse
This is the second verse!
[chorus]
This is the end
```

Also, edit the file `config/lyricsbot-keys` and paste your [twitter app
tokens][2] there.

```
# config/lyricsbot-keys

CONSUMER_KEY="<paste here>"
CONSUMER_SECRET="<paste here>"
ACCESS_TOKEN="<paste here>"
ACCESS_TOKEN_SECRET="<paste here>"
```

In order for the bot to run every hour, we need to configure a [systemd][3]
service and a timer for that. I have provided skeletons in `config/`. First,
edit the file `config/lyricsbot.service` and change every occurence of
`/path/to/` to the correct location where you cloned the repository.

> Just to be sure, check the file `scripts/run-bot-once.sh` and make sure the
> path to `pipenv` executable is consistent with your installation.

Finally, create symlinks for the service and timer files in
`~/.config/systemd/user` and start enable both of them.

> Instead of using systemd, you can always use the good old [cron][4].

```bash
mkdir -p ~/.config/systemd/user
cd ~/.config/systemd/user

ln -s /path/to/lyricsbot/config/lyricsbot.service lyricsbot.service
ln -s /path/to/lyricsbot/config/lyricsbot.timer lyricsbot.timer

systemctl --user daemon-reload
systemctl --user enable lyricsbot.service
systemctl --user enable lyricsbot.timer
systemctl --user start lyricsbot.timer
```

[1]: https://pipenv.kennethreitz.org/
[2]: https://developer.twitter.com/apps
[3]: https://www.freedesktop.org/wiki/Software/systemd/
[4]: https://en.wikipedia.org/wiki/Cron
