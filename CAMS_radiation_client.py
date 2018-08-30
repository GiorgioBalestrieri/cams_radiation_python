'''
Module to query data from CAMS radiation service API.
Info available [here](http://www.soda-pro.com/help/cams-services/cams-radiation-service/automatic-access#wget)
'''

import requests
import io
import pandas as pd

BASE_URL  = 'http://www.soda-is.com/service/wps'
VERSION   = '1.0.0'
VALID_TIMESTEPS = [1,15,60]

class CAMS_Client():
    
    def __init__(self, email, verbose=False, base_url=BASE_URL):
        self.email    = email
        self.verbose  = verbose
        self.base_url = base_url
        if self.verbose:
            print('Initiated CAMS Client with user {}', self.email)
    
    
    def query_radiation_service(self, start, end, timestep, 
                                latitude, longitude, altitude=0, 
                                format_cols=True, set_index=True):
        '''
        Args:
        ------
        - start:        dt or pd .datetime (included) 
        - end:          dt or pd .datetime (excluded) 
        - timestep:     int, timestep in minutes
        - latitude, longitude, altitude: int or float
        - format_cols:  remove spacing
        '''
        iso_interval = _get_iso_interval(timestep)
        
        params = {
            'Service': 'WPS',
            'Request': 'Execute',
            'Identifier': 'get_cams_radiation',
            'version': VERSION,
            'DataInputs': {
                'latitude': self.latitude,
                'longitude': longitude,
                'altitude': altitude,
                'date_begin': start.strftime(TIME_FORMAT),
                'date_end': (end - pd.Timedelta(days=1)).strftime(TIME_FORMAT),
                'time_ref': 'UT',
                'summarization': iso_interval,
                'username': email.replace('@','%2540')
            },
            RawDataOutput: 'radiation'
        }
        
        r = requests.get(self.base_url, params=params)
        if not r.ok:
            raise Exception('Request failed with status {}'.format(r.status))
        
        df = self._parse_request(r)
        if format_cols:
            df = _format_cols(df)
        if set_index:
            df = _set_index(df, start, end, timestep)
        
        return df


def _get_iso_interval(timestep):
    '''
    From timestep (minutes) to ISO8601 interval.
    See https://pypi.org/project/isodate/ for a proper solution.
    '''
    assert timestep in VALID_TIMESTEPS, \
        'timestep must be in {}'.format(VALID_TIMESTEPS)
    
    if timestep % 60 == 0:
        iso_interval = 'PT{:02.0f}H'.format(timestep/60)
    else:
        iso_interval = 'PT{:02.0f}M'.format(timestep)
    return iso_interval


def _parse_request(r):
    '''Parses the request output into a pandas DataFrame'''
    data = io.StringIO(r.text.split('#')[-1])
    df = pd.read_csv(data, delimiter=';')
    return df


def _format_cols(df)
    df.drop('Observation_period', axis=1, inplace=True)
    return df
    
    
def _set_index(df, start, end, timestep)
    index = pd.DatetimeIndex(start=start, end=end, 
                             freq=pd.Timedelta(minutes=timestep), 
                             closed='left')
    df.set_index(index, inplace=True)  
    return df
    