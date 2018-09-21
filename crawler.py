import requests
import shutil
chapters = "titlepage,cp,index,preface".split(",")
chapters.extend(["chapter%.2d"%x for x in range(1,10)])
chapters.extend(["appendix01","reference01"])

URL = "http://academic.hep.com.cn/skld//fileup/book/44205-00/swf/44205-00_%s/chapter%s.swf"

for ci, c in enumerate(chapters):
    page = 1
    print "Chapter: "+c
    while True:
        url = URL%(c,page)
        r = requests.get(url, stream=True)
        needBreak = False
        if r.status_code != 200:
            needBreak = True
            print 'Error: %s status %s' % (url, r.status_code)
        elif r.headers.get("content-type")[0:len("application/x-shockwave-flash")] != "application/x-shockwave-flash":
            needBreak = True
            print "Content-Type %s detected. Break." % r.headers.get('content-type')
        else:
            path = "./contents/%.3d-%s_%.3d.swf" % (ci, c, page)
            with open(path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                print "%s -> %s"%(url, path)
        r.close()
        if needBreak:
            break
        page += 1 
           
