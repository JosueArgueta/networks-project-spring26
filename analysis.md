# RTT Analysis

## Q1 Highest Inefficiency Ratio
Sendai, Japan had the highest inefficiency ratio at 14.63x, with a 
measured RTT of 1534.2ms against a theoretical minimum of 104.9ms.
Seoul (11.41x), London-Uni (11.43x), New Delhi (11.31x), and 
Johannesburg (10.45x) were also flagged as high inefficiency (ratio > 3.0)

The university servers show dramatically higher ratios than the Google
targets because Google uses CDN edge servers near Boston, while university
servers actually route packets to their physical location. Sendai's high
ratio likely reflects congestion, multiple routing hops across the Pasific,
and the overhead of crossing several autonomous systems between the US
and Japan.

## Q2 Closest to Theoretical Minimum
frankfurt had the most realistic ratio at 1.61x, meaning its measured
RTT (95.0ms) was only 61% above the theoretical minimum (59.0ms). Lagos
was also reasonable at 1.15x. These results make sense both are 
relatively well-connected to North America through major transatlantic
cables and internet exchange points

The Google targets (Tokyo, Mumbai, Singapore, Sydney) showed ratios
below 1.0, which is physically impossible. This happened because Google's
CDN answered requests from a nearby Boston-area edge server rather than
routing all the way to those countries. This is actually evidence of
excellent infrastructure, Google's network is so optimized that geography
becomes irrelevant for its own properties.

## Q3 Why Lagos Routes Through Europe
Africa historically lacked direct submarine cable links to North America.
Most cables were funded by European telecom companies, connecting African
cities to Europe first. As a result, traffic between the US and Africa
transits through Euorpean internet exchange points, adding thousands of
kilometers of unnecessary distance. This is visible in my results
Lagos (8,243 km away) had a ratio of 1.15x, but Johannesburg (12,646 km)
had a ratio of 10.45x, suggesting South Africa's routing is even more
indirect. New cables like Equiano an