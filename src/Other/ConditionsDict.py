import pathlib as pl

def load_conditions(
        src_default: str = "../../data/conditions_default",
        src_useradded: str = "../../data/conditions_useradded"
):
    path_default = pl.Path(src_default)
    path_useradded = pl.Path(src_useradded)

    if not path_default.is_file():
        raise AssertionError("Could not load conditions: The data/conditions_default file does not exist." +
                             "Has it been deleted?")

    to_load = [path_default]
    if path_useradded.is_file():
        to_load.append(path_useradded)

    return_list = []
    for p in to_load:
        with open(p) as cond_file:
            for line in cond_file:
                # ignore comments (lines starting with #) and blank lines
                if (line != "") and (line != "\n") and (line[0] != "#"):
                    return_list.append(line.rstrip("\n"))

    return_list = list(set(return_list))
    return_list.sort()
    return return_list

conditions_dict = {}
conditions_list = load_conditions()
for i in conditions_list:
    conditions_dict.update({i: False})
