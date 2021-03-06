#!/usr/bin/env python 
import yaml
import sys

from collections import OrderedDict

if True:
    def represent_odict(dumper, instance):
        return dumper.represent_mapping('tag:yaml.org,2002:map', instance.items())

    yaml.add_representer(OrderedDict, represent_odict)

    def construct_odict(loader, node):
        return OrderedDict(loader.construct_pairs(node))

    yaml.add_constructor('tag:yaml.org,2002:map', construct_odict)

#    yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
#        lambda loader, node: OrderedDict(loader.construct_pairs(node)))


def load(filename):
    data = None
    with open(filename) as f:
        data = yaml.safe_load(f)

    return data

def apply_link(data,filename):
    key1 = "link"
    linkcontent = ["nodename","nodetype","linktype"]
    linklist =  []
    for link in data[key1]:
        alink = []
        for content in linkcontent:
            if content in link.keys():
                alink.append( (content,link[content]) )
        #alink.append( ("filename",filename) )
        if "link" in link.keys():
            newlink = apply_link(link,filename)
            alink.append( ("link", newlink ) )
        linklist.append( OrderedDict(alink) )
        print(yaml.dump(linklist))
    return linklist

def add_tag_filename(data,filename):
    keys = list(data.keys())
    parentkey = ["workflow","link"]
    wfblockall = None
    linkall = []
    for key1 in keys:
        if key1 == parentkey[0]:
            raise 
        elif key1 == parentkey[1]:
            linkall.extend(apply_link(data,filename) )
        else:
            print("unknown key",key1)
            raise

    wfall = {}
    if wfblockall is not None:
        wfall =  wkblockall
        print(yaml.dump(wfall))

    if len(linkall)>0:
        print(len(linkall))
        wfall.update({"link":linkall } )
 
    return wfall

def load_all_yml(filenames):
   dataall = {}
   #dataall = {"workflow":[], "link":[]}

   for filename in sys.argv[1:]:
      data = load(filename)
      data = add_tag_filename(data,filename)
      for key in data:
          if key not in list(dataall.keys()):
              dataall[key] = []
          dataall[key].extend(data[key])

   return dataall

if __name__ == "__main__":

   wkall = load_all_yml(sys.argv[1:])

   with open("a.yml","w") as f: 
       yaml.dump(wkall,f)


