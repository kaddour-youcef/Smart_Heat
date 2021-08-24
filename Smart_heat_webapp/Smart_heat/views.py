from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
import joblib
from Smart_heat.models import fichier
from .forms import FichierForm
import pandas as pd 
from pathlib import Path
import time
import matplotlib.pyplot as plt
import numpy

#import pour live graph
from datetime import datetime
import random

i = 1


def home(request):
    """Fonction redirect Home """
    
    if request.method == 'POST':
        
        form = FichierForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect('/fichier/')
       
    else:
          
        form = FichierForm()
        
        

    return render(request, "home.html", {'form': form})
    

def result(request):

    """ Fonction redirect resultat d'estimation manuel"""
    cls = joblib.load('final_model_rl.sav')
    
    lis = []
    
    lis.append(request.GET['METO'])
    lis.append(request.GET['OCC1'])
    lis.append(request.GET['OCC2'])
    lis.append(request.GET['TMP1'])
    lis.append(request.GET['TMP2'])
    lis.append(request.GET['TEH1'])
    lis.append(request.GET['TEH2'])
    
    
    ans = cls.predict([lis])
    
    print(lis)
    
    return render(request, "result.html", {'ans' :ans ,'lis' : lis})
    
    
def result2(request):
    """  """
    
    data = pd.read_csv(r'..\Smart_heat(project)\media\fichiers\datateste.csv')
    data_f = pd.DataFrame(data, columns=['Date/Time',
                                 'TZ1 WORK:Zone People Occupant Count [](TimeStep)',
                                 'TZ2 MISC:Zone People Occupant Count [](TimeStep)',
                                 'Environment:Site Outdoor Air Drybulb Temperature [C](TimeStep)',
                                 'TZ1 WORK:Zone Air Temperature [C](TimeStep)',
                                 'TZ2 MISC:Zone Air Temperature [C](TimeStep)',
                                 'TZ1 WORK:Zone Thermostat Heating Setpoint Temperature [C](TimeStep)',
                                 'TZ2 MISC:Zone Thermostat Heating Setpoint Temperature [C](TimeStep)',
                                 'Electricity:Facility [J](TimeStep) '])
    X2 = data_f[['Environment:Site Outdoor Air Drybulb Temperature [C](TimeStep)',
          'TZ1 WORK:Zone People Occupant Count [](TimeStep)',
          'TZ2 MISC:Zone People Occupant Count [](TimeStep)',
          'TZ1 WORK:Zone Air Temperature [C](TimeStep)',
          'TZ2 MISC:Zone Air Temperature [C](TimeStep)',
          'TZ1 WORK:Zone Thermostat Heating Setpoint Temperature [C](TimeStep)',
          'TZ2 MISC:Zone Thermostat Heating Setpoint Temperature [C](TimeStep)']]
          
    cls = joblib.load('final_model_rl.sav')
    fig = plt.gcf()
    plt.xlabel('time (15 min)')
    plt.ylabel('Conso Energetique [J]')
    fig.show()
    fig.canvas.draw()
    time.sleep(0.001)
    
    
    for i, row in X2.iterrows():
        meto = row[0]
        occ1 = row[1]  
        occ2 = row[2] 
        tmp1 = row[3]
        tmp2 = row[4]
        teh1 = row[5]
        teh2 = row[6]
        
        lis = []
        
        lis.append(meto)
        lis.append(occ1)
        lis.append(occ2)
        lis.append(tmp1)
        lis.append(tmp2)
        lis.append(teh1)
        lis.append(teh2)
    
        ans = cls.predict([lis])
        print(ans)
        
        plt.scatter(i, ans, color='red')
        
        plt.pause(0.001)
        
        fig.canvas.draw()
        
        
        time.sleep(0.05)


    return render(request, "result2.html")
    




#live graph
def show_graph(request,template_name='live_graph.html'):
    return render(request,template_name)
#live graph
def show_graph2(request,template_name='live_graph2.html'):
    return render(request,template_name)
    

def Lin_R(data):
    """ Linear Regression Model"""
    LR = joblib.load('final_model_lr.sav')
    ans = LR.predict(data)
    return  ans.item()
    
def knn_R(data):
    """ KNN Regression Model """
    LR = joblib.load('final_model_knn.sav')
    ans = LR.predict(data)
    return  ans.item()

def bay_R(data):
    """ Bayesian Regression Model"""
    LR = joblib.load('final_model_bay.sav')
    ans = LR.predict(data)
    return  ans.item()
    
def List_ADD(meto, occ1, occ2, temp1, temp2, thm1, thm2):
    """Constitution d'une liste a donnée au modèle"""
    lis = []
    
    lis.append(meto)
    lis.append(occ1)
    lis.append(occ2)
    lis.append(temp1)
    lis.append(temp2)
    lis.append(thm1)
    lis.append(thm2)
    
    return  [lis]
    
