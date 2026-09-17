# Ubuntu Server 24.04 LTS base per a Serveis en Xarxa

Guia pràctica per crear, instal·lar, configurar i verificar una màquina virtual amb Ubuntu Server 24.04 LTS que servirà com a base per a les pràctiques del mòdul MP07 Serveis de Xarxa de 2n de SMX.

El procediment segueix la presentació `GUIA UBUNTU SERVER` i incorpora els aclariments i correccions de la guia docent associada. L'objectiu no és únicament aconseguir que Ubuntu arrenqui, sinó deixar una màquina identificable, actualitzada, administrable, connectada correctament i preparada per desplegar-hi serveis de xarxa.

> [!IMPORTANT]
> No copiïs cegament noms d'interfície, fitxers de Netplan o adreces IP de les captures. Valida sempre quins valors existeixen realment a la teva màquina.

## Índex

1. [Resultat final](#resultat-final)
2. [Convencions de la guia](#convencions-de-la-guia)
3. [Requisits previs](#requisits-previs)
4. [Crear la màquina virtual](#1-crear-la-màquina-virtual)
5. [Instal·lar Ubuntu Server](#2-instal·lar-ubuntu-server)
6. [Fer les primeres comprovacions](#3-fer-les-primeres-comprovacions)
7. [Actualitzar el sistema](#4-actualitzar-el-sistema)
8. [Configurar el nom del servidor](#5-configurar-el-nom-del-servidor)
9. [Comprovar OpenSSH](#6-comprovar-openssh)
10. [Gestionar els permisos administratius](#7-gestionar-els-permisos-administratius)
11. [Configurar el teclat](#8-configurar-el-teclat)
12. [Configurar la data i l'hora](#9-configurar-la-data-i-lhora)
13. [Afegir una segona interfície](#10-afegir-una-segona-interfície)
14. [Configurar Netplan](#11-configurar-netplan)
15. [Validar la màquina base](#12-validar-la-màquina-base)
16. [Crear una instantània](#13-crear-una-instantània)
17. [Protocol de diagnosi](#protocol-general-de-diagnosi)
18. [Errors freqüents](#errors-freqüents)
19. [Estructura proposada del repositori](#estructura-proposada-del-repositori)

## Resultat final

En completar la guia tindrem:

- [ ] Ubuntu Server 24.04 LTS instal·lat sense entorn gràfic.
- [ ] 4 GB de RAM i 25 GB de disc virtual.
- [ ] Sistema actualitzat.
- [ ] Servidor identificat com a `srv-smx01`.
- [ ] Usuari ordinari amb permisos administratius mitjançant `sudo`.
- [ ] OpenSSH instal·lat i comprovat.
- [ ] Fus horari `Europe/Madrid`.
- [ ] Sincronització de l'hora activada.
- [ ] Una interfície NAT amb DHCP per a Internet.
- [ ] Una interfície de xarxa interna amb IP estàtica per al laboratori.
- [ ] Configuració persistent després de reiniciar.
- [ ] Instantània d'una base funcional abans d'instal·lar altres serveis.

La configuració de xarxa final proposada és:

| Adaptador | Mode a VirtualBox | Configuració a Ubuntu | Funció |
|---|---|---|---|
| Adaptador 1 | NAT | DHCP | Accés a Internet, actualitzacions i descàrrega de paquets |
| Adaptador 2 | Xarxa interna `SMX-LAB` | `192.168.50.10/24` | Comunicació amb clients i servidors del laboratori |

La guia original menciona mDNS a l'índex, però no en desenvolupa la configuració. Per tant, no s'instal·larà en aquesta preparació inicial.

## Convencions de la guia

Els valors següents s'utilitzen com a proposta comuna:

| Element | Valor proposat |
|---|---|
| Nom de la màquina a VirtualBox | `UbuntuServer24.04_BASE` |
| Nom intern del servidor | `srv-smx01` |
| Nom complet local | `srv-smx01.aula.test` |
| Nom de la xarxa interna | `SMX-LAB` |
| Xarxa interna del laboratori | `192.168.50.0/24` |
| IP del servidor a la xarxa interna | `192.168.50.10/24` |
| Fus horari | `Europe/Madrid` |

Cal distingir tres noms diferents:

- `UbuntuServer24.04_BASE` identifica la màquina dins de VirtualBox.
- `srv-smx01` és el nom intern o `hostname` d'Ubuntu.
- El nom de l'usuari identifica el compte amb què s'inicia sessió.

## Requisits previs

Abans de començar, cal disposar de:

- Oracle VirtualBox instal·lat.
- ISO d'Ubuntu Server 24.04 LTS Live Server compatible amb l'arquitectura de l'equip.
- Com a mínim 25 GB lliures al disc físic.
- Connexió a Internet.
- Virtualització activada a la BIOS o UEFI.
- Capacitat per assignar 4 GB de RAM a la màquina virtual sense deixar l'amfitrió sense recursos.

La ISO es troba a l'ordinador físic. VirtualBox la presenta a la màquina virtual com un suport òptic d'instal·lació.

---

## 1. Crear la màquina virtual

### 1.1 Crear una màquina nova

Obre VirtualBox i selecciona **Màquina > Nova**.

Configura els valors següents:

| Paràmetre | Valor |
|---|---|
| Nom | `UbuntuServer24.04_BASE` |
| Tipus | Linux |
| Versió | Ubuntu 64-bit |
| Memòria RAM | 4096 MB |
| Disc virtual | 25 GB |
| Tipus de disc | VDI |
| Reserva del disc | Dinàmica |
| Xarxa inicial | NAT |

> [!NOTE]
> La presentació original mostra un disc de 10 GB. Per preparar una base útil per a actualitzacions i pràctiques posteriors, la guia docent recomana 25 GB.

### 1.2 Evitar la instal·lació desatesa

Si VirtualBox ofereix una instal·lació desatesa, selecciona l'opció equivalent a **Ometre instal·lació desatesa**.

Això permet seguir manualment totes les pantalles de l'instal·lador i comprendre les decisions adoptades.

### 1.3 Revisar la configuració

Amb la màquina apagada, entra a **Configuració** i comprova:

- [ ] RAM configurada a 4096 MB.
- [ ] Disc virtual de 25 GB connectat.
- [ ] Adaptador 1 activat en mode NAT.
- [ ] Opció de cable connectat activada.
- [ ] ISO d'Ubuntu Server muntada a la unitat òptica virtual.

Encara no afegeixis la segona interfície. Primer instal·larem i comprovarem el sistema amb una única connexió NAT.

### Problemes habituals

- **No apareix cap dispositiu d'arrencada:** comprova que la ISO estigui muntada i revisa l'ordre d'arrencada.
- **No apareix cap disc durant la instal·lació:** verifica que el disc virtual existeixi i estigui connectat al controlador.
- **La VM no arrenca:** comprova l'arquitectura de la ISO i que la virtualització estigui activada.
- **L'ordinador va molt lent:** revisa la RAM disponible a l'amfitrió i tanca altres màquines virtuals.

---

## 2. Instal·lar Ubuntu Server

### 2.1 Arrencar l'instal·lador

Inicia la màquina virtual i selecciona:

```text
Try or Install Ubuntu Server
```

Encara no estem utilitzant el sistema definitiu. Hem arrencat l'entorn que instal·larà Ubuntu al disc virtual.

Si les tecles no responen:

1. Fes clic dins la finestra de VirtualBox.
2. Comprova que la finestra tingui el focus.
3. Utilitza la tecla d'amfitrió configurada a VirtualBox per alliberar el teclat quan calgui.

### 2.2 Seleccionar l'idioma

Tria l'idioma acordat per a la instal·lació.

Per navegar per l'assistent pots utilitzar:

- Fletxes de direcció.
- Tabulador.
- Barra espaiadora.
- Enter.

L'idioma dels menús i la distribució del teclat són configuracions independents.

### 2.3 Configurar el teclat

Selecciona la distribució corresponent al teclat físic. Habitualment:

```text
Layout: Spanish
Variant: Spanish
```

Comprova que pots escriure correctament símbols com:

```text
/ : @ - _
```

No facis aquesta prova escrivint una contrasenya real en un camp visible.

### 2.4 Escollir la modalitat d'instal·lació

Selecciona la instal·lació normal:

```text
Ubuntu Server
```

No seleccionis `Ubuntu Server (minimized)` per a aquesta màquina base. Una instal·lació reduïda és vàlida, però pot no incloure eines que utilitzarem per aprendre i diagnosticar.

### 2.5 Comprovar la xarxa durant la instal·lació

L'instal·lador mostrarà una interfície semblant a `enp0s3`. El nom pot ser diferent.

Com que VirtualBox està configurat en NAT, el seu servei DHCP proporcionarà automàticament:

- Adreça IP.
- Màscara.
- Passarel·la.
- Servidors DNS.

És habitual veure una IP semblant a:

```text
10.0.2.15/24
```

No la copiïs ni la configuris manualment. És només un exemple habitual del NAT de VirtualBox.

Abans de continuar, comprova que:

- [ ] Hi ha una interfície detectada.
- [ ] La interfície apareix connectada.
- [ ] Ha rebut una adreça IP.

### 2.6 Configurar el proxy

Deixa el camp del proxy buit, tret que la xarxa real on treballis proporcioni explícitament una adreça de proxy.

No hi introdueixis la passarel·la, el DNS ni la IP del router.

### 2.7 Seleccionar el servidor de paquets

Mantén el mirall oficial proposat per l'instal·lador, per exemple:

```text
es.archive.ubuntu.com
```

Espera que l'instal·lador comprovi que pot contactar-hi.

Si falla, revisa abans de canviar el mirall:

1. Adaptador activat a VirtualBox.
2. Mode NAT.
3. Cable virtual connectat.
4. Connexió de l'amfitrió.
5. Configuració DNS.

Disposar d'una IP no demostra que funcionin la ruta, el DNS i l'accés exterior.

### 2.8 Configurar l'emmagatzematge

Selecciona:

- Utilitzar el disc complet.
- El disc virtual de 25 GB.
- LVM desactivat per seguir la configuració senzilla del material.

Abans de confirmar, revisa:

- Nom del disc.
- Mida aproximada de 25 GB.
- Resum de particions.

> [!WARNING]
> La confirmació del particionament és un punt destructiu. En aquesta pràctica només s'ha de modificar el disc virtual creat expressament per a Ubuntu Server.

### 2.9 Crear el perfil

Omple els camps de perfil. La configuració ha d'incloure:

| Camp | Valor |
|---|---|
| Nom personal | El teu nom |
| Nom del servidor | `srv-smx01` |
| Nom d'usuari | Un compte identificable |
| Contrasenya | Una contrasenya segura i recordable |

No utilitzis la contrasenya feble que pugui aparèixer a les captures del material.

### 2.10 Ometre Ubuntu Pro

Selecciona l'opció d'ometre Ubuntu Pro.

No és necessari per instal·lar el sistema, actualitzar-lo ni completar les pràctiques del mòdul.

### 2.11 Instal·lar OpenSSH

Marca:

```text
Install OpenSSH server
```

No importis claus de GitHub o Launchpad en aquesta primera preparació, tret que vulguis treballar explícitament amb autenticació per claus.

### 2.12 No instal·lar serveis opcionals

No seleccionis serveis addicionals de la llista de snaps.

Volem mantenir una base comuna i instal·lar cada servei quan en treballem la funció, la configuració i la diagnosi.

### 2.13 Finalitzar i reiniciar

Espera que acabi la instal·lació i selecciona:

```text
Reboot Now
```

Quan ho demani:

1. Retira la ISO de la unitat virtual.
2. Prem Enter.
3. Espera que arrenqui el sistema instal·lat.

La instal·lació haurà acabat correctament quan arribis a la petició d'inici de sessió sense tornar a passar per l'assistent.

Si torna a aparèixer l'instal·lador, apaga la VM, desmunta la ISO i revisa l'ordre d'arrencada.

---

## 3. Fer les primeres comprovacions

### 3.1 Iniciar sessió

Introdueix el nom d'usuari i la contrasenya creats durant la instal·lació.

Quan escriguis la contrasenya no apareixeran lletres ni asteriscs. És el comportament normal del terminal.

Comprova l'usuari:

```bash
whoami
```

El resultat ha de ser el nom del compte amb què has iniciat sessió.

### 3.2 Consultar l'estat inicial

Executa les ordres per separat:

```bash
whoami
hostname
pwd
ip -br a
ip route
df -h
```

Aquestes ordres permeten identificar:

- L'usuari actiu.
- El nom del servidor.
- El directori actual.
- Les interfícies i les adreces IP.
- La ruta per defecte.
- L'espai ocupat i disponible.

No és necessari que totes les dades coincideixin amb les captures. Cal interpretar si corresponen a la configuració real de la màquina.

---

## 4. Actualitzar el sistema

### 4.1 Actualitzar el catàleg de paquets

```bash
sudo apt update
```

Aquesta ordre actualitza la informació dels paquets disponibles, però no instal·la per si sola totes les actualitzacions.

### 4.2 Instal·lar les actualitzacions

```bash
sudo apt upgrade
```

Llegeix el resum i confirma l'operació quan ho demani.

La presentació mostra una versió combinada:

```bash
sudo apt update && sudo apt upgrade -y
```

En aquesta primera execució és preferible separar les ordres:

- `&&` executa la segona ordre només si la primera finalitza correctament.
- `-y` accepta automàticament les confirmacions.

### 4.3 Reiniciar després de les actualitzacions

```bash
sudo reboot
```

Després del reinici, torna a iniciar sessió i comprova:

```bash
whoami
hostname
ip -br a
```

### Errors habituals d'APT

- **Error de resolució o descàrrega:** comprova la xarxa i el DNS abans de repetir l'ordre.
- **Bloqueig d'APT:** espera si hi ha un altre gestor o una actualització automàtica treballant. No esborris fitxers de bloqueig a cegues.
- **Disc ple:** consulta `df -h` i identifica quin sistema de fitxers està afectat.
- **Configuració interrompuda:** si no hi ha cap altre gestor actiu i el diagnòstic ho indica, executa `sudo dpkg --configure -a`.

---

## 5. Configurar el nom del servidor

### 5.1 Establir el hostname

```bash
sudo hostnamectl set-hostname srv-smx01
```

### 5.2 Configurar la resolució local

Obre el fitxer:

```bash
sudo nano /etc/hosts
```

Conserva l'entrada de `localhost`:

```text
127.0.0.1 localhost
```

Afegeix o adapta l'entrada del servidor:

```text
127.0.1.1 srv-smx01.aula.test srv-smx01
```

No eliminis les entrades necessàries d'IPv6.

Per desar amb Nano:

```text
Ctrl + O
Enter
Ctrl + X
```

### 5.3 Comprovar el resultat

Obre una sessió nova o torna a iniciar sessió. Després executa:

```bash
hostname
hostname -f
```

Resultat esperat:

```text
srv-smx01
srv-smx01.aula.test
```

Editar `/etc/hosts` només crea una associació local al servidor. No configura el DNS del centre ni permet automàticament que altres equips resolguin aquest nom.

---

## 6. Comprovar OpenSSH

Consulta el servei i el socket:

```bash
systemctl status ssh.service ssh.socket --no-pager
```

Consulta els ports TCP en escolta:

```bash
sudo ss -ltnp
```

Hauries de trobar el port TCP 22 associat a SSH.

Ubuntu 24.04 pot activar SSH mitjançant un socket. Per això, veure únicament `ssh.service` inactiu no és suficient per concloure que SSH no funciona. Cal revisar també `ssh.socket` i els ports en escolta.

Amb NAT individual, una connexió entrant des de fora de la VM pot requerir reenviament de ports. La segona interfície interna que configurarem permetrà comunicar el servidor amb altres VM del laboratori.

### Interpretació d'errors SSH

- **Temps d'espera esgotat:** comprova IP, ruta, adaptadors i possibles filtres.
- **Connexió refusada:** comprova que hi hagi un servei escoltant al destí i port previstos.
- **Error d'autenticació:** revisa l'usuari, la contrasenya i els mètodes d'autenticació permesos.

---

## 7. Gestionar els permisos administratius

### 7.1 Comprovar sudo

```bash
whoami
sudo whoami
```

La segona ordre ha de retornar:

```text
root
```

La contrasenya que demana `sudo` és habitualment la del compte que executa l'ordre.

No és necessari habilitar una contrasenya directa per a root.

Si necessites temporalment una shell administrativa:

```bash
sudo -i
```

Per sortir-ne:

```bash
exit
```

### 7.2 Crear un segon administrador opcional

Crea el compte:

```bash
sudo adduser usuari2
```

Afegeix-lo al grup `sudo`:

```bash
sudo usermod -aG sudo usuari2
```

Comprova els grups:

```bash
id usuari2
```

El resultat ha d'incloure `sudo`.

Inicia una sessió nova amb `usuari2` i comprova:

```bash
sudo whoami
```

> [!WARNING]
> Utilitza `-aG`. Fer servir `-G` sense `-a` pot substituir els altres grups suplementaris de l'usuari.

---

## 8. Configurar el teclat

Si la distribució de la consola és incorrecta:

```bash
sudo dpkg-reconfigure keyboard-configuration
```

Selecciona el model, la distribució i la variant corresponents a l'equip.

Comprova caràcters habituals a les ordres:

```text
/ - _ : @
```

Si l'error només apareix durant una connexió SSH, revisa també el teclat i el terminal de l'equip client. Canviar el teclat de consola del servidor no corregeix necessàriament un problema originat al client.

---

## 9. Configurar la data i l'hora

### 9.1 Consultar l'estat

```bash
timedatectl
```

Interpreta especialment:

- `Local time`
- `Universal time`
- `Time zone`
- `System clock synchronized`
- `NTP service`

Veure UTC no significa automàticament que el rellotge sigui incorrecte.

### 9.2 Configurar el fus horari

```bash
sudo timedatectl set-timezone Europe/Madrid
timedatectl
```

Ha d'aparèixer:

```text
Time zone: Europe/Madrid
```

No ajustis manualment una hora més o menys per compensar l'horari d'estiu. La zona `Europe/Madrid` ja incorpora les regles estacionals.

### 9.3 Activar la sincronització

```bash
sudo timedatectl set-ntp true
timedatectl
```

Si el sistema utilitza `systemd-timesyncd`, amplia la comprovació amb:

```bash
systemctl status systemd-timesyncd --no-pager
timedatectl timesync-status
journalctl -u systemd-timesyncd -b --no-pager -n 30
```

Activar NTP no demostra que la sincronització sigui immediata. Cal verificar l'estat final.

---

## 10. Afegir una segona interfície

La segona interfície separarà la connexió exterior de la xarxa de pràctiques.

### 10.1 Apagar correctament el servidor

```bash
sudo poweroff
```

### 10.2 Configurar VirtualBox

Amb la VM apagada:

1. Entra a **Configuració > Xarxa**.
2. Mantén l'Adaptador 1 en NAT.
3. Activa l'Adaptador 2.
4. Selecciona **Xarxa interna**.
5. Escriu com a nom de xarxa `SMX-LAB`.
6. Confirma que el cable virtual estigui connectat.
7. Torna a iniciar la màquina.

Totes les VM que s'hagin de comunicar dins del laboratori han d'utilitzar exactament el mateix nom de xarxa interna.

### 10.3 Identificar les interfícies

```bash
ip -br link
ip -br a
```

És habitual trobar noms com `enp0s3` i `enp0s8`, però poden ser diferents.

Si tens dubtes, compara les adreces MAC mostrades per Ubuntu amb les configurades a VirtualBox.

Tenir dues interfícies no converteix automàticament Ubuntu en un encaminador i tampoc activa NAT dins del servidor.

---

## 11. Configurar Netplan

### 11.1 Identificar el fitxer existent

```bash
ls -l /etc/netplan
sudo netplan get
```

El fitxer pot tenir noms com:

```text
00-installer-config.yaml
50-cloud-init.yaml
```

No obris amb Nano un nom copiat sense haver comprovat que existeix. Si el nom no existeix, podries crear un YAML buit i afegir una configuració conflictiva.

Netplan pot combinar diversos fitxers YAML. Cal inspeccionar-los si la configuració aplicada no coincideix amb el fitxer editat.

### 11.2 Fer una còpia de seguretat

```bash
sudo cp -a /etc/netplan /root/netplan-abans-canvi
```

Comprova els fitxers i permisos:

```bash
ls -l /etc/netplan
```

Habitualment, els fitxers de configuració han de pertànyer a root i tenir permisos restrictius, com ara `600`.

### 11.3 Editar el fitxer real

Substitueix el nom de l'exemple pel fitxer que existeixi a la teva màquina:

```bash
sudo nano /etc/netplan/00-installer-config.yaml
```

Exemple de configuració:

```yaml
network:
  version: 2
  ethernets:
    enp0s3:
      dhcp4: true
    enp0s8:
      dhcp4: false
      addresses:
        - 192.168.50.10/24
```

Adapta `enp0s3` i `enp0s8` als noms reals.

Aquesta configuració estableix:

- Primera interfície per DHCP mitjançant NAT.
- Segona interfície amb IP estàtica `192.168.50.10/24`.
- Una única ruta de sortida, proporcionada pel NAT.
- Cap passarel·la fictícia a la xarxa interna.

No afegeixis una ruta per defecte a la xarxa interna si només ha de comunicar equips del mateix segment.

Utilitza espais i no tabuladors. La indentació forma part de la sintaxi YAML.

> [!NOTE]
> Abans d'utilitzar `192.168.50.0/24`, comprova que no se superposi amb una altra xarxa del teu entorn.

### 11.4 Validar la sintaxi

```bash
sudo netplan generate
```

Si no mostra errors, Netplan pot interpretar la sintaxi. Això encara no demostra que les IP, interfícies, rutes o DNS siguin adequats.

Si hi ha un error amb número de línia, revisa:

- La línia indicada i l'anterior.
- Els dos punts.
- La indentació.
- El nom exacte de les propietats.
- L'absència de tabuladors.

### 11.5 Provar la configuració

Des de la consola de VirtualBox:

```bash
sudo netplan try
```

Confirma dins del termini només si la configuració funciona.

Si treballes directament des de la consola i tens la còpia disponible, també pots aplicar:

```bash
sudo netplan apply
```

Mantén disponible la consola de VirtualBox. Un canvi incorrecte pot interrompre una sessió SSH.

### 11.6 Comprovar les adreces

```bash
ip -br a
```

Hauries de veure:

- Una IP automàtica a la interfície NAT.
- `192.168.50.10/24` a la interfície interna.

### 11.7 Comprovar les rutes

```bash
ip route
```

La ruta per defecte ha de correspondre a la interfície NAT. En aquesta base simplifiquem la configuració a una única sortida principal.

### 11.8 Comprovar el DNS

```bash
resolvectl status
getent hosts ubuntu.com
```

### 11.9 Fer proves de connectivitat

Prova connectivitat per IP:

```bash
ping -c 4 1.1.1.1
```

Prova resolució de noms:

```bash
ping -c 4 ubuntu.com
```

Un ping fallit no demostra per si sol que un servei sigui inaccessible, perquè ICMP pot estar filtrat. Cal provar també el servei concret que es necessita.

### Errors habituals de Netplan

- **S'obre un fitxer buit:** probablement has escrit un nom que no existia.
- **No afecta cap interfície:** comprova els noms amb `ip -br link`.
- **Es manté una IP automàtica inesperada:** revisa `dhcp4` i la resta de YAML.
- **Es perd SSH:** entra per la consola de VirtualBox, revisa el YAML i restaura la còpia correcta.
- **Restaures una còpia però el problema continua:** comprova si han quedat altres YAML que entren en conflicte.
- **Avís de permisos:** revisa propietari i permisos restrictius del fitxer.
- **No hi ha sortida exterior:** revisa `ip route` i comprova que la ruta per defecte sigui la del NAT.
- **Arriba per IP però no per nom:** revisa `resolvectl status` i la resolució DNS.

---

## 12. Validar la màquina base

Una instal·lació no es considera acabada simplement perquè arribi a la pantalla d'inici de sessió. Cal demostrar que la configuració funciona i persisteix.

### 12.1 Identitat i permisos

```bash
whoami
sudo whoami
```

### 12.2 Nom del servidor

```bash
hostname
hostname -f
```

Resultat esperat:

```text
srv-smx01
srv-smx01.aula.test
```

### 12.3 Interfícies i adreces

```bash
ip -br link
ip -br a
```

### 12.4 Rutes i DNS

```bash
ip route
resolvectl status
getent hosts ubuntu.com
```

### 12.5 OpenSSH

```bash
systemctl status ssh.service ssh.socket --no-pager
sudo ss -ltnp
```

### 12.6 Espai de disc

```bash
df -h
```

### 12.7 Fus i sincronització

```bash
timedatectl
```

### 12.8 Persistència

Reinicia:

```bash
sudo reboot
```

Després del reinici, repeteix:

```bash
hostname
hostname -f
ip -br a
ip route
resolvectl status
timedatectl
sudo ss -ltnp
```

La base només es dona per acabada si les configuracions pertinents es conserven després del reinici.

### Llista final de validació

- [ ] `whoami` identifica l'usuari correcte.
- [ ] `sudo whoami` retorna `root`.
- [ ] `hostname` retorna `srv-smx01`.
- [ ] `hostname -f` retorna `srv-smx01.aula.test`.
- [ ] La interfície NAT obté una IP per DHCP.
- [ ] La interfície interna conserva `192.168.50.10/24`.
- [ ] Només hi ha una ruta per defecte per a aquesta configuració base.
- [ ] La resolució de noms funciona.
- [ ] SSH escolta al port previst.
- [ ] El fus horari és `Europe/Madrid`.
- [ ] NTP està activat i se n'ha comprovat l'estat.
- [ ] Les dades continuen sent correctes després de reiniciar.

---

## 13. Crear una instantània

### 13.1 Fer una última actualització

```bash
sudo apt update
sudo apt upgrade
```

### 13.2 Apagar correctament

```bash
sudo poweroff
```

### 13.3 Crear la instantània a VirtualBox

Nom recomanat:

```text
00_BASE_UBUNTU_SERVER_24_04
```

Descripció recomanada:

```text
Ubuntu Server 24.04 LTS actualitzat.
Hostname srv-smx01.
OpenSSH instal·lat.
Adaptador 1 NAT amb DHCP.
Adaptador 2 SMX-LAB amb IP 192.168.50.10/24.
Zona horària Europe/Madrid i NTP actiu.
```

Una instantània facilita tornar a un estat anterior, però no substitueix una còpia independent perquè depèn dels fitxers de la màquina virtual.

Si es clona la base per desplegar diverses màquines en una mateixa pràctica, cal revisar els elements que han de ser únics:

- Nom del servidor.
- Adreça MAC.
- IP estàtica.
- Identificadors o credencials específics de la màquina.

---

## Protocol general de diagnosi

Quan alguna cosa no funcioni, evita modificar diversos elements alhora. Primer concreta el problema, formula una hipòtesi i fes una prova que no alteri la configuració.

### 1. Definir l'objectiu

- Què intentaves fer?
- Des de quin equip?
- A quin destí?
- Quin resultat esperaves?
- Quin missatge exacte has obtingut?
- Quin ha estat l'últim canvi?

### 2. Revisar VirtualBox

Comprova:

- Mode de xarxa.
- Adaptador activat.
- Cable virtual connectat.
- Nom de la xarxa interna.
- Adaptador físic seleccionat si s'utilitza mode pont.

### 3. Revisar l'enllaç i les adreces

```bash
ip -br link
ip -br a
```

Identifica:

- Quina interfície correspon a cada adaptador.
- Si està activa.
- Si té una IP adequada per a la xarxa connectada.

### 4. Revisar les rutes

```bash
ip route
```

Determina si el destí és local o necessita una passarel·la.

### 5. Revisar la resolució

```bash
resolvectl status
getent hosts ubuntu.com
```

Si es pot arribar a una IP però no a un nom, el problema probablement es troba en la resolució.

### 6. Revisar el servei

```bash
systemctl status NOM_SERVEI --no-pager
```

### 7. Revisar els ports

```bash
sudo ss -ltnp
```

### 8. Revisar els registres

```bash
journalctl -u NOM_SERVEI -b --no-pager -n 50
```

### 9. Documentar la resolució

Registra:

1. Símptoma observat.
2. Configuració inicial.
3. Hipòtesi plantejada.
4. Prova realitzada.
5. Resultat obtingut.
6. Solució aplicada.
7. Comprovació final.

---

## Errors freqüents

### El sistema torna a mostrar l'instal·lador

La ISO encara està muntada o té prioritat en l'ordre d'arrencada. Desmunta-la i arrenca des del disc virtual.

### No puc iniciar sessió

Comprova:

- Nom d'usuari real, no el nom complet ni el nom de la VM.
- Distribució del teclat.
- Bloq Maj.
- Símbols de la contrasenya.

### `sudo` no pot resoldre el nom del servidor

Revisa la coherència entre:

```bash
hostname
```

i:

```bash
cat /etc/hosts
```

### La interfície interna no rep cap IP

Una xarxa interna no proporciona DHCP automàticament. Configura una IP estàtica o incorpora un servidor DHCP a la xarxa.

### Dues VM amb NAT mostren la mateixa IP

En NAT individual poden tenir la mateixa IP virtual sense conflicte perquè es troben en entorns NAT separats.

### Les VM amb NAT no es veuen entre elles

El NAT individual no crea automàticament una xarxa comuna. Utilitza una mateixa xarxa NAT o una mateixa xarxa interna segons l'objectiu.

### Netplan no aplica el fitxer modificat

Comprova:

```bash
ls -l /etc/netplan
sudo netplan get
```

Pot haver-hi diversos YAML combinats o potser s'ha editat un fitxer que no era l'actiu.

### Hi ha Internet per IP però no per nom

Revisa:

```bash
resolvectl status
getent hosts ubuntu.com
```

### SSH no respon

Comprova per ordre:

```bash
ip -br a
ip route
systemctl status ssh.service ssh.socket --no-pager
sudo ss -ltnp
```

### L'hora és incorrecta

No canviïs el rellotge manualment abans de distingir entre:

- Fus horari incorrecte.
- NTP actiu però encara no sincronitzat.
- Problema de xarxa o DNS.
- Canvi produït després de pausar o reprendre la VM.

---

## Estructura proposada del repositori

El repositori es pot ampliar a mesura que avancin les pràctiques:

```text
ubuntu-server-smx/
├── README.md
├── docs/
│   ├── 01-installacio/
│   ├── 02-xarxa-base/
│   ├── 03-dhcp/
│   ├── 04-dns/
│   ├── 05-ssh/
│   ├── 06-transferencia-fitxers/
│   ├── 07-servidor-web/
│   └── 08-correu/
├── configuracions/
│   └── netplan/
├── scripts/
└── evidencies/
```

No publiquis al repositori:

- Contrasenyes.
- Claus privades SSH.
- Tokens.
- Còpies de fitxers que continguin credencials.
- Adreces o dades sensibles de la xarxa real del centre.

## Fonts tècniques de suport

- [Ubuntu Server documentation](https://ubuntu.com/server/docs)
- [Ubuntu Server installation requirements](https://ubuntu.com/server/docs/reference/installation/system-requirements/)
- [Ubuntu Server basic installation](https://ubuntu.com/server/docs/tutorial/basic-installation/)
- [Subiquity screen by screen](https://canonical-subiquity.readthedocs-hosted.com/en/latest/tutorial/screen-by-screen.html)
- [Oracle VirtualBox networking](https://docs.oracle.com/en/virtualization/virtualbox/7.1/user/networkingdetails.html)
- [Ubuntu network configuration](https://ubuntu.com/server/docs/explanation/networking/configuring-networks/)
- [Netplan YAML](https://netplan.readthedocs.io/en/stable/netplan-yaml/)
- [Netplan try](https://netplan.readthedocs.io/en/stable/netplan-try/)
- [Ubuntu OpenSSH](https://ubuntu.com/server/docs/how-to/security/openssh-server/)
- [Ubuntu user management](https://ubuntu.com/server/docs/how-to/security/user-management/)

## Autoria i ús docent

Aquesta guia reorganitza el procediment de la presentació d'instal·lació i configuració bàsica d'Ubuntu Server 24.04 LTS elaborada per Carlos Alonso Martínez, i incorpora els aclariments tècnics i didàctics de la guia docent complementària.

En qualsevol adaptació o lliurament cal conservar la referència a l'autoria i la llicència del material original, i diferenciar les ampliacions pròpies de les instruccions de partida.
