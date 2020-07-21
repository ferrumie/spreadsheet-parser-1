import os
import json
import pandas as pd
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsOwnerOrReadOnly
from rest_framework_jwt.settings import api_settings
import datetime
# Create your views here.


payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

load_dotenv()


class ExcelAPIView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def post(self, request):
        # print('.>>>>>', request.GET.get('q', None))
        api_key = os.getenv('API_KEY')
        user_api_key = request.data.get('API_KEY')
        if api_key == user_api_key:
            file_path = request.data.get('file_path')
            column = request.data.get('column')
            if file_path and column:
                df = pd.read_excel(file_path, encoding='utf-8', )
                data = df.dropna(axis=0, how='any')
                loc = data.loc[column-1:]
                final_data = loc.to_dict(orient='records')

                return Response(json.loads(json.dumps(final_data)), status=status.HTTP_200_OK)
            if file_path:
                df = pd.read_excel(file_path, encoding='utf-8', )
                data = df.dropna(axis=0, how='any')
                data.columns = data.columns.map(lambda x: str(x))
                data.columns = data.columns.map(lambda x: x.replace('\n', ''))
                final_data = data.to_dict(orient='records')

                return Response(json.loads(json.dumps(final_data)), status=status.HTTP_200_OK)
                
            else:
                return Response({'error': 'file path can not be empty'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'you are not authorized to perform this action.'},
                            status=status.HTTP_401_UNAUTHORIZED)

# {"file_path":"https://file-examples-com.github.io/uploads/2017/02/file_example_XLSX_10.xlsx","API_KEY":"whatiftheworldendstodayum"}
# {"file_path":"https://file-examples-com.github.io/uploads/2017/02/file_example_XLSX_10.xlsx","from":2,"to":7,"API_KEY":"whatiftheworldendstodayum"}

class dailyAPIView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    
    def post(self, request):
        if request.method == 'POST':
            api_key = os.getenv('API_KEY')
            user_api_key = request.data.get('API_KEY')
            if api_key == user_api_key:
                file_path = request.data.get('file_path')
                row_from = request.data.get('from')
                row_to = request.data.get('to')
                if file_path and row_from and row_to:
                    data = pd.read_excel(file_path, sheet_name=0)
                    data1 = data.dropna(axis=0, how='all', thresh=3)
                    data2 = data1.dropna(axis=1, how='all')
                    new = data2.loc[data.isnull().mean(axis=1).lt(0.5)]
                    new2 = new[new.columns[new.isnull().mean()<0.5]]

                    if 'Unnamed: 2' in new2.columns:
                        new_header = new2.iloc[0]
                        new2.columns = new_header
                        if "-" in new2.columns:
                            new_header = new2.iloc[1]
                            new2.columns = new_header
                        new2 = new2[1:]
                    new2 = new2.fillna('').reset_index(drop = True)
                    new3 = new2.loc[row_from:row_to]
                    daily_expenses = new3.to_dict(orient='records')
                    ohh = json.dumps(daily_expenses)
                    real_data = json.loads(ohh)
                    return Response(real_data, status= status.HTTP_200_OK)

                elif file_path and row_from:
                    data = pd.read_excel(file_path, sheet_name=0)
                   
                    data1 = data.dropna(axis=0, how='all', thresh=3)
                    
                    data2 = data1.dropna(axis=1, how='all')                 
                    new = data2.loc[data.isnull().mean(axis=1).lt(0.5)]
                    new2 = new[new.columns[new.isnull().mean()<0.5]]

                    if 'Unnamed: 2' in new2.columns:
                        new_header = new2.iloc[0]
                        new2.columns = new_header
                        if "-" in new2.columns:
                            new_header = new2.iloc[1]
                            new2.columns = new_header                           
                        new2 = new2[1:]
                    new2 = new2.fillna('').reset_index(drop = True)
                    new3 = new2.loc[row_from:]
                    daily_expenses = new3.to_dict(orient='records')
                    ohh = json.dumps(daily_expenses)
                    real_data2 = json.loads(ohh)
                    return Response(real_data2, status= status.HTTP_200_OK)
                elif file_path:
                    data = pd.read_excel(file_path, sheet_name=0)
                   
                    data1 = data.dropna(axis=0, how='all', thresh=3)
                    
                    data2 = data1.dropna(axis=1, how='all')
                                        
                    new = data2.loc[data.isnull().mean(axis=1).lt(0.5)]
                    new2 = new[new.columns[new.isnull().mean()<0.5]]
                    if 'Unnamed: 2' in new2.columns:

                        new_header = new2.iloc[0]
                        new2.columns = new_header
                        if "-" in new2.columns:
                            new_header = new2.iloc[1]
                            new2.columns = new_header
                           
                        new2 = new2[1:]
                    new2 = new2.fillna('').reindex()
                    daily_expenses = new2.to_dict(orient='records')
                    ohh = json.dumps(daily_expenses)
                    real_data2 = json.loads(ohh)
                    return Response(real_data2, status= status.HTTP_200_OK)

                else:
                    return Response({'error': 'file path can not be empty'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'you are not authorized to perform this action.'},
                                status=status.HTTP_401_UNAUTHORIZED)


#{"file_path":"https://fgn-web-crawler.herokuapp.com/static/expense/2020/01_02_2020.xlsx","API_KEY":"whatiftheworldendstodayum"}
#{"file_path":"https://opentreasury.gov.ng/images/2020/DAILYPAYMENT/JULY/04-07-20.xlsx","API_KEY":"whatiftheworldendstodayum"}
# {"file_path":"https://opentreasury.gov.ng/images/2020/DAILYPAYMENT/MARCH/11-03-20.xlsx","API_KEY":"whatiftheworldendstodayum"}
# {"file_path":"https://opentreasury.gov.ng/images/2020/MONTHLYBUDPERF/FGN/ADMIN/FEB.xlsx","API_KEY":"whatiftheworldendstodayum"}