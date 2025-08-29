#!/usr/bin/env python3
from __future__ import annotations

import random
import sys
from pathlib import Path

# Ensure repository root on path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from db.DBHelper import register_user, get_money, safe_add_coins


def award_vote(user_id: str) -> int:
    register_user(user_id, user_id)
    balance = get_money(user_id)
    if random.random() < 0.01:
        reward = max(1, int(balance * 0.25))
    else:
        ten_percent = int(balance * 0.10)
        reward = 100 if ten_percent < 100 else random.randint(100, ten_percent)
    safe_add_coins(user_id, reward)
    return reward


if __name__ == "__main__":
    uid = sys.argv[1]
    print(award_vote(uid))
