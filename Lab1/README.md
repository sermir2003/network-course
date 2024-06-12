# Лабораторная работа 1

## Построение сети

0. Допустим EVE-NG установлен и работает, и загружены какие-то образы Cisco Switch и Cisco Router.

1. Разместим два виртуальных компьютера, три коммутатора и один маршрутизатор, как показано на рисунке. Соединим их линками.
![`placeholder`](./meta/fig-title.png)

2. Включим все устройства и сконфигурируем их
    1. VPC1

        - Назначим узлу понятное имя
        - Назначим адрес в сети 10.0.10.0/24 и gateway
        - Запишем конфигурацию

        ```console
        set pcname VPC1
        ip 10.0.10.2/24 10.0.10.1
        save VPC1.cfg
        ```

    1. VPC2

        - Назначим узлу понятное имя
        - Назначим адрес в сети 10.0.20.0/24 и gateway
        - Запишем конфигурацию

        ```console
        set pcname VPC2
        ip 10.0.20.2/24 10.0.20.1
        save VPC2.cfg
        ```

    1. SW1

        - Назначим узлу понятное имя
        - Объявим два vlan: 10 и 20
        - Настроим линк с VPC1, чтобы создать виртуальную сеть vlan 10
        - Настроим линки с SW0 и SW2 так, чтобы сквозь них прокидывались vlan-ы
        - Запишем конфигурацию

        ```console
        enable
            configure terminal
                hostname SW1
                vlan 10
                    exit
                vlan 20
                    exit
                interface gi 0/2
                    switchport mode access
                    switchport access vlan 10
                    exit
                interface range gi 0/0-1
                    switchport trunk encapsulation dot1q
                    switchport mode trunk
                    switchport trunk allowed vlan 10,20
                    exit
                exit
            write memory
        ```

    1. SW2

        - Назначим узлу понятное имя
        - Объявим два vlan: 10 и 20
        - Настроим линк с VPC2, чтобы создать виртуальную сеть vlan 20
        - Настроим линки с SW0 и SW1 так, чтобы сквозь них прокидывались vlan-ы
        - Запишем конфигурацию

        ```console
        enable
            configure terminal
                hostname SW2
                vlan 10
                    exit
                vlan 20
                    exit
                interface gi 0/2
                    switchport mode access
                    switchport access vlan 20
                    exit
                interface range gi 0/0-1
                    switchport trunk encapsulation dot1q
                    switchport mode trunk
                    switchport trunk allowed vlan 10,20
                    exit
                exit
            write memory
        ```

    1. SW0

        - Назначим узлу понятное имя
        - Объявим два vlan: 10 и 20
        - Настроим линки с R0, SW1 и SW2 так, чтобы сквозь них прокидывались vlan-ы
        - Назначим узел корнем STP деревьев для vlan 10 и vlan 20
        - Запишем конфигурацию

        ```console
        enable
            configure terminal
                hostname SW0
                vlan 10
                    exit
                vlan 20
                    exit
                interface range gi 0/0-2
                    switchport trunk encapsulation dot1q
                    switchport mode trunk
                    switchport trunk allowed vlan 10,20
                    exit
                spanning-tree vlan 10 root primary
                spanning-tree vlan 20 root primary
                exit
            write memory
        ```

    1. R0

        - Назначим узлу понятное имя
        - Включим интерфейс на линке с SW0
        - Объявим на нём два подъинтерфейса для двух пар <vlan, сеть>
        - Запишем конфигурацию

        ```console
        Would you like to enter the initial configuration dialog? > no
        enable
            configure terminal
                hostname R0
                interface gi 0/1
                no shutdown

                interface gi 0/1.1
                    encapsulation dot1q 10
                    ip address 10.0.10.1 255.255.255.0
                    exit
                interface gi 0/1.2
                    encapsulation dot1q 20
                    ip address 10.0.20.1 255.255.255.0
                    exit
                exit
            write memory
        ```

## Проверка корректности и оценивание

