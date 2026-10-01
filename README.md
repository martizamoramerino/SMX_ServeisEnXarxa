# MP 0227 Serveis en Xarxa

Aquest repositori recull els materials, guies i pràctiques del mòdul professional **MP 0227 Serveis en Xarxa** de 2n del cicle formatiu de Sistemes Microinformàtics i Xarxes (SMX).

Al llarg del mòdul configurarem i administrarem serveis de xarxa en entorns Linux: preparació de servidors, configuració de xarxa, accés remot, resolució de noms, serveis web, compartició de recursos i altres serveis necessaris en una infraestructura informàtica.

## Lliçons disponibles

Fes clic a la **imatge** o al **títol** per obrir cada lliçó. Hi trobaràs les sis guies i activitats disponibles, ordenades segons la numeració dels fitxers. Els documents **00 A** i **00 B** preparen el servidor i el client del laboratori.

| Accés visual | Lliçó i continguts |
|---|---|
| [<img src="source/00_UbuntuServer_Images/55-server-virtualbox-resum-dos-adaptadors.png" alt="Obre la lliçó 00 A: Ubuntu Server 24.04 LTS" width="280">](00_A_UbuntuServer.md) | **[00 A · Ubuntu Server 24.04 LTS](00_A_UbuntuServer.md)**<br><br>Prepara la màquina virtual que utilitzaràs com a servidor al laboratori: instal·lació, configuració bàsica, SSH i xarxa amb Netplan.<br><br>**5 fases · 15 apartats**<br>Inclou validació, instantània, connexió amb un client i exportació d'una OVA. |
| [<img src="source/readme/00-b-zorin-os.svg" alt="Obre la lliçó 00 B: Instal·lació de Zorin OS" width="280">](00_B_Installacio_Zorin_OS.md) | **[00 B · Instal·lació de Zorin OS](00_B_Installacio_Zorin_OS.md)**<br><br>Prepara una VM independent amb Zorin OS Core com a client gràfic de les pràctiques: descàrrega i verificació de la ISO, creació de la VM i instal·lació.<br><br>**5 fases · 12 apartats**<br>Inclou actualitzacions, identificació de la xarxa NAT i conservació d'una base reutilitzable. |
| [<img src="source/01_Repas_TCP_IP/01-pila-tcp-ip.png" alt="Obre la lliçó 01: Repàs de xarxes TCP/IP" width="280">](01_Repas_TCP_IP_Guide_Activity.md) | **[01 · Repàs de xarxes TCP/IP](01_Repas_TCP_IP_Guide_Activity.md)**<br><br>Repassa les capes, l'adreçament IP, el càlcul de subxarxes, l'encaminament, els ports i NAT.<br><br>**3 fases · 10 apartats**<br>Inclou 8 activitats, pràctica amb Packet Tracer, solucionari raonat i autoavaluació. |
| [<img src="source/02_Servei_DHCP/00-servei-dhcp-portada.png" alt="Obre la lliçó 02: Introducció al servei DHCP" width="280">](02_Teoria_DHCP_Guide.md) | **[02 · Introducció al servei DHCP](02_Teoria_DHCP_Guide.md)**<br><br>Entén la configuració automàtica de xarxa: DORA, concessions, pools, reserves, relay i diagnosi del client.<br><br>**4 fases · 12 apartats**<br>Inclou incidències i protecció, 9 activitats, solucionari raonat i autoavaluació. |
| [<img src="source/02_Servei_DHCP/07-subxarxa-i-pool-dhcp.png" alt="Obre la lliçó 03: Configuració de DHCP amb Kea" width="280">](03_DHCP_Kea_Guia.md) | **[03 · Configuració de DHCP amb Kea](03_DHCP_Kea_Guia.md)**<br><br>Relaciona la teoria amb la configuració d'un servidor DHCPv4 a Ubuntu: interfícies, serveis, JSON, pools, opcions i temps de concessió.<br><br>**5 fases · 13 apartats**<br>Inclou validació del servei, comprovació del client, reserves, diagnosi i autoavaluació. |
| [<img src="source/02_Servei_DHCP/02b-dora-wireshark.png" alt="Obre la lliçó 04: Activitat guiada de DHCP amb Kea i Zorin" width="280">](04_DHCP_Kea_Activitat.md) | **[04 · Activitat guiada de DHCP amb Kea i Zorin](04_DHCP_Kea_Activitat.md)**<br><br>Desplega Kea amb les teves adreces de laboratori i comprova l'assignació des de Zorin. Captura i interpreta la negociació amb Wireshark.<br><br>**6 fases · 14 apartats**<br>Inclou consulta de concessions, prova d'una reserva, persistència i lliurament d'evidències. |

## Com seguir les guies

Comença per les guies **00 A** i **00 B** per disposar de les dues VM. Repassa TCP/IP i la teoria DHCP amb els documents **01** i **02**; després utilitza la guia **03** com a suport per resoldre l'activitat **04**.

Per treballar amb les guies:

1. **Ruta o itinerari de treball i índex:** localitza les fases i accedeix directament a cada apartat.
2. **Preparació:** revisa els objectius, les convencions i els requisits que s'hi indiquen.
3. **Treball per fases:** segueix els apartats i comprova l'objectiu i el resultat esperat de cadascun.
4. **Consulta i ajuda:** recupera les fonts i, quan n'hi hagi, els procediments de diagnosi i els errors freqüents.

En les activitats pràctiques, documenta el **valor esperat**, el **valor observat** i la **conclusió**. Consulta els solucionaris després d'haver intentat resoldre els exercicis.

Aquest índex s'ampliarà a mesura que s'incorporin noves lliçons.
