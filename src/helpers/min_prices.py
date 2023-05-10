
from datetime import datetime

import pandasql as ps
import pandas as pd

from src import api


def from_vvo_mow_to_hkt() -> pd.DataFrame:

    vladivostok = api.get_table_aviasales(from_='VVO', to_='HKT')
    vladivostok['depart_date'] = vladivostok['depart_date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').date())
    
    moscow = api.get_table_aviasales(from_='MOW', to_='HKT')
    moscow['depart_date'] = moscow['depart_date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').date())

    lower = ps.sqldf(
        env={'vladivostok': vladivostok, 'moscow': moscow}, 
        query="""
            with 
            vladivostok20 as (select price, depart_date from vladivostok order by price limit 20),
            moscow20 as (select price, depart_date from moscow order by price limit 20)
            
            select 'vl' as "city", price, depart_date from vladivostok20
            union all
            select 'msc', price, depart_date from moscow20
            order by depart_date
        """
    )

    return lower