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
            if system.cogs is None:
                continue
            for cog in system.cogs:
                self.add_cog(cog(self))

    async def on_ready(self):
        print("-----")
        print(self.user.name)
        print(self.user.id)
        print("-----")

    async def on_message(self, message: discord.Message):
        print("input")
        print(message.content)

        if message.author.bot:
            print("utterance myself")
            return
        if self.user.id in message.mentions:
            print("not mention")
            return

        channel = message.channel
        text = message.content
        out = None

        # 対話システムの応答
        for system in self.dialog_systems:
            out = system.reply(text)
            if out:
                out = message.author.mention + " " + out
                await channel.send(out)
                print("output")
                print(out)
                print("-------")
                return
