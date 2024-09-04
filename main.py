import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()


async def start_bot(token):
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} success connect!')

    @bot.command()
    async def dm(ctx, user_id: int, *, message):
        user = bot.get_user(user_id)
        if user:
            await ctx.send(f"How many times the message should be sent? {user}?")
            
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()
            
            try:
                response = await bot.wait_for('message', check=check, timeout=30)
                message_count = int(response.content)
                
                for _ in range(message_count):
                    await user.send(message)
                    
                await ctx.send(f'Successfully {message_count} message(s) to {user}!')
                
            except asyncio.TimeoutError:
                await ctx.send("Timeout. Process cancelled")
            
        else:
            await ctx.send("ID not found.")

    await bot.start(token)

async def main():
    with open('token.txt', 'r') as file:
        tokens = file.readlines()

    tokens = [token.strip() for token in tokens if token.strip()]

    await asyncio.gather(*(start_bot(token) for token in tokens))

if __name__ == "__main__":
    asyncio.run(main())

# !dm ID TEXT
