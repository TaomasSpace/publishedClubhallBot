# Clubhall Bot

Utility bot for Discord.

## Database Rebalancing

A maintenance script lives in `scripts/rebalance_db.py` to shrink coin totals and stats.
Run it with:

```bash
python scripts/rebalance_db.py
```

The script automatically locates `users.db` in the project root so it can be run from any directory.

**Important:** back up your `users.db` database before running the script.

## Setup Wizard

Run `/setup-wizard` on your server to walk through a complete configuration.
The wizard explains every step, lets you skip anything, and sets up channels
and anti-nuke options. For role shortcuts and command restrictions it points
you to the `/setrole` and `/setcommandrole` commands for later use.

## Environment variables

The bot and the Top.gg webhook server rely on the following environment variables:

* `DISCORD_TOKEN` – Discord bot token.
* `TOPGG_AUTH` – token used to validate incoming Top.gg votes.
* `PORT` – optional port for the webhook server (defaults to 80).

Example start command:

```bash
export DISCORD_TOKEN=<your_token>
export TOPGG_AUTH=<topgg_webhook_token>
python bot.py
```

`bot.py` automatically launches `server.js` so the webhook is ready whenever the bot runs.

