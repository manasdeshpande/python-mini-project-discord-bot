import discord

from discord.ext import commands

import openai


class chatgpt1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='chat')
    async def chat(self, ctx, *, args):
        user_query = ctx.message.content
        openai_api_key = "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"
        response = openai.Completion.create(api_key=f'{openai_api_key}',
                                            model="text-davinci-003",
                                            prompt=user_query,
                                            temperature=0.5,
                                            max_tokens=500,
                                            top_p=0.3,
                                            frequency_penalty=0.5,
                                            presence_penalty=0.0)
        response_v = content = response['choices'][0]['text'].replace(str(user_query), "")
        embed = discord.Embed(title='AI Response', description=f"{response_v}")
        embed.set_footer(text='Made with OpenAI')
        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(chatgpt1(bot))
