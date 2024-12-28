from pathlib import Path
import json
import itertools


def main():
    path_dir_blockstate = Path("src/main/resources/assets/cfm/blockstates")

    for type in list_type:
        data = {"variants": {}}

        list_combination = list(itertools.product(("false", "true"), repeat=4))
        list_combination = list(itertools.product(*[("false", "true")] * 4, ("north", "east", "south", "west")))
        for north, east, south, west, facing in list_combination:
            data_i = {}

            if (north == "true" and south == "true") or (east == "true" and west == "true"):
                data_i["model"] = f"cfm:block/{type}_table_center"
            else:
                data_i["model"] = f"cfm:block/{type}_table"

            data_i["y"] = 0 if facing == "north" else 90 if facing == "east" else 180 if facing == "south" else 270
            data_i["y"] = (data_i["y"] + 90) % 360

            data["variants"][f"north={north},east={east},south={south},west={west},facing={facing}"] = data_i

        with open(path_dir_blockstate / f"{type}_table.json", "w") as fp:
            json.dump(data, fp, indent=4)


list_type = [
    "oak",
    "birch",
    "spruce",
    "jungle",
    "acacia",
    "dark_oak",
    "crimson",
    "warped",
    "mangrove",
    "stripped_oak",
    "stripped_birch",
    "stripped_spruce",
    "stripped_jungle",
    "stripped_acacia",
    "stripped_dark_oak",
    "stripped_crimson",
    "stripped_warped",
    "stripped_mangrove",
]

if __name__ == "__main__":
    main()
