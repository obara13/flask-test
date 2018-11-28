# ISICON01 試験アプリ

## 環境構築手順

### gottyを入れる
```
yum install wget unzip
wget https://github.com/yudai/gotty/releases/download/v1.0.1/gotty_linux_amd64.tar.gz
tar zxvf gotty_linux_amd64.tar.gz
mv gotty /usr/local/bin/
```

### appを入れる
```
yum install git python python-virtualenv
git clone http://deviac.div.tis.co.jp/ISICON/isicon01-app.git
cd isicon01-app/isicon01-app/
virtualenv virt
source virt/bin/activate
pip install flask
```

### 起動
```
python app.py
```
