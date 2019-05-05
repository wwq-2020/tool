#encoding:utf8
#!/usr/bin/env python

import fire
import io


def opList(v, buf, dep=0):
    buf.write("[]")
    if len(v) == 0:
        buf.write("interface{}")
    else:
        if isinstance(v[0], str):
            buf.write("string")
        elif isinstance(v[0], int):
            buf.write("int64")
        elif isinstance(v[0], float):
            buf.write("float64")
        elif isinstance(v[0], list):
            opList(v[0], buf)
        elif isinstance(v[0], dict):
            opDict(v[0], buf, dep=dep+1)
        else:
            print("invalid type for value %s" % v)
            exit(-1)


def opDict(v, buf, dep=1):
    buf.write("struct {\n")

    if len(v) == 0:
        buf.write("interface{}")
    else:
        for newK, newV in v.items():
            newDep = dep + 1
            buf.write("\t" * newDep + newK + " ")
            if isinstance(newV, str):
                buf.write("string")
            elif isinstance(newV, int):
                buf.write("int64")
            elif isinstance(newV, float):
                buf.write("float64")
            elif isinstance(newV, list):
                opList(newV, buf)
            elif isinstance(newV, dict):
                opDict(newV, buf, dep=newDep)
            else:
                print("invalid type for value %s" % newV)
                exit(-1)
            buf.write(" `json:\"%s\"`\n" % newK)
    buf.write("\t" * dep + "}")


class Gotool(object):

    def j2s(self, jsonStr):
        if not isinstance(jsonStr, dict):
            print("must be dict")
            exit(-1)
        buf = io.StringIO()
        buf.write(u"type tmp struct {\n")
        for name, v in jsonStr.items():
            buf.write(u"\t%s " % name.capitalize())
            if isinstance(v, str):
                buf.write(u"string")
            elif isinstance(v, int):
                buf.write(u"int64")
            elif isinstance(v, float):
                buf.write(u"float64")
            elif isinstance(v, list):
                opList(v, buf)
            elif isinstance(v, dict):
                opDict(v, buf)
            else:
                print(u"invalid type for value %s" % v)
                exit(-1)
            buf.write(u" `json:\"%s\"`\n" % name.lower())

        buf.write(u"}")
        return buf.getvalue()


if __name__ == '__main__':
    fire.Fire(Gotool)
