#!/bin/sh

victim_ip='192.168.123.111'

#ルール初期化
iptables -F
iptables -X

# br0-tap0間を遮断
#iptables -P FORWARD DROP

#チェイン作成
iptables -N vboxin
iptables -N vboxout
iptables -F vboxin
iptables -F vboxout

#チェインに通信経路を設定
iptables -A FORWARD -m physdev --physdev-out tap0 -j vboxin
iptables -A FORWARD -m physdev --physdev-in tap0 -j vboxout

#チェイン設定
#iptables -A vboxin -j ACCEPT
#iptables -A vboxout -j ACCEPT

#入力
#iptables -A vboxin -p tcp --dport 23 -j ACCEPT
#iptables -A vboxin -p tcp -j DROP
#iptables -A vboxin -p tcp --dport 80 -j DROP

#出力
iptables -A vboxout -p tcp --dport 58455 -j DROP
iptables -A vboxout -d $victim_ip/24 -j DROP #同一のネットワークへの通信
#iptables -A vboxout -d 192.168.123.1 -j ACCEPT
#iptables -A vboxout -p tcp -j DROP


