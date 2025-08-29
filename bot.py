# pip install aiohttp topggpy
import os
import asyncio
import discord
from discord.ext import commands
from aiohttp import web
from topgg import WebhookManager

# ---- Deine Imports (gekürzt) ----
from config import *
from commands.fun_commands import setup as setup_fun, lowercase_locked
from commands.booster_commands import setup as setup_booster
from commands.economy_commands import setup as setup_economy
from commands.stats_commands import setup as setup_stats
from commands.action_commands import setup as setup_action
from commands.admin_commands import setup as setup_admin
from commands.antinuke_commands import setup as setup_antinuke
from commands.setup_wizard import setup as setup_wizard
from commands.explain_commands import setup as setup_explain
import events, anti_nuke

# ---------------------------------

TOPGG_AUTH = "lS6lvCvcDdDKklWoUHLLjtz10g0eZCW8"
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "3000"))

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# --- AIOHTTP + top.gg Webhook ---
app = web.Application()
wh = WebhookManager()
wh.dbl_webhook("/topgg", auth_key=TOPGG_AUTH)


@wh.listener()
async def on_vote(data: dict):
    # data: {'bot','user','type','isWeekend','query'}
    print("Neuer Vote:", data)
    user_id = data.get("user")
    is_weekend = data.get("isWeekend", False)

    # TODO: Idempotenz! Vote-Log in DB prüfen, dann Reward gutschreiben:
    # balance = await db.get_balance(user_id)
    # reward = max(round(balance * 0.10), 150)
    # if is_weekend: reward *= 2  # wenn du das wirklich willst
    # await db.add_balance(user_id, reward)
    # try: await bot.get_channel(CHANNEL_ID).send(f"Thanks for voting, <@{user_id}>! +{reward} coins")
    # except: pass


# Nicht blockierend starten:
async def start_webhook():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=WEBHOOK_PORT)
    await site.start()
    print(f"[top.gg] Webhook listening on 0.0.0.0:{WEBHOOK_PORT}/topgg")


# --- Discord Bot ---
class MyBot(commands.Bot):
    async def setup_hook(self):
        # startet den Webhook-Server, bevor on_ready feuert
        await start_webhook()


bot = MyBot(command_prefix="!", intents=intents)

# deine Cogs/Setups
setup_fun(bot)
setup_booster(bot)
setup_economy(bot)
setup_stats(bot, ROD_SHOP)
setup_action(bot)
setup_admin(bot)
setup_antinuke(bot)
setup_wizard(bot)
setup_explain(bot)
events.setup(bot, lowercase_locked)
anti_nuke.setup(bot)

if __name__ == "__main__":
    with open("code.txt", "r") as f:
        TOKEN = f.read().strip()
    bot.run(TOKEN)
