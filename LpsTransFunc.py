from json import dumps, loads


'''
[
    {
        "lineName":"exmple",
        "Info":"example",
        "Sub":{
            "0":
                {
                    "name":"name1",
                    'Info':"Info1",
                },
            "1":
                {
                    "name":"name2",
                    'Info':"Info2",
                },
            "2":
                {
                    "name":"...",
                    'Info':"...",
                },
            ...
                {...}
        }
    },
    {
        ...
    },
    
]
'''


class LpsList(list):



    def __init__(self, **kw):
        super().__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'LpsObj' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def First(self):
        return self[0]['Line0']

    def FindLine(self, key):
        for item in self:
            if item.get(key):
                return item[key]
        return None

    def FindAllLine(self, key):
        result = []
        for item in self:
            if item.get(key):
                result.append(item[key])
        return result

    def toJson(self):
        return dumps(self, ensure_ascii=False, indent=4)

    @classmethod
    def from_list(cls, list_obj: list):
        result = cls()
        for item in list_obj:
            result.append(item)
        return result


def dLpsEachLineParse(dict_obj: dict,
                      line_data: str,
                      line_index: int,
                      depth: int = 0, ):
    index = line_data.find(":|")
    if index == -1:
        return
    first_data = line_data[:index]
    second_data = line_data[index + 2:]

    if depth == 0:
        dict_obj["name"] = first_data[:first_data.find("#") if first_data.find("#") != -1 else len(first_data)]
        dict_obj["Info"] = first_data[first_data.find("#") + 1:] if first_data.find("#") != -1 else ""
        dict_obj["Sub"] = dict()
        dLpsEachLineParse(dict_obj["Sub"], second_data, line_index, depth + 1)
    else:
        dict_obj[str(depth - 1)] = {"name": first_data[:first_data.find("#")], "Info": first_data[first_data.find("#") + 1:]}
        dLpsEachLineParse(dict_obj, second_data, line_index, depth + 1)


def LpsListLineToLpsStr(lps_dict: dict, depth: int = 0):
    result = ""
    result += lps_dict["name"] + ("#" + lps_dict["Info"] if lps_dict["Info"] != "" else "") + ":|"
    for key, value in lps_dict["Sub"].items():
        result += value["name"] + ("#" + value["Info"] if value["Info"] != "" else "") + ":|"
    result += "\n"
    return result


def LpsFileToLpsList(path):
    lps_obj = LpsList()
    with open(path, 'r', encoding='utf-8') as f:
        lps = f.read()
    line_list = lps.split('\n')
    for index, line in enumerate(line_list):
        line_str = "Line%d" % index
        lps_obj.append(dict())
        if line.find(":|") != -1:
            dLpsEachLineParse(lps_obj[-1], line, index)
    return lps_obj


def LpsStrToLpsList(lps_str):
    lps_dict = LpsList()
    line_list = lps_str.split('\n')
    for index, line in enumerate(line_list):
        if line == "":
            continue
        lps_dict.append(dict())
        if line.find(":|") != -1 and line:
            dLpsEachLineParse(lps_dict[-1], line, index)
    return lps_dict


def JsonFileToLpsList(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        json_str = f.read()
    json_obj = loads(json_str)
    lps_list = LpsList.from_list(json_obj)
    return lps_list


def JsonStrToLpsList(json_str):
    json_obj = loads(json_str)
    lps_list = LpsList.from_list(json_obj)
    return lps_list


def LpsListToJsonStr(lps_list):
    return dumps(lps_list, ensure_ascii=False, indent=4)


def LpsListToJsonFile(lps_list, json_path):
    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(dumps(lps_list, ensure_ascii=False, indent=4))


def LpsListToLpsStr(lps_list):
    lps_str = ""
    for line in lps_list:
        lps_str += LpsListLineToLpsStr(line)
    return lps_str


def LpsListToLpsFile(lps_list, path):
    lps_str = LpsListToLpsStr(lps_list)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(lps_str)


def JsonStrToLpsStr(json_str):
    lps_list = JsonStrToLpsList(json_str)
    return LpsListToLpsStr(lps_list)


def JsonStrToLpsFile(json_str, path):
    lps_list = JsonStrToLpsList(json_str)
    LpsListToLpsFile(lps_list, path)


def JsonFileToLpsStr(json_path):
    lps_list = JsonFileToLpsList(json_path)
    return LpsListToLpsStr(lps_list)


def JsonFileToLpsFile(json_path, path):
    lps_list = JsonFileToLpsList(json_path)
    LpsListToLpsFile(lps_list, path)


def LpsStrToJsonStr(lps_str):
    lps_list = LpsStrToLpsList(lps_str)
    return LpsListToJsonStr(lps_list)


def LpsStrToJsonFile(lps_str, json_path):
    lps_list = LpsStrToLpsList(lps_str)
    LpsListToJsonFile(lps_list, json_path)


def LpsFileToJsonStr(path):
    lps_list = LpsFileToLpsList(path)
    return LpsListToJsonStr(lps_list)


def LpsFileToJsonFile(path, json_path):
    lps_list = LpsFileToLpsList(path)
    LpsListToJsonFile(lps_list, json_path)
