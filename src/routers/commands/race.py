import random
from typing import List, Dict


def get_race_results(
    users: List[str]
) -> Dict[str, float]:
    result = {}

    winner_user = random.choice(users)
    winner_time = round(random.uniform(7.4, 8.4), 2)

    for user in users:

        if user == winner_user:
            result[user] = winner_time

        difference = round(random.uniform(0.01, 0.35), 2)
        result[user] = round(winner_time + difference, 2)

    return sorted(result.items(), key=lambda x: x[1])