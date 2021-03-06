# A Discord selfbot with various commands

A selfbot that has various in-built commands as well as the ability to dynamically add commands using the ``>add`` command on discord.

1. [Features](#features)
2. [Setup](#setup)
3. [Running the Selfbot](#running-the-selfbot)
5. [Custom Commands](#custom-commands)
6. [Keyword Logger](#keyword-logger)
7. [Save Chat Messages](#save-chat-messages)
8. [Google API](#google-api)
9. [Other Things to Note](#other-things-to-note)

## Features

- Google web and image search.
- Keyword/mention logger. Log messages and/or get notified when keywords you specified are said in any of your servers. Useful to track if someone mentioned your name or your favorite show/book/whatever else keywords and you want to stalk— I mean, talk to them about it.
- Set your game to anything or set up multiple and cycle through them.
- Add custom commands/reactions. The commands get saved to ``commands.json`` which has some sample commands added to start with.
- Smart MyAnimeList search of anime and manga/LNs using google custom search (and if that fails, using myanimelist's api for search)
- Python interpreter. Modeled off of RoboDanny's ?debug command. Does both exec() and eval(). Ability to save and load scripts.
- Save/output the last n number of messages from a chat, including any messages that were deleted.
- Get detailed information about a server and all of its members.
- Set yourself as afk and reply to a user telling them you are away if they message/mention you. (note: frowned upon by Discord so not for practical use; meant to be used as a joke)
- Quick commands so you can post pointless stuff as fast as possible like ``lenny``, ``shrug``, ``flip``, ``unflip``, and ``comeatmebro``
- Purge the last n messages you sent in a channel.
- Simple calculator.
- Various other misc commands like spoiler tagging text (encrypts the text), creating strawpolls, embeding text, server/user info commands, and more.

## Setup

Start off by setting up the ``config.json`` file in the ``settings`` folder:

```json
{
	"my_id" : "",
	"token" : "",
	"google_api_key" : "",
    "custom_search_engine" : "",
	"mal_username" : "",
    "mal_password" : "",
	"set_afk" : "off",
	"afk_message" : "",
	"cmd_prefix": ">",
	"customcmd_prefix": ".",
	"bot_identifier": ":robot:"
}
```
The Google API, custom search engine, and MAL info are **not** necessary in order to get the bot running. However, they provide some very nice features like MAL search and google image search so do fill them in if you want to use the bot to its full potential.


- ``my_id`` - your discord ID. On Discord go to settings > Appearance and Enable Developer Mode. Right-click yourself on the sidebar or chat and click copy ID to get your ID.
- ``token`` - token obtained from ``localStorage.token`` On Discord do ``Ctrl + Shift + i`` for Windows or ``Cmd + Shift + i`` on Mac and then [go here to get your token.](https://i.imgur.com/h3g9uf6.png) Don't give this out to anyone!
- ``google_api_key`` and ``custom_search_engine`` need to be obtained from Google. See the [Google API](#google-api) section below for instructions.
- ``mal_username`` and ``mal_password`` - MyAnimeList username and password which is required in order to do a MAL search. This is required in order to use the MAL API to grab anime/manga information and is not used for anything else. A normal MAL account will suffice.
- ``set_afk`` - does not need to be changed. It defaults to ``off`` and can be changed through Discord by doing ``>setafk on`` or ``>setafk off``. Warning: As mentioned, this is not something Discord wants selfbots to do. More of a joke than anything.
- ``afk_message`` - the message that is sent when ``set_afk`` is enabled and someone pings you in a channel. This can be edited through Discord with the ``>setafkmsg`` cmd.
- ``cmd_prefix`` and ``customcmd_prefix`` - the prefix for in-built commands and custom commands respectively. Prefixes longer than one character are not supported. You may set the same prefix for both but be careful not to make a custom cmd with the same name as in in-built.
- ``bot_identifier`` - a word/message/emote the bot will add to the beginning of every message it sends (except embeds and replies to quick cmds). Make it empty if you don't want one.

## Running the selfbot

Note: You must have Python 3.5.2 or above installed. **When installing python, make sure you check "Add Python to PATH" in the install window.**

**Windows:** Double click ``run.bat`` to start the bot. If everything in the config is setup properly you should login fine. If you have a weak internet connection, the bot could take several minutes to log in.

**Mac/Linux:** Navigate to the bot's folder in terminal/shell and run: ``pip install -r requirements.txt`` Once it's finished, run: ``python loopself.py`` to start the bot.

**Updating the bot:**

Unless otherwise stated, all you need to do is save your ``settings`` folder and its contents, delete everything else, download the newest version, and then replace the ``settings`` folder with your ``settings`` folder.

## All Commands:
- ``>restart`` - restart the bot.
- ``>game <text>`` or ``>game <text1> | <text2> | <text3> | ...`` - Set your game. If multiple are given, it will cycle through them. The game won't show for yourself but other people can see it.
- ``>stats`` - Bot stats and some user info. Includes information such as uptime, messages sent and received across servers (since the bot started) and some other info. What it looks like:

![img](http://i.imgur.com/x7aEacJ.png)

**Custom Commands**

- ``>customcmds`` or ``>customcmds long`` - List all custom commands. The long version is more detailed (shows all the replies for each cmd as well). A sample custom command that outputs a picture:

![img](http://i.imgur.com/gBoKnjQ.png)
- ``>add <command> <response>`` or ``>add <command> <response_name> <response>`` - Add a custom command.
- ``>remove <command>`` or ``>remove <command> <response_name>`` - Remove a custom command.

See the [Custom Commands](#custom-commands) section for more info on how to invoke commands and set up multiple responses to the same command.

**Google web and image search commands**

- ``>g <tags>`` - Google search. Depending on the type of result, certain google cards can be parsed. Some results:

![img](http://i.imgur.com/xaqzej9.png?2)
![img](http://i.imgur.com/6isT5T0.png)
![img](http://i.imgur.com/0AzT1Ah.png)
- ``>i <tags>`` - Google image search. ``>i <n> <tags>`` gives the nth result. An image search result:

![img](http://i.imgur.com/neisYXe.png)

**Logging commands**

- ``>log`` - See what, where, and how you are logging/tracking. See the [Keyword Logger](#keyword-logger) section below for more commands used for keyword logging. A logged message:

![img](http://i.imgur.com/4I8B2IW.png)
- ``>log history <n>`` or ``>log history save <n>`` - Output/save the last ``<n>`` number of messages from the chat you just used the command in, including deleted messages. See [Save Chat Messages](#save-chat-messages) section for more details.


**MyAnimeList commands**

- ``>mal anime <tags>`` or ``>mal manga <tags>`` - Searches MyAnimeList for specified entry. Use ``manga`` for light novels as well.
- ``>mal anime [link] <tags>`` or ``>mal manga [link] <tags>`` - Just gets the link to the MAL page instead of the full info.

A MAL search result:

![img](http://i.imgur.com/NmqmzdM.png)

**Server commands**

- ``>server`` or ``>server <name of server>`` - Get various information about the server. What it looks like:

![img](http://i.imgur.com/gPF7K73.png)
- ``>server role <name of role>`` - Get info about said role.
- ``>server members`` - Uploads a txt file containing detailed information about every member on the server including join date, account created, color, top role, and more.
- ``>server avi`` or ``>server avi <name of server>`` - Gets the server image.
- ``>server emojis`` - Lists all the custom emojis for the current server.

**Python Interpreter**

- ``>py <code>`` - python interpreter. Similiar to RoboDanny's ?debug command. Works with exec and eval statements. Also has the ``>load <module>`` ``>unload <module>`` and ``>reload`` cmds to load, unload, and reload modules.
- ``>py save <filename>`` ``>py run <filename>`` ``>py list`` ``>py view <filename>`` ``>py delete <filename>`` - Save/run/delete/view the contents of scripts. ``>py save <filename>`` saves the last ``>py <code>`` you did into a file. ``>py list`` or ``>py list <page_number>`` lets you see the list of scripts you have saved.

Example usage of the python interpreter:

![img](http://i.imgur.com/MpAtJ7W.png)

![img](http://i.imgur.com/PF0inrv.png)

![img](http://i.imgur.com/gYUmyHC.png)

**Misc**

- ``>about`` - link to this github project
- ``>poll <title> = <Option 1> | <Option 2> | ...`` - Create a strawpoll.
- ``>spoiler <word> <some spoilers>`` or ``>spoiler <words> | <some spoiler>`` - Encrypt the spoiler and provides a link to decode it using ROT13. Basically spoiler tagging a message. Ex: ``>spoiler Book He lives`` or ``>spoiler Some movie | He was his brother all along``
- ``>calc`` - calculator. Ex: ``>calc 44 * (45-15)``
- ``>choose <Option 1> | <Option 2> | ...`` - Randomly chooses one of the given options.
- ``>d`` or ``>d <n>`` - Remove the last message or last n messages you sent (along with this one). ``>d !<n>`` will wait ``<n>`` seconds before deleting the message. It will also repeatedly edit the message and count down the seconds and show a little animation. Very stupid, very unnecessary, and it abuses the rate-limit...but it's pretty funny to see people's reactions. :P
- ``>info`` or ``>info <user>`` - See various discord info about yourself or a specified user. Also, ``>info avi`` or ``>info avi <user>`` to see a bigger verion of the users profile picture.

![img](http://i.imgur.com/n4mSRyD.png)
- ``>ping`` - Responds with ``pong`` and also gives the response time.
- ``>emoji <emoji>`` - Gets the image url for the specified emoji.
- ``>quote`` or ``>quote <words>`` - Quotes the last message in the channel if no words are given or finds the message (if it wasn't too long ago) with the given words and quotes that. Deleted messages can be quoted.
- ``>embed <words>`` - Make an embed out of the message.
- ``>l2g <tags>`` - Gives a https://googleitfor.me link with the specified tags for when you want to be a smartass.
- ``>setafk on`` or ``>setafk off`` - Turn the afk message trigger on or off.
- ``>setafkmsg <msg>`` - Set the afk message.

## Custom Commands:
**There are two ways to add custom commands.** The first way:

- ``>add <command> <response>`` Now, if you do ``.<command>`` you will receive ``<response>``.

Example: ``>add nervous http://i.imgur.com/K9gMjWo.gifv`` Then, doing ``.nervous`` will output this imgur link (images and gifs will auto embed)

However, **you may want to add multiple responses to the same command.** So the second way:

- ``>add <command> <response_name> <response>``. This way, you can add multiple responses to the same command.

Example: ``>add kaguya present http://i.imgur.com/7Px7EZx.png`` then you can add another to the ``.kaguya`` command: ``>add kaguya yes http://i.imgur.com/y0yAp1j.png``.

Invoke a specific response with ``.<command> <response_name>`` or get a random response for that command with ``.<command>``


**Removing commands:**
- ``>remove <command>`` or ``>remove <command> <response_name>`` if you want to remove a specific response for a command.

**Adding/removing commands/responses with multiple words:** 

If anything you are adding/removing is more than one word, **you must put each part in quotes**. Example: ``>add "kaguya" "how cute" "http://i.imgur.com/LtdE1zW.jpg"`` or ``>add "copypasta" "I identify as an attack helicopter."``

## Keyword Logger

The Keyword logger can be used for mentions (just like the recent mentions tab on discord) and also for any keywords you want. Here is another example of what it looks like when the bot finds a message with the specified keyword:

![img](http://i.imgur.com/TIqzsf0.png)

As you can see, it shows the context, the keyword it matched, time message was sent, server, channel, and the names of the users in the context.

So, here's how you get started with setting up the logger:

1. Make a channel where you want to receive these log messages. You can set it to be anwhere you want really, but if you don't want anyone else to read/send messages where it logs, create a server for just yourself and use a channel there.
2. In this channel, do ``>log location`` to set the log location to this channel. Now do ``>log`` and you should see that ``Log location:`` is set to this current channel in this server.
3. Add the keywords you want to log. ``>log addkey <word>`` Each key can be more than one word and case does not matter. Removing is just ``>log removekey <word>``. If you want to add mentions to the keywords, just tag yourself or the specified user as if you were mentioning them. When you view the keywords with ``>log``, the mentions will look like \<@1287683643986> or something but that's fine.
4. Add the servers you want to log or set it to log all servers. Go to a server and in any channel, do ``>log add`` to let the logger check that server for keywords. Do ``>log remove`` to remove the server you are in from the logger. If you want to set to all servers, do ``>log toggle``. Do it again to toggle back to only the specified servers.
5. Set the context length. This is the number of messages to show in the log message. The default is set to 4 (this is 4 messages before keyword message + the keyword message). Set it with ``>log context <number>``. You can go up to 20 messages.
6. Add users, words, or servers to the blacklist. These won't trigger the keyword logger even if a match is made. The syntax is: ``>log addblacklist [user] <user>`` or ``>log addblacklist [word] <word>`` or ``>log addblacklist [server]`` When blacklisting users, ``<user>`` can be their name + discriminator, a mention, or their user id. Removing is more or less the same but with ``>log removeblacklist`` instead.

Note: You can blacklist a word only for a certain server by doing ``>log addblacklist [word] [here] <word>``. For example, if you have ``overwatch`` as a keyword but you don't want to log it if it was said in the Overwatch Discord server, you go to the Overwatch server and in any channel, type ``>log addblacklist [word] [here] overwatch``. Removing is the same: ``>log removeblacklist [word] [here] overwatch``.

**Setting up a notifier for the keyword logger**

When keywords get logged, the bot doesn't notify you. This is because the bot is running on your account. Just like you can't ping and notify yourself, the bot can't either. However, it is possible to recieve notifications through a second bot account. The setup is easy:

1. Create a Discord bot account and get the bot's token. Then add the bot to the server where you are logging. [Follow these quick steps.](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)
2. Make sure to give the bot read, send, edit messages, and embed permissions in the channel you are keyword logging in.
3. Do ``>notify token <token>`` where ``<token>`` is the token you grabbed in step 1. Make sure you grabbed the **token** not the client secret!
4. Enable the notifier bot with ``>notify on``. You should see the bot you created come online on the sidebar. ``>notify off`` to disabled the notifier bot.
5. Set how to get notifications. ``>notify ping`` - get pinged when a keyword gets logged. ``>notify dm`` - the bot direct messages you the log. ``>notify none`` - posts in the keyword logger channel (no ping).

**Why would I need to blacklist words/servers?**

It's just for convenience. If you have 50+ servers and only a handful that you don't want to log, it would be a hastle to add every one to the ``servers`` list so instead you can just enable all servers and add the few to the blacklist. For words being blacklisted, this is just to allow you to specify more in-depth what kind of messages you are trying to look for with the keyword logger.

**Note:**

1. Only other people can trigger the log message. You yourself saying a keyword won't log the message. The channel the keyword logger is logging in is exempt from the keyword search as well.
2. If the logged message + context is too long, the log message will be split up into multiple messages. These mutiple messages don't use embeds so it won't look as neat, sadly. This shouldn't happen often though.

That should be it. Check your settings any time with ``>log``.

## Save Chat Messages

You can only save chat messages in the servers you are logging (see [Keyword Logger](#keyword-logger) section above). Use ``>log`` to see what servers are being logged. Every channel in the enabled servers (or every server if all servers is enabled) will have their messages added to logging. By default, the logger holds the latest 500 messages per channel. This value is determined by ``log_size`` in ``log.json`` under the ``settings`` folder. You can increase this value if you want; the upper limit is well over 500.
When you want to save some kind of memorable discussion/funny moment/important reminder or want to shame someone for a message they deleted or something, use the ``>log history`` command:

- ``>log history <n>`` outputs the last ``<n>`` number of messages from the chat you just used the command in. ``<n>`` can be as large as the ``log_size``. Increase ``log_size`` in ``log_json`` if you want more messages. A screencap of what it looks like:

![img](http://i.imgur.com/snAWT7C.png)
- ``>log history save <n>`` saves the messages to a file and uploads the file instead. This is useful when saving large number of messages. A screencap of what it looks like:

![img](http://i.imgur.com/MUwOhgp.png)

**Warning:** You probably want to stick with using ``save`` when grabbing large amounts of messages. Outputting walls of text by doing ``>log history 200`` might get you banned from most public servers.

## Google API

In order to use the ``>i`` command to image search and in order to get more accurate MyAnimeList search results, you will need a Google API key and a Custom Search Engine ID.

Follow these steps to obtain them:

1. Visit the [Google API Console](https://console.developers.google.com/). Once you are in the Console, create a new project.
2. Go to ``Library`` and search ``Custom Search API``. Click it and enable it.
3. Go to ``Credentials`` and click ``create credentials`` and choose ``API Key`` (no need to restrict the key). The value under "Key" is your api key. Paste this into the config.json under ``google_api_key``.
4. Go [here](https://cse.google.com/cse/all) and click ``Add`` and then ``Create`` (if asked to specify a site, just do www.google.com)
5. On the home page of the Custom Search webpage, click on the newly created search engine and change the ``Sites to Search`` option to ``Search the entire web but emphasize included sites``.
6. Make sure the ``Image search`` option is enabled and make sure to click the ``Update`` button at the bottom when you are done with the changes!
6. Go to ``Details`` section and click ``Search Engine ID`` to grab the ID. Copy this and add it for ``custom_search_engine`` in the config.json.

**Note:** Google may take a little while to properly register your key so the search feature may not work right away. If it's still not working after a few hours, then you may have messed up somewhere.

## Other Things to Note
- Free custom search has a limit of 100 searches per day. The commands ``>i`` and ``>mal`` use this search. Still, this should be more than enough but feel free to pay for more if you would like, although I don't think it's needed.
- Try not to keep ``setafk`` on for too long or use it too frequently. Technically, responding to someone else's ping with an automated response is not something Discord likes selfbots doing. I highly suggest this be used as a fun gimmick rather than for actual use all the time.
- Custom commands have a lot of other quirks and flexablility. Check the [Custom Commands](#custom-commands) section to see how you can do stuff like add more than one response for a command, get a random response for a command, add commands that have multiple words, etc.


## Acknowledgements

Used a lot of [Danny's](https://github.com/Rapptz) code for certain parts, especially parsing Google cards and the debugger. Also thanks to [IgneelDxD](https://github.com/IgneelDxD) for a lot of suggestions and fixes.