import json


class FileUtil(object):

    def readidpass(self,path):
        with open(path,"r") as f:
            content=json.load(f)
        id=content["id"]
        password=content["password"]
        return id,password


if __name__ == '__main__':
    fileutil=FileUtil()
    print(fileutil.readidpass("../password/password.txt"))

