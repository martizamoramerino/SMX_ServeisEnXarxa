![Portada](./source/00_Zorin_OS/00-instalacio-zorin-os-portada.png)

# Instal·lació de Zorin OS en una màquina virtual

> **MP 0227 · Serveis de xarxa · 2n SMX**

En aquesta guia crearàs una màquina virtual amb **Zorin OS Core** que utilitzarem com a client gràfic a les pràctiques de xarxa. Aquesta màquina servirà, entre altres usos, per comprovar el funcionament del servidor DHCP amb Kea instal·lat a Ubuntu Server.

> [!IMPORTANT]
> Zorin OS **no s'instal·la dins d'Ubuntu Server**. Ubuntu Server i Zorin seran dues màquines virtuals independents, executades al mateix ordinador amfitrió mitjançant VirtualBox.

<a id="itinerari-de-treball"></a>

## Ruta de treball

| Fase | Apartats | Què aconseguiràs? |
|---|---|---|
| **[Fase 1. Preparació](#fase-1)** | 1–2 | ISO oficial descarregada i verificada |
| **[Fase 2. Creació de la VM](#fase-2)** | 3–5 | Maquinari virtual i NAT configurats |
| **[Fase 3. Instal·lació](#fase-3)** | 6–8 | Zorin arrenca des del disc virtual sense la ISO |
| **[Fase 4. Preparació del client](#fase-4)** | 9–11 | Sistema actualitzat i xarxa identificada |
| **[Fase 5. Conservació de la base](#fase-5)** | 12 | Instantània o còpia base creada |

> [!TIP]
> La primera vegada, segueix els apartats en ordre. Si reprens la pràctica, consulta l'**objectiu** i el **resultat esperat** de cada apartat per saber des d'on continuar.

## Índex

- **Preparació:** [Objectius i resultats esperats](#objectius-i-resultats-esperats) · [Resultat final](#resultat-final-esperat) · [Convencions](#convencions-de-la-guia) · [Requisits previs](#requisits-previs)
- **[Fase 1 — Preparació](#fase-1):** [1. Descarregar Zorin OS Core](#1-descarregar-zorin-os-core) · [2. Comprovar la integritat de la ISO](#2-comprovar-la-integritat-de-la-iso)
- **[Fase 2 — Creació de la VM](#fase-2):** [3. Crear la màquina virtual](#3-crear-la-màquina-virtual) · [4. Assignar recursos](#4-assignar-recursos) · [5. Revisar la xarxa i la ISO](#5-revisar-la-xarxa-i-la-iso)
- **[Fase 3 — Instal·lació](#fase-3):** [6. Arrencar l'instal·lador](#6-arrencar-linstallador) · [7. Instal·lar Zorin OS](#7-installar-zorin-os) · [8. Reiniciar i retirar la ISO](#8-reiniciar-i-retirar-la-iso)
- **[Fase 4 — Preparació del client](#fase-4):** [9. Fer les comprovacions inicials](#9-fer-les-comprovacions-inicials) · [10. Actualitzar el sistema](#10-actualitzar-el-sistema) · [11. Identificar la xarxa del client](#11-identificar-la-xarxa-del-client)
- **[Fase 5 — Conservació de la base](#fase-5):** [12. Crear la base reutilitzable](#12-crear-la-base-reutilitzable) · [Comprovació final](#comprovació-final) · [Evidències](#evidències-recomanades) · [Reflexió](#preguntes-de-reflexió)
- **Consulta i ajuda:** [Preparació per a la pràctica de DHCP amb Kea](#preparació-per-a-la-pràctica-de-dhcp-amb-kea) · [Resolució d'incidències](#resolució-dincidències) · [Fonts de consulta](#fonts-de-consulta)

---

## Preparació

<a id="què-has-daconseguir"></a>

### Objectius i resultats esperats

- [ ] Descarregar la ISO oficial de Zorin OS Core i identificar-ne la versió.
- [ ] Comprovar la integritat del fitxer descarregat.
- [ ] Crear una màquina virtual adequada a VirtualBox.
- [ ] Instal·lar Zorin OS al disc virtual.
- [ ] Retirar la ISO després de la instal·lació.
- [ ] Actualitzar el sistema i comprovar-ne el funcionament.
- [ ] Identificar la interfície de xarxa, la MAC, l'adreça IP i la ruta per defecte.
- [ ] Crear una instantània o una còpia base abans de començar les pràctiques de xarxa.

#### Resultat final esperat

En acabar tindràs aquesta estructura:

| Màquina virtual | Sistema | Funció posterior | Xarxa en acabar aquesta guia |
|---|---|---|---|
| `UbuntuServer_BASE` | Ubuntu Server 24.04 LTS | Servidor de xarxa | La configurada a la guia d'Ubuntu Server |
| `ZorinClient_BASE` | Zorin OS Core | Client gràfic de proves | NAT |

La connexió a la xarxa interna `SMX-LAB` es farà més endavant, quan ho indiqui l'activitat de DHCP.

### Convencions de la guia

Segueix els apartats en ordre i compara cada resultat amb el **resultat esperat** abans de continuar. Adapta les rutes, els noms i les interfícies dels exemples a la teva màquina.

Els comentaris HTML que comencen per `CAPTURA` indiquen les evidències que cal preparar. Es veuen quan edites el Markdown, però no en la vista de lectura.

<a id="abans-de-començar"></a>

### Requisits previs

#### Material necessari

- VirtualBox instal·lat a l'ordinador amfitrió.
- Connexió a Internet.
- Espai lliure suficient per a la ISO, el disc virtual i les instantànies.
- La ISO oficial de Zorin OS Core.
- La màquina Ubuntu Server de la pràctica anterior, si ja està disponible.

#### Recursos de la màquina virtual

Els requisits mínims oficials de Zorin OS Core són un processador de 64 bits amb dos nuclis a 1 GHz, 2 GB de RAM i 15 GB d'emmagatzematge. Per treballar amb més comoditat al laboratori utilitzarem una configuració superior:

| Recurs | Configuració de laboratori | Observació |
|---|---:|---|
| CPU | 2 processadors virtuals | No assignis tots els nuclis de l'equip físic |
| RAM | 4 GB | Si l'equip va just, es pot reduir, però no per sota del mínim |
| Disc | 30 GB dinàmics | El fitxer creixerà a mesura que s'utilitzi |
| Vídeo | 128 MB | Activa l'acceleració 3D només si funciona de manera estable |
| Xarxa inicial | 1 adaptador NAT | Permet descarregar actualitzacions durant la preparació |

> [!CAUTION]
> Les màquines virtuals comparteixen CPU, memòria i disc amb l'ordinador físic. Assignar massa recursos pot fer que tant l'amfitrió com les VM funcionin pitjor.

---

<a id="fase-1"></a>

## Fase 1. Preparació

Obtén la ISO oficial i comprova'n la integritat abans d'utilitzar-la.

### 1. Descarregar Zorin OS Core

> **Objectiu:** obtenir la imatge d'instal·lació des del lloc oficial.
>
> **Resultat esperat:** disposes d'un fitxer `.iso` de Zorin OS Core i en coneixes la versió.

1. Accedeix a la pàgina oficial de descàrrega:
   - <https://zorin.com/os/download/>
2. Localitza l'edició **Zorin OS Core**.
3. Selecciona l'opció gratuïta de descàrrega.
4. Si apareix la subscripció al butlletí, pots subscriure-t'hi o utilitzar l'opció per continuar directament amb la descàrrega.
5. Desa la ISO en una ubicació que puguis trobar fàcilment.
6. No canviïs l'extensió ni descomprimeixis el fitxer.

Anota aquestes dades:

| Dada | Valor |
|---|---|
| Edició | Zorin OS Core |
| Versió descarregada |  |
| Nom complet de la ISO |  |
| Data de descàrrega |  |

**Concepte clau · ISO:** una ISO és una imatge que conté l'estructura d'un mitjà d'instal·lació. A VirtualBox la connectarem a una unitat òptica virtual; no cal gravar-la en un USB.

<!-- CAPTURA 01: pàgina oficial o carpeta de descàrregues on es vegi el nom complet de la ISO. No mostris dades personals. Fitxer suggerit: imatges/01-iso-zorin.png -->

### 2. Comprovar la integritat de la ISO

> **Objectiu:** verificar que la descàrrega no està incompleta ni alterada.
>
> **Resultat esperat:** el resum SHA-256 calculat coincideix amb el publicat per Zorin.

Una suma de comprovació és una empremta calculada a partir del contingut del fitxer. Si canvia un sol fragment de la ISO, el resultat també canvia.

1. Consulta els SHA-256 oficials:
   - <https://help.zorin.com/docs/getting-started/check-the-integrity-of-your-copy-of-zorin-os/>
2. Calcula el SHA-256 de la ISO descarregada.

#### A Windows amb PowerShell

```powershell
Get-FileHash "C:\RUTA\Zorin-OS.iso" -Algorithm SHA256
```

#### A Linux

```bash
sha256sum /ruta/Zorin-OS.iso
```

3. Compara tots els caràcters del resultat amb el valor oficial de la mateixa edició i versió.

**No continuïs si no coincideixen.** Elimina la còpia defectuosa i descarrega-la de nou des del lloc oficial.

**Pregunta de control:** que el nom del fitxer sigui correcte demostra que el contingut també ho és? No. El nom es pot conservar encara que la descàrrega estigui incompleta o el contingut hagi canviat.

<!-- CAPTURA 02: ordre i SHA-256 calculat. Ha de poder-se comparar amb el valor oficial. Fitxer suggerit: imatges/02-sha256-zorin.png -->

---

<a id="fase-2"></a>

## Fase 2. Creació de la VM

Crea una màquina independent i revisa els recursos, el disc, la ISO i la xarxa NAT.

### 3. Crear la màquina virtual

> **Objectiu:** crear una VM independent per al client Zorin.
>
> **Resultat esperat:** VirtualBox mostra una màquina nova anomenada `ZorinClient_BASE`.

1. Obre VirtualBox.
2. Prem **Nova**.
3. Utilitza aquests valors com a referència:

| Camp | Valor proposat |
|---|---|
| Nom | `ZorinClient_BASE` |
| Carpeta | La carpeta de màquines virtuals del curs |
| Imatge ISO | La ISO verificada de Zorin |
| Tipus | Linux |
| Versió | Ubuntu (64-bit) |

4. Si VirtualBox proposa una instal·lació desatesa, marca **Ometre instal·lació desatesa**. Així podràs observar i documentar totes les decisions de l'instal·lador.
5. Comprova que la màquina es crea en una carpeta amb prou espai lliure.

> [!NOTE]
> Segons la versió de VirtualBox, l'assistent pot mostrar les opcions en un altre ordre. No memoritzis els clics: identifica el nom, el tipus de sistema, la ISO i els recursos que estàs assignant.

<!-- CAPTURA 03: resum de creació de la VM amb nom, tipus i ISO. Fitxer suggerit: imatges/03-creacio-vm-zorin.png -->

### 4. Assignar recursos

> **Objectiu:** proporcionar recursos suficients sense esgotar l'equip físic.
>
> **Resultat esperat:** la VM disposa de 2 CPU, 4 GB de RAM i un disc dinàmic de 30 GB.

Configura:

1. **Memòria base:** `4096 MB`.
2. **Processadors:** `2`.
3. **Disc virtual:** crea'n un de nou.
4. **Format:** `VDI` si l'assistent ho pregunta.
5. **Reserva:** assignació dinàmica.
6. **Capacitat màxima:** `30 GB`.

#### Què significa disc dinàmic?

El disc virtual pot arribar als 30 GB, però el fitxer no ocupa necessàriament aquesta mida des del primer moment. Creix a mesura que la VM emmagatzema dades.

> [!WARNING]
> Dinàmic no significa il·limitat. Si el disc físic de l'amfitrió s'omple, la màquina virtual pot fallar encara que el disc virtual tingui capacitat teòrica disponible.

### 5. Revisar la xarxa i la ISO

> **Objectiu:** garantir que la màquina pot instal·lar-se i connectar-se a Internet.
>
> **Resultat esperat:** la ISO està muntada i l'adaptador 1 utilitza NAT.

Amb la VM apagada, entra a **Configuració** i revisa:

#### Sistema

- Ordre d'arrencada: òptic abans que disc dur durant la instal·lació.
- 2 processadors virtuals.
- 4096 MB de RAM, si l'equip físic ho permet.

#### Pantalla

- Memòria de vídeo: `128 MB`.
- Si apareixen defectes gràfics, prova de desactivar l'acceleració 3D.

#### Emmagatzematge

- La ISO de Zorin està connectada a la unitat òptica virtual.
- El disc VDI de 30 GB apareix connectat.

#### Xarxa

| Adaptador | Estat | Mode | Funció actual |
|---|---|---|---|
| 1 | Activat | NAT | Internet per a instal·lació i actualitzacions |
| 2 | Desactivat | — | Encara no s'utilitza |

**Concepte clau · NAT de VirtualBox:** la VM surt a Internet a través de l'amfitrió i pot rebre una configuració IP del DHCP virtual de VirtualBox. Aquest no és el servidor Kea de la pràctica.

**Pregunta de control:** si Zorin rep una IP mentre està en NAT, ja hem demostrat que el nostre Kea funciona? No. En aquesta fase respon la infraestructura virtual de VirtualBox.

<!-- CAPTURA 04: emmagatzematge amb ISO i disc virtual, i xarxa NAT. Fitxer suggerit: imatges/04-iso-disc-nat.png -->

---

<a id="fase-3"></a>

## Fase 3. Instal·lació

Completa la instal·lació i comprova que Zorin arrenca des del disc virtual.

### 6. Arrencar l'instal·lador

> **Objectiu:** iniciar la VM des de la ISO.
>
> **Resultat esperat:** apareix el menú inicial de Zorin OS.

1. Inicia `ZorinClient_BASE`.
2. Si VirtualBox demana un disc d'inici, selecciona la ISO descarregada.
3. Al menú d'arrencada, selecciona **Try or Install Zorin OS**.
4. Espera que es carregui l'entorn gràfic.
5. Selecciona l'idioma de treball.
6. Tria l'opció per instal·lar Zorin OS.

Si la finestra no mostra els botons inferiors:

- augmenta la resolució de la pantalla virtual, o
- mantén premuda la tecla `Super` i arrossega la finestra cap amunt.

**Diferència important:** provar Zorin executa un entorn temporal des de la ISO. Instal·lar-lo copia el sistema al disc virtual perquè els canvis es conservin.

<!-- CAPTURA 05: menú Try or Install Zorin OS o primera pantalla de l'instal·lador. Fitxer suggerit: imatges/05-inici-installador.png -->

### 7. Instal·lar Zorin OS

> **Objectiu:** completar la instal·lació al disc virtual.
>
> **Resultat esperat:** l'instal·lador finalitza sense errors i demana reiniciar.

Els textos exactes poden variar lleugerament segons la versió. Llegeix cada pantalla abans de continuar.

#### 7.1 Idioma i teclat

1. Selecciona l'idioma acordat a classe.
2. Selecciona la distribució del teclat corresponent.
3. Utilitza el camp de prova per comprovar caràcters com `ç`, accents, `/`, `-` i `:`.

#### 7.2 Connexió i actualitzacions

1. Confirma que la VM té connexió mitjançant NAT.
2. Si l'instal·lador ofereix descarregar actualitzacions durant la instal·lació, pots activar-ho.
3. Evita afegir programari o controladors que no siguin necessaris per a aquesta VM de laboratori.

#### 7.3 Tipus d'instal·lació

Selecciona **Esborra el disc i instal·la Zorin OS**.

> [!IMPORTANT]
> En aquesta pràctica, «el disc» és el **disc virtual nou de 30 GB**, no el disc físic de Windows. Abans de confirmar, comprova que estàs treballant dins de la finestra de la VM correcta.

No necessitem:

- arrencada dual;
- particionament manual;
- modificar el disc d'Ubuntu Server;
- compartir el mateix disc virtual entre les dues VM.

#### 7.4 Zona horària

Selecciona **Madrid** o la zona indicada pel docent. Una hora incorrecta pot dificultar la lectura de registres i la comparació d'esdeveniments entre client i servidor.

#### 7.5 Usuari i nom de l'equip

Utilitza una identificació coherent amb el laboratori:

| Camp | Exemple |
|---|---|
| Nom visible | `Alumne Cognom` |
| Nom de l'equip | `zorin-nomcognom` |
| Usuari | `alumne` o el criteri indicat |
| Contrasenya | Una contrasenya pròpia que puguis recordar |

Recomanacions per al nom de l'equip:

- minúscules;
- sense espais ni accents;
- guions si cal separar paraules;
- identificable quan aparegui a la xarxa.

> [!CAUTION]
> No incloguis contrasenyes a les captures, al Markdown ni al nom dels fitxers.

#### 7.6 Finalitzar

1. Confirma les decisions de l'instal·lador.
2. Espera que copiï els fitxers i configuri el sistema.
3. No tanquis VirtualBox ni apaguis l'ordinador durant el procés.
4. Quan aparegui el missatge final, selecciona **Reinicia ara**.

<!-- CAPTURA 06: resum o procés d'instal·lació sense contrasenyes visibles. Fitxer suggerit: imatges/06-installacio-zorin.png -->

### 8. Reiniciar i retirar la ISO

> **Objectiu:** arrencar el sistema instal·lat des del disc virtual.
>
> **Resultat esperat:** Zorin inicia sessió sense tornar a mostrar l'instal·lador.

Durant el reinici, l'instal·lador pot demanar que retiris el mitjà d'instal·lació.

1. Si VirtualBox l'expulsa automàticament, prem `Enter` quan ho indiqui Zorin.
2. Si torna a aparèixer l'instal·lador:
   1. apaga la VM;
   2. obre **Configuració → Emmagatzematge**;
   3. selecciona la unitat òptica;
   4. retira la ISO del lector virtual;
   5. torna a iniciar la VM.
3. Comprova que Zorin arrenca des del disc dur virtual.
4. Inicia sessió amb l'usuari creat.

#### Com saber des d'on ha arrencat?

- Si apareix el teu usuari i es conserven els canvis, probablement has iniciat el sistema instal·lat.
- Si torna a aparèixer **Try or Install**, has arrencat de nou des de la ISO.

<!-- CAPTURA 07: escriptori de Zorin després d'arrencar des del disc instal·lat. Fitxer suggerit: imatges/07-primer-inici.png -->

---

<a id="fase-4"></a>

## Fase 4. Preparació del client

Comprova el sistema, instal·la les actualitzacions i identifica la configuració de xarxa.

### 9. Fer les comprovacions inicials

> **Objectiu:** confirmar que el sistema instal·lat és funcional abans de modificar-lo.
>
> **Resultat esperat:** pots iniciar sessió, obrir el terminal i consultar la versió.

Obre un terminal amb `Ctrl` + `Alt` + `T` i executa:

```bash
hostnamectl
cat /etc/os-release
whoami
date
```

Interpreta els resultats:

| Ordre | Què has de comprovar |
|---|---|
| `hostnamectl` | Nom de l'equip i arquitectura |
| `cat /etc/os-release` | Distribució i versió instal·lades |
| `whoami` | Usuari amb què has iniciat sessió |
| `date` | Data, hora i zona horària coherents |

Comprova també:

- que el teclat escriu correctament;
- que la resolució permet treballar;
- que el ratolí entra i surt de la VM;
- que el sistema detecta la connexió de xarxa.

<!-- CAPTURA 08: terminal amb hostnamectl, os-release i data. Fitxer suggerit: imatges/08-comprovacions-sistema.png -->

### 10. Actualitzar el sistema

> **Objectiu:** deixar la base amb les actualitzacions disponibles instal·lades.
>
> **Resultat esperat:** APT acaba sense errors pendents.

Primer comprova la connectivitat per nom:

```bash
getent hosts zorin.com
```

Després actualitza la informació dels repositoris i els paquets:

```bash
sudo apt update
sudo apt upgrade
```

Llegeix el resum abans de confirmar. Si s'ha actualitzat el nucli o el sistema ho recomana, reinicia:

```bash
sudo reboot
```

#### Si `apt update` falla

No repeteixis l'ordre sense analitzar el missatge. Comprova:

```bash
ip -4 -br addr
ip route
resolvectl status
getent hosts zorin.com
```

Relaciona el símptoma amb una hipòtesi:

| Símptoma | Hipòtesi inicial |
|---|---|
| No hi ha cap IPv4 | Adaptador desactivat o DHCP no rebut |
| Hi ha IP però no hi ha ruta `default` | Configuració incompleta de xarxa |
| Hi ha ruta però no es resolen noms | Problema de DNS |
| Un repositori concret falla | Incidència del repositori o configuració d'APT |

<!-- CAPTURA 09: final d'apt update/upgrade sense errors. Fitxer suggerit: imatges/09-actualitzacio.png -->

### 11. Identificar la xarxa del client

> **Objectiu:** relacionar VirtualBox, la interfície Linux i la configuració rebuda.
>
> **Resultat esperat:** identifiques interfície, MAC, IPv4, ruta i DNS del client en NAT.

Executa:

```bash
ip -br link
ip -4 -br addr
ip route
resolvectl status
nmcli device status
nmcli connection show
```

Completa la taula amb dades reals:

| Element | Valor observat |
|---|---|
| Nom de la interfície |  |
| Adreça MAC |  |
| IPv4 i prefix |  |
| Passarel·la per defecte |  |
| DNS |  |
| Nom del perfil de NetworkManager |  |

#### Relació entre les dades

```text
VirtualBox: Adaptador 1 en NAT
        ↓
Linux: interfície, per exemple enp0s3
        ↓
NetworkManager: perfil de connexió
        ↓
Configuració rebuda: IP, prefix, ruta i DNS
```

El nom `enp0s3` és només un exemple. Utilitza sempre el que aparegui a la teva màquina.

#### Comprovar la MAC a VirtualBox

1. Apaga la VM.
2. Obre **Configuració → Xarxa → Adaptador 1 → Avançat**.
3. Anota la MAC.
4. Torna a iniciar Zorin i compara-la amb `ip -br link`.

La MAC pot aparèixer amb formats diferents:

- VirtualBox: `080027A1B2C3`
- Linux: `08:00:27:a1:b2:c3`

És el mateix valor; Linux hi afegeix separadors i acostuma a mostrar lletres en minúscula.

**Pregunta de control:** l'adreça IPv4 rebuda en NAT serà la mateixa que rebrà del servidor Kea a `SMX-LAB`? No necessàriament. Són xarxes i servidors DHCP diferents.

<!-- CAPTURA 10: ordres de xarxa que mostrin interfície, IPv4 i ruta. Fitxer suggerit: imatges/10-xarxa-nat.png -->

---

<a id="fase-5"></a>

## Fase 5. Conservació de la base

Desa una base recuperable, revisa els resultats i recull les evidències de la preparació.

### 12. Crear la base reutilitzable

> **Objectiu:** conservar un punt funcional abans de començar les pràctiques.
>
> **Resultat esperat:** pots tornar a una instal·lació neta i actualitzada si una configuració posterior falla.

#### 12.1 Neteja prèvia

1. Tanca aplicacions obertes.
2. Comprova que no hi ha actualitzacions en curs.
3. Buida la paperera si és necessari.
4. Apaga correctament la màquina:

```bash
sudo poweroff
```

#### 12.2 Crear una instantània

Amb la VM apagada:

1. Obre la secció **Instantànies** de VirtualBox.
2. Crea una instantània amb el nom:

```text
BASE_ZORIN_INSTAL·LAT_ACTUALITZAT
```

3. A la descripció, anota la versió de Zorin, la data i que l'adaptador està en NAT.

#### 12.3 Opcional: exportar una OVA

Si el docent demana una còpia portable:

1. Selecciona **Fitxer → Exporta un servei virtualitzat** o l'opció equivalent.
2. Selecciona `ZorinClient_BASE`.
3. Desa l'OVA en una ubicació amb espai suficient.
4. No donis per vàlida l'exportació només perquè existeix el fitxer: si és una entrega, importa-la i comprova-la segons les indicacions del docent.

> [!IMPORTANT]
> Una instantània depèn de la VM original. Una OVA és una exportació pensada per transportar o recrear la màquina. No són el mateix mecanisme.

<!-- CAPTURA 11: instantània creada amb el nom indicat i VM apagada. Fitxer suggerit: imatges/11-instantania-base.png -->

#### Comprovació final

Marca cada punt només quan l'hagis verificat:

- [ ] La VM es diu `ZorinClient_BASE`.
- [ ] La ISO prové del web oficial i el SHA-256 coincideix.
- [ ] Zorin arrenca des del disc virtual sense la ISO.
- [ ] L'usuari pot iniciar sessió.
- [ ] El teclat, la pantalla i el terminal funcionen.
- [ ] El sistema identifica correctament la versió instal·lada.
- [ ] `apt update` i `apt upgrade` han finalitzat correctament.
- [ ] L'adaptador 1 està en NAT.
- [ ] S'han identificat interfície, MAC, IPv4, ruta i DNS.
- [ ] S'ha creat una instantània amb la VM apagada.
- [ ] La base original encara no s'ha connectat a `SMX-LAB`.

#### Evidències recomanades

| Evidència | Què ha de demostrar |
|---|---|
| Captura 01 | ISO oficial i versió |
| Captura 02 | Coincidència SHA-256 |
| Captures 03–04 | Configuració de la VM, disc, ISO i NAT |
| Captures 05–07 | Inici, instal·lació i primer arrencada |
| Captures 08–09 | Identitat del sistema i actualització |
| Captura 10 | Configuració de xarxa en NAT |
| Captura 11 | Instantània final de la base |

Les captures han de ser pròpies, llegibles i útils. No capturis cada clic: selecciona evidències que demostrin decisions i resultats.

#### Preguntes de reflexió

1. Per què Zorin i Ubuntu Server han de ser VM independents?
2. Quina diferència hi ha entre la ISO i el disc VDI?
3. Per què calculem el SHA-256 abans d'instal·lar?
4. Per què utilitzem NAT durant la preparació?
5. Quin DHCP configura el client mentre està en NAT?
6. Per què no podem utilitzar aquesta concessió per demostrar que Kea funciona?
7. Quina diferència hi ha entre una instantània i una OVA?
8. Quines dades recolliries si el client té IP però no resol noms?

---

## Consulta i ajuda

### Preparació per a la pràctica de DHCP amb Kea

No facis encara aquests canvis si el docent no ha iniciat l'activitat de Kea. Quan arribi el moment:

1. Es crearà una còpia de treball de `ZorinClient_BASE`.
2. Es mantindrà la base original apagada.
3. El client deixarà d'utilitzar NAT durant la prova controlada.
4. Es connectarà a la xarxa interna `SMX-LAB`.
5. IPv4 quedarà en mode automàtic.
6. El client demanarà la configuració al servidor Kea d'Ubuntu Server.

| Fase | Qui proporciona DHCP? | Xarxa |
|---|---|---|
| Instal·lació i actualització | VirtualBox | NAT |
| Pràctica de Kea | Ubuntu Server amb Kea | `SMX-LAB` |

Aquesta separació permet saber quin servidor està responent i evita interpretar una concessió de NAT com una prova correcta de Kea.

### Resolució d'incidències

Segueix aquest ordre: **observa el símptoma, recull dades, formula una hipòtesi, comprova-la i documenta la solució**.

| Símptoma | Possible causa | Comprovació i següent pas |
|---|---|---|
| No apareix Ubuntu (64-bit) | Virtualització desactivada o hipervisor en conflicte | Comprova VT-x/AMD-V i la configuració de l'amfitrió |
| La VM no arrenca la ISO | ISO no muntada o ordre d'arrencada incorrecte | Revisa Emmagatzematge i Sistema |
| La ISO dona errors | Descàrrega corrupta | Compara el SHA-256 i torna a descarregar si no coincideix |
| L'instal·lador no cap a la pantalla | Resolució virtual massa baixa | Augmenta-la o mou la finestra amb `Super` |
| La instal·lació és molt lenta | Poca RAM/CPU o disc físic saturat | Revisa recursos sense esgotar l'amfitrió |
| Després de reiniciar torna l'instal·lador | ISO encara connectada | Retira-la de la unitat òptica virtual |
| Apareix `No bootable medium` | No s'ha instal·lat al disc o ordre incorrecte | Comprova el disc virtual i repeteix el procés si cal |
| No hi ha Internet en NAT | Adaptador desactivat, configuració o DNS | Revisa VirtualBox, IP, ruta i resolució de noms |
| La pantalla es veu malament | Controlador gràfic o 3D | Prova un altre controlador gràfic o desactiva 3D |
| No es pot actualitzar | Xarxa, DNS, repositori o APT ocupat | Llegeix l'error i comprova cada capa abans d'actuar |
| La MAC de Linux no coincideix | S'ha mirat un altre adaptador | Compara el número d'adaptador i el nom de la interfície |

### Fonts de consulta

- [Descàrrega oficial de Zorin OS](https://zorin.com/os/download/)
- [Zorin Help · Instal·lar Zorin OS a VirtualBox](https://help.zorin.com/docs/getting-started/install-zorin-os-in-virtualbox/)
- [Zorin Help · Instal·lar Zorin OS](https://help.zorin.com/docs/getting-started/install-zorin-os/)
- [Zorin Help · Requisits del sistema](https://help.zorin.com/docs/getting-started/system-requirements/)
- [Zorin Help · Comprovar la integritat de la ISO](https://help.zorin.com/docs/getting-started/check-the-integrity-of-your-copy-of-zorin-os/)

> Consulta sempre les instruccions de la versió instal·lada. Els noms i l'ordre d'algunes pantalles poden variar entre versions de Zorin OS i VirtualBox.
