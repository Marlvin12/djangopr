from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from pandas.io import json
from .models import Data

# Create your views here.
def hello(request):
    if request.method == 'POST':
        previous_data=Data.objects.all()
        previous_data.delete()
        file=(request.FILES['file'])
        df = pd.read_csv(file)
        json_records = df.reset_index().to_json(orient='records')
        data=[]
        data = json.loads(json_records)
        for d in data:
            name=d['property_name']
            price =d['property_price']
            rent=d['property_rent']
            emi=d['emi']
            tax=d['tax']
            exp=d['other_exp']
            expenses_monthly = emi+tax+exp
            income_monthly=rent-expenses_monthly
            dt=Data(name=name,price=price,rent=rent,emi=emi,tax=tax,exp=exp, expenses_monthly=
                    expenses_monthly,income_monthly=income_monthly)
            dt.save()
        data_objects=Data.objects.all()
        context = {'data_objects':data_objects}
        return render(request,'myapp/index.html',context)
    else:
        print("This is a get request")
    return render(request, 'myapp/index.html')
