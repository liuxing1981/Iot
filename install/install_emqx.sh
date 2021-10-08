#! /bin/sh
set -e

case $1 in
    "emqx-ee")
        broker="emqx-ee"
        package="emqx-ee"
        ;;
    "emqx-edge")
        broker="emqx-edge"
        package="emqx-edge"
        ;;
    *)
        broker="emqx-ce"
        package="emqx"
        ;;
esac

[ -f /etc/redhat-release ] && ISCENTOS=true
[ -f /etc/debian_version ] && ISDEB=true
[ ! -z "$(cat /etc/os-release |grep -o openSUSE)" ] && ISSUSE=true

if [ ! -z $ISDEB ]; then
    apt update && apt install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg-agent \
        software-properties-common \
        lsb-core

    curl -fsSL https://repos.emqx.io/gpg.pub | apt-key add -

    [ $(lsb_release -d | awk '{print $2}') = 'Ubuntu' ] && add-apt-repository \
        "deb [arch=amd64] https://repos.emqx.io/${broker}/deb/ubuntu/ \
        ./$(lsb_release -cs) \
        stable"

    [ $(lsb_release -d | awk '{print $2}') = 'Debian' ] && add-apt-repository \
        "deb [arch=amd64] https://repos.emqx.io/${broker}/deb/debian/ \
        ./$(lsb_release -cs) \
        stable"

    apt update && apt install -y ${package}
    echo "EMQ X install success"
fi

if [ ! -z $ISSUSE ]; then
    zypper in -y curl rsyslog
    curl -L -o /tmp/gpg.pub https://repos.emqx.io/gpg.pub
    rpmkeys --import /tmp/gpg.pub
    zypper ar -f -c https://repos.emqx.io/${broker}/redhat/opensuse/leap/stable emqx
    zypper in -y ${package}
    echo "EMQ X install success"
fi

if [ ! -z $ISCENTOS ];then
    yum install -y yum-utils \
        device-mapper-persistent-data \
        lvm2

    num=$(cat /etc/redhat-release | grep -o [0-9] |head -n 1)
    yum-config-manager \
        --add-repo \
        https://repos.emqx.io/${broker}/redhat/centos/${num}/${broker}.repo

    yum install -y ${package}
    echo "EMQ X install success"
fi
