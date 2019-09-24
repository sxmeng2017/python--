import hashlib

m = hashlib.md5()
print(m.digest_size)

def get_file_hash(file_path, mode='md5'):
    if not mode:
        raise ValueError('you should set a mode')
    if mode =='md5':
        m = hashlib.md5()
    with open(file_path,'rb') as fp:
        while True:
            blk = fp.read(4096)
            if not blk:
                break
            m.update(blk)
    return m.hexdigest()



