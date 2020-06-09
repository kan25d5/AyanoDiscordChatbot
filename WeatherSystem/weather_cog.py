import discord
from discord.ext import commands


class WeatherCog(commands.Cog):
    def __init__(self, bot, system):
        self.bot = bot
        self.system = system

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        print("------------")
        print("input")
        print(message.content)

        if message.author.bot:
            print("utterance myself")
            print("------------")
            return

        mentions = [mention.id for mention in message.mentions]
        if self.bot.user.id not in mentions:
            print("not mention")
            print("------------")
            return

        channel = message.channel
        text = message.content
        out = self.system.reply(text)

        print("user da", self.system.user_da)
        print("sys da", self.system.sys_da)
        print("frame", self.system.frame)
        print("now frame", self.system.now_frame)

        if out:
            print("out", out)
            await channel.send(out)


def setup(bot):
    bot.add_cog(WeatherCog(bot))
