import os
import shutil
from django.shortcuts import render
import datetime
import locale
locale.setlocale(locale.LC_ALL,'es_cl')
archivo_ventas="/home/nautilo/trc/trc/static/documentos/ventas.csv"
archivo_busqueda="/home/nautilo/trc/trc/busqueda.csv"
h = datetime.datetime.now()
hoy = h.strftime("%A %d de %B de %Y").capitalize()
hoypago=h.strftime('%Y-%m-%d')
def app(request,source=archivo_ventas):
    ventas=[]
    o = open(source,"r",encoding="utf-8",newline='')
    for i in o:
        if i!="\r\n" or i!="\n" or i!=["\n"]:
            i=i.split("|") #->|20
            i[20]=i[20].replace("\r\n","")
            i[20]=i[20].replace("\n","")
            x = datetime.datetime.strptime(i[11],'%d/%m/%Y')
            f_oc = datetime.datetime.strptime(i[12],'%d/%m/%Y')
            f_informe = datetime.datetime.strptime(i[13],'%d/%m/%Y')
            f_factura = datetime.datetime.strptime(i[14],'%d/%m/%Y')
            f_cancel = datetime.datetime.strptime(i[15].replace("\n",""),'%d/%m/%Y')
            delta_oc= (f_oc-h).days
            delta_informe=(f_informe-h).days
            delta_factura=(f_factura-h).days
            delta_cancel=(f_cancel-h).days
            i.append(10-delta_oc) #21 
            i.append(10-delta_informe) #22
            i.append(5-delta_factura) #23
            i.append(30-delta_cancel) #24
            if delta_oc>0:   #demostrar
                i.append(True) #25
            else:
                i.append(False)
            if delta_factura>0:
                i.append(True) #26
            else:
                i.append(False)
            if i[16]!="0":
                i.append(True) #27 arx
            else:
                i.append(False)
            if i[17]!="0":
                i.append(True) #28 arx
            else:
                i.append(False)
            if i[18]!="0":
                i.append(True) #29 arx
            else:
                i.append(False)
            if i[19][0]!="0":
                i.append(True) #30 arx
            else:
                i.append(False)
            if i[20]=="0":
                i.append(False) #31 fac
            else:
                i.append(True)  
            ventas.append(i)
    o.close()      
    dict_ventas={"ventas":ventas,"fecha":hoy,"hoypago":hoypago}
    return render(request,"index.html",dict_ventas)
def agregar(request):
    x = datetime.datetime.now()
    hoy = f"{x.day}/{x.month}/{x.year}"
    ventas=[]
    o = open(archivo_ventas,"r",encoding="utf-8")
    for i in o:
        ventas.append(i)
    nro = str(len(ventas)+1)
    o.close()
    cliente="%r"%request.GET["cliente"]
    solicitante="%r"%request.GET["solicitante"]
    n_ast_o_diag="%r"%request.GET["n_ast_o_diag"]
    n_cotizacion="%r"%request.GET["n_cotizacion"]
    n_oc="%r"%request.GET["n_oc"]
    fecha_ast="%r"%request.GET["fecha_ast"]
    informe="%r"%request.GET["informe"]
    n_factura="%r"%request.GET["n_factura"]
    n_guia="%r"%request.GET["n_guia"]
    cancel_doc="%r"%request.GET["cancel_doc"]
    f_oc =x+datetime.timedelta(days=10)
    f_informe=x+datetime.timedelta(days=10)
    f_factura=f_oc+datetime.timedelta(days=5)
    f_cancel=f_factura+datetime.timedelta(days=30)
    f_oc = f"{f_oc.day}/{f_oc.month}/{f_oc.year}"
    f_informe = f"{f_informe.day}/{f_informe.month}/{f_informe.year}"
    f_factura = f"{f_factura.day}/{f_factura.month}/{f_factura.year}"
    f_cancel = f"{f_cancel.day}/{f_cancel.month}/{f_cancel.year}"
    venta = f"{nro}|{cliente}|{solicitante}|{n_cotizacion}|{n_oc}|{n_ast_o_diag}|{fecha_ast}|{informe}|{n_guia}|{n_factura}|0|{hoy}|{f_oc}|{f_informe}|{f_factura}|{f_cancel}|0|0|0|0|0\n".replace("'","")
    with open(archivo_ventas,'a',encoding="utf-8",newline='') as file:
        if venta!="\n" or venta!="\r\n":
            file.write(venta)
    file.close()   
    return app(request)
