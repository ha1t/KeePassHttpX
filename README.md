# KeePassHttpX

> KeePass <-> KeePassHttpX <-> ChromeIPass

# TODO

- Passwordもダイアログでやりたい

# SETUP

- kptool.keepassdb の install
-- git clone して、 sudo python setup.py install

OSX の場合、

- sudo easy_install py2app

でpy2appをインストールできる。

# BUILD

`` export VERSIONER_PYTHON_PREFER_32_BIT=yes && python setup.py py2app -A ``
