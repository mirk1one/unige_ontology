# Installazione del server Virtuoso di Unige per la gestione di linked data

## Tabella del contenuto

* [Introduzione](#introduzione)
* [Problema affrontato](#problema-affrontato)
* [Installazione tool per utilizzare la macchina virtuale](#installazione-tool-per-utilizzare-la-macchina-virtuale)
* [Installazione tools per utilizzare Virtuoso](#installazione-tools-per-utilizzare-virtuoso)
    * [Configurazione del repository](#configurazione-del-repository)
    * [Installazione di Docker Engine](#installazione-di-docker-engine)
    * [Installazione container Docker di Virtuoso](#installazione-container-docker-di-virtuoso)
* [Utilizzo di Virtuoso](#utilizzo-di-virtuoso)

## Introduzione

In questo progetto affronto la realizzazione di un database semantico per Unige, riportando una banca dati di linked data relativi agli edifici e ai dipartimenti delle università di Genova. Lo scopo è quello di installare un server permanente che contenga i dati semantici e dell API che, se richiamate, restituiscano i dati ricercati.

## Problema affrontato

Per utilizzare questo database di linked data, ho utilizzato come server Virtuoso Universal Server, ovvero un database ibrido che utilizza le funzionalità di un tradizionale sistema di gestione di database relazionali (RDBMS), database relazionale a oggetti (ORDBMS), database virtuale, RDF, XML, testo libero, server di applicazioni web e file server di funzionalità in un unico sistema.

Per utilizzarlo mi sono appoggiato ad una macchina remota con installato come SO Linux, collegandomi tramite SSH e un browser embedded tramite l'utilizzo di MobaXTerm.

Per la parte di creazione dei linked data da usare come dati per il database e per le API, ho utilizzato degli script Python creati tramite Visual Studio Code.

Per dettagli maggiori su ogni singola parte, consultare i capitoli successivi.

## Installazione tool per utilizzare la macchina virtuale

Per questo progetto è stata installata una macchina virtuale in Unige con sistema operativo Linux Ubuntu Focal, release 20.04 LTS, con memoria disco di circa 32 GB e RAM di circa 8 GB. Per collegarmi alla macchina ho usato il tool [MobaXTerm](https://mobaxterm.mobatek.net/), un toolbox per remote computing dove in una sola applicazione si possono utilizzare dei tools di remote network, browser SFTP, ecc.

Si suppone inizialmente che ci si possa collegare alla rete della macchina remota, in caso ci si trovasse esternamente basta installare come tool la VPN [GlobalProtect](https://globalprotect.updatestar.com/it) e collegarsi con i propri username e password.

Dopo averlo scaricato e installato ci troveremo davanti alla schermata successiva, nella quale avremo a disposizione differenti funzionalità, ma quella principale che ci interessa e la parte "Session" (inquadrato di verde nell'immagine).

![plot](./Images/MobaXTerm_1.jpg)

Aprendo questa sezione avremo la possibilità di aggiungere una sessione che rimarrà salvata all'interno. Particolarmente a noi interessano le seguenti:

1) Sessione di remote network (SSH).

2) Sessione di trasferimento e manipolazione dei dati (SFTP).

3) Sessione di embedded browser (Browser).

![plot](./Images/MobaXTerm_2.jpg)

Partendo dalla sessione SSH, basta crearla e impostare l'indirizzo della macchina (nel mio caso è stata impostata a 130.251.22.225) e lasciare impostata la porta a 22. Non necessariamente si deve specificare un utente, ma si potrebbe impostare e salvare all'interno del tool per non doverlo chiedere ogni volta che ci si connette.

![plot](./Images/MobaXTerm_3.jpg)

In seguito si crea una sessione SFTP, non necessaria ma che ci agevola nell'inserimento dei files remoti e nella loro modifica. Per farlo basta seguire gli stessi passaggi fatti per la sessione SSH.

![plot](./Images/MobaXTerm_4.jpg)

Come ultima parte, basta configurare l'embedded browser che ci servirà per gestire la parte di UI di Virtuoso. Basta creare una sessione browser e impostare l'url al quale vogliamo connetterci. In questo caso dipende dall'installazione di Virtuoso fatta, nel mio caso (come si può vedere nell'immagine successiva) ho utilizzato lo stesso indirizzo IP precedente e configurato il servizio di Virtuoso UI alla porta 8890 (se si seguono successivamente i passi fatti da me, allora si può configurare così).

![plot](./Images/MobaXTerm_5.jpg)

A questo punto è stato configurato tutto il necessario per potersi connettere alla macchina virtuale, ora bisognerà configurarla per poter utilizzare tutti i tool necessari per Virtuoso.

## Installazione tools per utilizzare Virtuoso

Per l'utilizzo di Virtuoso sulla macchina remota bisogna [installare Docker Engine](https://docs.docker.com/engine/install/ubuntu/) e in seguito creare il [container per Virtuoso](https://hub.docker.com/r/openlink/virtuoso-closedsource-8), in seguito vengono descritti tutti i passi fatti.

N.B.: tutti i passaggi successivi per l'installazione sono fatti tramite la sessione SSH della macchina virtuale configurata.

### Configurazione del repository

Per l'installazione di Docker Engine, si inizia aggiornando l'indice del pacchetto apt e installando i paccherri per consentire ad apt di un repositori tramite HTTPS:

```sh
$ sudo apt-get update
```

```sh
$ sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

In seguito si deve aggiungere la chiave GPG ufficiale di Docker:

```sh
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

Si deve utilizzare il comando seguente per configurare il repository stable. Per aggiungere il repository **nightly** o **test**, si deve aggiungere la parola `nightly` o `test` (o entrambi) dopo la parola `stable` nei comandi seguenti.

```sh
$ echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Installazione di Docker Engine

Inizialmente si aggiorna l'indice del pacchetto apt e si installa l'ultima versione di Docker Engine e di containerd, oppure si può andare al passaggio successivo per installare una versione specifica:

```sh
$ sudo apt-get update
```

```sh
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```

Se si vuole installare una versione specifica di Docker Engine:

- Si elencano tutte le versioni disponibili nel repository.

    ```sh
    $ apt-cache madison docker-ce
    ```

- Quindi si seleziona e installa uno dei risultati precedenti, utilizzando la `version string` dalla seconda colonna, ad esempio `5:18.09.1~3-0~ubuntu-xenial`.

    ```sh
    $ sudo apt-get install docker-ce=<VERSION_STRING> docker-ce-cli=<VERSION_STRING> containerd.io
    ```

- Infine si verifica se Docker Engine è stato installato correttamente eseguendo l'immagine `hello-world`.

    ```sh
    $ sudo docker run hello-world
    ```

    Questo comando scarica un'immagine di prova e la esegue in un contenitore. Quando il contenitore viene eseguito, stampa un messaggio ed esce.

Arrivati a questo punto, Docker Engine è stato installato ed è funzionante. Il gruppo Docker viene creato ma non vi vengono aggiunti utenti. Si deve usare `sudo` per eseguire i comandi Docker.

Il daemon Docker si collega a un socket Unix anziché a una porta TCP. Per impostazione predefinita, quel socket Unix è di proprietà dell'utente `root` e altri utenti possono accedervi solo utilizzando `sudo`. Il demone Docker viene sempre eseguito come utente `root`.

Se non si vuole anteporre `sudo` al comando `docker`, si deve creare un gruppo Unix chiamato `docker` ed si aggiungono utenti ad esso. All'avvio, il daemon Docker crea un socket Unix accessibile dai membri del gruppo `docker`.

Quindi per creare il gruppo `docker` e aggiungere un utente, basta seguire i seguenti passaggi:

- Creare il gruppo Docker.

    ```sh
    $ sudo groupadd docker
    ```

- Aggiungere il proprio utente al gruppo `docker`.

    ```sh
    $ sudo usermod -aG docker $USER
    ```

- Uscire ed accedere nuovamente in modo che l'appartenenza al tuo gruppo venga rivalutata.

    Dato che si esegue il test su una macchina virtuale, potrebbe essere necessario riavviare la macchina virtuale per rendere effettive le modifiche.

    In un ambiente Linux desktop come X Windows, disconnettersi completamente dalla sessione e quindi accedere nuovamente.

    Su Linux, si può anche eseguire il seguente comando per attivare le modifiche ai gruppi:

    ```sh
    $ newgrp docker
    ```

- Si verifica di poter eseguire i comandi `docker` senza l'utilizzo di `sudo`.

    ```sh
    $ docker run hello-world
    ```

    Se inizialmente si sono eseguiti i comandi Docker CLI utilizzando `sudo` prima di aggiungere l'utente al gruppo `docker`, si potrebbe visualizzare il seguente errore, che indica che la propria directory `~/.docker/` è stata creata con autorizzazioni errate a causa dei comandi `sudo`.

    ```
    WARNING: Error loading config file: /home/user/.docker/config.json -
    stat /home/user/.docker/config.json: permission denied
    ```

    Per risolvere questo problema, basta rimuovere la directory `~/.docker/` (viene ricreata automaticamente, ma tutte le impostazioni personalizzate vengono perse) oppure modificarne la proprietà e le autorizzazioni utilizzando i seguenti comandi:

    ```sh
    $ sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
    ```

    ```sh
    $ sudo chmod g+rwx "$HOME/.docker" -R
    ```

La maggior parte delle attuali distribuzioni Linux (RHEL, CentOS, Fedora, Debian, Ubuntu 16.04 e versioni successive) utilizzano `systemd` per gestire quali servizi vengono avviati all'avvio del sistema. Quindi se si vuole configurare che Docker si esegua automaticamente all'avvio, il servizio Docker è configurato per eseguirsi all'avvio per impostazione predefinita. Per avviare automaticamente Docker e Containerd all'avvio per altre distribuzioni, bisogna utilizzare i comandi seguenti:

```sh
$ sudo systemctl enable docker.service
```

```sh
$ sudo systemctl enable containerd.service
```

Per disabilitare questo comportamento, basta utilizzare invece `disable`.

```sh
$ sudo systemctl disable docker.service
```

```sh
$ sudo systemctl disable containerd.service
```

### Installazione container Docker di Virtuoso

Per installare Virtuoso come container di Docker, si seguono i passaggi successivi. Per questa parte si suppone che si siano seguiti tutti i passaggi precedenti, compreso nel non utilizzo di `sudo` nei commandi.

Si fa il download dell'immagine, trasferendo l'ultima immagine Docker di Virtuoso 8.3 sul proprio sistema locale, utilizzando il commando seguente:

```sh
$ docker pull openlink/virtuoso-closedsource-8
```

Per verificare la versione del binary Virtuoso, si può usare il seguente comando:

```sh
$ docker run openlink/virtuoso-closedsource-8 version
```

A questo punto si può creare un'istanza di Virtuoso, più precisamente ora si potrà creare l'istanza per gestire l'installazione di una istanza del db di Unige. Non è necessario impostare tutti i dati come in questa guida, ma può essere customizzata a seconda della propria scelta, comunque vengono elencati successivamente tutti i passaggi fatti per poter modificare a propria scelta i parametri di input.

Si eseguono i seguenti comandi per creare l'istanza Unige di Vituoso sulla macchina virtuale:

```sh
$ mkdir unige_virtdb
```

```sh
$ cd unige_virtdb
```

```sh
$ docker run \
    --name unige_virtdb \
    --interactive \
    --tty \
    --env DBA_PASSWORD=dba \
    --publish 1111:1111 \
    --publish  8890:8890 \
    --volume `pwd`:/database \
    openlink/virtuoso-closedsource-8:latest
```

Questi passaggi creeranno un nuovo database Virtuoso nella sottodirectory `unige_virtdb` e avvierà un'istanza Virtuoso con il server HTTP in ascolto sulla porta `8890` e il server di dati ODBC / JDBC / ADO.Net / OLE-DB / ISQL in ascolto sulla porta `1111`.

L'immagine docker è in esecuzione in foreground (con `-i` o `--interactive`), così si può vedere tutto quello che farà.

Ora si è in grado di contattare il server HTTP Virtuoso utilizzando il seguente URL:

```sh
http://localhost:8890/
```

La parte di connessione a Virtuoso viene descritta nei dettagli in seguito.

## Utilizzo di Virtuoso

Per utilizzare Virtuoso bisogna avere la possibilità di accederci da UI, quindi tramite l'utilizzo di un browser. Come già raccontato nell'ultima parte del capitolo "[Installazione tool per utilizzare la macchina virtuale](#installazione-tool-per-utilizzare-la-macchina-virtuale)", è stato configurato un browser embedded allo stesso URL del server HTTP di Virtuoso, come configurato nell'ultima parte di "[Installazione container Docker di Virtuoso](#installazione-container-docker-di-virtuoso)" , quindi basterà aprire una sessione da MobaXTerm e cliccando su quella creata per il browser, come si può vedere dall'immagine successiva, si arriverà alla schermata principale di Virtuoso.

![plot](./Images/MobaXTerm_6.jpg)