1. Топология сети собрана по схеме из задания
1. VPC1 находится в VLAN 10 и имеет адрес 10.0.10.2/24
1. VPC2 находится в VLAN 20 и имеет адрес 10.0.20.2/24
1. Посмотрим, что коммутаторы думают о spanning-tree разных VLAN

    <details>
    <summary>VLAN 10</summary>

    ```console
    SW1>show spanning-tree vlan 10

    VLAN0010
    Spanning tree enabled protocol ieee
    Root ID    Priority    24586
                Address     5000.0002.0000
                Cost        4
                Port        1 (GigabitEthernet0/0)
                Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

    Bridge ID  Priority    32778  (priority 32768 sys-id-ext 10)
                Address     5000.0003.0000
                Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
                Aging Time  300 sec

    Interface           Role Sts Cost      Prio.Nbr Type
    ------------------- ---- --- --------- -------- --------------------------------
    Gi0/0               Root FWD 4         128.1    P2p 
    Gi0/1               Desg FWD 4         128.2    P2p 
    Gi0/2               Desg FWD 4         128.3    P2p
    ```

    ```console
    SW2>show spanning-tree vlan 10

    VLAN0010
    Spanning tree enabled protocol ieee
    Root ID    Priority    24586
                Address     5000.0002.0000
                Cost        4
                Port        1 (GigabitEthernet0/0)
                Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

    Bridge ID  Priority    32778  (priority 32768 sys-id-ext 10)
                Address     5000.0004.0000
                Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
                Aging Time  300 sec

    Interface           Role Sts Cost      Prio.Nbr Type
    ------------------- ---- --- --------- -------- --------------------------------
    Gi0/0               Root FWD 4         128.1    P2p 
    Gi0/1               Altn BLK 4         128.2    P2p
    ```

    ```console
    SW0>show spanning-tree vlan 10

    VLAN0010
    Spanning tree enabled protocol ieee
    Root ID    Priority    24586
                Address     5000.0002.0000
                This bridge is the root
                Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

    Bridge ID  Priority    24586  (priority 24576 sys-id-ext 10)
                Address     5000.0002.0000
                Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
                Aging Time  300 sec

    Interface           Role Sts Cost      Prio.Nbr Type
    ------------------- ---- --- --------- -------- --------------------------------
    Gi0/0               Desg FWD 4         128.1    P2p 
    Gi0/1               Desg FWD 4         128.2    P2p 
    Gi0/2               Desg FWD 4         128.3    P2p
    ```

    </details>

    <details>
    <summary>VLAN 20</summary>

    ```console
    SW1>show spanning-tree vlan 20

    VLAN0020
    Spanning tree enabled protocol ieee
    Root ID    Priority    24596
                Address     5000.0002.0000
                Cost        4
                Port        1 (GigabitEthernet0/0)
                Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

    Bridge ID  Priority    32788  (priority 32768 sys-id-ext 20)
                Address     5000.0003.0000
                Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
                Aging Time  300 sec

    Interface           Role Sts Cost      Prio.Nbr Type
    ------------------- ---- --- --------- -------- --------------------------------
    Gi0/0               Root FWD 4         128.1    P2p 
    Gi0/1               Desg FWD 4         128.2    P2p
    ```

    ```console
    SW2>show spanning-tree vlan 20

    VLAN0020
    Spanning tree enabled protocol ieee
    Root ID    Priority    24596
                Address     5000.0002.0000
                Cost        4
                Port        1 (GigabitEthernet0/0)
                Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

    Bridge ID  Priority    32788  (priority 32768 sys-id-ext 20)
                Address     5000.0004.0000
                Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
                Aging Time  300 sec

    Interface           Role Sts Cost      Prio.Nbr Type
    ------------------- ---- --- --------- -------- --------------------------------
    Gi0/0               Root FWD 4         128.1    P2p 
    Gi0/1               Altn BLK 4         128.2    P2p 
    Gi0/2               Desg FWD 4         128.3    P2p
    ```

    ```console
    SW0>show spanning-tree vlan 20

    VLAN0020
    Spanning tree enabled protocol ieee
    Root ID    Priority    24596
                Address     5000.0002.0000
                This bridge is the root
                Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

    Bridge ID  Priority    24596  (priority 24576 sys-id-ext 20)
                Address     5000.0002.0000
                Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
                Aging Time  300 sec

    Interface           Role Sts Cost      Prio.Nbr Type
    ------------------- ---- --- --------- -------- --------------------------------
    Gi0/0               Desg FWD 4         128.1    P2p 
    Gi0/1               Desg FWD 4         128.2    P2p 
    Gi0/2               Desg FWD 4         128.3    P2p
    ```

    </details>

    Важным для нас в этом пункте является то, что в обоих случаях SW0 считает себя корнем (`This bridge is the root`).
