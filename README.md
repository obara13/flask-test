# ISICON01 試験アプリ

## 環境構築手順

### gottyを入れる
```
yum install wget unzip
wget https://github.com/yudai/gotty/releases/download/v1.0.1/gotty_linux_amd64.tar.gz
tar zxvf gotty_linux_amd64.tar.gz
mv gotty /usr/local/bin/
```

### appを入れて起動
```
yum install git python python-virtualenv
git clone http://deviac.div.tis.co.jp/ISICON/isicon01-app.git
cd isicon01-app/isicon01-app/
virtualenv virt
source virt/bin/activate
pip install flask
python app.py
```

### 2回目以降
```
cd isicon01-app/isicon01-app/
source virt/bin/activate
python app.py
```


python3
```
yum install https://centos7.iuscommunity.org/ius-release.rpm
yum install python34 python34-virtualenv python34-pip
virtualenv-3 virt3
source virt3/bin/activate
pip install flask

yum install python36 python36u-pip
pip3.6 install virtualenv
/usr/local/bin/virtualenv virt3
source virt3/bin/activate
pip install flask

```

