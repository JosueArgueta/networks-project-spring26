# RTT Analysis

## Q1  Highest Inefficiency Ratio
Lagos has the highest inefficiency ratio (1.21) among reachable cities.
Looking at submarinecablemap.com, Lagos is served by cables like ACE and
MainOne, but these cables connect Africa to Europe rather than directly
to North America. This means a packet from Boston to Lagos likely routes
through a European hub first, adding extra distance and latency.

## Q2  Closest to Theoretical Minimum
Sydney and Singapore have measured RTTs very close to (or below) their
theoretical minimums. This is most likely because Google serves these
requests from a CDN edge node near Boston rather than routing all the
way to Australia or Singapore. It shows that Google's infrastructure
is highly optimized and geographically distributed.

## Q3 Why Lagos Routes Through Europe
Africa historically lacked direct submarine cable links to North America.
Most cables were built connecting African coastal cities to Europe first,
since European telecom companies funded the infrastructure. As a result,
traffic between the US and Africa still transits through European internet
exchange points. To fix this, new direct cables like the proposed
Equiano and 2Africa cables are being laid to connect Africa more directly
to the rest of the world.