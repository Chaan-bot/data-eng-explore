import csv, json, re
from pathlib import Path

# games.csv ships a broken header: `DiscountDLC count` is two column names
# whose separating comma was lost. Verified against games.json across 400
# games: field 7 is `discount`, field 8 is `dlc_count`.
HEADER_FIX_AT = 7
HEADER_FIX_TO = ['Discount', 'DLC count']


def snake(name: str) -> str:
    """'About the game' -> 'about_the_game' so SQL never needs quoting."""
    return re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')


def read_csv_rows(path, limit=None):
    """Yield each game as a dict, with the shipped header defect repaired."""
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        header[HEADER_FIX_AT:HEADER_FIX_AT + 1] = HEADER_FIX_TO
        columns = [snake(c) for c in header]

        for i, row in enumerate(reader):
            if limit is not None and i >= limit:
                return
            yield dict(zip(columns, row))


def clean_csv(src, dst, limit=None):
    """Read games.csv, repair the shipped header defect, write a loadable CSV."""
    with open(src, newline='', encoding='utf-8') as fin, \
         open(dst, 'w', newline='', encoding='utf-8') as fout:
        r, w = csv.reader(fin), csv.writer(fout)
        header = next(r)
        header[7:8] = ['Discount', 'DLC count']   # verified against games.json
        w.writerow([snake(c) for c in header])
        w.writerows(itertools.islice(r, limit) if limit else r)
    print(f"wrote {dst}")


def read_json_rows(path):
    """Yield (appid, json_text) pairs. games.json is one object keyed by appid."""
    with open(path, encoding='utf-8') as f:
        games = json.load(f)          # see the caveat below
    for appid, game in games.items():
        yield appid, json.dumps(game, ensure_ascii=False)


def write_jsonb_csv(src, dst):
    """Flatten games.json into a 2-column CSV that psql \\copy can load."""
    with open(dst, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['appid', 'data'])
        w.writerows(read_json_rows(src))
    print(f"wrote {dst}")


    read_csv_rows('/raw_downloaded_data/games.csv')


if __name__ == "__main__":
    HERE = Path(__file__).parent
    clean_csv(HERE / "raw_downloaded_data" / "games.csv",
              HERE / "games_clean.csv")