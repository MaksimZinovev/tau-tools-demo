# Running Selenium web UI Tests on Remote  Machine  Using Jenkins and AWS EC2 Instance: Beginners Guide

## **How to create EC2 instance AWS**

Detailed instructions can be easily found online. Here are the main steps

- Create Amazon AWS account

- Sign in as root user

- Set up with Amazon EC2

  - Create key pair
  - Save key in a safe place 
  - If you will use an SSH client on a Mac or Linux computer to connect to your Linux instance, use the following command to set the permissions of your private key file so that only you can read it.

  ``` 
  chmod 400 your_user_name-key-pair-region_name.pem
  ```

- AWS Management Console -> EC2

- Launch instance: instances -> select  instance -> actions ->start



## **How to connect to EC2 instance using SSH**

- AWS Management Console -> EC2->Connect

- copy prompt from popup window and run in terminal
- you can copy public DNS from EC2 Management Console

``` 
ssh -i path-to-private-key/mk_zin-key-pair-southeast-2.pem ec2-user@ec2-54-206-74-215.ap-southeast-2.compute.amazonaws.com
```

```
ssh -i <path-to-private-key/filename.pem> ec2-user@<your-public-dns>
```



- Success

```
       __|  __|_  )
       _|  (     /   Amazon Linux 2 AMI
      ___|\___|___|

https://aws.amazon.com/amazon-linux-2/

```

- Instructions  https://d1.awsstatic.com/Projects/P5505030/aws-project_Jenkins-build-server.pdf
- Instructions https://medium.com/@mohan08p/install-and-configure-jenkins-on-amazon-ami-8617f0816444

## Install and Start Jenkins

**Check for updates before proceeding**

```
sudo yum update –y
Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
amzn2-core                                               | 2.4 kB     00:00
No Match for argument: –y
No packages marked for update
[ec2-user@ip-172-31-9-135 ~]$
```

**Add the Jenkins repo using the following command**:

```
sudo wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat/jenkins.repo
```

**Import a key file from Jenkins-CI to enable installation from the package:**

```
 sudo rpm --import https://pkg.jenkins.io/redhat/jenkins.io.key
```



**Install Jenkins** 

```
 sudo yum install jenkins -y
```



**Succsess**

```
Installed:
  jenkins.noarch 0:2.232-1.1

Complete!
```



**If you Start Jenkins now you will get this error because Java not yet installed**

```
sudo service jenkins start
Starting jenkins (via systemctl):  Job for jenkins.service failed because the control process exited with error code. See "systemctl status jenkins.service" and "journalctl -xe" for details.
                                                           [FAILED]
```



**Install Java 1.8**

```
sudo yum install java-1.8.0
java -version
openjdk version "1.8.0_242"
OpenJDK Runtime Environment (build 1.8.0_242-b08)
OpenJDK 64-Bit Server VM (build 25.242-b08, mixed mode)
```



Now **Start Jenkins**

```
sudo service jenkins start
```



To stop Jenkins**

```
sudo service jenkins stop
```



**Connect to Jenkins via browser**

```
 http://<your_server_public_DNS>:8080
```



To **start the jenkins service at boot-up**, you can run,

```
chkconfig jenkins on
```

or

```
systemctl start jenkins.service
systemctl enable jenkins.service
```



**Get the password using below command** and paste it to Jenkins window with password request, 

