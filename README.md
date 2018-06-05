=GCE UTILS=

Utilities inside a docker container to provide some functionality to GCE instances.

== dns-update ==

Update DNS zone with instance ip address

Usage:

```
docker run -it --rm --network=host splitmedialabs/gce-utils dns-update <PROJECT> <DNS_ZONE>
```
