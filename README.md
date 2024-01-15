# README EN RELACIO A SNMP

# Introducció

Es tracta, mitjançant l'ús de SNMP i de contenidors Dockers, de poder executar diversos serveis web associats a diferents contenidors i poder monitoritzar-los mitjançant SNMP.

## Part 1

Creació d'un script que permeti executar o aturar N contenidors web (N>=1). Aquests contenidors són de tipus apache2 i s'executen en segon pla. Els contenidors s'han de crear a partir de la imatge de Docker (projecteinf/web). Aquesta imatge Docker conté l'agent SNMP configurat per a que es pugui monitoritzar el servei web que s'executa en el contenidor.

El màxim de contenidors Docker que es poden executar vindrà determinat pel número de contenidors que s'han executat en aquest script. Per exemple, si s'executa el script amb el paràmetre 3, es crearan 3 contenidors web. 

## Part 2

Execució de nous contenidors segons la càrrega del contenidor web. Utilitzarem el paràmetre "Server load" per a determinar la càrrega del servidor. 

Si la càrrega del servidor és superior a 0.5 s'executarà un nou contenidor web. Si la càrrega del servidor és inferior a 0.5 s'aturarà un contenidor web, excepte que hi hagi només un contenidor executant-se.


## Part 3

Guardar en una base de dades els valors de la càrrega dels contenidors web. 

# Creació i execució contenidor Docker

```bash
    docker run -d --name nom_del_contenidor -p port_local:port_contenidor nom_imatge
```

On:
    nom_del_contenidor és el nom que vols assignar al teu contenidor.
    port_local és el port del teu sistema local al qual vols redirigir el trànsit al contenidor.
    port_contenidor és el port al qual el servei web dins del contenidor està escoltant.
    nom_imatge és el nom de la imatge Docker que has construït per al teu servei web.

Per exemple, si vols que el teu contenidor escolti al port 80 del teu sistema local i el servei web dins del contenidor està escoltant també al port 80, la comanda seria:

```bash
docker run -d --name meu_contenidor -p 80:80 nom_imatge
```

Aquesta comanda crearà i executarà un contenidor Docker amb el teu servei web i l'agent SNMP configurat. Pots comprovar que el contenidor està en funcionament amb la comanda:

```bash
docker ps
```

Aquesta comanda mostrarà una llista dels contenidors Docker en funcionament al teu sistema.

Ara pots utilitzar la comanda snmpwalk o altres eines SNMP des de la teva màquina física per supervisar el teu servei web a través del protocol SNMP.

Per a executar un contenidor ja creat, utilitza la comanda:

```bash
docker start nom_del_contenidor
```

# Execució

Cal afegir l'usuari que executa les comandes al grup de docker

```bash
    sudo usermod -aG docker $USER
```

Per a executar el nostre script de Python cal executar la següent comanda:

```bash
    python3 TESTS/get.py
```

## Verificació funcionament - bash

```bash
    snmpwalk -v 2c -c public 172.17.0.2 1.3.6.1.2.1.1.1 # Comprovem que el contenidor està en funcionament
    snmpwalk -v2c -c public 172.17.0.2 # Veure tots els OIDs disponibles
```

## Comandes from history
```bash
    docker stop $(docker ps -a -q) # Parem tots els contenidors que s'estiguin executant
    docker rm $(docker ps -a -q) # Eliminem tots els contenidors
    docker image rm $(docker image ls -q) --force # Eliminem totes les imatges
    cd ./SNMP # Ens situem al directori on tenim el Dockerfile
    docker build -t web . # Construim la imatge (mba_nginx) a partir del Dockerfile
    docker image ls # Llistem les imatges
    docker run -d --name webcontainer -p 80:80 web # Creem i executem un contenidor a partir de la imatge web
    docker inspect webcontainer | grep '"IPAddress":' | cut -d ":" -f2 | cut -d "," -f1 | head -n1  # Adreça IP contenidor web
    python3 TESTS/get.py # Executem el script de Python per comprovar que el contenidor està en funcionament
```
 
# Publicar imatge a Docker
```bash
    docker login -u projecteinf
    IDIMG=$(docker image ls web -q)
    docker tag $IDIMG projecteinf/web
    docker push projecteinf/web
```

# Crear i executar contenidor a partir de la imatge publicada
```bash
    sudo docker build -t web SNMP/Contenidors/apache2/
    sudo docker run -d --name webcontainer -p 80:80 web
    sudo docker start webcontainer
```

# Peticions vàlides :-)
## Veure tots els OIDs
```bash
    snmpget -v2c -c public 172.17.0.2 .
```
## Veure un OID concret d'apache
```bash
    snmpget -v2c -c public 172.17.0.2 NET-SNMP-EXTEND-MIB::nsExtendOutLine.\"apache-status\".19

# Per a saber el OID concret d'apache-status
    snmptranslate -On NET-SNMP-EXTEND-MIB::nsExtendOutLine.\"apache-status\".19
```
