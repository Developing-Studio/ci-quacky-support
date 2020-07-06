import discord, json, time, asyncio
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 2.0, BucketType.user)
    async def ping(self, ctx):
        """ Ping Pong! Check the Bot's Latency. """
        start = time.perf_counter()
        message = await ctx.send(f":ping_pong: Pong!\nHeartbeat :heart: {round(self.bot.latency * 1000)}ms")
        end = time.perf_counter()
        await message.edit(content=f"{message.content}\nEdit Message <:Edit_Feature:690660539373846549> {round((end - start) * 1000)}ms")

    @commands.command(aliases=['updaterank'])
    @commands.cooldown(1, 300.0, BucketType.user)
    async def rankupdate(self, ctx):
        """ Updates your Roles in the Quacky Support Server to Match your Quacky Badges. """
        guild = self.bot.get_guild(665378018310488065)
        member = guild.get_member(ctx.author.id)
        File = open('/root/Quacky/Files/badges.json').read()
        data = json.loads(File)
        total = 0
        rank = 0
        for x in data['error']:
            if x['id'] == member.id:
                total = x['total']
        for a in data['donator']:
            if a['id'] == member.id:
                rank = a['rank']
        if member.id in data['special']:
            special = guild.get_role(689520201259417682)
            await member.add_roles(special, reason=f'Has Special Badge')
        donator = guild.get_role(690234363648016443)
        if rank == 3:
            mega = guild.get_role(690234610462097504)
            await member.add_roles(mega, donator, reason=f'Has MEGA Badge')
        elif rank == 2:
            mvp = guild.get_role(690234421294530657)
            await member.add_roles(mvp, donator, reason=f'Has MVP Badge')
        elif rank == 1:
            vip = guild.get_role(665423079454801930)
            await member.add_roles(vip, donator, reason=f'Has VIP Badge')
        if total >= 5:
            bug = guild.get_role(729501130723426334)
            await member.add_roles(bug, reason=f'Has Found {total} Bugs with Quacky')
        await ctx.send('<:check:678014104111284234> Updated your Roles in the Quacky Support Server.')

    @commands.command()
    @commands.cooldown(1, 300.0, BucketType.user)
    async def cleardata(self, ctx):
        msg = await ctx.send(f'Are you sure you want to do this, {ctx.author.mention}?\nThis will clear your error, donator, and special badge(s). __**THERE IS NO UNDO!**__')
        checkmark = self.bot.get_emoji(678014104111284234)
        redx = self.bot.get_emoji(678014058590502912)
        await msg.add_reaction(checkmark)
        await msg.add_reaction(redx)
        def check(reaction, user):
            if ctx.author == user:
                if reaction.emoji == checkmark:
                    return True
                elif reaction.emoji == redx:
                    return True
                else:
                    return False
            else:
                return False
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            return await msg.edit(content=f'~~{msg.content}~~\n\nYou took too long to react to the message!')
        else:
            if reaction.emoji == redx:
                return await ctx.send(f'Ok, I won\'t clear your data.')

        File = open('/root/Quacky/Files/badges.json').read()
        data = json.loads(File)
        error = data['error']
        donator = data['donator']
        special = data['special']
        for x in error:
            if x['id'] == ctx.author.id:
                error.remove(x)
        for a in donator:
            if a['id'] == ctx.author.id:
                donator.remove(a)
        if ctx.author.id in special:
            special.remove(ctx.author.id)
        with open('/root/Quacky/Files/badges.json', 'w') as f:
            json.dump(data, f, indent=4)
        guild = self.bot.get_guild()
        ctx_member = guild.get_member(ctx.author.id)
        await ctx.send('<:check:678014104111284234> Cleared your Quacky Data!\nIf you would like to sync your roles with your badges do `!rankupdate`')

def setup(bot):
    bot.add_cog(Misc(bot))
