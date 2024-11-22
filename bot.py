import discord, audioop, random, asyncio, traceback
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


bot = commands.Bot(command_prefix='-', intents=intents)
token = ""

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, I am {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def add(ctx, left: int, right: int):
    await ctx.send(left + right)

@bot.command()
async def subtract(ctx, left: int, right: int):
    await ctx.send(left - right)

@bot.command()
async def multiply(ctx, left: int, right: int):
    await ctx.send(left * right)

@bot.command()
async def divide(ctx, left: int, right: int):
    await ctx.send(left / right)

@bot.command()
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

@bot.command()
async def choose(ctx, *choices: str):
    await ctx.send(random.choice(choices))

@bot.command()
async def userinfo(ctx: commands.Context, user: discord.User):
    user_id = user.id
    username = user.name
    avatar = user.display_avatar.url
    await ctx.send(f'User found: {user_id} -- {username}\n{avatar}')

@userinfo.error
async def userinfo_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.BadArgument):
        return await ctx.send('Couldn\'t find that user.')
    else:
        traceback.print_exception(type(error), error, error.__traceback__)

@bot.command()
async def guess(ctx):
    await ctx.send('Guess a number between 1 and 10.')
    def is_correct(m):
        return m.author == ctx.author and m.content.isdigit()
    answer = random.randint(1, 10)
    try:
        guess = await bot.wait_for('message', check=is_correct, timeout=5.0)
    except asyncio.TimeoutError:
        return await ctx.send(f'Sorry, you took too long! It was {answer}.')
    if int(guess.content) == answer:
        await ctx.send('You are right!')
    else:
        await ctx.send(f'Oops. It was actually {answer}.')

@bot.command()
async def commands(ctx):
    await ctx.send("Current bot commands (you must put - before every command without any space, example: -heh 4): hello, heh + (num), add + (num) + (num), subtract + (num) + (num), multiply + (num) + (num), divide + (num) + (num), roll (wip, doesn't work like we want it to), choose + (option 1) + (option 2), userinfo + (display name), guess, commands")
                
bot.run(token)
