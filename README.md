#Transfer binaries through telnet without anything else available

A solution to transfer binaries to telnet host that don't have nor ssh nor ftp nor nc installed.

A bit hacky but it works.

In this repo you can find the following script:

* `shellcode_it.sh` convert a binary to shellcode and prints to standard output

```
Usage: shellcode_it.sh <binary>
```

* `telnet_transfer.py` transfer a shellcode to the telnet server while converting it to bin over-the-wire

```
Usage: telnet_transfer.py <host> <user> <password> <shellcode> <remote_location>
```
