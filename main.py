from scripts.core import DiscordBot
from scripts.config import TOKEN

if __name__ == "__main__":
    bot = DiscordBot()
    bot.run(TOKEN)
