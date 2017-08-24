# -*- coding: utf-8 -*-

# 用于md5加密
# @param str 字符串
# @return str 字符串
# @author WuXiaokun
def md5(src):
    import hashlib
    hash = hashlib.md5()
    if isinstance(src,str):
        src = src.encode('utf-8')
    hash.update(src)
    return hash.hexdigest()