'''
Module to query data from CAMS radiation service API.
Info available [here](http://www.soda-pro.com/help/cams-services/cams-radiation-service/automatic-access#wget)
'''

import requests
import io
import pandas as pd

SERVER  = 'www.soda-is.com'
VERSION = '1.0.0'
VALID_TIMESTEPS = [1,15,60]

class CAMS_Client():
    
    def __init__(self, email, verbose=False):
        self.email   = email
        self.verbose = verbose
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
        
        self.start = start
        self.end   = end
        self.timestep  = timestep
        self.latitude  = latitude
        self.longitude = longitude
        self.altitude  = altitude
        self.format_cols = True
        self.iso_interval = _get_iso_interval(timestep)
        
        self._get_req_str()
        
        r = self._query_service()
        
        df = self._parse_request(r)
        
        if set_index:
            df = self._set_index(df)
        
        return df
        
    def _get_req_str(self):
        '''Get string for API call.'''
        
        _email = self.email.replace('@','%2540') 
        req_str  = "http://{}/service/".format(SERVER)
        req_str += "wps?Service=WPS&Request=Execute&Identifier=get_cams_radiation"
        req_str += "&version={}".format(VERSION)
        req_str += "&DataInputs=latitude={};longitude={};altitude={};".format(
            self.latitude, self.longitude, self.altitude)
        req_str += "date_begin={};date_end={};time_ref=UT;".format(
            self.start.strftime('%Y-%m-%d'), 
            (self.end - pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        )
        req_str += "summarization={};".format(self.iso_interval)
        req_str += "username={}".format(_email)
        req_str += "&RawDataOutput=irradiation"
        self.req_str = req_str
    
    def _query_service(self):
        '''Performs the request.get method and validates the status of the results.'''
        
        r = requests.get(self.req_str)
        
        if not r.ok:
            raise Exception('Request failed with status {}'.format(r.status))
            
        return r

    def _parse_request(self, r):
        '''Parses the request output into a pandas DataFrame'''
        
        data = io.StringIO(r.text.split('#')[-1])
        df = pd.read_csv(data, delimiter=';')
        
        if self.format_cols:
            df.columns = df.columns.str.lstrip().str.rstrip().str.replace(' ','_')
            df.drop('Observation_period', axis=1, inplace=True)
            
        return df

    def _set_index(self, df):
        '''Set pd.DatetimeIndex to dataframe.'''
        index = pd.DatetimeIndex(start=self.start, end=self.end, 
                                 freq=pd.Timedelta(minutes=self.timestep), 
                                 closed='left')
        
        df.set_index(index, inplace=True)      
  
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
    