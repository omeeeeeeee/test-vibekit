import json

def create_fruit_dict():
    return {"apple": 1, "banana": 2, "cherry": 3}

if __name__ == "__main__":
    result = create_fruit_dict()
    print(json.dumps(result))