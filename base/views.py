import csv
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from models import Account
from templatetags.account_format import eligible, BizzFuzz


class AccountDetailView(DetailView):
   model = Account


class AccountUpdateView(UpdateView):
    model = Account
    fields = ['username', 'birthday', 'random_number']


class AccountListView(ListView):
    model = Account


class AccountDeleteView(DeleteView):
    model = Account
    success_url = reverse_lazy('account-list')


class AccountCreateView(CreateView):
    model = Account
    fields = ['username', 'birthday']


class CSVResponseMixin(TemplateView):
    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        writer = csv.writer(response)
        writer.writerow(
            ['Username', 'Birthday', 'Eligible', 'Random Number', 'BizzFuzz'])
        for i in Account.objects.all():
            writer.writerow([i.username, i.birthday.strftime("%m/%d/%Y"),
                eligible(i.birthday), i.random_number,
                BizzFuzz(i.random_number)])

        return response
