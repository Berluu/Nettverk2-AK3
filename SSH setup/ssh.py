    # importera nødvendige bibliotek
import serial
import time

# Seriell tilkopling

    #Brukar input, sett opp seriell port
port = input("Skriv inn seriell port (f.eks COM3, eller /dev/ttyS3)")

    # Prøv å opprette seriell tilkopling
try:
    ser = serial.Serial(
        port=port,
        baudrate=9600,
        parity="N",
        stopbits=1,
        bytesize=8,
        timeout=8
    )
        # Sjekk om tilkopling er oppretta
    if ser.isOpen():
        print("Serial port is open")
    else:
        print("Serial port failed to open")

except serial.SerialException as e:
    print(f"Error opening serial port: {e}")


# Velg om du skal sette opp switch eller ruter
Device = int(input("Ruter=1, Switch=2: "))

    # Felles variablar for user inputs
hostname = input("Sett hostnamn: ")
username = input("Sett brukarnamn (cisco): ")
password = input("Sett passord (cisco): ")
IPaddress = input("Sett IP adresse (xx.xx.xx.xx):")
print("Enhet starta opp, vent 20 sekund")

# Felles oppsett

    # Starta oppsettet med å avbryte startup config
ser.write("\r\n".encode())
ser.write("no\r\n".encode())
ser.write("yes\r\n".encode())
time.sleep(20) 


# Enter configuration terminal
ser.write("\r\n".encode())
ser.write("enable\r\n".encode())

    # Tilfelle passord blir spurt om (f.eks om skriptet måtte køyrast 2 gangar)
output = ser.read(ser.in_waiting or 1).decode(errors='ignore')
if "Password" in output:
    ser.write((password + "\r\n").encode())
    time.sleep(1)

ser.write("conf t\r\n".encode())
time.sleep(1)


# Spesifike oppsett for ruter eller switch

if Device==1:
    # Spesifikt oppsett for ruter

    # User inputs for ruter:
    MGMTport = input("Sett port for management nettverk (f.eks g0/0/0): ")

    commands_R = [    # Kommandoar for ruter
        f"hostname {hostname}",                     # Sett hostname
        f"interface {MGMTport}",                    # Sett interface
        "no shutdown",                              # Aktiver interface
        "exit",     
        f"interface {MGMTport}.99",                 # Sett subinterface
        "encapsulation dot1Q 99",                   # Sett vlan 99
        f"ip address {IPaddress} 255.255.255.0",    # Sett IP på subinterface
        "no shutdown",                              # Aktiver subinterface
        "exit",
    ]
        # Utfør kommandoane
    for cmd in commands_R:
        ser.write((cmd + "\r\n").encode())
        time.sleep(1)  # Vent på at kommandoen skal bli prosessert
        response = ser.read(ser.in_waiting or 1).decode(errors='ignore')
        if response:
            print(response, end="")
    
elif Device==2:
    # Spesifikt oppsett for switch

        # User inputs spesifikt for switch:
    Gateway = input("Skriv default gateway (xx.xx.xx.1):")
    Trnkport = input("Skriv inn trunk port (g1/0/.. eller Fa0/..): ")

    # Spør om access port skal settast opp
    VelgAcport = input("Vil du sette access port til management nettet? (y/n): ")
        # Sett access port om ynskjeleg
    if VelgAcport=="y":
        Acport = input("Skriv inn access port (g1/.. eller Fa0/..): ")
            
            # Kommandoar for access port
        commands_Acport = [    
            f"interface {Acport}",                  # Inn på access port
            "switchport mode access",               # Sett access mode
            "switchport access vlan 99",            # Sett access vlan
            "no shutdown",                          # Aktiver port
            "exit"
        ]
            # Utfør kommandoane
        for acmd in commands_Acport:
            ser.write((acmd + "\r\n").encode())
            time.sleep(1)  # Vent på at kommandoen skal bli prosessert
            response = ser.read(ser.in_waiting or 1).decode(errors='ignore')
            if response:
                print(response, end="")
    else:
        Acport = None
    
        # Kommandoar for switch
    commands_SW = [    
        f"hostname {hostname}",                     # Sett hostname
        "vlan 99",
        "exit",
        "interface vlan 99",                        # Inn på management vlan
        f"ip address {IPaddress} 255.255.255.0",    # Sett IP på vlan
        "no shutdown",                              # Aktiver vlan
        "exit",
        "ip routing",                               # Aktiver routing, trengs berre på layer 3 switch, kjem feilmelding på layer 2 switch men det går fint
        f"interface {Trnkport}",                    # Inn på trunk port
        "switchport mode trunk",                    # Sett trunk mode
        "no shutdown",                              # Aktiver port
        "exit",
        f"ip default-gateway {Gateway}"             # Sett default gateway
    ]
        # Utfør kommandoane
    for SWcmd in commands_SW:
        ser.write((SWcmd + "\r\n").encode())
        time.sleep(1)  # Vent på at kommandoen skal bli prosessert
        response = ser.read(ser.in_waiting or 1).decode(errors='ignore')
        if response:
            print(response, end="")
    
# SSH oppsett
commands_ssh = [
    f"enable secret {password}",                                # Sett passord på device
    "ip domain name eksempel.local",                            # Sett domenenamn
    f"username {username} privilege 15 password {password}",    # Sett brukarnamn og passord til SSH
    "crypto key generate rsa modulus 1024",                     # Generer RSA nøkkel
    "ip ssh version 2",                                         # Sett SSH versjon til 2
    "line vty 0 5",                                             # osv....
    "login local",
    "transport input ssh",
    "end"
]
    # Utfør kommandoane
for SSHcmd in commands_ssh:
        ser.write((SSHcmd + "\r\n").encode())
        time.sleep(1)  # Vent på at kommandoen skal bli prosessert
        response = ser.read(ser.in_waiting or 1).decode(errors='ignore')
        if response:
            print(response, end="")

    # Avslutt og lukk seriell tilkopling
print("SSH oppsett fullført")
ser.close()


