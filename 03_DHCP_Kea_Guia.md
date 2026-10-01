# Configuració de DHCP amb Kea a Ubuntu Server

> **MP 0227 · Serveis de xarxa · 2n SMX · RA1**

Guia d'estudi i consulta per entendre i configurar un servidor DHCPv4 amb Kea a Ubuntu Server 24.04 LTS. Desenvolupa la primera part de la presentació **UD02_AA2_DHCP_LinuxAmbKea.pdf**, pàgines 1–28 (portada i diapositives 1–27).

Partim del servidor preparat a la guia d'Ubuntu i de la teoria de DHCP. Ara relacionarem els conceptes —interfície, subxarxa, pool, opcions, concessió i reserva— amb els fitxers i les comprovacions del servei.

L'activitat que cal executar i documentar és en un document independent: [Activitat guiada amb Kea](04_DHCP_Kea_Activitat.md). Els valors de demostració d'aquesta guia no substitueixen els de l'activitat.

## Ruta de treball

| Fase | Apartats | Què aconseguiràs? |
|---|---|---|
| **[Fase 1. Preparar l'entorn](#fase-1)** | 1–2 | Distingir Netplan de Kea i identificar les dues interfícies. |
| **[Fase 2. Instal·lar i administrar](#fase-2)** | 3–4 | Identificar paquets, serveis, fitxers i estats. |
| **[Fase 3. Configurar DHCPv4](#fase-3)** | 5–8 | Entendre el JSON i construir un àmbit amb opcions i concessions. |
| **[Fase 4. Comprovar i reservar](#fase-4)** | 9–11 | Validar el servei, observar el client i assignar una reserva. |
| **[Fase 5. Consolidar](#fase-5)** | 12–13 | Diagnosticar errors i justificar les decisions. |

> [!TIP]
> La primera vegada, segueix els apartats en ordre. Si reprens la feina, consulta l’**objectiu** i el **resultat esperat** de cada apartat per saber des d’on continuar.

## Índex

- **Preparació:** [Objectius i resultats esperats](#objectius-i-resultats-esperats) · [Convencions](#convencions-de-la-guia) · [Requisits previs](#requisits-previs)
- **[Fase 1 — Preparar l'entorn](#fase-1):** [1. Què canvia respecte de la sessió anterior](#1-què-canvia-respecte-de-la-sessió-anterior) · [2. Preparar les interfícies](#2-preparar-les-interfícies)
- **[Fase 2 — Instal·lar i administrar](#fase-2):** [3. Instal·lar Kea](#3-installar-kea) · [4. Administrar els serveis](#4-administrar-els-serveis)
- **[Fase 3 — Configurar DHCPv4](#fase-3):** [5. Entendre el fitxer de configuració](#5-entendre-el-fitxer-de-configuració) · [6. Exemple complet de demostració](#6-exemple-complet-de-demostració) · [7. Temps de concessió i càlculs](#7-temps-de-concessió-i-càlculs) · [8. Concessions persistents](#8-concessions-persistents)
- **[Fase 4 — Comprovar i reservar](#fase-4):** [9. Validar i aplicar](#9-validar-i-aplicar) · [10. Comprovar el client](#10-comprovar-el-client) · [11. Afegir una reserva](#11-afegir-una-reserva)
- **[Fase 5 — Consolidar](#fase-5):** [12. Diagnosticar amb evidències](#12-diagnosticar-amb-evidències) · [13. Autoavaluació](#13-autoavaluació)
- **Consulta i ajuda:** [Fonts i correspondència amb el PDF](#fonts-i-correspondència-amb-el-pdf)

---

## Preparació

### Objectius i resultats esperats

En acabar hauràs de poder explicar quina interfície atén Kea, què distribueix el servei, com es desa una concessió i com demostres que un client ha rebut la configuració esperada.

### Convencions de la guia

> [!IMPORTANT]
> El PDF mostra adreces `192.169...`, que no pertanyen als blocs privats RFC 1918. Aquesta guia utilitza **192.168...** per al laboratori. És una correcció explícita d'adreçament; manté les funcions i el procediment de la presentació. Abans d'aplicar qualsevol exemple, comprova que el prefix no se superposi amb una altra xarxa del teu equip.

Els blocs de configuració són exemples complets quan així s'indica. Els fragments parcials s'han d'integrar al lloc especificat, no enganxar-se al final del fitxer.

### Requisits previs

- Disposar de la base funcional de la [guia d'Ubuntu Server](00_UbuntuServer_Guide.md).
- Haver treballat els conceptes de la [introducció al servei DHCP](02_Teoria_DHCP_Guide.md).

---

<a id="fase-1"></a>

## Fase 1. Preparar l'entorn

Distingeix la configuració de la màquina del servei que oferirà als clients.

### 1. Què canvia respecte de la sessió anterior

> **Objectiu:** separar la configuració de la màquina de la configuració que aquesta ofereix.
>
> **Resultat esperat:** pots explicar per què `dhcp4: true` no posa en marxa un servidor DHCP.

| Eina o component | Què configura | Fitxer o consulta |
|---|---|---|
| VirtualBox | A quina xarxa està connectat cada adaptador | Configuració de la VM |
| Netplan | Les interfícies del mateix Ubuntu Server | `/etc/netplan/*.yaml` |
| Kea DHCPv4 | Les dades que rebran els clients | `/etc/kea/kea-dhcp4.conf` |
| NetworkManager a Zorin | La connexió del client | Interfície gràfica o `nmcli` |

A la interfície NAT, Ubuntu pot ser **client DHCP** de VirtualBox. A la interfície interna, el mateix Ubuntu pot oferir **DHCP als altres equips mitjançant Kea**. Són funcions diferents, sobre interfícies diferents.

**Recorda:** DHCP comunica la IP d'un DNS i d'una passarel·la; no crea aquests serveis. Instal·lar Kea no activa encaminament ni NAT dins d'Ubuntu.

**Pregunta de control:** si el servidor obté `10.0.2.15` automàticament, ja pot repartir adreces al client Zorin? No. Cal configurar i iniciar el servei DHCP a la xarxa interna.

### 2. Preparar les interfícies

> **Objectiu:** conservar la sortida NAT i separar la xarxa de pràctiques.
>
> **Resultat esperat:** saps relacionar adaptador, MAC, interfície i IP.

La presentació comença amb NAT i afegeix una segona interfície interna. La nostra base ja les té: **no afegeixis un tercer adaptador per repetir un pas completat**.

| Adaptador del servidor | Mode | Configuració | Funció |
|---|---|---|---|
| 1 | NAT | DHCP | Instal·lar paquets i actualitzar |
| 2 | Xarxa interna `SMX-LAB` | IP estàtica | Atendre els clients DHCP del laboratori |

Comprova les MAC a VirtualBox i compara-les amb:

```bash
ip -br link
ip -4 -br addr
ip route
```

En els exemples, `enp0s3` és NAT i `enp0s8` és interna. **Substitueix-los si els teus noms són diferents.**

Per a una demostració que conserva la base anterior:

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:
      dhcp4: true
    enp0s8:
      dhcp4: false
      addresses:
        - 192.168.50.10/24
```

La interfície interna no declara passarel·la ni DNS: en aquest servidor la sortida exterior continua per NAT. La configuració que Kea anunciarà als clients és una decisió separada.

Abans d'editar, localitza el YAML real amb `ls -l /etc/netplan` i consulta `sudo netplan get`. Fes-ne una còpia fora de `/etc/netplan`, utilitza un nom nou per a cada còpia i treballa des de la consola de VirtualBox.

```bash
sudo netplan generate
sudo netplan try
ip -4 -br addr
ip route
```

Confirma `try` només després de comprovar el resultat. La reversió no substitueix la còpia ni la consola de recuperació.

<!-- IMATGE 01: topologia amb Ubuntu Server, NAT i SMX-LAB; etiqueta MAC, interfície i funció. Zorin és client de la xarxa interna. Fitxer suggerit: source/03_DHCP_Kea/01-topologia.png -->

**Errors freqüents:** editar un YAML inexistent; copiar `enp0s8` sense identificar-lo; donar una passarel·la inventada a la interfície interna; usar noms de xarxa interna diferents.

---

<a id="fase-2"></a>

## Fase 2. Instal·lar i administrar

Instal·la Kea i identifica els components que utilitzaràs al laboratori.

### 3. Instal·lar Kea

> **Objectiu:** instal·lar el programari sobre la base que ja funciona.
>
> **Resultat esperat:** pots consultar la versió i les unitats instal·lades.

Al servidor, amb NAT operatiu:

```bash
sudo apt update
sudo apt upgrade
sudo apt install kea
kea-dhcp4 -v
systemctl list-unit-files 'kea*'
```

`apt update` actualitza el catàleg; `apt upgrade` actualitza paquets. En aquesta primera execució els separem per poder interpretar el resultat. La presentació combina ordres amb `&&` i `-y`; `&&` condiciona la segona a l'èxit de la primera, i `-y` accepta confirmacions automàticament.

Kea és la implementació de DHCP que treballarem. No barregis aquesta configuració amb tutorials d'`isc-dhcp-server`: tenen fitxers i sintaxi diferents.

#### L'agent de control

La instal·lació del conjunt `kea` pot preguntar com configurar l'autenticació de `kea-ctrl-agent`. Seguint el material, selecciona la generació d'una contrasenya aleatòria si apareix l'assistent.

```bash
sudo dpkg-reconfigure kea-ctrl-agent
```

Aquesta ordre permet recuperar l'assistent si el paquet està instal·lat. La contrasenya de l'API no és la del teu usuari, ni una contrasenya que necessitin els clients per obtenir DHCP. Aquí administrarem Kea amb fitxers i `systemctl`; no necessitem publicar l'API.

**Si falla la instal·lació:** llegeix l'error. Resolució de noms, manca de disc i un altre procés APT actiu són problemes diferents. No eliminis fitxers de bloqueig sense diagnosticar-los.

### 4. Administrar els serveis

> **Objectiu:** entendre que Kea agrupa components independents.
>
> **Resultat esperat:** pots deixar DHCPv4 actiu i els serveis no utilitzats deshabilitats.

| Unitat de systemd habitual a Ubuntu | Fitxer | Funció |
|---|---|---|
| `kea-dhcp4-server` | `/etc/kea/kea-dhcp4.conf` | DHCP per a IPv4 |
| `kea-dhcp6-server` | `/etc/kea/kea-dhcp6.conf` | DHCP per a IPv6 |
| `kea-dhcp-ddns-server` | `/etc/kea/kea-dhcp-ddns.conf` | Actualitzacions dinàmiques de DNS |
| `kea-ctrl-agent` | `/etc/kea/kea-ctrl-agent.conf` | API de control |

El procés DDNS s'anomena `kea-dhcp-ddns`, però la unitat d'Ubuntu acostuma a acabar en **`-server`**. Confirma els noms amb `systemctl list-unit-files 'kea*'` si apareix `Unit not found`.

Per a aquest laboratori, després de comprovar que són les unitats instal·lades:

```bash
sudo systemctl disable --now kea-dhcp6-server
sudo systemctl disable --now kea-dhcp-ddns-server
sudo systemctl disable --now kea-ctrl-agent
```

Desactivar DHCPv6 de Kea **no desactiva IPv6 de tot Ubuntu**. Desactivar DDNS tampoc impedeix anunciar un DNS amb l'opció `domain-name-servers`.

| Acció | Significat |
|---|---|
| `start` / `stop` | Iniciar / aturar ara |
| `enable` / `disable` | Habilitar / deshabilitar l'arrencada automàtica |
| `disable --now` | Deshabilitar i aturar ara |
| `restart` | Aturar i iniciar, carregant la configuració |
| `status` | Consultar l'estat i missatges recents |

`active` i `enabled` no són sinònims. Un servei pot estar funcionant però no arrencar automàticament després d'un reinici.

---

<a id="fase-3"></a>

## Fase 3. Configurar DHCPv4

Relaciona el fitxer de configuració amb la subxarxa, les opcions i les concessions.

### 5. Entendre el fitxer de configuració

> **Objectiu:** reconèixer l'estructura abans d'editar-la.
>
> **Resultat esperat:** identifiques objectes, llistes, propietats i valors.

Kea llegeix `/etc/kea/kea-dhcp4.conf`. Conserva una còpia abans de substituir-ne el contingut:

```bash
sudo cp -a /etc/kea/kea-dhcp4.conf /etc/kea/kea-dhcp4.conf.abans-laboratori
sudo nano /etc/kea/kea-dhcp4.conf
```

Tria un altre nom si la còpia ja existeix. Copiar manté l'original al seu lloc; moure'l, com fa el PDF, el retira fins que es crea el fitxer nou.

#### JSON i comentaris

- `{ }` delimita un **objecte**, amb propietats i valors.
- `[ ]` delimita una **llista**, que pot contenir objectes o altres valors.
- `:` separa una propietat del seu valor.
- `,` separa elements consecutius; els exemples d'aquesta guia no posen coma després de l'últim.
- Les cadenes utilitzen cometes dobles; els nombres i `true`/`false`, no.

Kea admet extensions de comentaris, com `//` i `#`, en els seus fitxers. Això no converteix els comentaris en JSON estàndard. Els exemples complets d'aquesta guia utilitzen JSON estricte perquè sigui més fàcil veure'n l'estructura; la validació específica s'ha de fer amb **`kea-dhcp4 -t`**.

```json
{
  "interfaces-config": {
    "interfaces": ["enp0s8"]
  }
}
```

Aquest és només un fragment explicatiu: `interfaces-config` és un objecte i `interfaces` és una llista. No tots els «subapartats» van entre claudàtors.

**Connexió amb Netplan:** YAML dona importància estructural a la indentació; en JSON, claus, claudàtors, cometes i comes defineixen l'estructura. Indentar bé continua ajudant a llegir-lo.

### 6. Exemple complet de demostració

> **Objectiu:** relacionar cada concepte DHCP amb una clau del fitxer.
>
> **Resultat esperat:** pots explicar el pool, les opcions i la interfície sense memoritzar el bloc.

Aquest exemple conserva el servidor de la base a `192.168.50.10/24`. Utilitza un **pool `.100–.149`**, diferent del de l'activitat. El servidor només atén `enp0s8`.

```json
{
  "Dhcp4": {
    "interfaces-config": {
      "interfaces": ["enp0s8"]
    },
    "valid-lifetime": 4000,
    "renew-timer": 1000,
    "rebind-timer": 2000,
    "lease-database": {
      "type": "memfile",
      "persist": true,
      "name": "/var/lib/kea/kea-leases4.csv"
    },
    "subnet4": [
      {
        "id": 1,
        "subnet": "192.168.50.0/24",
        "pools": [
          { "pool": "192.168.50.100 - 192.168.50.149" }
        ],
        "option-data": [
          { "name": "routers", "data": "192.168.50.254" },
          { "name": "domain-name-servers", "data": "8.8.8.8" }
        ]
      }
    ]
  }
}
```

| Element | Què significa |
|---|---|
| `Dhcp4` | Configuració del servidor DHCPv4 |
| `interfaces-config` | Interfícies per les quals escolta |
| `subnet4` | Llista de subxarxes ateses |
| `id` | Identificador estable d'aquesta subxarxa dins de Kea |
| `subnet` | Xarxa i prefix; no és la IP del servidor |
| `pools` | Intervals que es poden assignar dinàmicament |
| `option-data` | Opcions que s'envien als clients |
| `routers` | Passarel·la anunciada al client |
| `domain-name-servers` | Servidors DNS anunciats |

La subxarxa conté 256 adreces, habitualment 254 hosts; el pool té `149 − 100 + 1 = 50` adreces. El servidor `.10` queda fora del pool. No restem dues adreces al pool perquè xarxa i broadcast ja en són fora.

> [!IMPORTANT]
> La passarel·la `.254` és una **opció anunciada**. Si no existeix un encaminador a aquella IP, el client rebrà l'opció però no tindrà sortida exterior per aquell camí. Això tampoc fa accessible `8.8.8.8`. En aquest exemple podem demostrar l'assignació DHCP sense haver desplegat encara encaminament.

**Comparació amb el PDF:** l'exemple inicial hi mostra `.10–.199` i després l'exemple de reserva utilitza `.100–.199`. No són el mateix interval. Aquí s'utilitza un únic pool coherent durant tota la demostració.

<!-- IMATGE 02: JSON amb fletxes que relacionen interfície, subxarxa, pool i opcions amb la topologia. Fitxer suggerit: source/03_DHCP_Kea/02-json-explicat.png -->

### 7. Temps de concessió i càlculs

> **Objectiu:** interpretar els temporitzadors com a moments del cicle DHCP.
>
> **Resultat esperat:** no confons T2 amb el venciment.

| Clau | Valor de l'exemple | Significat |
|---|---:|---|
| `renew-timer` | 1000 s | T1: començar a intentar renovar amb el servidor original |
| `rebind-timer` | 2000 s | T2: intentar renovar amb qualsevol servidor adequat mitjançant broadcast |
| `valid-lifetime` | 4000 s | Durada de la concessió; sense renovació, després expira |

La relació d'aquest exemple és `0 < 1000 < 2000 < 4000`. **T2 no elimina la IP.** L'expiració arriba al final de la durada vàlida si no hi ha renovació.

**Exemple 1.** La concessió comença a les 09.00:

- `1000 = 16 × 60 + 40`: T1 a les **09.16.40**.
- `2000 = 33 × 60 + 20`: T2 a les **09.33.20**.
- `4000 = 66 × 60 + 40`: venciment a les **10.06.40**.

**Exemple 2.** Si triem 3600 s de durada, T1 de 1800 s i T2 de 3150 s, una concessió iniciada a les 10.00 tindrà T1 a les 10.30, T2 a les 10.52.30 i venciment a les 11.00, si no es renova.

En teoria vam treballar els valors predeterminats del 50 % i del 87,5 %. A l'exemple del PDF, **els temporitzadors són explícits**: T1 és el 25 % i T2 el 50 % de 4000 s. No tornis a calcular-los com si no estiguessin configurats. Contrasta els valors efectivament rebuts a la captura DHCP.

### 8. Concessions persistents

> **Objectiu:** distingir configuració i estat del servei.
>
> **Resultat esperat:** localitzes el fitxer real on Kea desa les concessions.

`kea-dhcp4.conf` descriu les regles. El fitxer de concessions registra assignacions. Amb `memfile` i `persist: true`, l'exemple desa les dades a:

```text
/var/lib/kea/kea-leases4.csv
```

```bash
sudo head -n 6 /var/lib/kea/kea-leases4.csv
sudo tail -n 10 /var/lib/kea/kea-leases4.csv
```

Llegeix primer la capçalera i identifica IP, adreça de maquinari, identificador de client, durada, expiració i subxarxa quan apareguin.

El PDF esmenta dues rutes diferents: `/var/lib/kea/kea-leases4.csv` a l'exemple i `/var/lib/kea/dhcp4.leases` a l'activitat. **La ruta que mana és el valor `name` de la configuració carregada.** En aquests dos MD utilitzem explícitament la primera.

El CSV pot contenir successives actualitzacions d'una mateixa concessió fins que es compacta. Comptar línies no equival a comptar clients actius. No l'editis a mà mentre Kea funciona ni l'esborris per forçar una renovació.

---

<a id="fase-4"></a>

## Fase 4. Comprovar i reservar

Valida el servei i demostra l'assignació dinàmica i la reserva des del client.

### 9. Validar i aplicar

> **Objectiu:** detectar errors abans de reiniciar i comprovar el resultat després.
>
> **Resultat esperat:** configures, valides, reinicies i observes en aquest ordre.

```bash
sudo kea-dhcp4 -t /etc/kea/kea-dhcp4.conf
```

Si la prova falla, corregeix el fitxer i repeteix-la. Si finalitza correctament:

```bash
sudo systemctl restart kea-dhcp4-server
sudo systemctl enable kea-dhcp4-server
systemctl status kea-dhcp4-server --no-pager
sudo journalctl -u kea-dhcp4-server -b --no-pager -n 50
```

La ruta absoluta evita dependre del directori des d'on executes l'ordre. La validació no demostra que el client sigui al segment correcte ni que hi hagi una concessió real.

**Tres nivells de comprovació:** fitxer acceptat → procés funcionant → client configurat amb les dades correctes. Cal arribar al tercer.

<!-- CAPTURA 03: prova kea-dhcp4 -t correcta i estat active del servei amb el nom d'unitat visible. Fitxer suggerit: source/03_DHCP_Kea/03-validacio-servei.png -->

### 10. Comprovar el client

> **Objectiu:** comprovar l'assignació efectiva.
>
> **Resultat esperat:** identifiques IP, prefix, ruta, DNS i servidor DHCP.

El client ha d'estar a la mateixa xarxa interna i en mode IPv4 automàtic. Si prové de la base Ubuntu/Zorin, pot conservar la IP manual `.20`: cal canviar-ne el mètode i retirar els valors manuals.

A Zorin, desactiva i reactiva **la connexió interna correcta** des de la interfície gràfica. Per terminal, identifica primer el perfil:

```bash
nmcli connection show
nmcli device status
```

Exemple per a un perfil que s'anomena realment `Kea-LAB`:

```bash
sudo nmcli connection down "Kea-LAB"
sudo nmcli connection up "Kea-LAB"
ip -4 -br addr
ip route
nmcli -f GENERAL,IP4,DHCP4 device show enp0s8
```

Substitueix perfil i interfície. `nmcli` correspon a NetworkManager, habitual al client Zorin; no el donis per disponible al servidor gestionat amb `systemd-networkd`.

A Windows pots consultar `ipconfig /all` i renovar amb `ipconfig /renew` sobre l'adaptador adequat. No executis simultàniament un altre client DHCP manual en una interfície ja gestionada per NetworkManager.

**Interpretació:** una IP dins del rang és una pista; l'ACK, les opcions rebudes i la concessió al servidor permeten relacionar-la amb Kea. Si l'IP és del NAT, revisa l'adaptador abans de tocar el JSON.

### 11. Afegir una reserva

> **Objectiu:** assignar una IP concreta des del servidor mantenint DHCP al client.
>
> **Resultat esperat:** el client identificat rep la reserva i no una IP manual.

En aquesta demostració reservarem `192.168.50.55`, fora del pool `.100–.149`. Busca la MAC real de la interfície interna de Zorin:

```bash
ip -br link
```

Dins de l'objecte de subxarxa, al mateix nivell que `pools` i `option-data`, afegeix:

```json
"reservations": [
  {
    "hw-address": "08:00:27:aa:bb:cc",
    "ip-address": "192.168.50.55"
  }
]
```

**La MAC és fictícia: substitueix-la.** El fragment no és un fitxer complet. Afegeix la coma que separa aquesta propietat de l'anterior, però no afegeixis una coma després de l'última propietat de l'objecte.

Una reserva ha de pertànyer a la subxarxa. En aquest laboratori la situem fora del pool per facilitar la gestió; Kea també admet reserves dins del pool segons la configuració, de manera que no és una prohibició universal.

Repeteix validació, reinici, reconnexió del client i comprovació. El client ha de continuar amb mètode automàtic. Si encara conserva una concessió anterior, observa el nou intercanvi i espera que finalitzi abans de concloure que la reserva ha fallat.

**Error freqüent:** copiar la MAC del NAT, de l'amfitrió o d'una VM anterior a la importació. La reserva reconeix el client que realment envia la petició.

---

<a id="fase-5"></a>

## Fase 5. Consolidar

Diagnostica a partir d'evidències i comprova que pots justificar les decisions.

### 12. Diagnosticar amb evidències

> **Objectiu:** relacionar cada símptoma amb una hipòtesi i una comprovació concreta.
>
> **Resultat esperat:** justifiques el següent pas de diagnosi amb dades del client, del servei o de la captura.

| Símptoma | Què comprovar primer | Què fer després |
|---|---|---|
| Kea no accepta el fitxer | Línia de l'error, comes, claus, tipus de valor | Corregir i repetir `-t` |
| La prova passa però no arrenca | Registres, interfície, permisos del directori de concessions | Corregir la causa concreta |
| Servei actiu però cap oferta | Xarxa interna, interfície d'escolta, subxarxa, pool | Capturar petició i resposta al segment correcte |
| El client mostra `10.0.2.x` | Mode NAT o adaptador equivocat | Revisar VirtualBox i el perfil del client |
| Manté `.20` de la base | Perfil manual o configuració antiga | Passar la connexió de prova a automàtica |
| Rep IP però no navega | Existència del router anunciat i ruta exterior | Distingir DHCP correcte d'encaminament absent |
| No aplica la reserva | MAC real, subxarxa, JSON carregat i nova negociació | Comparar captura i concessió |
| El CSV indicat no existeix | Valor `lease-database.name` i registres | Consultar la ruta real; no crear fitxers buits |
| Apareixen ofertes inesperades | Servidor DHCP que les envia | Revisar altres VM i modes de xarxa |

Si revises ports, `sudo ss -lunp` aporta informació, però Kea pot utilitzar sockets de baix nivell: no utilitzis aquesta única sortida per decidir si atén clients. La captura a la interfície interna i els registres són les comprovacions decisives.

### 13. Autoavaluació

> **Objectiu:** comprovar si pots explicar i aplicar els conceptes sense consultar la guia.
>
> **Resultat esperat:** respons les preguntes amb una justificació i identifiques els apartats que cal repassar.

1. Què configura Netplan i què configura Kea?
2. Per què el servidor té una IP estàtica a la xarxa interna?
3. Quantes adreces hi ha entre `.10` i `.50`, incloses?
4. Què significa rebind i quan s'ha de deixar d'utilitzar una concessió?
5. Per què una passarel·la anunciada pot no proporcionar Internet?
6. Com demostres que `.55` prové d'una reserva i no d'una configuració manual?

<details>
<summary><strong>Respostes orientatives</strong></summary>

1. Netplan configura les interfícies d'Ubuntu; Kea defineix què ofereix als clients.
2. Per disposar d'una adreça estable i coherent amb la subxarxa que atén.
3. `50 − 10 + 1 = 41`.
4. Rebind és l'intent de renovar amb altres servidors; l'adreça deixa de ser vàlida quan expira la concessió sense renovació.
5. DHCP pot anunciar una IP encara que allà no hi hagi cap router funcional.
6. Client en automàtic, reserva al servidor, ACK i concessió associats a la MAC correcta.

</details>

---

## Consulta i ajuda

### Fonts i correspondència amb el PDF

| Pàgines del PDF | Contingut | Apartats d'aquesta guia |
|---|---|---|
| 1–3 | Presentació, índex i separació guia/activitat | Introducció |
| 4–7 | Preparació i xarxa | 1–2 |
| 8–10 | Instal·lació i agent de control | 3 |
| 11–15 | Components i systemd | 4 |
| 16–22 | Fitxer, JSON i exemple | 5–8 |
| 23–25 | Aplicació i client | 9–10 |
| 26–28 | Reserva i comprovació | 11 |
| 34–36 | Fonts, autoria i tancament | Fonts i autoavaluació |

Material de partida: **Carlos Alonso Martínez**, *UD2 AA2 DHCP Linux amb Kea*, v20250808; el PDF indica **CC BY-NC-ND 4.0**. Aquest MD és un suport explicatiu complementari amb exemples i aclariments propis; conserva el PDF original com a referència.

- [Ubuntu Server — Instal·lació i configuració de Kea](https://ubuntu.com/server/docs/how-to/networking/install-isc-kea/)
- [Kea 2.4.1 — DHCPv4, concessions i reserves](https://kea.readthedocs.io/en/kea-2.4.1/arm/dhcp4-srv.html)
- [NetworkManager — nmcli](https://networkmanager.dev/docs/api/latest/nmcli.html)
- [RFC 1918 — Adreçament privat](https://www.rfc-editor.org/rfc/rfc1918)

Consulta `kea-dhcp4 -v` i utilitza el manual de la versió instal·lada si difereix de la família 2.4. Les comprovacions aquí descrites s'han de repetir a les VM reals.
