# polylabel-py
1. fork from others 
2. support python3.6 主要修改了python2支持但是python3不支持的Queue的模块名字 range不能够直接相加
3. 修改了 class Cell 没有重载运算符'<'的错误
#polylabel
A pure python implementation of the polylabel algorithm originally found here: https://github.com/mapbox/polylabel

A fast algorithm for finding polygon pole of inaccessibility, the most 
distant internal point from the polygon outline (not to be confused with centroid).


## Python Usage
Currently assumes the given polygon is the exterior boundary.  Does not currently handle interior holes.
```
p = polylabel(polygon, precision=0.5)

```