
import json

def getFields(datas,items):
    """
    only return need list
    :return:
    """
    result = []
    for data in datas:
       tempdict = json.loads(data)
       temp = {}
       for item in items:
           temp[item] = tempdict[item]
       result.append(json.dumps(temp))

    return result



def main():
    pass


if __name__ == '__main__':
    main()