from django.shortcuts import render
from .main_process import total_process

def predictor_demanda(request):
    return render(request, 'predictor_demanda.html')

def notebooks_view(request):
    process_notebooks = total_process('notebooks')
    top10 = process_notebooks.head(10)
    # Pasa el dataframe top10 al contexto del template como un diccionario
    context = {
        'top10_data': top10.to_dict(orient='records'),
        'product_name': 'Notebooks'
    }
    return render(request, 'product.html', context)

def tablets_view(request):
    process_tablets = total_process('tablets')
    top10 = process_tablets.head(10)
    # Pasa el dataframe top10 al contexto del template como un diccionario
    context = {
        'top10_data': top10.to_dict(orient='records'),
        'product_name' : 'Tablets'
    }
    return render(request, 'product.html', context)

def pcs_view(request):
    process_pcs = total_process('pcs')
    top10 = process_pcs.head(10)
    # Pasa el dataframe top10 al contexto del template como un diccionario
    context = {
        'top10_data': top10.to_dict(orient='records'),
        'product_name' : 'PCs'
    }
    return render(request, 'product.html', context)

def impresoras_view(request):
    process_impresoras = total_process('impresoras')
    top10 = process_impresoras.head(10)
    # Pasa el dataframe top10 al contexto del template como un diccionario
    context = {
        'top10_data': top10.to_dict(orient='records'),
        'product_name' : 'Impresoras'
    }
    return render(request, 'product.html', context)