# README WOOOOOOOOOOOO

## Setup rekkefølge
Eg satt opp einingane i denne rekkefølga, men det viktigaste er at Ruter1.yml og Ruter2.yml blir køyrt før resten av switchane blir satt opp.
 - ssh.py til management switch (SW1)
 - ssh.py til ruter 1 (R1)
 - ssh.py til ruter 2 (R2)
 - ansible playbook Ruter1.yml og Ruter2.yml
 - ssh.py til neste switch (SW2)
 - ansible playbook SW2.yml
 - ssh.py til neste switch (SW3)
 - ansible playbook SW3.yml
 - ssh.py til neste switch (SW4)
 - ansible playbook SWaccess.yml

Du finn korleis ssh.py fungera [her](#ssh.py-sett-opp-ssh-på-rutera-og-switchar)
   
## FYI
- På SW1 blir det berre sett opp ein trunk port med ssh.py, du treng enda ein sidan begge ruterane skal koplast til
   - Sett opp og kople til med SSH
     ``` ssh cisco@10.99.1.2 ```
   - Sett opp trunk port, her er copypaste for deg:
```
enable
conf t

int g1/0/23
switchport mode trunk
no shutdown
end
 ```
- Sjekk at einingane dine bruka GigabitEthernet eller FastEthernet og om det stemmer overens i ansible. Eg har lagt til kommentarar alle plassar dette kan gjelde.


# ssh.py sett opp SSH på rutera og switchar


## Forutsetningar
 - Python er installert
 - Pyserial er installert

## Korleis skriptet fungera

1. Sørg for at du er kopla til ruteren eller switchen med konsoll kabel
2. Køyr skriptet
3. Skriv inn seriell porten du bruka (f.eks COM3 med windows, eller /dev/ttyS3 med linux)
4. Velg setup: skriv inn "1" for ruter setup og "2" for switch setup
5. Her blir du spurt om fleire inputs, følg det som står i overview (link??) for å sleppe å endre noko i ansible.
    - Med IP addresse blir det meint management IP-en du vil sette på eininga, f.eks på R1 sett du 10.99.1.1. Subnet maske blir satt automatisk til 255.255.255.0
6. Vent i ca. 20 sekund mens eininga startar opp

### Ruter oppsett
1. Skriv inn vilken port du skal bruke for management nettverket.
   - Det er den fysiske porten, f.eks på R1 sett du g0/0/0 (om det er den du skal bruke)
2. Resten skjer av seg sjølv:
   - Hostname blir satt.
   - Porten du satt blir aktivert.
   - Subinterface på porten blir satt med .99 (.99 for management VLAN).
   - IP adressa blir satt på subinterface.
3. Deretter går skriptet vidare til å faktisk sette opp SSH, som er same for både rutera og switchar. Dette skjer også automatisk.
  
### Switch oppsett
1. Skriv inn default gateway for switchen, f.eks på SW1 sett du 10.99.1.1
2. Skriv inn porten du vil bruke som trunk, f.eks på SW1 sett du g1/0/24
   - OBS! Enda ein trunk port må settast opp på SW1, men dette skriptet lar deg berre gjere sette ein om gongen
3. Om du treng ein access port til management nettverket skriv "y"
4. Om du valgte "y" blir du bedt om å skrive inn kva port du vil ha som access, f.eks på SW1 sett du g1/0/1
5. Resten skjer av seg sjølv:
   - Om access port blei valgt
     - Porten blir aktivert, og satt til access mode vlan 99
   - Hostname blir satt
   - VLAN 99 blir laga (det trengs i tilfelle access port ikkje blei satt)
   - VLAN 99 interface blir aktivert
   - IP adresse blir satt på VLAN interface
   - ip routing blir aktivert (tilfelle switchen er lag3 så trengs dette, det kjem feilmelding på lag2 switchar men øydelegg ingenting)
   - Trunk port blir aktivert og satt til switchport mode trunk
   - Default gateway blir satt
6. Deretter går skriptet vidare til å faktisk sette opp SSH, som er same for både rutera og switchar. Dette skjer også automatisk.




# Ansible for oppsett av rutera og switchar 
- Sjekk at einingane dine bruka GigabitEthernet eller FastEthernet og om det stemmer overens med .yml filene. Eg har lagt til kommentarar alle plassar dette kan gjelde.


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


