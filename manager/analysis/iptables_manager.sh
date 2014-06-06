#! /bin/sh

victim='192.168.228.240'
my_internal='192.168.228.1'
my_ip='192.168.100.50'
trusthost='192.168.100.60'

echo 1 > /proc/sys/net/ipv4/ip_forward

###
#Flush & Reset
###
/sbin/iptables -F
/sbin/iptables -t nat -F
/sbin/iptables -X

###
#Default Rule
###
/sbin/iptables -P INPUT DROP
/sbin/iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
#/sbin/iptables -P OUTPUT DROP
#/sbin/iptables -A OUTPUT -d 192.168.100.0/24 -j DROP
#/sbin/iptables -A OUTPUT -d 192.168.100.1 -j ACCEPT
/sbin/iptables -P FORWARD ACCEPT
#/sbin/iptables -P FORWARD DROP
#/sbin/iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT


###
#Loopback
###
/sbin/iptables -A INPUT -i lo -j ACCEPT
/sbin/iptables -A OUTPUT -o lo -j ACCEPT

###
#ssh -> myhost
###
#/sbin/iptables -A INPUT -p tcp ! --syn -m state --state NEW -j DROP
/sbin/iptables -A INPUT -p tcp -m state --state NEW -s $trusthost -d $my_ip --dport 22 -j ACCEPT
/sbin/iptables -A INPUT -p tcp -m state --state NEW -s $victim -d $my_ip --dport 22 -j ACCEPT

###
#ssh myhost -> 
###
/sbin/iptables -A OUTPUT -p tcp -m state --state NEW -d $trusthost -s $my_ip --dport 22 -j ACCEPT
/sbin/iptables -A OUTPUT -p tcp -m state --state NEW -d $victim -s $my_ip --dport 22 -j ACCEPT

###
#victimOS -> myhost
###
/sbin/iptables -A INPUT -s $victim -d $my_internal -j ACCEPT

###
#Masquerade
###
/sbin/iptables -t nat -A POSTROUTING -s $victim -o eth0 -j MASQUERADE

###
#victimOS
###
/sbin/iptables -A FORWARD -o eth0 -s $victim -d 192.168.100.0/24 -j DROP
/sbin/iptables -t nat -A PREROUTING -p tcp -d $my_ip --dport 58455 -j DNAT --to-destination $victim
