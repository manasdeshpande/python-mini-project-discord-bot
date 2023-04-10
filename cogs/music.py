import asyncio
import re
import urllib
import urllib.request
import discord
from discord.ext import commands
import youtube_dl
from urllib.parse import parse_qs


class music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.queue = []

    @commands.command(aliases=['j'], brief="used to add the bot to a voice channel")
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send('not in voice')
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command(brief="prints the voice channel the bot is currently in")
    async def printc(self, ctx):
        voice_client = ctx.voice_client
        if voice_client is None:
            await ctx.send("I am not currently in a voice channel.")
        else:
            channel = voice_client.channel
            await ctx.send(f"I am currently in the {channel.name} channel.")

    @commands.command(aliases=['dc'], brief="disconnects the bot from the voice channel")
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(name='playn', brief="plays a song by name")
    async def play_name(self, ctx, *, name):
        search_query = urllib.parse.quote(name)
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_query)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url = f"https://www.youtube.com/watch?v={video_ids[0]}"
        vc = ctx.voice_client
        await self.queue1(ctx, url)
        await asyncio.sleep(1)
        if vc is None or not vc.is_playing():
            await self.play(ctx)

    @commands.command(aliases=['q'], brief="adds a song to the queue")
    async def queue1(self, ctx, url):
        self.queue.append(url)
        await ctx.send(f"{url} has been added to the queue.")

    @commands.command(aliases=['p'], brief="plays the song")
    async def play(self, ctx):
        await self.join(ctx)
        while self.queue:
            url = self.queue.pop(0)
            ctx.voice_client.stop()
            YDL_OPTIONS = {'format': 'bestaudio'}
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                              'options': '-vn'}
            vc = ctx.voice_client
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                vc.play(source)
            while vc.is_playing():
                await asyncio.sleep(1)
        await ctx.send("Queue is empty.")

    @commands.command(aliases=['r'], brief="resumes the song ")
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.send('resume')

    @commands.command(brief="pauses the song")
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send('pause')

    @commands.command(brief="skips the current song and plays the next one in the queue")
    async def skip(self, ctx):
        vc = ctx.voice_client
        if vc is None or not vc.is_playing():
            await ctx.send("I am not currently playing anything.")
            return
        vc.stop()
        await self.play(ctx)


async def setup(bot):
    await bot.add_cog(music(bot))
