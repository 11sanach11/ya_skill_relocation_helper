# relocation-helper
## Pre requirements
```shell
apt install python3-pip build-essential libsystemd-dev git
pip3 install poetry
```
## Installation (example)
- clone repo from github into /opt:
```shell
WORKDIR=/opt
sudo mkdir -p $WORKDIR/relocation-helper
sudo chown $USER:$USER $WORKDIR/relocation-helper
cd $WORKDIR
git clone https://github.com/11sanach11/ya_skill_relocation_helper.git
cd relocation-helper
poetry install
cp ./test_config.json ./config.json
<<<!!! PREPARE CONFIG FILE, SET server.port, etc...
sudo cp ./template_for_service/relocation-helper.service /etc/systemd/system/relocation-helper.service
sudo sed -i -e "s/%USER%/$USER/g" -e "s|%WORKDIR%|$WORKDIR|g" /etc/systemd/system/relocation-helper.service
sudo systemctl enable relocation-helper
$WORKDIR/update.sh
```

## UPDATE
```shell
relocation-helper
$WORKDIR/relocation-helper/update.sh
```
