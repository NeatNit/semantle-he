from argparse import ArgumentParser
from argparse import ArgumentTypeError
from datetime import datetime
import os
import sys

base = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.extend([base])

from common.session import get_mongo
from common.session import get_redis
from logic import CacheSecretLogic


def valid_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise ArgumentTypeError("Bad date: should be of the format YYYY-mm-dd")


def main():
    parser = ArgumentParser("Set SematleHe secret for any date")
    parser.add_argument('secret', metavar='SECRET', help="Secret to set")
    parser.add_argument(
        '-d', '--date', metavar='DATE', type=valid_date, help="Date of secret. If not provided today's date is used"
    )
    parser.add_argument(
        '--dry', action='store_true', help="If passed, just prints the list of 1000 closest words"
    )

    args = parser.parse_args()

    mongo = get_mongo()
    redis = get_redis()

    logic = CacheSecretLogic(mongo, redis, args.secret, args.date)
    logic.set_secret(args.dry)
    if args.dry:
        cache = logic.cache[::-1]
        print(cache)
        for rng in (range(1, 11), range(100, 1000, 100)):
            for i in rng:
                score, w = cache[i]
                print(f"{i}: {score}: {w[::-1]}")


if __name__ == '__main__':
    main()
