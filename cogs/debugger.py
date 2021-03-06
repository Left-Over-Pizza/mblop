import contextlib
import sys
import inspect
import os
import shutil
import appuselfbot
import glob
import math
import json
import gc
from discord.ext import commands
from io import StringIO

# Common imports that can be used by the debugger.
import datetime
import time
import traceback
import prettytable
import re
import io
import asyncio
import discord
import random
import subprocess
from bs4 import BeautifulSoup
import urllib
import requests

'''Module for the python interpreter as well as saving, loading, viewing, etc. the cmds/scripts ran with the interpreter.'''

# Used to get the output of exec()
@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

class Debugger:

    def __init__(self, bot):
        self.bot = bot

    # Posts code to hastebin and retrieves link.
    async def post_to_hastebin(self, string):
        '''Posts a string to hastebin.'''
        data = string.encode('utf-8')

        url = 'https://hastebin.com/documents'
        try:
            response = requests.post(url, data=data)
        except requests.exceptions.RequestException as e:
            return 'Error'

        try:
            return 'https://hastebin.com/{}'.format(response.json()['key'])
        except Exception as e:
            return 'Error'

    # Executes/evaluates code. Got the idea from RoboDanny bot by Rapptz. RoboDanny uses eval() but I use exec() to cover a wider scope of possible inputs.
    async def interpreter(self, env, code):
        if code.startswith('[m]'):
            code = code[3:].strip()
            code_block = False
        else:
            code_block = True
        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except SyntaxError:
            try:
                with stdoutIO() as s:
                    result = exec(code, env)
                    if inspect.isawaitable(result):
                        result = await result
                result = s.getvalue()
            except Exception as g:
                return appuselfbot.isBot + '```{}```'.format(type(g).__name__ + ': ' + str(g))

        except Exception as e:
            return appuselfbot.isBot + '```{}```'.format(type(e).__name__ + ': ' + str(e))

        if len(str(result)) > 1950:
            url = await self.post_to_hastebin(result)
            return appuselfbot.isBot + 'Large output. Posted to hastebin: %s' % url
        else:
            if code_block:
                return appuselfbot.isBot + '```py\n{}\n```'.format(result)
            else:
                return result

    @commands.group(pass_context=True)
    async def py(self, ctx):
        """Python interpreter. See the README for more info."""

        if ctx.invoked_subcommand is None:
            code = ctx.message.content[4:].strip('` ')

            env = {
                'bot': self.bot,
                'ctx': ctx,
                'message': ctx.message,
                'server': ctx.message.server,
                'channel': ctx.message.channel,
                'author': ctx.message.author
            }
            env.update(globals())

            result = await self.interpreter(env, code)

            os.chdir(os.getcwd())
            with open('%s/cogs/utils/temp.txt' % os.getcwd(), 'w') as temp:
                temp.write(ctx.message.content[4:])

            await self.bot.send_message(ctx.message.channel, result)

    # Save last >py cmd/script.
    @py.command(pass_context=True)
    async def save(self, ctx, *, msg):
        msg = msg.strip()[:-3] if msg.strip().endswith('.txt') else msg.strip()
        os.chdir(os.getcwd())
        if not os.path.exists('%s/cogs/utils/temp.txt' % os.getcwd()):
            return await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + 'Nothing to save. Run a ``>py`` cmd/script first.')
        if not os.path.isdir('%s/cogs/utils/save/' % os.getcwd()):
            os.makedirs('%s/cogs/utils/save/' % os.getcwd())
        if os.path.exists('%s/cogs/utils/save/%s.txt' % (os.getcwd(), msg)):
            await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + '``%s.txt`` already exists. Overwrite? ``y/n``.' % msg)
            reply = await self.bot.wait_for_message(author=ctx.message.author)
            if reply.content.lower().strip() != 'y':
                return await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + 'Cancelled.')
            if os.path.exists('%s/cogs/utils/save/%s.txt' % (os.getcwd(), msg)):
                os.remove('%s/cogs/utils/save/%s.txt' % (os.getcwd(), msg))

        try:
            shutil.move('%s/cogs/utils/temp.txt' % os.getcwd(), '%s/cogs/utils/save/%s.txt' % (os.getcwd(), msg))
            await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + 'Saved last run cmd/script as ``%s.txt``' % msg)
        except:
            await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + 'Error saving file as ``%s.txt``' % msg)

    # Load a cmd/script saved with the >save cmd
    @py.command(pass_context=True)
    async def run(self, ctx, *, msg):
        save_file = msg[:-3].strip() if msg.endswith('.txt') else msg.strip()
        if not os.path.exists('%s/cogs/utils/save/%s.txt' % (os.getcwd(), save_file)):
            return await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + 'Could not find file ``%s.txt``' % save_file)

        script = open('%s/cogs/utils/save/%s.txt' % (os.getcwd(), save_file)).read()

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'server': ctx.message.server,
            'channel': ctx.message.channel,
            'author': ctx.message.author
        }
        env.update(globals())

        result = await self.interpreter(env, script.strip('` '))

        await self.bot.send_message(ctx.message.channel, result)

    # List saved cmd/scripts
    @py.command(pass_context=True)
    async def list(self, ctx):
        os.chdir('%s/cogs/utils/save/' % os.getcwd())
        try:
            if ctx.message.content[8:]:
                numb = ctx.message.content[8:].strip()
                if numb.isdigit():
                    numb = int(numb)
                else:
                    await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + 'Invalid syntax. Ex: ``>py list 1``')
            else:
                numb = 1
            filelist = glob.glob('*.txt')
            if len(filelist) == 0:
                return await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + 'No saved cmd/scripts.')
            filelist.sort()
            msg = ''
            pages = math.ceil(len(filelist) / 10)
            if numb < 1:
                numb = 1
            elif numb > pages:
                numb = pages

            for i in range(10):
                try:
                    msg += filelist[i + (10 * (numb-1))] + '\n'
                except:
                    break

            await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + 'List of saved cmd/scripts. Page ``%s of %s`` ```%s```' % (numb, pages, msg))
        except Exception as e:
            await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + 'Error, something went wrong: ``%s``' % e)
        finally:
            os.chdir('..')
            os.chdir('..')
            os.chdir('..')

    # View a saved cmd/script
    @py.group(pass_context=True)
    async def view(self, ctx, *, msg: str):
        msg = msg.strip()[:-3] if msg.strip().endswith('.txt') else msg.strip()
        os.chdir('%s/cogs/utils/save/' % os.getcwd())
        try:
            if os.path.exists('%s.txt' % msg):
                f = open('%s.txt' % msg, 'r').read()
                await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + 'Viewing ``%s.txt``: ```%s```' % (msg, f.strip('` ')))
            else:
                await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + '``%s.txt`` does not exist.' % msg)

        except Exception as e:
            await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + 'Error, something went wrong: ``%s``' % e)
        finally:
            os.chdir('..')
            os.chdir('..')
            os.chdir('..')

    # Delete a saved cmd/script
    @py.group(pass_context=True)
    async def delete(self, ctx, *, msg: str):
        msg = msg.strip()[:-3] if msg.strip().endswith('.txt') else msg.strip()
        os.chdir('%s/cogs/utils/save/' % os.getcwd())
        try:
            if os.path.exists('%s.txt' % msg):
                os.remove('%s.txt' % msg)
                await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + 'Deleted ``%s.txt`` from saves.' % msg)
            else:
                await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + '``%s.txt`` does not exist.' % msg)
        except Exception as e:
            await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + 'Error, something went wrong: ``%s``' % e)
        finally:
            os.chdir('..')
            os.chdir('..')
            os.chdir('..')

    @commands.command(pass_context=True)
    async def load(self, ctx, *, msg):
        """Load a module"""
        try:
            self.bot.load_extension(msg)
        except Exception as e:
            await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + 'Failed to load module: `{}`'.format(msg))
            await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + '{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + 'Loaded module: `{}`'.format(msg))
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def unload(self, ctx, *, msg):
        """Unload a module"""
        try:
            self.bot.unload_extension(msg)
        except Exception as e:
            await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + 'Failed to unload module: `{}`'.format(msg))
            await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + '{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.send_message(ctx.message.channel, appuselfbot.isBot + 'Unloaded module: `{}`'.format(msg))
        await self.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(Debugger(bot))
