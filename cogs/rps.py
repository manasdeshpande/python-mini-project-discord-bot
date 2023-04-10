from discord.ext import commands
import discord, random


class rps(commands.Cog):

    def init(self, bot):
        self.bot = bot

    @commands.command()
    async def rps(self, ctx, msg: str):
        c = ["rock", "paper", "scissors"]
        computer = random.choice(c)
        player = msg.lower()
        if player == computer:
            await ctx.send("Tie!")
        elif player == "rock":
            if computer == "paper":
                await ctx.send(
                    "You Lose! I picked {0} while you picked {1} and {0} covers {1}...".format(computer, player))
            else:
                await ctx.send(
                    "You won! I picked {1} and you picked {0} and {0} crushes {1}...".format(player, computer))
        elif player == "paper":
            if computer == "scissors":
                await ctx.send(
                    "You lose! I picked {0} while you picked {1} and {0} cut {1}...".format(computer, player))
            else:
                await ctx.send(
                    "You won! I picked {1} while you picked {0} and {0} covers {1}...".format(player, computer))
        elif player == "scissors":
            if computer == "rock":
                await ctx.send(
                    "You lose! I picked {0} and you picked {1} and {0} smashes {1}...".format(computer, player))
            else:
                await ctx.send("You won! I picked {1} and you picked {0} and {0} cut {1}... ".format(player, computer))
        else:
            await ctx.send("hmmm... Thats not a valid choice please check your spelling and try again")


async def setup(bot):
    await bot.add_cog(rps(bot))
