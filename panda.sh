#!/bin/bash
echo "deb http://packages.deepin.com/deepin/ panda main contrib non-free" > /etc/apt/sources.list
apt-get update
cd /debian_security_checker/
python3 get_source_version.py
