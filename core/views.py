from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.utils import Api
from rest_framework import status

@api_view()
def get_supported_currencies(request):
    api = Api()
    return Response(api.supported_currencies)


@api_view()
def get_plot_data(request):
    api=Api()
    base = request.GET.get('base')
    target = request.GET.get('target')
    start_at = request.GET.get('start_at')
    end_at = request.GET.get('end_at')
    response = api.get_rates(base=base,target_list=[target], start_date=start_at, end_date= end_at)

    try:
        rates_by_date = response['rates']
        hist_data = []
        for key, value in rates_by_date.items():
            hist_dict = {'date': key, 'exchange_rate': value[target]}
            hist_data.append(hist_dict)
        hist_data.sort(key = lambda x:x['date'])

        return Response(hist_data)
    except:
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view()
def get_latest(request):
    api = Api()
    resp = api.get_rates()["rates"]
    data = []
    for key, value in resp.items():
        dictx = {'symbol':key, 'rate': value}
        data.append(dictx)
    return Response(data)

@api_view(['GET'])
def get_symbols_with_countries(request):
    api = Api()
    return Response(api.get_currencies_with_countries())



