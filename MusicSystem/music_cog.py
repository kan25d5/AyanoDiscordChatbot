import json
import discord
import youtube_dl as ytl
from discord.ext import commands
import os


class MusicCog(commands.Cog):
    def __init__(self, bot, system):
        self.bot = bot
        self.system = system
        self.voice = None

    @commands.command()
    async def play(self, ctx: commands.Context):
        print("引数が足らない")
        return

    @commands.command()
    async def play(self, ctx: commands.Context, url: str):
        vc = ctx.author.voice

        if vc is None:
            print("ユーザーはVCにいない")
            return

        # 一時音源ファイルを削除
        if os.path.isfile("temp.mp3"):
            os.remove("temp.mp3")

        # 一時音源ファイルのダウンロード
        ydl = ytl.YoutubeDL({"format": "bestaudio/best", "outtmpl": "temp.mp3"})
        info_log = ydl.extract_info(url, download=True)

        # VC接続
        try:
            self.voice = await self.bot.get_channel(vc.channel.id).connect()
        except discord.errors.ClientException:
            print("Already connected to a voice channel.")

        # 曲のロード
        self.voice.play(discord.FFmpegPCMAudio("temp.mp3", executable="ffmpeg.exe"))
        self.voice.source = discord.PCMVolumeTransformer(self.voice.source)

        # 再生
        self.voice.is_playing()

    @commands.command()
    async def stop(self, ctx: commands.Context):
        vc = ctx.author.voice
        if vc is None:
            print("ユーザーはVCにいない")
            return
        if not self.voice.is_playing():
            print("プレイがない")
            return
        self.voice.stop()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        return


def setup(bot):
    bot.add_cog(MusicCog(bot))
