"""
Gruszka Bot
-----------
A simple bot for fun and moderation.
"""
__author__ = "RobiPoire"

import asyncio
import json
import logging
import os
from logging.config import fileConfig

import discord
import yaml
from discord.ext import commands

# Load the logging configuration
with open("./database/logging_config.json", "r") as f:
    logging_config = json.load(f)

# Apply the configuration
logging.config.dictConfig(logging_config)


class Bot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.config = yaml.load(open("config.yml", "r"), Loader=yaml.FullLoader)

    async def on_ready(self) -> None:
        logging.info(f"Logged in as {self.user} ({self.user.id})")
        await self.sync()
        logging.info("Extensions synchronized")

    async def sync(self) -> None:
        self.tree.copy_global_to(guild=discord.Object(self.config["SERVER_OWNER"]))
        # self.tree.sync(guild=discord.Object(self.config["SERVER_OWNER"]))

    async def load(self):
        for file in os.listdir("./commands"):
            if file.endswith(".py"):
                logging.info(f"Loading {file[:-3]}")
                await self.load_extension(f"commands.{file[:-3]}")

    async def run_bot(self):
        await self.load()
        await self.start(self.config["TOKEN"])


bot = Bot(command_prefix=".", intents=discord.Intents.all())
asyncio.run(bot.run_bot())
