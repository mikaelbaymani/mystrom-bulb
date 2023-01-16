#! /usr/bin/env python3


################################################################################
# Imports.
################################################################################
import aiohttp
import asyncio
################################################################################


class Colors:


    RED = 0
    YELLOW = 60
    GREEN = 120
    CYAN = 180
    BLUE = 240
    MAGENTA = 300

    # !class Colors


class Bulb:


    def __init__( self, ip : str = "192.168.1.199", mac : str = "CC50E3FACDAC" ):
        self._url = f"http://{ip}/api/v1/device/{mac}"
        self._mac = mac
        self._data = {}
        self._sess = None


    async def _request( self, method : str = "GET", *args, **kwargs ):
        if self._sess is None: self._sess = aiohttp.ClientSession()
        response = await self._sess.request( method, self._url, *args, **kwargs )
        return response


    async def close( self ):
        if self._sess: await self._sess.close()


    def is_on( self ): return self._data['on']


    async def on( self, action ): await self._request( "POST", data = "action=on" )


    async def off( self, action ): await self._request( "POST", data = "action=off" )


    def get_color( self ):
        hue, saturation, luminance = map( int, self._data["color"].split( ';' ) )
        return {"hue" : hue, "saturation" : saturation, "luminance" : luminance}


    async def set_color( self, hue, saturation, luminance ):
        data = f"action=on&color={hue};{saturation};{luminance}"
        await self._request( "POST", data = data )


    @property
    async def get_state( self ):
        response = await self._request()
        response = await response.json()
        self._data = response[self._mac]


    @property
    def get_report( self ): return self._data
    def __str__( self ): return str( self.get_report )

    # !class Bulb


async def main():

    bulb = Bulb()
    await bulb.get_state, print( bulb )

    is_on, color = bulb.is_on(), bulb.get_color()

    for i in range( Colors.RED, Colors.MAGENTA, 5 ):
        await bulb.set_color( i, 100, 60 )
        await asyncio.sleep( .150 )
        await bulb.set_color( i, 100, 100 )
        await asyncio.sleep( .150 )
        await bulb.get_state, print( f"Hue: {bulb.get_color()['hue']}" )

    await bulb.set_color( color["hue"], color["saturation"], color["luminance"] )
    await bulb.close()


if __name__ == "__main__": asyncio.run( main() )


# EOF