```
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Install suggested plugins



##   Set Up Jenkins and Create Jenkins job: Selenium Tests (Python) 

- Preconditions: Jenkins installed on ec2 instance

- navigate to https://aws.amazon.com/console/

- login as root user

- open ec2 console

- start ec2 instance:  instances -> select  instance -> actions ->start 

- connect to instance (see above)

- If you creatin Jenkins job for the first time:

- install git:

  ```
  sudo yum install -y git
  ```

- install chtomedriver **- !important - use stable release supported by Chrome browser which will be installed in the next step**

  Installing chromedriver https://understandingdata.com/install-google-chrome-selenium-ec2-aws/

  ```
  [ec2-user@ip-172-31-9-135 tmp]$ pwd
  /tmp
  [ec2-user@ip-172-31-9-135 tmp]$ wget https://chromedriver.storage.googleapis.com/83.0.4103.14/chromedriver_linux64.zip
  [ec2-user@ip-172-31-9-135 tmp]$ sudo unzip chromedriver_linux64.zip
  Archive:  chromedriver_linux64.zip
    inflating: chromedriver
  [ec2-user@ip-172-31-9-135 tmp]$ sudo mv chromedriver /usr/bin/chromedriver
  [ec2-user@ip-172-31-9-135 tmp]$ chromedriver --version
  ```

  

- install Chrome browser 

  ```
  sudo curl https://intoli.com/install-google-chrome.sh
  google-chrome --version
  ```

- install pip

  ```
  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
  sudo python get-pip.py
  ```
  
- install virtualenv

  ``` 
  sudo python -m pip install virtualenv
  ```

- install python3

  ```
  sudo yum install -y python3
  ```

- start jenkins

- Jenkins--> System-->Global credentials (unrestricted)-->Add credentials

  - Username (use GitHub email)
  - Password  (use GitHub token, **NOT password**)
  - Description (GitHub)

- Jenkins --> Source Code Management --> GitHub project --> add Project url (copy from browser address bar)

- Jenkins --> Source Code Management -->Git --> add Repository url (copy from Clone/download)

- Jenkins-->  Source Code Management -->Build Triggers--> "H 8 * * *" - run once per day

- Jenkins-->  Source Code Management -->Build Environment--> "Delete workspace before build starts" 

- Jenkins-->  Source Code Management -->Build --> Execute shell-->Command

  ```
  virtualenv -p python3 venv
  source venv/bin/activate
  pip install -r requirements.txt
  pytest tests/login/test_login_valid.py -k test_site_title 
  ```

- Jenkins-->  Source Code Management--> Save

- Jenkins--> Project-->Build Now 



======

Run something as Jenkins

sudo -su jenkins

exit to finish session and go back to est-user

======







## Create Jenkins job - commands history and logs





```
▶ ssh -i /Users/maksim/Documents/2_SOFTWARE_TESTING/10_AWS/mk_zin-key-pair-southeast-2.pem  ec2-user@ec2-13-55-210-56.ap-southeast-2.compute.amazonaws.com
The authenticity of host 'ec2-13-55-210-56.ap-southeast-2.compute.amazonaws.com (13.55.210.56)' can't be established.
ECDSA key fingerprint is SHA256:+M47a5lnmKONWe8Zvq9JJcn5EFZUXs/nqoh9iU1Qe9M.
Are you sure you want to continue connecting (yes/no)? y
Please type 'yes' or 'no': yes
Warning: Permanently added 'ec2-13-55-210-56.ap-southeast-2.compute.amazonaws.com,13.55.210.56' (ECDSA) to the list of known hosts.
Last login: Sun Apr 19 07:56:24 2020 from 139.168.204.138

       __|  __|_  )
       _|  (     /   Amazon Linux 2 AMI
      ___|\___|___|

https://aws.amazon.com/amazon-linux-2/
[ec2-user@ip-172-31-9-135 ~]$ ll
total 0
[ec2-user@ip-172-31-9-135 ~]$ ls -la
total 16
drwx------ 3 ec2-user ec2-user  95 Apr 19 09:54 .
drwxr-xr-x 3 root     root      22 Apr 19 07:04 ..
-rw------- 1 ec2-user ec2-user 876 Apr 19 09:54 .bash_history
-rw-r--r-- 1 ec2-user ec2-user  18 Jan 16 00:56 .bash_logout
-rw-r--r-- 1 ec2-user ec2-user 193 Jan 16 00:56 .bash_profile
-rw-r--r-- 1 ec2-user ec2-user 231 Jan 16 00:56 .bashrc
drwx------ 2 ec2-user ec2-user  29 Apr 19 07:04 .ssh
[ec2-user@ip-172-31-9-135 ~]$ sudo service jenkins start
Starting jenkins (via systemctl):                          [  OK  ]
[ec2-user@ip-172-31-9-135 ~]$ git --version
-bash: git: command not found
[ec2-user@ip-172-31-9-135 ~]$ sudo yum install -y git
Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
amzn2-core                                                     | 2.4 kB  00:00:00
(1/3): amzn2-core/2/x86_64/group_gz                            | 2.5 kB  00:00:00
(2/3): amzn2-core/2/x86_64/updateinfo                          | 203 kB  00:00:00
(3/3): amzn2-core/2/x86_64/primary_db                          |  40 MB  00:00:00
Resolving Dependencies
--> Running transaction check
---> Package git.x86_64 0:2.23.1-1.amzn2.0.2 will be installed
--> Processing Dependency: perl-Git = 2.23.1-1.amzn2.0.2 for package: git-2.23.1-1.amzn2.0.2.x86_64
--> Processing Dependency: git-core-doc = 2.23.1-1.amzn2.0.2 for package: git-2.23.1-1.amzn2.0.2.x86_64
--> Processing Dependency: git-core = 2.23.1-1.amzn2.0.2 for package: git-2.23.1-1.amzn2.0.2.x86_64
--> Processing Dependency: emacs-filesystem >= 25.3 for package: git-2.23.1-1.amzn2.0.2.x86_64
--> Processing Dependency: perl(Term::ReadKey) for package: git-2.23.1-1.amzn2.0.2.x86_64
--> Processing Dependency: perl(Git::I18N) for package: git-2.23.1-1.amzn2.0.2.x86_64
--> Processing Dependency: perl(Git) for package: git-2.23.1-1.amzn2.0.2.x86_64
--> Processing Dependency: libsecret-1.so.0()(64bit) for package: git-2.23.1-1.amzn2.0.2.x86_64
--> Running transaction check
---> Package emacs-filesystem.noarch 1:25.3-3.amzn2.0.1 will be installed
---> Package git-core.x86_64 0:2.23.1-1.amzn2.0.2 will be installed
---> Package git-core-doc.noarch 0:2.23.1-1.amzn2.0.2 will be installed
---> Package libsecret.x86_64 0:0.18.5-2.amzn2.0.2 will be installed
---> Package perl-Git.noarch 0:2.23.1-1.amzn2.0.2 will be installed
--> Processing Dependency: perl(Error) for package: perl-Git-2.23.1-1.amzn2.0.2.noarch
---> Package perl-TermReadKey.x86_64 0:2.30-20.amzn2.0.2 will be installed
--> Running transaction check
---> Package perl-Error.noarch 1:0.17020-2.amzn2 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

======================================================================================
 Package                Arch         Version                   Repository        Size
======================================================================================
Installing:
 git                    x86_64       2.23.1-1.amzn2.0.2        amzn2-core       135 k
Installing for dependencies:
 emacs-filesystem       noarch       1:25.3-3.amzn2.0.1        amzn2-core        64 k
 git-core               x86_64       2.23.1-1.amzn2.0.2        amzn2-core       5.0 M
 git-core-doc           noarch       2.23.1-1.amzn2.0.2        amzn2-core       2.4 M
 libsecret              x86_64       0.18.5-2.amzn2.0.2        amzn2-core       153 k
 perl-Error             noarch       1:0.17020-2.amzn2         amzn2-core        32 k
 perl-Git               noarch       2.23.1-1.amzn2.0.2        amzn2-core        47 k
 perl-TermReadKey       x86_64       2.30-20.amzn2.0.2         amzn2-core        31 k

Transaction Summary
======================================================================================
Install  1 Package (+7 Dependent packages)

Total download size: 7.9 M
Installed size: 40 M
Downloading packages:
(1/8): emacs-filesystem-25.3-3.amzn2.0.1.noarch.rpm            |  64 kB  00:00:00
(2/8): git-2.23.1-1.amzn2.0.2.x86_64.rpm                       | 135 kB  00:00:00
(3/8): git-core-doc-2.23.1-1.amzn2.0.2.noarch.rpm              | 2.4 MB  00:00:00
(4/8): libsecret-0.18.5-2.amzn2.0.2.x86_64.rpm                 | 153 kB  00:00:00
(5/8): perl-Error-0.17020-2.amzn2.noarch.rpm                   |  32 kB  00:00:00
(6/8): git-core-2.23.1-1.amzn2.0.2.x86_64.rpm                  | 5.0 MB  00:00:00
(7/8): perl-Git-2.23.1-1.amzn2.0.2.noarch.rpm                  |  47 kB  00:00:00
(8/8): perl-TermReadKey-2.30-20.amzn2.0.2.x86_64.rpm           |  31 kB  00:00:00
--------------------------------------------------------------------------------------
Total                                                     22 MB/s | 7.9 MB  00:00
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : git-core-2.23.1-1.amzn2.0.2.x86_64                                 1/8
  Installing : git-core-doc-2.23.1-1.amzn2.0.2.noarch                             2/8
  Installing : 1:perl-Error-0.17020-2.amzn2.noarch                                3/8
  Installing : perl-TermReadKey-2.30-20.amzn2.0.2.x86_64                          4/8
  Installing : libsecret-0.18.5-2.amzn2.0.2.x86_64                                5/8
  Installing : 1:emacs-filesystem-25.3-3.amzn2.0.1.noarch                         6/8
  Installing : perl-Git-2.23.1-1.amzn2.0.2.noarch                                 7/8
  Installing : git-2.23.1-1.amzn2.0.2.x86_64                                      8/8
  Verifying  : git-2.23.1-1.amzn2.0.2.x86_64                                      1/8
  Verifying  : 1:emacs-filesystem-25.3-3.amzn2.0.1.noarch                         2/8
  Verifying  : libsecret-0.18.5-2.amzn2.0.2.x86_64                                3/8
  Verifying  : perl-TermReadKey-2.30-20.amzn2.0.2.x86_64                          4/8
  Verifying  : perl-Git-2.23.1-1.amzn2.0.2.noarch                                 5/8
  Verifying  : git-core-2.23.1-1.amzn2.0.2.x86_64                                 6/8
  Verifying  : 1:perl-Error-0.17020-2.amzn2.noarch                                7/8
  Verifying  : git-core-doc-2.23.1-1.amzn2.0.2.noarch                             8/8

Installed:
  git.x86_64 0:2.23.1-1.amzn2.0.2

Dependency Installed:
  emacs-filesystem.noarch 1:25.3-3.amzn2.0.1   git-core.x86_64 0:2.23.1-1.amzn2.0.2
  git-core-doc.noarch 0:2.23.1-1.amzn2.0.2     libsecret.x86_64 0:0.18.5-2.amzn2.0.2
  perl-Error.noarch 1:0.17020-2.amzn2          perl-Git.noarch 0:2.23.1-1.amzn2.0.2
  perl-TermReadKey.x86_64 0:2.30-20.amzn2.0.2

Complete!
[ec2-user@ip-172-31-9-135 ~]$ cd /tmp
[ec2-user@ip-172-31-9-135 tmp]$ git clone https://github.com/MaksimZinovev/aerofiler-pytest.git
Cloning into 'aerofiler-pytest'...
Username for 'https://github.com': MaksimZinovev
Password for 'https://MaksimZinovev@github.com':
remote: Invalid username or password.
fatal: Authentication failed for 'https://github.com/MaksimZinovev/aerofiler-pytest.git/'
[ec2-user@ip-172-31-9-135 tmp]$ git clone https://github.com/MaksimZinovev/aerofiler-pytest.git
Cloning into 'aerofiler-pytest'...
Username for 'https://github.com': maksimzinovevsubmit@gmail.com
Password for 'https://maksimzinovevsubmit@gmail.com@github.com':
remote: Invalid username or password.
fatal: Authentication failed for 'https://github.com/MaksimZinovev/aerofiler-pytest.git/'
[ec2-user@ip-172-31-9-135 tmp]$ git clone https://github.com/MaksimZinovev/aerofiler-pytest.git
Cloning into 'aerofiler-pytest'...
Username for 'https://github.com': MaksimZinovev
Password for 'https://MaksimZinovev@github.com':
remote: Enumerating objects: 635, done.
remote: Counting objects: 100% (635/635), done.
remote: Compressing objects: 100% (282/282), done.
remote: Total 635 (delta 326), reused 628 (delta 323), pack-reused 0
Receiving objects: 100% (635/635), 677.60 KiB | 844.00 KiB/s, done.
Resolving deltas: 100% (326/326), done.
[ec2-user@ip-172-31-9-135 tmp]$ pwd
/tmp
[ec2-user@ip-172-31-9-135 tmp]$ wget https://chromedriver.storage.googleapis.com/83.0.4103.14/chromedriver_linux64.zip
--2020-04-25 05:10:14--  https://chromedriver.storage.googleapis.com/83.0.4103.14/chromedriver_linux64.zip
Resolving chromedriver.storage.googleapis.com (chromedriver.storage.googleapis.com)... 172.217.25.144, 2404:6800:4006:804::2010
Connecting to chromedriver.storage.googleapis.com (chromedriver.storage.googleapis.com)|172.217.25.144|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 5208334 (5.0M) [application/zip]
Saving to: ‘chromedriver_linux64.zip’

100%[======================================>] 5,208,334   --.-K/s   in 0.07s

2020-04-25 05:10:14 (67.0 MB/s) - ‘chromedriver_linux64.zip’ saved [5208334/5208334]

[ec2-user@ip-172-31-9-135 tmp]$ ls
aerofiler-pytest
akuma4706740710166255455jar
akuma796521989446258153jar
chromedriver_linux64.zip
hsperfdata_ec2-user
hsperfdata_jenkins
hsperfdata_root
jetty-0_0_0_0-8080-war-_-any-1949807998560654925.dir
jetty-0_0_0_0-8080-war-_-any-4363885720030732656.dir
jna1994348788991608150jar
jna3660287464293344091jar
systemd-private-5298c4cbc22e4a6082bc500cab27a34d-chronyd.service-31dtbE
winstone2906487597864836434.jar
winstone724034183948416490.jar
[ec2-user@ip-172-31-9-135 tmp]$ sudo unzip chromedriver_linux64.zip
Archive:  chromedriver_linux64.zip
  inflating: chromedriver
[ec2-user@ip-172-31-9-135 tmp]$ sudo mv chromedriver /usr/bin/chromedriver
[ec2-user@ip-172-31-9-135 tmp]$ chromedriver --version
ChromeDriver 83.0.4103.14 (be04594a2b8411758b860104bc0a1033417178be-refs/branch-heads/4103@{#119})
[ec2-user@ip-172-31-9-135 tmp]$ sudo curl https://intoli.com/install-google-chrome.sh
#! /bin/bash


# Copyright 2017-present: Intoli, LLC
# Source: https://intoli.com/blog/installing-google-chrome-on-centos/
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


# What this script does is explained in detail in a blog post located at:
# https://intoli.com/blog/installing-google-chrome-on-centos/
# If you're trying to figure out how things work, then you should visit that!


# Require that this runs as root.
[ "$UID" -eq 0 ] || exec sudo "$0" "$@"


# Define some global variables.
working_directory="/tmp/google-chrome-installation"
repo_file="/etc/yum.repos.d/google-chrome.repo"


# Work in our working directory.
echo "Working in ${working_directory}"
mkdir -p ${working_directory}
rm -rf ${working_directory}/*
pushd ${working_directory}


# Add the official Google Chrome Centos 7 repo.
echo "Configuring the Google Chrome repo in ${repo_file}"
echo "[google-chrome]" > $repo_file
echo "name=google-chrome" >> $repo_file
echo "baseurl=http://dl.google.com/linux/chrome/rpm/stable/\$basearch" >> $repo_file
echo "enabled=1" >> $repo_file
echo "gpgcheck=1" >> $repo_file
echo "gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub" >> $repo_file


# Install the Google Chrome signing key.
yum install -y wget
wget https://dl.google.com/linux/linux_signing_key.pub
rpm --import linux_signing_key.pub


# A helper to make sure that Chrome is linked correctly
function installation_status() {
    google-chrome-stable --version > /dev/null 2>&1
    [ $? -eq 0 ]
}


# Try it the old fashioned way, should work on RHEL 7.X.
echo "Attempting a direction installation with yum."
yum install -y google-chrome-stable
if [ $? -eq 0 ]
then
    if installation_status; then
        # Print out the success message.
        echo "Successfully installed Google Chrome!"
        rm -rf ${working_directory}
        popd > /dev/null
        exit 0
    fi
fi


# Uninstall any existing/partially installed versions.
yum --setopt=tsflags=noscripts -y remove google-chrome-stable


# Install yumdownloader/repoquery and download the latest RPM.
echo "Downloading the Google Chrome RPM file."
yum install -y yum-utils
# There have been issues in the past with the Chrome repository, so we fall back to downloading
# the latest RPM directly if the package isn't available there. For further details:
# https://productforums.google.com/forum/#!topic/chrome/xNtfk_wAUC4;context-place=forum/chrome
yumdownloader google-chrome-stable || \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
rpm_file=$(echo *.rpm)
echo "Downloaded ${rpm_file}"


# Install the RPM in a broken state.
rpm -ih --nodeps ${rpm_file}
rm ${rpm_file}


# Install font dependencies, see: https://bugs.chromium.org/p/chromium/issues/detail?id=782161
echo "Installing the required font dependencies."
yum install -y \
    fontconfig \
    fontpackages-filesystem \
    ipa-gothic-fonts \
    xorg-x11-fonts-100dpi \
    xorg-x11-fonts-75dpi \
    xorg-x11-fonts-misc \
    xorg-x11-fonts-Type1 \
    xorg-x11-utils


# Helper function to install packages in the chroot by name (as an argument).
function install_package() {
    # We'll leave the RPMs around to avoid redownloading things.
    if [ -f "$1.rpm" ]; then
        return 0
    fi

    # Find the URL for the package.
    url=$(repoquery --repofrompath=centos7,http://mirror.centos.org/centos/7/os/`arch` \
        --repoid=centos7 -q --qf="%{location}" "$1" | \
        sed s/x86_64.rpm$/`arch`.rpm/ | \
        sed s/i686.rpm$/`arch`.rpm/g | \
        sort -u
    )

    # Download the RPM.
    wget "${url}" -O "$1.rpm"

    # Extract it.
    echo "Extracting $1..."
    rpm2cpio $1.rpm | cpio -idmv > /dev/null 2>&1
}


# Install glibc/ld-linux from CentOS 7.
install_package glibc


# Make the library directory and copy over glibc/ld-linux.
lib_directory=/opt/google/chrome/lib
mkdir -p $lib_directory
cp ./lib/* $lib_directory/ 2> /dev/null
cp ./lib64/* $lib_directory/ 2> /dev/null


# Install `mount` and its mandatory dependencies from CentOS 7.
for package in "glibc" "util-linux" "libmount" "libblkid" "libuuid" "libselinux" "pcre"; do
    install_package "${package}"
done


# Create an `ldd.sh` script to mimic the behavior of `ldd` within the namespace (without bash, etc. dependencies).
echo '#!/bin/bash' > ldd.sh
echo '' >> ldd.sh
echo '# Usage: ldd.sh LIBRARY_PATH EXECUTABLE' >> ldd.sh
echo 'mount --make-rprivate /' >> ldd.sh
echo 'unshare -m bash -c "`tail -n +7 $0`" "$0" "$@"' >> ldd.sh
echo 'exit $?' >> ldd.sh
echo '' >> ldd.sh
echo 'LD=$({ ls -1 ${1}/ld-linux* | head -n1 ; } 2> /dev/null)' >> ldd.sh
echo 'mount --make-private -o remount /' >> ldd.sh
echo 'mount --bind ${1} $(dirname "$({ ls -1 /lib/ld-linux* /lib64/ld-linux* | head -n1 ; } 2> /dev/null)")' >> ldd.sh
echo 'for directory in lib lib64 usr/lib usr/lib64; do' >> ldd.sh
echo '    PATH=./:./bin:./usr/bin LD_LIBRARY_PATH=${1}:./lib64:./usr/lib64:./lib:./usr/lib mount --bind ${1} /${directory} 2> /dev/null' >> ldd.sh
echo 'done' >> ldd.sh
echo 'echo -n "$(LD_TRACE_LOADED_OBJECTS=1 LD_LIBRARY_PATH="${1}" "${LD}" "${2}")"' >> ldd.sh
chmod a+x ldd.sh


# Takes the executable as an argument and recursively installs all missing dependencies.
function install_missing_dependencies() {
    executable="${1}"
    # Loop through and install missing dependencies.
    while true
    do
        finished=true
        # Loop through each of the missing libraries for this round.
        while read -r line
        do
            # Parse the various library listing formats.
            if [[ $line == *"/"* ]]; then
                # Extract the filename when a path is present (e.g. /lib64/).
                file=`echo $line | sed 's>.*/\([^/:]*\):.*>\1>'`
            else
                # Extract the filename for missing libraries without a path.
                file=`echo $line | awk '{print $1;}'`
            fi

            if [ -z $file ]; then
                continue
            fi

            # We'll require an empty round before completing.
            finished=false

            echo "Finding dependency for ${file}"

            # Find the package name for this library.
            package=$(repoquery --repofrompath=centos7,http://mirror.centos.org/centos/7/os/`arch` \
                --repoid=centos7 -q --qf="%{name}" --whatprovides "$file" | head -n1)

            install_package "${package}"

            # Copy it over to our library directory.
            find . | grep /${file} | xargs -n1 -I{} cp {} ${lib_directory}/
        done <<< "$(./ldd.sh "${lib_directory}" "${executable}" 2>&1 | grep -e "no version information" -e "not found")"

        # Break once no new files have been copied in a loop.
        if [ "$finished" = true ]; then
            break
        fi
    done
}


# Install the missing dependencies for Chrome.
install_missing_dependencies /opt/google/chrome/chrome


if ! installation_status; then
    # Time for the big guns, we'll try to patch the executables to use our lib directory.
    yum install -y gcc gcc-c++ make autoconf automake
    echo "Linking issues were encountered, attempting to patch the `chrome` executable."
    wget https://github.com/NixOS/patchelf/archive/0.9.tar.gz -O 0.9.tar.gz
    tar zxf 0.9.tar.gz
    pushd patchelf-0.9
    ./bootstrap.sh
    ./configure
    make
    LD="$({ ls -1 ${lib_directory}/ld-linux* | head -n1 ; } 2> /dev/null)"
    ./src/patchelf --set-interpreter "${LD}" --set-rpath "${lib_directory}" /opt/google/chrome/chrome
    ./src/patchelf --set-interpreter "${LD}" --set-rpath "${lib_directory}" /opt/google/chrome/chrome-sandbox
    sed -i 's/\(.*exec cat.*\)/LD_LIBRARY_PATH="" \1/g' /opt/google/chrome/google-chrome
    popd > /dev/null
    echo "Attempted experimental patching of Chrome to use a relocated glibc version."
fi

# Clean up the directory stack.
rm -rf ${working_directory}
popd > /dev/null

# Print out the success status message and exit.
version="$(google-chrome-stable --version)"
if [ $? -eq 0 ]; then
    echo "Successfully installed google-chrome-stable, ${version}."
    exit 0
else
    echo "Installation has failed."
    echo "Please email contact@intoli.com with the details of your operating system."
    echo "If you're using using AWS, please include the AMI identifier for the instance."
    exit 1
fi
[ec2-user@ip-172-31-9-135 tmp]$ sudo curl https://intoli.com/install-google-chrome.sh | bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  9526  100  9526    0     0   9861      0 --:--:-- --:--:-- --:--:--  9851
Working in /tmp/google-chrome-installation
/tmp/google-chrome-installation /tmp
Configuring the Google Chrome repo in /etc/yum.repos.d/google-chrome.repo
Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
amzn2-core                                               | 2.4 kB     00:00
google-chrome                                            | 1.3 kB     00:00
google-chrome/x86_64/primary                               | 1.7 kB   00:00
google-chrome                                                               3/3
Package wget-1.14-18.amzn2.1.x86_64 already installed and latest version
Nothing to do
--2020-04-25 05:14:10--  https://dl.google.com/linux/linux_signing_key.pub
Resolving dl.google.com (dl.google.com)... 216.58.203.110, 2404:6800:4006:809::200e
Connecting to dl.google.com (dl.google.com)|216.58.203.110|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 10218 (10.0K) [application/octet-stream]
Saving to: ‘linux_signing_key.pub’

100%[======================================>] 10,218      --.-K/s   in 0.02s

2020-04-25 05:14:10 (531 KB/s) - ‘linux_signing_key.pub’ saved [10218/10218]

Attempting a direction installation with yum.
Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
Resolving Dependencies
--> Running transaction check
---> Package google-chrome-stable.x86_64 0:81.0.4044.122-1 will be installed
--> Processing Dependency: xdg-utils for package: google-chrome-stable-81.0.4044.122-1.x86_64
--> Processing Dependency: liberation-fonts for package: google-chrome-stable-81.0.4044.122-1.x86_64
--> Processing Dependency: libgdk-3.so.0()(64bit) for package: google-chrome-stable-81.0.4044.122-1.x86_64
--> Processing Dependency: libatspi.so.0()(64bit) for package: google-chrome-stable-81.0.4044.122-1.x86_64
--> Processing Dependency: libXss.so.1()(64bit) for package: google-chrome-stable-81.0.4044.122-1.x86_64
--> Processing Dependency: libappindicator3.so.1()(64bit) for package: google-chrome-stable-81.0.4044.122-1.x86_64
--> Processing Dependency: libgtk-3.so.0()(64bit) for package: google-chrome-stable-81.0.4044.122-1.x86_64
--> Processing Dependency: libvulkan.so.1()(64bit) for package: google-chrome-stable-81.0.4044.122-1.x86_64
--> Processing Dependency: libatk-bridge-2.0.so.0()(64bit) for package: google-chrome-stable-81.0.4044.122-1.x86_64
--> Running transaction check
---> Package at-spi2-atk.x86_64 0:2.22.0-2.amzn2.0.2 will be installed
---> Package at-spi2-core.x86_64 0:2.22.0-1.amzn2.0.2 will be installed
---> Package gtk3.x86_64 0:3.22.30-3.amzn2 will be installed
--> Processing Dependency: libwayland-cursor(x86-64) >= 1.9.91 for package: gtk3-3.22.30-3.amzn2.x86_64
--> Processing Dependency: libepoxy(x86-64) >= 1.0 for package: gtk3-3.22.30-3.amzn2.x86_64
--> Processing Dependency: cairo-gobject(x86-64) >= 1.14.0 for package: gtk3-3.22.30-3.amzn2.x86_64
--> Processing Dependency: libxkbcommon.so.0(V_0.5.0)(64bit) for package: gtk3-3.22.30-3.amzn2.x86_64
--> Processing Dependency: dconf(x86-64) for package: gtk3-3.22.30-3.amzn2.x86_64
--> Processing Dependency: adwaita-icon-theme for package: gtk3-3.22.30-3.amzn2.x86_64
--> Processing Dependency: libxkbcommon.so.0()(64bit) for package: gtk3-3.22.30-3.amzn2.x86_64
--> Processing Dependency: libwayland-egl.so.1()(64bit) for package: gtk3-3.22.30-3.amzn2.x86_64
--> Processing Dependency: libwayland-cursor.so.0()(64bit) for package: gtk3-3.22.30-3.amzn2.x86_64
--> Processing Dependency: librest-0.7.so.0()(64bit) for package: gtk3-3.22.30-3.amzn2.x86_64
--> Processing Dependency: libjson-glib-1.0.so.0()(64bit) for package: gtk3-3.22.30-3.amzn2.x86_64
--> Processing Dependency: libepoxy.so.0()(64bit) for package: gtk3-3.22.30-3.amzn2.x86_64
--> Processing Dependency: libcolord.so.2()(64bit) for package: gtk3-3.22.30-3.amzn2.x86_64
--> Processing Dependency: libcairo-gobject.so.2()(64bit) for package: gtk3-3.22.30-3.amzn2.x86_64
---> Package libXScrnSaver.x86_64 0:1.2.2-6.1.amzn2.0.2 will be installed
---> Package libappindicator-gtk3.x86_64 0:12.10.0-13.amzn2.0.1 will be installed
--> Processing Dependency: libindicator3.so.7()(64bit) for package: libappindicator-gtk3-12.10.0-13.amzn2.0.1.x86_64
--> Processing Dependency: libdbusmenu-gtk3.so.4()(64bit) for package: libappindicator-gtk3-12.10.0-13.amzn2.0.1.x86_64
--> Processing Dependency: libdbusmenu-glib.so.4()(64bit) for package: libappindicator-gtk3-12.10.0-13.amzn2.0.1.x86_64
---> Package liberation-fonts.noarch 1:1.07.2-16.amzn2 will be installed
--> Processing Dependency: liberation-serif-fonts = 1:1.07.2-16.amzn2 for package: 1:liberation-fonts-1.07.2-16.amzn2.noarch
--> Processing Dependency: liberation-sans-fonts = 1:1.07.2-16.amzn2 for package: 1:liberation-fonts-1.07.2-16.amzn2.noarch
--> Processing Dependency: liberation-narrow-fonts = 1:1.07.2-16.amzn2 for package: 1:liberation-fonts-1.07.2-16.amzn2.noarch
--> Processing Dependency: liberation-mono-fonts = 1:1.07.2-16.amzn2 for package: 1:liberation-fonts-1.07.2-16.amzn2.noarch
---> Package vulkan.x86_64 0:1.0.61.1-2.amzn2 will be installed
--> Processing Dependency: vulkan-filesystem = 1.0.61.1-2.amzn2 for package: vulkan-1.0.61.1-2.amzn2.x86_64
---> Package xdg-utils.noarch 0:1.1.0-0.17.20120809git.amzn2 will be installed
--> Processing Dependency: desktop-file-utils for package: xdg-utils-1.1.0-0.17.20120809git.amzn2.noarch
--> Running transaction check
---> Package adwaita-icon-theme.noarch 0:3.26.0-1.amzn2 will be installed
--> Processing Dependency: adwaita-cursor-theme = 3.26.0-1.amzn2 for package: adwaita-icon-theme-3.26.0-1.amzn2.noarch
---> Package cairo-gobject.x86_64 0:1.15.12-4.amzn2 will be installed
--> Processing Dependency: cairo(x86-64) = 1.15.12-4.amzn2 for package: cairo-gobject-1.15.12-4.amzn2.x86_64
---> Package colord-libs.x86_64 0:1.3.4-1.amzn2.0.2 will be installed
--> Processing Dependency: libgusb.so.2(LIBGUSB_0.1.1)(64bit) for package: colord-libs-1.3.4-1.amzn2.0.2.x86_64
--> Processing Dependency: libgusb.so.2(LIBGUSB_0.1.0)(64bit) for package: colord-libs-1.3.4-1.amzn2.0.2.x86_64
--> Processing Dependency: libusb-1.0.so.0()(64bit) for package: colord-libs-1.3.4-1.amzn2.0.2.x86_64
--> Processing Dependency: liblcms2.so.2()(64bit) for package: colord-libs-1.3.4-1.amzn2.0.2.x86_64
--> Processing Dependency: libgusb.so.2()(64bit) for package: colord-libs-1.3.4-1.amzn2.0.2.x86_64
---> Package dconf.x86_64 0:0.28.0-4.amzn2 will be installed
---> Package desktop-file-utils.x86_64 0:0.23-2.amzn2 will be installed
---> Package json-glib.x86_64 0:1.4.2-2.amzn2 will be installed
---> Package libdbusmenu.x86_64 0:16.04.0-4.amzn2.0.2 will be installed
---> Package libdbusmenu-gtk3.x86_64 0:16.04.0-4.amzn2.0.2 will be installed
---> Package libepoxy.x86_64 0:1.3.1-2.amzn2 will be installed
---> Package liberation-mono-fonts.noarch 1:1.07.2-16.amzn2 will be installed
--> Processing Dependency: liberation-fonts-common = 1:1.07.2-16.amzn2 for package: 1:liberation-mono-fonts-1.07.2-16.amzn2.noarch
---> Package liberation-narrow-fonts.noarch 1:1.07.2-16.amzn2 will be installed
---> Package liberation-sans-fonts.noarch 1:1.07.2-16.amzn2 will be installed
---> Package liberation-serif-fonts.noarch 1:1.07.2-16.amzn2 will be installed
---> Package libindicator-gtk3.x86_64 0:12.10.1-6.amzn2.0.2 will be installed
---> Package libwayland-cursor.x86_64 0:1.17.0-1.amzn2 will be installed
---> Package libwayland-egl.x86_64 0:1.17.0-1.amzn2 will be installed
---> Package libxkbcommon.x86_64 0:0.7.1-3.amzn2 will be installed
--> Processing Dependency: xkeyboard-config for package: libxkbcommon-0.7.1-3.amzn2.x86_64
---> Package rest.x86_64 0:0.8.0-2.amzn2 will be installed
--> Processing Dependency: libsoup-gnome-2.4.so.1()(64bit) for package: rest-0.8.0-2.amzn2.x86_64
--> Processing Dependency: libsoup-2.4.so.1()(64bit) for package: rest-0.8.0-2.amzn2.x86_64
---> Package vulkan-filesystem.noarch 0:1.0.61.1-2.amzn2 will be installed
--> Running transaction check
---> Package adwaita-cursor-theme.noarch 0:3.26.0-1.amzn2 will be installed
---> Package cairo.x86_64 0:1.14.8-2.amzn2.0.2 will be updated
---> Package cairo.x86_64 0:1.15.12-4.amzn2 will be an update
---> Package lcms2.x86_64 0:2.6-3.amzn2.0.2 will be installed
---> Package liberation-fonts-common.noarch 1:1.07.2-16.amzn2 will be installed
---> Package libgusb.x86_64 0:0.2.9-1.amzn2.0.2 will be installed
---> Package libsoup.x86_64 0:2.56.0-6.amzn2 will be installed
--> Processing Dependency: glib-networking(x86-64) >= 2.38.0 for package: libsoup-2.56.0-6.amzn2.x86_64
---> Package libusbx.x86_64 0:1.0.21-1.amzn2 will be installed
---> Package xkeyboard-config.noarch 0:2.20-1.amzn2 will be installed
--> Running transaction check
---> Package glib-networking.x86_64 0:2.56.1-1.amzn2 will be installed
--> Processing Dependency: libgnutls.so.28(GNUTLS_3_1_0)(64bit) for package: glib-networking-2.56.1-1.amzn2.x86_64
--> Processing Dependency: libgnutls.so.28(GNUTLS_3_0_0)(64bit) for package: glib-networking-2.56.1-1.amzn2.x86_64
--> Processing Dependency: libgnutls.so.28(GNUTLS_2_12)(64bit) for package: glib-networking-2.56.1-1.amzn2.x86_64
--> Processing Dependency: libgnutls.so.28(GNUTLS_1_4)(64bit) for package: glib-networking-2.56.1-1.amzn2.x86_64
--> Processing Dependency: gsettings-desktop-schemas for package: glib-networking-2.56.1-1.amzn2.x86_64
--> Processing Dependency: libproxy.so.1()(64bit) for package: glib-networking-2.56.1-1.amzn2.x86_64
--> Processing Dependency: libgnutls.so.28()(64bit) for package: glib-networking-2.56.1-1.amzn2.x86_64
--> Running transaction check
---> Package gnutls.x86_64 0:3.3.29-9.amzn2 will be installed
--> Processing Dependency: trousers >= 0.3.11.2 for package: gnutls-3.3.29-9.amzn2.x86_64
--> Processing Dependency: libnettle.so.4()(64bit) for package: gnutls-3.3.29-9.amzn2.x86_64
--> Processing Dependency: libhogweed.so.2()(64bit) for package: gnutls-3.3.29-9.amzn2.x86_64
---> Package gsettings-desktop-schemas.x86_64 0:3.28.0-2.amzn2 will be installed
---> Package libproxy.x86_64 0:0.4.11-10.amzn2.0.3 will be installed
--> Processing Dependency: libmodman.so.1()(64bit) for package: libproxy-0.4.11-10.amzn2.0.3.x86_64
--> Running transaction check
---> Package libmodman.x86_64 0:2.0.1-8.amzn2.0.2 will be installed
---> Package nettle.x86_64 0:2.7.1-8.amzn2.0.2 will be installed
---> Package trousers.x86_64 0:0.3.14-2.amzn2.0.2 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

================================================================================
 Package                   Arch   Version                   Repository     Size
================================================================================
Installing:
 google-chrome-stable      x86_64 81.0.4044.122-1           google-chrome  64 M
Installing for dependencies:
 adwaita-cursor-theme      noarch 3.26.0-1.amzn2            amzn2-core    641 k
 adwaita-icon-theme        noarch 3.26.0-1.amzn2            amzn2-core     12 M
 at-spi2-atk               x86_64 2.22.0-2.amzn2.0.2        amzn2-core     81 k
 at-spi2-core              x86_64 2.22.0-1.amzn2.0.2        amzn2-core    159 k
 cairo-gobject             x86_64 1.15.12-4.amzn2           amzn2-core     26 k
 colord-libs               x86_64 1.3.4-1.amzn2.0.2         amzn2-core    186 k
 dconf                     x86_64 0.28.0-4.amzn2            amzn2-core    105 k
 desktop-file-utils        x86_64 0.23-2.amzn2              amzn2-core     68 k
 glib-networking           x86_64 2.56.1-1.amzn2            amzn2-core    144 k
 gnutls                    x86_64 3.3.29-9.amzn2            amzn2-core    673 k
 gsettings-desktop-schemas x86_64 3.28.0-2.amzn2            amzn2-core    606 k
 gtk3                      x86_64 3.22.30-3.amzn2           amzn2-core    4.4 M
 json-glib                 x86_64 1.4.2-2.amzn2             amzn2-core    133 k
 lcms2                     x86_64 2.6-3.amzn2.0.2           amzn2-core    152 k
 libXScrnSaver             x86_64 1.2.2-6.1.amzn2.0.2       amzn2-core     24 k
 libappindicator-gtk3      x86_64 12.10.0-13.amzn2.0.1      amzn2-core     37 k
 libdbusmenu               x86_64 16.04.0-4.amzn2.0.2       amzn2-core    133 k
 libdbusmenu-gtk3          x86_64 16.04.0-4.amzn2.0.2       amzn2-core     35 k
 libepoxy                  x86_64 1.3.1-2.amzn2             amzn2-core    198 k
 liberation-fonts          noarch 1:1.07.2-16.amzn2         amzn2-core     13 k
 liberation-fonts-common   noarch 1:1.07.2-16.amzn2         amzn2-core     27 k
 liberation-mono-fonts     noarch 1:1.07.2-16.amzn2         amzn2-core    228 k
 liberation-narrow-fonts   noarch 1:1.07.2-16.amzn2         amzn2-core    202 k
 liberation-sans-fonts     noarch 1:1.07.2-16.amzn2         amzn2-core    279 k
 liberation-serif-fonts    noarch 1:1.07.2-16.amzn2         amzn2-core    298 k
 libgusb                   x86_64 0.2.9-1.amzn2.0.2         amzn2-core     40 k
 libindicator-gtk3         x86_64 12.10.1-6.amzn2.0.2       amzn2-core     63 k
 libmodman                 x86_64 2.0.1-8.amzn2.0.2         amzn2-core     29 k
 libproxy                  x86_64 0.4.11-10.amzn2.0.3       amzn2-core     61 k
 libsoup                   x86_64 2.56.0-6.amzn2            amzn2-core    401 k
 libusbx                   x86_64 1.0.21-1.amzn2            amzn2-core     62 k
 libwayland-cursor         x86_64 1.17.0-1.amzn2            amzn2-core     22 k
 libwayland-egl            x86_64 1.17.0-1.amzn2            amzn2-core     15 k
 libxkbcommon              x86_64 0.7.1-3.amzn2             amzn2-core    110 k
 nettle                    x86_64 2.7.1-8.amzn2.0.2         amzn2-core    329 k
 rest                      x86_64 0.8.0-2.amzn2             amzn2-core     63 k
 trousers                  x86_64 0.3.14-2.amzn2.0.2        amzn2-core    294 k
 vulkan                    x86_64 1.0.61.1-2.amzn2          amzn2-core    1.2 M
 vulkan-filesystem         noarch 1.0.61.1-2.amzn2          amzn2-core    6.2 k
 xdg-utils                 noarch 1.1.0-0.17.20120809git.amzn2
                                                            amzn2-core     70 k
 xkeyboard-config          noarch 2.20-1.amzn2              amzn2-core    799 k
Updating for dependencies:
 cairo                     x86_64 1.15.12-4.amzn2           amzn2-core    732 k

Transaction Summary
================================================================================
Install  1 Package  (+41 Dependent packages)
Upgrade             (  1 Dependent package)

Total download size: 89 M
Downloading packages:
Delta RPMs disabled because /usr/bin/applydeltarpm not installed.
(1/43): adwaita-cursor-theme-3.26.0-1.amzn2.noarch.rpm     | 641 kB   00:00
(2/43): at-spi2-atk-2.22.0-2.amzn2.0.2.x86_64.rpm          |  81 kB   00:00
(3/43): at-spi2-core-2.22.0-1.amzn2.0.2.x86_64.rpm         | 159 kB   00:00
(4/43): cairo-1.15.12-4.amzn2.x86_64.rpm                   | 732 kB   00:00
(5/43): cairo-gobject-1.15.12-4.amzn2.x86_64.rpm           |  26 kB   00:00
(6/43): colord-libs-1.3.4-1.amzn2.0.2.x86_64.rpm           | 186 kB   00:00
(7/43): dconf-0.28.0-4.amzn2.x86_64.rpm                    | 105 kB   00:00
(8/43): desktop-file-utils-0.23-2.amzn2.x86_64.rpm         |  68 kB   00:00
(9/43): glib-networking-2.56.1-1.amzn2.x86_64.rpm          | 144 kB   00:00
(10/43): adwaita-icon-theme-3.26.0-1.amzn2.noarch.rpm      |  12 MB   00:00
(11/43): gnutls-3.3.29-9.amzn2.x86_64.rpm                  | 673 kB   00:00
(12/43): gsettings-desktop-schemas-3.28.0-2.amzn2.x86_64.r | 606 kB   00:00
(13/43): json-glib-1.4.2-2.amzn2.x86_64.rpm                | 133 kB   00:00
(14/43): lcms2-2.6-3.amzn2.0.2.x86_64.rpm                  | 152 kB   00:00
(15/43): libXScrnSaver-1.2.2-6.1.amzn2.0.2.x86_64.rpm      |  24 kB   00:00
(16/43): libappindicator-gtk3-12.10.0-13.amzn2.0.1.x86_64. |  37 kB   00:00
(17/43): gtk3-3.22.30-3.amzn2.x86_64.rpm                   | 4.4 MB   00:00
(18/43): libdbusmenu-16.04.0-4.amzn2.0.2.x86_64.rpm        | 133 kB   00:00
(19/43): libdbusmenu-gtk3-16.04.0-4.amzn2.0.2.x86_64.rpm   |  35 kB   00:00
(20/43): libepoxy-1.3.1-2.amzn2.x86_64.rpm                 | 198 kB   00:00
(21/43): liberation-fonts-common-1.07.2-16.amzn2.noarch.rp |  27 kB   00:00
(22/43): liberation-fonts-1.07.2-16.amzn2.noarch.rpm       |  13 kB   00:00
(23/43): liberation-narrow-fonts-1.07.2-16.amzn2.noarch.rp | 202 kB   00:00
(24/43): liberation-mono-fonts-1.07.2-16.amzn2.noarch.rpm  | 228 kB   00:00
(25/43): liberation-sans-fonts-1.07.2-16.amzn2.noarch.rpm  | 279 kB   00:00
(26/43): libgusb-0.2.9-1.amzn2.0.2.x86_64.rpm              |  40 kB   00:00
(27/43): libindicator-gtk3-12.10.1-6.amzn2.0.2.x86_64.rpm  |  63 kB   00:00
(28/43): liberation-serif-fonts-1.07.2-16.amzn2.noarch.rpm | 298 kB   00:00
(29/43): libmodman-2.0.1-8.amzn2.0.2.x86_64.rpm            |  29 kB   00:00
(30/43): libproxy-0.4.11-10.amzn2.0.3.x86_64.rpm           |  61 kB   00:00
(31/43): libsoup-2.56.0-6.amzn2.x86_64.rpm                 | 401 kB   00:00
(32/43): libusbx-1.0.21-1.amzn2.x86_64.rpm                 |  62 kB   00:00
(33/43): libwayland-egl-1.17.0-1.amzn2.x86_64.rpm          |  15 kB   00:00
(34/43): libwayland-cursor-1.17.0-1.amzn2.x86_64.rpm       |  22 kB   00:00
(35/43): libxkbcommon-0.7.1-3.amzn2.x86_64.rpm             | 110 kB   00:00
(36/43): rest-0.8.0-2.amzn2.x86_64.rpm                     |  63 kB   00:00
(37/43): nettle-2.7.1-8.amzn2.0.2.x86_64.rpm               | 329 kB   00:00
(38/43): trousers-0.3.14-2.amzn2.0.2.x86_64.rpm            | 294 kB   00:00
(39/43): vulkan-filesystem-1.0.61.1-2.amzn2.noarch.rpm     | 6.2 kB   00:00
(40/43): vulkan-1.0.61.1-2.amzn2.x86_64.rpm                | 1.2 MB   00:00
(41/43): xdg-utils-1.1.0-0.17.20120809git.amzn2.noarch.rpm |  70 kB   00:00
(42/43): xkeyboard-config-2.20-1.amzn2.noarch.rpm          | 799 kB   00:00
(43/43): google-chrome-stable-81.0.4044.122-1.x86_64.rpm   |  64 MB   00:03
--------------------------------------------------------------------------------
Total                                               21 MB/s |  89 MB  00:04
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Updating   : cairo-1.15.12-4.amzn2.x86_64                                1/44
  Installing : 1:liberation-fonts-common-1.07.2-16.amzn2.noarch            2/44
  Installing : cairo-gobject-1.15.12-4.amzn2.x86_64                        3/44
  Installing : at-spi2-core-2.22.0-1.amzn2.0.2.x86_64                      4/44
  Installing : at-spi2-atk-2.22.0-2.amzn2.0.2.x86_64                       5/44
  Installing : libdbusmenu-16.04.0-4.amzn2.0.2.x86_64                      6/44
  Installing : libusbx-1.0.21-1.amzn2.x86_64                               7/44
  Installing : libgusb-0.2.9-1.amzn2.0.2.x86_64                            8/44
  Installing : 1:liberation-serif-fonts-1.07.2-16.amzn2.noarch             9/44
  Installing : 1:liberation-mono-fonts-1.07.2-16.amzn2.noarch             10/44
  Installing : 1:liberation-narrow-fonts-1.07.2-16.amzn2.noarch           11/44
  Installing : 1:liberation-sans-fonts-1.07.2-16.amzn2.noarch             12/44
  Installing : 1:liberation-fonts-1.07.2-16.amzn2.noarch                  13/44
  Installing : vulkan-filesystem-1.0.61.1-2.amzn2.noarch                  14/44
  Installing : vulkan-1.0.61.1-2.amzn2.x86_64                             15/44
  Installing : libepoxy-1.3.1-2.amzn2.x86_64                              16/44
  Installing : json-glib-1.4.2-2.amzn2.x86_64                             17/44
  Installing : lcms2-2.6-3.amzn2.0.2.x86_64                               18/44
  Installing : colord-libs-1.3.4-1.amzn2.0.2.x86_64                       19/44
  Installing : libwayland-cursor-1.17.0-1.amzn2.x86_64                    20/44
  Installing : libwayland-egl-1.17.0-1.amzn2.x86_64                       21/44
  Installing : gsettings-desktop-schemas-3.28.0-2.amzn2.x86_64            22/44
  Installing : xkeyboard-config-2.20-1.amzn2.noarch                       23/44
  Installing : libxkbcommon-0.7.1-3.amzn2.x86_64                          24/44
  Installing : libXScrnSaver-1.2.2-6.1.amzn2.0.2.x86_64                   25/44
  Installing : dconf-0.28.0-4.amzn2.x86_64                                26/44
  Installing : adwaita-cursor-theme-3.26.0-1.amzn2.noarch                 27/44
  Installing : adwaita-icon-theme-3.26.0-1.amzn2.noarch                   28/44
  Installing : trousers-0.3.14-2.amzn2.0.2.x86_64                         29/44
  Installing : desktop-file-utils-0.23-2.amzn2.x86_64                     30/44
  Installing : xdg-utils-1.1.0-0.17.20120809git.amzn2.noarch              31/44
  Installing : nettle-2.7.1-8.amzn2.0.2.x86_64                            32/44
  Installing : gnutls-3.3.29-9.amzn2.x86_64                               33/44
  Installing : libmodman-2.0.1-8.amzn2.0.2.x86_64                         34/44
  Installing : libproxy-0.4.11-10.amzn2.0.3.x86_64                        35/44
  Installing : glib-networking-2.56.1-1.amzn2.x86_64                      36/44
  Installing : libsoup-2.56.0-6.amzn2.x86_64                              37/44
  Installing : rest-0.8.0-2.amzn2.x86_64                                  38/44
  Installing : gtk3-3.22.30-3.amzn2.x86_64                                39/44
  Installing : libindicator-gtk3-12.10.1-6.amzn2.0.2.x86_64               40/44
  Installing : libdbusmenu-gtk3-16.04.0-4.amzn2.0.2.x86_64                41/44
  Installing : libappindicator-gtk3-12.10.0-13.amzn2.0.1.x86_64           42/44
  Installing : google-chrome-stable-81.0.4044.122-1.x86_64                43/44
Redirecting to /bin/systemctl start atd.service
  Cleanup    : cairo-1.14.8-2.amzn2.0.2.x86_64                            44/44
  Verifying  : libusbx-1.0.21-1.amzn2.x86_64                               1/44
  Verifying  : rest-0.8.0-2.amzn2.x86_64                                   2/44
  Verifying  : libmodman-2.0.1-8.amzn2.0.2.x86_64                          3/44
  Verifying  : nettle-2.7.1-8.amzn2.0.2.x86_64                             4/44
  Verifying  : 1:liberation-serif-fonts-1.07.2-16.amzn2.noarch             5/44
  Verifying  : xdg-utils-1.1.0-0.17.20120809git.amzn2.noarch               6/44
  Verifying  : gtk3-3.22.30-3.amzn2.x86_64                                 7/44
  Verifying  : colord-libs-1.3.4-1.amzn2.0.2.x86_64                        8/44
  Verifying  : libproxy-0.4.11-10.amzn2.0.3.x86_64                         9/44
  Verifying  : libindicator-gtk3-12.10.1-6.amzn2.0.2.x86_64               10/44
  Verifying  : 1:liberation-mono-fonts-1.07.2-16.amzn2.noarch             11/44
  Verifying  : 1:liberation-fonts-common-1.07.2-16.amzn2.noarch           12/44
  Verifying  : desktop-file-utils-0.23-2.amzn2.x86_64                     13/44
  Verifying  : glib-networking-2.56.1-1.amzn2.x86_64                      14/44
  Verifying  : 1:liberation-narrow-fonts-1.07.2-16.amzn2.noarch           15/44
  Verifying  : cairo-1.15.12-4.amzn2.x86_64                               16/44
  Verifying  : google-chrome-stable-81.0.4044.122-1.x86_64                17/44
  Verifying  : gnutls-3.3.29-9.amzn2.x86_64                               18/44
  Verifying  : libgusb-0.2.9-1.amzn2.0.2.x86_64                           19/44
  Verifying  : trousers-0.3.14-2.amzn2.0.2.x86_64                         20/44
  Verifying  : 1:liberation-sans-fonts-1.07.2-16.amzn2.noarch             21/44
  Verifying  : at-spi2-atk-2.22.0-2.amzn2.0.2.x86_64                      22/44
  Verifying  : adwaita-cursor-theme-3.26.0-1.amzn2.noarch                 23/44
  Verifying  : libxkbcommon-0.7.1-3.amzn2.x86_64                          24/44
  Verifying  : libdbusmenu-gtk3-16.04.0-4.amzn2.0.2.x86_64                25/44
  Verifying  : dconf-0.28.0-4.amzn2.x86_64                                26/44
  Verifying  : libXScrnSaver-1.2.2-6.1.amzn2.0.2.x86_64                   27/44
  Verifying  : cairo-gobject-1.15.12-4.amzn2.x86_64                       28/44
  Verifying  : xkeyboard-config-2.20-1.amzn2.noarch                       29/44
  Verifying  : gsettings-desktop-schemas-3.28.0-2.amzn2.x86_64            30/44
  Verifying  : vulkan-1.0.61.1-2.amzn2.x86_64                             31/44
  Verifying  : libwayland-egl-1.17.0-1.amzn2.x86_64                       32/44
  Verifying  : libsoup-2.56.0-6.amzn2.x86_64                              33/44
  Verifying  : libwayland-cursor-1.17.0-1.amzn2.x86_64                    34/44
  Verifying  : adwaita-icon-theme-3.26.0-1.amzn2.noarch                   35/44
  Verifying  : lcms2-2.6-3.amzn2.0.2.x86_64                               36/44
  Verifying  : json-glib-1.4.2-2.amzn2.x86_64                             37/44
  Verifying  : 1:liberation-fonts-1.07.2-16.amzn2.noarch                  38/44
  Verifying  : libepoxy-1.3.1-2.amzn2.x86_64                              39/44
  Verifying  : libdbusmenu-16.04.0-4.amzn2.0.2.x86_64                     40/44
  Verifying  : at-spi2-core-2.22.0-1.amzn2.0.2.x86_64                     41/44
  Verifying  : vulkan-filesystem-1.0.61.1-2.amzn2.noarch                  42/44
  Verifying  : libappindicator-gtk3-12.10.0-13.amzn2.0.1.x86_64           43/44
  Verifying  : cairo-1.14.8-2.amzn2.0.2.x86_64                            44/44

Installed:
  google-chrome-stable.x86_64 0:81.0.4044.122-1

Dependency Installed:
  adwaita-cursor-theme.noarch 0:3.26.0-1.amzn2
  adwaita-icon-theme.noarch 0:3.26.0-1.amzn2
  at-spi2-atk.x86_64 0:2.22.0-2.amzn2.0.2
  at-spi2-core.x86_64 0:2.22.0-1.amzn2.0.2
  cairo-gobject.x86_64 0:1.15.12-4.amzn2
  colord-libs.x86_64 0:1.3.4-1.amzn2.0.2
  dconf.x86_64 0:0.28.0-4.amzn2
  desktop-file-utils.x86_64 0:0.23-2.amzn2
  glib-networking.x86_64 0:2.56.1-1.amzn2
  gnutls.x86_64 0:3.3.29-9.amzn2
  gsettings-desktop-schemas.x86_64 0:3.28.0-2.amzn2
  gtk3.x86_64 0:3.22.30-3.amzn2
  json-glib.x86_64 0:1.4.2-2.amzn2
  lcms2.x86_64 0:2.6-3.amzn2.0.2
  libXScrnSaver.x86_64 0:1.2.2-6.1.amzn2.0.2
  libappindicator-gtk3.x86_64 0:12.10.0-13.amzn2.0.1
  libdbusmenu.x86_64 0:16.04.0-4.amzn2.0.2
  libdbusmenu-gtk3.x86_64 0:16.04.0-4.amzn2.0.2
  libepoxy.x86_64 0:1.3.1-2.amzn2
  liberation-fonts.noarch 1:1.07.2-16.amzn2
  liberation-fonts-common.noarch 1:1.07.2-16.amzn2
  liberation-mono-fonts.noarch 1:1.07.2-16.amzn2
  liberation-narrow-fonts.noarch 1:1.07.2-16.amzn2
  liberation-sans-fonts.noarch 1:1.07.2-16.amzn2
  liberation-serif-fonts.noarch 1:1.07.2-16.amzn2
  libgusb.x86_64 0:0.2.9-1.amzn2.0.2
  libindicator-gtk3.x86_64 0:12.10.1-6.amzn2.0.2
  libmodman.x86_64 0:2.0.1-8.amzn2.0.2
  libproxy.x86_64 0:0.4.11-10.amzn2.0.3
  libsoup.x86_64 0:2.56.0-6.amzn2
  libusbx.x86_64 0:1.0.21-1.amzn2
  libwayland-cursor.x86_64 0:1.17.0-1.amzn2
  libwayland-egl.x86_64 0:1.17.0-1.amzn2
  libxkbcommon.x86_64 0:0.7.1-3.amzn2
  nettle.x86_64 0:2.7.1-8.amzn2.0.2
  rest.x86_64 0:0.8.0-2.amzn2
  trousers.x86_64 0:0.3.14-2.amzn2.0.2
  vulkan.x86_64 0:1.0.61.1-2.amzn2
  vulkan-filesystem.noarch 0:1.0.61.1-2.amzn2
  xdg-utils.noarch 0:1.1.0-0.17.20120809git.amzn2
  xkeyboard-config.noarch 0:2.20-1.amzn2

Dependency Updated:
  cairo.x86_64 0:1.15.12-4.amzn2

Complete!
Successfully installed Google Chrome!
[ec2-user@ip-172-31-9-135 tmp]$ google-chrome --version &amp;&amp; which google-chrome
-bash: syntax error near unexpected token `;&'
[ec2-user@ip-172-31-9-135 tmp]$ google-chrome --version
Google Chrome 81.0.4044.122
[ec2-user@ip-172-31-9-135 tmp]$ which google-chrome
/usr/bin/google-chrome
[ec2-user@ip-172-31-9-135 tmp]$ python --version
Python 2.7.16
[ec2-user@ip-172-31-9-135 tmp]$ virtualenv
-bash: virtualenv: command not found
[ec2-user@ip-172-31-9-135 tmp]$ pip -V
-bash: pip: command not found
[ec2-user@ip-172-31-9-135 tmp]$ python -m pip install --user virtualenv
/usr/bin/python: No module named pip
[ec2-user@ip-172-31-9-135 tmp]$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 1764k  100 1764k    0     0  19.1M      0 --:--:-- --:--:-- --:--:-- 19.1M
[ec2-user@ip-172-31-9-135 tmp]$ python get-pip.py
DEPRECATION: Python 2.7 reached the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 is no longer maintained. A future version of pip will drop support for Python 2.7. More details about Python 2 support in pip, can be found at https://pip.pypa.io/en/latest/development/release-process/#python-2-support
Defaulting to user installation because normal site-packages is not writeable
Collecting pip
  Downloading pip-20.0.2-py2.py3-none-any.whl (1.4 MB)
     |████████████████████████████████| 1.4 MB 27.0 MB/s
Collecting wheel
  Downloading wheel-0.34.2-py2.py3-none-any.whl (26 kB)
Installing collected packages: pip, wheel
Successfully installed pip-20.0.2 wheel-0.34.2
[ec2-user@ip-172-31-9-135 tmp]$ python -m pip install --user virtualenv
DEPRECATION: Python 2.7 reached the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 is no longer maintained. A future version of pip will drop support for Python 2.7. More details about Python 2 support in pip, can be found at https://pip.pypa.io/en/latest/development/release-process/#python-2-support
Collecting virtualenv
  Downloading virtualenv-20.0.18-py2.py3-none-any.whl (4.6 MB)
     |████████████████████████████████| 4.6 MB 29.3 MB/s
Collecting distlib<1,>=0.3.0
  Downloading distlib-0.3.0.zip (571 kB)
     |████████████████████████████████| 571 kB 42.0 MB/s
Collecting pathlib2<3,>=2.3.3; python_version < "3.4" and sys_platform != "win32"
  Downloading pathlib2-2.3.5-py2.py3-none-any.whl (18 kB)
Collecting contextlib2<1,>=0.6.0; python_version < "3.3"
  Downloading contextlib2-0.6.0.post1-py2.py3-none-any.whl (9.8 kB)
Collecting importlib-resources<2,>=1.0; python_version < "3.7"
  Downloading importlib_resources-1.4.0-py2.py3-none-any.whl (20 kB)
Collecting importlib-metadata<2,>=0.12; python_version < "3.8"
  Downloading importlib_metadata-1.6.0-py2.py3-none-any.whl (30 kB)
Collecting filelock<4,>=3.0.0
  Downloading filelock-3.0.12.tar.gz (8.5 kB)
Collecting appdirs<2,>=1.4.3
  Downloading appdirs-1.4.3-py2.py3-none-any.whl (12 kB)
Requirement already satisfied: six<2,>=1.9.0 in /usr/lib/python2.7/site-packages (from virtualenv) (1.9.0)
Collecting scandir; python_version < "3.5"
  Downloading scandir-1.10.0.tar.gz (33 kB)
Collecting singledispatch; python_version < "3.4"
  Downloading singledispatch-3.4.0.3-py2.py3-none-any.whl (12 kB)
Collecting typing; python_version < "3.5"
  Downloading typing-3.7.4.1-py2-none-any.whl (26 kB)
Collecting zipp>=0.4; python_version < "3.8"
  Downloading zipp-1.2.0-py2.py3-none-any.whl (4.8 kB)
Collecting configparser>=3.5; python_version < "3"
  Downloading configparser-4.0.2-py2.py3-none-any.whl (22 kB)
Building wheels for collected packages: distlib, filelock, scandir
  Building wheel for distlib (setup.py) ... done
  Created wheel for distlib: filename=distlib-0.3.0-py2-none-any.whl size=340453 sha256=ef9dd42986f583b0aca12ad5d22529fda7bc713e6667b63ec5191210db30b7d3
  Stored in directory: /home/ec2-user/.cache/pip/wheels/0c/88/ac/41500883ea902d3409a83a827870a726346b5ebfd0523e91df
  Building wheel for filelock (setup.py) ... done
  Created wheel for filelock: filename=filelock-3.0.12-py2-none-any.whl size=7576 sha256=888e7dbfe15ce00e10a8f124a0c2aeb8563d9894b15debdbc99f2ee100587695
  Stored in directory: /home/ec2-user/.cache/pip/wheels/b9/91/23/b559c1f4fd55056712b3a71cd9cab1dc0089e2232d502ed72e
  Building wheel for scandir (setup.py) ... done
  Created wheel for scandir: filename=scandir-1.10.0-cp27-cp27mu-linux_x86_64.whl size=11163 sha256=ac21e50e9329e3219a323ec8a002a4f35e272fec8379a19cdab38f965d5793b1
  Stored in directory: /home/ec2-user/.cache/pip/wheels/58/2c/26/52406f7d1f19bcc47a6fbd1037a5f293492f5cf1d58c539edb
Successfully built distlib filelock scandir
Installing collected packages: distlib, scandir, pathlib2, contextlib2, singledispatch, zipp, configparser, importlib-metadata, typing, importlib-resources, filelock, appdirs, virtualenv
Successfully installed appdirs-1.4.3 configparser-4.0.2 contextlib2-0.6.0.post1 distlib-0.3.0 filelock-3.0.12 importlib-metadata-1.6.0 importlib-resources-1.4.0 pathlib2-2.3.5 scandir-1.10.0 singledispatch-3.4.0.3 typing-3.7.4.1 virtualenv-20.0.18 zipp-1.2.0
[ec2-user@ip-172-31-9-135 tmp]$ virtualenv -V
usage: virtualenv [--version] [--with-traceback] [-v | -q] [--app-data APP_DATA] [--clear-app-data] [--discovery {builtin}] [-p py] [--creator {builtin,cpython2-posix}] [--seeder {app-data,pip}] [--no-seed] [--activators comma_sep_list]
                  [--clear] [--system-site-packages] [--symlinks | --copies] [--download | --no-download] [--extra-search-dir d [d ...]] [--pip version] [--setuptools version] [--wheel version] [--no-pip] [--no-setuptools] [--no-wheel]
                  [--symlink-app-data] [--prompt prompt] [-h]
                  dest
virtualenv: error: too few arguments
[ec2-user@ip-172-31-9-135 tmp]$ virtualenv -v
find interpreter for spec PythonSpec(path=/usr/bin/python)
proposed PythonInfo({'base_exec_prefix': None, 'system_stdlib': u'/usr/lib64/python2.7', 'has_venv': False, 'prefix': u'/usr', 'stdout_encoding': u'UTF-8', 'executable': '/usr/bin/python', 'implementation': u'CPython', 'exec_prefix': u'/usr', 'platform': u'linux2', 'version': u'2.7.16 (default, Dec 12 2019, 23:58:22) \n[GCC 7.3.1 20180712 (Red Hat 7.3.1-6)]', 'sysconfig_paths': {u'platstdlib': u'{platbase}/lib64/python{py_version_short}', u'platlib': u'{platbase}/lib64/python{py_version_short}/site-packages', u'purelib': u'{base}/lib/python{py_version_short}/site-packages', u'stdlib': u'{base}/lib64/python{py_version_short}', u'scripts': u'{base}/bin', u'include': u'{base}/include/python{py_version_short}', u'data': u'{base}'}, 'base_prefix': None, 'system_stdlib_platform': u'/usr/lib64/python2.7', 'file_system_encoding': u'UTF-8', 'version_info': VersionInfo(major=2, minor=7, micro=16, releaselevel=u'final', serial=0), 'sysconfig_vars': {u'base': u'/usr', u'platbase': u'/usr', u'PYTHONFRAMEWORK': u'', u'py_version_short': u'2.7'}, 'path': [u'/home/ec2-user/.local/bin', u'/usr/lib/python27.zip', u'/usr/lib64/python2.7', u'/usr/lib64/python2.7/plat-linux2', u'/usr/lib64/python2.7/lib-tk', u'/usr/lib64/python2.7/lib-old', u'/usr/lib64/python2.7/lib-dynload', u'/home/ec2-user/.local/lib/python2.7/site-packages', u'/usr/lib64/python2.7/site-packages', u'/usr/lib/python2.7/site-packages'], 'max_size': 9223372036854775807, 'real_prefix': None, 'distutils_install': {u'purelib': u'lib/python2.7/site-packages', u'headers': u'include/python2.7/UNKNOWN', u'platlib': u'lib64/python2.7/site-packages', u'data': u'', u'scripts': u'bin'}, 'architecture': 64, 'original_executable': u'/usr/bin/python', 'os': u'posix', 'system_executable': u'/usr/bin/python'})
usage: virtualenv [--version] [--with-traceback] [-v | -q] [--app-data APP_DATA] [--clear-app-data] [--discovery {builtin}] [-p py] [--creator {builtin,cpython2-posix}] [--seeder {app-data,pip}] [--no-seed] [--activators comma_sep_list]
                  [--clear] [--system-site-packages] [--symlinks | --copies] [--download | --no-download] [--extra-search-dir d [d ...]] [--pip version] [--setuptools version] [--wheel version] [--no-pip] [--no-setuptools] [--no-wheel]
                  [--symlink-app-data] [--prompt prompt] [-h]
                  dest
virtualenv: error: too few arguments
[ec2-user@ip-172-31-9-135 tmp]$ virtualenv -help
usage: virtualenv [--version] [--with-traceback] [-v | -q] [--app-data APP_DATA] [--clear-app-data] [--discovery {builtin}] [-p py] [--creator {builtin,cpython2-posix}] [--seeder {app-data,pip}] [--no-seed] [--activators comma_sep_list]
                  [--clear] [--system-site-packages] [--symlinks | --copies] [--download | --no-download] [--extra-search-dir d [d ...]] [--pip version] [--setuptools version] [--wheel version] [--no-pip] [--no-setuptools] [--no-wheel]
                  [--symlink-app-data] [--prompt prompt] [-h]
                  dest
virtualenv: error: argument -h/--help: ignored explicit argument 'elp'
[ec2-user@ip-172-31-9-135 tmp]$ virtualenv --version
virtualenv 20.0.18 from /home/ec2-user/.local/lib/python2.7/site-packages/virtualenv/__init__.pyc
[ec2-user@ip-172-31-9-135 tmp]$ python3
-bash: python3: command not found
[ec2-user@ip-172-31-9-135 tmp]$ pwd
/tmp
[ec2-user@ip-172-31-9-135 tmp]$ virtualenv -p python3 venv
RuntimeError: failed to find interpreter for Builtin discover of python_spec='python3'
[ec2-user@ip-172-31-9-135 tmp]$ sudo yum install -y python3
Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
amzn2-core                                               | 2.4 kB     00:00
Resolving Dependencies
--> Running transaction check
---> Package python3.x86_64 0:3.7.6-1.amzn2.0.1 will be installed
--> Processing Dependency: python3-libs(x86-64) = 3.7.6-1.amzn2.0.1 for package: python3-3.7.6-1.amzn2.0.1.x86_64
--> Processing Dependency: python3-setuptools for package: python3-3.7.6-1.amzn2.0.1.x86_64
--> Processing Dependency: python3-pip for package: python3-3.7.6-1.amzn2.0.1.x86_64
--> Processing Dependency: libpython3.7m.so.1.0()(64bit) for package: python3-3.7.6-1.amzn2.0.1.x86_64
--> Running transaction check
---> Package python3-libs.x86_64 0:3.7.6-1.amzn2.0.1 will be installed
---> Package python3-pip.noarch 0:9.0.3-1.amzn2.0.2 will be installed
---> Package python3-setuptools.noarch 0:38.4.0-3.amzn2.0.6 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

================================================================================
 Package                Arch       Version                 Repository      Size
================================================================================
Installing:
 python3                x86_64     3.7.6-1.amzn2.0.1       amzn2-core      71 k
Installing for dependencies:
 python3-libs           x86_64     3.7.6-1.amzn2.0.1       amzn2-core     9.1 M
 python3-pip            noarch     9.0.3-1.amzn2.0.2       amzn2-core     1.9 M
 python3-setuptools     noarch     38.4.0-3.amzn2.0.6      amzn2-core     617 k

Transaction Summary
================================================================================
Install  1 Package (+3 Dependent packages)

Total download size: 12 M
Installed size: 50 M
Downloading packages:
(1/4): python3-3.7.6-1.amzn2.0.1.x86_64.rpm                |  71 kB   00:00
(2/4): python3-libs-3.7.6-1.amzn2.0.1.x86_64.rpm           | 9.1 MB   00:00
(3/4): python3-pip-9.0.3-1.amzn2.0.2.noarch.rpm            | 1.9 MB   00:00
(4/4): python3-setuptools-38.4.0-3.amzn2.0.6.noarch.rpm    | 617 kB   00:00
--------------------------------------------------------------------------------
Total                                               36 MB/s |  12 MB  00:00
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : python3-pip-9.0.3-1.amzn2.0.2.noarch                         1/4
  Installing : python3-3.7.6-1.amzn2.0.1.x86_64                             2/4
  Installing : python3-setuptools-38.4.0-3.amzn2.0.6.noarch                 3/4
  Installing : python3-libs-3.7.6-1.amzn2.0.1.x86_64                        4/4
  Verifying  : python3-setuptools-38.4.0-3.amzn2.0.6.noarch                 1/4
  Verifying  : python3-pip-9.0.3-1.amzn2.0.2.noarch                         2/4
  Verifying  : python3-3.7.6-1.amzn2.0.1.x86_64                             3/4
  Verifying  : python3-libs-3.7.6-1.amzn2.0.1.x86_64                        4/4

Installed:
  python3.x86_64 0:3.7.6-1.amzn2.0.1

Dependency Installed:
  python3-libs.x86_64 0:3.7.6-1.amzn2.0.1
  python3-pip.noarch 0:9.0.3-1.amzn2.0.2
  python3-setuptools.noarch 0:38.4.0-3.amzn2.0.6

Complete!
[ec2-user@ip-172-31-9-135 tmp]$ virtualenv -p python3 venv
created virtual environment CPython3.7.6.final.0-64 in 365ms
  creator CPython3Posix(dest=/tmp/venv, clear=False, global=False)
  seeder FromAppData(download=False, pip=latest, setuptools=latest, wheel=latest, via=copy, app_data_dir=/home/ec2-user/.local/share/virtualenv/seed-app-data/v1.0.1)
  activators PythonActivator,FishActivator,XonshActivator,CShellActivator,PowerShellActivator,BashActivator
[ec2-user@ip-172-31-9-135 tmp]$ source venv/bin/activate
(venv) [ec2-user@ip-172-31-9-135 tmp]$ pip -V
pip 20.0.2 from /tmp/venv/lib/python3.7/site-packages/pip (python 3.7)
(venv) [ec2-user@ip-172-31-9-135 tmp]$ sudo service jenkins restart
Restarting jenkins (via systemctl):                        [  OK  ]
(venv) [ec2-user@ip-172-31-9-135 tmp]$ virtualenv -V
usage: virtualenv [--version] [--with-traceback] [-v | -q] [--app-data APP_DATA] [--clear-app-data] [--discovery {builtin}] [-p py] [--creator {builtin,cpython2-posix}] [--seeder {app-data,pip}] [--no-seed] [--activators comma_sep_list]
                  [--clear] [--system-site-packages] [--symlinks | --copies] [--download | --no-download] [--extra-search-dir d [d ...]] [--pip version] [--setuptools version] [--wheel version] [--no-pip] [--no-setuptools] [--no-wheel]
                  [--symlink-app-data] [--prompt prompt] [-h]
                  dest
virtualenv: error: too few arguments
(venv) [ec2-user@ip-172-31-9-135 tmp]$ virtualenv --version
virtualenv 20.0.18 from /home/ec2-user/.local/lib/python2.7/site-packages/virtualenv/__init__.pyc
(venv) [ec2-user@ip-172-31-9-135 tmp]$ which virtualenv
~/.local/bin/virtualenv
(venv) [ec2-user@ip-172-31-9-135 tmp]$ cat ~/.local/bin/virtualenv
#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys
from virtualenv.__main__ import run_with_catch
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(run_with_catch())
(venv) [ec2-user@ip-172-31-9-135 tmp]$ sudo -su jenkins
(venv) [jenkins@ip-172-31-9-135 tmp]$ virtualenv
bash: virtualenv: command not found
(venv) [jenkins@ip-172-31-9-135 tmp]$ pip
bash: pip: command not found
(venv) [jenkins@ip-172-31-9-135 tmp]$ python3
Python 3.7.6 (default, Feb 26 2020, 20:54:15)
[GCC 7.3.1 20180712 (Red Hat 7.3.1-6)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> quit()
(venv) [jenkins@ip-172-31-9-135 tmp]$ deactivate
bash: deactivate: command not found
(venv) [jenkins@ip-172-31-9-135 tmp]$ exit
exit
(venv) [ec2-user@ip-172-31-9-135 tmp]$ deactivate
[ec2-user@ip-172-31-9-135 tmp]$ sudo -su jenkins
[jenkins@ip-172-31-9-135 tmp]$ python get-pip.py
DEPRECATION: Python 2.7 reached the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 is no longer maintained. A future version of pip will drop support for Python 2.7. More details about Python 2 support in pip, can be found at https://pip.pypa.io/en/latest/development/release-process/#python-2-support
Defaulting to user installation because normal site-packages is not writeable
Collecting pip
  Downloading pip-20.0.2-py2.py3-none-any.whl (1.4 MB)
     |████████████████████████████████| 1.4 MB 20.2 MB/s
Collecting wheel
  Downloading wheel-0.34.2-py2.py3-none-any.whl (26 kB)
Installing collected packages: pip, wheel
  WARNING: The scripts pip, pip2 and pip2.7 are installed in '/var/lib/jenkins/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
  WARNING: The script wheel is installed in '/var/lib/jenkins/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
Successfully installed pip-20.0.2 wheel-0.34.2
[jenkins@ip-172-31-9-135 tmp]$ python -m pip install --user virtualenv
DEPRECATION: Python 2.7 reached the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 is no longer maintained. A future version of pip will drop support for Python 2.7. More details about Python 2 support in pip, can be found at https://pip.pypa.io/en/latest/development/release-process/#python-2-support
Collecting virtualenv
  Downloading virtualenv-20.0.18-py2.py3-none-any.whl (4.6 MB)
     |████████████████████████████████| 4.6 MB 20.4 MB/s
Collecting distlib<1,>=0.3.0
  Downloading distlib-0.3.0.zip (571 kB)
     |████████████████████████████████| 571 kB 43.3 MB/s
Collecting pathlib2<3,>=2.3.3; python_version < "3.4" and sys_platform != "win32"
  Downloading pathlib2-2.3.5-py2.py3-none-any.whl (18 kB)
Collecting contextlib2<1,>=0.6.0; python_version < "3.3"
  Downloading contextlib2-0.6.0.post1-py2.py3-none-any.whl (9.8 kB)
Collecting importlib-resources<2,>=1.0; python_version < "3.7"
  Downloading importlib_resources-1.4.0-py2.py3-none-any.whl (20 kB)
Collecting importlib-metadata<2,>=0.12; python_version < "3.8"
  Downloading importlib_metadata-1.6.0-py2.py3-none-any.whl (30 kB)
Collecting filelock<4,>=3.0.0
  Downloading filelock-3.0.12.tar.gz (8.5 kB)
Collecting appdirs<2,>=1.4.3
  Downloading appdirs-1.4.3-py2.py3-none-any.whl (12 kB)
Requirement already satisfied: six<2,>=1.9.0 in /usr/lib/python2.7/site-packages (from virtualenv) (1.9.0)
Collecting scandir; python_version < "3.5"
  Downloading scandir-1.10.0.tar.gz (33 kB)
Collecting singledispatch; python_version < "3.4"
  Downloading singledispatch-3.4.0.3-py2.py3-none-any.whl (12 kB)
Collecting typing; python_version < "3.5"
  Downloading typing-3.7.4.1-py2-none-any.whl (26 kB)
Collecting zipp>=0.4; python_version < "3.8"
  Downloading zipp-1.2.0-py2.py3-none-any.whl (4.8 kB)
Collecting configparser>=3.5; python_version < "3"
  Downloading configparser-4.0.2-py2.py3-none-any.whl (22 kB)
Building wheels for collected packages: distlib, filelock, scandir
  Building wheel for distlib (setup.py) ... done
  Created wheel for distlib: filename=distlib-0.3.0-py2-none-any.whl size=340453 sha256=bfad83971e6c1a7ffed332ab9a4b099a6f405c98ad7a6a94e8c1f9831c45972a
  Stored in directory: /var/lib/jenkins/.cache/pip/wheels/0c/88/ac/41500883ea902d3409a83a827870a726346b5ebfd0523e91df
  Building wheel for filelock (setup.py) ... done
  Created wheel for filelock: filename=filelock-3.0.12-py2-none-any.whl size=7576 sha256=021d7dd861c3c3c4eb559ff2bc358ccd9b57e1f7978adb505b16127208434851
  Stored in directory: /var/lib/jenkins/.cache/pip/wheels/b9/91/23/b559c1f4fd55056712b3a71cd9cab1dc0089e2232d502ed72e
  Building wheel for scandir (setup.py) ... done
  Created wheel for scandir: filename=scandir-1.10.0-cp27-cp27mu-linux_x86_64.whl size=11163 sha256=fd0d3600f313f95dad0a7c220fc607650a84a037fe74b30f2aab386a944fcd1c
  Stored in directory: /var/lib/jenkins/.cache/pip/wheels/58/2c/26/52406f7d1f19bcc47a6fbd1037a5f293492f5cf1d58c539edb
Successfully built distlib filelock scandir
Installing collected packages: distlib, scandir, pathlib2, contextlib2, singledispatch, zipp, configparser, importlib-metadata, typing, importlib-resources, filelock, appdirs, virtualenv
  WARNING: The script virtualenv is installed in '/var/lib/jenkins/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
Successfully installed appdirs-1.4.3 configparser-4.0.2 contextlib2-0.6.0.post1 distlib-0.3.0 filelock-3.0.12 importlib-metadata-1.6.0 importlib-resources-1.4.0 pathlib2-2.3.5 scandir-1.10.0 singledispatch-3.4.0.3 typing-3.7.4.1 virtualenv-20.0.18 zipp-1.2.0
[jenkins@ip-172-31-9-135 tmp]$ virtualenv
bash: virtualenv: command not found
[jenkins@ip-172-31-9-135 tmp]$ exit
exit
[ec2-user@ip-172-31-9-135 tmp]$ sudo python get-pip.py
DEPRECATION: Python 2.7 reached the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 is no longer maintained. A future version of pip will drop support for Python 2.7. More details about Python 2 support in pip, can be found at https://pip.pypa.io/en/latest/development/release-process/#python-2-support
Collecting pip
  Downloading pip-20.0.2-py2.py3-none-any.whl (1.4 MB)
     |████████████████████████████████| 1.4 MB 28.1 MB/s
Collecting wheel
  Downloading wheel-0.34.2-py2.py3-none-any.whl (26 kB)
Installing collected packages: pip, wheel
Successfully installed pip-20.0.2 wheel-0.34.2
[ec2-user@ip-172-31-9-135 tmp]$ sudo python -m pip install --user virtualen
DEPRECATION: Python 2.7 reached the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 is no longer maintained. A future version of pip will drop support for Python 2.7. More details about Python 2 support in pip, can be found at https://pip.pypa.io/en/latest/development/release-process/#python-2-support
ERROR: Could not find a version that satisfies the requirement virtualen (from versions: none)
ERROR: No matching distribution found for virtualen
[ec2-user@ip-172-31-9-135 tmp]$ sudo python -m pip install virtualen
DEPRECATION: Python 2.7 reached the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 is no longer maintained. A future version of pip will drop support for Python 2.7. More details about Python 2 support in pip, can be found at https://pip.pypa.io/en/latest/development/release-process/#python-2-support
ERROR: Could not find a version that satisfies the requirement virtualen (from versions: none)
ERROR: No matching distribution found for virtualen
[ec2-user@ip-172-31-9-135 tmp]$ sudo python -m pip install virtualenv
DEPRECATION: Python 2.7 reached the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 is no longer maintained. A future version of pip will drop support for Python 2.7. More details about Python 2 support in pip, can be found at https://pip.pypa.io/en/latest/development/release-process/#python-2-support
Collecting virtualenv
  Downloading virtualenv-20.0.18-py2.py3-none-any.whl (4.6 MB)
     |████████████████████████████████| 4.6 MB 17.1 MB/s
Collecting distlib<1,>=0.3.0
  Downloading distlib-0.3.0.zip (571 kB)
     |████████████████████████████████| 571 kB 36.3 MB/s
Collecting pathlib2<3,>=2.3.3; python_version < "3.4" and sys_platform != "win32"
  Downloading pathlib2-2.3.5-py2.py3-none-any.whl (18 kB)
Collecting contextlib2<1,>=0.6.0; python_version < "3.3"
  Downloading contextlib2-0.6.0.post1-py2.py3-none-any.whl (9.8 kB)
Collecting importlib-resources<2,>=1.0; python_version < "3.7"
  Downloading importlib_resources-1.4.0-py2.py3-none-any.whl (20 kB)
Collecting importlib-metadata<2,>=0.12; python_version < "3.8"
  Downloading importlib_metadata-1.6.0-py2.py3-none-any.whl (30 kB)
Collecting filelock<4,>=3.0.0
  Downloading filelock-3.0.12.tar.gz (8.5 kB)
Collecting appdirs<2,>=1.4.3
  Downloading appdirs-1.4.3-py2.py3-none-any.whl (12 kB)
Requirement already satisfied: six<2,>=1.9.0 in /usr/lib/python2.7/site-packages (from virtualenv) (1.9.0)
Collecting scandir; python_version < "3.5"
  Downloading scandir-1.10.0.tar.gz (33 kB)
Collecting singledispatch; python_version < "3.4"
  Downloading singledispatch-3.4.0.3-py2.py3-none-any.whl (12 kB)
Collecting typing; python_version < "3.5"
  Downloading typing-3.7.4.1-py2-none-any.whl (26 kB)
Collecting zipp>=0.4; python_version < "3.8"
  Downloading zipp-1.2.0-py2.py3-none-any.whl (4.8 kB)
Collecting configparser>=3.5; python_version < "3"
  Downloading configparser-4.0.2-py2.py3-none-any.whl (22 kB)
Building wheels for collected packages: distlib, filelock, scandir
  Building wheel for distlib (setup.py) ... done
  Created wheel for distlib: filename=distlib-0.3.0-py2-none-any.whl size=340453 sha256=2d992e9b942a61b854c8f29ee47bc461310e743b1a57f74f765f7b0950893f7f
  Stored in directory: /root/.cache/pip/wheels/0c/88/ac/41500883ea902d3409a83a827870a726346b5ebfd0523e91df
  Building wheel for filelock (setup.py) ... done
  Created wheel for filelock: filename=filelock-3.0.12-py2-none-any.whl size=7576 sha256=8c1d54d2ec1a6c64152221f03916105527f30f28bfcb065bd054f9d332a97592
  Stored in directory: /root/.cache/pip/wheels/b9/91/23/b559c1f4fd55056712b3a71cd9cab1dc0089e2232d502ed72e
  Building wheel for scandir (setup.py) ... done
  Created wheel for scandir: filename=scandir-1.10.0-cp27-cp27mu-linux_x86_64.whl size=11163 sha256=5aa5a820177911d792ce0a57f165bcfbe5503fab0d19e1040de24a85cc5d2448
  Stored in directory: /root/.cache/pip/wheels/58/2c/26/52406f7d1f19bcc47a6fbd10

~
~
~
~
~
~                              VIM - Vi IMproved
~
~                               version 8.1.1602
~                           by Bram Moolenaar et al.
~           Modified by Amazon Linux https://forums.aws.amazon.com/
~                 Vim is open source and freely distributable
~
~                        Help poor children in Uganda!
~                type  :help iccf<Enter>       for information
~
~                type  :q<Enter>               to exit
~                type  :help<Enter>  or  <F1>  for on-line help
~                type  :help version8<Enter>   for version info
~
~
~
~
~
                                                              0,0-1         All
37a5f293492f5cf1d58c539edb
Successfully built distlib filelock scandir
Installing collected packages: distlib, scandir, pathlib2, contextlib2, singledispatch, zipp, configparser, importlib-metadata, typing, importlib-resources, filelock, appdirs, virtualenv
Successfully installed appdirs-1.4.3 configparser-4.0.2 contextlib2-0.6.0.post1 distlib-0.3.0 filelock-3.0.12 importlib-metadata-1.6.0 importlib-resources-1.4.0 pathlib2-2.3.5 scandir-1.10.0 singledispatch-3.4.0.3 typing-3.7.4.1 virtualenv-20.0.18 zipp-1.2.0
[ec2-user@ip-172-31-9-135 tmp]$
[ec2-user@ip-172-31-9-135 tmp]$ sudo -su jenkins
[jenkins@ip-172-31-9-135 tmp]$ virtualenv
usage: virtualenv [--version] [--with-traceback] [-v | -q] [--app-data APP_DATA] [--clear-app-data] [--discovery {builtin}] [-p py] [--creator {builtin,cpython2-posix}] [--seeder {app-data,pip}] [--no-seed] [--activators comma_sep_list]
                  [--clear] [--system-site-packages] [--symlinks | --copies] [--download | --no-download] [--extra-search-dir d [d ...]] [--pip version] [--setuptools version] [--wheel version] [--no-pip] [--no-setuptools] [--no-wheel]
                  [--symlink-app-data] [--prompt prompt] [-h]
                  dest
virtualenv: error: too few arguments
[jenkins@ip-172-31-9-135 tmp]$ exit
exit
[ec2-user@ip-172-31-9-135 tmp]$ vim
[ec2-user@ip-172-31-9-135 tmp]$ ls
aerofiler-pytest
akuma4651371416864187358jar
akuma796521989446258153jar
chromedriver_linux64.zip
get-pip.py
hsperfdata_ec2-user
hsperfdata_jenkins
hsperfdata_root
jetty-0_0_0_0-8080-war-_-any-1949807998560654925.dir
jetty-0_0_0_0-8080-war-_-any-290324139520912267.dir
jna1275370094734093217jar
jna1994348788991608150jar
systemd-private-5298c4cbc22e4a6082bc500cab27a34d-chronyd.service-31dtbE
venv
winstone724034183948416490.jar
winstone8980879300570731852.jar
[ec2-user@ip-172-31-9-135 tmp]$ 1
-bash: 1: command not found
[ec2-user@ip-172-31-9-135 tmp]$ 2
-bash: 2: command not found
[ec2-user@ip-172-31-9-135 tmp]$ 3
-bash: 3: command not found
[ec2-user@ip-172-31-9-135 tmp]$ curl https://intoli.com/install-google-chrome.sh

#! /bin/bash


# Copyright 2017-present: Intoli, LLC
# Source: https://intoli.com/blog/installing-google-chrome-on-centos/
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


# What this script does is explained in detail in a blog post located at:
# https://intoli.com/blog/installing-google-chrome-on-centos/
# If you're trying to figure out how things work, then you should visit that!


# Require that this runs as root.
[ "$UID" -eq 0 ] || exec sudo "$0" "$@"


# Define some global variables.
working_directory="/tmp/google-chrome-installation"
repo_file="/etc/yum.repos.d/google-chrome.repo"


# Work in our working directory.
echo "Working in ${working_directory}"
mkdir -p ${working_directory}
rm -rf ${working_directory}/*
pushd ${working_directory}


# Add the official Google Chrome Centos 7 repo.
echo "Configuring the Google Chrome repo in ${repo_file}"
echo "[google-chrome]" > $repo_file
echo "name=google-chrome" >> $repo_file
echo "baseurl=http://dl.google.com/linux/chrome/rpm/stable/\$basearch" >> $repo_file
echo "enabled=1" >> $repo_file
echo "gpgcheck=1" >> $repo_file
echo "gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub" >> $repo_file


# Install the Google Chrome signing key.
yum install -y wget
wget https://dl.google.com/linux/linux_signing_key.pub
rpm --import linux_signing_key.pub


# A helper to make sure that Chrome is linked correctly
function installation_status() {
    google-chrome-stable --version > /dev/null 2>&1
    [ $? -eq 0 ]
}


# Try it the old fashioned way, should work on RHEL 7.X.
echo "Attempting a direction installation with yum."
yum install -y google-chrome-stable
if [ $? -eq 0 ]
then
    if installation_status; then
        # Print out the success message.
        echo "Successfully installed Google Chrome!"
        rm -rf ${working_directory}
        popd > /dev/null
        exit 0
    fi
fi


# Uninstall any existing/partially installed versions.
yum --setopt=tsflags=noscripts -y remove google-chrome-stable


# Install yumdownloader/repoquery and download the latest RPM.
echo "Downloading the Google Chrome RPM file."
yum install -y yum-utils
# There have been issues in the past with the Chrome repository, so we fall back to downloading
# the latest RPM directly if the package isn't available there. For further details:
# https://productforums.google.com/forum/#!topic/chrome/xNtfk_wAUC4;context-place=forum/chrome
yumdownloader google-chrome-stable || \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
rpm_file=$(echo *.rpm)
echo "Downloaded ${rpm_file}"


# Install the RPM in a broken state.
rpm -ih --nodeps ${rpm_file}
rm ${rpm_file}


# Install font dependencies, see: https://bugs.chromium.org/p/chromium/issues/detail?id=782161
echo "Installing the required font dependencies."
yum install -y \
    fontconfig \
    fontpackages-filesystem \
    ipa-gothic-fonts \
    xorg-x11-fonts-100dpi \
    xorg-x11-fonts-75dpi \
    xorg-x11-fonts-misc \
    xorg-x11-fonts-Type1 \
    xorg-x11-utils


# Helper function to install packages in the chroot by name (as an argument).
function install_package() {
    # We'll leave the RPMs around to avoid redownloading things.
    if [ -f "$1.rpm" ]; then
        return 0
    fi

    # Find the URL for the package.
    url=$(repoquery --repofrompath=centos7,http://mirror.centos.org/centos/7/os/`arch` \
        --repoid=centos7 -q --qf="%{location}" "$1" | \
        sed s/x86_64.rpm$/`arch`.rpm/ | \
        sed s/i686.rpm$/`arch`.rpm/g | \
        sort -u
    )

    # Download the RPM.
    wget "${url}" -O "$1.rpm"

    # Extract it.
    echo "Extracting $1..."
    rpm2cpio $1.rpm | cpio -idmv > /dev/null 2>&1
}


# Install glibc/ld-linux from CentOS 7.
install_package glibc


# Make the library directory and copy over glibc/ld-linux.
lib_directory=/opt/google/chrome/lib
mkdir -p $lib_directory
cp ./lib/* $lib_directory/ 2> /dev/null
cp ./lib64/* $lib_directory/ 2> /dev/null


# Install `mount` and its mandatory dependencies from CentOS 7.
for package in "glibc" "util-linux" "libmount" "libblkid" "libuuid" "libselinux" "pcre"; do
    install_package "${package}"
done


# Create an `ldd.sh` script to mimic the behavior of `ldd` within the namespace (without bash, etc. dependencies).
echo '#!/bin/bash' > ldd.sh
echo '' >> ldd.sh
echo '# Usage: ldd.sh LIBRARY_PATH EXECUTABLE' >> ldd.sh
echo 'mount --make-rprivate /' >> ldd.sh
echo 'unshare -m bash -c "`tail -n +7 $0`" "$0" "$@"' >> ldd.sh
echo 'exit $?' >> ldd.sh
echo '' >> ldd.sh
echo 'LD=$({ ls -1 ${1}/ld-linux* | head -n1 ; } 2> /dev/null)' >> ldd.sh
echo 'mount --make-private -o remount /' >> ldd.sh
echo 'mount --bind ${1} $(dirname "$({ ls -1 /lib/ld-linux* /lib64/ld-linux* | head -n1 ; } 2> /dev/null)")' >> ldd.sh
echo 'for directory in lib lib64 usr/lib usr/lib64; do' >> ldd.sh
echo '    PATH=./:./bin:./usr/bin LD_LIBRARY_PATH=${1}:./lib64:./usr/lib64:./lib:./usr/lib mount --bind ${1} /${directory} 2> /dev/null' >> ldd.sh
echo 'done' >> ldd.sh
echo 'echo -n "$(LD_TRACE_LOADED_OBJECTS=1 LD_LIBRARY_PATH="${1}" "${LD}" "${2}")"' >> ldd.sh
chmod a+x ldd.sh


# Takes the executable as an argument and recursively installs all missing dependencies.
function install_missing_dependencies() {
    executable="${1}"
    # Loop through and install missing dependencies.
    while true
    do
        finished=true
        # Loop through each of the missing libraries for this round.
        while read -r line
        do
            # Parse the various library listing formats.
            if [[ $line == *"/"* ]]; then
                # Extract the filename when a path is present (e.g. /lib64/).
                file=`echo $line | sed 's>.*/\([^/:]*\):.*>\1>'`
            else
                # Extract the filename for missing libraries without a path.
                file=`echo $line | awk '{print $1;}'`
            fi

            if [ -z $file ]; then
                continue
            fi

            # We'll require an empty round before completing.
            finished=false

            echo "Finding dependency for ${file}"

            # Find the package name for this library.
            package=$(repoquery --repofrompath=centos7,http://mirror.centos.org/centos/7/os/`arch` \
                --repoid=centos7 -q --qf="%{name}" --whatprovides "$file" | head -n1)

            install_package "${package}"

            # Copy it over to our library directory.
            find . | grep /${file} | xargs -n1 -I{} cp {} ${lib_directory}/
        done <<< "$(./ldd.sh "${lib_directory}" "${executable}" 2>&1 | grep -e "no version information" -e "not found")"

        # Break once no new files have been copied in a loop.
        if [ "$finished" = true ]; then
            break
        fi
    done
}


# Install the missing dependencies for Chrome.
install_missing_dependencies /opt/google/chrome/chrome


if ! installation_status; then
    # Time for the big guns, we'll try to patch the executables to use our lib directory.
    yum install -y gcc gcc-c++ make autoconf automake
    echo "Linking issues were encountered, attempting to patch the `chrome` executable."
    wget https://github.com/NixOS/patchelf/archive/0.9.tar.gz -O 0.9.tar.gz
    tar zxf 0.9.tar.gz
    pushd patchelf-0.9
    ./bootstrap.sh
    ./configure
    make
    LD="$({ ls -1 ${lib_directory}/ld-linux* | head -n1 ; } 2> /dev/null)"
    ./src/patchelf --set-interpreter "${LD}" --set-rpath "${lib_directory}" /opt/google/chrome/chrome
    ./src/patchelf --set-interpreter "${LD}" --set-rpath "${lib_directory}" /opt/google/chrome/chrome-sandbox
    sed -i 's/\(.*exec cat.*\)/LD_LIBRARY_PATH="" \1/g' /opt/google/chrome/google-chrome
    popd > /dev/null
    echo "Attempted experimental patching of Chrome to use a relocated glibc version."
fi

# Clean up the directory stack.
rm -rf ${working_directory}
popd > /dev/null

# Print out the success status message and exit.
version="$(google-chrome-stable --version)"
if [ $? -eq 0 ]; then
#! /bin/bash


# Copyright 2017-present: Intoli, LLC
# Source: https://intoli.com/blog/installing-google-chrome-on-centos/
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
"install-google-chrome.sh" 264L, 9526C                        1,1           Top
    echo "Successfully installed google-chrome-stable, ${version}."
    exit 0
else
    echo "Installation has failed."
    echo "Please email contact@intoli.com with the details of your operating system."
    echo "If you're using using AWS, please include the AMI identifier for the instance."
    exit 1
fi
[ec2-user@ip-172-31-9-135 tmp]$ wget https://intoli.com/install-google-chrome.sh
--2020-04-25 06:03:57--  https://intoli.com/install-google-chrome.sh
Resolving intoli.com (intoli.com)... 34.233.178.250
Connecting to intoli.com (intoli.com)|34.233.178.250|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 9526 (9.3K) [application/octet-stream]
Saving to: ‘install-google-chrome.sh’

100%[======================================>] 9,526       --.-K/s   in 0s

2020-04-25 06:03:58 (215 MB/s) - ‘install-google-chrome.sh’ saved [9526/9526]

[ec2-user@ip-172-31-9-135 tmp]$ vim install-google-chrome.sh
[ec2-user@ip-172-31-9-135 tmp]$
[ec2-user@ip-172-31-9-135 tmp]$
[ec2-user@ip-172-31-9-135 tmp]$ ls
aerofiler-pytest
akuma4651371416864187358jar
akuma796521989446258153jar
chromedriver_linux64.zip
get-pip.py
hsperfdata_ec2-user
hsperfdata_jenkins
hsperfdata_root
install-google-chrome.sh
jetty-0_0_0_0-8080-war-_-any-1949807998560654925.dir
jetty-0_0_0_0-8080-war-_-any-290324139520912267.dir
jna1275370094734093217jar
jna1994348788991608150jar
systemd-private-5298c4cbc22e4a6082bc500cab27a34d-chronyd.service-31dtbE
venv
winstone724034183948416490.jar
winstone8980879300570731852.jar
[ec2-user@ip-172-31-9-135 tmp]$ rm chromedriver_linux64.zip
[ec2-user@ip-172-31-9-135 tmp]$ 1
-bash: 1: command not found
[ec2-user@ip-172-31-9-135 tmp]$ 2
-bash: 2: command not found
[ec2-user@ip-172-31-9-135 tmp]$ 3
-bash: 3: command not found
[ec2-user@ip-172-31-9-135 tmp]$ sudo curl https://intoli.com/install-google-chrome.sh
#! /bin/bash


# Copyright 2017-present: Intoli, LLC
# Source: https://intoli.com/blog/installing-google-chrome-on-centos/
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


# What this script does is explained in detail in a blog post located at:
# https://intoli.com/blog/installing-google-chrome-on-centos/
# If you're trying to figure out how things work, then you should visit that!


# Require that this runs as root.
[ "$UID" -eq 0 ] || exec sudo "$0" "$@"


# Define some global variables.
working_directory="/tmp/google-chrome-installation"
repo_file="/etc/yum.repos.d/google-chrome.repo"


# Work in our working directory.
echo "Working in ${working_directory}"
mkdir -p ${working_directory}
rm -rf ${working_directory}/*
pushd ${working_directory}


# Add the official Google Chrome Centos 7 repo.
echo "Configuring the Google Chrome repo in ${repo_file}"
echo "[google-chrome]" > $repo_file
echo "name=google-chrome" >> $repo_file
echo "baseurl=http://dl.google.com/linux/chrome/rpm/stable/\$basearch" >> $repo_file
echo "enabled=1" >> $repo_file
echo "gpgcheck=1" >> $repo_file
echo "gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub" >> $repo_file


# Install the Google Chrome signing key.
yum install -y wget
wget https://dl.google.com/linux/linux_signing_key.pub
rpm --import linux_signing_key.pub


# A helper to make sure that Chrome is linked correctly
function installation_status() {
    google-chrome-stable --version > /dev/null 2>&1
    [ $? -eq 0 ]
}


# Try it the old fashioned way, should work on RHEL 7.X.
echo "Attempting a direction installation with yum."
yum install -y google-chrome-stable
if [ $? -eq 0 ]
then
    if installation_status; then
        # Print out the success message.
        echo "Successfully installed Google Chrome!"
        rm -rf ${working_directory}
        popd > /dev/null
        exit 0
    fi
fi


# Uninstall any existing/partially installed versions.
yum --setopt=tsflags=noscripts -y remove google-chrome-stable


# Install yumdownloader/repoquery and download the latest RPM.
echo "Downloading the Google Chrome RPM file."
yum install -y yum-utils
# There have been issues in the past with the Chrome repository, so we fall back to downloading
# the latest RPM directly if the package isn't available there. For further details:
# https://productforums.google.com/forum/#!topic/chrome/xNtfk_wAUC4;context-place=forum/chrome
yumdownloader google-chrome-stable || \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
rpm_file=$(echo *.rpm)
echo "Downloaded ${rpm_file}"


# Install the RPM in a broken state.
rpm -ih --nodeps ${rpm_file}
rm ${rpm_file}


# Install font dependencies, see: https://bugs.chromium.org/p/chromium/issues/detail?id=782161
echo "Installing the required font dependencies."
yum install -y \
    fontconfig \
    fontpackages-filesystem \
    ipa-gothic-fonts \
    xorg-x11-fonts-100dpi \
    xorg-x11-fonts-75dpi \
    xorg-x11-fonts-misc \
    xorg-x11-fonts-Type1 \
    xorg-x11-utils


# Helper function to install packages in the chroot by name (as an argument).
function install_package() {
    # We'll leave the RPMs around to avoid redownloading things.
    if [ -f "$1.rpm" ]; then
        return 0
    fi

    # Find the URL for the package.
    url=$(repoquery --repofrompath=centos7,http://mirror.centos.org/centos/7/os/`arch` \
        --repoid=centos7 -q --qf="%{location}" "$1" | \
        sed s/x86_64.rpm$/`arch`.rpm/ | \
        sed s/i686.rpm$/`arch`.rpm/g | \
        sort -u
    )

    # Download the RPM.
    wget "${url}" -O "$1.rpm"

    # Extract it.
    echo "Extracting $1..."
    rpm2cpio $1.rpm | cpio -idmv > /dev/null 2>&1
}


# Install glibc/ld-linux from CentOS 7.
install_package glibc


# Make the library directory and copy over glibc/ld-linux.
lib_directory=/opt/google/chrome/lib
mkdir -p $lib_directory
cp ./lib/* $lib_directory/ 2> /dev/null
cp ./lib64/* $lib_directory/ 2> /dev/null


# Install `mount` and its mandatory dependencies from CentOS 7.
for package in "glibc" "util-linux" "libmount" "libblkid" "libuuid" "libselinux" "pcre"; do
    install_package "${package}"
done


# Create an `ldd.sh` script to mimic the behavior of `ldd` within the namespace (without bash, etc. dependencies).
echo '#!/bin/bash' > ldd.sh
echo '' >> ldd.sh
echo '# Usage: ldd.sh LIBRARY_PATH EXECUTABLE' >> ldd.sh
echo 'mount --make-rprivate /' >> ldd.sh
echo 'unshare -m bash -c "`tail -n +7 $0`" "$0" "$@"' >> ldd.sh
echo 'exit $?' >> ldd.sh
echo '' >> ldd.sh
echo 'LD=$({ ls -1 ${1}/ld-linux* | head -n1 ; } 2> /dev/null)' >> ldd.sh
echo 'mount --make-private -o remount /' >> ldd.sh
echo 'mount --bind ${1} $(dirname "$({ ls -1 /lib/ld-linux* /lib64/ld-linux* | head -n1 ; } 2> /dev/null)")' >> ldd.sh
echo 'for directory in lib lib64 usr/lib usr/lib64; do' >> ldd.sh
echo '    PATH=./:./bin:./usr/bin LD_LIBRARY_PATH=${1}:./lib64:./usr/lib64:./lib:./usr/lib mount --bind ${1} /${directory} 2> /dev/null' >> ldd.sh
echo 'done' >> ldd.sh
echo 'echo -n "$(LD_TRACE_LOADED_OBJECTS=1 LD_LIBRARY_PATH="${1}" "${LD}" "${2}")"' >> ldd.sh
chmod a+x ldd.sh


# Takes the executable as an argument and recursively installs all missing dependencies.
function install_missing_dependencies() {
    executable="${1}"
    # Loop through and install missing dependencies.
    while true
    do
        finished=true
        # Loop through each of the missing libraries for this round.
        while read -r line
        do
            # Parse the various library listing formats.
            if [[ $line == *"/"* ]]; then
                # Extract the filename when a path is present (e.g. /lib64/).
                file=`echo $line | sed 's>.*/\([^/:]*\):.*>\1>'`
            else
                # Extract the filename for missing libraries without a path.
                file=`echo $line | awk '{print $1;}'`
            fi

            if [ -z $file ]; then
                continue
            fi

            # We'll require an empty round before completing.
            finished=false

            echo "Finding dependency for ${file}"

            # Find the package name for this library.
            package=$(repoquery --repofrompath=centos7,http://mirror.centos.org/centos/7/os/`arch` \
                --repoid=centos7 -q --qf="%{name}" --whatprovides "$file" | head -n1)

            install_package "${package}"

            # Copy it over to our library directory.
            find . | grep /${file} | xargs -n1 -I{} cp {} ${lib_directory}/
        done <<< "$(./ldd.sh "${lib_directory}" "${executable}" 2>&1 | grep -e "no version information" -e "not found")"

        # Break once no new files have been copied in a loop.
        if [ "$finished" = true ]; then
            break
        fi
    done
}


# Install the missing dependencies for Chrome.
install_missing_dependencies /opt/google/chrome/chrome


if ! installation_status; then
    # Time for the big guns, we'll try to patch the executables to use our lib directory.
    yum install -y gcc gcc-c++ make autoconf automake
    echo "Linking issues were encountered, attempting to patch the `chrome` executable."
    wget https://github.com/NixOS/patchelf/archive/0.9.tar.gz -O 0.9.tar.gz
    tar zxf 0.9.tar.gz
    pushd patchelf-0.9
    ./bootstrap.sh
    ./configure
    make
    LD="$({ ls -1 ${lib_directory}/ld-linux* | head -n1 ; } 2> /dev/null)"
    ./src/patchelf --set-interpreter "${LD}" --set-rpath "${lib_directory}" /opt/google/chrome/chrome
    ./src/patchelf --set-interpreter "${LD}" --set-rpath "${lib_directory}" /opt/google/chrome/chrome-sandbox
    sed -i 's/\(.*exec cat.*\)/LD_LIBRARY_PATH="" \1/g' /opt/google/chrome/google-chrome
    popd > /dev/null
    echo "Attempted experimental patching of Chrome to use a relocated glibc version."
fi

# Clean up the directory stack.
rm -rf ${working_directory}
popd > /dev/null

# Print out the success status message and exit.
version="$(google-chrome-stable --version)"
if [ $? -eq 0 ]; then
    echo "Successfully installed google-chrome-stable, ${version}."
    exit 0
else
    echo "Installation has failed."
    echo "Please email contact@intoli.com with the details of your operating system."
    echo "If you're using using AWS, please include the AMI identifier for the instance."
    exit 1
fi
[ec2-user@ip-172-31-9-135 tmp]$
[ec2-user@ip-172-31-9-135 tmp]$
[ec2-user@ip-172-31-9-135 tmp]$
[ec2-user@ip-172-31-9-135 tmp]$ sudo wget https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_linux64.zip
--2020-04-25 06:07:39--  https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_linux64.zip
Resolving chromedriver.storage.googleapis.com (chromedriver.storage.googleapis.com)... 172.217.25.144, 2404:6800:4006:805::2010
Connecting to chromedriver.storage.googleapis.com (chromedriver.storage.googleapis.com)|172.217.25.144|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 4943146 (4.7M) [application/zip]
Saving to: ‘chromedriver_linux64.zip’

100%[======================================>] 4,943,146   17.8MB/s   in 0.3s

2020-04-25 06:07:40 (17.8 MB/s) - ‘chromedriver_linux64.zip’ saved [4943146/4943146]

[ec2-user@ip-172-31-9-135 tmp]$ ls
aerofiler-pytest
akuma4651371416864187358jar
akuma796521989446258153jar
chromedriver_linux64.zip
get-pip.py
hsperfdata_ec2-user
hsperfdata_jenkins
hsperfdata_root
install-google-chrome.sh
jetty-0_0_0_0-8080-war-_-any-1949807998560654925.dir
jetty-0_0_0_0-8080-war-_-any-290324139520912267.dir
jna1275370094734093217jar
jna1994348788991608150jar
systemd-private-5298c4cbc22e4a6082bc500cab27a34d-chronyd.service-31dtbE
venv
winstone724034183948416490.jar
winstone8980879300570731852.jar
[ec2-user@ip-172-31-9-135 tmp]$ sudo unzip chromedriver_linux64.zip
Archive:  chromedriver_linux64.zip
  inflating: chromedriver
[ec2-user@ip-172-31-9-135 tmp]$ sudo mv chromedriver /usr/bin/chromedriver
[ec2-user@ip-172-31-9-135 tmp]$ chromedriver --version
ChromeDriver 80.0.3987.106 (f68069574609230cf9b635cd784cfb1bf81bb53a-refs/branch-heads/3987@{#882})
[ec2-user@ip-172-31-9-135 tmp]$ sudo service jenkins stop
Stopping jenkins (via systemctl):                          [  OK  ]
[ec2-user@ip-172-31-9-135 tmp]$ quit
-bash: quit: command not found
[ec2-user@ip-172-31-9-135 tmp]$ Connection to ec2-13-55-210-56.ap-southeast-2.compute.amazonaws.com closed by remote host.
Connection to ec2-13-55-210-56.ap-southeast-2.compute.amazonaws.com closed.

~
```

