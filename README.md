# polylabel-py
A pure python implementation of the polylabel algorithm originally 
found here: https://github.com/mapbox/polylabel

A fast algorithm for finding polygon pole of inaccessibility, the most 
distant internal point from the polygon outline (not to be confused with centroid).


## Python Usage
Currently assumes the given polygon is the exterior boundary.  Does not currently handle interior holes.
```
p = polylabel(polygon, precision=0.5)

```