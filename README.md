# ISICON01 試験アプリ

### gotty
'''
yum install wget unzip
wget https://github.com/yudai/gotty/releases/download/v1.0.1/gotty_linux_amd64.tar.gz
tar zxvf gotty_linux_amd64.tar.gz
mv gotty /usr/local/bin/
'''

### app
'''
yum install git python python-virtualenv
cd isicon01-app/isicon01-app/
virtualenv virt
source virt/bin/activate
pip install flask
'''

### 起動
'''
python app.py
'''