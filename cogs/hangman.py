from discord.ext import commands
import random


class hangman(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    words = ["python", "programming", "computer", "discord", "hangman"]

    # Function to start a new game
    def start_game(self):
        global word, guessed_letters, attempts
        word = random.choice(self.words)
        guessed_letters = []
        attempts = 6
        print("New game started. The word is:", word)

    def update_display(self):
        display_word = ""
        for letter in word:
            if letter in guessed_letters:
                display_word += letter + " "
            else:
                display_word += "_ "
        return "```" + display_word.strip() + "```"

    def game_over(self):
        if attempts == 0:
            return True
        elif "_" not in self.update_display():
            return True
        else:
            return False

    # Function to handle user input
    def handle_input(self, guess):
        global attempts
        if guess in guessed_letters:
            return "You already guessed that letter!"
        elif guess in word:
            guessed_letters.append(guess)
            if self.game_over():
                return "Congratulations, you won!"
            else:
                return self.update_display()
        else:
            attempts -= 1
            if self.game_over():
                return "Game over! The word was " + word
            else:
                return "Wrong guess! You have " + str(attempts) + " attempts left."

    # Discord bot command to start a new game
    @commands.command(name='hangman', brief='start the hangman game')
    async def hangman(self, ctx):
        self.start_game()
        await ctx.send("New game started. The word has " + str(len(word)) + " letters: " + self.update_display())

    # Discord bot command to handle user guesses
    @commands.command(aliases=['g'], brief='type !guess followed by a letter')
    async def guess(self, ctx, letter):
        response = self.handle_input(letter)
        await ctx.send(response)


async def setup(bot):
    await bot.add_cog(hangman(bot))
