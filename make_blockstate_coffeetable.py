from pathlib import Path
import json
import itertools


def main():
    path_dir_model = Path("src/main/resources/assets/cfm/models/block")

    list_path_coffeetable = path_dir_model.glob("coffee_table_*.json")
    list_coffeetable_parent = [path.stem for path in list_path_coffeetable]

    for type in list_type:
        list_path_type_coffeetable = path_dir_model.glob(f"{type}_coffee_table_*.json")
        for path_type_coffeetable in list_path_type_coffeetable:
            path_type_coffeetable.unlink(missing_ok=True)

        type_leg = type[9:] if "stripped_" in type else f"stripped_{type}"
        for coffeetable_parent in list_coffeetable_parent:
            data = {
                "parent": f"cfm:block/{coffeetable_parent}",
                "textures": {
                    "top": f"block/{type}_log",
                    "legs": f"block/{type_leg}_log"
                }
            }

            with open(path_dir_model / f"{type}_{coffeetable_parent}.json", "w") as fp:
                json.dump(data, fp, indent=4)

    path_dir_blockstate = Path("src/main/resources/assets/cfm/blockstates")

    for type in list_type:
        data = {"variants": {}}

        list_combination = list(itertools.product(("false", "true"), repeat=4))
        list_combination = list(itertools.product(*[("false", "true")] * 4, ("north", "east", "south", "west"), ("false", "true")))
        for north, east, south, west, facing, tall in list_combination:
            data_i = {}
            name_tall = "short" if tall == "false" else "tall"
            north_r, east_r, south_r, west_r = round_orientation(north, east, south, west, facing)

            if (north_r == "true" and south_r == "true") or (east_r == "true" and west_r == "true"):
                data_i["model"] = f"cfm:block/{type}_coffee_table_{name_tall}_none"
            elif south_r == "true" and east_r == "true":
                data_i["model"] = f"cfm:block/{type}_coffee_table_{name_tall}_northwest"
            elif south_r == "true" and west_r == "true":
                data_i["model"] = f"cfm:block/{type}_coffee_table_{name_tall}_northeast"
            elif north_r == "true" and west_r == "true":
                data_i["model"] = f"cfm:block/{type}_coffee_table_{name_tall}_southeast"
            elif north_r == "true" and east_r == "true":
                data_i["model"] = f"cfm:block/{type}_coffee_table_{name_tall}_southwest"
            elif north_r == "true":
                data_i["model"] = f"cfm:block/{type}_coffee_table_{name_tall}_south"
            elif east_r == "true":
                data_i["model"] = f"cfm:block/{type}_coffee_table_{name_tall}_west"
            elif south_r == "true":
                data_i["model"] = f"cfm:block/{type}_coffee_table_{name_tall}_north"
            elif west_r == "true":
                data_i["model"] = f"cfm:block/{type}_coffee_table_{name_tall}_east"
            else:
                data_i["model"] = f"cfm:block/{type}_coffee_table_{name_tall}_all"

            data_i["y"] = 0 if facing == "north" else 90 if facing == "east" else 180 if facing == "south" else 270

            data["variants"][f"north={north},east={east},south={south},west={west},facing={facing},tall={tall}"] = data_i

        with open(path_dir_blockstate / f"{type}_coffee_table.json", "w") as fp:
            json.dump(data, fp, indent=4)


def round_orientation(north, east, south, west, facing):
    if facing == "north":
        return north, east, south, west
    elif facing == "east":
        return east, south, west, north
    elif facing == "south":
        return south, west, north, east
    elif facing == "west":
        return west, north, east, south
    raise


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
