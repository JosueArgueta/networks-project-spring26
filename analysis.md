# RTT Analysis

## Q1  Highest Inefficiency Ratio
Among the cities that were reachable, Lagos had the highest inefficiency 
ratio at 1.21, meaning my measured RTT (99.7ms) was 21% higher than the 
theoretical minimum (82.4ms). London and Frankfurt also showed high 
inefficiency ratios of 2.04 and 1.85 respectively, which makes sense 
since they are relatively close to Boston but still showed about 110ms RTTs.
Looking at submarinecablemap.com, Lagos is served by cables like ACE and
MainOne, but these connect Africa to Europe rather than directly to North
America. This means my packet from Boston to Lagos likely routed through
a European hub first, adding extra distance and explaining the higher
inefficiency compared to cities like Tokyo or Singapore. 
Sao Paulo was completely unreachable during my measurement, returning
100% packet loss across aall the probes

## Q2  Closest to Theoretical Minimum
Tokyo, Mumbai, Singapore, and Sydney all showed inefficiency ratios 
below 1.0 (0.87, 0.76, 0.67, and 0.68 respectively), which is physically 
impossible, you cannot have a measured RTT lower than the speed-of-light 
minimum. I think this happened because Google uses a globally distributed CDN 
(Content Delivery Network). When I sent a request to google.co.jp, Google 
did not route my packet all the way to Tokyo instead it was answered by 
a nearby edge server, likely in or around Boston. 

## Q3 Why Lagos Routes Through Europe
Africa historically lacked direct submarine cable links to North America.
Most cables were funded and built by European telecom companies, connecting
African coastal cities to Europe first. As a result, traffic between the
US and Africa still transits through European internet exchange points,
adding thousands of kilometers of unnecessary distance. This explains why
Lagos (8,243 km from Boston) had a higher inefficiency ratio than Tokyo
(10,794 km away), the routing path for Lagos is less direct despite the
shorter physical distance. New cables like Equiano and 2Africa are being
laid to connect Africa more directly, which should improve this over time.