def borrar(request):
    form=request.GET
    lista_seleccionados=[]
    text=[]
    for i in form:
        lista_seleccionados.append(i)
    o = open(archivo_ventas,"r",encoding="utf-8")
    for i in o:
        a=i.split("|")
        if a[0] not in lista_seleccionados:
            text.append(f"{i}")
    o.close()
    with open(archivo_ventas,'w',encoding="utf-8") as file:
        for line in text:
            file.write(line)
    file.close()   
    return app(request)
def archivos(request):
    form=request.GET
    for key,value in form.items():
        if value!="":
            for r,d,f in os.walk('C:/Users/TRC Equipos'):
                if "Dropbox" in d:
                    d.remove("Dropbox")
                if ".vscode" in d:
                    d.remove(".vscode")
                for files in f:
                    if files == value:
                        direccion=os.path.join(r,files)
                        if key[1:]=='n_cotizacionA':
                            url_cotiz= value
                            shutil.copy2(direccion,  f'C:/Program Files/trc_ventas/trc/trc/static/documentos/cotizaciones/{value}')
                        if key[1:]=='n_ocA':
                            url_oc= value
                            shutil.copy2(direccion, f'C:/Program Files/trc_ventas/trc/trc/static/documentos/órdenes de compra/{value}')
                        if key[1:]=='informeA':
                            url_informe = value
                            shutil.copy2(direccion,f'C:/Program Files/trc_ventas/trc/trc/static/documentos/informes técnicos/{value}')
                        if key[1:]=='n_facturaA':
                            url_factura=value
                            shutil.copy2(direccion, f'C:/Program Files/trc_ventas/trc/trc/static/documentos/facturas/{value}')
    text = []
    o = open(archivo_ventas,"r",encoding="utf-8")
    u=0
    for i in o:
        if i!="\n" or i!="\r\n":
            u+=1
            line=f"{u}|"
            i=i.split("|")
            i[20]=i[20].replace("\n","")
            if f'{u}n_cotizacionA' in form:
                if form[f'{u}n_cotizacionA']!="":
                    i[16]=url_cotiz
                else:
                    i[16]="0"
            if f'{u}n_ocA' in form:
                if form[f'{u}n_ocA']!="":
                    i[17]=url_oc
                else:
                    i[17]="0"
            if f'{u}informeA' in form:
                if form[f'{u}informeA']!="":
                    i[18]=url_informe
                else:
                    i[18]="0"
            if f'{u}n_facturaA' in form:
                if form[f'{u}n_facturaA']:
                    i[19]=url_factura
                else:
                    i[19]="0"
            if f'{u}borrar_cotiz' in form and form[f'{u}borrar_cotiz']=='on':
                i[16]="0" 
            if f'{u}borrar_oc' in form and form[f'{u}borrar_oc']=='on':
                i[17]="0" 
            if f'{u}borrar_informe' in form and form[f'{u}borrar_informe']=='on':
                i[18]="0" 
            if f'{u}borrar_factura' in form and form[f'{u}borrar_factura']=='on':
                i[19]="0" 
            line+=f"{i[1]}|{i[2]}|{i[3]}|{i[4]}|{i[5]}|{i[6]}|{i[7]}|{i[8]}|{i[9]}|{i[10]}|{i[11]}|{i[12]}|{i[13]}|{i[14]}|{i[15]}|{i[16]}|{i[17]}|{i[18]}|{i[19]}|{i[20]}\n"   
            text.append(line)
            line=""
    o.close()
    with open(archivo_ventas,'w',encoding="utf-8") as file:
        for line in text:
            if line!="\n" or line!="\r\n":
                file.write(line)
    file.close()   
    return app(request)
