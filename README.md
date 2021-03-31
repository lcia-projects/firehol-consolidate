# Louisiana Cyber Investigators Alliance
# Firehol-Consolidate

### Firehol IP Blocklists : http://iplists.firehol.org/
This IP list is a composition of other IP lists.
The objective is to create a blacklist that can be safe enough to be used on all systems, with a firewall, to block access entirely, from and to its listed IPs.
The key prerequisite for this cause, is to have no false positives. All IPs listed should be bad and should be blocked, without exceptions.
To accomplish this, we include the following IP lists:

- fullbogons - the unroutable IPs 
- spamhaus drop and edrop - Don't Route Or Peer IPs 
- dshield - the top 20 attacking class-C 
- malware lists - the Command and Control IPs 

This simple python script downloads the lists from the github, consolidates them into 
either a YAML or CSV file for use with elasticsearch/logstash or any other tool. 

you can run this script on a cron job every 4-6 hours to get updated blocklists then
apply them to your processing tools. 
