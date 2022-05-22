from discord.ext import commands;import requests, discord, json
with open("config.json", "r") as f: config = json.load(f);feather_key=config["feather_key"];token=config["token"];intents = discord.Intents.default(); intents.members = True; intents.message_content = True; bot = commands.Bot(command_prefix="f!", help_command=None, intents=intents);bot.remove_command("help")
@bot.command()
async def help(ctx):embed=discord.Embed(title="Feather Invite bot");embed.add_field(name="f!invite", value="Invite a player to Feather client", inline=False);await ctx.reply(embed=embed)
@bot.event
async def on_command(ctx): print(f"{ctx.message.author} used {ctx.message.content} in \"{ctx.guild}\" | {ctx.guild.id}")
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandOnCooldown): em = discord.Embed(title=f"Feather Invite bot",description=f"Try again in {error.retry_after:.2f}s.", color=discord.Color.red()); await ctx.reply(embed=em)
    elif isinstance(error, commands.errors.MissingRequiredArgument): embed = discord.Embed(title="Feather Invite bot", description="Missing the IGN", color=discord.Color.red()); await ctx.reply(embed=embed)
    elif isinstance(error, commands.errors.CommandNotFound): await ctx.reply(embed=discord.Embed(description=f"Command is not a thing!", color=discord.Color.green()))
@bot.command(name="invite", description="Invites a player to Feather Client", aliases=["inv"])
@commands.cooldown(1, 30, commands.BucketType.user)
async def invite(ctx, ign):
    origionalmsg = await ctx.reply(embed=discord.Embed(title="Checking for {}".format(ign))); r = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{ign}",headers={"Host": "api.mojang.com", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none", "Sec-Fetch-User": "?1"})
    if r.status_code == 200:
        await origionalmsg.edit(embed=discord.Embed(title="Valid Mojang account")); d = r.json(); uuid = d['id']; uid1 = uuid[0:8]; uid2 = uuid[8:12]; uid3 = uuid[12:16]; uid4 = uuid[16:20]; uid5 = uuid[20:32]; uidset = uid1 + "-" + uid2 + "-" + uid3 + "-" + uid4 + "-" + uid5;sex = requests.post(f"https://wl.feathermc.com/invite/{uidset}", headers={"Host": "wl.feathermc.com","Connection": "keep-alive","Accept": "application/json, text/plain, */*","Authorization": feather_key,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) FeatherLauncher/1.2.1 Chrome/91.0.4472.164 Electron/13.1.9 Safari/537.36","Sec-Fetch-Site": "cross-site","Sec-Fetch-Mode": "cors","Sec-Fetch-Dest": "empty","Accept-Language": "en-US", "Accept-Encoding": "gzip, deflate","Content-Length": "0"})
        if sex.status_code == 200:print(f"{ign} has been whitelisted to feather!"); embed = discord.Embed(title=f"{ign} has been whitelisted to feather client!"); embed.add_field(name="Download:", value="https://feathermc.com/download/windows"); embed.set_footer(text="Made with <3 by qoft#0001"); await origionalmsg.edit(embed=embed)
        elif sex.status_code == 400:print(f"{ign} was already whitelisted to feather!");embed = discord.Embed(title=f"{ign} is already whitelisted!");embed.add_field(name="Download:", value="https://feathermc.com/download/windows");embed.set_footer(text="Made with <3 by qoft#0001");await origionalmsg.edit(embed=embed)
        elif sex.status_code == 401:await ctx.send("<@961331484214587403> REFRESH THE TOKEN");embed = discord.Embed(title=f"Wait for qoft to refresh the token");embed.set_footer(text="Made with <3 by qoft#0001");await origionalmsg.edit(embed=embed)
    else: print(f"{ign} is not valid!"); embed = discord.Embed(title=f"{ign} is not a valid minecraft account!"); embed.set_footer(text="Made with <3 by qoft#0001"); await origionalmsg.edit(embed=embed)
@bot.event
async def on_ready(): print(f"Logged in as {bot.user}");await bot.change_presence(activity=discord.Game(name="with my heart"))
bot.run(token)