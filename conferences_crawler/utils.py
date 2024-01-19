import hashlib

class Utils:
    @staticmethod
    def generateUID(url):
        # replace :// and . with _
        url = url.replace("://", "_").replace(".", "_").replace("/", "_")
        return url

