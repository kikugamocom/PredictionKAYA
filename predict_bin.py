#-*- coding:utf-8 -*-
import tensorflow as tf
import pandas as pd
import arrow
import pyrebase

#Secrets
config = {

}

#Secrets
email = 
password = 

model_dir = r'C:\Users\Rasta\AppData\Local\Programs\Python\Python35\Scripts\jupyter-Test\model9'


class Bin_predict():
    FEATURES = ('hod','current_lv','min_diff','tf_id','dow') #'dow'
    LABLE = 'interesting_lv'
    HIDDEN_UNITS = [7, 7, 7]


    """docstring for Bin_predict"""
    def __init__(self, model_dir=model_dir, model_settings=None):
        super(Bin_predict, self).__init__()
        
        # setup tf estimator
        self.estimator = tf.contrib.learn.DNNRegressor(
                    feature_columns=[tf.contrib.layers.real_valued_column(k) for k in self.FEATURES],
                    hidden_units=self.HIDDEN_UNITS,
                    model_dir=model_dir
        )

        # setup Firebase
        firebase = pyrebase.initialize_app(config)
        self.auth = firebase.auth()
        self.db = firebase.database()

        # load id_mapper from Google sheets
        self.id_mapper = self.load_tf_sensor_id_mapper()

    def data_init(self, data_set):
        feature_cols = {k: tf.constant(data_set[k].values) for k in self.FEATURES}
        if not self.LABLE in data_set:
            lables = None
        else:
            lables = tf.constant(data_set[self.LABLE].values)
        return feature_cols, lables

    def predict_lv(self, sensor_id, target_time):

        # get current bin info        
        current_lv = self.get_current_volume(sensor_id)
        if current_lv == -1:
            # no this sensor info!
            return -1
        elif current_lv == -2:
            return -2
        qry_time = arrow.get(target_time)   # TODO check weather qry time is more than now?
        tf_id = self.id_mapper[sensor_id]['tf_id']
        now = arrow.now()

        # if qry_time < now:
        #     return "error"


        df = pd.DataFrame(
            {  
                'tf_id': [tf_id] ,
                'current_lv': [current_lv],
                'min_diff': [round((qry_time - now).total_seconds()/60)], 
                'hod' : [now.hour],     
                'dow': [arrow.now().weekday()]
            }
        )

        y_predict = self.estimator.predict(input_fn=lambda: self.data_init(df), as_iterable=False)
        if y_predict > 100:
            y_predict = 100
            return y_predict
        return float(y_predict[0]) if len(y_predict) == 1 else -1 

    def load_tf_sensor_id_mapper(self):
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
            credential_path = os.path.join(credential_dir,'sheets.googleapis.com-python-quickstart.json')
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
        rangeName = 'TF_mapper!A2:D'
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
                is_learned = row[3]
                sensor_mapper[sensor_id] = {}
                sensor_mapper[sensor_id]['tf_id']= int(tensor_flow_id)
                sensor_mapper[sensor_id]['is_learned'] = is_learned=='1'
        return sensor_mapper


    def get_current_volume(self, sensor_id):
        found = False
        level = -1
        learn = False
     
        user = self.auth.sign_in_with_email_and_password(email, password)   # sign-in
        bin_info = self.db.child('kaya/bin').get(user['idToken'])
        bin_info = bin_info.val()
        
        for key in bin_info.keys():
            if found:
                break
            if 'node'  not in bin_info[key]:
                ss_id = bin_info[key]['sensor']['id']
                learn =  self.id_mapper[ss_id]['is_learned']
              
                if sensor_id == ss_id:
                    found = True
                    level =  bin_info[key]['sensor']['volume_percentage']
                    break
            else:
                for a in bin_info[key]['node']:
                    ss_id = bin_info[key]['node'][a]['sensor']['id']
                    learn =  self.id_mapper[ss_id]['is_learned']
                   
                    if sensor_id == ss_id:
                        found = True
                        level =  bin_info[key]['node'][a]['sensor']['volume_percentage']
                        break
        if not found: 
            print('The sensor_id is not found!')
            return -1
        if not learn: 
            print('There is no learned model!')
            return -2
            
        return level