<!--

# generate key
ssh-keygen -t ed25519 -C "github-actions" -f github_action_key


# copy ssh into vps
ssh-copy-id -i ~/.ssh/windows-nomad.pub root@144.172.109.241

# login
 ssh root@144.172.109.241

# create a new user
adduser bot01

pass: adgsd303d

# give it a password

# add to sudoers
usermod -aG sudo bot01

# get vps ready for github actions and docker deployment:

sudo apt update && sudo apt upgrade -y

# install docker

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Add your user to docker group
sudo usermod -aG docker bot01
# log out and log back in for group change to take effect

# install docker-compose

root@ubuntu-Utah-0:~# export DOCKER_COMPOSE_VERSION=2.20.2
root@ubuntu-Utah-0:~# sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100 57.6M  100 57.6M    0     0  27.3M      0  0:00:02  0:00:02 --:--:-- 41.8M
root@ubuntu-Utah-0:~# sudo chmod +x /usr/local/bin/docker-compose
root@ubuntu-Utah-0:~# docker-compose version
Docker Compose version v2.20.2
root@ubuntu-Utah-0:~#



 -->
