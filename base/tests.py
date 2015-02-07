from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from datetime import date, timedelta

from templatetags.account_format import eligible, BizzFuzz, _13_years
from models import Account


class AccountTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.account = Account(username='test', birthday='2001-01-01')
        self.account.save()
    
    def check_post_response(self, url, data={}):
        response = self.client.post(url, data)
        self.failUnlessEqual(response.status_code, 302) 
        return response      

    def post_template_response(self, url, template, data):
        response = self.client.post(url)
        self.assertTemplateUsed(response, template)
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')        
        return self.check_post_response(url, data)
    
    def get_template_response(self, url, template):
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template)
        return response
        
    def test_list(self):
        response = self.get_template_response(reverse('account-list'),
                                     'base/account_list.html')
        for i in Account.objects.all():
            self.assertContains(response, i)
            self.assertContains(response, i.random_number)

    def test_detail(self):
        url = reverse('account-detail', args=[self.account.id])
        template = 'base/account_detail.html'
        response = self.get_template_response(url, template)
        self.assertContains(response, self.account)
        self.assertContains(response, self.account.random_number)

    def test_edit(self):
        url = reverse('account-edit', args=[self.account.id])
        template = 'base/account_form.html'
        self.get_template_response(url, template)
        
        response = self.post_template_response(url, template,
            {'username': self.account.username,
            'birthday': self.account.birthday,
            'random_number': self.account.random_number })
        self.assertRedirects(response,
            reverse('account-detail', args=[self.account.id]))        

    def test_create(self):
        url = reverse('account-add')
        template = 'base/account_form.html'
        self.get_template_response(url, template)
        
        self.post_template_response(url, template,
            {'username': 'test2', 'birthday': '2014-01-01'})
        
    def test_delete(self):
        url = reverse('account-delete', args=[self.account.id])
        self.get_template_response(url, 'base/account_confirm_delete.html')
    
        response = self.check_post_response(url)
        self.assertRedirects(response, reverse('account-list')) 
        
    def test_eligible(self):
        today = date.today()
        self.assertEqual(eligible(today), 'blocked')
        self.assertEqual(
            eligible(today - timedelta(days=_13_years)), 'allowed')
   
    def test_BizzFuzz(self):
        self.assertEqual(BizzFuzz(6), 'Bizz')
        self.assertEqual(BizzFuzz(10), 'Fuzz')
        self.assertEqual(BizzFuzz(15), 'BizzFuzz')
        self.assertEqual(BizzFuzz(98), 98)
 