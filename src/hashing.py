import hashlib

def hashFile(path):
    """Generates MD5, SHA-1 and SHA-256 hashes for a file.

    Args:
        path (string): Takes the path of the file to hash

    Returns:
        dictionary: returns the hashes in dictionary
    """
    bufferSize = 65536

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()

    with open(path,'rb') as f:
        while True:
            data = f.read(bufferSize)
            if not data:
                break
            md5.update(data)
            sha1.update(data)
            sha256.update(data)

    return {
        "MD5": md5.hexdigest(),
        "SHA1": sha1.hexdigest(),
        "SHA256": sha256.hexdigest()
    }