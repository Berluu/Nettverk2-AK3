# Ansible for oppsett av rutera og switchar 
Her skriv eg om korleis anisble oppsettet mitt fungera

## Forutsetningar
- Du har eit miljø der ansible er satt opp riktig
- Du har installert cisco.ios ansible modulen
- Einingane er satt opp riktig med ssh

## Hosts fila
- Eg har lagt inn alle einingane som ansible hosts, om du har brukt andre IP-adresser enn i det eg har gjort så må det endrast her
- Om du vil sette opp meir enn 1 access switch så kan du det:
    - Eg har lagt til ein ansible host for enda ein access switch som er kommentert ut, den kan brukast
    - Hugs å endre "hosts: " i SWaccess.yml om du gjer dette.

## Funksjonaliteten til playbookane
Her er ei oversikt over kva som skjer i dei forskjellege playbookane 

### Ruter1.yml
- Setter opp sub interfaces med IP-adresser for VLAN 10, 20, og 99.
- Sett opp HSRP for 192.168.10.1 (preempt), 192.168.20.1, og 10.99.2.1 (preempt).
- Sett opp OSPF for nettverka 10.99.1.0, 10.99.2.0, 192.168.10.0, og 192.168.20.0.
- Sett opp DHCP for VLAN 10 og 20, der dei fyrste 10 adressene er excluded 

### Ruter2.yml
- Setter opp sub interfaces med IP-adresser for VLAN 10, 20, og 99.
- Sett opp HSRP for 192.168.10.1, 192.168.20.1 (preempt), og 10.99.2.1.
- Sett opp OSPF for nettverka 10.99.1.0, 10.99.2.0, 192.168.10.0, og 192.168.20.0.
- Sett opp DHCP for VLAN 10 og 20, der dei fyrste 10 adressene er excluded 

### SW2.yml
- Lagar VLAN 10, og 20
- Sett port Fa0/23 som trunk sidan begge ruterane skal vere kopla til denne.


### SW3.yml
- Lagar VLAN 10, og 20
- Sett port Fa0/23 og Fa0/24 til trunk for å bruke til access switchane
- Sett opp Etherchannel på Fa0/1 og Fa0/2, og sett begge til trunk

### SWaccess.yml
- Lagar VLAN 10, og 20
- Sett port g1/0/1 til access VLAN 10
- Sett port g1/0/2 til access VLAN 20

Du må endre "hosts: " om enda ein access switch blir satt opp.
