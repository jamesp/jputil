"""Uses the google charts API to generate a spakline for a list of numbers.

"""

def sparkline(data, size="140x40", colour="990000",):
    """Returns the url string for a sparkline of the given data list."""
    scaling = lambda x: float(x - min(data)) / (max(data) - min(data)) * 95.2
    data_list = ",".join(["%2.1f" % scaling(x) for x in data])
    return "http://chart.apis.google.com/chart?\
cht=lc&\
chs={sz}&\
chd=t:{dat}&chco={col}&\
chls=1,1,0\
&chm=o,{col},0,{last_id},4&chxt=r,x,y&\
chxs=0,{col},11,0,_|1,{col},1,0,_|2,{col},1,0,_&\
chxl=0:|{label}|1:||2:||&chxp=0,{last}".format(dat=data_list,col=colour,sz=size, \
last_id=len(data)-1,label=data[-1],last=str(scaling(data[-1])))

def download(url, destination):
    """Download a file at the given url and save at the given destination."""
    import urllib
    urllib.urlretrieve(url, destination)

if __name__ == '__main__':
    download(sparkline([1.4142,
    1.4003,
    1.397,
    1.3984,
    1.3924,
    1.3884,
    1.402 ,
    1.3947,
    1.3978,
    1.3967,
    1.4107,
    1.4148,
    1.4105,
    1.4231]), "/Users/jp/EUR.png")