import os
from twitchio.ext import commands

# Load environment variables
CHANNEL = os.getenv("TWITCH_CHANNEL")
BOT_NICK = os.getenv("BOT_USERNAME")
TOKEN = os.getenv("TWITCH_OAUTH_TOKEN")

# Simple in-memory queue
queue = []

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=TOKEN, prefix='!', initial_channels=[CHANNEL])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        await self.handle_commands(message)

    @commands.command(name='join')
    async def join(self, ctx):
        user = ctx.author.name
        if user in queue:
            await ctx.send(f"{user}, you're already in the queue!")
        else:
            queue.append(user)
            await ctx.send(f"{user} joined the queue! Position: {len(queue)}")

    @commands.command(name='leave')
    async def leave(self, ctx):
        user = ctx.author.name
        if user in queue:
            queue.remove(user)
            await ctx.send(f"{user} has left the queue.")
        else:
            await ctx.send(f"{user}, you are not in the queue.")

@commands.command(name='queue')
async def show_queue(self, ctx):
    if queue:
        shown = ', '.join(queue[:10])
        msg = f"Queue (in order): {shown}"
        if len(queue) > 10:
            msg += f" ...and {len(queue) - 10} more"
        await ctx.send(msg)
    else:
        await ctx.send("The queue is currently empty.")
    

    @commands.command(name='position')
    async def position(self, ctx):
        user = ctx.author.name
        if user in queue:
            pos = queue.index(user) + 1
            await ctx.send(f"{user}, your position in the queue is {pos}.")
        else:
            await ctx.send(f"{user}, you are not in the queue.")

    @commands.command(name='next')
    async def next(self, ctx):
        if ctx.author.is_mod:
            if queue:
                user = queue.pop(0)
                await ctx.send(f"Next up: {user}")
            else:
                await ctx.send("The queue is empty.")
        else:
            await ctx.send("Only mods can use this command.")

    @commands.command(name='clearqueue')
    async def clear_queue(self, ctx):
        if ctx.author.is_mod:
            queue.clear()
            await ctx.send("Queue cleared.")
        else:
            await ctx.send("Only mods can use this command.")

bot = Bot()
bot.run()