def Extract_data(request):
    """ Extraction des données pour les sénario intérne"""
    num = request.session.get('num')
    if num is None:
      num = 1
    if num >= 672 : 
      num = 0
    request.session['num'] = num+1
    data2 = pd.read_csv(r'..\Smart_heat(project)\media\fichiers\datateste.csv')
    data_f = pd.DataFrame(data2, columns=['Date/Time',
                                 'TZ1 WORK:Zone People Occupant Count [](TimeStep)',
                                 'TZ2 MISC:Zone People Occupant Count [](TimeStep)',
                                 'Environment:Site Outdoor Air Drybulb Temperature [C](TimeStep)',
                                 'TZ1 WORK:Zone Air Temperature [C](TimeStep)',
                                 'TZ2 MISC:Zone Air Temperature [C](TimeStep)',
                                 'TZ1 WORK:Zone Thermostat Heating Setpoint Temperature [C](TimeStep)',
                                 'TZ2 MISC:Zone Thermostat Heating Setpoint Temperature [C](TimeStep)',
                                 'Electricity:Facility [J](TimeStep) '])
                                
    data_x = data_f['Electricity:Facility [J](TimeStep) '].to_numpy() 
    data_m = data_f['Environment:Site Outdoor Air Drybulb Temperature [C](TimeStep)'].to_numpy()
    data_temp1 = data_f['TZ1 WORK:Zone Air Temperature [C](TimeStep)'].to_numpy()
    data_temp2 = data_f['TZ2 MISC:Zone Air Temperature [C](TimeStep)'].to_numpy()
    data_occ1 = data_f['TZ1 WORK:Zone People Occupant Count [](TimeStep)'].to_numpy()
    data_occ2 = data_f['TZ1 WORK:Zone People Occupant Count [](TimeStep)'].to_numpy()
    data_thm1 = data_f['TZ1 WORK:Zone Thermostat Heating Setpoint Temperature [C](TimeStep)'].to_numpy()
    data_thm2 = data_f['TZ2 MISC:Zone Thermostat Heating Setpoint Temperature [C](TimeStep)'].to_numpy()
    data_t = data_f['Date/Time'].to_numpy()
    
    lis= List_ADD( data_m[num], data_occ1[num], data_occ2[num], data_temp1[num], data_temp2[num],
                    data_thm1[num], data_thm2[num])

    return (data_m[num], data_occ1[num], data_occ2[num], data_temp1[num], data_temp2[num], data_thm1[num], data_thm2[num], data_x[num], data_t[num], lis)
    
def data_choice(i, request):
    """ choix de la donné a afficher """
    data_fetch =0
    meto, occ1, occ2, temp1, temp2, thm1, thm2, Eng, dat, lis= Extract_data(request)
    
    if(i == '1'): 
        data_fetch = Lin_R(lis)
        
    elif(i== '2'):
        data_fetch = meto
    elif(i== '3'):
        data_fetch = temp1
    elif(i== '4'):
        data_fetch = temp2
    elif(i== '5'):
        data_fetch = occ1
    elif(i== '6'):
        data_fetch = occ2
    elif(i== '7'):
        data_fetch = thm1
    elif(i== '8'):
        data_fetch = thm2
    elif(i== '9'):
        data_fetch = Eng
    elif(i== '12'):
        data_fetch = bay_R(lis)
    elif(i== '13'):
        data_fetch = knn_R(lis)
        
    #ajouter des conditions pour ajouter des models 
    

    return  (str(data_fetch), str(dat))
    
    
def fetch_sensor_values_ajax(request):

    """ fonction qui traite les http request et renvoi les données approprier"""
    data1= {}
    
    
    if request.is_ajax():
            
            com_port = request.GET.get('id', None)
            print(com_port)
            sen_data=[]
             
            sen_val, ok_date = data_choice(com_port, request)
            
            try:
                
                if(sen_val):
                    sen_data.append(sen_val+','+ok_date)
                else:
                    sen_data.append(sen_val+','+ok_date)
            except Exception as e:
                    sen_data.append(sen_val+','+ok_date)
            data1['result']= sen_data
    else:
        data1['result']='Not Ajax'
    return JsonResponse(data1)
    
    
def fetch_sensor_values_ajax2(request):

    """ fonction qui traite les http request et renvoi les données approprier en réel avec les capteurs"""
    data= {}
    
    
    if request.is_ajax():
            
            com_port = request.GET.get('id', None)
            print(com_port)
            sensor_data=[]
            
            now=datetime.now()
            ok_date=str(now.strftime('%Y-%m-%d %H:%M:%S'))   
            sensor_val, ok_date = data_choice(com_port, request)
            
            try:
                
                #a modifier selon l'entré des capteurs 
                sr=serial.Serial("COM9",9600)
                st=list(str(sr.readline(),'utf-8'))
                sr.close()
                sensor_val=str(''.join(st[:]))
                
                if(sensor_val):
                    sensor_data.append(sensor_val+','+ok_date)
                else:
                    sensor_data.append(sensor_val+','+ok_date)
            except Exception as e:
                    sensor_data.append(sensor_val+','+ok_date)
            data1['result']=sensor_data
    else:
        data1['result']='Not Ajax'
    return JsonResponse(data1)
    
# by youcef kaddour
