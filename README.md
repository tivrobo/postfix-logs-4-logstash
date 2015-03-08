# postfix-logs-4-logstash
monitor postfix log, wait for all pieces of queue log lifecycle, then output

You can use it with program input in syslog-ng or logsthash

### syslog-ng

source s_postfix { program ( "unbuffer /etc/postfix/postfix-tail.py" flags(no-parse) ); };

destination d_postfix { udp("log-server.example.com" port(5140) template( "${ISODATE} postfix: ${MSG}" ) ); };

log { source(s_postfix); destination(d_postfix); };

### sample output:

Mar  8 22:30:22 mxgate postfix/smtpd[22337]: C166280088: client=mail.server[123.123.123.123]; Mar  8 22:30:22 mxgate postfix/cleanup[22416]: C166280088: message-id=<1234567890@mailserver.local>; Mar  8 22:30:28 mxgate postfix/qmgr[21787]: C166280088: from=<someone@example.com>, size=4236, nrcpt=1 (queue active); Mar  8 22:30:29 mxgate postfix/smtp[22422]: C166280088: to=<someone@somewhere.out>, relay=relay.server[234.234.234.234]:25, delay=6.9, delays=6.2/0.01/0.13/0.6, dsn=2.0.0, status=sent (250 Requested mail action okay, completed: id=0Lub9E-1XV0VB2eUC-00zmjo); Mar  8 22:30:29 mxgate postfix/qmgr[21787]: C166280088: removed
