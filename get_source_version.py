#!/usr/bin/python3
import apt
import json

apt_cache = apt.Cache()
with open('result.json','r') as f:
    data = json.load(f)

compared_list = []
for security_package in data:
    compared = security_package
    for pkg in apt_cache:
        if apt_cache[pkg.name].candidate.source_name == compared["package"]:
            compared["repo_version"] = apt_cache[pkg.name].candidate.version
            break
    compared_list.append(compared)
    if os.system("dpkg --compare-versions %s gt %s"%(compared["unstable"],compared["repo_version"])) == 0:
        compared_list["panda_status"] = "danger"
    else:
        compared_list["panda_status"] ="safe"

with open('compared.json','w') as f:
    json.dump(compared_list,f)