1. В продолжение предыдущего пункта заметим, что на коммутаторе SW2 в деревьях STP как для VLAN 10, так и для VLAN 20 линк c SW1 (интерфейс Gi0/1) считается альтернативным и заблокированным: `Gi0/1    Altn BLK 4    128.2    P2p`. Может немного смущать, что тот же самый линк Desg и FWD на другой стороне, но люди пишут, что это нормально

    > Spanning tree won’t block both, because after one switch blocks it the link ceases to be a loop.
    >
    > — Someone on [community.spiceworks.com](https://community.spiceworks.com/t/hp-procurve-switch-spanning-tree-is-blocking-only-one-side-of-a-redunant-link/305718)
1. VPC1 и VPC2 могут достучаться до VPC1 и VPC2

    ```console
    VPC1> ping 10.0.10.2

    10.0.10.2 icmp_seq=1 ttl=64 time=0.001 ms
    10.0.10.2 icmp_seq=2 ttl=64 time=0.001 ms
    10.0.10.2 icmp_seq=3 ttl=64 time=0.001 ms
    10.0.10.2 icmp_seq=4 ttl=64 time=0.001 ms
    10.0.10.2 icmp_seq=5 ttl=64 time=0.001 ms

    VPC1> ping 10.0.20.2

    84 bytes from 10.0.20.2 icmp_seq=1 ttl=63 time=9.588 ms
    84 bytes from 10.0.20.2 icmp_seq=2 ttl=63 time=7.080 ms
    84 bytes from 10.0.20.2 icmp_seq=3 ttl=63 time=8.379 ms
    84 bytes from 10.0.20.2 icmp_seq=4 ttl=63 time=8.733 ms
    84 bytes from 10.0.20.2 icmp_seq=5 ttl=63 time=6.686 ms
    ```

    ```console
    VPC2> ping 10.0.10.2

    84 bytes from 10.0.10.2 icmp_seq=1 ttl=63 time=17.683 ms
    84 bytes from 10.0.10.2 icmp_seq=2 ttl=63 time=6.103 ms
    84 bytes from 10.0.10.2 icmp_seq=3 ttl=63 time=8.145 ms
    84 bytes from 10.0.10.2 icmp_seq=4 ttl=63 time=6.996 ms
    84 bytes from 10.0.10.2 icmp_seq=5 ttl=63 time=13.530 ms

    VPC2> ping 10.0.20.2

    10.0.20.2 icmp_seq=1 ttl=64 time=0.001 ms
    10.0.20.2 icmp_seq=2 ttl=64 time=0.001 ms
    10.0.20.2 icmp_seq=3 ttl=64 time=0.001 ms
    10.0.20.2 icmp_seq=4 ttl=64 time=0.001 ms
    10.0.20.2 icmp_seq=5 ttl=64 time=0.001 ms
    ```

1. Работа выполнена в EVE-NG, файлы конфигурации устройств лежат в директории `configs` текущего репозитория, экспортированная лабораторная работа в архиве `exported-lab.zip`.
1. Отказоустойчивость

    В случае если все три линка между маршрутизаторами работают, сеть связна. Мы убедились в этом в позапрошлом пункте, когда пинговали узлы. Учитывая конфигурацию, сеть должна выдерживать отказ одного из этих линков. Но для большей уверенности попробуем отдельно отключить каждый из линков и проверим связность:

    1. Линк между SW0 и SW1

        ![`placeholder`](./meta/fig-del-sw0-sw1.png)

        ```console
        VPC1> ping 10.0.20.2 -c 3

        84 bytes from 10.0.20.2 icmp_seq=1 ttl=63 time=9.992 ms
        84 bytes from 10.0.20.2 icmp_seq=2 ttl=63 time=9.194 ms
        84 bytes from 10.0.20.2 icmp_seq=3 ttl=63 time=9.378 ms
        ```

        ```console
        VPC2> ping 10.0.10.2 -c 3

        84 bytes from 10.0.10.2 icmp_seq=1 ttl=63 time=9.439 ms
        84 bytes from 10.0.10.2 icmp_seq=2 ttl=63 time=7.725 ms
        84 bytes from 10.0.10.2 icmp_seq=3 ttl=63 time=7.955 ms
        ```

    1. Линк между SW0 и SW2

        ![`placeholder`](./meta/fig-del-sw0-sw2.png)

        ```console
        VPC1> ping 10.0.20.2 -c 3

        84 bytes from 10.0.20.2 icmp_seq=1 ttl=63 time=9.453 ms
        84 bytes from 10.0.20.2 icmp_seq=2 ttl=63 time=7.539 ms
        84 bytes from 10.0.20.2 icmp_seq=3 ttl=63 time=10.126 ms
        ```

        ```console
        VPC2> ping 10.0.10.2 -c 3

        84 bytes from 10.0.10.2 icmp_seq=1 ttl=63 time=9.150 ms
        84 bytes from 10.0.10.2 icmp_seq=2 ttl=63 time=10.693 ms
        84 bytes from 10.0.10.2 icmp_seq=3 ttl=63 time=28.803 ms
        ```

    1. Линк между SW1 и SW2

        ![`placeholder`](./meta/fig-del-sw1-sw2.png)

        ```console
        VPC1> ping 10.0.20.2 -c 3

        84 bytes from 10.0.20.2 icmp_seq=1 ttl=63 time=6.260 ms
        84 bytes from 10.0.20.2 icmp_seq=2 ttl=63 time=7.824 ms
        84 bytes from 10.0.20.2 icmp_seq=3 ttl=63 time=6.584 ms
        ```

        ```console
        VPC2> ping 10.0.10.2 -c 3

        84 bytes from 10.0.10.2 icmp_seq=1 ttl=63 time=6.343 ms
        84 bytes from 10.0.10.2 icmp_seq=2 ttl=63 time=5.625 ms
        84 bytes from 10.0.10.2 icmp_seq=3 ttl=63 time=5.467 ms
        ```

1. Данная работа сопровождается каким-то описанием.
