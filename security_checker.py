#!/usr/bin/python3
import requests
import re
from lxml import html
import json
root_url = "https://lists.debian.org/debian-security-announce/2016/"
mail_index_url = root_url + "threads.html"
mail_index = requests.get(mail_index_url).text
r_mail_index = re.compile("\[SECURITY\] \[.+\] (.+) security update")
tree = html.fromstring(mail_index)
# example <a name="00000" href="msg00000.html">[SECURITY] [DSA 3431-1] ganeti security update</a>
result = tree.xpath('//li/strong/a/@href')
pkg_url_list = []
for href in result:
    package_url = root_url + href
    pkg_url_list.append(package_url)

test_list = ['https://lists.debian.org/debian-security-announce/2016/msg00325.html','https://lists.debian.org/debian-security-announce/2016/msg00323.html']
def get_package_info(url):
    package_info = {}
    url_text = requests.get(url).text
    re_date = re.compile(".+Date.+\:.+\, (.+)\<\/li\>")
    re_package = re.compile("Package        : (.+)")
    re_cve = re.compile("CVE ID         : (.+)")
    re_debian_bug = re.compile("Debian Bug     : (.+)")
    re_stable = re.compile("For the stable.+fixed in\\nversion (.+)\.")
    re_unstable = re.compile("For the unstable.+fixed in\\nversion (.+)\.")
    package_name = re_package.findall(url_text)[0]
    _date = re_date.findall(url_text)[0]
    if len(re_cve.findall(url_text)):
        cve_id = re_cve.findall(url_text)[0]
    else:
        cve_id = 'none'
    if len(re_debian_bug.findall(url_text)):
        debian_bug = re_debian_bug.findall(url_text)[0]
    else:
        debian_bug = 'none'
    if len(re_stable.findall(url_text)):
        stable_version = re_stable.findall(url_text)[0]
    else:
        stable_version = 'none'

    if len(re_unstable.findall(url_text)):
        unstable_version = re_unstable.findall(url_text)[0]
    else:
        unstable_version = 'none'
    package_info["date"] = _date
    package_info["package"] = package_name
    package_info["CVE_ID"] = cve_id
    package_info["debian_bug"] = debian_bug
    package_info["stable"] = stable_version
    package_info["unstable"] = unstable_version
    package_info["url"] = url
    return package_info

whole_info = []
for url in pkg_url_list:
    whole_info.append(get_package_info(url))

print(whole_info)
with open('result.json', 'w') as fp:
    json.dump(whole_info, fp)
