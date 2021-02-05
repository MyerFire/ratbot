from datetime import datetime
from urllib.parse import quote
from config import songs
import random

import discord
import discord.ext.commands as commands
from typing import Optional, Union

import asyncio
import aiohttp


def birthday_link(name):
    return f"https://itsyourbirthday.today/#{quote(name)}"


def now():
    return str(datetime.today().strftime("%d-%m-%Y %H:%M:%S"))


async def log(bot, msg: str):
    channel = bot.get_channel(762166605458964510)
    await channel.send(content=msg)


async def get_verse(verse):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://bible-api.com/{quote(verse)}") as resp:
            respuesta = await resp.json()
            return {
                "heading": respuesta["reference"],
                "text": respuesta["text"].replace("\n", "")
            }


class Fun(commands.Cog):
    """Miscellaneous drivellous commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["bM", "bm"])
    async def bM_meter(self, ctx, *, option: Optional[str]):
        """decides Based or Cringe"""
        option = option.replace("```", "Armenium") if option else "Your"
        random.seed(option.lower())
        bc_decision = random.choice(["Based", "Cringe"]) if option else "Cringe"
        punctuation_ending = random.choice([random.choice(("!", ".")) * x for x in range(1, 8)])

        await ctx.send(f"**{option}** are **{bc_decision}**{punctuation_ending}")
        await log(self.bot, "```"
                            f"{option}, {bc_decision}{punctuation_ending}   [{ctx.message.created_at}]"
                            "```")

    @commands.command(aliases=["time", "now", "EST", "est"])
    async def based_time(self, ctx):
        """Tells the Ernie Standard Time"""
        await ctx.send(f"it\'s {now()} in EST (Ernie Standard Time)")
        return

    @commands.command(aliases=["CC", "cc"])
    async def cringecount(self, ctx, iteration: int = 1):
        """\"Liking liking things is cringe is cringe\""""
        if iteration < 105:
            await ctx.channel.send("""Bro.... Liking {'"Liking ' * int}Things {'Is Cringe" ' * int}is Cringe....""")
        else:
            await ctx.channel.send("no")

    @commands.command(aliases=["bd"])
    async def birthday(self, ctx, recipient: Union[discord.Member, str], *, name: Optional[str]):
        if not isinstance(recipient, str) and not name:  # if the person is mentioned without additional name
            await ctx.channel.send(f"happy birthday {recipient.mention}! \n{birthday_link(recipient.display_name)}")
        elif not isinstance(recipient, str) and name:  # if the person is mentioned with name
            await ctx.channel.send(f"happy birthday {recipient.mention}! \n{birthday_link(name)}")
        elif isinstance(recipient, str) and not name:
            await ctx.channel.send(f"happy birthday {recipient}! \n{birthday_link(recipient)}")
        elif isinstance(recipient, str) and name:
            await ctx.channel.send(f"happy birthday {recipient}! \n{birthday_link(name)}")

    @commands.command(aliases=["song", "rs"])
    async def random_song(self, ctx):
        """Pulls a random song from the configuration file"""
        await ctx.channel.send(f"https://youtu.be/{random.choice(songs)}")

    @commands.command(aliases=["verse"])
    async def bible_verse(self, ctx, *, verse):
        verse = await get_verse(verse)
        embed = discord.Embed(title=verse["heading"], description=verse["text"],
                              url=f"https://www.biblegateway.com/passage/?search={quote(verse['heading'])}&version=KJV",
                              timestamp=ctx.message.created_at)
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
