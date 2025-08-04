import discord
from discord import app_commands
from discord.ext import commands
from random import choice, random
from typing import Optional
from collections import defaultdict
from db.DBHelper import get_role
from utils import has_role
import requests

lowercase_locked: dict[int, set[int]] = defaultdict(set)


def setup(bot: commands.Bot):
    @bot.tree.command(
        name="forcelowercase",
        description="Force a member's messages to lowercase (toggle)",
    )
    @app_commands.describe(member="Member to lock/unlock")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def forcelowercase(interaction: discord.Interaction, member: discord.Member):
        locked = lowercase_locked[interaction.guild.id]
        if member.id in locked:
            locked.remove(member.id)
            await interaction.response.send_message(
                f"🔓 {member.display_name} unlocked – messages stay unchanged.",
                ephemeral=True,
            )
        else:
            locked.add(member.id)
            await interaction.response.send_message(
                f"🔒 {member.display_name} locked – messages will be lower-cased.",
                ephemeral=True,
            )

    @bot.tree.command(name="punch", description="Punch someone with anime style")
    async def punch(interaction: discord.Interaction, user: discord.Member):
        response = requests.get(
            "https://api.otakugifs.xyz/gif?reaction=punch&format=gif"
        )

        gif = response.json()
        gif = gif["url"]
        if user.id == interaction.user.id:
            await interaction.response.send_message(
                "You can't punch yourself ... or maybe you can?", ephemeral=True
            )
            return

        embed = discord.Embed(
            title=f"{interaction.user.display_name} punches {user.display_name}!",
            color=discord.Colour.red(),
        )
        embed.set_image(url=gif)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="stab", description="Stab someone with anime style")
    async def stab(interaction: discord.Interaction, user: discord.Member):

        sender_id = interaction.user.id
        try:
            if user.id == sender_id:
                if random() < 0.20:
                    embed = discord.Embed(
                        title=f"{interaction.user.display_name} tried to stab themselves... and succeeded?!",
                        color=discord.Color.red(),
                    )
                    await interaction.response.send_message(embed=embed)
                    return
                else:
                    await interaction.response.send_message(
                        "You can't stab yourself... or can you?", ephemeral=True
                    )
                    return
            if random() < 0.50:
                embed = discord.Embed(
                    title=f"{interaction.user.display_name} stabs {user.display_name}!",
                    color=discord.Color.red(),
                )
                await interaction.response.send_message(embed=embed)
            else:
                fail_messages = [
                    "Isn't that illegal?",
                    "You don't have a knife.",
                    "You missed completely!",
                ]
                await interaction.response.send_message(choice(fail_messages))
        except Exception:
            await interaction.response.send_message(
                "You can't stab someone with higher permission than me.", ephemeral=True
            )

    @bot.tree.command(name="dance", description="hit a cool dance")
    async def dance(interaction: discord.Interaction):
        response = requests.get(
            "https://api.otakugifs.xyz/gif?reaction=dance&format=gif"
        )

        gif = response.json()
        gif = gif["url"]
        embed = discord.Embed(
            title=f"{interaction.user.display_name} Dances", color=discord.Color.red()
        )
        embed.set_image(url=gif)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="kiss", description="kiss another user")
    async def kiss(interaction: discord.Interaction, user: discord.Member):
        response = requests.get(
            "https://api.otakugifs.xyz/gif?reaction=kiss&format=gif"
        )

        gif = response.json()
        gif = gif["url"]
        embed = discord.Embed(
            title=f"{interaction.user.display_name} kisses {user.display_name} ꨄ︎",
            color=discord.Color.red(),
        )
        embed.set_image(url=gif)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="blush", description="blush (bcs of another user)")
    async def blush(interaction: discord.Interaction, user: discord.Member = None):
        response = requests.get(
            "https://api.otakugifs.xyz/gif?reaction=blush&format=gif"
        )

        gif = response.json()
        gif = gif["url"]
        if user == None:
            embed = discord.Embed(
                title=f"{interaction.user.display_name} blushes",
                color=discord.Color.red(),
            )
            embed.set_image(url=gif)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title=f"{interaction.user.display_name} blushes because of {user.display_name} ꨄ",
                color=discord.Color.red(),
            )
            embed.set_image(url=gif)
            await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="woah", description="woah")
    async def woah(interaction: discord.Interaction):
        response = requests.get(
            "https://api.otakugifs.xyz/gif?reaction=woah&format=gif"
        )

        gif = response.json()
        gif = gif["url"]

        embed = discord.Embed(
            title=f"{interaction.user.display_name} says woah!",
            color=discord.Color.red(),
        )
        embed.set_image(url=gif)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="tickle", description="tickle another user")
    async def tickle(interaction: discord.Interaction, user: discord.Member):
        response = requests.get(
            "https://api.otakugifs.xyz/gif?reaction=tickle&format=gif"
        )

        gif = response.json()
        gif = gif["url"]
        embed = discord.Embed(
            title=f"{interaction.user.display_name} tickles {user.display_name} ",
            color=discord.Color.red(),
        )
        embed.set_image(url=gif)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="slap", description="slap another user")
    async def slap(interaction: discord.Interaction, user: discord.Member):
        try:
            response = requests.get(
                "https://api.otakugifs.xyz/gif?reaction=slap&format=gif",
                timeout=5,
            )
            response.raise_for_status()
            data = response.json()
            gif = data.get("url", "")
        except requests.RequestException:
            gif = ""
        embed = discord.Embed(
            title=f"{interaction.user.display_name} slaps {user.display_name} really hard!",
            color=discord.Color.red(),
        )
        if gif:
            embed.set_image(url=gif)
        await interaction.response.send_message(
            embed=embed if gif else None,
            content=None if gif else "*whiff* Can't fetch a slap gif right now.",
        )

    @bot.tree.command(name="lick", description="Lick another member")
    async def lick(interaction: discord.Interaction, user: discord.Member):
        response = requests.get(
            "https://api.otakugifs.xyz/gif?reaction=lick&format=gif"
        )

        gif = response.json()
        gif = gif["url"]
        embed = discord.Embed(
            title=f"{interaction.user.display_name} licks {user.display_name} ꨄ︎ how does it taste?",
            color=discord.Color.red(),
        )
        embed.set_image(url=gif)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="good", description="Tell someone he/she is a good boy/girl")
    async def good(interaction: discord.Interaction, user: discord.Member):

        response = requests.get("https://api.otakugifs.xyz/gif?reaction=pat&format=gif")

        gif = response.json()
        gif = gif["url"]
        try:
            sheher_id = get_role(interaction.guild.id, "sheher")
            hehim_id = get_role(interaction.guild.id, "hehim")
            if sheher_id and has_role(user, sheher_id) and not user.name == "goodyb":
                embed = discord.Embed(
                    title=f"{interaction.user.display_name} calls {user.display_name} a good girl",
                    color=discord.Color.red(),
                )
                embed.set_image(url=gif)
                await interaction.response.send_message(embed=embed)
            elif hehim_id and has_role(user, hehim_id):
                embed = discord.Embed(
                    title=f"{interaction.user.display_name} calls {user.display_name} a good boy",
                    color=discord.Color.red(),
                )
                embed.set_image(url=gif)
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(
                    title=f"{interaction.user.display_name} calls {user.display_name} a good child",
                    color=discord.Color.red(),
                )
                embed.set_image(url=gif)
                await interaction.response.send_message(embed=embed)
        except Exception:
            await interaction.response.send_message(
                "Command didnt work, sry :(", ephemeral=True
            )

    return (
        forcelowercase,
        punch,
        stab,
        dance,
        good,
        kiss,
        lick,
        blush,
        woah,
        tickle,
    )
