import discord
import gettext

from discord.ext import commands

t = gettext.translation('messages', './locale', languages=['ru'])
_ = t.gettext

PREFIX = '.'

client = commands.Bot(command_prefix=PREFIX)
client.remove_command('help')

embAdm = discord.Embed(title='Navigating commands',
                       color=discord.Color.dark_red())  # Color for administrator
emb = discord.Embed(title='Navigating commands',
                    color=discord.Color.gold())  # Color for users


@client.event
async def on_ready():
    print(_("Bot started!"))


# Command .help for administrator
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def helpAdmin(ctx):
    await ctx.channel.purge(limit=1)

    embAdm.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)

    embAdm.add_field(name='{}clearAdmin'.format(PREFIX),
                     value=_('Clearing the chat'))
    embAdm.add_field(name='{}kick'.format(PREFIX),
                     value=_('Kick the user'))

    await ctx.send(embed=embAdm)


# Command .help for users
@client.command(pass_context=True)
async def help(ctx):
    await ctx.channel.purge(limit=1)

    emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)

    emb.add_field(name='{}clear'.format(PREFIX),
                  value=_('Clearing the chat. For example .clear 3'))

    await ctx.send(embed=emb)


# Command .clearAdmin for administrator that clears the chat
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clearAdmin(ctx, amount=100):
    await ctx.channel.purge(limit=amount)


# Command .clear for all users that clears the chat
@client.command(pass_context=True)
async def clear(ctx, amount: int = None):
    if amount is not None:
        await ctx.channel.purge(limit=amount)
    else:
        await ctx.send(_("Enter the number of messages to delete! " +
                         "For example .clear 3"))


# Command .kick for administrator
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)

    await member.kick(reason=reason)


# Connect
token = open('token.txt', 'r').readline()

client.run(token)
