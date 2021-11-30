# I was forced to write my own yaml file, because original could not be found during the execution of GitHub job

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def is_integer(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def load(path: str) -> dict:
    """A procedure which converts the yaml file at the path specified into a dictionary.

    Args:
        path (str): The path of the yaml file.

    Returns:
        config (dict): The yaml file in dictionary form.
    """

    with open(path, "r") as yaml:
        levels = []
        data = {}
        indentation_str = ""

        for line in yaml.readlines():
            if line.replace(line.lstrip(), '') != "" and indentation_str == "":
                indentation_str = line.replace(line.lstrip(), '')
            if line.strip() == "":
                continue
            elif line.rstrip()[-1] == ":":
                if len(line.replace(line.strip(), '')) // 2 < len(levels):
                    levels[len(line.replace(line.strip(), '')) // 2] = f"['{line.strip()[:-1]}']"
                else:
                    levels.append(f"['{line.strip()[:-1]}']")
                exec(f"data{''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}['{line.strip()[:-1]}']" + " = {}")

                continue

            value = line.split(":")[-1].strip()

            if is_float(value) or is_integer(value) or value == "True" or value == "False":
                exec(f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}['{line.split(':')[0].strip()}'] = {value}")

            else:
                exec(f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}['{line.split(':')[0].strip()}'] = '{value}'")

    return data
