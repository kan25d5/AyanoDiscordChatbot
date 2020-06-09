import discord
from discord.ext import commands


class Ayano(commands.Bot):
    def __init__(self, dialog_systems, command_prefix):
        super().__init__(command_prefix=command_prefix)
        self.dialog_systems = dialog_systems
        self.__add_cogs()

    def __add_cogs(self):
        """dialog_systemsが持つコグを綾乃ちゃんに登録する"""
        for system in self.dialog_systems:
            if system.cog:
                self.add_cog(system.cog(self, system))

    async def on_ready(self):
        print("-----")
        print(self.user.name)
        print(self.user.id)
        print("-----")
