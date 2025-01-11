import json


def read_json(infile):
    with open(infile, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)
    return loaded_data

def write_json(outfile, data):
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def remove_label(infile, outfile):
    data = read_json(infile)
    for item in data:
        item['relationship'] = []
    write_json(outfile, data)

if __name__ == "__main__":
    infile = "DiaDP/data/dialog/test.json"
    outfile = "DiaDP/data/dialog/test_.json"
    remove_label(infile, outfile)