def editar(request):
    form=request.GET
    text = []
    o = open(archivo_ventas,"r",encoding="utf-8")
    u=0
    for i in o:
        if i!="\n" or i!="\r\n":
            u+=1
            line=f"{u}|"
            keys=[f"{u}clienteN",f"{u}solicitanteN",f"{u}n_cotizacionN",f"{u}n_ocN",f"{u}n_ast_o_diagN",f"{u}fecha_astN",f"{u}informeN",f"{u}n_guiaN",f"{u}n_facturaN",f"{u}cancel_docN"]
            i=i.split("|")
            i[20]=i[20].replace("\n","")
            if f'{u}banco' in form:
                a=f"{form[f'{u}pago']}".split("-")
                a=f"{a[2]}-{a[1]}-{a[0]}"
                if form[f'{u}banco'] == "1":
                    i[10]=f"BCI ({a})"
                elif form[f'{u}banco'] == "2":
                    i[10]=f"Banco Estado ({a})"
            if f'{u}fechafac' in form and f'{u}cancelfac' in form and form[f'{u}cancelfac']=='on':
                cancel_fac=f"{form[f'{u}fechafac']}".split("-")
                cancel_fac=f"{cancel_fac[2]}-{cancel_fac[1]}-{cancel_fac[0]}"
                i[9]+=f"({cancel_fac})"
                i[20] = "1"
            if f'{u}fechaast' in form and f'{u}cancelast' in form and form[f'{u}cancelast']=='on':
                cancel_ast=f"{form[f'{u}fechaast']}".split("-")
                cancel_ast=f"{cancel_ast[2]}-{cancel_ast[1]}-{cancel_ast[0]}"
                i[6]=f"({cancel_ast})"
            if f'{u}fechacot' in form and f'{u}cancelcot' in form and form[f'{u}cancelcot']=='on':
                cancel_cot=f"{form[f'{u}fechacot']}".split("-")
                lista_fecha=cancel_cot
                for k in lista_fecha:
                    if k[0]=="0":
                        lista_fecha[lista_fecha.index(k)]=k.replace("0","") 
                nhoystr=f"{lista_fecha[2]}/{lista_fecha[1]}/{lista_fecha[0]}"
                x = datetime.datetime.strptime(nhoystr,'%d/%m/%Y')
                fecha=x.strftime("%A %d de %B de %Y").capitalize()
                cot_p="" #Lo que va escrito en el elemento <p> de la cotización
                parentesis=False
                for k in i[3]:
                    if parentesis == False and k not in ["(",")"]:
                        cot_p+=k
                    if k=="(":
                        parentesis=True
                    if k==")":
                        parentesis=False
                i[3]=f"{cot_p}({fecha})"
                f_oc =x+datetime.timedelta(days=10)
                f_informe=x+datetime.timedelta(days=10)
                f_factura=f_oc+datetime.timedelta(days=5)
                f_cancel=f_factura+datetime.timedelta(days=30)
                f_oc = f"{f_oc.day}/{f_oc.month}/{f_oc.year}"
                f_informe = f"{f_informe.day}/{f_informe.month}/{f_informe.year}"
                f_factura = f"{f_factura.day}/{f_factura.month}/{f_factura.year}"
                f_cancel = f"{f_cancel.day}/{f_cancel.month}/{f_cancel.year}"
                i[11]=nhoystr
                i[12]=f_oc
                i[13]=f_informe
                i[14]=f_factura
                i[15]=f_cancel   
            for k in keys:
                if k in form:
                    line+=f"{form[k]}|".replace("\r\n","")
                else:
                    line+=f"{i[keys.index(k)+1]}|"
            line+=f"{i[11]}|{i[12]}|{i[13]}|{i[14]}|{i[15]}|{i[16]}|{i[17]}|{i[18]}|{i[19]}|{i[20]}\n"   
            text.append(line)
            line=""
    o.close()
    with open(archivo_ventas,'w',encoding="utf-8") as file:
        for line in text:
            if line!="\n" or line!="\r\n":
                file.write(line)
    file.close()   
    return app(request)
def buscar(request):
    busqueda="%r"%request.GET["busqueda"]
    busqueda=busqueda.strip().lower().replace("'","")
    if busqueda!="":
        o = open(archivo_ventas,"r",encoding="utf-8")
        text=[]
        for i in o:
            p=i
            i=i.replace("\n","").strip().lower()
            if i.count(busqueda)!=0:
                text.append(p)
        o.close()
        with open(archivo_busqueda,'w',encoding="utf-8") as file:
            for line in text:
                file.write(line)
        file.close()
        return app(request,archivo_busqueda)    
    else:
        return app(request)