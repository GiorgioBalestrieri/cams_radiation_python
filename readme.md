# CAMS Radiation Client

A Python client for the CAMS radiation service.

From the website:
> Copernicus Atmosphere Monitoring Service (CAMS) radiation service provides time series of Global, Direct, and Diffuse Irradiations on horizontal surface, and Direct Irradiation on normal plane (DNI) for the actual weather conditions as well as for clear-sky conditions. The geographical coverage is the field-of-view of the Meteosat satellite, roughly speaking Europe, Africa, Atlantic Ocean, Middle East (-66° to 66° in both latitudes and longitudes). Time coverage is 2004-02-01 up to 2 days ago. Data are available with a time step ranging from 1 min to 1 month. The number of automatic or manual requests is limited to 40 per day.

* Copernicus main page is available [here](https://atmosphere.copernicus.eu/)
* The service main page is available [here](http://www.soda-pro.com/web-services/radiation/cams-radiation-service)
* For info about the API, see [here](http://www.soda-pro.com/help/cams-services/cams-radiation-service/automatic-access#wget)
* For exampe scripts, see [here](http://www.soda-pro.com/help/automatic-access/examples-of-scripts)

The repo contains the main module and two example notebooks, illustrating how to query radiation data and how to obtain 
PV power production results through [pvlib](http://pvlib-python.readthedocs.io/en/latest).

__note__: CAMS radiation data are in __$wh/m^2$__, but libraries such as pvlib expect inputs in terms of power (for a number of good reasons), 
therefore it is necessary to scale the data when working with timesteps different than one hour.

## Dependencies

* `pandas`