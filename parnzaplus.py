import tensorflow as tf
import glob
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from IPython.display import display, HTML
from sklearn.metrics import mean_squared_error
from math import sqrt
from google.cloud import bigquery


MODEL_NAME = 'model8'

def parneiei():



	def load_tf_sensor_id_mapper():
	    import httplib2
	    import os

	    from apiclient import discovery
	    from oauth2client import client
	    from oauth2client import tools
	    from oauth2client.file import Storage

	    # If modifying these scopes, delete your previously saved credentials
	    # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
	    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
	    CLIENT_SECRET_FILE = r'C:\git download\instruction_media\Python for prediction\example\data\client_secret.json'
	    APPLICATION_NAME = 'Google Sheets API Python Quickstart'


	    def get_credentials():
	        """Gets valid user credentials from storage.

	        If nothing has been stored, or if the stored credentials are invalid,
	        the OAuth2 flow is completed to obtain the new credentials.

	        Returns:
	            Credentials, the obtained credential.
	        """
	        home_dir = os.path.expanduser('~')
	        credential_dir = os.path.join(home_dir, '.credentials')
	        if not os.path.exists(credential_dir):
	            os.makedirs(credential_dir)
	        credential_path = os.path.join(credential_dir,
	                                       'sheets.googleapis.com-python-quickstart.json')

	        store = Storage(credential_path)
	        credentials = store.get()
	        if not credentials or credentials.invalid:
	            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
	            flow.user_agent = APPLICATION_NAME
	            if flags:
	                credentials = tools.run_flow(flow, store, flags)
	            else: # Needed only for compatibility with Python 2.6
	                credentials = tools.run(flow, store)
	            print('Storing credentials to ' + credential_path)
	        return credentials
	    
	    credentials = get_credentials()
	    http = credentials.authorize(httplib2.Http())
	    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
	                    'version=v4')
	    service = discovery.build('sheets', 'v4', http=http,
	                              discoveryServiceUrl=discoveryUrl)

	    spreadsheetId = '1RzpNKzVJDJI4MmzS8bQo-72xDsSXu_yJ5euSXJ9GgXY'
	    rangeName = 'TF_mapper!A2:C'
	    result = service.spreadsheets().values().get(
	        spreadsheetId=spreadsheetId, range=rangeName).execute()
	    values = result.get('values', [])

	    sensor_mapper = {}
	    if not values:
	        print('No data found.')
	    else:
	        for row in values:
	            # Print columns B and C, which correspond to indices 1 and 2.
	            sensor_id = row[1]
	            tensor_flow_id = row[2]
	            sensor_mapper[sensor_id] = int(tensor_flow_id)
	    return   sensor_mapper



	   #Secrets
	bq_client = bigquery.Client.from_service_account_json('')

		#Secrets
	query_string = ''
	query_job = bq_client.query(query_string)

	#print(query_job.to_dataframe)
	results = query_job.result()
	datas = []
	date = []
	sensor_id = []
	for row in results:
	    #print(row.temperature_c,row.distance_cm)
	    datas.append(row.distance_cm)
	    date.append(row.log_timestamp)
	    sensor_id.append(row.bin_id)




	df = pd.DataFrame({'LV': datas,
	                              'DATE': date,
	                               'SENSOR_ID':sensor_id
	                 })



	df = df.loc[(df['LV'] < 100) & (df['LV'] > 0)]

	SENSOR_MAPPER = load_tf_sensor_id_mapper()

	sensor_id_tf = []
	for _, row in df.iterrows():
	    sensor_id_tf.append(
	        SENSOR_MAPPER[str(row.SENSOR_ID)]
	    )

	df['sensor_id_tf'] = sensor_id_tf

	df['HOD'] = [date.hour for date in df['DATE']]
	df.sort_values('DATE', inplace=True, ascending=True)
	df = df.reset_index(drop=True)

	dow = []
	for ii in df['DATE']:
	    dow.append(ii.dayofweek)


	df['wod'] = dow

	df['volume_percentage'] = 100-(df['LV']-20)/(113-20)*100


	# group into sensor ids
	sensor_grp = df.groupby('sensor_id_tf')


	threshold = 5
	rounded_dfs = []
	# loop for each group and  divided in to rounds
	for sensor_id_tf, ss_df in sensor_grp:   
	    started = False  
	    range_idxs = []
	    for i in range(1,len(ss_df)):
	        current_lv = ss_df.iloc[i].volume_percentage
	        prev_lv = ss_df.iloc[i-1].volume_percentage
	        diff = current_lv - prev_lv
	        
	        if not started:
	            if  diff > 0:
	                start = i-1
	                started = True
	        
	        elif diff <= -threshold:
	            end = i-1
	            if ss_df.iloc[start].volume_percentage < ss_df.iloc[end].volume_percentage:                    
	                range_idxs.append({'start': start, 'end': end})
	            started = False
	            
	    # create new sensor df    
	    _date = []
	    _level = []
	    _round = []
	    _hod = []
	    _wod = []
	    for i in range(len(range_idxs)):
	        lvs = ss_df.iloc[ range_idxs[i]['start']: range_idxs[i]['end'] ].volume_percentage
	        times = ss_df.iloc[ range_idxs[i]['start']: range_idxs[i]['end'] ].DATE
	        hours = ss_df.iloc[ range_idxs[i]['start']: range_idxs[i]['end'] ].HOD
	        wods = ss_df.iloc[ range_idxs[i]['start']: range_idxs[i]['end'] ].wod
	        
	        _rnd = [i]*len(times)             
	        _round.extend(_rnd)
	        _date.extend(times)
	        _level.extend(lvs)
	        _hod.extend(hours)
	        _wod.extend(wods)
	        
	    rounded_dfs.append(
	        pd.DataFrame({
	                'sensor_id_tf': [sensor_id_tf]*len(_date),
	                'date' :  _date,
	                'level':  _level,
	                'round': _round,
	                'hod': _hod,
	                'wod': _wod
	            })
	    )



	df2 =  pd.concat(rounded_dfs)
	df2_grp = df2.groupby('sensor_id_tf')



	_date = []                                       
	_level = []
	_round = []
	_hod = []
	_min_diff = []
	_interesting_lv = []
	_ssid = []
	_wodss = []
	for sensorid, data in df2_grp: ## เก็บแต่ละเซ็นเซอร์
	    df2_g = data.groupby('round')
	    for rnd, df_round in df2_g:
	        for i in range(len(df_round)):
	            for j in range(i+1, len(df_round)):
	                b = df_round.iloc[i]['date']
	                a = df_round.iloc[j]['date']
	                min_diff = int((a  - b).total_seconds()/60)
	                sensor_id = sensorid 
	                _date.append( df_round.iloc[i]['date'])
	                _level.append( df_round.iloc[i]['level'] )
	                _hod.append(df_round.iloc[i]['hod'])
	                _min_diff.append(min_diff)
	                _interesting_lv.append(df_round.iloc[j]['level'])
	                _wodss.append(df_round.iloc[i]['wod'])
	                _ssid.append(sensor_id)
	    #break




	d3 = {
	        'date' :  _date,
	        'hod' :  _hod,
	        'level':  _level,
	        'min_diff': _min_diff,
	        'interesting_lv': _interesting_lv,
	        'sensor_id': _ssid,
	        'wod':_wodss
	     }


	df3 = pd.DataFrame(d3)

	#Split train / test data (70:30%)

	train_df = df3.iloc[:round(len(df3)*.7)]
	test_df = df3.iloc[round(len(df3)*.7)+1:]

	FEATURES = df3.columns[~df3.columns.isin(['date', 'interesting_lv'])].tolist()
	LABLE = 'interesting_lv'


	#input data

	def data_init(data_set):
	    feature_cols = {k: tf.constant(data_set[k].values) for k in FEATURES}
	    lables = tf.constant(data_set[LABLE].values)
	    return feature_cols, lables


	# Initializes a DNNRegressor instance with 2 hidden layer, each 4 nodes
	# Create DNN model and train 

	estimator = tf.contrib.learn.DNNRegressor(
	                    feature_columns=[tf.contrib.layers.real_valued_column(k) for k in FEATURES],
	                    hidden_units=[7,7,7],
	                    model_dir=MODEL_NAME
	)

	    # training
	estimator.fit(input_fn=lambda: data_init(train_df), max_steps=5000)#Predict

	#Predict

	y_predict = estimator.predict(input_fn=lambda: data_init(test_df), as_iterable=False)

	#Evaluate

	y_test = test_df[LABLE].values
	mae = np.mean([abs(true-predict) for true,predict in zip(y_test, y_predict)])
	rmse = sqrt(mean_squared_error(y_test, y_predict))
	mape = np.mean([abs(true-predict)/true for true,predict in zip(y_test, y_predict)])* 100

	print('# of data: \t\t\t%d' % len(y_test))
	print('Mean absolute error (MAE): \t\t\t%.2f %%' % mae)
	print('Root mean square error (RMSE): \t\t%.2f %%' % rmse)
	print('Mean absolute percentage error (MAPE): \t%.2f %%' % mape)
