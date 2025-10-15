# Python skript for å sette opp SSH på rutera og switchar

## Forutsetningar
 - Python er installert
 - Pyserial er installert

## Korleis skriptet fungera
!! For alle inputs, følg overview (link??) !!

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
3. Deretter går skriptet vidare til å faktisk sette opp SSH, som er same for både rutera og switchar. Dette skjer også automatisk
  
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
6. Deretter går skriptet vidare til å faktisk sette opp SSH, som er same for både rutera og switchar. Dette skjer også automatisk

### Det som skjer under SSH oppsett
Alt dette skjer automatisk:
- enable secret blir satt til "cisco"
- domenet blir satt til eksempel.local
- Brukarnamn og passord til SSH blir satt til "cisco"
- Rsa nøkkel blir generert
- Sett ssh til version 2
- Sett line vty til 0 5
- Sett login local
- Sett transport input ssh

Det er alt som skjer i ssh.py



