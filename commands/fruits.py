import discord
from discord import app_commands
from discord.ext import commands

from database.models.fruit import Fruit


def get_case_insensitive(dictionary, key, default_value=None):
    lower_case_dict = {k.lower(): v for k, v in dictionary.items()}
    return lower_case_dict.get(key.lower(), default_value)


class CmdFruits(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="randomfruit", description="Get a random fruit")
    async def random_fruit(self, interaction: discord.Interaction) -> None:
        rand_fruit = Fruit.get_random()
        fruit_name = rand_fruit.get_name()
        fruit_description = rand_fruit.get_description()
        embed = discord.Embed(title=fruit_name, description=fruit_description, color=0x71e21d)
        embed.set_image(url=rand_fruit.get_image())
        embed.set_author(name="RandomFruit")
        await interaction.response.send_message(embed=embed, ephemeral=False)

    @app_commands.command(name="fruit", description="Get a fruit by name")
    async def fruit(self, interaction: discord.Interaction, fruit_name: str = None) -> None:
        if not fruit_name:
            fruits_list = "\n".join(Fruit.get_all_names())
            embed = discord.Embed(title="Fruits", description=fruits_list, color=0x71e21d)
            embed.set_author(name="Fruit")
            await interaction.response.send_message(embed=embed, ephemeral=False)
        else:
            try:
                fruit = Fruit(fruit_name)
                fruit_description = fruit.get_description()
                embed = discord.Embed(title=fruit_name, description=fruit_description, color=0x71e21d)
                embed.set_author(name="Fruit")
                embed.set_image(url=fruit.get_image())
                await interaction.response.send_message(embed=embed, ephemeral=False)
            except ValueError as e:
                embed = discord.Embed(title="Error", description=str(e), color=0xff0000)
                embed.set_author(name="Fruit")
                await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CmdFruits(bot))
